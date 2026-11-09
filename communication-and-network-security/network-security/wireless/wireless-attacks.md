# Wireless attacks

## Summary

Because Wi-Fi travels through the air, an attacker within radio range can attack it without any physical connection, and several attacks exploit that reach: the *evil twin* and *rogue access point* impersonate or add a wireless network to lure clients and intercept traffic, *deauthentication* frames knock clients off to force reconnection (for capture or denial of service), and *handshake and PMKID capture* feed offline cracking of the passphrase. The common thread is that wireless trusts signals from the air that it cannot physically verify. Defenses combine WPA3 (which closes several of these), Protected Management Frames, wireless intrusion prevention, and the enterprise-authentication hygiene from the neighboring notes.

## Prerequisites

- [Wi-Fi security protocols](wifi-security-protocols.md) and [enterprise Wi-Fi](enterprise-wifi.md).
- [Network threat model](../foundations/network-threat-model.md): the adjacent attacker within radio range.
- [Man-in-the-middle](../network-attacks/man-in-the-middle.md): the on-path goal.

Authorized use only: wireless testing is done under written authorization, often in a controlled RF environment, because it can disrupt others' connectivity. This note frames the attacks for defense.

## Core concepts

### Definition

*Wireless attacks* are techniques that exploit the radio medium and the 802.11 protocols to intercept, disrupt or gain access to Wi-Fi networks and their clients. They include access-point impersonation, management-frame abuse, and credential/handshake capture.

### Analogy

A wired network is a set of physical sockets you must plug into. Wi-Fi is like shouting across an open plaza: anyone in earshot can listen, and anyone can shout back pretending to be the information desk. An *evil twin* is a fake information desk with the same sign as the real one, set up louder and closer, so people walk up and talk to it. A *deauth* attack is someone shouting "the desk is closed, go to the other one" to send people to the fake desk. The plaza's openness, not any single flaw, is what enables all of it.

The analogy holds well; it breaks in that WPA3's Protected Management Frames add a way to authenticate the "the desk is closed" announcements, which a shouted announcement in a plaza cannot have.

### Evil twin and rogue access points

- A *rogue access point* is an unauthorized access point connected to the network, often plugged in innocently by an employee (a personal router) or maliciously, creating an uncontrolled entry point that bypasses the wired security controls.
- An *evil twin* is an attacker-controlled access point broadcasting the SSID of a legitimate network, often with a stronger signal, to lure clients into connecting. Once a client associates, the attacker is on-path and can intercept traffic, present a captive portal to phish credentials, or (against misconfigured [enterprise Wi-Fi](enterprise-wifi.md)) harvest the EAP credentials the client offers. MITRE ATT&CK tracks the evil twin as Adversary-in-the-Middle: Evil Twin (T1557.004).

### Deauthentication and management-frame attacks

In WPA2 and earlier, 802.11 *management frames* (including deauthentication and disassociation) are not authenticated, so an attacker can forge a deauth frame that forces a client to disconnect. Uses:

- *Denial of service*: repeatedly deauth clients so they cannot stay connected.
- *Forcing a handshake*: deauth a client so it reconnects, letting the attacker capture the new 4-way handshake for offline cracking.
- *Herding to an evil twin*: deauth clients from the real access point so they reconnect to the attacker's stronger-signal twin.

*Protected Management Frames* (PMF, mandatory in WPA3) authenticate management frames, defeating deauth attacks. This is one of WPA3's most practically important improvements.

### Handshake and PMKID capture

Against WPA2-Personal, the passphrase can be attacked offline from captured material:

- Capturing the *4-way handshake* (often by forcing a reconnect with deauth) enables offline dictionary attack on the passphrase.
- The *PMKID* attack captures a value the access point sends in the first handshake message, enabling offline cracking without even waiting for a client to connect, in some configurations.

Both reduce WPA2-Personal security to passphrase strength. WPA3's SAE handshake removes the offline-cracking avenue (see [Wi-Fi security protocols](wifi-security-protocols.md)).

### Other wireless risks

- *Karma / known-SSID attacks*: devices probe for remembered networks; an attacker answers as any requested SSID, luring devices onto a fake network. Mitigated by not auto-connecting to open networks and by OS behavior changes.
- *Jamming*: raw RF interference denies service; a physical-layer attack addressed by RF monitoring and, ultimately, locating the jammer.

