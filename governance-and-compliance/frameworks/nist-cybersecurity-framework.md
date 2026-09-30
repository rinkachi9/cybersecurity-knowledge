---
title: Cybersecurity Framework (CSF)
area: governance and compliance
level: unrated
status: draft
last_verified: unverified
tags: [migrated, nist, csf]
migrated_from: Security.html, page 36
---

# Cybersecurity Framework (CSF)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

The **Cybersecurity Framework (CSF)** is a **risk-based, outcome-oriented framework** developed by the **National Institute of Standards and Technology (NIST)** to help organizations **identify, assess, manage, and reduce cybersecurity risk**.

The CSF is **not a prescriptive standard**. Instead, it provides:

- A **common language** for cybersecurity risk management
- A **structured taxonomy** of cybersecurity outcomes
- A **flexible model** adaptable to organizations of any size, sector, or maturity

Originally released in 2014 and significantly evolved (CSF 1.1 → CSF 2.0), the framework is now used globally across:

- Critical infrastructure
- Cloud-native organizations
- Software companies
- Government and regulated sectors
- DevSecOps and product security teams

## Core design principles

The CSF is built on several fundamental principles that every security professional must understand:

### Risk-Based

Security controls are selected and prioritized based on **business risk**, not technical fashion.

#### Outcome-Focused

CSF defines **what should be achieved**, not **how** to implement it.

#### Technology-Agnostic

Applicable to:

- On-premise
- Cloud (IaaS, PaaS, SaaS)
- Containers & Kubernetes
- IoT and OT environments

#### Adaptable & Incremental

Supports gradual maturity improvements rather than “big bang” transformations.

## Structure overview

The CSF consists of **four integrated components**:

1. **Core**
2. **Profiles**
3. **Implementation Tiers**
4. **CSF Governance & Risk Integration (CSF 2.0 enhancement)**

### Core - functions, categories, subcategories

The **Core** defines cybersecurity activities and desired outcomes using a hierarchical structure:

#### Six CSF Functions (CSF 2.0)

| Function | Purpose |
| --- | --- |
| **Govern** | Establish cybersecurity governance, risk strategy, and oversight |
| **Identify** | Understand organizational context, assets, and risks |
| **Protect** | Implement safeguards to limit impact |
| **Detect** | Identify cybersecurity events |
| **Respond** | Contain and mitigate incidents |
| **Recover** | Restore services and improve resilience |

> Important:
>
> Govern
>
> was added in CSF 2.0 to explicitly address executive accountability and enterprise risk management (ERM).

#### GOVERN Function (New in CSF 2.0)

**Purpose:** Ensure cybersecurity is treated as a **strategic business risk**, not an IT issue.

Key areas:

- Cybersecurity policy & strategy
- Roles and responsibilities
- Legal & regulatory requirements
- Third-party and supply chain risk
- Metrics, KPIs, and reporting

**Security Specialist Insight:**

This function bridges **security engineering with leadership**, making it critical for senior, lead, and advisory roles.

#### IDENTIFY Function

**Purpose:** Understand *what must be protected* and *why*.

Key Categories:

- Asset Management
- Business Environment
- Governance (legacy in 1.1)
- Risk Assessment
- Risk Management Strategy
- Supply Chain Risk Management

**Key Skills Required:**

- Asset inventory (including shadow IT)
- Threat modeling (STRIDE, PASTA)
- Risk assessment methodologies (qualitative & quantitative)
- Cloud asset discovery

#### PROTECT Function

**Purpose:** Reduce likelihood and impact of incidents.

Key Categories:

- Identity and Access Management (IAM)
- Awareness and Training
- Data Security
- Platform Security
- Protective Technology

**Typical Controls:**

- Zero Trust Architecture
- Least Privilege & RBAC/ABAC
- Secrets management
- Encryption (at rest & in transit)
- Secure SDLC & DevSecOps pipelines

#### DETECT Function

**Purpose:** Identify anomalies and security events quickly.

Key Categories:

- Continuous Monitoring
- Detection Processes
- Anomalies and Events

