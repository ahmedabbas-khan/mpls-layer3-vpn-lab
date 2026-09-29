# Router configurations

One file per router. Each file is the **final** state after every step of the lab (5.0 to 5.9), so you can paste a whole file at once instead of typing the steps one by one.

| File | Router | Role | Notes |
|------|--------|------|-------|
| `R1.cfg` | R1 | CE, HBL Head Office | OSPF 10 only |
| `R2.cfg` | R2 | PE, owns VRF A | OSPF 1, LDP, VRF A, OSPF 10 in VRF, MP-BGP |
| `R3.cfg` | R3 | P router (core) | OSPF 1 and LDP only. No VRF, no BGP |
| `R4.cfg` | R4 | PE, owns VRF B | OSPF 1, LDP, VRF B, OSPF 10 in VRF, MP-BGP |
| `R5.cfg` | R5 | CE, HBL Branch | OSPF 10 only |
| `addressing.csv` | all | Addressing plan | Used by the validator |

## How to load a file

1. Open the console of the router in GNS3.
2. Type `enable`, then `configure terminal`.
3. Paste the whole file.
4. Type `end`, then `write memory`.

Load all five routers, then wait one to two minutes for OSPF, LDP and BGP to settle before you test.

## Why the route-targets look longer than in the lab sheet

The lab types `route-target 1:1`. On Cisco IOS that shortcut means **both** export and import, so the running configuration shows two lines. These files write them out in full so you can see the design at a glance:

| VRF | Exports | Imports |
|-----|---------|---------|
| A on R2 | 1:1 | 1:1 and 1:2 |
| B on R4 | 1:2 | 1:2 and 1:1 |

## Check the files

From the repository root:

```bash
python tools/validate_configs.py
```

It confirms that every address in a config matches `addressing.csv`, both ends of each link share a network, and the BGP and VRF settings agree on R2 and R4.
