# Network access control and 802.1X

## Summary

Network Access Control (NAC) decides whether a device may join a network at all, and what it may reach once admitted, based on the device's identity and health rather than merely which port or Wi-Fi it connected to. Its core standard is IEEE 802.1X, which authenticates a device or user at the moment of connection, before the port carries general traffic, using the Extensible Authentication Protocol (EAP) and a RADIUS server. 802.1X closes the most basic weakness of a switched or wireless network, that physical or radio access alone grants network access, and it is the foundation on which dynamic VLAN assignment and posture checks are built.

## Prerequisites

- [Switch security](switch-security.md): the port-level controls 802.1X complements.
- [Authentication methods](../../../identity-and-access-management/identity-and-access/authentication/authentication-methods.md) and [authentication vs authorization](../../../identity-and-access-management/identity-and-access/authentication-vs-authorization.md).
- [Enterprise Wi-Fi](../wireless/enterprise-wifi.md): 802.1X applied to wireless.

## Core concepts

### Definition

*Network Access Control* is the policy and technology that admit, deny or constrain devices as they connect, based on identity, compliance and context. *IEEE 802.1X* is the port-based access control standard that performs the authentication: it blocks all traffic on a port except the authentication exchange until the connecting device proves its identity.

Three roles:

- *Supplicant*: the device seeking access (its 802.1X client software).
- *Authenticator*: the switch or wireless access point controlling the port.
- *Authentication server*: usually a RADIUS server that checks credentials against a directory.

### Analogy

802.1X is the locked lobby turnstile of a building. The person at the turnstile (supplicant) presents a badge, the turnstile (authenticator) does not judge the badge itself but passes it to the security office (RADIUS server), which checks it against the employee database and tells the turnstile to open or stay shut. Until then, the turnstile lets nothing through except the badge check. Dynamic VLAN assignment is the security office also telling the turnstile which floor the badge may reach.

The analogy breaks because a network port, unlike a turnstile, can be bypassed by devices that cannot authenticate (printers, cameras), which is why NAC needs fallback mechanisms like MAC Authentication Bypass.

### Mechanism

```mermaid
sequenceDiagram
    participant S as Supplicant (device)
    participant A as Authenticator (switch/AP)
    participant R as RADIUS server
    S->>A: connects; port is "unauthorized" (only EAP allowed)
    A->>S: EAP-Request Identity
    S->>A: EAP-Response Identity
    A->>R: RADIUS Access-Request (relays EAP)
    R->>S: EAP method exchange (e.g. EAP-TLS: mutual certificate check)
    R->>A: RADIUS Access-Accept (+ VLAN, ACL attributes)
    A->>S: port "authorized"; normal traffic flows
```

Before success, the port forwards only EAP over LAN (EAPOL) frames. On success, RADIUS can return authorization attributes that place the device in a specific VLAN or apply an ACL, so authentication and segmentation are decided together.

### EAP methods

The security of 802.1X depends on the EAP method and on the supplicant validating the server:

| EAP method | Credential | Mutual auth | Note |
| --- | --- | --- | --- |
| EAP-TLS | Client and server certificates | Yes | Strongest; no password to phish or spray; needs a certificate infrastructure |
| PEAP / EAP-TTLS | Password inside a server-authenticated TLS tunnel | Server only, by certificate | Common; secure only if the client validates the server certificate |
| EAP-MD5 | Password hash | No | Obsolete, offline-crackable, no server auth; do not use |

The recurring failure is a client configured not to validate the RADIUS server's certificate: an attacker stands up a fake access point and RADIUS server, the client connects and sends its credentials into the tunnel, and the attacker captures them. EAP-TLS avoids this because there is no password to capture and both sides authenticate by certificate.

### NAC beyond authentication

Full NAC adds:

- *Posture / health checks*: is the device patched, encrypted, running endpoint protection. Non-compliant devices go to a remediation VLAN.
- *Profiling*: identifying device type so that cameras and printers can be recognized and placed appropriately.
- *MAC Authentication Bypass (MAB)*: for devices that cannot do 802.1X, the switch authenticates by MAC address against an allow list. Weaker (MACs are spoofable) but necessary for legacy and IoT devices, which should go to tightly restricted segments.
- *Guest onboarding*: captive portals and sponsored access for visitors.

## Worked example

