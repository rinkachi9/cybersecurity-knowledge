# SYN flood

## Summary

A SYN flood is a denial-of-service technique that exhausts a server's table of half-open TCP connections. The attacker starts many TCP handshakes by sending SYN packets but never completes them, so each one leaves the server holding reserved state while it waits for a reply that never comes. When the backlog fills, the server refuses new legitimate connections. It is efficient for the attacker because a tiny packet ties up a comparatively expensive resource. The standard defense, SYN cookies, removes the need to hold any state until the handshake is proven genuine, which is why a modern, correctly configured server is largely immune.

## Prerequisites

- [Denial of service](denial-of-service.md): the general model this is an instance of.
- The TCP three-way handshake (SYN, SYN-ACK, ACK).
- [Network threat model](../../foundations/network-threat-model.md): off-path spoofing.

Authorized use only. The mechanism is described so it can be detected and mitigated; this note generates no attack traffic.

## Core concepts

### Definition

A *SYN flood* sends a high rate of TCP SYN segments, often with spoofed source addresses, to a listening port, with no intention of completing the handshakes. It targets the *connection backlog*: the kernel's queue of connections that have received a SYN and sent a SYN-ACK but not yet received the final ACK (the SYN-RECEIVED state). It is tracked as part of MITRE ATT&CK Endpoint Denial of Service (T1499).

### Analogy

Think of a receptionist who, on each phone call, writes down the caller's details and holds the line open waiting for them to confirm an appointment. An attacker calls hundreds of times, gives details, then goes silent. Every line is held open waiting for a confirmation that never comes, and real callers get a busy signal. SYN cookies are the receptionist's trick of not writing anything down: they hand the caller a reference number computed on the spot and only open a file when the caller calls back and repeats it.

The analogy breaks because the "reference number" must be unforgeable and self-verifying without storage, which is a cryptographic trick, not just a memory aid.

### Mechanism

```mermaid
sequenceDiagram
    participant A as Attacker (spoofed sources)
    participant S as Server
    A->>S: SYN (source spoofed)
    S->>S: allocate backlog entry (SYN-RECEIVED)
    S-->>A: SYN-ACK (goes to the spoofed address, or nowhere)
    Note over S: waits for ACK that never comes;<br/>entry held until timeout, retransmits SYN-ACK
    Note over A,S: repeat fast enough to keep the backlog full
```

The server reserves a backlog slot and retransmits the SYN-ACK several times before timing out (on Linux, controlled by `tcp_synack_retries`, default 5, which is tens of seconds). While the slot is held, it counts against the backlog limit. If SYNs arrive faster than slots free up, the backlog stays full and new connections are dropped. Spoofing the source serves two purposes: it hides the attacker and ensures the SYN-ACK goes to an address that will not send a reset, so the slot is held for the full timeout.

### SYN cookies

A *SYN cookie* lets the server respond to a SYN without allocating any backlog entry. Instead of storing the connection state, the server encodes it into the initial sequence number of the SYN-ACK: a value computed from the connection's addresses and ports, a slowly changing timestamp, and a secret, hashed together. The server then forgets the connection entirely. When a genuine client sends the final ACK, its acknowledgment number is the cookie plus one; the server recomputes the cookie, checks it matches, and reconstructs the connection on the spot. A spoofed SYN never produces a matching ACK, so it costs the server nothing after the SYN-ACK is sent.

The trade-off is that a few TCP options cannot be fully preserved in the cookie, so cookies are typically enabled to trigger only when the backlog is actually under pressure (`net.ipv4.tcp_syncookies = 1` on Linux does exactly this). On this reference host that default is already set.

## Worked example

Inspecting the defensive configuration on a Linux host (kernel 6.8, 2026-10):

```bash
sysctl net.ipv4.tcp_syncookies net.ipv4.tcp_max_syn_backlog net.ipv4.tcp_synack_retries
```

Output:

```text
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_synack_retries = 5
```

Reading this: SYN cookies are enabled and activate when the 1,024-entry backlog is full, so the host does not fall over when the backlog is exhausted; it switches to stateless handling for new SYNs. Lowering `tcp_synack_retries` makes abandoned half-open entries time out sooner, freeing slots faster during an attack. A SYN flood against this host degrades gracefully rather than denying service outright, as long as the link itself is not also saturated.

On an infrastructure scale, the same idea appears as a *stateless front-end*: a load balancer or scrubbing device completes the handshake (or validates it with cookies) before passing a proven connection to the real server, so the server's state table is never exposed to raw SYNs.

## Trade offs and when to use it

Defenses, with costs:

- **SYN cookies (enable-on-pressure).** Nearly free, preserves service under attack, loses a few TCP options only while active. This should be on everywhere.
- **Larger backlog and shorter SYN-ACK timeout.** Buys time and frees slots faster, but larger tables cost memory and a very short timeout can drop clients on lossy links.
- **Stateless validation upstream (load balancer, scrubber).** Protects the whole fleet, at the cost of a device in the path.
- **Rate limiting new SYNs per source.** Helps against a single source, useless against spoofed, distributed SYNs.

A SYN flood that also saturates the link becomes a volumetric problem, so host-level SYN defenses must be paired with upstream capacity for large attacks.

## Common mistakes

- **Disabling SYN cookies for performance.** Fix: leave the enable-on-pressure default on; it does not affect normal operation.
- **Relying on per-source rate limits against spoofed floods.** The sources are forged and distributed. Fix: SYN cookies, which do not depend on identifying the source.
- **A stateful firewall with no SYN protection in front of the server.** The firewall's state table becomes the first thing to fill. Fix: SYN cookies or validation on the firewall itself.
- **Forgetting the link.** SYN packets are small, but a large distributed flood can still fill bandwidth. Fix: upstream scrubbing for large attacks.

## Practice

1. Which specific resource does a SYN flood exhaust, and in which TCP state are the entries held?
2. How does a SYN cookie let a server answer a SYN without storing anything?
3. Why does the attacker spoof the source address?
4. Why does the Linux default enable SYN cookies only when the backlog is full rather than always?
5. Why do per-source rate limits fail against a typical SYN flood?

### Answers

1. The connection backlog, the queue of half-open connections in the SYN-RECEIVED state.
2. It encodes the connection state into the SYN-ACK's initial sequence number (a keyed hash of the addresses, ports and a timestamp) and forgets the connection; a genuine final ACK carries that value back and lets the server reconstruct the connection.
3. To hide the attacker and to make the SYN-ACK go to an address that will not reply with a reset, so the backlog slot is held for the full timeout.
4. Because cookies cannot preserve every TCP option; enabling them only under pressure keeps full option support during normal operation and switches to stateless handling only when needed.
5. The source addresses are spoofed and spread across many values, so there is no stable source to rate-limit.

## Further reading

- RFC 4987, TCP SYN Flooding Attacks and Common Mitigations (2007): https://www.rfc-editor.org/rfc/rfc4987
- Bernstein, D.J., SYN cookies, the original description: https://cr.yp.to/syncookies.html
- Linux kernel documentation, `Documentation/networking/ip-sysctl.rst`, for `tcp_syncookies`, `tcp_max_syn_backlog`, `tcp_synack_retries`.
- MITRE ATT&CK, Endpoint Denial of Service (T1499): https://attack.mitre.org/techniques/T1499/
