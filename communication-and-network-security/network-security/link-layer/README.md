# Link layer security

Attacks and controls at layer 2, where an attacker who has plugged into a port or joined the Wi-Fi tries to spoof, flood or hop their way to an on-path position. The switch is where most of these are prevented.

Read [switch security](switch-security.md) first; it is the control home that the attack notes point back to.

## Notes

- [Switch security](switch-security.md): port security, DHCP snooping, DAI, IP Source Guard, BPDU Guard and storm control. The defensive foundation.
- [ARP spoofing](arp-spoofing/README.md): forging ARP to become on-path, with a tested lab showing host resistance and the switch-side fix.
- [MAC flooding](mac-flooding.md): overflowing the MAC table to force a switch to fail open.
- [VLAN hopping](vlan-hopping.md): switch spoofing and double tagging across VLAN boundaries.
- [DHCP attacks](dhcp-attacks.md): rogue DHCP servers and starvation, stopped by DHCP snooping.
- [Network access control and 802.1X](network-access-control-8021x.md): authenticating devices before the port carries traffic.

Scripts: [arp-spoofing/scripts/arp-cache-demo.py](arp-spoofing/scripts/arp-cache-demo.py), used by the ARP spoofing note in the isolated lab.

Back to [Network security](../README.md).
