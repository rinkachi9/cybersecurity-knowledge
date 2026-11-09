# VPNs

## Summary

A virtual private network (VPN) extends a private network across a public one by tunneling traffic through an encrypted, authenticated channel. Two uses dominate: *site-to-site* VPNs link whole networks (offices, data centers, cloud) over the internet, and *remote-access* VPNs let an individual device join the corporate network from anywhere. VPNs were the backbone of remote work and perimeter extension for two decades, and they remain widely used, but their security model (once you are on the VPN, you are "inside") is exactly what [zero-trust networking](../architecture/zero-trust-networking.md) argues against. The modern view is that a VPN is a transport control, not an access-control strategy: it protects traffic in transit and should be paired with strong authentication, segmentation and per-application authorization, not treated as a trust boundary by itself.

## Prerequisites

- [IPsec](ipsec.md) and [TLS in network security](tls-in-network-security.md): the protocols VPNs are built on.
- [Network segmentation](../architecture/network-segmentation.md) and [zero-trust networking](../architecture/zero-trust-networking.md): what a VPN should and should not replace.
- [Network threat model](../foundations/network-threat-model.md).

## Core concepts

### Definition

A *VPN* is an encrypted, authenticated tunnel that carries private-network traffic across an untrusted network. The tunnel endpoints authenticate each other, agree on keys, and encapsulate traffic so that an on-path observer sees only ciphertext between the endpoints.

### Analogy

A VPN is a private, armored pneumatic tube running through a public building. A remote worker's tube connects their desk to the head office so they can use office resources as if they were there; a site-to-site tube joins two offices' internal mail systems. Anyone in the public building sees a tube but cannot open it or read what is inside. The danger is treating "connected to the tube" as "trusted employee": the tube only proves the connection is private, not that whoever is at the far end should have the run of the building.

The analogy holds well; it breaks in that a VPN endpoint, unlike a tube, is software that can be exploited remotely, which is why VPN gateways are themselves high-value targets.

### Site-to-site vs remote-access

| | Site-to-site | Remote-access |
| --- | --- | --- |
| Connects | Two networks (gateways) | One device to a network |
| Typical protocol | IPsec (IKEv2) | IPsec IKEv2, TLS-based (OpenVPN, SSL-VPN), WireGuard |
| Authentication | Gateway certificates / PSK | User credentials + MFA, device certificate |
| Lifetime | Permanent | Per session |
| Main risk | Over-broad tunnel, weak crypto | Credential theft, split tunneling, endpoint posture |

### The protocols

- **IPsec (IKEv2).** The standard for site-to-site and robust mobile remote access (see [IPsec](ipsec.md)). Mature, interoperable, complex.
- **TLS-based VPNs (OpenVPN, vendor SSL-VPNs).** Run over TLS, often on port 443, so they traverse restrictive firewalls easily. Vendor SSL-VPN appliances have been a repeated source of critical vulnerabilities and a favorite initial-access vector for attackers.
- **WireGuard.** A modern, deliberately minimal VPN protocol with a tiny codebase, fixed modern cryptography (Curve25519, ChaCha20-Poly1305), and simple key-based peer configuration. Faster and easier to audit than IPsec or OpenVPN; less flexible by design. Increasingly the default for new deployments where its model fits.

### Split tunneling

*Split tunneling* sends only corporate-destined traffic through the VPN and lets other traffic go directly to the internet. *Full tunneling* sends everything through the VPN.

- Split tunneling improves performance and reduces VPN load, but the device is simultaneously on the corporate network and the open internet, so a compromise of the device can bridge the two, and the organization loses visibility into the direct traffic.
- Full tunneling gives the organization visibility and control over all the device's traffic (including DNS and web, enabling [protective DNS](../dns-security/protective-dns.md) and inspection), at the cost of performance and backhaul.

The choice is a real trade-off; security-sensitive environments often prefer full tunneling for managed devices.

### Why VPNs are not a trust strategy

The traditional VPN grants a connected device broad network access, recreating the flat-perimeter problem: one phished credential or one compromised laptop is "inside". VPN gateways are also directly internet-exposed and have been repeatedly exploited for initial access (several of the most-exploited vulnerabilities in recent CISA catalogs are VPN appliances). The modern response:

- Treat the VPN as transport only; require strong authentication (MFA, device certificates) and apply [segmentation](../architecture/network-segmentation.md) so a VPN client reaches only what it needs.
- Move toward [zero-trust network access (ZTNA)](../architecture/zero-trust-networking.md), which authenticates and authorizes each application access rather than admitting the device to a network.
- Patch VPN gateways promptly and minimize their exposed surface; they are a prime target.

