# Firewall rule design

## Summary

This note turns the firewall policy model into concrete, tested rules. It covers the order of a well-formed rule set, stateful matching, anti-spoofing, rate limiting and logging, using a real nftables ruleset loaded in the [network security lab](../../foundations/network-security-lab/README.md). It then shows how rule sets decay into anomalies (shadowed, redundant and overly broad rules) and provides a script that audits an access control list for them. The goal is the judgment to read a rule set and see both what it permits and what it accidentally permits.

## Prerequisites

- [Firewalls](../firewalls.md): the conceptual model of stateless, stateful and next-generation firewalls.
- [Network segmentation](../../architecture/network-segmentation.md): where rule sets come from (the flow matrix).
- The [network security lab](../../foundations/network-security-lab/README.md) to run the examples.

## Core concepts

### Definition

A *firewall rule set* is an ordered list of rules, each matching some traffic and assigning an action. For a first-match firewall (nftables, iptables, most router ACLs, most cloud security groups evaluate differently), the first matching rule wins, so order is part of the logic, not a detail.

### Analogy

A rule set is like the triage instructions at a clinic door, read top to bottom: "chest pain, go straight in; high fever, room two; everyone else, waiting room". If "everyone else" were written first, nobody would ever reach the chest-pain rule. A rule placed below a broader rule above it is dead text.

### The shape of a good rule set

Order from most specific and cheapest to most general:

1. **Fast path for existing connections.** `ct state established,related accept`. Most packets match here, so it goes first for performance.
2. **Drop clearly bad packets.** `ct state invalid drop`, and anything that fails sanity checks.
3. **Anti-spoofing.** Drop packets arriving on an interface with a source address that cannot legitimately come from there (see [IP spoofing and source validation](../../core-protocols/ip-spoofing-and-source-validation.md)).
4. **Explicit allows for new connections**, narrowest first, in the intended direction only.
5. **Rate limits** for scarce or abusable services.
6. **Logging of the remainder**, rate-limited.
7. **Default deny** as the chain policy.

### The baseline ruleset

The file [scripts/fw-baseline.nft](scripts/fw-baseline.nft) implements this for the lab firewall. The important parts:

```
chain forward {
    type filter hook forward priority filter; policy drop;      # default deny
    ct state established,related accept                          # fast path for replies
    ct state invalid drop
    iifname "eth0" ip saddr 198.51.100.0/24 drop                 # anti-spoofing: inside source from outside
    iifname "eth0" oifname "eth1" ip daddr 198.51.100.20 tcp dport 443 ct state new accept   # public web
    iifname "eth0" oifname "eth1" ip saddr 192.0.2.10 ip daddr 198.51.100.20 tcp dport 22 ct state new accept  # admin ssh
    ...
    limit rate 10/minute log prefix "fw-forward-drop: " level info
    counter comment "dropped by default policy"
}
```

Every allow rule names the incoming interface, the outgoing interface, the exact destination, the exact port and `ct state new`. This is least privilege expressed in nftables.

### State and the order trap for ICMP

One subtlety the lab exposed. A naive input chain puts `ct state established,related accept` first and a rate limit on echo requests later:

```
ct state established,related accept
ip protocol icmp icmp type echo-request limit rate 5/second accept   # wrong: rarely runs
```

This does not limit a ping flood. Linux connection tracking groups echo requests that share an ICMP identifier into one "connection", so after the first packet the rest match `established` and the rate limit never sees them. The fix is to rate-limit *before* the state rule:

```
icmp type echo-request limit rate over 5/second burst 10 packets drop   # correct
ct state established,related accept
```

Tested in the lab (nftables 1.0.2, kernel 6.8, 2026-10): sending 50 echo requests at 20 per second through the corrected firewall, 22 arrive (the burst of 10 plus 5 per second over the 2.5 second run) and 28 are dropped. With the naive order, all 50 arrive. The lesson generalizes: a rule's position relative to the state rules changes whether it runs at all.

### Rule set anomalies

As rule sets grow, they develop anomalies. The classic classification (Al-Shaer and Hamed, 2005):

| Anomaly | Definition | Consequence |
| --- | --- | --- |
| Shadowing | An earlier rule matches all traffic of a later rule, with the opposite action | The later rule never fires; policy does not match intent |
| Redundancy | An earlier rule matches all traffic of a later rule, with the same action | The later rule is dead weight; removing it changes nothing |
| Generalization | A later rule is broader than an earlier one with the opposite action | Often intended (an exception before a general rule), but worth confirming |
| Correlation | Two rules partly overlap with opposite actions | The outcome depends on their order |

### Auditing a rule set

The script [scripts/audit-acl.py](scripts/audit-acl.py) reads a simple access control list and reports these anomalies plus two risk heuristics: rules that open a wide port range to any source, and rules that expose a high-risk admin service (SSH, RDP, SMB, WinRM) to any source.

