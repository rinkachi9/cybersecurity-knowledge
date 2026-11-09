# TCP attacks

## Summary

TCP provides a reliable, ordered byte stream on top of unreliable IP, using sequence numbers to order data and a handshake to set up connections. Several attacks exploit the gap between what TCP assumes and what an attacker can forge: *RST injection* tears down a connection with a forged reset, *session hijacking* injects data into an established connection, and *SYN flooding* exhausts connection state (covered in its own note). Historically these needed only guessable sequence numbers; modern stacks randomize the initial sequence number and validate incoming segments more strictly (RFC 5961), which makes blind off-path attacks hard but not impossible, and leaves on-path attackers able to do all of them. The defense that actually closes the content attacks is end-to-end authentication and encryption.

## Prerequisites

- [Network threat model](../foundations/network-threat-model.md): off-path vs on-path.
- [Protocol design weaknesses](../foundations/protocol-design-weaknesses.md): predictable fields.
- The TCP handshake, sequence and acknowledgment numbers, the RST flag.
- [SYN flood](../network-attacks/denial-of-service/syn-flood.md) for the state-exhaustion attack.

Authorized use only.

## Core concepts

### Definition

A *TCP attack* in this note is one that forges or injects TCP segments to disrupt or take over a connection. The key fields an attacker must get right are the four-tuple (source and destination address and port) and the *sequence* and *acknowledgment* numbers, which must fall within the receiver's current window for a segment to be accepted.

### Analogy

A TCP connection is like a numbered conversation where each party says "this is message 5,001, I heard up to your 7,200". To butt in convincingly, an impostor must know roughly which numbers are current. If the numbers were predictable (say they always started at 1), anyone could join; randomizing the starting number is like starting each conversation at a secret, unguessable count, so an outsider who cannot hear the conversation can only guess.

The analogy breaks because an on-path attacker *can* hear the numbers, so randomization defends only against those who cannot see the traffic.

### Attack 1: RST injection (connection reset)

A TCP segment with the RST flag tells the receiver to tear down the connection immediately. An attacker who forges a RST with the right four-tuple and an acceptable sequence number can drop a connection. On-path, this is trivial and is used for censorship and interference. Off-path, it requires guessing the sequence number within the window; RFC 5961 tightened the rules (an off-path RST must match the next expected sequence number exactly, not just fall in the window) to make blind resets much harder. It is tracked as part of MITRE ATT&CK and is the mechanism behind some nation-scale connection interference.

### Attack 2: session hijacking and data injection

If an attacker can inject a segment with an in-window sequence number carrying data, the receiver accepts it as part of the stream. On-path, this allows inserting commands into an unauthenticated session (classic Telnet or FTP hijacking) or desynchronizing the two ends. Off-path, it faces the same sequence-guessing barrier as RST injection, made impractical by ISN randomization. The decisive defense is TLS: injected bytes fail the integrity check and are discarded.

### Attack 3: SYN flooding

Covered fully in [SYN flood](../network-attacks/denial-of-service/syn-flood.md): the attacker exhausts the half-open connection backlog. Mitigated by SYN cookies.

### The historical weakness and its fix

Early stacks used predictable initial sequence numbers (ISNs), sometimes incrementing by a fixed amount, so an off-path attacker could guess them and inject or reset blindly (the 1990s Mitnick-style attacks). The fixes:

- **Randomized ISNs** (RFC 6528): each connection starts at an unpredictable number derived from a secret and the connection four-tuple, so off-path guessing fails.
- **Stricter segment validation** (RFC 5961): narrows which off-path RST, SYN and data segments are accepted, closing blind injection windows.
- **TCP timestamps and PAWS**: add another field that must match, incidentally raising the bar for blind injection.

These are standard in modern kernels; on this reference host TCP timestamps are enabled (`net.ipv4.tcp_timestamps = 1`).

## Worked example

Observe the handshake and a normal teardown in a capture, then reason about where an attacker would have to intervene. From the [packet capture note](../monitoring-and-detection/packet-capture-analysis/README.md) sample (tcpdump 4.99.1):

