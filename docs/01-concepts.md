# 1. Concepts from zero

This page explains the idea behind an MPLS Layer 3 VPN in plain English. If you read only one page before the configuration, read this one.

## The problem

HBL has a **Head Office** and a **Branch** in different places. They must reach each other as if they shared one private network. The cables between them belong to a **provider** (a telecom company) that also carries traffic for many other customers.

Two things must be true:

1. **Privacy.** The provider must keep every customer separate, even if two customers use the same IP addresses.
2. **Simplicity in the middle.** The provider's core routers should not need to know every route of every customer.

An MPLS Layer 3 VPN solves both.

## The courier analogy

The provider is a courier company. The Head Office hands over a parcel (an IP packet) for the Branch. The courier puts it in an envelope and sticks **two stickers** on it:

| Sticker | Real name | What it tells the depots |
|---------|-----------|--------------------------|
| Inner sticker | **VPN label** | Which customer shelf the parcel belongs to (VRF A or VRF B). Only the last depot reads it. |
| Outer sticker | **MPLS label** | Which road to take to reach the last depot. The middle depots read only this one. |

The middle depot (R3) never opens the envelope, so it never needs to know customer addresses.

## The words you must know

| Word | Plain English | In this lab |
|------|---------------|-------------|
| **CE** (Customer Edge) | The customer's own router at the edge of their site | R1 (Head Office), R5 (Branch) |
| **PE** (Provider Edge) | The provider's router that touches the customer. It is the smart one and knows customer routes | R2 and R4 |
| **P** (Provider) | A router inside the provider core. It only swaps labels | R3 |
| **MPLS** | Forwarding by a short label instead of reading the full IP address at every hop | R2, R3, R4 |
| **LDP** | The protocol neighbours use to say "for network X, use label Y" | Between R2 and R3, and R3 and R4 |
| **LFIB** | The label table of a router. Shown with `show mpls forwarding-table` | R2, R3, R4 |
| **VRF** | A private routing table inside one router, like a virtual router. One per customer | VRF A on R2, VRF B on R4 |
| **RD** (Route Distinguisher) | A stamp put in front of a route so two customers with the same address never clash | 12:1 on R2, 12:2 on R4 |
| **RT** (Route Target) | A tag on a route saying who may take it. Export means "I attach this tag". Import means "I accept routes with this tag" | 1:1 Head Office, 1:2 Branch |
| **MP-BGP** (VPNv4) | BGP that can carry VPN routes (RD + address + label) between PEs | R2 and R4, AS 10 |
| **PHP** (Penultimate Hop Popping) | The router before the last one removes the outer label so the last router does less work | R3 pops the label for R4 |

### Memory tricks

* **RD = Route Different.** It makes the route unique.
* **RT = Route Target.** It decides who the route is aimed at.
* **Export = "I am giving away this tag".** **Import = "I will accept this tag".**
* **CE, PE, P.** C is for Customer, P is for Provider, and E is for Edge. The lone P in the middle is the plain core router.

## The two layers of routing

An MPLS VPN is really two networks stacked on top of each other.

| Layer | Who runs it | What it carries |
|-------|-------------|-----------------|
| **Underlay** (the provider core) | OSPF 1 and LDP on R2, R3, R4 | Only the addresses of the provider routers (loopbacks and links) |
| **Overlay** (the customer VPN) | OSPF 10 inside the VRFs, and MP-BGP between the PEs | Customer routes, kept inside the VRFs |

The underlay builds the roads. The overlay decides which parcel goes to which shelf at the end of the road.

## Why loopbacks?

LDP and BGP both use the **loopback** address of a router as their identity.

* A loopback is a virtual port. It never goes down while the router is alive.
* OSPF 1 advertises it, so every core router can reach it.
* BGP sessions built on loopbacks survive a single link failure if another path exists.

That is why the lab types `mpls ldp router-id Loopback0` and `neighbor 44.4.4.4 update-source Loopback0`.

## Why send-community extended?

The Route Target travels inside BGP as an **extended community**. By default a router does not send extended communities to its neighbour. Without `send-community extended` the route-target is lost and the other PE cannot decide which VRF should accept the route.

## Why the IP address disappears after ip vrf forwarding

An interface belongs to one routing table at a time. When you move it into a VRF, IOS clears its Layer 3 settings, because the old address was tied to the global table. You must type the address again, and it must be **after** the `ip vrf forwarding` line.
