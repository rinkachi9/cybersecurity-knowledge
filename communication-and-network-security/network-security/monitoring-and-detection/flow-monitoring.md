# Flow monitoring

## Summary

Flow monitoring records summaries of network connections, who talked to whom, when, over what protocol and port, and how much data, without keeping the packet contents. Because a flow record is tiny compared with full packet capture, flows can be collected network-wide and kept for months, making them the backbone of long-term network visibility, behavioral detection and incident investigation. The main standards are Cisco's NetFlow, the IETF's IPFIX, and sFlow (sampled); in the cloud the equivalent is VPC/VNet flow logs. Flows cannot show content, so they do not replace packet capture, but they answer most "who contacted what, and how much" questions and work regardless of encryption.

## Prerequisites

- [Network security monitoring](network-security-monitoring.md): where flows fit among data types.
- [Packet capture analysis](packet-capture-analysis/README.md): the content-rich counterpart.
- Basic TCP/IP: the five-tuple.

## Core concepts

### Definition

A *flow* is a unidirectional (or bidirectional, depending on the standard) sequence of packets sharing key attributes, usually the five-tuple: source and destination IP, source and destination port, and protocol. A *flow record* summarizes it: the five-tuple plus start and end time, packet and byte counts, and TCP flags seen. *Flow monitoring* is the collection, storage and analysis of these records.

### Analogy

Flow records are an itemized phone bill: who called whom, when, for how long, and how much data, but not what was said. You cannot read the conversation, but the bill alone reveals a great deal: a desk calling the same foreign number every five minutes all night, a sudden huge data transfer, a device talking to hundreds of others in a minute. Full packet capture is recording the calls themselves, far more detail but far more storage and far more sensitive.

The analogy is close; it breaks only in that flow records are generated automatically by the network devices themselves, so collecting them often needs no extra sensor.

### Why flows are the backbone of visibility

- **Compact and keepable.** A flow record is a few hundred bytes regardless of how much data the connection carried, so a network's flows for months fit where full packets for hours would not. This makes flows the data you still have when investigating an intrusion discovered weeks later.
- **Network-wide.** Routers and switches generate flows natively (NetFlow/IPFIX), so coverage can be broad without deploying packet sensors everywhere.
- **Encryption-proof.** Flows are metadata, so TLS does not blind them; who-talked-to-whom, timing and volume are all visible. This is why [beaconing detection](beaconing-detection/README.md) and [exfiltration](../network-attacks/data-exfiltration.md) volume analysis run on flows.

### The standards

| Standard | Origin | Note |
| --- | --- | --- |
| NetFlow (v5, v9) | Cisco | The original; v9 is template-based and flexible |
| IPFIX | IETF (RFC 7011) | The standardized successor to NetFlow v9 |
| sFlow | Industry | Packet-sampling based; scales to high speeds, statistical not exact |
| VPC / VNet flow logs | Cloud providers | The cloud equivalent; essential for cloud visibility |

NetFlow/IPFIX account for every flow; sFlow samples a fraction of packets, trading exactness for scalability on very fast links.

### What flows are good and bad at

Good at: top talkers, connection patterns, volume anomalies, beaconing (timing), lateral-movement fan-out (one host to many), exfiltration (large uploads to new destinations), scanning (one source to many ports/hosts), long-term "has this host ever contacted that IP" lookups. Bad at: anything needing content (what was in the HTTP request, which file was transferred, the exact DNS name, unless enriched), and exactness under sampling.

Flow analysis is behavioral: it finds patterns rather than signatures, which complements signature-based [IDS/IPS](suricata-and-snort.md).

## Worked example

Flow records drive the behavioral detections in this subarea, which is their primary security use. The tested [beaconing detector](beaconing-detection/README.md) consumes exactly flow-style records (source, destination, port, bytes, time). Its output on synthetic flows (Python 3.10, 2026-10):

```text
source       destination     port conns median gap  skew   mad  size hours  score
192.0.2.23   203.0.113.80     443   290       299s  0.98  0.90  0.95  1.00  0.96   <- beacon
192.0.2.21   198.51.100.13    443   129        49s  ...                      0.31   <- human browsing
```

Reading it: from flow records alone, with no packet content, the regular 300-second check-in to one destination stands out as a [C2](../network-attacks/command-and-control-traffic.md) beacon against the irregular human browsing. The same flow data answers other security questions directly: a host appearing as a source to hundreds of destination ports in a minute is [scanning](../network-attacks/network-scanning.md); a server suddenly sending gigabytes to a never-before-seen destination is possible [exfiltration](../network-attacks/data-exfiltration.md); a workstation making SMB flows to many peers is [lateral movement](../network-attacks/lateral-movement.md). None of these needs packet content, which is why flows carry so much of network detection and why they work over encryption.

## Trade offs and when to use it

- **Flows vs full packets.** Flows are compact, keepable and encryption-proof but have no content; packets have content but are huge and briefly retained. Use flows for broad long-term visibility and behavioral detection, packets for deep investigation at key points.
- **NetFlow/IPFIX vs sFlow.** Full accounting (NetFlow/IPFIX) is exact but heavier; sFlow samples and scales to high speeds at the cost of exactness. Choose by link speed and need for precision.
- **Native vs sensor-generated.** Device-native flows give broad coverage cheaply; dedicated generators give richer records. Combine as needed.
- **Cloud flows are not optional.** In cloud environments, VPC/VNet flow logs are often the main network visibility available, since you cannot TAP the provider's fabric.

## Common mistakes

- **Not collecting flows because you have packet capture.** Packets cannot be kept long enough for later investigation. Fix: keep flows for months as the long-term record.
- **Expecting content from flows.** They are metadata only. Fix: pair with logs/packets where content is needed.
- **Ignoring cloud flow logs.** Leaves cloud traffic invisible. Fix: enable and centralize VPC/VNet flow logs.
- **Only signature detection, no behavioral.** Misses novel C2, scanning and exfiltration patterns. Fix: run behavioral analysis (beaconing, volume, fan-out) on flows.
- **Over-sampling with sFlow on links where exactness matters.** Misses low-and-slow activity. Fix: full accounting on critical links.

## Practice

1. What does a flow record contain, and what does it deliberately omit?
2. Why can flows be kept for months when full packet capture cannot?
3. Why does flow analysis still work when traffic is encrypted?
4. Give three security questions flows answer well and one they cannot.
5. Why are cloud flow logs especially important?

### Answers

1. The five-tuple (source/destination IP, source/destination port, protocol) plus timing, packet and byte counts and TCP flags; it omits the packet contents (the payload).
2. A flow record is a tiny fixed-size summary regardless of how much data the connection carried, so a network's flows for months occupy far less storage than full packets for hours.
3. Flows are metadata (who, when, how much), which is visible regardless of payload encryption, so TLS does not hide the connection patterns flow analysis relies on.
4. Well: beaconing/C2 (timing), scanning (fan-out to many ports), exfiltration (large uploads to new destinations); also lateral movement and top talkers. Cannot: anything needing content, such as the exact HTTP request or transferred file.
5. You cannot TAP the cloud provider's fabric, so VPC/VNet flow logs are often the primary network visibility available for cloud workloads.

## Further reading

- RFC 7011, Specification of the IP Flow Information Export (IPFIX) Protocol: https://www.rfc-editor.org/rfc/rfc7011
- Cisco NetFlow and sFlow documentation for the respective standards.
- [Beaconing detection](beaconing-detection/README.md) and [data exfiltration](../network-attacks/data-exfiltration.md) for flow-based detection in practice.
- Cloud provider documentation for VPC/VNet flow logs.
