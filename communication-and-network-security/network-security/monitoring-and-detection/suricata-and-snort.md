# Suricata and Snort

## Summary

Suricata and Snort are the two dominant open-source network intrusion detection and prevention engines. They inspect traffic against *rules* (signatures) describing known-bad patterns and raise alerts, or, deployed inline, block the matching traffic. They are the signature-based layer of network detection: sharp and actionable against known threats, but blind to what no rule describes, which is why they pair with the descriptive, behavioral tools like [Zeek](zeek.md) and [flow monitoring](flow-monitoring.md). Understanding the rule language, how detection and prevention modes differ, and how rules are tuned is the practical core of running these engines well. The conceptual difference between detection (IDS) and prevention (IPS) is covered in the defensive-operations area; this note is the network-engine view.

## Prerequisites

- [IDS](../../../security-operations/defensive-operations/detection/ids/README.md) and [IPS](../../../security-operations/defensive-operations/detection/ips.md): the detection/prevention concepts.
- [Network security monitoring](network-security-monitoring.md): where alerts fit among data types.
- [Network scanning](../network-attacks/network-scanning.md) and the attacks these rules detect.

## Core concepts

### Definition

*Suricata* and *Snort* are network intrusion detection/prevention systems (NIDS/NIPS) that match network traffic against a ruleset of signatures and generate alerts (IDS mode) or drop matching traffic (inline IPS mode). Snort (by Cisco/Sourcefire) is the long-standing original; Suricata (by OISF) is a newer, multi-threaded engine with broadly compatible rule syntax and added capabilities.

### Analogy

These engines are a security guard with a thick book of mugshots and descriptions of known offenders, watching everyone pass and shouting (or stopping them) when someone matches a description. They are excellent at catching known offenders quickly, and useless against a criminal whose description is not in the book. That is the strength and the limit of signature detection: precise on the known, blind to the novel.

The analogy holds well; it breaks in that the "book" (ruleset) is updated continuously from threat intelligence, so the set of recognized patterns grows daily.

### The rule language

Suricata and Snort share a largely compatible rule format. A rule has an *action*, a *header* (protocol, addresses, ports, direction) and *options* (what to match and metadata). Illustrative rule:

```text
alert tcp any any -> $HOME_NET 445 (msg:"SMB possible exploit attempt"; \
    flow:to_server,established; content:"|ff|SMB"; sid:1000001; rev:1;)
```

