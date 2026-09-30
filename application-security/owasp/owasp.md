---
title: OWASP
area: application security
level: unrated
status: draft
last_verified: unverified
tags: [migrated, owasp]
migrated_from: Security.html, page 24
---

# OWASP

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

OWASP (Open Worldwide Application Security Project) is a **global non-profit organization** dedicated to improving **application security**.

It provides:

- Open-source security tools
- Best practices
- Standards and guidelines
- Educational resources

**Core objective:**

To help organizations **build, deploy, and maintain secure applications** by providing **practical, accessible security knowledge**.

## Importance

Modern systems are:

- API-driven
- Cloud-native
- Highly distributed

This increases:

- Attack surface
- Complexity
- Risk of vulnerabilities

OWASP addresses this by:

- Standardizing **application security practices**
- Providing **developer-friendly guidance**
- Supporting **secure SDLC (Secure Software Development Lifecycle)**

This makes it:

- Essential for **DevSecOps**
- Widely adopted across:
  - Enterprises
  - Startups
  - Security teams

## Core philosophy

OWASP is built around:

### Open Knowledge

All resources are:

- Free
- Community-driven
- Publicly available

#### Developer-Centric Security

Focus on:

> “Helping developers build secure code from the start”

#### Practical Security

OWASP emphasizes:

- Real-world vulnerabilities
- Actionable mitigations

#### Continuous Improvement

Projects are:

- Updated regularly
- Based on evolving threat landscape

## Key OWASP Projects

### OWASP Top 10

#### What it is?

A **list of the 10 most critical web application security risks**.

#### Current Categories (OWASP Top 10 - 2021)

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

#### Purpose

- Raise awareness
- Guide secure development
- Prioritize security efforts

### OWASP ASVS (Application Security Verification Standard)

#### What it is?

A **framework for validating application security controls**.

#### Levels

- Level 1 → Basic
- Level 2 → Standard
- Level 3 → High security

#### Use cases

- Security requirements
- Testing and validation
- Compliance

### OWASP SAMM (Software Assurance Maturity Model)

#### What it is?

A **framework for assessing and improving security maturity**.

#### Domains

- Governance
- Design
- Implementation
- Verification
- Operations

### OWASP Testing Guide

#### What it is?

A comprehensive guide for:

- Penetration testing
- Security testing methodologies

### OWASP Cheat Sheet Series

#### What it is?

Practical guides for:

- Secure coding
- Specific vulnerabilities

#### Examples

- Authentication Cheat Sheet
- JWT Cheat Sheet
- Input Validation Cheat Sheet

### OWASP ZAP (Zed Attack Proxy)

#### What it is?

An open-source tool for:

- Dynamic Application Security Testing (DAST)

## OWASP Model Structure

```text
Awareness (Top 10)
      ↓
Standards (ASVS)
      ↓
Maturity (SAMM)
      ↓
Testing (Testing Guide, ZAP)
      ↓
Implementation (Cheat Sheets)
```

## Practical Example

### Vulnerability: Broken Access Control

#### Scenario

- User accesses admin endpoint without authorization

#### Root Cause (CWE)

- CWE-284 (Improper Access Control)

#### Attack Pattern (CAPEC)

- Privilege escalation

#### ATT&CK Mapping

- Privilege Escalation / Initial Access

#### Mitigation (OWASP)

- Enforce RBAC
- Validate access on server side
- Use least privilege

## OWASP vs MITRE

| Aspect | OWASP | MITRE |
| --- | --- | --- |
| Focus | Application security | Threat intelligence |
| Perspective | Developer | Attacker/defender |
| Output | Best practices | Knowledge bases |

## OWASP vs CWE

| Aspect | OWASP | CWE |
| --- | --- | --- |
| Focus | Risks | Weaknesses |
| Use case | Awareness | Root cause |

## OWASP vs NIST

| Aspect | OWASP | NIST |
| --- | --- | --- |
| Type | Community project | Government framework |
| Focus | Application security | Broad security governance |

## OWASP in DevSecOps

### Design Phase

- Use:
  - OWASP Top 10
  - ASVS

#### Development

- Apply:
  - Cheat Sheets
  - Secure coding practices

#### CI/CD

- Integrate:
  - SAST
  - DAST (ZAP)
  - SCA

#### Runtime

- Monitoring
- Logging
- Incident detection

#### Example Pipeline

```text
Code → SAST → OWASP checks → DAST (ZAP) → Deploy
```

## OWASP in Cloud & Kubernetes

### Common Risks

- API misconfiguration
- IAM issues
- SSRF in cloud metadata services

#### Kubernetes Examples

- Exposed dashboards
- Weak RBAC
- Insecure container configs

#### Cloud Example (GCP)

- Misconfigured IAM
- Public storage buckets
- API abuse

OWASP helps:

- Secure APIs
- Reduce attack surface
- Implement Zero Trust principles

## Strengths

- Practical and developer-friendly
- Widely adopted
- Free and open
- Regularly updated

## Weaknesses

- Focused mainly on applications
- Not a full governance framework
- Requires integration with other standards

## Common pitfalls

- Treating OWASP Top 10 as exhaustive
- Ignoring secure design (only focusing on coding)
- Lack of automation in CI/CD
- Not training developers

## Skills Required

- Secure coding
- Application security
- DevSecOps practices
- Basic threat modeling

## When to Use OWASP

Best suited for:

- Web and API security
- Secure development
- Developer training
- Security testing

## When NOT to Use Alone

Avoid using OWASP alone for:

- Threat intelligence
- Risk governance
- Advanced detection engineering

## Integration with Other Frameworks

OWASP works best with:

- **CWE** → root causes
- **CAPEC** → attack patterns
- **MITRE ATT&CK** → attacker behavior
- **CVSS** → prioritization
- **NIST CSF** → governance

## Strategic Value

OWASP transforms development from:

> “Build first, secure later”

into:

> “Build secure by design.”

## Summary

OWASP is:

- The **most important ecosystem for application security**
- Focused on:
  - Developers
  - Secure coding
  - Practical security

It provides:

- Awareness (Top 10)
- Standards (ASVS)
- Tools (ZAP)
- Guidance (Cheat Sheets)

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
