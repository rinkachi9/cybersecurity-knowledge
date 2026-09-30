---
title: Attack Simulation and Threat Analysis (PASTA)
area: threat modeling
level: unrated
status: draft
last_verified: unverified
tags: [migrated, pasta]
migrated_from: Security.html, page 17
---

# Attack Simulation and Threat Analysis (PASTA)

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

PASTA (Process for Attack Simulation and Threat Analysis) is a **risk-centric, attacker-focused threat modeling methodology** designed to:

- Align security analysis with **business impact and risk**
- Simulate **real-world attack scenarios**
- Identify **exploitable weaknesses before attackers do**
- Enable **informed security decision-making**

**Core objective:**

To model how real attackers would compromise a system and evaluate the **business impact of those attacks**, enabling **prioritized and risk-driven security controls**.

## Importance

Traditional threat modeling approaches (e.g., STRIDE):

- Focus on categorizing threats
- Often lack deep **business context**
- Do not simulate real attack paths
- Can be too abstract or theoretical

PASTA addresses these gaps by:

- Starting from **business objectives and risk**
- Simulating **real attack scenarios**
- Mapping **technical vulnerabilities to business impact**

This makes it:

- Highly aligned with **DevSecOps and risk management**
- Suitable for **modern distributed systems (microservices, cloud)**
- Effective for **security testing and validation**

## Core philosophy

PASTA is built around:

### Risk-Driven Security

Security decisions are based on:

- Business impact
- Threat likelihood
- Real attacker capabilities

#### Attacker-Centric Modeling

Instead of asking:

> “What threats exist?”

PASTA asks:

> “How would a real attacker compromise this system?”

#### Simulation-Based Approach

PASTA emphasizes:

- Attack path simulation
- Exploit chaining
- Realistic adversarial thinking

#### Business Context Integration

Security is evaluated in terms of:

- Financial loss
- Operational disruption
- Regulatory impact
- Reputation damage

## Key concepts

### Assets

Anything of value:

- Sensitive data (PII, financial data)
- APIs and services
- Infrastructure (cloud, containers, networks)

#### Threat Actors

Entities that may attack the system:

- External attackers
- Insider threats
- Automated bots
- Advanced Persistent Threats (APTs)

#### Attack Surface

All entry points into the system:

- APIs
- Web interfaces
- Network endpoints
- CI/CD pipelines
- Supply chain dependencies

#### Vulnerabilities

Weaknesses that can be exploited:

- Misconfigurations (e.g., IAM, Kubernetes)
- Software flaws (OWASP Top 10)
- Weak authentication/authorization

#### Attack Paths

Sequences of actions an attacker can take:

Example:

```text
Phishing → Credential theft → API access → Privilege escalation → Data exfiltration
```

#### Risk

Defined as:

- Likelihood of attack success
- Impact on business

PASTA explicitly connects:

> Technical exploit → Business consequence

## PASTA Model Structure

PASTA is a **7-stage process** that moves from business context to technical validation.

It combines:

- Business analysis
- System decomposition
- Threat intelligence
- Attack simulation

### PASTA Process

#### Stage 1 - Define Business Objectives

Identify:

- Business goals
- Critical processes
- Compliance requirements (e.g., ISO 27001, GDPR)

**Output:**

- Business impact criteria
- Risk tolerance

#### Stage 2 - Define Technical Scope

Identify:

- Application boundaries
- Architecture components
- Data flows

Includes:

- APIs
- Microservices
- Cloud infrastructure
- External integrations

#### Stage 3 - Application Decomposition

Break down the system into:

- Components
- Trust boundaries
- Data flows

Tools:

- Data Flow Diagrams (DFD)
- Architecture diagrams

#### Stage 4 - Threat Analysis

Identify threats using:

- Threat intelligence
- MITRE ATT&CK framework
- OWASP Top 10

Focus:

- Real-world attack techniques
- Known adversary behaviors

#### Stage 5 - Vulnerability Analysis

Map:

- Known vulnerabilities (CVEs)
- Misconfigurations
- Weak controls

Sources:

- SAST/DAST
- Dependency scanning
- Cloud security tools (CSPM)

#### Stage 6 - Attack Simulation

This is the **core differentiator of PASTA**.

Simulate:

- Attack scenarios
- Exploit chains
- Lateral movement

Techniques:

- Red teaming
- Penetration testing
- Attack path modeling

