# Encrypted traffic analysis

## Summary

Encrypted traffic analysis (ETA) extracts security signal from traffic without decrypting it, using the metadata that encryption leaves exposed: the server name (SNI), certificate details, the sizes and timing of packets, and distinctive fingerprints of the TLS client and server (JA3/JA4). As most traffic is now encrypted and [TLS inspection](../secure-transport/tls-inspection.md) is costly and sometimes impossible, ETA is how defenders keep visibility. It cannot read content, so it does not replace deep inspection where that is feasible, but it reliably detects many threats, malware with distinctive TLS fingerprints, [C2 beaconing](beaconing-detection/README.md), connections to bad destinations, by behavior and metadata alone.

## Prerequisites

- [TLS in network security](../secure-transport/tls-in-network-security.md): what TLS exposes and hides.
- [Beaconing detection](beaconing-detection/README.md) and [flow monitoring](flow-monitoring.md): behavioral signals ETA builds on.
- [Zeek](zeek.md): extracts the TLS/certificate metadata ETA uses.

## Core concepts

### Definition

*Encrypted traffic analysis* is the detection and classification of threats in encrypted traffic using observable metadata and behavior rather than decrypted content. It relies on the fact that encryption protects the payload but leaves the envelope, addresses, names, sizes, timing and handshake details, visible.

### Analogy

ETA is reading sealed letters without opening them. You cannot see the text, but you can see the addresses, the sender's distinctive handwriting and stationery (TLS fingerprint), how thick each letter is and how often they are sent (size and timing), and whose seal is on them (certificate). A spy sending a coded note every evening in an unusual envelope to the same foreign address is recognizable without ever breaking the seal.

The analogy holds closely; it breaks only in that network "envelopes" expose consistent, machine-readable features (fingerprints) that make automated recognition far more reliable than judging handwriting.

### What encryption leaves exposed

| Exposed metadata | What it reveals |
| --- | --- |
| Destination IP and port | Who is contacted (reputation, known-bad) |
| SNI (server name) | The hostname requested, unless [Encrypted Client Hello](../secure-transport/tls-in-network-security.md) is used |
| Certificate (ssl/x509) | Issuer, validity, self-signed, mismatched names, shared across bad infrastructure |
| JA3/JA4 fingerprints | A hash of the TLS client's (or server's) handshake parameters, often distinctive to a tool or malware |
| Packet sizes and timing | Beaconing, interactive vs bulk, traffic classification |
| Flow volume and direction | Exfiltration, download, upload patterns |

### TLS fingerprinting (JA3/JA4)

A TLS client reveals, in its unencrypted ClientHello, the set and order of its supported versions, cipher suites, extensions and curves. These choices differ between implementations, so a hash of them (*JA3*, and the newer, more robust *JA4*) acts as a fingerprint of the client software. Malware and attacker tools often have fingerprints distinct from ordinary browsers, and the same tool produces the same fingerprint across infections, so matching JA3/JA4 against known-bad fingerprints flags malicious TLS clients without decryption. Server-side fingerprints (JA3S/JA4S) similarly characterize the server.

### Behavioral signals

Independent of fingerprints, behavior betrays threats in encrypted traffic:

- *Beaconing*: regular check-ins to one destination, the [tested detector](beaconing-detection/README.md) works entirely on metadata.
- *Destination reputation*: new, rare or known-bad IPs and domains (from SNI).
- *Certificate anomalies*: self-signed certs on services that should have CA-signed ones, certificates reused across known-bad infrastructure, name mismatches.
- *Traffic shape*: interactive shells, file transfers and automated C2 have different size/timing profiles even when encrypted.

### ETA vs TLS inspection

[TLS inspection](../secure-transport/tls-inspection.md) decrypts to read content, gaining full visibility at the cost of a plaintext choke point, privacy issues, breakage and risk. ETA keeps traffic encrypted and reads only metadata, avoiding those costs but seeing less. They are not either/or: ETA covers the (growing) traffic you cannot or should not decrypt (pinned apps, privacy-sensitive categories, unmanaged devices), while inspection is reserved for where it is justified. As Encrypted Client Hello hides SNI and inspection gets harder, ETA's metadata and fingerprint signals become relatively more important.

## Worked example

Detecting C2 in encrypted traffic with ETA, combining this subarea's tools (conceptual, since Zeek is not installed here, but the behavioral detector is tested):

