---
title: Center for Internet Security (CIS) Controls Framework
area: governance and compliance
level: unrated
status: draft
last_verified: unverified
tags: [migrated, cis, controls]
migrated_from: Security.html, page 42
---

# Center for Internet Security (CIS) Controls Framework

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

The **CIS Controls Framework** (formerly *CIS Critical Security Controls*) is a **prioritized set of cybersecurity best practices** developed by the **Center for Internet Security**.

> Core objective:
>
> Provide a
>
> practical, actionable, and prioritized roadmap
>
> for defending against the most common and impactful cyber threats.

Unlike theoretical frameworks:

- CIS Controls are **operational and implementation-focused**
- Designed for **real-world defense against known attack patterns**

## Importance

Organizations struggle with:

- Too many security controls (ISO, NIST → complexity)
- Lack of prioritization
- Misalignment with real threats

CIS Controls were created based on:

- Analysis of **real-world cyber attacks**
- Alignment with **MITRE ATT&CK**
- Practical defensive strategies

> CIS answers:
>
> “What should we implement first to reduce risk quickly?”

## Evolution of CIS Controls

- Originally developed by SANS → *Critical Security Controls*
- Maintained and expanded by CIS
- Current version: **CIS Controls v8**

Key updates in v8:

- Focus on **modern environments (cloud, SaaS, remote work)**
- Simplified structure
- Better mapping to frameworks

## Core structure

The framework consists of:

- **18 Controls**
- **153 Safeguards (sub-controls)**

```text
Control → Safeguard → Implementation Guidance
```

## The 18 CIS Controls

---

### Inventory and Control of Enterprise Assets

- Identify and manage all hardware
- Prevent unauthorized devices

#### Inventory and Control of Software Assets

- Track installed software
- Prevent unauthorized applications

#### Data Protection

- Data classification
- Encryption
- Data handling policies

#### Secure Configuration of Enterprise Assets and Software

- Hardening baselines
- Configuration management

#### Account Management

- Identity lifecycle management
- Privileged account control

#### Access Control Management

- Authentication mechanisms
- Authorization enforcement

#### Continuous Vulnerability Management

- Vulnerability scanning
- Patch management

#### Audit Log Management

- Centralized logging
- Log protection

#### Email and Web Browser Protections

- Phishing defense
- Browser security controls

#### Malware Defenses

- Endpoint protection
- Detection mechanisms

#### Data Recovery

- Backup strategies
- Recovery testing

#### Network Infrastructure Management

- Secure network devices
- Segmentation

#### Network Monitoring and Defense

- IDS/IPS
- Traffic analysis

#### Security Awareness and Skills Training

- User education
- Social engineering defense

#### Service Provider Management

- Vendor risk management
- Third-party controls

#### Application Software Security

- Secure SDLC
- Code security practices

#### Incident Response Management

- Incident handling procedures
- Response playbooks

#### Penetration Testing

- Red teaming
- Continuous validation

## Implementation Groups (IG)

CIS Controls introduce **Implementation Groups** to match maturity and risk level.

### IG1 - Basic Cyber Hygiene

- Small organizations
- Minimal resources
- Focus: essential protections

#### IG2 - Intermediate

- Medium organizations
- Moderate risk exposure
- More structured controls

#### IG3 - Advanced

- Large enterprises
- High-value targets
- Advanced threat defense

## CIS Controls and Threat Mapping

CIS Controls align with:

- MITRE ATT&CK techniques
- Known attacker behaviors

Example:

- Credential access → IAM controls
- Lateral movement → network segmentation
- Persistence → logging and monitoring

## CIS Controls vs Other Frameworks

| Framework | Focus |
| --- | --- |
| NIST CSF | Risk outcomes |
| RMF | Risk process |
| ISO 27001 | Compliance |
| CSA CCM | Cloud controls |
| **CIS Controls** | **Operational defense** |

## CIS Controls in DevSecOps

CIS Controls are highly applicable to DevSecOps:

**Examples:**

- CI/CD pipeline security → Control 16
- IaC validation → Control 4
- Secrets management → Control 5/6
- Container security → Control 10/12

### CIS Benchmarks

CIS also provides:

#### CIS Benchmarks

- Hardening guidelines for:
  - OS
  - Cloud platforms (AWS, Azure, GCP)
  - Kubernetes
  - Databases

#### CIS Hardened Images

- Pre-secured cloud images

## Practical Implementation Approach

### Step 1 - Asset Visibility

- Implement inventory systems

#### Step 2 - Secure Baselines

- Apply CIS Benchmarks

#### Step 3 - Access Control

- Enforce IAM policies

#### Step 4 - Monitoring

- Central logging + SIEM

#### Step 5 - Continuous Improvement

- Vulnerability scanning
- Pen testing

## Mapping to Cloud Environments

CIS Controls apply to:

- AWS
- Azure
- GCP

Examples:

- IAM → least privilege roles
- Logging → CloudTrail / Cloud Logging
- Network → VPC segmentation

## Common pitfalls

- Treating controls as checklist
- Ignoring automation
- Lack of asset inventory
- Weak IAM implementation
- No continuous monitoring

## Skills Required for CIS Mastery

- Networking fundamentals
- System administration
- Cloud security
- DevSecOps practices
- Threat detection and response
- Risk management

## Strategic Value of CIS Controls

CIS Controls provide:

- Quick risk reduction
- Practical implementation path
- Alignment with real threats
- Standardized security baseline

## Real-World Use Cases

- Security baseline for startups
- Enterprise security programs
- Cloud migration hardening
- Compliance preparation
- DevSecOps pipeline security

## Maturity Model

### Level 1 - Basic

- IG1 controls implemented

#### Level 2 - Managed

- IG2 controls

#### Level 3 - Advanced

- IG3 + automation

#### Level 4 - Optimized

- Continuous monitoring

## CIS Controls in the Security Ecosystem

If:

- **NIST CSF** defines *what to achieve*
- **RMF** defines *how to manage risk*
- **CSA CCM** defines *cloud controls*

Then:

> CIS Controls define what to implement first to stop real attacks.

## Summary

The CIS Controls Framework is one of the **most practical cybersecurity frameworks available**.

It is:

- Actionable
- Prioritized
- Threat-informed
- Widely adopted

For cybersecurity professionals, mastering CIS Controls is critical because:

- It directly maps to attacker behavior
- It provides immediate defensive value
- It bridges theory and implementation

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
