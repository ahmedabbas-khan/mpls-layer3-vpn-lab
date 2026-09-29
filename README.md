# MPLS Layer 3 VPN Lab — HBL Head Office and Branch

[![Validate lab files](https://github.com/ahmedabbas-khan/mpls-layer3-vpn-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/ahmedabbas-khan/mpls-layer3-vpn-lab/actions/workflows/validate.yml)
![Platform](https://img.shields.io/badge/platform-Cisco%20IOS%20%7C%20GNS3-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A five router **MPLS Layer 3 VPN** built and documented from scratch: two customer sites (HBL Head Office and HBL Branch) reach each other privately across a shared provider core, using OSPF, MPLS/LDP, VRFs, and MP-BGP (VPNv4).

> Built and documented by **Ahmed Abbas** — IT student (Networking), Bahauddin Zakariya University, Multan. Part of a personal Cisco lab portfolio alongside [`cisco-secure-acs-aaa-lab`](https://github.com/ahmedabbas-khan/cisco-secure-acs-aaa-lab) and [`intro-to-networking-labs`](https://github.com/ahmedabbas-khan).

## Topology

![Logical topology](images/topology-logical.png)

R1 and R5 are the two customer sites. **R2 and R4 are Provider Edge (PE)** routers, each holding one VRF. **R3 is a core (P) router** that runs no VRF and no BGP — it forwards every packet by MPLS label alone and never sees a single customer route.

| Router | Role | Runs |
|--------|------|------|
| R1 | CE — HBL Head Office | OSPF 10 |
| R2 | PE — owns VRF A | OSPF 1, MPLS/LDP, VRF A, OSPF 10 in VRF, MP-BGP |
| R3 | P — provider core | OSPF 1, MPLS/LDP only |
| R4 | PE — owns VRF B | OSPF 1, MPLS/LDP, VRF B, OSPF 10 in VRF, MP-BGP |
| R5 | CE — HBL Branch | OSPF 10 |

## Why this design

* **Privacy.** Each site's routes live in their own VRF (virtual routing table), tagged with a unique Route Distinguisher, so two customers could even reuse the same IP addresses without conflict.
* **A lean core.** The provider's own routers (R3 especially) never learn a customer route — every core to core packet is forwarded purely by MPLS label. Proven directly in [`docs/04-verification.md`](docs/04-verification.md).
* **Controlled reachability.** Sites only reach each other because their VRFs explicitly **import** each other's Route Target — nothing crosses by accident.

## Repository layout

```
mpls-layer3-vpn-lab/
├── configs/                    Final router configurations, ready to paste
│   ├── R1.cfg  R2.cfg  R3.cfg  R4.cfg  R5.cfg
│   ├── addressing.csv          Machine-readable IP addressing plan
│   └── README.md               How to load a config, why route-targets expand
├── docs/
│   ├── 01-concepts.md          MPLS VPN theory from zero, in plain English
│   ├── 02-design-and-addressing.md   Topology, addressing table, OSPF cost math
│   ├── 03-configuration-guide.md     All 10 steps, commands + expected output
│   ├── 04-verification.md      One packet traced hop by hop, label by label
│   ├── 05-troubleshooting.md   Symptom → command to check → likely cause
│   ├── 06-command-reference.md Every command used, grouped, one line each
│   ├── 07-command-corrections.md  Fixes to the original lab sheet's commands
│   ├── 08-study-guide.md       Cheat sheet, common mistakes, practice Q&A
│   └── Study-Notes-MPLS-L3VPN.docx  Full illustrated Word write-up
├── images/                     Both topology diagrams + 48 output screenshots
├── tools/
│   └── validate_configs.py     Checks addressing, configs, BGP and VRF design
└── .github/workflows/validate.yml   Runs the validator on every push
```

## Quick start (GNS3 / Cisco IOS)

1. Build the topology in GNS3 exactly as shown above (five routers, links per the table in [`docs/02-design-and-addressing.md`](docs/02-design-and-addressing.md)).
2. For each router, open its console and paste the matching file from [`configs/`](configs/):
   ```
   enable
   configure terminal
   <paste the file>
   end
   write memory
   ```
3. Give OSPF, LDP and BGP a minute or two to converge.
4. Verify:
   ```
   R1#ping 55.5.5.5 source Loopback0
   R5#ping 11.1.1.1 source Loopback0
   ```
   Both should succeed at 100 percent. Full expected output for every step is in the docs.

## Validate the files yourself

```bash
python tools/validate_configs.py
```

Checks that every interface address agrees between `configs/*.cfg` and `configs/addressing.csv`, that both ends of every link share a network, that R2 and R4's BGP neighbours and VRF route-targets are consistent, and that R3 (the P router) carries no VRF or BGP configuration. Runs automatically on every push via GitHub Actions.

## Read the write-up

Start with [`docs/01-concepts.md`](docs/01-concepts.md) if MPLS VPNs are new to you — it explains CE/PE/P, RD, RT and MP-BGP with a courier analogy before any configuration appears. Then follow [`docs/03-configuration-guide.md`](docs/03-configuration-guide.md) step by step, and use [`docs/04-verification.md`](docs/04-verification.md) to see exactly how one packet is labelled, forwarded and delivered. A fully illustrated Word version of the same material is in [`docs/Study-Notes-MPLS-L3VPN.docx`](docs/Study-Notes-MPLS-L3VPN.docx).

## Tools used

Cisco IOS (routers), GNS3 (topology emulation), Python 3 (validation script), GitHub Actions (CI).

## License

[MIT](LICENSE) — free to use for learning or teaching, with attribution appreciated.
