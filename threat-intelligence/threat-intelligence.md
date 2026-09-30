---
title: Threat Intelligence (Threat Intel)
area: threat intelligence
level: unrated
status: draft
last_verified: unverified
tags: [migrated]
migrated_from: Security.html, page 12
---

# Threat Intelligence (Threat Intel)

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Threat Intelligence (TI)**, often called **Cyber Threat Intelligence (CTI)**, is the **systematic collection, analysis, and operationalization of information about adversaries, threats, and risks** to support **informed security decisions**.

> Core purpose:
>
> Transform raw threat data into
>
> actionable intelligence
>
> that improves
>
> prevention, detection, response, and strategic decision-making
>
> .

Threat intelligence answers four critical questions:

1. **Who** is attacking?
2. **How** are they attacking?
3. **Why** are they attacking?
4. **What should we do about it?**

### Purpose

Threat Intel helps organizations:

- Stay **ahead of adversaries**
- Understand **how attacks happen**
- Identify **who might be targeting them**
- Respond to **incidents more effectively**
- **Prioritize risks** based on real-world data

### Key functions

- **Threat detection**: Spot anomalies and early signs of compromise.
- **Threat hunting**: Proactively search for indicators in your environment.
- **Incident response**: Provide context and evidence during investigations.
- **Vulnerability management**: Prioritize patching based on real-world exploitation.
- **Security awareness**: Inform staff about emerging phishing or scam tactics.

## Importance

Traditional security fails because it is:

- Reactive
- Tool-centric
- Blind to attacker intent

Threat intelligence exists to:

- Shift security from **reactive to proactive**
- Focus defenses on **real adversaries**
- Prioritize controls based on **actual threat likelihood**
- Reduce noise and wasted effort

> Key insight:
>
> Vulnerabilities are infinite.
>
> Threats are contextual.

## Benefits

| Benefit | Description |
| --- | --- |
| **Proactive defense** | Helps stop attacks before they happen. |
| **Reduced alert fatigue** | Filters and prioritizes threat data. |
| **Faster response** | Cuts time in detection, triage, and mitigation. |
| **Better decision-making** | Informs investments, controls, and policies. |
| **Threat actor tracking** | Reveals motivations, targets, and likely next steps. |

## Core components

| Component | Description |
| --- | --- |
| **Indicators of Compromise (IoCs)** | Data artifacts showing potential intrusion (e.g., malicious IPs, hashes, domain names). |
| **Tactics, Techniques, and Procedures (TTPs)** | Patterns of behavior attackers use - aligned with the MITRE ATT&CK framework. |
| **Threat Actor Profiles** | Insights into specific hacker groups, motives, targets, and capabilities. |
| **Threat Feeds** | Streams of threat data, often automated, from commercial, community, or open-source providers. |
| **Contextual Analysis** | Adds meaning to the data - the “who, what, when, why, and how” behind a threat. |

## Threat Intelligence vs Raw Threat Data

A fundamental distinction every professional must understand:

| Data | Intelligence |
| --- | --- |
| IP addresses | Why those IPs matter |
| Hashes | Which campaign they belong to |
| Alerts | What they indicate |
| Logs | What story they tell |

**Threat intelligence = analysis + context + decision support**.

## Core principles

### Adversary-Centric

Focus on **attackers**, not just tools.

#### Evidence-Driven

Based on telemetry, forensics, malware, and incidents.

#### Actionable

Must influence:

- SOC detections
- IR playbooks
- Architecture decisions
- Executive risk discussions

#### Timely

Late intelligence is often useless.

## Threat Intelligence Lifecycle

Threat intelligence follows a structured lifecycle:

1. **Direction** - define intelligence requirements
2. **Collection** - gather relevant data
3. **Processing** - normalize and enrich
4. **Analysis** - transform data into insight
5. **Dissemination** - deliver to stakeholders
6. **Feedback** - improve requirements

This lifecycle is continuous, not linear.

## Types

Threat intelligence is commonly divided into **four levels**, each serving different stakeholders.

### Strategic Threat Intelligence

**Audience:** Executives, CISOs, risk committees

**Focus:**

- Geopolitical threats
- Industry-specific risks
- Long-term trends
- Business impact

**Examples:**

- Nation-state targeting trends
- Sector-specific ransomware activity
- Regulatory and geopolitical risk

**Value:**

Supports **investment, prioritization, and governance**.

#### Operational Threat Intelligence

**Audience:** Security leadership, IR leads

**Focus:**

- Active campaigns
- Threat actor objectives
- Targeting patterns
- Attack timelines

**Examples:**

- Ransomware group playbooks
- Campaign-specific TTPs
- Sector-focused intrusion waves

This level bridges **strategy and tactics**.

#### Tactical Threat Intelligence

