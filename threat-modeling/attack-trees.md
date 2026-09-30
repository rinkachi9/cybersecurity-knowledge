---
title: Attack Trees
area: threat modeling
level: unrated
status: draft
last_verified: unverified
tags: [migrated, attack-trees]
migrated_from: Security.html, page 16
---

# Attack Trees

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

Attack Trees are a **structured threat modeling technique** used to represent how an attacker can achieve a specific malicious goal.

They were formalized by Bruce Schneier.

An attack tree models:

- A **root goal (attacker objective)**
- Multiple **paths to achieve that goal**
- Logical relationships between attack steps

**Core objective:**

To systematically analyze **all possible ways an attacker can compromise a system**, enabling prioritization of defenses.

## Importance

Without structured modeling of attack paths:

- Security analysis becomes fragmented
- Complex attack chains are overlooked
- Defense strategies are reactive

Attack Trees provide:

- A **visual and logical representation of attacks**
- Insight into **multi-step attack scenarios**
- Support for **risk-based decision-making**

This makes them:

- Highly valuable for **complex systems (cloud, microservices)**
- Useful for **security architecture and red teaming**
- Complementary to methodologies like STRIDE and PASTA

## Core philosophy

Attack Trees are built around:

### Goal-Oriented Security

Start from:

> “What is the attacker trying to achieve?”

Instead of:

> “What vulnerabilities exist?”

#### Decomposition of Attacks

Break down complex attacks into:

- Smaller, manageable steps
- Logical combinations of actions

#### Logical Relationships

Attack steps are connected via:

- **AND nodes** → all conditions must be met
- **OR nodes** → any condition is sufficient

#### Adversarial Thinking

Focus on:

- Realistic attacker behavior
- Creative exploitation paths

## Key concepts

### Root Node (Goal)

The main attacker objective.

Examples:

- Steal sensitive data
- Gain admin access
- Disrupt service

#### Child Nodes (Sub-goals)

Steps required to achieve the goal.

#### Leaf Nodes

Atomic actions:

- Exploit vulnerability
- Phish user
- Brute-force password

#### AND Nodes

All child nodes must be satisfied.

Example:

```diff
Access database:
AND
- Obtain credentials
- Access network
```

#### OR Nodes

Any child node is sufficient.

Example:

```diff
Obtain credentials:
OR
- Phishing
- Credential stuffing
- Keylogging
```

#### Attack Paths

A full path from:

- Root → Leaf nodes

Represents a **complete attack scenario**.

#### Attributes (Optional)

Each node can include:

- Cost
- Time
- Skill required
- Likelihood
- Detectability

## Attack Tree Structure

Basic structure:

```text
Root Goal
 ├── OR: Path A
 │    ├── Step 1
 │    └── Step 2
 └── OR: Path B
      ├── AND:
      │    ├── Step 1
      │    └── Step 2
```

## Attack Tree Process

### Step 1 - Define Attacker Goal

Examples:

- “Exfiltrate customer data”
- “Gain admin access”

#### Step 2 - Identify High-Level Attack Strategies

Break goal into:

- Major attack paths

#### Step 3 - Decompose into Sub-steps

Expand each path into:

- Detailed steps
- Exploits
- Preconditions

#### Step 4 - Define Logical Relationships

Assign:

- AND / OR relationships

#### Step 5 - Add Attributes (Optional)

Quantify:

- Risk
- Cost
- Likelihood

#### Step 6 - Analyze Attack Paths

Identify:

- Most likely paths
- Most impactful paths
- Weakest points

#### Step 7 - Define Mitigations

For each path:

- Break the chain
- Add controls

## Practical Example

**System:**

Cloud-based application (Kubernetes + API)

**Goal (Root):**

Steal customer data

**Attack Tree:**

```text
Steal customer data
 ├── OR: Exploit API
 │    ├── Bypass authentication
 │    ├── Access sensitive endpoint
 │
 ├── OR: Compromise credentials
 │    ├── Phishing
 │    ├── Credential stuffing
 │
 └── OR: Exploit infrastructure
      ├── Misconfigured IAM
      ├── Container escape
```

**Mitigations:**

- Strong authentication (OIDC, MFA)
- API Gateway + rate limiting
- IAM least privilege
- Runtime security monitoring

## Attack Trees vs STRIDE

| Aspect | Attack Trees | STRIDE |
| --- | --- | --- |
| Focus | Attack paths | Threat categories |
| Approach | Goal-oriented | Systematic classification |
| Visualization | Strong | Limited |
| Complexity | Medium - High | Low - Medium |
| Use case | Deep analysis | Initial threat identification |

## Attack Trees vs PASTA

| Aspect | Attack Trees | PASTA |
| --- | --- | --- |
| Scope | Modeling technique | Full methodology |
| Simulation | Conceptual | Practical simulation |
| Business context | Optional | Strong |
| Use case | Attack path analysis | End-to-end threat modeling |

## Attack Trees in DevSecOps

Attack Trees integrate into:

### Design Phase

- Architecture threat modeling
- Identifying attack surfaces

#### CI/CD

- Security test case generation
- Threat-based testing

#### Runtime

- Detection rules based on attack paths
- SIEM correlation

**Example:**

Attack path:

```text
Phishing → Credential theft → API access
```

→ Create:

- Detection rules
- Alerts
- Automated response

## Attack Trees in Cloud Environments

Use cases:

- Kubernetes attack paths
- IAM privilege escalation
- API abuse scenarios

Example:

```javascript
Gain cluster admin:
 ├── Exploit misconfigured RBAC
 ├── Use compromised service account
 ├── Exploit container escape
```

Helps:

- Identify lateral movement
- Strengthen Zero Trust architecture
- Secure multi-tenant systems

## Strengths

- Clear visualization of attacks
- Supports complex attack scenarios
- Encourages adversarial thinking
- Flexible and extensible
- Works well with risk analysis

## Weaknesses

- Can become very complex
- Requires expertise
- Not standardized like STRIDE
- May lack business context if not extended

## Common pitfalls

- Overcomplicating trees
- Missing attack paths
- Not updating with system changes
- Ignoring real-world threat intelligence

## Skills required

- Threat modeling
- Security architecture
- Knowledge of attack techniques (MITRE ATT&CK)
- Analytical thinking

## When to Use Attack Trees

Best suited for:

- Complex systems
- High-risk environments
- Security architecture design
- Red teaming and simulations

## When NOT to Use

Avoid if:

- Small/simple applications
- Early prototyping
- Limited resources

## Integration with Other Frameworks

Attack Trees work well with:

- **STRIDE** → identify threats
- **PASTA** → simulate attacks
- **MITRE ATT&CK** → map techniques
- **CVSS** → prioritize vulnerabilities
- **NIST RMF** → risk governance

## Strategic Value

Attack Trees transform security analysis from:

> “List threats”

into:

> “Understand how attacks actually happen step by step.”

## Summary

Attack Trees are:

- A powerful technique for modeling **real attack paths**
- Essential for understanding **multi-step compromises**
- Highly valuable in **modern cloud and DevSecOps environments**

They provide:

- Clear visualization
- Deep attacker perspective
- Strong support for defensive design

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
