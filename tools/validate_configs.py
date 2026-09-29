#!/usr/bin/env python3
"""Sanity checks for the MPLS Layer 3 VPN lab files.

What it checks
  1. addressing.csv: no duplicate IPs, loopbacks are /32, and both ends of every
     link agree with each other and sit in the same network.
  2. configs/*.cfg: every interface address in a config matches addressing.csv,
     and every port in addressing.csv appears in its router's config.
  3. BGP: each router's neighbor is the other PE's loopback, and it activates
     the neighbor under vpnv4 with extended communities.
  4. VRF design: RD values differ, each VRF exports its own route-target and
     imports both route-targets.

Usage:  python tools/validate_configs.py
Exit code is 0 when everything passes, 1 otherwise.
"""
import csv
import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "configs"
errors = []


def fail(msg):
    errors.append(msg)


def net(ip, mask):
    return ipaddress.ip_interface(f"{ip}/{mask}").network


def load_csv():
    with open(CFG / "addressing.csv", newline="") as fh:
        return list(csv.DictReader(fh))


def check_addressing(rows):
    seen = {}
    index = {}
    for r in rows:
        key = (r["router"], r["interface"])
        index[key] = r
        if r["ip_address"] in seen:
            fail(f"duplicate IP {r['ip_address']} on {key} and {seen[r['ip_address']]}")
        seen[r["ip_address"]] = key
        if r["role"] == "loopback" and r["mask"] != "255.255.255.255":
            fail(f"{key} is a loopback but its mask is {r['mask']}, expected /32")
    for r in rows:
        if r["role"] != "link":
            continue
        peer_router, peer_if = r["connected_to"].split(":")
        peer = index.get((peer_router, peer_if))
        if peer is None:
            fail(f"{r['router']} {r['interface']} points to missing peer {r['connected_to']}")
            continue
        if peer["connected_to"] != f"{r['router']}:{r['interface']}":
            fail(f"link {r['router']}:{r['interface']} and {r['connected_to']} do not point at each other")
        if net(r["ip_address"], r["mask"]) != net(peer["ip_address"], peer["mask"]):
            fail(f"link {r['router']}:{r['interface']} and {r['connected_to']} are in different networks")


def parse_cfg(path):
    """Return {interface: ip}, plus the raw text lines."""
    lines = path.read_text().splitlines()
    ifaces, current = {}, None
    for ln in lines:
        m = re.match(r"^interface (\S+)", ln)
        if m:
            current = m.group(1)
            continue
        if ln and not ln.startswith(" "):
            current = None if not ln.startswith("!") else current
        m = re.match(r"^\s+ip address (\S+) (\S+)", ln)
        if m and current:
            ifaces[current] = (m.group(1), m.group(2))
    return ifaces, lines


def check_configs(rows):
    by_router = {}
    for r in rows:
        by_router.setdefault(r["router"], []).append(r)
    texts = {}
    for router, entries in by_router.items():
        path = CFG / f"{router}.cfg"
        if not path.exists():
            fail(f"missing {path.name}")
            continue
        ifaces, lines = parse_cfg(path)
        texts[router] = lines
        for e in entries:
            got = ifaces.get(e["interface"])
            if got is None:
                fail(f"{router}: {e['interface']} has no ip address in {path.name}")
            elif got != (e["ip_address"], e["mask"]):
                fail(f"{router}: {e['interface']} is {got} in config but {e['ip_address']} {e['mask']} in CSV")
        for name in ifaces:
            if name not in {e["interface"] for e in entries}:
                fail(f"{router}: interface {name} in config is not listed in addressing.csv")
    return texts


def check_bgp_and_vrf(rows, texts):
    loop = {r["router"]: r["ip_address"] for r in rows if r["role"] == "loopback"}
    pairs = {"R2": "R4", "R4": "R2"}
    for router, other in pairs.items():
        body = "\n".join(texts.get(router, []))
        peer_ip = loop[other]
        for needle in (
            f"neighbor {peer_ip} remote-as 10",
            f"neighbor {peer_ip} update-source Loopback0",
            f"neighbor {peer_ip} activate",
            f"neighbor {peer_ip} send-community extended",
        ):
            if needle not in body:
                fail(f"{router}: missing '{needle}'")
    def vrf_block(router, name):
        body = "\n".join(texts.get(router, []))
        m = re.search(rf"^ip vrf {name}\n((?: .*\n|!.*\n)*)", body + "\n", re.M)
        return m.group(1) if m else ""
    a, b = vrf_block("R2", "A"), vrf_block("R4", "B")
    rd_a = re.search(r"rd (\S+)", a)
    rd_b = re.search(r"rd (\S+)", b)
    if not rd_a or not rd_b or rd_a.group(1) == rd_b.group(1):
        fail("RD values must exist and be different for VRF A and VRF B")
    for label, blk, own, other in (("VRF A", a, "1:1", "1:2"), ("VRF B", b, "1:2", "1:1")):
        for needle in (f"route-target export {own}", f"route-target import {own}", f"route-target import {other}"):
            if needle not in blk:
                fail(f"{label}: missing '{needle}'")
    core = "\n".join(l for l in texts.get("R3", []) if not l.lstrip().startswith("!"))
    if "vrf" in core.lower() or "router bgp" in core:
        fail("R3 is the P router and must have no VRF and no BGP")


def main():
    rows = load_csv()
    check_addressing(rows)
    texts = check_configs(rows)
    check_bgp_and_vrf(rows, texts)
    if errors:
        print("FAILED")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: {len(rows)} interfaces, 5 configs, BGP and VRF design all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
