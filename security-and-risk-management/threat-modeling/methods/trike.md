# Trike

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Trike** is a **risk-based threat modeling methodology** designed to:

- Define **acceptable risk levels explicitly**
- Model threats based on **stakeholder-defined risk requirements**
- Create a **formal, structured approach to security design**

> Core objective:
>
> Ensure that system security is aligned with
>
> explicit risk tolerance
>
> , rather than implicit assumptions.

## Importance

Traditional threat modeling approaches (e.g., STRIDE):

- Focus on **identifying threats**
- Often lack **quantitative risk alignment**
- Can be subjective

Trike addresses this gap by:

> Starting from risk requirements, not threats.

This makes it:

- More **governance-aligned**
- More **auditable**
- Better suited for **high-assurance systems**

## Core philosophy

Trike is built around:

### Risk-Driven Security

Security is defined by:

- What level of risk is acceptable
- Who defines that risk (stakeholders)

#### Formal Modeling

Uses:

- Matrices
- Roles
- Permissions
- Actions

#### Requirement-Centric Approach

Instead of:

> “What can go wrong?”

Trike asks:

> “What level of risk is acceptable, and what violates it?”

## Key concepts

### Assets

Anything of value:

- Data
- Systems
- Services
- Infrastructure

#### Actors

Entities interacting with the system:

- Users
- Services
- Attackers (modeled as actors)

#### Actions

What actors can do:

- Read
- Write
- Execute
- Modify

#### Risk

Defined as:

```text
Risk = Probability × Impact
```

But in Trike:

- Risk is **predefined and constrained**
- Acceptable thresholds are defined first

#### Requirements Model

Defines:

- Acceptable risk per actor-action-asset combination

This is the **core innovation of Trike**.

## Trike Model Structure

Trike uses a **matrix-based model**:

| Actor | Asset | Action | Allowed Risk |
| --- | --- | --- | --- |
| User | Database | Read | Low |
| Admin | Server | Modify | Medium |

This defines:

- What is acceptable
- What is a violation

## Trike Process

### Step 1 - Define Actors

Identify all entities:

- Internal users
- External users
- Services
- Potential attackers

#### Step 2 - Define Assets

Identify:

- Sensitive data
- Critical services
- Infrastructure components

#### Step 3 - Define Actions

Determine:

- Possible operations on assets

#### Step 4 - Define Risk Requirements

This is critical:

- Assign acceptable risk levels
- Based on business context

#### Step 5 - Build Requirements Matrix

Combine:

- Actors
- Assets
- Actions
- Risk levels

#### Step 6 - Identify Threats

Threat =

Any action that **exceeds acceptable risk**

#### Step 7 - Define Mitigations

Implement controls to:

- Reduce risk
- Enforce acceptable boundaries

## Trike vs STRIDE

| Aspect | STRIDE | Trike |
| --- | --- | --- |
| Approach | Threat-first | Risk-first |
| Focus | Attack types | Risk thresholds |
| Output | Threat list | Risk-based model |
| Use | Design analysis | Governance + design |

## Trike vs Risk Management Framework (RMF)

| Aspect | RMF | Trike |
| --- | --- | --- |
| Scope | Organizational | System-level |
| Focus | Risk lifecycle | Threat modeling |
| Output | Risk decisions | Threat + requirements model |

## Practical Example

### System:

API for financial transactions

#### Actors:

- User
- Admin
- External attacker

#### Asset:

- Transaction database

#### Action:

- Modify transaction

#### Risk Requirement:

- Only admin → low risk acceptable
- Others → zero tolerance

#### Threat:

- Unauthorized modification by user

#### Mitigation:

- RBAC
- Strong authentication
- Audit logging

## Trike in DevSecOps

Trike fits well with:

- Threat modeling in design phase
- Security requirements definition
- Policy-as-code

Example:

- Define acceptable risk → enforce via CI/CD

## Trike in Cloud Environments

Use cases:

- IAM design
- API security
- Multi-tenant systems

Trike helps:

- Define access boundaries
- Prevent privilege escalation

## Strengths

- Strong alignment with risk management
- Formal and structured
- Auditable
- Good for regulated environments

## Weaknesses

- Complex to implement
- Requires strong risk definition
- Less intuitive than STRIDE
- Not widely adopted

## Common pitfalls

- Poorly defined risk thresholds
- Overcomplicated models
- Lack of stakeholder involvement
- Ignoring dynamic threats

## Skills Required

- Risk analysis
- System modeling
- IAM understanding
- Security architecture
- Threat modeling techniques

## When to Use Trike

Best suited for:

- High-security systems
- Financial systems
- Regulated industries
- Systems requiring auditability

## When NOT to Use

Avoid if:

- Rapid prototyping
- Small projects
- Low-risk environments

## Integration with Other Frameworks

Trike works well with:

- RMF → risk governance
- ISO 27001 → compliance
- CIS Controls → implementation
- STRIDE → complementary threat identification

## Strategic Value

Trike transforms threat modeling from:

> “List possible attacks”
>
> into
>
> “Enforce acceptable risk boundaries.”

## Summary

Trike is one of the **most rigorous and formal threat modeling methodologies**, but also one of the least used due to its complexity.

For advanced security professionals, it provides:

- Deep understanding of risk
- Structured threat modeling
- Strong alignment with governance

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
