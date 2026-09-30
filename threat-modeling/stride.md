---
title: STRIDE
area: threat modeling
level: unrated
status: draft
last_verified: unverified
tags: [migrated, stride]
migrated_from: Security.html, page 15
---

# STRIDE

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

STRIDE is a **threat classification framework** developed by Microsoft to systematically identify security threats in software systems.

STRIDE is an acronym representing six categories of threats:

- **S** - Spoofing
- **T** - Tampering
- **R** - Repudiation
- **I** - Information Disclosure
- **D** - Denial of Service
- **E** - Elevation of Privilege

**Core objective:**

To identify potential security threats by analyzing how a system can be attacked across these six categories.

## Importance

Without structured threat modeling:

- Security analysis is inconsistent
- Critical threats may be overlooked
- Teams rely on intuition instead of methodology

STRIDE provides:

- A **systematic approach** to threat identification
- A **shared language** for developers and security teams
- A foundation for **secure design decisions**

This makes it:

- Ideal for **early-stage threat modeling**
- Widely used in **Secure SDLC**
- Accessible for both **developers and security engineers**

## Core philosophy

STRIDE is built around:

### Threat-Centric Modeling

Instead of starting from risk or business impact, STRIDE focuses on:

> “What types of threats can affect this system?”

#### Systematic Enumeration

Every component is analyzed against:

- All six STRIDE categories
- Ensuring **complete coverage**

#### Simplicity and Accessibility

STRIDE is:

- Easy to understand
- Quick to apply
- Suitable for iterative development

## Key concepts

### System Components

Analyzed elements include:

- Processes (services, microservices)
- Data stores (databases, storage)
- Data flows (API calls, messaging)
- External entities (users, systems)

#### Trust Boundaries

Critical concept:

- Points where **trust level changes**
- Example:
  - Internet → API Gateway
  - Service → Database

Threats are most likely at:

- Boundaries
- Interfaces

#### Data Flow Diagrams (DFD)

STRIDE is typically applied on:

- Data Flow Diagrams

These define:

- Components
- Interactions
- Trust boundaries

#### Threat Mapping

Each STRIDE category maps to specific system elements:

| Element | STRIDE Threats |
| --- | --- |
| External Entity | Spoofing, Repudiation |
| Process | All |
| Data Store | Tampering, Repudiation, Info Disclosure |
| Data Flow | Tampering, Info Disclosure, DoS |

## STRIDE Categories

### Spoofing (Identity)

**Definition:**

Impersonating another user, system, or service.

**Examples:**

- Stolen credentials
- Forged JWT tokens
- API key abuse

**Mitigations:**

- Strong authentication (OAuth2, OpenID Connect via Keycloak)
- Multi-Factor Authentication (MFA)
- Certificate-based authentication (mTLS)

#### Tampering (Integrity)

**Definition:**

Unauthorized modification of data or code.

**Examples:**

- Modifying API requests
- Changing database records
- Manipulating CI/CD artifacts

**Mitigations:**

- Data integrity checks (hashing, HMAC)
- Code signing
- Immutable infrastructure

#### Repudiation (Non-repudiation)

**Definition:**

Ability to deny performing an action.

**Examples:**

- User denies transaction
- Lack of audit logs

**Mitigations:**

- Audit logging
- Secure logging pipelines (e.g., Elastic Stack)
- Digital signatures

#### Information Disclosure (Confidentiality)

**Definition:**

Exposure of sensitive data.

**Examples:**

- Data leaks via APIs
- Misconfigured cloud storage
- Secrets in logs

**Mitigations:**

- Encryption (TLS, at-rest encryption)
- Secrets management (e.g., HashiCorp Vault)
- Least privilege access

#### Denial of Service (Availability)

**Definition:**

Making a system unavailable.

**Examples:**

- API flooding
- Resource exhaustion in Kubernetes
- Dependency abuse

**Mitigations:**

- Rate limiting
- Autoscaling
- WAF (Web Application Firewall)

#### Elevation of Privilege (Authorization)

**Definition:**

Gaining higher access than permitted.

**Examples:**

- Exploiting IAM misconfigurations
- Breaking RBAC
- Container escape

**Mitigations:**

- Role-Based Access Control (RBAC)
- Zero Trust architecture
- Privilege minimization

## STRIDE Model Structure

