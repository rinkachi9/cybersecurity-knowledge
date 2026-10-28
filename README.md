# Cybersecurity Knowledge

A personal knowledge base about defending systems, understanding attackers and building secure software and infrastructure.

## Table of Contents

- [About](#about)
- [Purpose](#purpose)
- [Scope](#scope)
- [Knowledge areas](#knowledge-areas)
- [Taxonomy](#taxonomy)
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

The eight top level content directories use the eight domains in the [ISC2 CISSP Certification Exam Outline, effective April 15, 2024](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf). The outline describes the CISSP common body of knowledge. It is a certification content outline, not an ISO standard or a prescribed repository file tree. Every domain has a `README.md` with its current notes and a reading order.

| CISSP domain | Repository section | Current material |
| --- | --- | --- |
| 1. Security and Risk Management | [Security and risk management](security-and-risk-management/README.md) | Foundations, governance, risk, threat modeling, awareness, privacy law and reference material, including the CISSP and its domains. |
| 2. Asset Security | [Asset security](asset-security/README.md) | Privacy and data protection, with asset lifecycle topics planned. |
| 3. Security Architecture and Engineering | [Security architecture and engineering](security-architecture-and-engineering/README.md) | Design principles, cryptography, cloud, operating systems, secure AI architecture and planned component security. |
| 4. Communication and Network Security | [Communication and network security](communication-and-network-security/README.md) | Zero trust architecture, with more network topics planned. |
| 5. Identity and Access Management | [Identity and access management](identity-and-access-management/README.md) | Authentication, authorization, identity protocols and credential attacks. |
| 6. Security Assessment and Testing | [Security assessment and testing](security-assessment-and-testing/README.md) | Team exercises and planned assessment methods. |
| 7. Security Operations | [Security operations](security-operations/README.md) | Monitoring, response, digital forensics, threat intelligence, vulnerability management and attack patterns. |
| 8. Software Development Security | [Software development security](software-development-security/README.md) | Application security, software testing and supply chain security. |

## Taxonomy

The domain names and their scope come from the [ISC2 CISSP Certification Exam Outline](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf), effective April 15, 2024 and checked in October 2026. ISC2 says a [new outline takes effect April 15, 2027](https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline); review this mapping against that edition when it becomes effective. The domain structure is a practical organization for this knowledge base. Notes are placed by their main learning objective, and related domains link to the single home note. The [GUIDELINE](GUIDELINE.md#311-cissp-domain-placement) defines the placement rules.

The existing material maps into the domains as follows:

| Topic group | Home domain | Reason |
| --- | --- | --- |
| Security concepts, CIA triad, governance, risk, threat modeling and social engineering | [Security and Risk Management](security-and-risk-management/README.md) | CISSP sections 1.2, 1.3, 1.9, 1.10 and 1.12 cover these topics. |
| Privacy framework and data protection concepts | [Asset Security](asset-security/README.md) | The main concern is the protection and handling of information. Privacy laws sit in Domain 1. |
| Cryptography, defense in depth, cloud, operating systems, secure AI architecture and components | [Security Architecture and Engineering](security-architecture-and-engineering/README.md) | The notes explain system design and technical security mechanisms. The NIST AI RMF has its home in Domain 1 because it focuses on risk management. |
| Network security and zero trust architecture | [Communication and Network Security](communication-and-network-security/README.md) | The notes concern access to networked resources and network design. |
| Authentication, authorization, identity protocols and credential attacks | [Identity and Access Management](identity-and-access-management/README.md) | The notes explain identity controls and their failure modes. |
| Red, blue and purple team exercises and planned authorized testing | [Security Assessment and Testing](security-assessment-and-testing/README.md) | The focus is testing controls and reporting findings. |
| SOC, detection, incident response, threat intelligence, vulnerability management and attack patterns | [Security Operations](security-operations/README.md) | The notes support monitoring, investigation, response and maintenance. |
| OWASP, application weaknesses, SAST, DAST, SCA and software supply chains | [Software Development Security](software-development-security/README.md) | The notes focus on the software development lifecycle and application testing. |

Organizations and certifications live in [Domain 1 reference material](security-and-risk-management/reference/README.md). They are supporting context, not an additional CISSP domain. No dedicated notes yet cover asset classification, general security audits, network protocols, disaster recovery or most of digital forensics (only chain of custody is covered). These are visible as planned topics instead of placeholder notes.

## Full table of contents

[ToC.md](ToC.md) lists every file in the repository as an indented tree. It is kept in sync with every change.

## How to use this repository

1. **Start with the [GUIDELINE](GUIDELINE.md).** It defines how notes are structured, how concepts are explained, the writing style and the quality bar. Read it before adding or editing anything.
2. **Browse by area.** Pick an area from the table above. Each area has an entry point that lists its topics in a sensible reading order. [ToC.md](ToC.md) shows everything at once.
3. **Read notes top to bottom the first time.** Notes are written to build from a plain language summary to precise detail. Later visits can jump straight to the section that is needed.
4. **Follow the links.** Notes link to prerequisites and related topics instead of repeating them.
5. **Check the metadata.** Each content note has a `.md.json` sidecar for Librarian OS. The Markdown is the source of truth for prose. Sidecars are marked `draft` until the note meets the [quality checklist](GUIDELINE.md#10-quality-checklist).

## Repository layout

```text
.
|-- README.md                       # repository overview and domain mapping
|-- GUIDELINE.md                    # writing and classification rules
|-- INSTRUCTIONS.md                 # Librarian OS integration guide
|-- librarian-os.json               # eight Librarian OS entry points
|-- ToC.md                          # complete file tree
|-- _roadmaps/                      # main roadmap, one sub-roadmap per domain (d1 to d8) and thematic roadmaps
|-- _assets/<domain>/               # media and downloadable files
`-- <cissp-domain>/                 # one of the eight CISSP domains
    |-- README.md                   # domain entry point and reading order
    |-- <topic>.md                  # individual note
    `-- <subarea>/                  # related notes with their own README
```

The naming and placement rules are in [GUIDELINE.md](GUIDELINE.md#3-repository-structure-and-naming). [Librarian OS](INSTRUCTIONS.md) reads the eight configured domains; root guidance files stay outside its content tree.

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

The structure and rules are in place. The first batch of notes was migrated from an older HTML export and has `TODO:` markers where the standard in the GUIDELINE is not yet met (see [migrated notes](GUIDELINE.md#41-migrated-notes)). Content is being added and reviewed area by area.
