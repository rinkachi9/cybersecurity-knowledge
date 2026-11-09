# Man-in-the-middle (adversary-in-the-middle)

## Summary

A man-in-the-middle attack, now more precisely called adversary-in-the-middle (AiTM), is one where the attacker sits on the path between two parties and relays their traffic while reading or altering it, so both believe they are talking directly and securely. It is not a single technique but a *position*, reached by many of the attacks in this area: ARP spoofing, rogue DHCP, DNS poisoning, BGP hijacking, an evil-twin access point, or a malicious proxy. This note ties those together, explains what the on-path position enables, and shows why end-to-end authenticated encryption (TLS with validation) is the defense that holds even when the attacker achieves the position. MITRE ATT&CK tracks the family as T1557.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): the on-path position and how it is reached.
- The link-layer, DNS, routing and wireless attacks that achieve it (linked below).
- [TLS in network security](../secure-transport/tls-in-network-security.md): the defense.

Authorized use only.

## Core concepts

### Definition

An *adversary-in-the-middle* attack places the attacker on the communication path between two endpoints so they can intercept (read), and optionally alter or drop, the traffic, while relaying it so the communication appears normal. The older term "man-in-the-middle" means the same thing; this repository uses AiTM / on-path, matching current usage.

### Analogy

It is the classic trick of a dishonest translator between two people who do not share a language. Each speaker trusts the translator to relay faithfully; in fact the translator reads everything, can change what is said, and neither speaker knows. The only defense is for the two to share a secret the translator cannot fake, or to verify each other's identity by something the translator cannot forge, which is exactly what certificate-validated encryption provides.

The analogy holds closely; it breaks only in that network relaying is automatic and invisible, so unlike a human translator there is no pause or tell.

### A position, not one technique

AiTM is the *goal*; many attacks are *ways to reach it*, grouped by layer:

| Layer | Attack that reaches on-path | Note |
| --- | --- | --- |
| Link (L2) | ARP spoofing | [arp-spoofing](../link-layer/arp-spoofing/README.md) |
| Link (L2) | Rogue DHCP (poison gateway/DNS) | [dhcp-attacks](../link-layer/dhcp-attacks.md) |
| Link (L2) | LLMNR/NBT-NS poisoning | [local-name-resolution-poisoning](../core-protocols/local-name-resolution-poisoning.md) |
| Internet (L3) | DNS cache poisoning / hijacking | [dns-threat-landscape](../dns-security/dns-threat-landscape.md) |
| Internet (L3) | BGP hijacking | [bgp-security](../core-protocols/bgp-security.md) |
| Internet (L3) | IPv6 rogue router advertisement | [ipv6-security](../core-protocols/ipv6-security.md) |
| Wireless | Evil twin access point | [wireless-attacks](../wireless/wireless-attacks.md) |
| Application | Malicious/compromised proxy or CDN | [tls-inspection](../secure-transport/tls-inspection.md) |

Recognizing AiTM as a position clarifies defense: you can try to prevent the position (stop ARP spoofing, validate routes) *and* make the position useless (end-to-end encryption), and the second is more robust because there are so many ways to reach the first.

### What the position enables

Once on-path, the attacker can:

- *Eavesdrop*: read any cleartext traffic (credentials, cookies, data).
- *Modify*: alter requests and responses (inject content, change amounts, deliver malware).
- *Downgrade/strip*: remove or prevent encryption (SSL stripping, STARTTLS stripping) so traffic that could have been protected is not.
- *Capture credentials*: harvest logins from cleartext protocols or from TLS the client fails to validate.
- *Session hijack*: steal session tokens and impersonate the user.

Modern AiTM phishing kits also defeat many forms of MFA by relaying the login in real time: the victim authenticates to the attacker's proxy, which relays to the real site and steals the resulting session cookie (MITRE T1557 combined with phishing).

### Why end-to-end encryption is the real defense

Preventing every path to the on-path position is hard because there are so many. The robust defense is to make the position unprofitable: with properly validated TLS, an on-path attacker sees only ciphertext and cannot impersonate the server (they lack a certificate the client will accept) or alter data (integrity protection detects it). This is why "assume the network is hostile and encrypt end to end" is the governing principle, and why the dangerous residue is exactly where encryption is missing, not validated, or strippable.

## Worked example

A café-Wi-Fi AiTM against a user visiting a bank, showing where each defense bites:

