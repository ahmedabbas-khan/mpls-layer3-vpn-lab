# 6. Command reference

Every command used in this lab, grouped by purpose, with a one line meaning. Full syntax always starts from global configuration mode unless noted.

## Interfaces and basic IP

| Command | Meaning |
|---------|---------|
| `hostname NAME` | Set the router's name |
| `interface TYPE NUMBER` | Enter configuration for one port, e.g. `interface Serial1/0` |
| `ip address A.B.C.D MASK` | Give the interface an address |
| `no shutdown` | Turn the interface on (interfaces start off) |
| `description TEXT` | A label for humans reading the config, has no effect on traffic |
| `show ip interface brief` | One line per interface: address and up/down state |
| `show ip route` | The router's main (global) routing table |

## OSPF

| Command | Meaning |
|---------|---------|
| `router ospf PROCESS-ID` | Start or enter an OSPF process. The process ID is only local to the router |
| `router ospf PROCESS-ID vrf NAME` | Same, but the process runs inside a VRF |
| `network A.B.C.D WILDCARD area N` | Put every interface matching the address and wildcard into that OSPF area |
| `redistribute bgp AS subnets` | Bring BGP routes into this OSPF process. `subnets` is required for subnetted and /32 routes |
| `show ip ospf neighbor` | List OSPF neighbours and their state |

## MPLS and LDP

| Command | Meaning |
|---------|---------|
| `ip cef` | Turn on Cisco Express Forwarding, required for MPLS |
| `mpls ip` (global) | Enable MPLS on the router |
| `mpls ip` (interface) | Enable label switching on this interface |
| `mpls label protocol ldp` | Choose LDP as the label distribution protocol |
| `mpls ldp router-id Loopback0` | Use this loopback as the router's LDP identity |
| `show mpls ldp neighbor` | List LDP neighbours |
| `show mpls forwarding-table` | The LFIB: local label, outgoing label, prefix, outgoing interface |

## VRF

| Command | Meaning |
|---------|---------|
| `ip vrf NAME` | Create a VRF (a private routing table) |
| `rd ASN:NUMBER` | Set the Route Distinguisher, makes routes from this VRF unique |
| `route-target export ASN:NUMBER` | Tag routes leaving this VRF with this value |
| `route-target import ASN:NUMBER` | Accept incoming routes carrying this tag |
| `route-target ASN:NUMBER` | Shortcut for both export and import at once |
| `ip vrf forwarding NAME` | Move an interface into a VRF (this erases its IP address) |
| `show ip vrf` | List VRFs and their interfaces |
| `show ip route vrf NAME` | Routing table of one VRF |
| `ping vrf NAME ADDRESS` | Ping using one VRF's table instead of the global table |

## BGP

| Command | Meaning |
|---------|---------|
| `router bgp ASN` | Start BGP with this AS number |
| `no synchronization` | Do not wait for IGP to carry a route before advertising it in BGP |
| `no auto-summary` | Do not automatically summarise routes to their classful boundary |
| `neighbor ADDRESS remote-as ASN` | Define a BGP neighbour. Same ASN as mine means iBGP |
| `neighbor ADDRESS update-source Loopback0` | Use the loopback, not a physical address, as the local end of the session |
| `address-family vpnv4` | Enter the section for VPN routes (RD + address + label) |
| `address-family ipv4 vrf NAME` | Enter the section for one VRF's own IPv4 routes |
| `neighbor ADDRESS activate` | Turn on this address family for that neighbour |
| `neighbor ADDRESS send-community extended` | Send the route-target tag along with each route |
| `redistribute ospf PROCESS match internal external 1 external 2` | Bring in every kind of OSPF route from that VRF |
| `exit-address-family` | Leave an address family section |
| `show ip bgp summary` | List BGP neighbours and session state |
| `show ip bgp vpnv4 all` | All VPNv4 routes known to this router |
| `show ip bgp vpnv4 vrf NAME labels` | VPNv4 routes for one VRF, with their labels |

## Verification

| Command | Meaning |
|---------|---------|
| `ping ADDRESS` | Test reachability using the global table |
| `ping ADDRESS source Loopback0` | Ping using the loopback as the source address |
| `traceroute ADDRESS` | Show every router hop on the way to a destination |
