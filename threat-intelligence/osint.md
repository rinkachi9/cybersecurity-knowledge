---
title: OSINT
area: threat intelligence
level: unrated
status: draft
last_verified: unverified
tags: [migrated, osint, reconnaissance]
migrated_from: Security.html, page 4
---

# OSINT

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it it?

**Open-Source Intelligence (OSINT)** refers to the **collection, analysis, and use of publicly available information** to uncover insights about potential threats, vulnerabilities, or targets. Unlike covert or proprietary sources, OSINT relies entirely on **freely accessible data** - including websites, social media, forums, data breaches, and more.

In cybersecurity, OSINT is used to **support reconnaissance, threat hunting, incident response, and vulnerability discovery** - often by identifying weak points before attackers do.

### Importance

- Helps **detect exposed data** (e.g., credentials, infrastructure info)
- Identifies **external attack surfaces**
- Tracks **threat actors** and their behavior
- Supports **digital forensics** and **threat attribution**
- Provides **early warnings** from forums or leaked information

## Sources

| Category | Examples |
| --- | --- |
| **Websites** | Company sites, blogs, employee bios, GitHub |
| **Social Media** | LinkedIn, Twitter, Facebook, Instagram |
| **Search Engines** | Google Dorking, Shodan, Censys |
| **Paste Sites** | Pastebin, Ghostbin (often used for leaks) |
| **Public Repositories** | GitHub, GitLab (hardcoded secrets, configs) |
| **WHOIS/DNS Records** | Domain ownership, DNS info |
| **Data Breach Dumps** | Have I Been Pwned, DeHashed, IntelligenceX |
| **Forums/IRC/Dark Web** | Criminal forums, ransomware leak sites |

## Tools & frameworks

| Tool | Use Case |
| --- | --- |
| **Maltego** | Visual link analysis for people, domains, networks |
| **Recon-ng** | Web reconnaissance framework (modular, CLI-based) |
| **theHarvester** | Finds emails, domains, subdomains, names |
| **SpiderFoot** | Automated OSINT collection and correlation |
| **Google Dorks** | Advanced Google search operators for sensitive data |
| **Shodan** | Search engine for internet-connected devices |
| **Amass** | Subdomain enumeration and mapping attack surface |

### OSINT in the Cyber Kill Chain

- **Pre-Attack (Reconnaissance)**: Adversaries use OSINT to collect data on target systems, employees, or technologies.
- **Defense**: Security teams use OSINT to spot leaked credentials, sensitive infrastructure, or threat actor chatter.

## Defensive uses

- Monitor for **exposed credentials**
- Identify **employee oversharing** (e.g., on LinkedIn)
- Detect **typosquatted domains** or **spoofed emails**
- Discover **cloud buckets or repositories** left open to the public
- Map **shadow IT** infrastructure or outdated public-facing services
- Track **threat actor activity** in forums or darknet marketplaces

### Legal and ethical considerations

While OSINT uses public data, ethical and legal boundaries **must be respected**:

- Avoid unauthorized data access (e.g., bypassing authentication)
- Ensure privacy laws (e.g., GDPR) are followed
- Clearly separate **reconnaissance** from **intrusion**

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