STRIDE is applied as:

- A **matrix of components vs threat categories**

For each system element:

- Evaluate all six threat types

### STRIDE Process

#### Step 1 - Define System Scope

Identify:

- Application boundaries
- Components
- External dependencies

#### Step 2 - Create Data Flow Diagram (DFD)

Model:

- Processes
- Data flows
- Data stores
- Trust boundaries

#### Step 3 - Identify Threats Using STRIDE

For each component:

- Apply all STRIDE categories

Example:

```diff
API Service:
- Spoofing → fake tokens
- Tampering → request manipulation
- Repudiation → missing logs
- Info Disclosure → data leak
- DoS → overload
- EoP → privilege escalation
```

#### Step 4 - Document Threats

Include:

- Description
- Impact
- Likelihood

#### Step 5 - Define Mitigations

Map threats to:

- Security controls
- Best practices

#### Step 6 - Validate and Iterate

- Review with stakeholders
- Update with architecture changes

## STRIDE vs PASTA

| Aspect | STRIDE | PASTA |
| --- | --- | --- |
| Approach | Threat-based | Risk + attack simulation |
| Complexity | Low - Medium | High |
| Business context | Limited | Strong |
| Simulation | No | Yes |
| Use case | Early design | Advanced modeling |

## STRIDE vs Trike

| Aspect | STRIDE | Trike |
| --- | --- | --- |
| Focus | Threat identification | Risk definition |
| Approach | Category-based | Requirement-based |
| Complexity | Low | High |
| Output | Threat list | Risk model |

## Practical Example

**System:**

Microservices-based API (Kubernetes, GKE)

**Component:**

Authentication Service

**STRIDE Analysis:**

- Spoofing → fake tokens
- Tampering → token manipulation
- Repudiation → lack of login logs
- Info Disclosure → leaking user data
- DoS → login endpoint flooding
- EoP → privilege escalation via token misuse

**Mitigations:**

- OAuth2 + OIDC (Keycloak)
- JWT validation
- Rate limiting
- Audit logging
- RBAC policies

## STRIDE in DevSecOps

STRIDE integrates well into:

### Design Phase

- Threat modeling workshops
- Architecture reviews

#### Development Phase

- Secure coding practices
- Code reviews

#### CI/CD

- SAST, DAST
- IaC scanning

#### Runtime

- Monitoring (Prometheus, Grafana)
- Logging (Elastic Stack)
- Detection (SIEM)

## STRIDE in Cloud Environments

Use cases:

- API security modeling
- IAM threat analysis
- Kubernetes threat modeling

Example threats:

- Spoofing → compromised service account
- EoP → overly permissive IAM role
- Info Disclosure → public S3/GCS bucket

STRIDE helps:

- Identify misconfigurations
- Improve Zero Trust posture
- Secure service-to-service communication

## Strengths

- Simple and easy to use
- Widely adopted
- Good for early-stage modeling
- Developer-friendly

## Weaknesses

- No built-in risk prioritization
- No attack simulation
- Can generate large threat lists
- Limited business alignment

## Common pitfalls

- Treating it as a checklist only
- Ignoring trust boundaries
- Not updating models over time
- Lack of integration with CI/CD

## Skills Required

- Basic security knowledge
- System architecture understanding
- Knowledge of common vulnerabilities (OWASP Top 10)

## When to Use STRIDE

Best suited for:

- Early-stage design
- Agile development
- Microservices and APIs
- Teams starting with threat modeling

## When NOT to Use

Avoid as the only method when:

- High-risk systems
- Regulatory environments
- Advanced threat scenarios

(Use with PASTA or Trike instead)

## Integration with Other Frameworks

STRIDE works well with:

- **OWASP Top 10** → vulnerability mapping
- **MITRE ATT&CK** → attacker techniques
- **NIST RMF** → risk governance
- **ISO 27001** → compliance
- **PASTA** → deeper analysis

## Strategic Value

STRIDE transforms threat modeling from:

> “Ad hoc thinking”

into:

> “Structured, repeatable threat identification.”

## Summary

STRIDE is:

- One of the most **widely used threat modeling methodologies**
- Simple yet effective for identifying threats
- Ideal as a **starting point for security analysis**

However:

- It should be complemented with **risk-based (Trike)** or **simulation-based (PASTA)** approaches for advanced security maturity.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
