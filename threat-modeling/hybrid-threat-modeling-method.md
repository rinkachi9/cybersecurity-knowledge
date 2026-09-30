---
title: Hybrid Threat Modeling Method (hTMM)
area: threat modeling
level: unrated
status: draft
last_verified: unverified
tags: [migrated, htmm]
migrated_from: Security.html, page 20
---

# Hybrid Threat Modeling Method (hTMM)

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

Hybrid Threat Modeling Method (hTMM) is a **combined threat modeling approach** that integrates multiple methodologies (e.g., STRIDE, PASTA, Attack Trees, Security Cards) to leverage their strengths while mitigating their weaknesses.

hTMM is not a single standardized framework but rather a **practical strategy** used by mature security teams to:

- Balance **simplicity and depth**
- Combine **threat identification + risk analysis + attack simulation**
- Adapt threat modeling to **real-world constraints**

**Core objective:**

To create a **flexible, scalable, and context-aware threat modeling process** that aligns with both **technical and business needs**.

## Importance

Single-method approaches often have limitations:

- STRIDE → lacks risk prioritization
- PASTA → complex and resource-heavy
- Attack Trees → may lack structure
- Security Cards → informal

hTMM addresses this by:

- Combining multiple perspectives
- Allowing **progressive maturity**
- Supporting **continuous threat modeling**

This makes it:

- Ideal for **DevSecOps environments**
- Suitable for **cloud-native systems**
- Effective for **large-scale architectures**

## Core philosophy

hTMM is built around:

### Composability

Use the right method for the right stage:

- STRIDE → identification
- PASTA → deep analysis
- Attack Trees → attack paths

#### Risk-Driven Security

Prioritize based on:

- Business impact
- Exploitability
- Exposure

#### Iterative Modeling

Threat modeling is:

- Continuous
- Integrated into CI/CD
- Updated with system evolution

#### Pragmatism Over Purity

Instead of strictly following one framework:

> Combine methods to achieve practical results.

## Key concepts

### Multi-Method Integration

Typical components:

- STRIDE → threat categorization
- PASTA → attack simulation
- Attack Trees → path modeling
- CVSS → severity scoring
- MITRE ATT&CK → attacker techniques

#### Layered Analysis

Threat modeling is performed at:

- High level (architecture)
- Mid level (services)
- Low level (implementation)

#### Context Awareness

Adapt methodology based on:

- System complexity
- Risk level
- Team maturity

#### Continuous Feedback Loop

Integrate:

- Runtime telemetry
- Incident data
- Threat intelligence

## hTMM Model Structure

hTMM is typically structured as:

```text
1. Threat Discovery (STRIDE / Security Cards)
2. System Decomposition (DFD / Architecture)
3. Attack Modeling (Attack Trees)
4. Risk Analysis (CVSS + Business Context)
5. Simulation (PASTA / Red Teaming)
6. Mitigation & Validation
7. Continuous Monitoring & Feedback
```

## hTMM Process

### Step 1 - Define Scope & Context

Identify:

- Business objectives
- Critical assets
- Compliance requirements

#### Step 2 - Initial Threat Identification

Use:

- STRIDE (structured)
- Security Cards (creative)

Goal:

- Generate broad threat list

#### Step 3 - System Decomposition

Create:

- Data Flow Diagrams
- Architecture diagrams

Identify:

- Trust boundaries
- Attack surfaces

#### Step 4 - Attack Modeling

Use Attack Trees to:

- Model attack paths
- Identify multi-step exploits

#### Step 5 - Risk Analysis

Combine:

- CVSS (severity)
- Business impact
- Exposure

#### Step 6 - Attack Simulation

Use:

- PASTA stages (simulation)
- Pen testing
- Red teaming

#### Step 7 - Mitigation Design

Define:

- Preventive controls
- Detective controls
- Response mechanisms

#### Step 8 - DevSecOps Integration

Embed into:

- CI/CD pipelines
- Security testing
- Policy enforcement

#### Step 9 - Continuous Monitoring

Use:

- SIEM
- Observability tools
- Threat intelligence

## Practical Example

**System:**

Cloud-native SaaS (Kubernetes + API + Keycloak)

### Step 1 - STRIDE

Identify threats:

- Spoofing → token abuse
- EoP → IAM misconfiguration

#### Step 2 - Attack Tree

```text
Gain admin access
 ├── Exploit IAM misconfiguration
 ├── Steal credentials
 └── Abuse API vulnerability
```

#### Step 3 - CVSS

- IAM misconfiguration → High severity
- API bug → Medium

#### Step 4 - PASTA Simulation

Simulate:

- Credential theft → lateral movement → privilege escalation

#### Step 5 - Mitigation

- RBAC hardening
- MFA
- API Gateway
- Monitoring

## hTMM vs STRIDE

| Aspect | hTMM | STRIDE |
| --- | --- | --- |
| Scope | Comprehensive | Threat identification |
| Flexibility | High | Low |
| Depth | High | Medium |
| Use case | Advanced | Entry-level |

## hTMM vs PASTA

| Aspect | hTMM | PASTA |
| --- | --- | --- |
| Approach | Hybrid | Structured |
| Flexibility | High | Medium |
| Complexity | Adjustable | High |
| Use case | Real-world DevSecOps | Deep analysis |

## hTMM in DevSecOps

hTMM is ideal for:

### CI/CD Integration

- Threat modeling as code
- Security gates
- Automated scanning

#### Secure SDLC

- Design → STRIDE
- Build → SAST/SCA
- Test → DAST
- Run → Monitoring

#### Example

Pipeline:

```text
Code → STRIDE checks → SAST → CVSS scoring → Policy enforcement → Deploy
```

## hTMM in Cloud Environments

Use cases:

- Kubernetes security
- IAM modeling
- API security
- Multi-tenant systems

hTMM helps:

- Combine:
  - Architecture-level analysis
  - Runtime threat detection
- Support Zero Trust

## Strengths

- Flexible and adaptable
- Combines best methodologies
- Suitable for modern architectures
- Supports continuous security

## Weaknesses

- Requires expertise
- No strict standardization
- Can become complex if unmanaged

## Common pitfalls

- Overengineering the process
- Using too many methods unnecessarily
- Lack of clear ownership
- Poor integration with CI/CD

## Skills Required

- Threat modeling (STRIDE, PASTA)
- Risk analysis
- Cloud security
- DevSecOps practices
- Security architecture

## When to Use hTMM

Best suited for:

- Mature DevSecOps teams
- Cloud-native systems
- Large-scale architectures
- High-risk environments

## When NOT to Use

Avoid if:

- Small projects
- Low security maturity
- Limited resources

## Integration with Other Frameworks

hTMM integrates naturally with:

- **MITRE ATT&CK** → attacker techniques
- **NIST RMF** → governance
- **ISO 27001** → compliance
- **CIS Controls** → implementation
- **OWASP** → vulnerabilities

## Strategic Value

hTMM transforms threat modeling from:

> “Use one methodology”

into:

> “Use the right methodology at the right time.”

## Summary

hTMM is:

- A **practical, real-world approach to threat modeling**
- Designed for **modern DevSecOps environments**
- Focused on **flexibility, integration, and effectiveness**

It provides:

- Depth (PASTA)
- Structure (STRIDE)
- Visualization (Attack Trees)
- Prioritization (CVSS)

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
