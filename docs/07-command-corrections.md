# 7. Corrections made to the original lab sheet

The lab was originally written as a document with screenshots. Every command in it was checked against this repository. Most of the problems are missing spaces (the text was run together when the document was made) and a few shortened words. They would be rejected or misread if typed exactly as printed. The corrected form is what appears everywhere in `configs/` and in the guide.

| As printed | Correct command | What was wrong |
|------------|-----------------|-----------------|
| `ipcef` | `ip cef` | Missing space. IOS replies "Unrecognized command" |
| `mplsip` | `mpls ip` | Missing space (both the global and the interface command) |
| `mplsldp router-id lo0` | `mpls ldp router-id Loopback0` | Missing space. `lo0` works as a short name, `Loopback0` is written out for clarity |
| `ipvrf A`, `ipvrf B` | `ip vrf A`, `ip vrf B` | Missing space |
| `ipvrf forwarding A` | `ip vrf forwarding A` | Missing space |
| `ip add 1.1.1.2 255.0.0.0` | `ip address 1.1.1.2 255.0.0.0` | Shortened word. Works on the router, written in full here |
| `network ... a 0` | `network ... area 0` | Shortened word. Works, written in full here |
| `int s 1/1`, `int serial 1/0` | `interface Serial1/1`, `interface Serial1/0` | Shortened word. Works, written in full here |
| `update-source lo0` | `update-source Loopback0` | Short name, written in full |
| `exit` immediately inside `address-family` | `exit-address-family` | `exit` also works, but `exit-address-family` is the command meant for this |
| `show ip bgp vpnv4 vrf B label` | `show ip bgp vpnv4 vrf B labels` | The keyword is `labels`. Both were accepted in the original screenshot, but the full word is safest |
| `ping 55.5.5.5 source loopback 0` | `ping 55.5.5.5 source Loopback0` | Written in full to match interface naming used elsewhere |
| No interface addresses shown at all | Full `ip address` and `no shutdown` added for every port | The original document jumped straight to step 5.1 and never listed the address commands. Step 5.0 in this repository adds them for all five routers |

## What was already correct

The design itself was right in the original lab:

* The RD and RT values (12:1 / 1:1 for VRF A, 12:2 / 1:2 for VRF B).
* `route-target import 1:2` on VRF A and `route-target import 1:1` on VRF B.
* `send-community extended` on both BGP neighbours.
* `redistribute ospf 10 match internal external 1 external 2`.
* `redistribute bgp 10 subnets`.

## One thing to remember when comparing screenshots

**Label numbers change.** The LFIB screenshot taken at step 5.2 and the one taken again at step 5.10 show different numbers for the same prefix (for example, the label for 44.4.4.4/32 on R2). This is normal: labels are handed out again whenever LDP restarts or a session resets. Always read the label from the table you are currently looking at, never memorise a specific number as fixed.

A small related note: if LDP is already running when you change a router's ID, add `force` (`mpls ldp router-id Loopback0 force`) so the change takes effect immediately. In this lab LDP was not running yet when the ID was set, so `force` was not needed.
