# IP spoofing and source address validation

## Summary

IP spoofing is sending IP packets with a forged source address. The internet protocol lets any sender write any value in the source field, because IP was designed to route packets, not to verify who sent them. Spoofing enables reflection and amplification floods, blind injection against stateless services, and evasion of address-based access control. The defense is *source address validation*: networks drop packets whose source address could not legitimately have come from where they arrived. The main mechanisms are ingress filtering (BCP 38) at network edges and unicast Reverse Path Forwarding (uRPF) on routers and hosts. Source validation is a collective good: deploying it protects others from being attacked using your network.

## Prerequisites

- [Protocol design weaknesses](../foundations/protocol-design-weaknesses.md): unauthenticated source.
- [Network threat model](../foundations/network-threat-model.md): off-path and on-path attackers.
- [Denial of service](../network-attacks/denial-of-service/denial-of-service.md): reflection and amplification.

Authorized use only.

## Core concepts

### Definition

*IP spoofing* is the construction of IP packets with a source address other than the sender's own. *Source address validation* (SAV) is the practice of verifying, as close to the origin as possible, that a packet's source address is plausible for the interface or network it came from, and dropping it otherwise.

### Analogy

IP spoofing is like posting a letter with someone else's return address. The postal system delivers based on the destination and never checks the return address, so you can make mail appear to come from anyone, and any replies go to the forged address, not to you. Ingress filtering is the local post office refusing to accept outgoing mail whose return address is not one of the streets it serves.

The analogy breaks because, unlike a letter, a spoofed packet can be sent millions of times per second and can trigger a reply far larger than itself (reflection), turning the forged return address into a weapon.

### Why spoofing is useful to an attacker

- **Reflection and amplification.** Spoof the victim's address as the source of requests to open servers (DNS, NTP, memcached); the replies, often much larger, flood the victim. See [DDoS](../network-attacks/denial-of-service/distributed-denial-of-service.md).
- **Blind injection.** Against stateless or weakly randomized protocols, an off-path attacker can inject packets (forged DNS answers, forged TCP resets) that appear to come from a trusted address.
- **Hiding and evasion.** Obscuring the real origin, or impersonating an address that an ACL trusts.

Spoofing is limited by the fact that the attacker usually does not see the replies (they go to the forged address), so it suits one-way attacks: floods and injection, not two-way sessions.

### Defense 1: ingress filtering (BCP 38)

BCP 38 (RFC 2827) says each network should drop outbound packets whose source address does not belong to that network, and drop inbound packets claiming a source that lies inside the network. If every network did this, spoofing would be impossible. In practice adoption is incomplete, which is why reflection attacks persist. It is a collective defense: filtering your egress stops your network being used to attack others, and filtering your ingress stops outsiders impersonating your internal addresses.

### Defense 2: unicast Reverse Path Forwarding (uRPF)

uRPF (RFC 3704) automates source validation on a router: for each incoming packet, it checks the routing table to see whether the packet's source address is reachable back through the interface it arrived on.

- *Strict mode* drops the packet unless the best route back to its source is exactly the arrival interface. Correct on single-homed edges; breaks on asymmetric routing.
- *Loose mode* drops the packet only if the source has no route at all anywhere. Weaker, but safe where routing is asymmetric (multi-homed cores).

Linux implements this as `rp_filter`. On this reference host (checked 2026-10):

```text
net.ipv4.conf.all.rp_filter = 2      # 2 = loose mode
net.ipv4.conf.all.accept_source_route = 0   # source routing disabled
```

Loose mode (`2`) is the common default on multi-homed Linux hosts; strict mode (`1`) is used on simple single-homed edges. Source routing, an old option that lets the sender dictate the path and is a classic spoofing aid, is disabled by default.

### Related: disabling source routing and redirects

Two legacy IP features aid spoofing and redirection and are disabled on hardened systems: *source routing* (`accept_source_route = 0`) lets a sender choose the return path, helping replies reach a spoofer; *ICMP redirects* (`accept_redirects = 0` on this host) let a gateway change a host's routing table and can be abused to redirect traffic. See [ICMP security](icmp-security.md).

