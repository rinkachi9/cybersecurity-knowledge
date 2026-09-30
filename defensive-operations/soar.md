---
title: SOAR
area: defensive operations
level: unrated
status: draft
last_verified: unverified
tags: [migrated, soar]
migrated_from: Security.html, page 58
---

# SOAR

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

If the SIEM is the "Brain" that processes information and spots trouble, SOAR (Security Orchestration, Automation, and Response) is the "Nervous System" and "Muscles." It is the technology that allows a SecOps team to take the information provided by the SIEM and act on it - often at machine speed.

## Core concepts

To understand SOAR, you must look at its three distinct functional pillars:

### Orchestration (Connecting the Tools)

Modern environments use dozens of disconnected security tools (Firewalls, EDR, Email Gateways, Active Directory). Orchestration is the "glue." It allows these different technologies to talk to each other and work together in a unified workflow.

#### Automation (Executing the Tasks)

This is the ability to execute tasks without human intervention. If a task is repetitive (e.g., checking a file hash on VirusTotal), SOAR automates it. This eliminates the "grunt work" that leads to analyst burnout.

#### Response (Neutralizing the Threat)

This is the final stage. Once a threat is confirmed, SOAR facilitates the remediation - whether that’s automatically isolating a laptop from the network, deleting a malicious email from 500 mailboxes simultaneously, or resetting a compromised user's password.

## Core engine: playbooks

The heart of any SOAR platform is the Playbook. A playbook is a digital, automated version of a Standard Operating Procedure (SOP).

> Example: The Phishing Playbook
>
> Trigger: An employee reports a suspicious email.
>
> Orchestration: SOAR extracts the URL from the email and sends it to a sandbox (e.g., Joe Security) and a reputation service (e.g., URLScan).
>
> Decision: If the URL is flagged as malicious:
>
> Action A: Automatically block the URL on the corporate Firewall.
>
> Action B: Search all other mailboxes for the same email and delete them.
>
> Action C: Post a message in the Security Slack channel:
>
> "Threat neutralized."
>
> Closing: The ticket is automatically resolved in Jira/ServiceNow.

Total time taken: 30 seconds. (A human would take 30-60 minutes).

## SIEM vs. SOAR

It is common to confuse the two, but they serve different roles in the SecOps ecosystem:

| **Feature** | **SIEM (The Brain)** | **SOAR (The Muscle)** |
| --- | --- | --- |
| Primary Goal | Log collection, correlation, and alerting. | Task automation and incident response. |
| Output | An Alert (e.g., "Potential malware detected"). | An Action (e.g., "Laptop isolated"). |
| Focus | Identifying what is happening. | Deciding how to handle what is happening. |
| Data Flow | Ingests massive amounts of raw data. | Interacts with APIs of other security tools. |

### Importance

The "Security Gap" is the main driver for SOAR adoption. Organizations face three major problems:

1. Alert Fatigue: SIEMs generate thousands of alerts. Humans can't keep up. SOAR filters the noise.
2. The Talent Shortage: There aren't enough skilled cybersecurity professionals. SOAR allows a small team to perform like a much larger one.
3. MTTR (Mean Time to Respond): Hackers move fast. Manual response is too slow. SOAR reduces response times from hours to seconds.

## Critical challenges

SOAR is not a "plug-and-play" solution. It requires maturity:

- Garbage In, Garbage Out: If your manual processes are messy, automating them will only create "automated mess." You must have clear processes before you can build playbooks.
- Maintenance: APIs change. A playbook that worked yesterday might break today because a vendor updated their software.
- Trust Issues: Many organizations are afraid to let a machine automatically "block" things for fear of breaking business-critical systems (e.g., accidentally blocking the CEO's account).

## Leading tools

- Palo Alto Networks (Cortex XSOAR): Widely considered the market leader with the largest library of pre-built integrations.
- Splunk SOAR (formerly Phantom): Deeply integrated with the Splunk ecosystem.
- Google Chronicle SOAR (formerly Siemplify): Known for its intuitive, analyst-centric "case management" approach.
- Fortinet (FortiSOAR): Highly customizable for large enterprises and MSSPs (Managed Security Service Providers).

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
