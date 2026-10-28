# Intrusion Detection System (IDS)

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

An **Intrusion Detection System (IDS)** is a security control designed to **monitor, analyze, and detect malicious or policy-violating activity** within a network or host environment.

> Core objective:
>
> Provide
>
> early detection of attacks, misuse, and anomalies
>
> by continuously analyzing traffic, system behavior, and logs.

Unlike preventive controls (firewalls, IPS), an IDS is **detective** in nature:

- It **alerts**
- It **does not block** (in its pure form)

IDS is a foundational component of:

- Security Operations Centers (SOC)
- Threat detection programs
- Incident response workflows
- Threat hunting initiatives

## Importance

No preventive control is perfect:

- Firewalls are bypassed
- Credentials are stolen
- Misconfigurations happen
- Zero-days are exploited

IDS exists because:

> Prevention eventually fails - detection must succeed.

IDS reduces:

- Attacker dwell time
- Lateral movement window
- Mean Time to Detect (MTTD)

## IDS vs IPS

| Feature | IDS | IPS |
| --- | --- | --- |
| Mode | Passive | Inline |
| Action | Alert | Block |
| Risk of False Positive | Low operational impact | High operational impact |
| Latency Impact | None | Possible |

**IDS is visibility-focused.**

**IPS is prevention-focused.**

Many modern solutions operate as **IDS/IPS hybrid systems**.

## Types

IDS systems are categorized by **monitoring scope**.

### Network-Based IDS (NIDS)

#### Definition

Monitors **network traffic** at strategic points (SPAN port, TAP, gateway).

#### What It Analyzes

- Packet payloads
- Protocol behavior
- Traffic patterns
- Session anomalies

#### Strengths

- Broad visibility
- Detects lateral movement
- Protocol-aware inspection

#### Limitations

- Encrypted traffic blindness (unless decrypted)
- Limited host-level visibility

#### Typical Deployment

- Data center core
- Cloud VPC mirroring
- Internet edge

### Host-Based IDS (HIDS)

#### Definition

Installed directly on endpoints or servers.

#### What It Monitors

- File integrity
- Process execution
- Registry changes
- System calls
- Local logs

#### Strengths

- Deep host visibility
- Detects insider abuse
- Detects persistence mechanisms

#### Limitations

- Agent management overhead
- Limited network-wide perspective

Modern HIDS often evolves into **Endpoint Detection and Response (EDR)**.

## Detection Methodologies

IDS systems rely on **three primary detection models**.

### Signature-Based Detection

Matches known patterns:

- Exploit payloads
- Malware fingerprints
- Known bad IPs
- Attack regex rules

**Advantages**

- Low false positives
- High precision

**Limitations**

- Cannot detect unknown attacks
- Reactive by nature

#### Anomaly-Based Detection

Detects deviations from normal behavior.

Examples:

- Abnormal traffic volume
- Rare protocol usage
- Suspicious process execution

**Advantages**

- Can detect zero-days
- Identifies insider threats

**Limitations**

- Higher false positive rate
- Requires baselining

#### Behavior-Based Detection

Focuses on attacker tradecraft (TTPs).

Examples:

- Credential dumping sequence
- Suspicious PowerShell chain
- Lateral movement pattern

Often mapped to **MITRE ATT&CK**.

This is the most mature detection approach.

## IDS Architecture

A modern IDS consists of:

1. Data collection (packet capture, logs)
2. Parsing & normalization
3. Detection engine
4. Alerting mechanism
5. Logging & storage
6. SOC integration

In advanced environments:

- Machine learning layers
- Threat intelligence enrichment
- SOAR integration

## IDS in Cloud Environments

Cloud-native IDS differs from traditional deployments.

### Challenges:

- No physical TAPs
- Encrypted east-west traffic
- Ephemeral workloads
- API-driven environments

#### Solutions:

- VPC traffic mirroring
- Cloud-native IDS sensors
- Log-based detection (CloudTrail, audit logs)
- Identity-based detection