## Worked example

Reading the defensive posture of the reference Linux host (2026-10):

```bash
sysctl net.ipv4.conf.all.rp_filter net.ipv4.conf.all.accept_source_route net.ipv4.conf.all.accept_redirects
```

```text
net.ipv4.conf.all.rp_filter = 2
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
```

Interpretation: the host performs loose reverse-path checking (drops packets whose source has no route at all), ignores source-routed packets, and ignores ICMP redirects. For a single-homed server, tightening `rp_filter` to `1` (strict) would additionally drop any packet arriving on an interface that is not the best path back to its claimed source, which catches more spoofing at the cost of breaking multi-path setups. On routers, the equivalent is `ip verify unicast source reachable-via rx` (strict) or `any` (loose) in Cisco terms, applied on customer-facing interfaces per BCP 38.

A firewall also contributes: the lab's [baseline ruleset](../traffic-filtering/firewall-rule-design/scripts/fw-baseline.nft) includes an anti-spoofing rule that drops packets arriving on the outside interface claiming an inside source address, a per-device form of ingress filtering.

## Trade offs and when to use it

- **Strict vs loose uRPF.** Strict catches more but breaks asymmetric and multi-homed routing; loose is safe everywhere but only drops packets to non-existent sources. Use strict on single-homed edges, loose in multi-homed cores.
- **Ingress filtering is low-cost, collective-benefit.** It barely affects your own operations but protects the whole internet; the weak incentive (you protect others, not mainly yourself) is why adoption lags, not technical difficulty.
- **Source validation does not stop on-path spoofing.** An attacker already on the path can use real-looking addresses; SAV targets off-path spoofing and reflection.

## Common mistakes

- **No egress filtering.** Your network can be used for reflection attacks on others, and you may be blocklisted. Fix: BCP 38 egress filtering on all customer edges.
- **Strict uRPF on asymmetric links.** Drops legitimate traffic. Fix: loose mode, or per-interface tuning.
- **Leaving source routing or redirect acceptance on.** Aids spoofing and redirection. Fix: disable both (as this host does).
- **Trusting source IP for authentication.** ACLs that trust an internal address can be spoofed into by an off-path attacker if ingress filtering is absent. Fix: authenticate, do not trust addresses.

## Practice

1. Why does IP allow a sender to forge the source address at all?
2. What does BCP 38 ingress filtering require a network to drop?
3. What is the difference between strict and loose uRPF, and when does strict break?
4. Why is source validation described as a collective good with weak individual incentive?
5. Why does spoofing suit floods and injection but not two-way sessions?

### Answers

1. IP was designed to route packets by destination and includes no mechanism to verify the source field, so any sender can write any source address.
2. Outbound packets whose source does not belong to the network, and inbound packets claiming a source that is inside the network.
3. Strict drops a packet unless its best return route is exactly the arrival interface; loose drops only if the source has no route anywhere. Strict breaks on asymmetric or multi-homed routing where return paths differ from arrival interfaces.
4. Egress filtering mainly prevents your network from attacking others, so the benefit accrues to the wider internet rather than directly to the deploying network, weakening the incentive to deploy it.
5. The replies go to the forged source address, not to the attacker, so the attacker cannot complete a handshake or carry on a conversation; it only works where no reply needs to return to the real sender.

## Further reading

- BCP 38 / RFC 2827, Network Ingress Filtering (2000): https://www.rfc-editor.org/rfc/rfc2827
- BCP 84 / RFC 3704, Ingress Filtering for Multihomed Networks (2004), including uRPF modes: https://www.rfc-editor.org/rfc/rfc3704
- MANRS (Mutually Agreed Norms for Routing Security), the industry initiative for source validation and routing hygiene: https://www.manrs.org/
- Linux kernel `Documentation/networking/ip-sysctl.rst` for `rp_filter`, `accept_source_route`, `accept_redirects`.