Reading it: *action* `alert`; match `tcp` from `any` source to the home network on port `445`; only on established connections to the server; where the payload contains the bytes `|ff|SMB`; with an identifier (`sid`) and revision. Options can match content, byte patterns, regular expressions, protocol fields, and thresholds. Rules come from maintained rulesets (Emerging Threats, Snort's Talos rules) plus local custom rules.

### Detection vs prevention mode

- *IDS mode* (passive, out of band via a TAP/SPAN): the engine sees a copy of traffic and alerts; it cannot block. Safe (no risk of blocking legitimate traffic) but reactive.
- *IPS mode* (inline, in the traffic path): the engine can drop matching packets/flows, stopping the attack, but a false positive now blocks legitimate traffic and the engine is a potential point of failure and latency. See the [IPS](../../../security-operations/defensive-operations/detection/ips.md) note for the trade-offs.

Suricata's multi-threading helps it keep up inline on fast links; both engines support both modes.

### Beyond signatures

Modern Suricata does more than content signatures: it extracts protocol metadata and files (like a lightweight [Zeek](zeek.md)), supports [JA3/JA4](encrypted-traffic-analysis.md) TLS fingerprinting, and can log flow and protocol records. This narrows the gap with descriptive tools, but the core model is still rule-matching, so the signature blind spot remains and behavioral analysis is still complementary.

### Tuning: the real work

An untuned ruleset either floods analysts with false positives (every rule enabled) or misses attacks (too few rules). Tuning is the ongoing work:

- Enable rules relevant to your environment; disable noisy or irrelevant ones.
- Set `$HOME_NET` and variables correctly so direction-based rules work.
- Use thresholds and suppression to cut alert floods.
- Add local rules for your specific threats (including [virtual-patching](../traffic-filtering/web-application-firewalls.md)-style rules).
- Review alerts and feed back: a rule that only ever false-positives is noise.

## Worked example

This is conceptual on this host (neither engine is installed; the current lines are Suricata 8.x and Snort 3 as of 2026-10). The workflow:

1. **Deploy.** Suricata runs in IDS mode on a TAP at the edge and a segment boundary, with the Emerging Threats ruleset plus local rules, feeding alerts to the SIEM.
2. **A scan.** The [port scan](../network-attacks/network-scanning.md) from the [capture sample](packet-capture-analysis/README.md) trips a scan-detection rule (many SYNs to many ports from one source), raising an alert identifying `203.0.113.66` as scanning `198.51.100.20`, corroborating the behavioral detection the pcap summarizer produced.
3. **A known exploit.** A packet matching a signature for a specific CVE exploit against SMB triggers an alert (or a drop, inline); the `sid` and `msg` tell the analyst exactly which threat.
4. **Tuning.** A local application legitimately uses a pattern that matches a rule, causing false positives; the analyst suppresses that rule for that source rather than disabling it globally.
5. **The blind spot.** A novel, custom C2 over TLS matches no signature and passes Suricata silently; it is caught instead by the behavioral [beaconing detector](beaconing-detection/README.md) on the flow data and by [Zeek](zeek.md) logs. This is why signature and behavioral detection run together.

The example shows the engine as the sharp known-threat layer, corroborated by and complemented with the behavioral tools in this subarea.

## Trade offs and when to use it

- **IDS vs IPS mode.** IDS is safe and informative but cannot stop attacks; IPS stops them but risks blocking legitimate traffic and adds inline latency/failure risk. Start in IDS, move high-confidence rules to IPS. See [IPS](../../../security-operations/defensive-operations/detection/ips.md).
- **Suricata vs Snort.** Suricata is multi-threaded (better on fast links) with extra metadata/file/JA3 features; Snort 3 is mature with the Talos ruleset. Rule syntax is largely shared. Choose by performance needs and ruleset preference.
- **Signature vs behavioral.** Signatures are precise on known threats, blind to novel ones; pair with Zeek and flow-based behavioral detection. Neither alone suffices.
- **Ruleset breadth vs noise.** More rules catch more but create false positives; tuning to the environment is mandatory ongoing work.

## Common mistakes

- **Enabling every rule.** Alert flood, analysts tune out. Fix: enable relevant rules, tune thresholds, suppress noise.
- **Wrong `$HOME_NET`/variables.** Direction-based rules misfire or miss. Fix: configure network variables correctly.
- **Relying on signatures alone.** Misses novel threats. Fix: pair with Zeek/flow behavioral detection.
- **Inline IPS with untuned rules.** False positives block legitimate traffic. Fix: tune in IDS mode first, promote high-confidence rules to block.
- **Never updating rules.** Misses new threats. Fix: automated ruleset updates from maintained feeds.

## Practice

1. What is the core detection model of Suricata and Snort, and what is its fundamental blind spot?
2. What does each part of a rule (action, header, options) specify?
3. What is the difference between IDS and IPS mode for these engines, and the risk of each?
4. Why must signature engines be paired with behavioral tools like Zeek and flow analysis?
5. Why is ruleset tuning described as the real ongoing work?

### Answers

1. They match traffic against a ruleset of signatures describing known-bad patterns and alert or block on matches; the blind spot is any threat no rule describes (novel or custom attacks).
2. The action (alert/drop), the header (protocol, source/destination addresses and ports, direction), and the options (what content/fields to match plus metadata like the signature id and message).
3. IDS mode passively alerts on a copy of traffic (safe but cannot block); IPS mode is inline and can drop matching traffic (stops attacks but a false positive blocks legitimate traffic and the engine adds latency and a failure point).
4. Signatures catch only known patterns; novel or custom attacks (for example bespoke C2 over TLS) match no rule and pass silently, so behavioral detection is needed to catch the unknown.
5. An untuned ruleset either floods analysts with false positives or misses attacks; continuously enabling relevant rules, setting variables, thresholding, suppressing noise and adding local rules is what makes the engine useful.

## Further reading

- Suricata documentation and rule format: https://docs.suricata.io/
- Snort 3 documentation and the Talos ruleset: https://www.snort.org/
- Emerging Threats open ruleset: https://rules.emergingthreats.net/
- [IDS](../../../security-operations/defensive-operations/detection/ids/README.md) and [IPS](../../../security-operations/defensive-operations/detection/ips.md) for the detection/prevention concepts.