```text
192.0.2.10.51515 > 198.51.100.20.80: Flags [S], seq 1000
198.51.100.20.80 > 192.0.2.10.51515: Flags [S.], seq 5000, ack 1001
192.0.2.10.51515 > 198.51.100.20.80: Flags [.], ack 5001
... data ...
192.0.2.10.51515 > 198.51.100.20.80: Flags [F.], seq 76, ack 44
```

To reset this connection, an attacker must forge a segment with the exact four-tuple (`192.0.2.10:51515` to `198.51.100.20:80`), the RST flag, and under RFC 5961 the receiver's next expected sequence number. An on-path attacker reads these values from the traffic and succeeds instantly. An off-path attacker must guess the sequence number out of roughly four billion possibilities, within the window, before the connection closes naturally, which is why blind RST attacks are impractical against a modern stack but blind attacks against protocols with long-lived connections and predictable ports (historically BGP between routers) were a real concern, addressed with TCP-AO/MD5 authentication of the segments.

The lesson: randomization and RFC 5961 defend against the off-path attacker; only authenticated/encrypted transport defends against the on-path one.

## Trade offs and when to use it

- **TCP-AO / TCP-MD5** authenticate TCP segments themselves, used to protect long-lived infrastructure sessions such as BGP from injection and reset. Cost: key management between peers; TCP-AO (RFC 5925) supersedes the weaker MD5 option.
- **TLS** protects application data from injection and tampering but not the TCP control segments; a RST can still tear down the TCP connection under TLS (seen as an abrupt disconnect), so availability is not fully protected.
- **Relying on ISN randomization alone** defends off-path only; it is free and on by default, but it is not a substitute for authentication against on-path adversaries.

## Common mistakes

- **Assuming TLS prevents connection resets.** TLS protects the data stream, not the TCP layer; a forged RST still drops the connection. Fix: for critical long-lived sessions, authenticate the TCP layer (TCP-AO) or detect and re-establish.
- **Running unauthenticated cleartext sessions (Telnet, FTP) where injection matters.** On-path hijacking inserts commands directly. Fix: SSH, TLS.
- **Old stacks with predictable ISNs on exposed devices.** Embedded and legacy systems may still be guessable. Fix: patch or replace; isolate.
- **Exposing infrastructure TCP sessions (BGP) without segment authentication.** Fix: TCP-AO and ACLs restricting peers.

## Practice

1. Which fields must an attacker get right for a forged TCP segment to be accepted?
2. How does RFC 5961 make blind off-path RST injection harder than it was?
3. Why does ISN randomization not protect against an on-path attacker?
4. Why does TLS not prevent a connection reset?
5. What protects long-lived BGP sessions between routers from injection, and why is it needed there specifically?

### Answers

1. The four-tuple (source and destination IP and port), the correct flags, and a sequence/acknowledgment number within the receiver's current window (for RST, under RFC 5961, matching the next expected sequence number).
2. It requires an off-path RST to match the exact next expected sequence number rather than merely falling anywhere in the window, shrinking the chance of a blind guess succeeding.
3. An on-path attacker can read the current sequence numbers directly from the traffic, so there is nothing to guess.
4. TLS protects the application data stream's integrity, but the TCP control segments (including RST) are below it and unauthenticated, so a forged RST still tears down the connection.
5. TCP-AO (or legacy TCP-MD5) authenticates the segments; BGP sessions are long-lived, between known peers on predictable ports, making them attractive targets for blind reset or injection that would disrupt routing.

## Further reading

- RFC 793 / RFC 9293, Transmission Control Protocol (the base specification): https://www.rfc-editor.org/rfc/rfc9293
- RFC 5961, Improving TCP's Robustness to Blind In-Window Attacks (2010): https://www.rfc-editor.org/rfc/rfc5961
- RFC 6528, Defending Against Sequence Number Attacks (2012): https://www.rfc-editor.org/rfc/rfc6528
- RFC 5925, The TCP Authentication Option (2010): https://www.rfc-editor.org/rfc/rfc5925
- Bellovin, S., "Security Problems in the TCP/IP Protocol Suite" (1989), the original description of sequence-number attacks.
