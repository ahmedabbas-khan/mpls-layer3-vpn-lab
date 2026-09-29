# 8. Study guide: revision and exam practice

## Cheat sheet

| Ask yourself | Answer |
|--------------|--------|
| Who forwards by label, who does not? | R2, R3, R4 forward by MPLS label. R1 and R5 are plain IP routers |
| Which router never sees a customer route? | R3, the P router |
| What makes routes from two customers with the same address safe to carry? | The Route Distinguisher, prepended to every VRF route |
| What decides which VRF a route is allowed into? | The Route Target: export tags it, import accepts it |
| Where does OSPF 10 run for the Head Office? | On R1, and on R2 inside VRF A |
| Where does OSPF 1 run? | Only on R2, R3, R4, in the provider core |
| What protocol carries VPN routes between R2 and R4? | MP-BGP, address family VPNv4 |
| Why does the address disappear after `ip vrf forwarding`? | The interface leaves the global table, so its old Layer 3 setting is cleared |
| What is Penultimate Hop Popping? | The second to last router (R3) removes the outer MPLS label before the last hop, to save the last router work |

## Common mistakes to avoid in an exam

1. Writing `route-target import` and forgetting `route-target export` also exists (or forgetting that the plain `route-target X:Y` line means both).
2. Putting the customer's network in OSPF 1 (the core process) by mistake. It must stay out of the core and only appear inside a VRF's own OSPF process.
3. Forgetting `subnets` on `redistribute bgp 10 subnets`, which silently drops /32 and other subnetted routes.
4. Forgetting `send-community extended`, so the route-target never reaches the other PE and the import rule has nothing to match.
5. Typing the interface's IP address before `ip vrf forwarding` instead of after. The VRF command must come first.
6. Believing R3 needs an IP VRF too. It does not: R3 only runs OSPF 1 and MPLS.

## Practice questions

**Q1. Why do both customer sites use OSPF process number 10 without conflict?**
An OSPF process number is local to one router; it is not exchanged with neighbours. VRF A and VRF B are separate routing tables on separate (or the same) router, so process 10 in VRF A and process 10 in VRF B never mix.

**Q2. R2 can ping 1.1.1.1 successfully with `ping vrf A 1.1.1.1` but not with a plain `ping 1.1.1.1`. Why?**
The interface toward R1 was moved into VRF A. Its route lives only in VRF A's table. A plain `ping` searches the global table, which no longer has that route.

**Q3. What two labels does a Head Office to Branch packet carry while it crosses R3, and which one does R3 read?**
It carries an outer MPLS label and an inner VPN label. R3 reads and pops only the MPLS label; it never inspects the VPN label.

**Q4. Which single command, if left out on R4, would prevent R5 from ever learning the Head Office routes, even though R4 itself already has them in BGP?**
`redistribute bgp 10 subnets` inside `router ospf 10 vrf B` on R4.

**Q5. What is the purpose of `update-source Loopback0` in the BGP configuration?**
It makes the router use its loopback address as the source of the BGP session, rather than the address of whichever physical interface happens to be used. Because the loopback stays up as long as the router is up, the session survives if one physical link fails and another path to the loopback exists.

**Q6. Why must `mpls ip` NOT be configured on R2's Serial1/0 (the link to R1)?**
That link carries plain customer traffic, not core traffic. MPLS is only needed for the provider's own core links between R2, R3 and R4.