1. **Reach the position.** The attacker runs an [evil twin](../wireless/wireless-attacks.md) with the café's SSID; the victim's device associates. The attacker is on-path. (Defense that would have prevented this: WPA3/PMF, not auto-joining open networks.)
2. **Strip encryption.** The victim types `bank.example` (no `https://`). The attacker intercepts the initial HTTP request and keeps the session on HTTP (SSL stripping), relaying to the real HTTPS site. (Defense: HSTS preloading, so the browser refuses HTTP for the bank outright.)
3. **If stripping fails.** With HSTS, the browser insists on HTTPS. The attacker can only present their own certificate, which the browser rejects because it does not validate to a trusted CA for `bank.example`. The victim sees a certificate error and the attack fails. (Defense: TLS with certificate validation, the decisive one.)
4. **AiTM phishing variant.** The attacker instead lures the victim to `bank-login.example`, a lookalike they proxy to the real bank, relaying the login and MFA in real time to steal the session cookie. (Defense: phishing-resistant MFA (FIDO2/passkeys bound to the real origin), [protective DNS](../dns-security/protective-dns.md) blocking the lookalike.)

The pattern: preventing the position helps, but validated end-to-end encryption and origin-bound authentication are what hold when the position is achieved.

## Detection and mitigation

- **End-to-end authenticated encryption** (TLS 1.3 with certificate validation, [mTLS](../secure-transport/tls-in-network-security.md) internally) makes the on-path position yield only ciphertext and blocks impersonation. The primary defense.
- **Enforce, do not just offer, encryption**: HSTS (preloaded), refuse plaintext, MTA-STS/DANE for mail, disable old TLS so downgrade has nowhere to land.
- **Phishing-resistant MFA** (FIDO2/passkeys) bound to the origin defeats real-time AiTM credential relay.
- **Prevent the position** where practical: Dynamic ARP Inspection, DHCP snooping, RA Guard, disabling LLMNR/NBT-NS, DNSSEC, RPKI, WPA3/PMF, the per-layer controls in this area.
- **Detect** the on-path signatures: certificate warnings, unexpected certificate changes/pinning failures, one MAC claiming many IPs ([ARP](../link-layer/arp-spoofing/README.md)), rogue RAs and duplicate SSIDs ([WIPS](../wireless/wireless-attacks.md)).

## Trade offs and when to use it

- **Prevent-the-position vs make-it-useless.** Preventing every path (L2/L3/wireless controls) is valuable defense in depth but incomplete because the paths are many; end-to-end encryption is the robust backstop. Do both, prioritizing encryption.
- **HSTS preloading** strongly protects but is hard to reverse quickly if a domain must serve HTTP; plan before preloading.
- **Phishing-resistant MFA** defeats AiTM relay but requires FIDO2/passkey rollout; it is the direction of travel for high-value access.

## Common mistakes

- **Relying on preventing the position alone.** Too many paths lead to it. Fix: end-to-end validated encryption as the backstop.
- **Offering TLS without enforcing it.** SSL/STARTTLS stripping keeps traffic in cleartext. Fix: HSTS, refuse plaintext, MTA-STS/DANE.
- **Assuming ordinary MFA stops AiTM.** Real-time relay kits defeat OTP and push MFA. Fix: phishing-resistant, origin-bound MFA.
- **Ignoring certificate warnings.** Users clicking through a certificate error hand the attacker the session. Fix: hard-fail on certificate errors; user training; HSTS removes the click-through option.
- **Treating it as one technique to block.** It is a position reached many ways. Fix: layered per-layer controls plus encryption.

## Practice

1. Why is adversary-in-the-middle best understood as a position rather than a single technique?
2. List three different attacks, at different layers, that put an attacker on-path.
3. Why is validated end-to-end encryption a more robust defense than trying to prevent every path to the on-path position?
4. How does an AiTM phishing proxy defeat ordinary MFA, and what stops it?
5. What does HSTS preloading prevent in an AiTM scenario?

### Answers

1. Many distinct attacks (ARP spoofing, DNS poisoning, BGP hijack, evil twin, rogue proxy) all aim to reach the same on-path position; the position, not any one technique, is what enables interception, so defenses are framed around it.
2. For example ARP spoofing (link), DNS cache poisoning or BGP hijacking (internet), and an evil-twin access point (wireless).
3. There are many ways to reach the on-path position, so blocking them all is hard and incomplete; validated end-to-end encryption makes the position useless (only ciphertext, no impersonation) regardless of how it was reached.
4. It relays the victim's login and MFA response to the real site in real time and steals the resulting session cookie, so a one-time code or push approval is passed straight through; phishing-resistant, origin-bound MFA (FIDO2/passkeys) stops it because the credential will not authenticate to the attacker's origin.
5. It prevents the browser from ever using plaintext HTTP for the domain, defeating SSL stripping, because the browser refuses the downgrade and insists on validated HTTPS.

## Further reading

- MITRE ATT&CK, Adversary-in-the-Middle (T1557) and its sub-techniques: https://attack.mitre.org/techniques/T1557/
- RFC 6797, HTTP Strict Transport Security: https://www.rfc-editor.org/rfc/rfc6797
- CISA guidance on AiTM phishing and phishing-resistant MFA.
- The per-layer attack notes linked above for how the position is reached and prevented.
