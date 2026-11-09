# IPv6 security

## Summary

IPv6 is not "IPv4 with longer addresses"; it changes how hosts find each other and configure themselves, and those changes bring their own attacks. Neighbor Discovery (the ICMPv6 replacement for ARP) and router advertisements let any host on a link claim to be a router or hijack an address, much as rogue DHCP and ARP spoofing do in IPv4. The most dangerous and common IPv6 risk, though, is the one people forget: IPv6 is enabled by default on modern systems, so a network secured only for IPv4 often has an unmonitored, unfiltered IPv6 path running in parallel. Securing IPv6 means treating it as a first-class protocol with its own filtering, monitoring and link-layer protections.

## Prerequisites

- [ICMP security](icmp-security.md): ICMPv6 carries Neighbor Discovery.
- [DHCP attacks](../link-layer/dhcp-attacks.md) and [ARP spoofing](../link-layer/arp-spoofing/README.md): the IPv4 analogues.
- Basic IPv6: addresses, link-local addresses, SLAAC.

## Core concepts

### Definition

*IPv6* (RFC 8200) is the current version of the Internet Protocol, with 128-bit addresses and built-in autoconfiguration. Hosts find routers and neighbors using the *Neighbor Discovery Protocol* (NDP, RFC 4861), carried over ICMPv6, and can self-assign addresses using *Stateless Address Autoconfiguration* (SLAAC) based on *Router Advertisement* (RA) messages.

### Analogy

If an IPv4 network is a town where new arrivals ask a central office (DHCP) for an address and look up neighbors by shouting (ARP), an IPv6 town lets arrivals configure their own address from information on public noticeboards (router advertisements) and find neighbors by a politer, built-in directory (NDP). The weakness is the same: the noticeboards and the directory are unauthenticated, so anyone can post a fake "I am the router" notice (rogue RA) and redirect the town's traffic.

The analogy breaks in one important way: in the IPv6 town, every house already speaks the new language by default even if the town council only polices the old one, which is the dual-stack blind-spot problem.

### The main IPv6-specific attacks

| Attack | Mechanism | IPv4 analogue | Defense |
| --- | --- | --- | --- |
| Rogue Router Advertisement | Attacker sends RAs claiming to be the default router; hosts route through them | Rogue DHCP | RA Guard on switches |
| RA flooding | Many forged RAs with different prefixes overwhelm hosts | - | RA Guard, rate limiting |
| Neighbor spoofing | Forged Neighbor Advertisement binds a victim IP to attacker MAC | ARP spoofing | SEND (rare), NDP inspection, RA Guard |
| Rogue DHCPv6 | Fake DHCPv6 server supplies DNS and options | Rogue DHCP | DHCPv6 Guard |
| Dual-stack bypass | IPv6 path unfiltered while IPv4 is secured | - | Equal IPv6 policy and monitoring |

### The dual-stack blind spot

This is the risk that bites real networks. Modern operating systems enable IPv6 by default and often prefer it over IPv4. If the security team has written firewall rules, segmentation, monitoring and detection only for IPv4:

- Hosts may reach the internet over IPv6 with no egress filtering.
- A rogue RA can set up IPv6 connectivity on a supposedly IPv4-only LAN and become on-path, because nothing is watching IPv6 (the SLAAC attack used by tools like the classic "THC-IPv6" suite and MITM frameworks).
- Attackers prefer the unmonitored path.

The fix is not necessarily to disable IPv6 (which can break modern systems and is increasingly the primary protocol), but to give IPv6 the same controls as IPv4: filter it, monitor it, and deploy RA Guard and DHCPv6 Guard on switches. If IPv6 genuinely is not used and not needed, disabling it consistently everywhere is acceptable, but half-disabling it (off on some hosts, on others) is the worst state.

### Why NDP is unauthenticated

Like ARP, NDP trusts the messages on the link. SEND (SEcure Neighbor Discovery, RFC 3971) adds cryptographic protection but is barely deployed because of complexity. In practice the defense is in the switch (RA Guard, DHCPv6 Guard, NDP inspection), mirroring how DAI and DHCP snooping defend IPv4.

## Worked example

Checking whether IPv6 is quietly enabled, the first step in closing the blind spot. On the reference host (2026-10):

```bash
sysctl net.ipv6.conf.all.accept_ra
ip -6 addr show scope global 2>/dev/null | grep -c inet6
```

