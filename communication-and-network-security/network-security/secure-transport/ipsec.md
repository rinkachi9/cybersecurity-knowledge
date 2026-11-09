# IPsec

## Summary

IPsec is a suite of protocols that secures IP traffic at the network layer, below the applications, so that whole flows or whole networks can be authenticated and encrypted without any change to the applications themselves. It is the classic technology for site-to-site VPNs (linking two offices over the internet) and one option for remote-access VPNs. Its two workhorses are the Encapsulating Security Payload (ESP), which encrypts and authenticates packets, and the Internet Key Exchange (IKE), which authenticates the peers and negotiates keys. IPsec is powerful and standards-based but notoriously complex to configure correctly, which is both its main operational cost and a frequent source of weak deployments.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): on-path confidentiality and integrity.
- [Public Key Infrastructure](../../../security-architecture-and-engineering/cryptography/public-key-infrastructure.md): certificate-based peer authentication.
- Basic IP routing and the idea of a tunnel.

## Core concepts

### Definition

*IPsec* (RFC 4301 and related) secures IP at the network layer. It provides confidentiality, integrity, data-origin authentication and anti-replay for IP packets. Because it works on IP packets, it protects everything above (TCP, UDP, applications) transparently.

### Analogy

IPsec is an armored courier route between two buildings. Instead of protecting each individual letter (which is what TLS does per application), the courier takes every outgoing item, seals it inside an armored container addressed building-to-building, drives it over public roads, and unpacks it at the other end. The applications inside each building do not know the road exists; they just hand items to the internal mail system. Setting up the route requires both buildings to agree on the armor, the locks and each other's identity, which is the complex part.

The analogy breaks in that IPsec can also protect a single host's traffic (transport mode), not only building-to-building, and that "unpacking at the other end" means the plaintext exists inside each site, so IPsec protects the path, not the endpoints.

### Modes and protocols

| Component | Role |
| --- | --- |
| ESP (Encapsulating Security Payload) | Encrypts and authenticates the packet; the protocol actually used in practice |
| AH (Authentication Header) | Authenticates only (no encryption); rarely used, breaks through NAT |
| IKE (Internet Key Exchange, v2) | Authenticates the peers and negotiates the keys and parameters (the Security Associations) |

Two modes:

- *Tunnel mode* encapsulates the entire original IP packet inside a new one, hiding the internal addresses. This is used for site-to-site and gateway-to-gateway VPNs.
- *Transport mode* protects the payload of a packet between two hosts, keeping the original header. Used for host-to-host.

### How a tunnel is built (IKEv2)

```mermaid
sequenceDiagram
    participant A as Gateway A
    participant B as Gateway B
    A->>B: IKE_SA_INIT (propose crypto, Diffie-Hellman exchange)
    B->>A: IKE_SA_INIT (agree crypto, DH)
    A->>B: IKE_AUTH (prove identity: certificate or PSK)
    B->>A: IKE_AUTH (prove identity; establish Child SA)
    Note over A,B: ESP-protected tunnel: all site-to-site IP traffic encrypted
```

IKEv2 (RFC 7296) authenticates the two peers (by certificate or, less securely, a pre-shared key), performs a Diffie-Hellman exchange for forward secrecy, and sets up the Security Associations that ESP then uses to protect traffic.

### Security choices that matter

- **Peer authentication.** Certificates scale and resist offline attack; *pre-shared keys* (PSK) are easy but a weak or reused PSK undermines the whole tunnel and is subject to offline cracking. Prefer certificates for anything beyond a small static setup.
- **Strong, modern crypto.** Use AES-GCM (AEAD) for ESP and strong DH groups; disable legacy DES/3DES, MD5, and weak DH groups. Old IKEv1 aggressive mode with PSK leaks a crackable hash and should not be used.
- **Perfect forward secrecy.** Enable PFS so each rekey uses a fresh DH exchange.
- **NAT traversal.** ESP does not pass cleanly through NAT; NAT-T encapsulates ESP in UDP 4500 to cross it. AH cannot traverse NAT at all.

### IPsec vs TLS vs WireGuard

IPsec protects at the network layer (any IP traffic, whole networks), TLS at the application layer (per connection, with easy certificate-based server auth), and [WireGuard](vpns.md) is a newer, far simpler VPN protocol that achieves similar goals with a tiny, opinionated codebase. IPsec's strength is universality and standards support across all vendors; its weakness is configuration complexity, which is exactly why simpler alternatives gained ground.

## Worked example

