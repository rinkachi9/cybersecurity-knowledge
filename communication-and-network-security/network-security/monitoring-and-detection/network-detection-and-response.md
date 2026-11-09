# Network detection and response

## Summary

Network detection and response (NDR) is a category of security product that combines network monitoring, behavioral and machine-learning detection, and response actions into one system. It evolved from standalone IDS and [network security monitoring](network-security-monitoring.md) by adding automated analytics across all network data and the ability to respond (alert, isolate, block), and it is one of the three pillars of modern detection alongside endpoint (EDR) and the unifying SIEM/XDR. NDR's value is seeing the network-wide behavioral picture, especially the east-west and encrypted traffic that signatures and endpoint agents miss; its limits are the usual ones of behavioral detection: tuning, false positives, and dependence on visibility.

## Prerequisites

- [Network security monitoring](network-security-monitoring.md): the data foundation NDR builds on.
- [IDS](../../../security-operations/defensive-operations/detection/ids.md)/[IPS](../../../security-operations/defensive-operations/detection/ips.md) and [SIEM](../../../security-operations/defensive-operations/operations/siem.md)/[SOAR](../../../security-operations/defensive-operations/operations/soar.md): neighboring categories.
- [Encrypted traffic analysis](encrypted-traffic-analysis.md) and [beaconing detection](beaconing-detection/README.md): techniques NDR automates.

## Core concepts

### Definition

*Network detection and response* is a security solution that continuously analyzes network traffic (and metadata) using behavioral analytics and machine learning to detect threats, and provides or integrates response capabilities. It is the network-focused sibling of Endpoint Detection and Response (EDR), and it feeds and is coordinated by SIEM/XDR.

### Analogy

If [NSM](network-security-monitoring.md) is the building's cameras and logbooks, NDR is a trained security team that watches all the feeds at once, knows what normal looks like, notices the unusual (a person wandering floors they never visit, a van idling by the loading dock every night), and can act, lock a door, raise an alarm, call for backup. It is the monitoring data plus the analytics and response wrapped together.

The analogy holds well; it breaks in that NDR's "team" is largely automated analytics, which is fast and tireless but makes mistakes (false positives) that a human must still adjudicate.

### What NDR adds over plain monitoring

- **Behavioral and ML analytics across all network data.** Rather than only signature matching, NDR baselines normal behavior and flags deviations: [beaconing](beaconing-detection/README.md), [lateral movement](../network-attacks/lateral-movement.md), unusual data flows, [scanning](../network-attacks/network-scanning.md), suspicious [encrypted traffic](encrypted-traffic-analysis.md). It automates the kinds of detection this subarea's scripts illustrate.
- **Correlation and context.** It links related events into a single incident (this host beaconed, then moved laterally, then uploaded data) rather than isolated alerts.
- **Response.** NDR can alert, trigger [SOAR](../../../security-operations/defensive-operations/operations/soar.md) playbooks, instruct a firewall or NAC to isolate a host, or (inline) block. "Response" ranges from notification to automated containment.
- **East-west and encrypted coverage.** Modern NDR emphasizes internal and encrypted traffic, the gaps that perimeter signatures and endpoint agents miss.

### NDR, EDR, SIEM and XDR

| Category | Focus | Sees |
| --- | --- | --- |
| NDR | Network traffic and metadata | East-west and north-south traffic, including devices with no agent (IoT, OT) |
| EDR | Endpoint activity | Process, file, memory on hosts that run an agent |
| SIEM | Logs from everything | What is logged to it; correlation and storage |
| XDR | Unifying layer | Correlates NDR, EDR and more into one view |

Their complementarity is the point: NDR sees traffic from devices that cannot run an agent and sees the network behavior EDR cannot, while EDR sees on-host detail NDR cannot. XDR (or a SIEM) ties them together. Relying on only one leaves gaps, no agent on an IoT device (EDR blind), encrypted payload (NDR cannot read content), unlogged activity (SIEM blind).

## Worked example

An intrusion unfolds and NDR ties it together (conceptual, illustrating the category's value over the isolated detections this subarea's scripts perform):

