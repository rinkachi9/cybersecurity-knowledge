# Enterprise Wi-Fi

## Summary

Enterprise Wi-Fi (WPA2/WPA3-Enterprise) authenticates each user or device individually with 802.1X and a RADIUS server, instead of sharing one passphrase as home networks do. This gives per-user credentials, individual revocation, and the ability to place devices in the right network segment based on who they are. Its security hinges almost entirely on one detail: the client must validate the RADIUS server's certificate. When it does not, an attacker can stand up a fake access point and RADIUS server and capture the credentials the client offers. Enterprise Wi-Fi done right (EAP-TLS with certificates, strict server validation) is strong; done wrong (PEAP with no server validation) it leaks credentials wholesale.

## Prerequisites

- [Wi-Fi security protocols](wifi-security-protocols.md): the WPA framework.
- [Network access control and 802.1X](../link-layer/network-access-control-8021x.md): the authentication machinery (supplicant, authenticator, RADIUS, EAP).
- [Wireless attacks](wireless-attacks.md): the evil-twin attack this must resist.

## Core concepts

### Definition

*Enterprise Wi-Fi* is WPA2 or WPA3 in *enterprise mode*, where authentication uses 802.1X with EAP and a RADIUS server rather than a shared pre-shared key. Each connecting device authenticates with its own credential (a certificate or a username and password), and the network can authorize it individually.

### Analogy

Home Wi-Fi is a building with one key that everyone copies: you cannot tell who entered or revoke one person without re-keying for all. Enterprise Wi-Fi is a building where each person badges in with their own ID, checked by a central security office (RADIUS), which can admit, deny or revoke each person and send them to the right floor. The critical subtlety is that the badge reader must prove it is the real security office; if a fake reader is set up in the lobby, people badge into it and hand over their credentials to a thief.

The analogy is close; the "fake reader" is the evil-twin access point, and "proving the reader is real" is the client validating the RADIUS server certificate.

### How it builds on 802.1X

Enterprise Wi-Fi is 802.1X (see [that note](../link-layer/network-access-control-8021x.md) for the full mechanism) applied over the air:

- The *supplicant* is the Wi-Fi client; the *authenticator* is the access point/controller; the *authentication server* is RADIUS.
- Until authentication succeeds, the access point passes only the EAP exchange.
- On success, RADIUS can return attributes assigning the device to a VLAN or applying policy, so authentication and [segmentation](../architecture/network-segmentation.md) are linked.
- Each session derives unique encryption keys, so unlike a shared PSK, one user cannot decrypt another's traffic.

### The EAP method is everything

The security of enterprise Wi-Fi depends on the EAP method and on server validation:

- *EAP-TLS*: client and server authenticate with certificates. There is no password to phish or capture, and both sides prove identity. The strongest option; its cost is a client-certificate infrastructure.
- *PEAP / EAP-TTLS*: the client sends a username and password inside a TLS tunnel to the server. Secure *only if* the client validates the server's certificate (checks it is signed by the expected CA and matches the expected RADIUS server name). If validation is off or misconfigured, the client will complete the tunnel with any server, including an attacker's, and send the credentials into it.

The recurring, severe misconfiguration is PEAP clients that do not validate the server certificate. An attacker sets up an evil-twin SSID and a RADIUS server, the client connects and tunnels its credentials to the attacker, and the attacker captures the username and a crackable password hash (MSCHAPv2). This is a staple of wireless penetration tests.

### Doing it right

- Prefer **EAP-TLS** with client certificates: no phishable password, mutual authentication.
- If using PEAP/EAP-TTLS, **enforce server-certificate validation** on every client via configuration (specify the trusted CA and the exact RADIUS server name), and do not let users accept unknown certificates.
- Use a **private CA** for the RADIUS server certificate and distribute its root to managed clients, so only that server is trusted.
- Assign VLANs and policy from RADIUS so devices land in the correct segment by identity.
- Protect the RADIUS server and its secrets; it is the center of trust.

## Worked example

This is conceptual (no radio in the lab). Two deployments of the same enterprise SSID:

1. **Misconfigured PEAP.** Clients are set to "connect to this SSID" with server validation disabled (a common default when configured by hand). An attacker nearby broadcasts the same SSID with a stronger signal and runs a rogue RADIUS server. A user's device associates, starts PEAP, does not check the server certificate, and sends the user's domain username and MSCHAPv2 response into the attacker's tunnel. The attacker captures it and cracks the password offline. One rogue access point harvests many users' domain credentials.
2. **EAP-TLS.** Clients have device certificates from the corporate CA and are configured to trust only the corporate RADIUS server's certificate. The attacker's rogue access point and RADIUS server cannot present a certificate the client trusts, so the handshake fails and no credential is ever sent; there is no password to capture in any case. The evil twin gathers nothing.

The difference is entirely in the authentication method and server validation, not in signal strength or encryption. This is why "enterprise Wi-Fi" is only as strong as its EAP configuration.

## Trade offs and when to use it

- **EAP-TLS vs PEAP.** EAP-TLS is phishing-resistant and the right default for managed devices, at the cost of issuing and managing client certificates; PEAP is easier but safe only with correctly enforced server validation, which is error-prone. Prefer EAP-TLS.
- **Enterprise vs personal.** Enterprise gives per-user credentials, revocation and identity-based segmentation, at the cost of RADIUS and certificate infrastructure; personal (PSK/SAE) is simpler but shares one secret. Use enterprise for organizations of any size that can run it.
- **Managed vs BYOD.** Enforcing server validation and deploying certificates is straightforward on managed devices; personal devices need an onboarding process (often a provisioning tool) to configure them correctly, or they will be misconfigured.
- **WPA3-Enterprise 192-bit mode** for high-security environments, at some client-support cost.

## Common mistakes

- **PEAP with server validation disabled.** The single most damaging enterprise Wi-Fi misconfiguration; enables credential harvesting via evil twin. Fix: enforce validation of the RADIUS server certificate (CA and name), or use EAP-TLS.
- **Letting users manually configure the SSID.** They skip server validation. Fix: push a managed profile that pins the CA and server name.
- **Using a public CA for the RADIUS certificate.** Any certificate from that CA might be trusted. Fix: a private CA, trusting only your RADIUS server's certificate.
- **Weak passwords behind PEAP/MSCHAPv2.** Captured responses crack easily. Fix: EAP-TLS (no password), or strong passphrases and monitoring.
- **Unprotected RADIUS server.** It is the trust center; compromise is total. Fix: harden, segment and monitor it.

## Practice

1. What does enterprise Wi-Fi provide that a shared pre-shared key cannot?
2. Why is client validation of the RADIUS server certificate the critical security detail?
3. How does an evil-twin attack capture credentials from a misconfigured PEAP client?
4. Why is EAP-TLS resistant to that attack?
5. Why should the RADIUS server certificate use a private CA rather than a public one?

### Answers

1. Per-user (or per-device) credentials with individual authentication and revocation, unique per-session encryption keys so users cannot decrypt each other's traffic, and identity-based VLAN/policy assignment.
2. Without it, the client will complete authentication with any RADIUS server, including an attacker's, and send its credentials there; validating the certificate ensures the client only talks to the genuine server.
3. The attacker runs a rogue access point with the same SSID and a rogue RADIUS server; the client associates, starts PEAP, skips server validation, and sends its username and MSCHAPv2 response into the attacker's tunnel, which the attacker captures and cracks offline.
4. EAP-TLS uses mutual certificate authentication with no password to capture, and the client validates the server's certificate, so a rogue server cannot present a trusted certificate or complete the handshake.
5. A public CA could issue a certificate for the RADIUS server's name to anyone, so a client trusting that CA might accept an attacker's certificate; a private CA lets the client trust only the specific corporate RADIUS certificate.

## Further reading

- NIST SP 800-97, Establishing Wireless Robust Security Networks (802.11i): https://doi.org/10.6028/NIST.SP.800-97
- RFC 5216, EAP-TLS Authentication Protocol: https://www.rfc-editor.org/rfc/rfc5216
- [Network access control and 802.1X](../link-layer/network-access-control-8021x.md) for the underlying mechanism.
- Wi-Fi Alliance, WPA3 and Enterprise security specifications: https://www.wi-fi.org/discover-wi-fi/security