## Worked example

A company supports 500 remote workers. Comparing a legacy and a modern design:

**Legacy VPN.** Users connect with a username and password to an SSL-VPN appliance, which places them on the general corporate LAN with split tunneling. Problems: a phished password plus no MFA gives an attacker full LAN access; the appliance has a critical unpatched CVE exposed to the internet; and split tunneling means a compromised laptop bridges the internet and the LAN while the company sees none of the direct traffic.

**Hardened design.** Users connect with a device certificate plus MFA. The gateway is patched and its management interface is not internet-facing. Authenticated clients are placed in a restricted segment and reach only the specific applications they are authorized for (enforced by segmentation, moving toward per-application ZTNA). Full tunneling routes all traffic through the corporate egress, so protective DNS and content policy apply. Result: a stolen password alone is useless (MFA and device cert), a connected client cannot roam the whole LAN, and the organization retains visibility.

The difference is not the VPN protocol but the surrounding controls: authentication strength, segmentation, patching and tunneling policy.

## Trade offs and when to use it

- **VPN vs ZTNA.** VPNs are simple, well-understood and fine for site-to-site and for extending a network; ZTNA better fits remote access to specific applications with least privilege. Many organizations run both during migration.
- **Protocol choice.** IPsec for interoperable site-to-site; WireGuard for simple, fast, auditable tunnels; TLS-based for firewall traversal, accepting a larger attack surface and patch burden.
- **Split vs full tunneling.** Performance vs visibility and containment; prefer full tunneling for managed, security-sensitive devices.
- **Gateway exposure.** Any VPN gateway is internet-facing and a target; the operational cost of keeping it patched and minimal is part of the decision.

## Common mistakes

- **Treating VPN connection as trust.** Grants broad access from one credential. Fix: MFA, device certificates, segmentation, move to ZTNA.
- **Unpatched or over-exposed VPN appliances.** A top initial-access vector. Fix: prompt patching, hide management interfaces, minimize exposed features.
- **Split tunneling on sensitive managed devices without compensating controls.** Bridges internet and LAN, loses visibility. Fix: full tunneling or strict host controls.
- **Weak VPN crypto or PSKs.** Fix: modern ciphers, certificates, IKEv2/WireGuard; retire legacy IKEv1 and SSL-VPN defaults.
- **No segmentation behind the VPN.** A connected client reaches everything. Fix: place VPN clients in a restricted segment with least-privilege flows.

## Practice

1. What is the core security difference between site-to-site and remote-access VPNs in terms of what they connect and authenticate?
2. Why is split tunneling a trade-off rather than simply better or worse?
3. Why does a traditional VPN recreate the flat-perimeter problem, and what is the modern alternative?
4. Why are VPN gateways themselves a major target?
5. What makes WireGuard attractive compared with IPsec and OpenVPN?

### Answers

1. Site-to-site connects two networks and authenticates gateways (certificates or PSK) with a permanent tunnel; remote-access connects one device and authenticates the user and device (credentials plus MFA, device certificate) per session.
2. Split tunneling improves performance and reduces load but puts the device on the corporate network and the open internet at once (bridging risk, lost visibility); full tunneling gives control and visibility at a performance cost.
3. It admits a connected device to a broad network zone, so one stolen credential or compromised device is "inside"; the modern alternative is zero-trust network access, authenticating and authorizing per application rather than admitting to a network.
4. They are internet-exposed by necessity and grant network access, so a vulnerability in the gateway is a direct, high-value initial-access path, which attackers exploit frequently.
5. A small, auditable codebase, fixed modern cryptography, and simple key-based configuration, giving better performance and a smaller attack surface than the more complex IPsec and OpenVPN.

## Further reading

- NIST SP 800-77 Rev. 1, Guide to IPsec VPNs (2020): https://doi.org/10.6028/NIST.SP.800-77r1
- NIST SP 800-113, Guide to SSL VPNs: https://doi.org/10.6028/NIST.SP.800-113
- NSA/CISA, Selecting and Hardening Remote Access VPN Solutions (2021): https://media.defense.gov/2021/Sep/28/2002863184/-1/-1/0/CSI_SELECTING-HARDENING-REMOTE-ACCESS-VPNS-20210928.PDF
- WireGuard protocol and whitepaper: https://www.wireguard.com/papers/wireguard.pdf
- NIST SP 800-207, Zero Trust Architecture, for the ZTNA alternative: https://doi.org/10.6028/NIST.SP.800-207