**Key Practices:**

- Centralized logging
- SIEM & XDR
- Behavioral analytics
- Detection engineering (Sigma, YARA-L)

#### RESPOND Function

**Purpose:** Contain incidents and minimize damage.

Key Categories:

- Incident Response Planning
- Communications
- Analysis
- Mitigation
- Improvements

**Security Specialist Focus:**

- IR playbooks
- Forensics readiness
- Legal & regulatory coordination
- Crisis communication

#### RECOVER Function

**Purpose:** Restore operations and strengthen resilience.

Key Categories:

- Recovery Planning
- Improvements
- Communications

**Key Topics:**

- Disaster Recovery (DR)
- Business Continuity (BCP)
- RTO/RPO definitions
- Post-incident reviews (lessons learned)

### CSF Profiles

A **Profile** represents alignment between:

- **Current State** (what you do today)
- **Target State** (desired outcomes)

Profiles allow organizations to:

- Measure gaps
- Prioritize improvements
- Align cybersecurity with business objectives

Example Profiles:

- Cloud-native SaaS startup
- Financial institution (regulated)
- Industrial IoT operator
- Healthcare provider

**Professional Use Case:**

Profiles are widely used in **security assessments, audits, and roadmaps**.

### Implementation tiers

Implementation Tiers describe how well cybersecurity risk management is integrated into organizational practices.

| Tier | Name | Characteristics |
| --- | --- | --- |
| Tier 1 | Partial | Ad-hoc, reactive |
| Tier 2 | Risk Informed | Some policies, inconsistent execution |
| Tier 3 | Repeatable | Formalized, documented processes |
| Tier 4 | Adaptive | Continuous improvement, threat-informed |

> Tiers measure
>
> process maturity
>
> , not technical security level.

### Informative References (Control Mapping)

CSF maps to existing standards and best practices, including:

- ISO/IEC 27001 & 27002
- NIST SP 800-53
- CIS Critical Security Controls
- COBIT
- Cloud provider security frameworks

**Why This Matters:**

CSF acts as a **meta-framework**, enabling alignment across compliance, audits, and engineering controls.

## CSF and DevSecOps

For modern security specialists, CSF integrates naturally with DevSecOps:

| CSF Function | DevSecOps Example |
| --- | --- |
| Govern | Security policies as code |
| Identify | IaC scanning, asset discovery |
| Protect | SAST, DAST, secrets scanning |
| Detect | Runtime security, observability |
| Respond | Automated incident workflows |
| Recover | Immutable infrastructure |

## Common pitfalls

- Treating CSF as a checklist
- Ignoring business context
- Over-focusing on Protect, ignoring Detect/Respond
- No metrics or KPIs
- Poor executive engagement

## CSF in Practice

- **Security program design**
- **Gap analysis & maturity assessment**
- **Vendor risk evaluation**
- **Cloud security posture management**
- **Regulatory alignment**
- **Board-level reporting**

## CSF Mastery

A professional fluent in CSF demonstrates:

- Risk-based thinking
- Strategic security planning
- Communication with executives
- Ability to design scalable security programs
- Cross-domain security understanding (cloud, app, infra)

## CSF 2.0 - Strategic Shift

CSF 2.0 emphasizes:

- Governance and accountability
- Enterprise Risk Management (ERM)
- Supply chain security
- Metrics and continuous improvement

This reflects the reality that **cybersecurity is now a core business risk**.

## Apply CSF

Recommended path:

1. Study CSF Core in detail
2. Map it to real systems you know
3. Build Profiles for different organizations
4. Align CSF with DevSecOps workflows
5. Practice communicating CSF outcomes to non-technical stakeholders

## Final Perspective

The NIST Cybersecurity Framework is **not a tool** - it is a **mental model**.

For aspiring and advanced security professionals, CSF provides:

- Structure without rigidity
- Strategy without abstraction
- A shared language across technical and business domains

Mastering CSF is foundational for roles such as:

- Security Engineer
- DevSecOps Engineer
- Security Architect
- GRC Specialist
- CISO / Security Lead

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
