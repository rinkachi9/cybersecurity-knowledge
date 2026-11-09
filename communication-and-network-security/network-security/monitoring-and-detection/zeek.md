# Zeek

## Summary

Zeek (formerly Bro) is an open-source network analysis framework that turns raw traffic into rich, structured logs of what actually happened: every connection, DNS query, TLS handshake, HTTP request, file transfer and more, each as a tidy record. Unlike a signature-based IDS that only tells you when a known-bad pattern appears, Zeek describes all the traffic, giving the transaction logs that are the backbone of [network security monitoring](network-security-monitoring.md), threat hunting and incident investigation. It is programmable, so analysts can write detection logic in its scripting language. Zeek is the tool most responsible for turning packets into answerable questions.

## Prerequisites

- [Network security monitoring](network-security-monitoring.md): Zeek produces the transaction-log data type.
- [Packet capture analysis](packet-capture-analysis/README.md): Zeek is the scalable, structured alternative to reading packets by hand.
- [Encrypted traffic analysis](encrypted-traffic-analysis.md): Zeek extracts TLS/certificate metadata.

## Core concepts

### Definition

*Zeek* is a passive network analysis framework that observes traffic (from a live interface or a [pcap](packet-capture-analysis/README.md)) and produces structured logs describing network activity at the protocol level, plus an event-driven scripting language for custom analysis. It is not primarily a signature engine; it is a traffic *describer*.

### Analogy

If [full packet capture](packet-capture-analysis/README.md) is a raw audio recording of every conversation in a building, Zeek is a diligent clerk who listens and writes a structured minute of each one: who spoke to whom, when, for how long, what was requested, what certificate was shown. You rarely need the raw audio; the clerk's organized minutes answer most questions instantly and take a fraction of the space. The clerk can also be given standing instructions ("flag any call that does X"), which is Zeek scripting.

The analogy is close; it breaks in that Zeek understands dozens of protocols deeply, so its "minutes" are far more detailed and exact than a human clerk could produce.

### What Zeek produces

Zeek writes a set of logs, one per protocol or activity, as structured records. The important ones for security:

| Log | Contents | Security use |
| --- | --- | --- |
| `conn.log` | Every connection: five-tuple, duration, bytes, state | The basis for [beaconing](beaconing-detection/README.md), scanning, lateral-movement analysis |
| `dns.log` | Every query and answer | [DNS tunneling](../dns-security/dns-tunneling/README.md), malicious domains |
| `http.log` | HTTP requests and responses | Web attacks, downloads, C2 over HTTP |
| `ssl.log` / `x509.log` | TLS handshakes and certificates | [Encrypted traffic analysis](encrypted-traffic-analysis.md), JA3/JA4, odd certs |
| `files.log` | Files seen crossing the wire, with hashes | Malware (hash matching), exfiltration |
| `notice.log` | Things Zeek's scripts flagged | Built-in and custom detections |

The `conn.log` fields are exactly the flow-style records the [beaconing detector](beaconing-detection/README.md) in this subarea consumes, which is why that note uses Zeek-style input.

### Programmable detection

Zeek's scripting language is event-driven: scripts react to events like "a new connection", "a DNS request", "a TLS certificate seen". Analysts and the community write scripts to detect specific behaviors (a host resolving many failed domains, a self-signed certificate on a non-standard port, a file hash on a blocklist). This programmability is why Zeek is a *framework*, not just a logger: it adapts to new detection needs without waiting for vendor signatures.

### Zeek vs signature IDS

[Suricata and Snort](suricata-and-snort.md) match traffic against signatures of known threats and alert on hits. Zeek describes all traffic, whether or not anything matches a signature. They are complementary: the signature IDS gives sharp alerts on known-bad; Zeek gives the complete context to hunt for unknown-bad and to investigate any alert. Most NSM deployments run both, often on the same sensor.

## Worked example

This is conceptual on this host (Zeek is not installed; the current stable line is the 8.x LTS/feature releases as of 2026-10). The workflow is what matters.

Run Zeek over a capture (the same sample from [packet capture analysis](packet-capture-analysis/README.md)) and it produces `conn.log`, `dns.log` and others. The `conn.log` would contain records like:

```text
ts            id.orig_h    id.resp_h      id.resp_p  proto  duration  orig_bytes  resp_bytes  conn_state
...           192.0.2.10   198.51.100.20  80         tcp    0.04      75          43          SF
...           203.0.113.66 198.51.100.20  22         tcp    -         0           0           S0/REJ...
```

and `dns.log` would record the long, high-entropy query name that the [DNS tunnel detector](../dns-security/dns-tunneling/README.md) flags. The security value is that these logs are then fed directly to the analysis tools in this subarea: the [beaconing detector](beaconing-detection/README.md) runs on `conn.log`, the [DNS tunnel detector](../dns-security/dns-tunneling/README.md) on `dns.log`, and an analyst hunts across all of them. Zeek is the engine that converts the raw traffic those detectors would otherwise have to parse themselves into clean, structured input, at a scale where reading packets by hand is impossible.

During an incident, Zeek logs answer questions fast: "every connection host X made in the last month" (`conn.log`), "every domain it resolved" (`dns.log`), "every certificate it saw" (`ssl.log`), "every file it downloaded and their hashes" (`files.log`), without ever needing the original packets.

## Trade offs and when to use it

- **Zeek vs full packet capture.** Zeek logs are compact, structured and keepable long-term but are a summary; keep short-term full packets at key points for when the bytes themselves are needed. Use Zeek as the primary, always-on record.
- **Zeek vs signature IDS.** Zeek describes everything (context, hunting); signature IDS alerts on known-bad (sharp, actionable). Run both; they answer different questions.
- **Resource cost.** Zeek must process all traffic on its sensor; high-speed links need clustering and tuning. It is CPU-bound on parsing.
- **Encrypted traffic.** Zeek cannot see TLS content but extracts rich TLS/certificate metadata (ssl.log, x509.log) for [ETA](encrypted-traffic-analysis.md), so it stays valuable as traffic encrypts.

## Common mistakes

- **Treating Zeek as an alerting IDS.** It is mainly a describer; expecting it to alert like Suricata misses its point. Fix: use it for logs, context and custom scripts; pair with a signature IDS for alerts.
- **Collecting Zeek logs but never hunting in them.** The value is in querying them. Fix: feed them to a SIEM and the detectors in this subarea; hunt regularly.
- **Under-resourcing the sensor.** Dropped packets mean incomplete logs. Fix: cluster and tune for the link speed; watch for drops.
- **Ignoring the TLS/x509 logs.** They are key for encrypted-traffic detection. Fix: use ssl.log/x509.log for JA3/JA4 and certificate anomalies.
- **No retention plan.** Zeek logs are compact; keep them for months for investigation. Fix: central storage with long retention.

## Practice

1. How does Zeek differ fundamentally from a signature-based IDS?
2. Which Zeek log underpins beaconing, scanning and lateral-movement analysis, and why?
3. Why does Zeek remain useful even as traffic becomes encrypted?
4. What makes Zeek a framework rather than just a logger?
5. Why run Zeek and a signature IDS together?

### Answers

1. A signature IDS matches traffic against patterns of known threats and alerts on hits; Zeek describes all traffic as structured protocol logs regardless of whether anything matches a signature.
2. `conn.log`, because it records every connection's five-tuple, timing and byte counts, which are exactly the flow-style inputs those behavioral detections need.
3. It cannot read TLS content but extracts rich metadata (TLS handshakes, certificates, JA3/JA4) into ssl.log/x509.log, which supports encrypted-traffic analysis.
4. Its event-driven scripting language lets analysts write custom detection logic that reacts to network events, so it adapts to new needs rather than only emitting fixed logs.
5. Zeek gives complete context for hunting and investigation and catching unknown-bad; the signature IDS gives sharp, actionable alerts on known-bad; together they cover both known and unknown threats.

## Further reading

- Zeek documentation and the log reference: https://docs.zeek.org/
- Zeek `conn.log` fields: https://docs.zeek.org/en/master/logs/conn.html
- [Network security monitoring](network-security-monitoring.md) and [beaconing detection](beaconing-detection/README.md) for how Zeek data is used.
- Bejtlich, R., The Practice of Network Security Monitoring, which uses Zeek (Bro) extensively.