## Worked example

This is conceptual (no radio in the lab). An attacker targets an office Wi-Fi to intercept a user's traffic:

1. **Reconnaissance.** The attacker observes the legitimate SSID and the channels and clients present.
2. **Evil twin.** They broadcast the same SSID with a stronger signal from a position near the target.
3. **Herding (WPA2).** They send deauthentication frames to the client, forcing it off the real access point. Because WPA2 management frames are unauthenticated, the client obeys and reconnects, choosing the attacker's stronger-signal twin.
4. **Interception.** The client associates with the twin; the attacker is now on-path and can intercept traffic, serve a captive portal to phish, or capture credentials.
5. **With WPA3 and defenses.** Protected Management Frames reject the forged deauthentication, so the client is not herded; the client's configuration (validated server certificate for enterprise, or SAE for personal) means even association with a twin yields no crackable credential; and a wireless intrusion prevention system detects the duplicate SSID and alerts. The attack is blunted at multiple points.

The example shows that the evil twin depends on herding (deauth) and on weak client configuration, both of which WPA3 and proper setup remove.

## Detection and mitigation

- **WPA3 with mandatory PMF** defeats deauthentication and herding, and SAE removes offline passphrase cracking. The single highest-value step.
- **Wireless Intrusion Prevention (WIPS)** monitors the RF environment for rogue and duplicate-SSID access points, deauth floods and anomalies, and can locate or contain them.
- **Enterprise authentication done right** (EAP-TLS, or PEAP with enforced server-certificate validation) means an evil twin captures no usable credential; see [enterprise Wi-Fi](enterprise-wifi.md).
- **Client hygiene**: do not auto-connect to open or remembered networks, forget old networks, prefer networks that validate the server.
- **Rogue AP detection**: scan for unauthorized access points on the wired network (switch port monitoring, WIPS), and use [802.1X](../link-layer/network-access-control-8021x.md) so an unauthorized AP cannot simply join.
- **Strong passphrases** where personal mode is used, so any captured WPA2 handshake resists offline cracking.

## Trade offs and when to use it

- **WPA3 adoption** closes most of these but requires client support; transition modes reopen WPA2 weaknesses. Move to WPA3-only as the fleet allows.
- **WIPS** gives RF visibility and containment, at the cost of sensors and tuning (and containment of a rogue AP can raise legal questions if it is someone else's). Deploy in sensitive environments.
- **Open guest networks** are convenient but inherently interceptable; treat all traffic on them as public and require TLS end to end, or use a secure onboarding method.

## Practice

1. What is the difference between a rogue access point and an evil twin?
2. Why does WPA2 allow deauthentication attacks, and how does WPA3 stop them?
3. How does an attacker use deauthentication to crack a WPA2-Personal passphrase?
4. Why does a correctly configured enterprise Wi-Fi client give an evil twin nothing useful?
5. What does a WIPS add to wireless defense?

### Answers

1. A rogue access point is an unauthorized AP connected to the network (often an innocent personal router) creating an uncontrolled entry point; an evil twin is an attacker-controlled AP impersonating a legitimate SSID to lure clients for interception.
2. WPA2 leaves management frames (including deauthentication) unauthenticated, so an attacker can forge them; WPA3 makes Protected Management Frames mandatory, authenticating these frames so forged deauths are rejected.
3. The attacker deauthenticates a connected client to force it to reconnect, captures the resulting 4-way handshake, and performs an offline dictionary attack on the passphrase against the captured handshake.
4. With EAP-TLS there is no password to capture and mutual certificate authentication fails against the twin; with PEAP and enforced server validation the client refuses the twin's untrusted certificate, so no credential is sent.
5. Radio-environment monitoring that detects rogue and duplicate-SSID access points, deauthentication floods and other anomalies, and can alert on or contain them.

## Further reading

- MITRE ATT&CK, Adversary-in-the-Middle: Evil Twin (T1557.004): https://attack.mitre.org/techniques/T1557/004/
- NIST SP 800-97, Establishing Wireless Robust Security Networks: https://doi.org/10.6028/NIST.SP.800-97
- Vanhoef, M., KRACK and later Wi-Fi attack research: https://www.krackattacks.com/
- Wi-Fi Alliance, WPA3 and Protected Management Frames: https://www.wi-fi.org/discover-wi-fi/security
