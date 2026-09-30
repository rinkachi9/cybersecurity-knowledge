# Security Cards

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

Security Cards are a **collaborative threat modeling technique** that uses a deck of cards to help teams **identify threats, risks, and attack scenarios through guided discussion**.

They were introduced by researchers including Tamara Denning and Adam Shostack.

The method is designed to:

- Encourage **creative and adversarial thinking**
- Support **team-based threat discovery**
- Make threat modeling more **accessible and engaging**

**Core objective:**

To help teams explore **“what could go wrong?”** using structured prompts that represent attackers, assets, and attack techniques.

## Importance

Traditional threat modeling approaches (e.g., STRIDE, PASTA):

- Can be too formal or technical
- Require security expertise
- May limit creative thinking

Security Cards address this by:

- Lowering the barrier to entry
- Encouraging **diverse perspectives**
- Facilitating **interactive threat discovery**

This makes them:

- Ideal for **early-stage design**
- Useful in **cross-functional teams (dev, product, security)**
- Effective for **brainstorming and workshops**

## Core philosophy

Security Cards are built around:

### Human-Centered Security

Focus on:

- How people think about threats
- Collaborative reasoning
- Shared understanding

#### Adversarial Thinking Through Prompts

Instead of:

> “List threats”

Security Cards ask:

> “What if this attacker targets this asset using this method?”

#### Exploration Over Formality

The goal is:

- Discovery, not precision
- Breadth, not strict modeling

#### Gamification of Security

Security becomes:

- Interactive
- Engaging
- Easier to adopt across teams

## Key concepts

Security Cards typically include multiple categories:

### Attacker Cards

Define:

- Who is attacking?

Examples:

- Insider
- Script kiddie
- Organized crime
- Nation-state actor

#### Motivation Cards

Define:

- Why is the attack happening?

Examples:

- Financial gain
- Espionage
- Sabotage
- Reputation damage

#### Asset Cards

Define:

- What is being targeted?

Examples:

- User data
- API endpoints
- Infrastructure
- Credentials

#### Attack Technique Cards

Define:

- How is the attack performed?

Examples:

- Phishing
- Injection
- API abuse
- Supply chain compromise

#### Impact Cards

Define:

- What is the consequence?

Examples:

- Data breach
- Service disruption
- Financial loss
- Compliance violation

## Security Cards Model Structure

Security Cards operate as:

- A **scenario generation system**

Typical flow:

```text
Attacker + Motivation + Asset + Technique → Threat Scenario
```

## Security Cards Process

### Step 1 - Define System Context

Identify:

- Application/system scope
- Key assets
- Architecture overview

#### Step 2 - Assemble Team

Include:

- Developers
- Security engineers
- Product owners
- Architects

#### Step 3 - Draw Cards

Randomly or intentionally select:

- Attacker
- Motivation
- Asset
- Technique

#### Step 4 - Build Threat Scenarios

Example:

```text
Attacker: Insider
Motivation: Financial gain
Asset: Customer database
Technique: Data exfiltration
```

→ Scenario:

> Insider steals customer data for profit

#### Step 5 - Discuss and Analyze

Evaluate:

- Feasibility
- Impact
- Existing controls

#### Step 6 - Identify Mitigations

Define:

- Preventive controls
- Detective controls
- Response strategies

#### Step 7 - Document Findings

Convert scenarios into:

- Threat models
- Security requirements
- Backlog items

## Practical Example

**System:**

Cloud-based SaaS platform

**Cards Drawn:**

- Attacker: External attacker
- Motivation: Financial gain
- Asset: Payment API
- Technique: API abuse

**Scenario:**

- Attacker exploits API to perform fraudulent transactions

**Mitigations:**

- Rate limiting
- Fraud detection
- Strong authentication (OAuth2)
- Monitoring and alerting

## Security Cards vs STRIDE

| Aspect | Security Cards | STRIDE |
| --- | --- | --- |
| Approach | Scenario-based | Category-based |
| Structure | Flexible | Structured |
| Ease of use | High | Medium |
| Formality | Low | Medium |
| Use case | Brainstorming | Systematic analysis |

## Security Cards vs PASTA

| Aspect | Security Cards | PASTA |
| --- | --- | --- |
| Complexity | Low | High |
| Focus | Exploration | Risk & simulation |
| Output | Threat scenarios | Full threat model |
| Use case | Early stage | Advanced analysis |

## Security Cards in DevSecOps

Security Cards fit well into:

### Design Phase

- Threat modeling workshops
- Architecture brainstorming

#### Planning Phase

- Security backlog creation
- Risk identification

#### Development

- Translate scenarios into:
  - User stories
  - Security requirements

#### Example

Scenario:

```text
Phishing → Credential theft → API abuse
```

→ Actions:

- Add MFA
- Implement anomaly detection
- Improve logging

## Security Cards in Cloud Environments

Use cases:

- API security brainstorming
- IAM risk exploration
- Multi-tenant threat discovery

Example:

- Attacker: External
- Asset: Kubernetes cluster
- Technique: Misconfigured RBAC

→ Scenario:

- Privilege escalation via IAM misconfiguration

## Strengths

- Easy to use and adopt
- Encourages creativity
- Great for cross-functional teams
- Improves security awareness
- Flexible and adaptable

## Weaknesses

- Not formal or standardized
- May miss technical depth
- Depends on participant expertise
- No built-in prioritization

## Common pitfalls

- Treating it as a game only (no follow-up)
- Lack of documentation
- Ignoring real threat intelligence
- Not translating scenarios into actions

## Skills Required

- Basic security awareness
- System understanding
- Ability to think adversarially
- Facilitation skills

## When to Use Security Cards

Best suited for:

- Early design phases
- Brainstorming sessions
- Teams new to threat modeling
- Product and UX discussions

## When NOT to Use

Avoid as the only method when:

- High-risk systems
- Regulatory environments
- Deep technical analysis required

## Integration with Other Frameworks

Security Cards work well with:

- **STRIDE** → structure threats
- **PASTA** → simulate attacks
- **MITRE ATT&CK** → map techniques
- **CVSS** → prioritize vulnerabilities
- **NIST RMF** → risk governance

## Strategic Value

Security Cards transform threat modeling from:

> “Formal security exercise”

into:

> “Collaborative exploration of real-world threats.”

## Summary

Security Cards are:

- A **human-centric, collaborative threat modeling technique**
- Ideal for **early-stage exploration and brainstorming**
- Highly effective for **engaging non-security stakeholders**

They provide:

- Creativity
- Accessibility
- Broad threat discovery

However:

- They should be complemented with:
  - STRIDE (structure)
  - PASTA (depth)
  - Risk frameworks (prioritization)

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
