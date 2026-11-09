# Wi-Fi security protocols

## Summary

Wi-Fi security protocols protect the wireless link, where anyone within radio range can hear the traffic, so the stakes are higher than on a wired network that requires physical access. The protocols evolved from WEP (broken), through WPA and WPA2 (WPA2 still widely used, with known weaknesses), to WPA3 (current, fixing the main WPA2 flaws). The core jobs are encrypting the air link and authenticating devices without letting an eavesdropper recover the key. Understanding the handshake, why WEP and then WPA2's pre-shared-key handshake were attackable, and what WPA3's SAE and Protected Management Frames add, is the foundation for securing both home and enterprise wireless.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): the adjacent attacker, now within radio range.
- [Enterprise Wi-Fi](enterprise-wifi.md) and [wireless attacks](wireless-attacks.md): the next notes.
- Basic symmetric encryption and key exchange.

## Core concepts

### Definition

*Wi-Fi security protocols* (defined in IEEE 802.11 and the Wi-Fi Alliance's WPA certifications) authenticate devices to a wireless network and encrypt the traffic over the air. Two authentication modes recur: *personal* (a shared passphrase, PSK) for homes and small sites, and *enterprise* (802.1X with individual credentials) for organizations, covered in [enterprise Wi-Fi](enterprise-wifi.md).

### Analogy

Wireless is a conversation in a crowded, open square: everyone nearby can hear. The security protocol is a scheme for two people to agree on a private code and speak in it despite being overheard. WEP used a weak, reused code that eavesdroppers could reconstruct by listening long enough. WPA2-Personal improved the code but let an eavesdropper who recorded the initial "let us agree on a code" exchange take it home and guess the passphrase at leisure. WPA3 changed the agreement so that recording it reveals nothing useful to guess against, and each person's conversation gets its own private code even on a shared passphrase.

The analogy holds well; it breaks only in that the "codes" are cryptographic keys and the guessing is automated, so a weak passphrase still falls quickly even to WPA3's stronger scheme if it is short.

### The evolution

| Protocol | Year | Encryption | Key weakness |
| --- | --- | --- | --- |
| WEP | 1999 | RC4, static key | Fundamentally broken; key recoverable from captured traffic in minutes. Do not use. |
| WPA | 2003 | TKIP (RC4-based) | Interim fix for WEP; TKIP later broken. Obsolete. |
| WPA2 | 2004 | AES-CCMP | Strong cipher, but the 4-way handshake allows offline PSK cracking and was exposed by KRACK; management frames unprotected |
| WPA3 | 2018 | AES (CCMP/GCMP) | Current; SAE handshake resists offline cracking, PMF mandatory, forward secrecy |

### The WPA2 4-way handshake and its weakness

When a device joins a WPA2-Personal network, it performs a *4-way handshake* that derives the session keys from the pre-shared passphrase. An attacker who captures this handshake (by sniffing, or by forcing a reconnection with a deauthentication, see [wireless attacks](wireless-attacks.md)) can then perform an *offline dictionary attack*: guess passphrases and check each against the captured handshake, with no further interaction and no lockout. A weak passphrase falls quickly. This is the central WPA2-Personal weakness: the security reduces to the strength of the passphrase, and the handshake can be captured and attacked offline.

*KRACK* (Key Reinstallation Attack, 2017) additionally exploited a flaw in the handshake state machine to force key reuse, allowing decryption of some traffic; it was patched in implementations, but it illustrated the handshake's fragility.

### What WPA3 fixes

- *SAE (Simultaneous Authentication of Equals)*, a password-authenticated key exchange (the "Dragonfly" handshake), replaces the WPA2 PSK handshake. Capturing the exchange does not let an attacker guess the passphrase offline: each guess requires a fresh, interactive attempt against the network, which is rate-limited and detectable. This is the key improvement, it breaks the offline-cracking attack.
- *Protected Management Frames (PMF)* become mandatory, so management frames (including deauthentication) are authenticated, defeating the deauth attacks that WPA2 allowed.
- *Forward secrecy*: capturing traffic and later learning the passphrase does not decrypt past sessions.
- *WPA3-Enterprise* offers a 192-bit mode for high-security environments.

WPA3 still depends on a strong passphrase for the personal mode (SAE resists offline cracking but not a trivially short password tried online), and transition modes that support both WPA2 and WPA3 reintroduce WPA2's weaknesses for WPA2 clients.

## Worked example

This is conceptual; the namespace lab has no radio, so no Wi-Fi capture is run here.

Compare an attacker's options against the same network under WPA2 and WPA3:

1. **WPA2-Personal.** The attacker sniffs nearby, sends a deauthentication frame to force a client to reconnect (management frames are unprotected), captures the resulting 4-way handshake, and takes it offline. They then run billions of passphrase guesses against the captured handshake on their own hardware, with no interaction with the network and no rate limit. An 8-character or dictionary passphrase falls; a 20-character random passphrase likely does not.
2. **WPA3-Personal.** The deauthentication attack fails because Protected Management Frames authenticate management frames. Even if the attacker observes an SAE exchange, it yields nothing to crack offline: each passphrase guess must be made interactively against the access point, which rate-limits and logs attempts. Offline cracking is removed as an option.

The practical lesson: on WPA2, network security equals passphrase strength plus the risk of offline capture; WPA3 removes the offline-capture avenue, but a strong passphrase (or enterprise authentication) is still required.

## Trade offs and when to use it

- **WPA3 vs WPA2.** Use WPA3 wherever client support allows; it closes offline cracking and deauth attacks. WPA2 remains common and acceptable with a strong passphrase and PMF enabled, but is the weaker choice.
- **Transition mode.** Supporting both WPA2 and WPA3 eases migration but exposes WPA2 clients to WPA2's weaknesses; move to WPA3-only when the device fleet allows.
- **Personal vs enterprise.** Personal (PSK/SAE) is simple but shares one secret and cannot distinguish or revoke individual devices; [enterprise](enterprise-wifi.md) (802.1X) gives per-user credentials and revocation, at the cost of a RADIUS/certificate infrastructure. Use enterprise for organizations.
- **Never WEP or WPA/TKIP.** Both are broken; their presence is a critical finding.

## Common mistakes

- **Still running WEP or WPA/TKIP.** Trivially broken. Fix: WPA2-AES minimum, WPA3 preferred.
- **Weak Wi-Fi passphrases on personal mode.** Offline cracking (WPA2) or online guessing succeeds. Fix: long random passphrases, or enterprise authentication.
- **Leaving PMF disabled on WPA2.** Allows deauthentication attacks. Fix: enable Protected Management Frames; prefer WPA3 where it is mandatory.
- **Permanent WPA2/WPA3 transition mode.** Keeps WPA2 weaknesses alive. Fix: migrate to WPA3-only.
- **Treating a shared PSK as per-user security.** Everyone shares one secret with no revocation. Fix: enterprise 802.1X for organizations.

## Practice

1. Why is link-layer encryption more essential on Wi-Fi than on a wired switched network?
2. What is the central weakness of the WPA2-Personal 4-way handshake?
3. How does WPA3's SAE handshake defeat offline passphrase cracking?
4. What attack do Protected Management Frames prevent, and why could WPA2 allow it?
5. Why does a WPA2/WPA3 transition mode weaken security?

### Answers

1. Anyone within radio range can passively receive the traffic without any physical access, whereas a wired switched network delivers unicast only to the intended port and requires physical connection, so wireless is exposed to a far larger set of adjacent attackers.
2. An attacker can capture the handshake (often by forcing a reconnection) and then perform an offline dictionary attack against the passphrase with no interaction and no rate limiting, so security reduces to passphrase strength plus capture risk.
3. SAE is a password-authenticated key exchange where observing the exchange reveals nothing to guess against; each passphrase attempt must be made interactively against the access point, which is rate-limited and detectable, removing offline cracking.
4. Deauthentication (and other management-frame) attacks that force a client to disconnect/reconnect; WPA2 left management frames unauthenticated by default, so an attacker could forge them.
5. It continues to support WPA2 clients using the weaker WPA2 handshake, so those clients remain exposed to WPA2's offline-cracking and deauthentication weaknesses.

## Further reading

- IEEE 802.11 standard and the Wi-Fi Alliance WPA3 specification: https://www.wi-fi.org/discover-wi-fi/security
- NIST SP 800-97, Establishing Wireless Robust Security Networks (802.11i): https://doi.org/10.6028/NIST.SP.800-97
- Vanhoef, M. and Piessens, F., "Key Reinstallation Attacks" (KRACK, 2017): https://www.krackattacks.com/
- [Wireless attacks](wireless-attacks.md) and [enterprise Wi-Fi](enterprise-wifi.md) for the attack and enterprise-authentication details.
