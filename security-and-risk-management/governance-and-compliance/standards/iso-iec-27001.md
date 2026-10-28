# ISO/IEC 27001

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**ISO/IEC 27001** is an international standard published by the **International Organization for Standardization** and the **International Electrotechnical Commission** that defines requirements for establishing, implementing, maintaining, and continually improving an:

> Information Security Management System (ISMS)

### Core Objective

Ensure that organizations:

- Protect **confidentiality**
- Maintain **integrity**
- Ensure **availability** (CIA triad)

## Purpose

ISO 27001 is:

- A **management system standard** (not just technical controls)
- A **risk-based framework**
- A **certifiable standard**
- A **governance + operational model**

### Key Insight

> ISO 27001 focuses more on
>
> process, governance, and risk management
>
> than on specific technologies.

## Importance

Organizations face:

- Data breaches
- Regulatory pressure
- Supply chain risk
- Customer trust issues

ISO 27001 provides:

- Structured approach to security
- Global trust and credibility
- Standardized risk management

## Core components

ISO 27001 consists of two main parts:

### Clauses (4-10) - Management System Requirements

These define **how to build and operate ISMS**.

| Clause | Area |
| --- | --- |
| 4 | Context of the organization |
| 5 | Leadership |
| 6 | Planning |
| 7 | Support |
| 8 | Operation |
| 9 | Performance evaluation |
| 10 | Improvement |

#### Annex A - Security Controls

- A catalog of **93 controls (ISO 27001:2022)**
- Grouped into 4 domains

## Annex A Control Domains

### Organizational Controls (37)

- Policies
- Roles and responsibilities
- Risk management
- Supplier relationships

#### People Controls (8)

- Training
- Awareness
- HR security

#### Physical Controls (14)

- Secure areas
- Equipment protection
- Physical access control

#### Technological Controls (34)

- Access control
- Cryptography
- Logging
- Network security

## ISMS (Information Security Management System)

### Definition

A structured system that integrates:

- Policies
- Procedures
- Processes
- Controls

#### Purpose

Manage:

- Information security risks
- Continuous improvement

## PDCA Cycle

ISO 27001 is built on:

### Plan

- Define scope
- Identify risks
- Select controls

#### Do

- Implement controls
- Deploy policies

#### Check

- Monitor and audit

#### Act

- Improve continuously

## Risk Management in ISO 27001

### Key Concept

> Security decisions are driven by
>
> risk assessment
>
> , not arbitrary control selection.

#### Risk Assessment

Steps:

1. Identify assets
2. Identify threats
3. Identify vulnerabilities
4. Assess likelihood and impact
5. Calculate risk

#### Risk Treatment

Options:

- Mitigate
- Transfer
- Accept
- Avoid

#### Statement of Applicability (SoA)

A key document that:

- Lists selected controls
- Justifies inclusion/exclusion
- Maps controls to risks

## Certification Process

### Step 1 - Preparation

- Define ISMS scope
- Perform gap analysis

#### Step 2 - Implementation

- Deploy controls
- Establish policies

#### Step 3 - Internal Audit

- Verify readiness

#### Step 4 - Certification Audit

##### Stage 1

- Documentation review

##### Stage 2

- Full audit

#### Step 5 - Maintenance

- Continuous monitoring
- Annual audits

## ISO 27001 in DevSecOps

ISO 27001 integrates with DevSecOps through:

### Key Areas:

- Secure SDLC → Annex A controls
- CI/CD security → change management
- Secrets management → access control
- Logging & monitoring → audit requirements
- IaC → configuration management

## ISO 27001 vs Other Frameworks

| Framework | Focus |
| --- | --- |
| CIS Controls | Operational security |
| NIST CSF | Risk outcomes |
| RMF | Risk process |
| CSA CCM | Cloud controls |
| **ISO 27001** | **Governance + certification** |

## ISO 27001 vs ISO 27002

- **ISO 27001** → requirements (what must be done)
- **ISO 27002** → guidance (how to implement controls)

## Mapping to Cloud Security

ISO 27001 applies to:

- Cloud infrastructure
- SaaS
- Hybrid environments

Examples:

- IAM → access control policies
- Logging → audit requirements
- Encryption → data protection

## Common pitfalls

- Treating ISO as checkbox compliance
- Over-documentation without real security
- Ignoring technical controls
- Weak risk assessment process
- Lack of management involvement

## Tools supporting ISO 27001

- GRC tools (Governance, Risk, Compliance)
- SIEM systems
- IAM platforms
- Vulnerability scanners
- Asset management tools

## Skills Required for ISO 27001 Mastery

- Risk management
- Security governance
- Compliance frameworks
- Audit processes
- Technical security controls
- Documentation and policy design

## Real-World Use Cases

- SaaS companies → customer trust
- Enterprises → regulatory compliance
- Cloud providers → security assurance
- Startups → competitive advantage

## Strategic Value

ISO 27001 provides:

- Global recognition
- Structured security governance
- Risk-driven approach
- Business alignment

## ISO 27001 in the Security Ecosystem

If:

- CIS Controls → implementation
- CSA CCM → cloud controls
- RMF → risk management

Then:

> ISO 27001 ensures governance, compliance, and trust.

## Summary

ISO 27001 is essential for:

- Building **enterprise-grade security programs**
- Aligning **technical and business risk**
- Achieving **certification and trust**

It transforms security from:

> “Technical implementation”
>
> into
>
> “Business-driven risk management.”

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