A company deploys 802.1X on wired access ports and corporate Wi-Fi, with EAP-TLS for managed laptops and MAB for printers:

1. A managed laptop connects. The switch starts EAP; the laptop and RADIUS server validate each other's certificates (EAP-TLS). RADIUS returns Access-Accept with VLAN 20 (corporate). The laptop is on the corporate VLAN with no password ever sent.
2. A printer connects. It has no supplicant, so after an EAPOL timeout the switch falls back to MAB, sends the printer's MAC to RADIUS, which matches it on the printer allow list and returns VLAN 40 (device VLAN, tightly filtered). The printer works, confined to a restricted segment.
3. A visitor's unknown laptop connects to a wall port. It cannot do EAP-TLS and its MAC is not on any list, so RADIUS rejects it; the port stays unauthorized or drops it to a guest-only VLAN with internet access and nothing internal.
4. A personal laptop with corporate credentials but failing posture check (no disk encryption) is placed in a remediation VLAN until fixed.

The same wall port behaves differently per device, decided by identity and health, not by which socket was used. This is NAC's value: the physical network no longer grants trust.

## Trade offs and when to use it

- **EAP-TLS vs PEAP.** EAP-TLS is stronger and phishing-resistant but requires issuing and managing client certificates. PEAP is easier but hinges entirely on server-certificate validation, which is often misconfigured. Prefer EAP-TLS for managed devices.
- **MAB** is necessary for devices that cannot authenticate, but MACs are spoofable, so MAB-authenticated devices belong in restricted segments with their own monitoring.
- **Deployment friction.** 802.1X touches every device and port; a phased rollout with a monitor-only mode first avoids locking out the organization. Closed mode (deny by default) is the end state.
- **Fail-open vs fail-closed on RADIUS outage.** If RADIUS is unreachable, do ports open or stay shut. Fail-open keeps the business running but suspends the control; critical environments fail closed with redundant RADIUS.

## Common mistakes

- **Supplicants not validating the server certificate (PEAP).** Enables credential theft via a fake access point. Fix: enforce server-certificate validation, pin the CA, prefer EAP-TLS.
- **MAB devices on sensitive VLANs.** A spoofed MAC then reaches sensitive systems. Fix: restrict MAB devices to isolated segments.
- **No fallback plan for RADIUS outage.** Either the business stops or the control silently disappears. Fix: redundant RADIUS and a deliberate fail policy.
- **Treating 802.1X as the whole of security.** It controls admission, not what an authenticated-but-compromised device does. Fix: combine with segmentation and monitoring.
- **Leaving unused ports in a live VLAN without 802.1X.** Fix: apply 802.1X or disable unused ports.

## Practice

1. What does an 802.1X-controlled port allow before authentication succeeds?
2. Name the three 802.1X roles and what each does.
3. Why is EAP-TLS resistant to the fake-access-point credential theft that affects PEAP?
4. What is MAC Authentication Bypass for, and why are MAB devices placed in restricted segments?
5. Why must you decide the RADIUS-outage behavior in advance?

### Answers

1. Only the authentication exchange (EAPOL / EAP frames); all other traffic is blocked until the port becomes authorized.
2. Supplicant (the connecting device proving identity), authenticator (the switch or access point controlling the port), authentication server (RADIUS, which checks credentials and returns the decision and attributes).
3. EAP-TLS uses mutual certificate authentication with no password to capture, and the client validates the server's certificate, so a fake server cannot complete the handshake or harvest a secret.
4. For devices that cannot run an 802.1X supplicant (printers, cameras); they are authenticated by MAC, which is spoofable, so they are confined to restricted segments to limit the damage if spoofed.
5. If RADIUS is unreachable, ports either fail open (business continues, control suspended) or fail closed (control preserved, connectivity lost); the right choice depends on the environment and must be configured deliberately with redundancy.

## Further reading

- IEEE 802.1X, Port-Based Network Access Control: https://standards.ieee.org/
- RFC 3748, Extensible Authentication Protocol (EAP), and RFC 5216, EAP-TLS: https://www.rfc-editor.org/rfc/rfc5216
- NIST SP 800-97, Establishing Wireless Robust Security Networks (802.11i), for 802.1X in wireless: https://doi.org/10.6028/NIST.SP.800-97
- NSA, Network Infrastructure Security Guide (2022), the authentication sections.