Cloud IDS increasingly becomes **identity-centric rather than packet-centric**.

## IDS and Encryption

Modern traffic is predominantly encrypted (TLS 1.3).

Options:

- Decrypt at gateway
- TLS inspection proxies
- Endpoint-level detection
- Metadata-based detection
- Behavioral heuristics

Encryption reduces NIDS visibility, increasing reliance on HIDS/EDR.

## IDS and Threat Intelligence

IDS becomes significantly more powerful when enriched with:

- IOC feeds
- Threat actor TTPs
- Campaign tracking
- Sector-specific intelligence

Threat intelligence helps:

- Reduce false positives
- Improve prioritization
- Map detections to adversaries

## IDS and Detection Engineering

High-maturity organizations treat IDS as part of:

> Detection Engineering

This involves:

- Writing custom detection rules
- Mapping to ATT&CK
- Continuous tuning
- Purple team validation
- Telemetry coverage analysis

IDS is no longer just “turn it on.”

## Common IDS Use Cases

- Detecting command-and-control traffic
- Identifying brute-force attempts
- Detecting lateral movement
- Monitoring data exfiltration
- Alerting on suspicious DNS patterns
- Identifying privilege escalation attempts

## Common pitfalls

- Excessive reliance on signatures
- Ignoring false positive tuning
- Lack of SOC triage process
- No integration with incident response
- Overlooking encrypted traffic gaps
- Treating IDS as a “set and forget” tool

## IDS Performance Considerations

Critical factors:

- Throughput capacity
- Packet loss tolerance
- Latency
- Deep packet inspection overhead
- Storage requirements

In high-volume networks:

- Horizontal scaling
- Load balancing
- Sampling strategies

## IDS in Zero Trust Architecture

IDS supports Zero Trust by:

- Monitoring identity abuse
- Detecting policy violations
- Verifying segmentation
- Identifying anomalous east-west movement
- Ensuring least privilege enforcement

Zero Trust requires continuous verification - IDS provides the telemetry.

## IDS Maturity Model

### Level 1 - Basic Alerts

- Default signatures
- Minimal tuning

#### Level 2 - Tuned Detection

- False positive reduction
- Custom rules

#### Level 3 - Threat-Informed Detection

- ATT&CK mapping
- Adversary simulation validation

#### Level 4 - Behavior-Centric Detection

- Cross-signal correlation
- Automated enrichment

#### Level 5 - Proactive Hunting

- Intelligence-driven detection creation
- Continuous purple teaming

## IDS vs Modern Detection Stack

Modern environments often use:

- IDS
- IPS
- EDR
- NDR (Network Detection and Response)
- XDR
- SIEM

IDS remains foundational but is part of a **larger detection ecosystem**.

## Skills Required for IDS Mastery

A senior IDS engineer must understand:

- TCP/IP deeply
- Protocol internals (HTTP, DNS, SMTP, SMB)
- Operating systems
- Malware behavior
- Log analysis
- ATT&CK framework
- Threat hunting
- Detection engineering
- Performance optimization

IDS expertise is highly technical.

## Strategic Value of IDS

IDS enables:

- Reduced attacker dwell time
- Early breach detection
- Evidence preservation
- Threat-informed defense
- Improved SOC effectiveness

It shifts security from:

> “We hope nothing gets through.”
>
> to
>
> “If something gets through, we will detect it quickly.”

## Summary

Intrusion Detection Systems are a **cornerstone of defensive cybersecurity**.

They are:

- Visibility engines
- Telemetry amplifiers
- Detection foundations
- Incident response triggers

In modern security programs, IDS evolves from a simple alerting tool into a **core component of detection engineering and threat-informed defense**.

For cybersecurity specialists, mastering IDS means mastering:

- Adversary behavior
- Network internals
- Detection design
- SOC operations

It is one of the defining skills of a true Blue Team professional.

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