**Audience:** SOC, Blue Team, Detection Engineers

**Focus:**

- Tactics, Techniques, and Procedures (TTPs)
- Detection opportunities
- ATT&CK mappings

**Examples:**

- Credential dumping techniques
- Lateral movement methods
- C2 behaviors

This is the **core fuel of detection engineering**.

#### Technical Threat Intelligence

**Audience:** SOC, automation systems

**Focus:**

- Indicators of Compromise (IOCs)

**Examples:**

- IPs
- Domains
- Hashes
- URLs

> Important:
>
> Technical intelligence has the
>
> shortest lifespan
>
> and
>
> lowest standalone value
>
> .

## Pyramid of Pain

The **Pyramid of Pain** explains the **cost to attackers when defenders act on intelligence**:

From lowest to highest impact:

- Hashes
- IP addresses
- Domains
- Network artifacts
- Tools
- TTPs

**Key lesson:**

Intelligence that targets **TTPs** hurts attackers the most.

## Threat Intelligence Sources

### Internal Sources

- SOC telemetry
- Incident response data
- Logs and alerts
- Forensics artifacts

#### External Sources

- Open-source intelligence (OSINT)
- Commercial feeds
- ISACs / industry sharing
- Vendor intelligence reports

#### Intelligence Providers

Organizations like **Mandiant** specialize in **high-confidence, adversary-attributed intelligence** based on real intrusions.

## Threat Actor Modeling

Threat intelligence often models adversaries by:

- Motivation (financial, espionage, hacktivism)
- Capability
- Resources
- Target selection
- Tradecraft

This enables **threat-informed defense**, not generic security.

## Threat Intelligence and MITRE ATT&CK

The **MITRE ATT&CK** framework is the **backbone of modern tactical threat intelligence**.

Threat intelligence uses ATT&CK to:

- Normalize reporting
- Map detections
- Identify coverage gaps
- Align red, blue, and purple teams

ATT&CK turns intelligence into **engineering-ready input**.

## Threat Intelligence and Detection Engineering

High-maturity organizations use threat intelligence to:

- Design detections for **behaviors**, not indicators
- Validate SOC coverage
- Reduce false positives
- Prioritize engineering work

This is where intelligence becomes **operational power**.

## Threat Intelligence and Incident Response

During incidents, threat intelligence helps:

- Identify attacker group
- Predict next attacker steps
- Scope compromise
- Choose remediation priorities
- Communicate risk accurately

IR without threat intelligence is **blind containment**.

## Threat Intelligence in Cloud & SaaS

Modern threat intelligence covers:

- Identity-centric attacks
- Token theft
- API abuse
- SaaS compromise
- Cloud misconfiguration exploitation

Cloud TI focuses more on **behavior and identity abuse** than on network indicators.

## Threat Intelligence vs Vulnerability Management

| Vulnerability Management | Threat Intelligence |
| --- | --- |
| What *can* be exploited | What *is* being exploited |
| CVEs | Campaigns |
| Static | Dynamic |
| Volume-driven | Priority-driven |

**Best practice:**

Use threat intelligence to **prioritize vulnerabilities**.

## Common pitfalls

- Collecting feeds without analysis
- IOC overload
- No feedback loop
- Intelligence not mapped to actions
- Intelligence isolated from SOC and IR
- Over-reliance on vendor reports

## Skills Required for Threat Intelligence Mastery

A professional CTI specialist must understand:

- Adversary tradecraft
- Networking and OS internals
- Malware behavior
- ATT&CK framework
- Data analysis
- Writing and briefing skills
- Business risk communication

Threat intelligence is both **technical and analytical**.

## Maturity levels

1. Ad-hoc IOC consumption
2. Structured reporting
3. ATT&CK-aligned intelligence
4. Intelligence-driven detection
5. Adversary-focused security program

Most organizations stall at **level 2**.

## Strategic value

Threat intelligence enables:

- Proactive defense
- Smarter investment decisions
- Reduced dwell time
- Better incident outcomes
- Executive-level risk awareness

It turns security from:

> “We react to alerts”
>
> into
>
> “We anticipate adversaries.”

## Framework landscape

If:

- **NIST CSF** defines risk outcomes
- **RMF** governs risk decisions
- **SANS** builds skills
- **Mandiant** exposes real attackers
- **SLSA** secures supply chains
- **SAIF** secures AI systems

Then:

> Threat Intelligence connects attackers to all of them.

## Summary

Threat intelligence is **not about data**.

It is about **understanding intent, capability, and impact**.

Organizations with mature threat intelligence:

- Waste less effort
- Detect faster
- Respond smarter
- Invest wisely

For cybersecurity specialists, **threat intelligence literacy is a defining skill** - whether you work in SOC, IR, cloud security, DevSecOps, or leadership.

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
