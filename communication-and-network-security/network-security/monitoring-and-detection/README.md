# Monitoring and detection

Seeing what happens on the network and finding the attacks that got past prevention. These notes cover the data to collect, the tools that produce and analyze it, and the detection and hunting practices built on top. Several come with tested scripts run in the lab.

Read [network security monitoring](network-security-monitoring.md) first; it frames the data types and sensor placement the rest depend on.

## Notes

- [Network security monitoring](network-security-monitoring.md): data types, sensor placement, blind spots. The foundation.
- [Packet capture analysis](packet-capture-analysis/README.md): reading packets, BPF filters, triage. Tested scripts.
- [Flow monitoring](flow-monitoring.md): NetFlow/IPFIX/sFlow and cloud flow logs, the backbone of long-term visibility.
- [Zeek](zeek.md): turning traffic into structured transaction logs.
- [Suricata and Snort](suricata-and-snort.md): signature-based detection and prevention engines.
- [Encrypted traffic analysis](encrypted-traffic-analysis.md): JA3/JA4, SNI and certificate metadata, detecting threats without decryption.
- [Beaconing detection](beaconing-detection/README.md): finding C2 check-ins statistically. Tested scripts.
- [Network detection and response](network-detection-and-response.md): the NDR product category, analytics plus response.
- [Network threat hunting](network-threat-hunting.md): proactive, hypothesis-driven search.
- [Deception and honeypots](deception-and-honeypots.md): high-fidelity detection from decoys and honeytokens.

Scripts: pcap generation and triage under [packet-capture-analysis/scripts](packet-capture-analysis/scripts/); beacon log generation and scoring under [beaconing-detection/scripts](beaconing-detection/scripts/).

Related: [IDS](../../../security-operations/defensive-operations/detection/ids.md), [IPS](../../../security-operations/defensive-operations/detection/ips.md), [SIEM](../../../security-operations/defensive-operations/operations/siem.md) and [SOAR](../../../security-operations/defensive-operations/operations/soar.md) in defensive operations.

Back to [Network security](../README.md).
