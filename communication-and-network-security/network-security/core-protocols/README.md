# Core protocol security

The internet and transport protocols (IP, TCP, ICMP, IPv6, BGP) and the name and mail protocols that ride on them, each with its trust assumption, its attacks, and the add-on that secures it. These notes explain why the default protocols can be lied to and what actually closes each gap.

## Notes

- [IP spoofing and source address validation](ip-spoofing-and-source-validation.md): forged source addresses, BCP 38 ingress filtering and uRPF.
- [TCP attacks](tcp-attacks.md): RST injection, session hijacking, sequence-number randomization and RFC 5961.
- [ICMP security](icmp-security.md): keeping the useful ICMP, dropping the dangerous, without breaking the network.
- [IPv6 security](ipv6-security.md): rogue router advertisements, Neighbor Discovery, and the dual-stack blind spot.
- [BGP security](bgp-security.md): prefix hijacks, route leaks, RPKI, ROV, ASPA and MANRS.
- [Local name resolution poisoning](local-name-resolution-poisoning.md): LLMNR, NBT-NS, mDNS and WPAD abuse, and credential capture.
- [Insecure legacy protocols](insecure-legacy-protocols.md): Telnet, FTP, SNMPv1/v2c, SMBv1 and their secure replacements.
- [Email transport security](email-transport-security.md): SPF, DKIM, DMARC, MTA-STS and DANE.

Related: [SYN flood](../network-attacks/denial-of-service/syn-flood.md) is a TCP state-exhaustion attack kept with the denial-of-service family.

Back to [Network security](../README.md).
