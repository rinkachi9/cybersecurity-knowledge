---
title: SIEM
area: defensive operations
level: unrated
status: draft
last_verified: unverified
tags: [migrated, siem]
migrated_from: Security.html, page 57
---

# SIEM

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

To understand SecOps, you have to understand its "brain": the SIEM (Security Information and Event Management). If a SOC (Security Operations Center) is a cockpit, the SIEM is the entire dashboard of instruments, sensors, and black boxes combined into one interface.

SIEM is not a single tool but a combination of two historically distinct disciplines:

- SIM (Security Information Management): The "Librarian." It collects, stores, and analyzes log data for long-term reporting and compliance.
- SEM (Security Event Management): The "First Responder." It monitors systems in real-time, correlates events, and notifies the team of immediate threats.

Modern SIEM merges these, providing a centralized view of an organization's security posture by ingesting data from every corner of the network.

## SIEM Data Pipeline

A SIEM is only as good as the data it consumes. The process follows a specific lifecycle:

1. Data Aggregation: Gathering logs from diverse sources - firewalls, antivirus, servers, databases, and cloud apps (AWS, Azure, SaaS).
2. Normalization: Every device speaks a different "language." A firewall might log an IP as `src_ip`, while a server calls it `source`. The SIEM converts this into a single, uniform format.
3. Correlation: This is the "magic." The SIEM looks for patterns.
4. *Example:* 5 failed logins on a laptop (Event A) followed by a successful login from an IP in a different country (Event B) = High Priority Alert.
5. Retention: Storing data for months or years to meet legal requirements (GDPR, HIPAA, PCI-DSS) and for forensic "time-travel" during investigations.

## Key capabilities & features

| **Capability** | **Description** |
| --- | --- |
| Real-time Alerting | Instant notification when a predefined "rule" is triggered (e.g., "Privileged account created"). |
| UEBA | *User and Entity Behavior Analytics*. Using AI to learn what "normal" looks like for a user, then flagging deviations (e.g., "Why is Bob downloading 50GB of data at 3 AM?"). |
| Threat Intelligence | Integrating external feeds that list known "bad" IP addresses and malicious domains. |
| Compliance Reporting | Generating automated reports for auditors to prove the network is monitored and secure. |
| Forensics | Providing a searchable history so analysts can see exactly how an attacker moved through the network six months ago. |

### "Next-Gen" SIEM Evolution

Legacy SIEMs were notorious for being slow and producing too many "False Positives." Next-Gen SIEMs (often cloud-native) have changed the game by adding:

- SOAR Integration: The ability to not just *detect* but also *act* (e.g., automatically disabling a user account when a breach is detected).
- Machine Learning: Moving away from static "If/Then" rules toward identifying "Anomalous Patterns" that humans might miss.
- Cloud Scalability: Processing terabytes of data per day without needing a massive on-premise data center.

## Critical challenges

It’s not all sunshine and rainbows. Implementing a SIEM comes with significant hurdles:

- Alert Fatigue: If not tuned correctly, a SIEM will scream "Fire!" 10,000 times a day. Analysts quickly burn out and start ignoring the alerts.
- "Garbage In, Garbage Out": If you don’t feed it the right logs, the SIEM is blind.
- Cost: Many SIEMs charge by the volume of data ingested. This can lead to "Security vs. Budget" dilemmas where teams stop monitoring certain systems to save money.

## Leading tools

- Splunk Enterprise Security: The "Gold Standard" for high-end customization and powerful search capabilities.
- Microsoft Sentinel: A cloud-native leader, especially powerful for organizations already deep in the Azure/Microsoft 365 ecosystem.
- IBM QRadar: Known for its robust correlation engine and long-standing presence in enterprise SOCs.
- LogRhythm: Focused heavily on workflow and ease of use for security analysts.
- Elastic Security: An open-source-based favorite for teams that want flexibility and speed.

## Summary

Think of the SIEM as the Foundational Layer of SecOps. Without it, your security team is just a group of people staring at individual screens, hoping they get lucky. With it, they have a unified, searchable, and intelligent map of their entire digital kingdom.

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