#### Stage 7 - Risk Analysis & Mitigation

Evaluate:

- Likelihood of attack success
- Business impact

Define:

- Security controls
- Mitigation strategies
- Risk prioritization

## PASTA vs STRIDE

| Aspect | PASTA | STRIDE |
| --- | --- | --- |
| Approach | Risk-driven | Threat category-based |
| Focus | Real attack simulation | Threat identification |
| Business alignment | Strong | Limited |
| Complexity | High | Moderate |
| Use case | Enterprise, critical systems | General threat modeling |

## PASTA vs Risk Management Framework (RMF)

| Aspect | PASTA | RMF |
| --- | --- | --- |
| Scope | Threat modeling | Governance & compliance |
| Focus | Attack simulation | Risk lifecycle |
| Output | Attack paths & mitigations | Risk decisions |
| Integration | Tactical/operational | Strategic |

## Practical Example

**System:**

Cloud-based financial API (microservices on Kubernetes)

**Assets:**

- Transaction data
- User credentials
- Payment processing service

**Threat Actor:**

- External attacker

**Attack Path:**

1. Exploit API misconfiguration
2. Bypass authentication
3. Access internal service
4. Escalate privileges
5. Extract financial data

**Vulnerabilities:**

- Weak API authentication
- Misconfigured IAM roles
- Lack of network segmentation

**Business Impact:**

- Financial loss
- Regulatory penalties (GDPR)
- Reputation damage

**Mitigations:**

- Strong authentication (OAuth2 + mTLS)
- Zero Trust architecture
- Network policies (Kubernetes)
- API Gateway (e.g., Apigee)
- Runtime security monitoring

## PASTA in DevSecOps

PASTA integrates naturally into **Secure SDLC**:

### Design Phase

- Threat modeling using PASTA stages 1-4

#### Build Phase

- SAST, SCA, IaC scanning

#### Test Phase

- DAST
- Pen testing
- Attack simulations

#### Deploy Phase

- Security gates in CI/CD

#### Operate Phase

- Runtime monitoring
- Threat detection (SIEM, EDR)

**Example:**

- Define attack scenarios → implement detection rules in SIEM
- Simulate attacks → validate security controls in pipeline

## PASTA in Cloud Environments

Highly relevant for:

- Kubernetes (GKE, EKS)
- Serverless (Cloud Run, Lambda)
- API-driven architectures

Use cases:

- IAM misconfiguration analysis
- API attack surface modeling
- Multi-tenant isolation validation

PASTA helps:

- Prevent privilege escalation
- Identify lateral movement paths
- Validate Zero Trust architecture

## Strengths

- Strong alignment with **real-world attacks**
- Deep integration with **business risk**
- Highly effective for **advanced threat modeling**
- Supports **red teaming and simulation**
- Works well with **MITRE ATT&CK**

## Weaknesses

- Complex and time-consuming
- Requires high expertise
- Heavy initial investment
- Not ideal for small teams/projects

## Common pitfalls

- Skipping business context (Stage 1)
- Treating it as theoretical (no simulation)
- Lack of threat intelligence integration
- Overcomplicating attack paths
- Not integrating results into CI/CD

## Skills Required

- Threat modeling
- Security architecture
- Cloud security (IAM, Kubernetes)
- Risk analysis
- Penetration testing
- Knowledge of MITRE ATT&CK

## When to Use PASTA

Best suited for:

- Financial systems
- Healthcare systems
- Cloud-native architectures
- High-risk applications
- Systems requiring **deep security validation**

## When NOT to Use

Avoid if:

- Small/simple applications
- Early-stage prototypes
- Low-risk systems
- Limited security maturity

## Integration with Other Frameworks

PASTA works well with:

- **NIST RMF (Risk Management Framework)** → governance
- **ISO 27001** → compliance
- **CIS Controls** → implementation
- **MITRE ATT&CK** → threat intelligence
- **OWASP** → vulnerability classification

## Strategic Value

PASTA transforms threat modeling from:

> “List possible threats”

into:

> “Simulate real attacks and measure business impact.”

## Summary

PASTA is one of the most **advanced and realistic threat modeling methodologies**, designed for:

- Modern cloud-native systems
- High-risk environments
- Security-driven organizations

It provides:

- Deep attacker perspective
- Strong business alignment
- Practical, simulation-based insights

However:

- It requires maturity, expertise, and investment

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