## Worked example

The sample list [scripts/sample-acl.csv](scripts/sample-acl.csv) contains deliberate mistakes. Running the audit (Python 3.10, 2026-10):

```text
SHADOWED    rule 30 (deny 192.0.2.66/32 -> 198.51.100.20/32 tcp/22) never matches, rule 20 (allow 192.0.2.0/24 -> 198.51.100.0/24 tcp/22) catches all of its traffic first
REDUNDANT   rule 40 (allow 192.0.2.10/32 -> 198.51.100.20/32 tcp/22) never matches, rule 20 (allow 192.0.2.0/24 -> 198.51.100.0/24 tcp/22) catches all of its traffic first
GENERALIZES rule 50 (allow 0.0.0.0/0 -> 198.51.100.0/24 tcp/1-65535) is a wider version of rule 30 (deny 192.0.2.66/32 -> 198.51.100.20/32 tcp/22) with the opposite action (check intent)
TOO BROAD   rule 50 (allow 0.0.0.0/0 -> 198.51.100.0/24 tcp/1-65535) allows a large port range from any source
REDUNDANT   rule 60 (allow 0.0.0.0/0 -> 198.51.100.30/32 tcp/3389) never matches, rule 50 (allow 0.0.0.0/0 -> 198.51.100.0/24 tcp/1-65535) catches all of its traffic first
EXPOSED     rule 60 (allow 0.0.0.0/0 -> 198.51.100.30/32 tcp/3389) opens RDP (3389) to any source

9 rules, 7 findings
```

Reading the findings:

- **Rule 30** was meant to block the untrusted host from SSH, but rule 20 already allows the whole `/24` to SSH. The intended deny is dead. Fix: put the deny above rule 20, or narrow rule 20.
- **Rule 40** duplicates what rule 20 already allows. Harmless but misleading.
- **Rule 50** opens every TCP port to the whole server subnet from anywhere, which also makes the specific rule 60 redundant and exposes RDP to the internet. This single rule undoes most of the policy.

The audit catches in seconds what is easy to miss when reading 200 rules by eye.

## Trade offs and when to use it

- **First-match lists vs policy objects.** Hand-ordered lists are transparent but fragile at scale. Object-based systems (address groups, service groups, cloud security groups) are easier to maintain but hide ordering and overlap, which is why an audit is still needed.
- **Dropping invalid early vs logging it.** Dropping `invalid` early is cheap and safe, but it can hide misconfigurations (asymmetric routing). Log a sample before dropping if you are unsure.
- **Rate limiting vs blocking.** A rate limit keeps a service usable under light abuse but passes some attack traffic. A hard block is cleaner but can lock out legitimate bursts. Choose per service.

## Common mistakes

- **Putting a broad allow above specific denies.** Fix: order specific before general; audit for shadowing.
- **Rate limits placed after the state-accept rule.** Fix: rate-limit before the connection becomes "established", as shown above.
- **Allowing replies with broad rules instead of using state.** Fix: one `established,related accept` rule plus rules for new connections only.
- **No anti-spoofing on edge interfaces.** Fix: drop packets whose source cannot arrive on that interface; see source validation.
- **Never auditing.** Fix: run an anomaly audit in change review and periodically; treat findings as defects.

## Practice

1. Why must the `established,related accept` rule usually come first for performance but the echo-request rate limit come before it for correctness?
2. In the sample ACL, how would you fix the shadowed rule 30 without weakening rule 20 for the rest of the subnet?
3. What is the difference between a shadowed and a redundant rule?
4. Why is a stateless anti-spoofing drop safe to place high in the chain?
5. Why does an object-based firewall still need anomaly auditing?

### Answers

1. Most packets belong to existing connections, so matching them first is fast; but connection tracking folds repeated echo requests into one "established" flow, so a limit placed after the state rule never sees the flood.
2. Move the deny for the untrusted host above rule 20, so it is evaluated first; the rest of the `/24` still matches rule 20 below it.
3. Both never fire because an earlier rule covers them. Shadowed has the opposite action (a real policy error); redundant has the same action (harmless clutter).
4. It matches on fixed header fields (interface and source network) regardless of state, and it only drops traffic that is illegitimate by definition, so it cannot block valid connections.
5. Groups and objects hide overlap and precedence; two overlapping rules with opposite actions can still exist, and broad address groups can still expose risky services.

## Further reading

- Al-Shaer, E. and Hamed, H., "Conflict Classification and Analysis of Distributed Firewall Policies", IEEE JSAC 23(10), 2005. The source of the anomaly taxonomy.
- nftables wiki, especially the pages on stateful objects, sets and rate limiting: https://wiki.nftables.org/
- NIST SP 800-41 Rev. 1, Guidelines on Firewalls and Firewall Policy (2009): https://doi.org/10.6028/NIST.SP.800-41r1
