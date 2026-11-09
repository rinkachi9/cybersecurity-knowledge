# Ping of death

## Summary

The ping of death is a historic denial-of-service attack that crashed or froze a target by sending a malformed ICMP echo request that, once reassembled from its fragments, exceeded the maximum legal size of an IP packet. Vulnerable 1990s network stacks allocated a buffer for the normal maximum and overflowed it during reassembly, corrupting memory and crashing the system. A single packet was enough. It is important mainly as the clearest example of a whole class: a malformed input that triggers a software defect rather than exhausting a resource. The specific bug was fixed decades ago, but oversized and overlapping fragments remain a thing network stacks and firewalls must handle correctly.

## Prerequisites

- [Denial of service](denial-of-service.md): the general model; ping of death is the "software correctness" class.
- IP fragmentation and reassembly.
- ICMP echo (the `ping` request and reply).

Authorized use only. This note explains the historic mechanism so the class of defect is understood; it provides no exploit.

## Core concepts

### Definition

The *ping of death* is a denial-of-service attack that sends an ICMP echo request whose fragments reassemble into an IP packet larger than the 65,535-byte maximum that the 16-bit total-length field of the IPv4 header can describe. On a vulnerable system, reassembly wrote past the end of the buffer reserved for a maximum-size packet, corrupting kernel memory and causing a crash, hang or reboot.

### Analogy

Imagine a mail sorting machine built on the assumption that no parcel is longer than one meter, with a one-meter slot milled into it. Someone ships a three-meter parcel in sections labeled "piece 1 of 3" and so on. The machine dutifully reassembles the sections, the result jams three times past the end of the slot, and the machine breaks. The flaw is not the volume of mail; it is the single impossible parcel and the machine's failure to check the total length before building it.

The analogy holds well: the defect is trusting the declared pieces without validating the assembled whole. It breaks only in that a real packet's "length" is a header field an attacker controls, so the lie is trivial to tell.

### Mechanism

IP packets larger than a link's maximum transmission unit are split into fragments, each carrying an offset saying where it belongs in the reassembled packet. The receiver collects fragments and reassembles them. The attack crafts fragments whose last fragment's offset plus length exceeds 65,535 bytes. A correct stack notices the total is illegal and discards it. A vulnerable stack reserved exactly 65,535 bytes and copied each fragment to its offset, so the final fragment wrote beyond the buffer.

The attack is one instance of *fragmentation-based attacks*, a family that also includes overlapping fragments (teardrop), tiny fragments that split a header across fragments to evade filters, and fragment floods that exhaust reassembly buffers. All of them exploit the gap between what the fragmentation rules allow a sender to claim and what a receiver safely handles.

### Why it is fixed, and what remains

Operating systems added the missing length check in the late 1990s, and the ping of death in its original form does not work against any current system. What remains relevant:

- Reassembly must still bound total size and reject illegal offsets. This is now standard, but new stacks (embedded devices, IoT, custom appliances) reintroduce such bugs periodically.
- Overlapping and tiny fragments are still used to evade inspection devices, because a firewall and an endpoint can reassemble fragments differently and disagree about what the packet contains.
- Fragment reassembly consumes memory, which is itself a resource an attacker can target.

## Worked example

The defense is a correct, bounded reassembly path in the network stack. Its effect is observable from the sending side: a modern stack will not even construct an illegal packet. On the [network security lab](../../foundations/network-security-lab/README.md) (kernel 6.8, 2026-10), the largest legal echo request is accepted and one byte more is rejected by the sender's own stack before anything goes on the wire:

```bash
ping -c1 -s 65507 192.0.2.1   # 65,507 data + 8 ICMP + 20 IP = 65,535, the maximum
ping -c1 -s 65508 192.0.2.1   # one byte over
```

Output:

```text
# 65,507 bytes of payload: a legal maximum-size packet, delivered as fragments and reassembled
65515 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=0.383 ms
# 65,508 bytes: refused locally, never sent
ping: local error: message too long, mtu=1500
```

Reading this: the stack enforces the 65,535-byte ceiling at both ends. The legal packet is fragmented across the 1,500-byte link and reassembled correctly; the illegal one is rejected at the source. A receiving stack applies the same bound during reassembly, which is the actual ping-of-death defense. Firewalls add a second layer by validating or dropping malformed and overlapping fragments and by limiting the memory spent on reassembly.

## Trade offs and when to use it

- **Validate fragments at the firewall vs pass them to the endpoint.** Validating (or reassembling) at the firewall catches evasion by overlapping and tiny fragments, at the cost of state and CPU on the firewall. Passing them through relies entirely on the endpoint reassembling safely.
- **Rate-limit or bound reassembly memory.** Needed against fragment-flood resource exhaustion, with a small risk of dropping legitimate fragmented traffic on lossy paths.
- **Patch, do not work around.** The only real fix for the correctness class is a correct stack; firewall rules are defense in depth, not a substitute for patching a vulnerable device.

Ping of death itself is not something you "defend against" today beyond keeping systems patched; its value is as the exemplar that teaches the class.

## Common mistakes

- **Assuming malformed-packet attacks are purely historic.** New embedded and IoT stacks reintroduce reassembly bugs. Fix: include fragmentation handling in testing and keep firmware patched.
- **Blocking all fragments.** Breaks legitimate large UDP (DNS over UDP, some VPNs). Fix: validate and bound fragments rather than dropping all.
- **Ignoring the firewall-endpoint reassembly mismatch.** An evasive attacker exploits the two disagreeing. Fix: reassemble or normalize fragments at the inspection point.
- **Treating a crash bug as low priority because it is "only" DoS.** A remotely triggerable crash can be chained or used as cover. Fix: patch promptly.

## Practice

1. What illegal condition does the ping of death create, and why did it crash vulnerable systems?
2. Why was a single packet enough, unlike a flood?
3. Name two other fragmentation-based attacks in the same family.
4. Why does blocking all fragments cause operational problems?
5. Why can an attacker and defender disagree about a fragmented packet's contents, and how is that abused?

### Answers

1. Fragments that reassemble to more than 65,535 bytes, the IPv4 maximum. Vulnerable stacks reserved a maximum-size buffer and wrote past its end during reassembly, corrupting memory.
2. It exploits a software defect (a buffer overflow in reassembly), not a resource limit, so one malformed packet triggers the crash rather than needing volume.
3. Teardrop (overlapping fragments), tiny-fragment header splitting, and fragment floods that exhaust reassembly memory.
4. Legitimate traffic is sometimes fragmented (large UDP such as DNS, some tunnels), so dropping all fragments breaks it.
5. A firewall and an endpoint may reassemble overlapping or tiny fragments differently, so the firewall inspects one payload while the endpoint sees another; attackers use this to slip content past inspection.

## Further reading

- CERT Advisory CA-1996-26, Denial-of-Service Attack via ping (the original ping of death advisory).
- RFC 791, Internet Protocol (1981), section on fragmentation and reassembly, and the 16-bit total-length field: https://www.rfc-editor.org/rfc/rfc791
- RFC 1858, Security Considerations for IP Fragment Filtering (1995), on tiny and overlapping fragments: https://www.rfc-editor.org/rfc/rfc1858
- MITRE ATT&CK, Endpoint Denial of Service (T1499): https://attack.mitre.org/techniques/T1499/