1. **Beaconing.** NDR's behavioral analytics flag a workstation making regular HTTPS check-ins to a rare destination, the automated form of the [tested beacon detection](beaconing-detection/README.md), corroborated by a malicious JA3/JA4 fingerprint from [ETA](encrypted-traffic-analysis.md).
2. **Lateral movement.** Shortly after, the same host starts SMB connections to many internal peers, NDR recognizes the [lateral-movement](../network-attacks/lateral-movement.md) fan-out from east-west visibility that a perimeter sensor would miss.
3. **Exfiltration.** The host then uploads an unusually large volume to a new external destination, flagged as possible [exfiltration](../network-attacks/data-exfiltration.md).
4. **Correlation and response.** NDR correlates these into one incident rather than three disconnected alerts, scores it high, and triggers a response: a [SOAR](../../../security-operations/defensive-operations/operations/soar.md) playbook instructs NAC to isolate the host and opens a case, while EDR (via XDR) adds the on-host process detail.
5. **Analyst.** The analyst sees the whole chain in one incident with network and endpoint context, confirms, and contains fully.

The example shows NDR as the automation and correlation layer over the individual network detections, plus response, integrated with endpoint and SIEM.

## Trade offs and when to use it

- **Automation vs false positives.** Behavioral/ML detection finds novel threats signatures miss but produces false positives; automated response must be tuned and gated (isolate on high confidence, alert-only on lower) to avoid disrupting the business.
- **NDR vs building it yourself.** The detections NDR automates (beaconing, scanning, exfiltration) can be built from [Zeek](zeek.md), [flow](flow-monitoring.md) and scripts (as this subarea shows); NDR packages, scales and correlates them with response, at a licensing cost. Choose by scale and team capacity.
- **Visibility dependence.** NDR is only as good as the traffic it sees; it needs the same [sensor placement](network-security-monitoring.md) and cloud flow logs, and it inherits the encrypted-content limit (hence [ETA](encrypted-traffic-analysis.md)).
- **One pillar of three.** NDR complements EDR and SIEM/XDR; it is not a replacement for either.

## Common mistakes

- **Treating NDR as a silver bullet.** It misses on-host detail and encrypted content. Fix: combine with EDR and SIEM/XDR.
- **Fully automated response without tuning.** False positives isolate legitimate systems. Fix: gate automated containment on high confidence; alert-only otherwise.
- **Deploying NDR with poor visibility.** It cannot analyze traffic it does not see. Fix: proper sensor placement, east-west coverage, cloud flow logs.
- **Ignoring the encrypted-content limit.** Expecting NDR to read TLS payloads. Fix: rely on behavioral and metadata (ETA) detection for encrypted traffic.
- **No integration.** Isolated NDR alerts without endpoint/log context slow response. Fix: integrate into SIEM/XDR for correlation.

## Practice

1. What does NDR add over plain network security monitoring?
2. Why do NDR, EDR and SIEM/XDR complement rather than replace each other?
3. What network stages did NDR tie together in the worked example, and why does correlation matter?
4. Why must automated response in NDR be tuned and gated?
5. What is NDR's dependence that limits its effectiveness regardless of its analytics?

### Answers

1. Behavioral and ML analytics across all network data (not just signatures), correlation of related events into incidents, and response capabilities (alert, isolate, block), with emphasis on east-west and encrypted traffic.
2. NDR sees network traffic including from agentless devices but not on-host detail or encrypted content; EDR sees on-host process/file/memory but not the network picture; SIEM/XDR correlates logs and both; each covers the others' blind spots.
3. Beaconing (C2), lateral movement, and exfiltration; correlating them into one scored incident reveals the attack chain and enables a proportionate response, rather than three disconnected low-context alerts.
4. Behavioral detection produces false positives, so automatically isolating or blocking on every alert would disrupt legitimate systems; response should be gated on confidence (contain on high, alert on lower).
5. Visibility: it can only analyze traffic that reaches its sensors, so poor sensor placement or unmonitored cloud/east-west traffic blinds it, and it cannot read encrypted payloads.

## Further reading

- Gartner, Network Detection and Response market definition and guides.
- [Network security monitoring](network-security-monitoring.md), [beaconing detection](beaconing-detection/README.md) and [encrypted traffic analysis](encrypted-traffic-analysis.md) for the underlying techniques.
- [SIEM](../../../security-operations/defensive-operations/operations/siem.md) and [SOAR](../../../security-operations/defensive-operations/operations/soar.md) for the correlation and response context.
- MITRE ATT&CK for mapping NDR detections to adversary techniques: https://attack.mitre.org/
