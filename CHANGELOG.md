# Changelog

All notable changes to this project are listed here.

## [1.0.0] 2026-09-28

### Added
- Complete five-router MPLS Layer 3 VPN lab: OSPF core, MPLS/LDP, two VRFs, OSPF to the customers, MP-BGP VPNv4 between the PEs, and route-target import for site to site reachability.
- Final configuration for each router in `configs/`, with every port address and `no shutdown`.
- Machine readable addressing plan `configs/addressing.csv`.
- `tools/validate_configs.py` to check addresses, links, BGP and VRF design, plus a GitHub Actions workflow that runs it.
- Documentation in `docs/`: concepts, design, step by step guide, verification with expected output, troubleshooting, command reference, corrections log and study guide.
- Both topology diagrams and 48 output screenshots in `images/`.
- Word study notes in `docs/Study-Notes-MPLS-L3VPN.docx`.

### Fixed
- Commands that were run together or shortened in the original lab sheet are written in correct full form (see `docs/07-command-corrections.md`).
