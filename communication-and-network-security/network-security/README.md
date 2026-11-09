# Network security

Network security protects systems and data while they communicate: it limits who can reach what, makes traffic hard to read or forge in transit, and records enough to detect and investigate what got through. The notes are grouped by layer and by function, from the threat model and the protocols up to architecture, filtering, monitoring and operations. Offensive techniques are described for labs, CTFs and penetration tests with written permission, and each attack note ends with detection and mitigation.

## Reading order

1. [Foundations](foundations/README.md): attacker positions, why the core protocols trust by default, attacks and controls by layer, the control taxonomy and the namespace lab used by the tested examples. Read first.
2. [Link layer](link-layer/README.md): switch security, ARP spoofing, MAC flooding, VLAN hopping, DHCP attacks and 802.1X.
3. [Core protocols](core-protocols/README.md): IP spoofing, TCP, ICMP, IPv6, BGP, local name resolution, legacy protocols and email transport.
4. [DNS security](dns-security/README.md): DNS threats, DNSSEC, encrypted DNS, DNS tunneling and protective DNS.
5. [Wireless](wireless/README.md): Wi-Fi security protocols, enterprise Wi-Fi, wireless attacks and Bluetooth.
6. [Secure transport](secure-transport/README.md): TLS from the network view, TLS inspection, IPsec, VPNs and SSH.
7. [Architecture](architecture/README.md): zones and DMZ, segmentation, microsegmentation, the management plane, zero trust and SASE.
8. [Traffic filtering](traffic-filtering/README.md): firewalls, rule design, egress filtering, proxies and web application firewalls.
9. [Network attacks](network-attacks/README.md): man-in-the-middle, scanning, lateral movement, command and control, exfiltration and denial of service.
10. [Monitoring and detection](monitoring-and-detection/README.md): network security monitoring, packet capture, flows, Zeek, Suricata, encrypted traffic analysis, beaconing, NDR, hunting and deception.
11. [Cloud and modern networks](cloud-and-modern-networks/README.md): cloud networks, Kubernetes networking and SD-WAN.
12. [OT and IoT](ot-and-iot/README.md): industrial control networks and embedded devices.
13. [Operations and assurance](operations-and-assurance/README.md): device hardening, network security assessment and network incident response.

## Related areas

- [Cryptography](../../security-architecture-and-engineering/cryptography/README.md) holds PKI and the planned TLS protocol note.
- [Detection](../../security-operations/defensive-operations/detection/README.md) holds the general IDS and IPS notes that the monitoring notes build on.
- [Cloud and infrastructure security](../../security-architecture-and-engineering/cloud-and-infrastructure-security/README.md) holds posture management for cloud networks.

The [ISC2 CISSP Exam Outline, effective April 15, 2024](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf) covers network architecture, components and secure channels in sections 4.1-4.3. Checked 2026-10.

Back to [Communication and network security](../README.md).