```text
net.ipv6.conf.all.accept_ra = 1
```

`accept_ra = 1` means the host will accept router advertisements and autoconfigure IPv6 from them, so a rogue RA on this link could give the host an IPv6 default route through an attacker. For a host that should not use IPv6 autoconfiguration, this would be set to `0`; for a host that does use IPv6, the defense belongs on the switch (RA Guard), because the host cannot tell a legitimate RA from a forged one.

Switch-side defenses (reference configuration, not run in the namespace lab):

```text
ipv6 nd raguard policy HOST        ! ports facing hosts must not send RAs
 device-role host
interface range GigabitEthernet0/1 - 24
 ipv6 nd raguard attach-policy HOST
interface GigabitEthernet0/48
 ipv6 nd raguard policy ROUTER     ! the uplink toward the real router may
```

Reading it: access ports are declared "host" ports and any RA appearing on them is dropped, so a rogue RA from an endpoint never reaches other hosts; only the designated router port may originate RAs. This is the IPv6 equivalent of DHCP snooping's trusted/untrusted model.

## Trade offs and when to use it

- **Disable IPv6 vs secure IPv6.** Disabling is simple where IPv6 is truly unused, but it must be consistent and it forgoes a protocol that is now primary in many networks. Securing it (RA Guard, filtering, monitoring) is the forward-looking choice and the only option where IPv6 is in use.
- **RA Guard vs SEND.** RA Guard in the switch is practical and widely deployed; SEND is cryptographically stronger but almost never used due to complexity. Prefer RA Guard.
- **Privacy addresses.** IPv6 privacy extensions (temporary addresses) protect user privacy but complicate tracking a host for security, a trade-off between privacy and attribution.

## Common mistakes

- **Securing IPv4 only on a dual-stack network.** Leaves an unmonitored IPv6 path attackers prefer. Fix: equal IPv6 policy, filtering and monitoring.
- **Half-disabling IPv6.** Inconsistent state is the worst; some hosts still autoconfigure. Fix: either secure IPv6 everywhere or disable it everywhere, consistently.
- **No RA Guard.** A rogue RA becomes the default router. Fix: RA Guard on access ports, DHCPv6 Guard for DHCPv6.
- **Blocking all ICMPv6.** Breaks NDP and path MTU, so IPv6 stops working. Fix: RFC 4890 allow list.
- **Assuming NAT hides IPv6 hosts.** IPv6 commonly has no NAT, so hosts are globally routable; a missing firewall rule exposes them directly. Fix: explicit IPv6 firewall policy.

## Practice

1. Why is "we only secured IPv4" a serious problem on a modern network?
2. What is a rogue Router Advertisement, and which IPv4 attack is it analogous to?
3. Why can hosts not reliably defend themselves against rogue RAs, and where does the defense belong?
4. Why is blocking all ICMPv6 worse than blocking all ICMPv4?
5. When is disabling IPv6 acceptable, and what is the worst middle state?

### Answers

1. IPv6 is enabled and often preferred by default, so an IPv4-only security posture leaves an unfiltered, unmonitored IPv6 path that attackers can use or set up via a rogue RA.
2. A forged RA that claims to be the default router so hosts route through the attacker; it is analogous to a rogue DHCP server in IPv4.
3. NDP and RAs are unauthenticated, so a host cannot distinguish a legitimate RA from a forged one; the defense is RA Guard enforced on the switch.
4. ICMPv6 carries Neighbor Discovery and path-MTU signalling essential to IPv6 operation, so blocking it breaks connectivity entirely, unlike much of ICMPv4.
5. Disabling IPv6 is acceptable when it is genuinely unused and is disabled consistently everywhere; the worst state is half-disabled, where some hosts still autoconfigure and go unmonitored.

## Further reading

- RFC 8200, Internet Protocol, Version 6: https://www.rfc-editor.org/rfc/rfc8200
- RFC 4861, Neighbor Discovery for IPv6, and RFC 4862, SLAAC: https://www.rfc-editor.org/rfc/rfc4861
- RFC 6105, IPv6 Router Advertisement Guard: https://www.rfc-editor.org/rfc/rfc6105
- RFC 4890, Filtering ICMPv6 Messages in Firewalls: https://www.rfc-editor.org/rfc/rfc4890
- NIST SP 800-119, Guidelines for the Secure Deployment of IPv6: https://doi.org/10.6028/NIST.SP.800-119
