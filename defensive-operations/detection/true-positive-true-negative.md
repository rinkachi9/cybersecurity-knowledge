---
title: True Negative / True Positive
area: defensive operations
level: unrated
status: draft
last_verified: unverified
tags: [migrated, detection, metrics]
migrated_from: Security.html, page 8
---

# True Negative / True Positive

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

In cybersecurity, detection systems make decisions about whether activity is **malicious** or **benign**. These decisions can be correct or incorrect:

|  | **Threat Present** | **No Threat Present** |
| --- | --- | --- |
| **Alert Raised** | Correct: **True Positive** | Warning: False Positive |
| **No Alert** | Incorrect: False Negative | Correct: **True Negative** |

## True Positive (TP)

A **true positive** occurs when the system **correctly detects and alerts on a real threat**.

**Importance:**

- Shows the system is doing its job effectively.
- Critical to preventing breaches or attacks.
- Helps responders act quickly and mitigate the threat.

**Real-World Examples:**

- A firewall detects and blocks a **SQL injection attempt** on a login page.
- An antivirus tool correctly quarantines a **known ransomware sample** before it executes.
- An EDR system detects **lateral movement** using pass-the-hash tactics and alerts analysts.

## True Negative (TN)

A **true negative** occurs when the system **correctly identifies legitimate activity and takes no action**.

**Importance:**

- Reduces noise and unnecessary alerts.
- Prevents interruption of legitimate business processes.
- Shows good tuning and balance in the detection system.

**Real-World Examples:**

- A user logs into their work email from a trusted device - no alert is triggered.
- A developer uploads code to GitHub, and the system recognizes it as an approved action.
- Scheduled backups or automated scripts run, and the system does not flag them as suspicious.

## Importance

Together, **True Positives** and **True Negatives** represent the **desired outcomes** of any cybersecurity detection system:

- **True Positives** allow fast and accurate response to real threats.
- **True Negatives** ensure normal operations are not disrupted.

Over time, systems are **tuned and improved** to increase the rates of TPs and TNs while reducing FPs and FNs.

## Summary

| Term | Meaning | Impact |
| --- | --- | --- |
| **True Positive (TP)** | Real threat detected | Enables quick response |
| **True Negative (TN)** | Benign activity ignored | Keeps operations smooth |
| **False Positive (FP)** | Benign activity flagged | Wastes time/resources |
| **False Negative (FN)** | Real threat missed | Risk of breach/damage |

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