1. **Behavioral.** The [beaconing detector](beaconing-detection/README.md) runs on flow/`conn.log` records and flags `192.0.2.23 -> 203.0.113.80:443` as a beacon (score 0.96) purely from timing and size, despite the traffic being TLS. Tested output:

```text
192.0.2.23   203.0.113.80   443   290   299s   ...   0.96   <- beacon over HTTPS
```

2. **Fingerprint.** [Zeek](zeek.md)'s `ssl.log` records the JA3/JA4 fingerprint of the client on that connection. Matching it against a known-bad fingerprint list identifies the TLS client as a known C2 implant, not a browser, confirming the suspicion without decryption.
3. **Certificate.** The `x509.log` shows the server presented a self-signed certificate with a random name, on a destination with no reputation, another independent red flag.
4. **Decision.** Three independent encrypted-traffic signals (beacon behavior, malicious JA3/JA4, anomalous certificate) converge on the same connection, giving high confidence it is C2, all without ever reading the payload. The connection is then cut at [egress](../traffic-filtering/egress-filtering.md) and sinkholed via [protective DNS](../dns-security/protective-dns.md).

The example shows ETA's method: combine behavioral and metadata signals that encryption cannot hide, rather than trying to read content.

## Trade offs and when to use it

- **ETA vs decryption.** ETA keeps privacy and avoids the inspection choke point but sees only metadata; decryption sees content but at real cost and sometimes impossibly. Use ETA as the default for encrypted traffic and reserve decryption for where it is justified and feasible.
- **Fingerprints age.** JA3/JA4 fingerprints change as software updates and attackers deliberately randomize them; they are strong signals but not permanent. Combine with behavior and reputation.
- **False positives.** Legitimate automation also beacons and some tools share fingerprints with benign software; corroborate multiple signals and use allow lists.
- **ECH and privacy trends** reduce SNI visibility over time, shifting weight to fingerprints, timing and destination reputation. Plan for less metadata, not more.

## Common mistakes

- **Assuming encryption blinds detection entirely.** Metadata and behavior remain. Fix: invest in ETA (fingerprints, beaconing, reputation, certificate anomalies).
- **Relying on a single signal.** One JA3 match or one beacon score can mislead. Fix: converge multiple independent signals.
- **Treating JA3/JA4 as permanent identifiers.** They change and can be randomized. Fix: combine with behavior and keep fingerprint lists updated.
- **Ignoring certificate metadata.** Self-signed and reused certs are strong flags. Fix: analyze ssl.log/x509.log.
- **Defaulting to decrypt everything.** Costly, privacy-invasive, sometimes impossible. Fix: ETA first, decrypt selectively where justified.

## Practice

1. What does encrypted traffic analysis use instead of decrypted content?
2. What is a JA3/JA4 fingerprint, and why can it identify malware over TLS?
3. Why does beaconing detection work on encrypted traffic?
4. How do ETA and TLS inspection relate, rather than compete?
5. Why does Encrypted Client Hello increase the relative importance of fingerprints and behavior?

### Answers

1. Observable metadata and behavior that encryption leaves exposed: destination, SNI, certificate details, TLS client/server fingerprints, and packet sizes, timing and volumes.
2. A hash of the TLS client's handshake choices (versions, cipher suites, extensions, curves) sent unencrypted in the ClientHello; malware tools often have distinctive, consistent fingerprints different from browsers, so matching against known-bad fingerprints flags them without decryption.
3. Beaconing is a timing-and-size pattern (regular check-ins, constant sizes) visible as metadata regardless of payload encryption.
4. They are complementary: ETA reads metadata without decrypting and covers traffic that cannot or should not be decrypted; TLS inspection decrypts for full content where that is justified and feasible. ETA is the default, inspection selective.
5. ECH hides the SNI, removing one of the clearest metadata signals, so detection must lean more on TLS fingerprints, timing/size behavior and destination reputation that remain visible.

## Further reading

- JA3 and JA4 TLS fingerprinting: https://github.com/FoxIO-LLC/ja4
- Cisco, Encrypted Traffic Analytics white papers (the origin of the ETA term).
- [Zeek](zeek.md) ssl.log/x509.log and [beaconing detection](beaconing-detection/README.md) for the data and behavioral method.
- RFC 9849, TLS Encrypted Client Hello (2026), for the SNI-hiding trend: https://www.rfc-editor.org/rfc/rfc9849