This is a configuration-level walkthrough; a full IPsec tunnel needs two gateways and is not run in the namespace lab, so it is marked not tested here.

Two offices, A (`10.1.0.0/16` behind gateway `203.0.113.1`) and B (`10.2.0.0/16` behind `198.51.100.1`), want a site-to-site tunnel. A sound configuration:

1. **Peers authenticate by certificate** from a shared internal CA, not a pre-shared key, so a leaked static secret cannot compromise the tunnel.
2. **IKEv2** negotiates AES-256-GCM for ESP, a strong DH group (for example group 20, 384-bit ECP), and PFS on rekey.
3. **Tunnel mode**: packets from `10.1.0.0/16` to `10.2.0.0/16` are encapsulated and encrypted between the gateways; the internal addresses are hidden on the public path.
4. **Traffic selectors** scope the tunnel to exactly those subnets, so only intended traffic uses it.
5. **NAT-T** (UDP 4500) is enabled in case either gateway is behind NAT.

The result: a workstation in office A reaches a server in office B as if on one network, with all traffic authenticated and encrypted across the internet, and neither the applications nor the users are aware of IPsec. A weak version of the same tunnel, IKEv1 aggressive mode with a short shared PSK and 3DES, would be crackable offline and is a common legacy finding.

## Trade offs and when to use it

- **Site-to-site is IPsec's sweet spot.** For linking networks over the internet with broad vendor interoperability, IPsec is the standard.
- **Remote access: IPsec (IKEv2) vs TLS VPN vs WireGuard.** IKEv2 remote access is robust and mobile-friendly (MOBIKE handles roaming); TLS-based VPNs traverse restrictive firewalls more easily (port 443); WireGuard is simpler and faster but newer. Choose by client support and firewall environment.
- **Complexity cost.** IPsec has many knobs and mismatched settings silently fail or fall back to weak options; it needs expertise to deploy safely. This is the main argument for simpler alternatives where interoperability is not required.
- **Protects the path, not the endpoints.** Plaintext exists inside each site; combine with endpoint and application controls.

## Common mistakes

- **Pre-shared keys that are weak, shared or in IKEv1 aggressive mode.** Offline-crackable. Fix: certificates, or strong unique PSKs and IKEv2 only.
- **Legacy crypto (DES/3DES, MD5, weak DH, no PFS).** Fix: AES-GCM, strong DH groups, PFS; disable IKEv1.
- **Over-broad traffic selectors.** Tunnel carries more than intended. Fix: scope selectors to the needed subnets.
- **Forgetting NAT traversal.** ESP breaks through NAT without NAT-T. Fix: enable NAT-T (UDP 4500); avoid AH where NAT is present.
- **Assuming the tunnel secures the endpoints.** It secures the path; a compromised host at either end is still compromised. Fix: layer endpoint and segmentation controls.

## Practice

1. At which layer does IPsec operate, and why does that make it transparent to applications?
2. What is the difference between tunnel mode and transport mode?
3. Why are certificates preferred over pre-shared keys for peer authentication?
4. Why does ESP need NAT-T to cross a NAT device?
5. What is IPsec's main operational weakness compared with WireGuard or TLS VPNs?

### Answers

1. The network layer (IP); because it protects IP packets, everything above it (TCP, UDP, applications) is secured without the applications being aware or modified.
2. Tunnel mode encapsulates the entire original IP packet in a new one (hiding internal addresses, used gateway-to-gateway); transport mode protects only the payload between two hosts, keeping the original header.
3. Certificates scale, are individually revocable, and resist offline attack, whereas a pre-shared key can be weak, reused, or (in IKEv1 aggressive mode) exposed as a crackable hash.
4. ESP is its own IP protocol that NAT devices cannot rewrite port information for; NAT-T wraps ESP in UDP 4500 so it can traverse NAT.
5. Configuration complexity: it has many parameters that must match and can silently fall back to weak options, so it needs expertise to deploy securely, which simpler protocols avoid.

## Further reading

- RFC 4301, Security Architecture for the Internet Protocol (IPsec): https://www.rfc-editor.org/rfc/rfc4301
- RFC 7296, Internet Key Exchange Protocol Version 2 (IKEv2): https://www.rfc-editor.org/rfc/rfc7296
- NIST SP 800-77 Rev. 1, Guide to IPsec VPNs (2020): https://doi.org/10.6028/NIST.SP.800-77r1
- NSA/CISA, Selecting and Hardening Remote Access VPN Solutions (2021).
