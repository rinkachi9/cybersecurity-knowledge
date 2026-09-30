# Cybersecurity Knowledge

A personal knowledge base about defending systems, understanding attackers and building secure software and infrastructure.

## Table of Contents

- [About](#about)
- [Purpose](#purpose)
- [Scope](#scope)
- [Knowledge areas](#knowledge-areas)
- [Full table of contents](#full-table-of-contents)
- [How to use this repository](#how-to-use-this-repository)
- [Repository layout](#repository-layout)
- [Contributing and working with AI agents](#contributing-and-working-with-ai-agents)
- [Related knowledge bases](#related-knowledge-bases)
- [Status](#status)

## About

This repository collects structured notes, explanations, checklists and worked examples about cybersecurity. It covers both the defensive side (hardening, detection, response) and the offensive knowledge that a defender needs (how attacks work, why they succeed, how they are found). Everything here is written for learning, for authorized testing and for defensive use.

This is a personal knowledge base, not a tutorial site or a product. The goal is depth and correctness. Notes are written so that they are still useful and understandable when I come back to them after a year, and so that someone new to the topic can follow them from top to bottom.

## Purpose

The repository exists to:

- build a durable, well organized reference for cybersecurity that I can search, extend and trust,
- force real understanding by requiring every concept to be explained precisely, with examples and analogies,
- keep a single, consistent standard for how knowledge is written down, so the collection stays coherent as it grows,
- provide a source of truth that both people and AI assistants can work with under the same rules.

## Scope

**In scope**

- Concepts, mechanisms and the reasoning behind them.
- Worked examples, exercises, comparisons, checklists and decision guides.
- Summaries of papers, books, documentation and talks, always in my own words and with a link to the source.

**Out of scope**

- Working malware, weaponized exploits or step by step guides aimed at real, unauthorized targets.
- Credentials, tokens, private keys, real customer data or anything obtained from a real breach.
- General software engineering topics that have no security angle (they belong in software-engineering-knowledge).

## Knowledge areas

The content is organized into the areas below. Each area has a `README.md` with its notes in a recommended reading order. Areas marked planned have no notes yet.

| Area | What it covers |
| --- | --- |
| [Foundations](foundations/README.md) | Cybersecurity basics, the CIA triad, defense in depth. |
| [Cryptography](cryptography/README.md) | Hashing and password hashing, public key infrastructure, and later encryption, TLS and key management. |
| [Identity and access](identity-and-access/README.md) | Authentication, authorization, tokens, OAuth and OpenID Connect. |
| [Threat modeling](threat-modeling/README.md) | Threat modeling concepts and the STRIDE, attack tree, PASTA, Trike, hTMM and Security Cards methods. |
| [Vulnerability management](vulnerability-management/README.md) | CVE, NVD, CVSS, CWE and zero-day attacks. |
| [Threat intelligence](threat-intelligence/README.md) | Threat intelligence, OSINT, VirusTotal and the MITRE knowledge bases. |
| [Threats and attacks](threats-and-attacks/README.md) | Attack categories, malware, social engineering, web and credential attacks, reconnaissance, privilege escalation. |
| [Application security](application-security/README.md) | OWASP, XSS, SAST, DAST, SCA and software supply chain security. |
| [Defensive operations](defensive-operations/README.md) | SOC, SecOps, SIEM, SOAR, detection systems, and later logging, incident response and forensics. |
| [Governance and compliance](governance-and-compliance/README.md) | Risk management, control frameworks (NIST, CIS, CSA) and ISO/IEC 27001. |
| [Privacy and data protection](privacy-and-data-protection/README.md) | GDPR, PIPEDA, HIPAA, FTC Act, COPPA, GLBA and the NIST Privacy Framework. |
| [AI security](ai-security/README.md) | Security of AI and ML systems. |
| [Cloud and infrastructure security](cloud-and-infrastructure-security/README.md) | Security posture management, and later shared responsibility, hardening, secrets, container and Kubernetes security. |
| [Operating system security](operating-system-security/README.md) | Operating system mechanisms such as seccomp on Linux. |
| [Organizations and certifications](organizations-and-certifications/README.md) | NIST, SANS, Mandiant and ISC2. |
| [Network security](network-security/README.md) (planned) | Protocols, segmentation, firewalls, VPNs, traffic analysis. |
| [Offensive security](offensive-security/README.md) (planned) | Penetration testing methodology, exploitation concepts, red team tradecraft (authorized contexts only). |

## Full table of contents

[ToC.md](ToC.md) lists every file in the repository as an indented tree. It is kept in sync with every change.

## How to use this repository

1. **Start with the [GUIDELINE](GUIDELINE.md).** It defines how notes are structured, how concepts are explained, the writing style and the quality bar. Read it before adding or editing anything.
2. **Browse by area.** Pick an area from the table above. Each area has an entry point that lists its topics in a sensible reading order. [ToC.md](ToC.md) shows everything at once.
3. **Read notes top to bottom the first time.** Notes are written to build from a plain language summary to precise detail. Later visits can jump straight to the section that is needed.
4. **Follow the links.** Notes link to prerequisites and related topics instead of repeating them.

## Repository layout

The layout will grow with the content. The current shape is:

```text
.
|-- README.md          # this file: what the repository is and how to navigate it
|-- GUIDELINE.md       # how to write and maintain material in this repository
|-- ToC.md             # full tree of every file, updated with every change
|-- AGENTS.md          # instructions for AI agents, points to GUIDELINE.md
|-- CLAUDE.md          # instructions for Claude Code, points to GUIDELINE.md
|-- .gitignore
|-- assets/<area>/     # images, diagram sources, media and downloadable files
|-- scripts/<area>/    # scripts and tools referenced by notes (repository tooling is in scripts/)
`-- <area>/            # one directory per knowledge area (see GUIDELINE.md)
    |-- README.md      # entry point and reading order for the area
    |-- <topic>.md     # individual notes
    `-- <subarea>/     # optional group of related notes, with its own README.md
```

The exact naming and structure rules are described in [GUIDELINE.md](GUIDELINE.md#3-repository-structure-and-naming).

## Contributing and working with AI agents

The repository is maintained by one person, but it is designed so that AI assistants can help write and review material. [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) both point to [GUIDELINE.md](GUIDELINE.md), which is the single source of truth for conventions. If a rule needs to change, change it in the GUIDELINE and nowhere else.

## Related knowledge bases

This repository is one of a family of knowledge bases. Topics that belong elsewhere are linked, not duplicated.

- **data-analytics-knowledge**: statistics, SQL, experimentation and analytics engineering.
- **databases-knowledge**: data models, storage, transactions and operations.
- **devops-knowledge**: CI/CD, infrastructure as code, containers and observability.
- **google-cloud-knowledge**: Google Cloud services, architecture and operations.
- **ml-al-knowledge**: machine learning, deep learning and AI systems.
- **software-engineering-knowledge**: design, architecture, testing and code quality.

## Status

The structure and rules are in place. The first batch of notes was migrated from an older HTML export and is marked `status: draft` with `TODO:` markers where the standard in the GUIDELINE is not yet met (see [migrated notes](GUIDELINE.md#41-migrated-notes)). Content is being added and reviewed area by area.
