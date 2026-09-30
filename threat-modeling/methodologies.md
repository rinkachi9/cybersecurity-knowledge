---
title: Threat modeling methodologies
area: threat modeling
level: unrated
status: draft
last_verified: unverified
tags: [migrated, methodologies]
migrated_from: Security.html, page 14
---

# Threat modeling methodologies

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## Introduction

Threat modeling methodologies do not exist because security engineers lack imagination.

They exist because:

- Human cognition is biased and incomplete
- Complex systems exceed individual mental capacity
- Organizations need **shared language and repeatability**
- Different stakeholders reason about risk differently

A methodology is therefore not a *truth machine*.

It is a **constraint system** that:

- Forces structured thinking
- Reduces blind spots
- Enables collaboration
- Produces artifacts others can reason about

The danger begins when the methodology is mistaken for **the result**, rather than **the thinking aid**.

### 2. The Core Failure of Most Threat Modeling Efforts

Before diving into specific methodologies, it is important to name the dominant failure mode:

> Teams select a methodology
>
> before
>
> understanding what kind of system they are modeling and
>
> what questions they need answered
>
> .

This leads to:

- Correct-looking but useless threat models
- False sense of security
- Overconfidence in coverage
- Neglect of systemic and business logic threats

The correct order is:

1. Define what kind of failure matters
2. Choose a methodology that exposes that failure
3. Accept that no single methodology is sufficient

---

### 3. STRIDE - A Failure Taxonomy, Not a Model

STRIDE is often introduced as *the* threat modeling framework.

This is a fundamental misunderstanding.

STRIDE is **not a threat model**.

It is a **classification system for types of security failure**.

#### What STRIDE Actually Is

STRIDE categorizes failures into six abstract dimensions:

- Spoofing (identity)
- Tampering (integrity)
- Repudiation (accountability)
- Information disclosure (confidentiality)
- Denial of service (availability)
- Elevation of privilege (authorization)

These categories correspond loosely to the CIA triad plus accountability and authorization.

#### What STRIDE Is Good At

STRIDE excels at:

- Ensuring coverage of classical security properties
- Structuring early-stage architectural discussions
- Helping non-security engineers reason about failure modes
- Teaching security fundamentals

It is particularly effective for:

- CRUD-style applications
- Traditional client-server systems
- Early design reviews
- Educational contexts

#### Where STRIDE Fails (Critically)

STRIDE fails when:

- Threats are emergent rather than categorical
- Business logic abuse is dominant
- Attacks rely on *sequence*, *timing*, or *economics*
- The attacker behaves “legitimately”

STRIDE cannot naturally express:

- Abuse of refund logic
- Incentive manipulation
- Multi-step trust erosion
- Supply chain compromise
- Socio-technical failures

STRIDE answers:

> “What property could fail?”

It does **not** answer:

> “How would failure realistically unfold?”

---

### 4. Attack Trees - Modeling Adversarial Intent

Attack Trees reverse the perspective.

Instead of starting with the system, they start with:

> What outcome does the attacker want?

#### The Nature of Attack Trees

An attack tree:

- Defines a malicious goal as the root
- Decomposes it into sub-goals
- Represents logical relationships (AND / OR)
- Explores alternative paths to success

Attack Trees force you to think in terms of:

- Preconditions
- Dependencies
- Substitution
- Cost and effort

This makes them powerful for:

- Understanding adversarial creativity
- Comparing attack feasibility
- Evaluating defense-in-depth

#### Where Attack Trees Shine

Attack Trees are particularly strong when:

- The attacker’s objective is clear
- You are defending high-value assets
- You need to compare alternative attack paths
- You want to reason about effort vs payoff

They are excellent for:

- Fraud scenarios
- Credential compromise
- Privilege escalation
- Targeted attacks

#### Where Attack Trees Break Down

Attack Trees struggle when:

- Failure is accidental, not adversarial
- Threats are systemic or emergent
- Human error is central
- Attack surface is highly dynamic

They also tend to:

- Over-focus on malicious intent
- Underrepresent operational complexity
- Age quickly in fast-changing systems

Attack Trees answer:

> “How could an attacker achieve this goal?”

They do **not** answer:

> “Which failures are most likely or most damaging to the business?”

---

### 5. PASTA - Risk-Driven, but Heavyweight

PASTA (Process for Attack Simulation and Threat Analysis) is often presented as “enterprise-grade threat modeling”.

This is both true - and misleading.

#### What PASTA Actually Optimizes For

PASTA is designed to:

- Integrate threat modeling with business risk
- Align security with organizational objectives
- Support formal governance and reporting
- Produce defensible artifacts for leadership

It explicitly connects:

- Business objectives
- Threat actors
- Attack scenarios
- Impact analysis

#### Strengths of PASTA

PASTA is strong where:

- Regulatory scrutiny exists
- Formal risk governance is required
- Multiple stakeholders must align
- Threat modeling informs investment decisions

It is well-suited for:

- Financial institutions
- Critical infrastructure
- Regulated industries
- Large enterprises

#### Structural Weaknesses

PASTA often fails in practice because:

- It is resource-intensive
- It requires mature organizational processes
- It assumes stable architectures
- It is slow relative to modern delivery cycles

In DevSecOps environments, PASTA frequently becomes:

- A parallel compliance activity
- Detached from real design decisions
- Too slow to influence outcomes

PASTA answers:

> “How does this threat translate into business risk?”

It often fails to answer:

> “How do engineers prevent this tomorrow?”

---

### 6. Threat Modeling as Methodology Composition

Mature organizations do **not** pick one methodology.

They compose them.

Example:

- STRIDE to ensure coverage
- Attack Trees for critical assets
- PASTA for executive risk alignment
- Ad-hoc narrative modeling for business logic

The key skill is **methodological literacy**, not loyalty.

A security engineer should be able to say:

> “This methodology will not surface the risk we care about here.”

That statement is a sign of maturity.

---

### 7. Why Methodologies Fail Against Business Logic Attacks

Business logic attacks exploit:

- Valid features
- Intended workflows
- Legitimate permissions
- Correct APIs

They break:

- Assumptions
- Incentives
- Economic models
- Sequencing logic

No classical methodology handles this well.

Effective modeling here requires:

- Domain knowledge
- Process understanding
- Economic reasoning
- Adversarial empathy

This is why business logic threats are often found:

- By fraud teams
- By product managers
- After incidents

Not by scanners or checklists.

---

### 8. Human-Centered Failure and Methodological Blind Spots

Most methodologies assume:

- Rational actors
- Correct process execution
- Stable environments

Real systems include:

- Fatigue
- Time pressure
- Cognitive overload
- Informal workarounds

Threat modeling that ignores human behavior is incomplete.

This is where **socio-technical threat modeling** becomes essential - and where formal frameworks offer little guidance.

---

### 9. Choosing the Right Lens (Not the Right Tool)

The most important question is not:

> “Which methodology should we use?”

It is:

> “What kind of failure are we trying to understand?”

- Identity confusion → STRIDE
- Targeted compromise → Attack Trees
- Executive decisions → PASTA
- Abuse and fraud → Narrative modeling
- Cloud misconfiguration → Trust boundary analysis

Methodologies are lenses - not maps.

---

### 10. Closing Perspective

Threat modeling methodologies are **scaffolding for thought**.

They:

- Reduce cognitive load
- Encourage completeness
- Enable collaboration

They do **not**:

- Replace judgment
- Eliminate uncertainty
- Guarantee security

The most dangerous threat models are:

- Perfectly formatted
- Technically correct
- Strategically irrelevant

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
