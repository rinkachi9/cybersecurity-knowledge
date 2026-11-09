# Secure transport

Encrypting and authenticating traffic in transit: the protocols that make an on-path position far less rewarding, and how to deploy, enforce and sometimes inspect them.

A note on the TLS protocol itself is planned in the [cryptography area](../../../security-architecture-and-engineering/cryptography/README.md); this subarea covers the network-security view.

## Notes

- [TLS in network security](tls-in-network-security.md): termination points, enforcement, mutual TLS, certificate management and exposed metadata.
- [TLS inspection](tls-inspection.md): sanctioned break-and-inspect, its value and its real risks.
- [IPsec](ipsec.md): network-layer VPN protocol, ESP and IKEv2, for site-to-site and remote access.
- [VPNs](vpns.md): site-to-site and remote-access VPNs, split tunneling, and why a VPN is transport, not a trust strategy.
- [SSH security](ssh-security.md): key-based authentication, hardening, key management and tunneling.

Related: [email transport security](../core-protocols/email-transport-security.md) enforces TLS between mail servers.

Back to [Network security](../README.md).
