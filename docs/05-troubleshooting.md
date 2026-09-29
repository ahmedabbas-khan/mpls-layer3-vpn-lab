# 5. Troubleshooting

A problem, in order of where it sits in the design, with the command that finds it and the usual cause.

| Symptom | Check with | Usual cause |
|---------|-----------|--------------|
| A port shows `administratively down` | `show ip interface brief` | Forgot `no shutdown` (step 5.0) |
| Two adjacent routers can ping the cable but no further | `show ip ospf neighbor` on both ends | OSPF `network` statement wildcard mask is wrong, or the two ends are in different areas |
| `show mpls ldp neighbor` shows nothing between two core routers | `show mpls interfaces` | `mpls ip` was typed globally but forgotten on that interface |
| `ip vrf forwarding` removed the address and it was never re-typed | `show ip interface brief` (shows `unassigned`) | Forgot to type `ip address` again after `ip vrf forwarding` |
| `show ip route vrf A` is empty right after step 5.3 | This is expected | No interface has joined the VRF yet. Continue to step 5.4 |
| `R2#ping 1.1.1.1` fails but `R2#ping vrf A 1.1.1.1` works | Compare `show ip route` and `show ip route vrf A` | Normal. The route lives only inside the VRF, not the global table |
| BGP neighbor stays in `Idle` or `Active`, never `Established` | `show ip bgp neighbor 44.4.4.4` | `update-source Loopback0` missing on one side, loopback not reachable, or the two loopbacks are not in OSPF 1 |
| BGP neighbor bounces Down then Up right after typing `neighbor x activate` | This is expected | Activating a new address family restarts that session once |
| `show ip bgp vpnv4 all` is empty on a PE | `show ip protocols` under `router bgp` | Forgot `redistribute ospf 10 match internal external 1 external 2` inside `address-family ipv4 vrf X` |
| Head Office routes show on R2 but never reach R4 | `show ip vrf` and check RT | Forgot `route-target import` for the other site's tag (step 5.8) |
| R4 has the far site's routes in BGP but R5 never sees them | `show ip route vrf B` | Forgot `redistribute bgp 10 subnets` inside `router ospf 10 vrf B` (step 5.9) |
| A /32 loopback route is missing after BGP to OSPF redistribution | Compare with and without `subnets` | The `subnets` keyword was left off `redistribute bgp 10` |
| R3 shows a customer route in `show ip route` | `show running-config` on R3 | A VRF or BGP command was mistakenly typed on the P router |
| Ping works but is slow or inconsistent | `show mpls forwarding-table`, check for repeated NBRCHG messages | LDP session flapping, often from a flapping link or duplicate router-id |

## General method

1. **Bottom up.** Check physical and IP connectivity first (`show ip interface brief`, a directly connected ping), then OSPF neighbours, then LDP, then BGP, then the VRF routes.
2. **One VRF at a time.** If VRF A works and VRF B does not, compare the two configurations side by side; the fault is almost always a missed line unique to the broken one.
3. **Read the LFIB like a story.** `show mpls forwarding-table` tells you exactly which label goes out which interface. If a label is missing, the two neighbouring LDP routers have not agreed yet.
4. **Use `show ip bgp vpnv4 all` before blaming OSPF.** If the route is not in BGP, no amount of OSPF redistribution on the far side will produce it.
