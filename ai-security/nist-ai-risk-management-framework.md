# NIST AI Risk Management Framework (AI RMF)

## Summary

The NIST AI Risk Management Framework (AI RMF 1.0, January 2023) is a voluntary framework for managing the risks that AI systems pose to people, organizations and society. It organizes the work in four functions: Govern (build a risk management culture and structures), Map (understand the context and identify risks), Measure (assess, analyze and track the risks) and Manage (prioritize and act on them). It borrows the shape of the NIST Cybersecurity Framework, but its subject is broader than security: it asks whether an AI system is valid and reliable, safe, secure and resilient, accountable and transparent, explainable, privacy-enhanced and fair. Security is one characteristic of a trustworthy AI system, and a necessary one.

Checked against NIST AI 100-1 (AI RMF 1.0, January 2023), 2026-10. The generative AI profile (NIST AI 600-1, July 2024) is described from secondary sources and was not read.

## Prerequisites

- [NIST CSF 2.0](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md): the structure (functions, categories, subcategories, profiles) that the AI RMF reuses.
- [NIST frameworks overview](../governance-and-compliance/frameworks/nist-frameworks-overview.md).
- [Information risk management](../governance-and-compliance/risk-management/information-risk-management.md): risk as likelihood and impact.
- [Google's Secure AI Framework](google-secure-ai-framework.md) for a security-focused vendor view of AI systems.

## Core concepts

### Definition

NIST AI 100-1 defines **risk** for the framework as the composite measure of an event's probability of occurring and the magnitude or degree of its consequences. The consequences of AI systems can be positive, negative or both, so risk can include opportunities as well as threats. For negative impact, risk is a function of the magnitude of harm and the likelihood of occurrence. Harm can be experienced by individuals, groups, communities, organizations, society, the environment and the planet. The AI RMF helps to minimize anticipated negative impacts and also to identify opportunities to maximize positive ones.

The framework is intended for **AI actors**, the parties involved across the stages of the AI system life cycle (the document describes representative actors and their tasks in Figures 2 and 3 and in Appendix A). It is voluntary, rights-preserving, non-sector-specific and use-case agnostic, and it is called a "living document" that NIST expects to update. A companion online resource, the AI RMF Playbook, gives suggested tactical actions.

### Why a separate framework for AI

NIST states that AI risks differ from traditional software risks, with a dedicated appendix on the differences. Examples it points to include difficulty of measurement, risks from third-party data and models, and the socio-technical nature of AI systems: behavior depends on training data, human use and context, not only on code. Humans may also assume AI systems work well in all settings, which adds risk. The measurement challenge is also stated openly: failing to measure a risk does not mean the risk is low or high.

### Analogy

Think of a drug approval and monitoring system. Before a drug is released, someone decides which problem it addresses and who might be harmed (map), tests it with defined methods and tracks side effects (measure), decides on dosing, warnings and withdrawal (manage), and the whole system runs inside a regulator and a hospital culture that takes safety seriously (govern).

The analogy breaks in one place. A drug is a fixed molecule tested on defined populations. An AI system's behavior changes with data, prompts, updates and the way people use it, so measurement must continue after deployment.

### Trustworthy AI: seven characteristics

![Characteristics of trustworthy AI systems: Safe, Secure and Resilient, Explainable and Interpretable, Privacy-Enhanced, Fair with Harmful Bias Managed, all resting on Valid and Reliable, with Accountable and Transparent as a vertical box. Source: NIST AI 100-1, Fig. 4.](../_assets/ai-security/nist-ai-rmf-trustworthy-characteristics.png)

NIST names the characteristics: **valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed**. In the figure, valid and reliable is a necessary condition and the base for the others, and accountable and transparent relates to all the others. NIST adds that:

- addressing the characteristics individually does not make a system trustworthy;
- trade-offs are usual (for example between interpretability and privacy, or between predictive accuracy and interpretability);
- rarely do all characteristics apply in every setting;
- trustworthiness is a social concept, and a system is only as strong as its weakest characteristic;
- human judgment is needed to choose metrics and threshold values.

"Secure and resilient" is the part that overlaps with this repository's scope. It connects to the [CIA triad](../foundations/cia-triad/README.md): the attacks that violate confidentiality, integrity and availability of models, training data and outputs.

### The Core

![The AI RMF Core: Govern in the centre, with Map (context is recognized and risks related to context are identified), Measure (identified risks are assessed, analyzed or tracked) and Manage (risks are prioritized and acted upon based on a projected impact) around it. Source: NIST AI 100-1, Fig. 5.](../_assets/ai-security/nist-ai-rmf-core-functions.png)

The Core has four functions and, in total, 19 categories (6 Govern, 5 Map, 4 Measure, 4 Manage), each divided into subcategories. The count of categories was derived from the document's tables. NIST states that actions do not constitute a checklist or an ordered set of steps. Govern is cross-cutting and "infused throughout" the other three. After instituting Govern outcomes, most users would start with Map and continue to Measure or Manage, but the process should be iterative.

#### Govern

Govern cultivates and implements a culture of risk management, outlines the processes, documents and organizational structures that anticipate, identify and manage risk, incorporates processes to assess potential impacts, aligns risk management with organizational principles and strategy, and covers the full product life cycle including third-party software, hardware and data.

| Category | Meaning (paraphrased) | Examples |
| --- | --- | --- |
| GOVERN 1 | Policies, processes, procedures and practices for mapping, measuring and managing AI risk are in place, transparent and implemented | GOVERN 1.1 legal and regulatory requirements are understood, 1.2 trustworthy AI characteristics are built into policies, 1.6 mechanisms to inventory AI systems, 1.7 decommissioning |
| GOVERN 2 | Accountability structures with empowered, responsible and trained teams | GOVERN 2.3 executive leadership takes responsibility for decisions about AI risk |
| GOVERN 3 | Workforce diversity, equity, inclusion and accessibility are prioritized in mapping, measuring and managing | GOVERN 3.2 roles for human-AI configurations and oversight |
| GOVERN 4 | A culture that considers and communicates AI risk | GOVERN 4.3 practices that enable AI testing, incident identification and information sharing |
| GOVERN 5 | Engagement processes with relevant AI actors | GOVERN 5.1 collect and integrate feedback from those external to the team |
| GOVERN 6 | Policies address risks and benefits from third-party software and data | GOVERN 6.1 third-party and intellectual property risks, 6.2 contingency processes for third-party failures or incidents |

#### Map

Map establishes the context. NIST says outcomes of Map are the basis for Measure and Manage, and that without contextual knowledge risk management is difficult.

| Category | Meaning (paraphrased) | Examples |
| --- | --- | --- |
| MAP 1 | Context is established and understood | MAP 1.1 intended purposes, beneficial uses, laws, norms, settings and users are understood and documented |
| MAP 2 | The AI system is categorized | MAP 2.1 the tasks it supports (classifier, generative model, recommender), 2.2 knowledge limits and human oversight |
| MAP 3 | Capabilities, usage, goals, benefits and costs are understood | MAP 3.1 benefits, 3.2 costs including non-monetary costs of errors |
| MAP 4 | Risks and benefits are mapped for all components including third-party software and data | MAP 4.1 mapping approaches for technology and legal risk, 4.2 internal risk controls for components |
| MAP 5 | Impacts to individuals, groups, communities, organizations and society are characterized | MAP 5.1 likelihood and magnitude of each identified impact |

#### Measure

| Category | Meaning (paraphrased) | Examples |
| --- | --- | --- |
| MEASURE 1 | Appropriate methods and metrics are identified and applied | MEASURE 1.1 risks from Map are selected for measurement, and those that cannot be measured are documented |
| MEASURE 2 | The system is evaluated for the trustworthy characteristics | MEASURE 2.1 test sets, metrics and tools used in test, evaluation, verification and validation (TEVV) are documented |
| MEASURE 3 | Mechanisms for tracking identified risks over time are in place | MEASURE 3.1 regularly identify and track existing, unanticipated and emergent risks |
| MEASURE 4 | Feedback about the efficacy of measurement is gathered and assessed | MEASURE 4.1 measurement approaches are connected to deployment context and informed by domain experts and end users |

#### Manage

| Category | Meaning (paraphrased) | Examples |
| --- | --- | --- |
| MANAGE 1 | Risks from assessments are prioritized, responded to and managed | MANAGE 1.1 decide whether the system achieves its purpose and whether development or deployment should proceed, 1.2 treat risks by impact, likelihood and resources |
| MANAGE 2 | Strategies to maximize benefits and minimize negative impacts are planned and documented | MANAGE 2.1 resources are considered along with viable non-AI alternatives |
| MANAGE 3 | Risks and benefits from third-party entities are managed | MANAGE 3.2 pre-trained models used for development are monitored as part of regular monitoring |
| MANAGE 4 | Risk treatments, including response and recovery, and communication plans are documented and monitored | MANAGE 4.1 post-deployment monitoring plans with user input, appeal and override, decommissioning, incident response, recovery and change management |

Note MANAGE 1.1: the framework explicitly allows the conclusion that development or deployment should not proceed. A risk management process with no "stop" option is not a risk decision.

### Profiles

The AI RMF provides for **profiles** that adapt the Core to a use case, sector or situation, in the same sense as CSF profiles. A generative AI profile, **NIST AI 600-1** (July 2024 according to secondary sources), applies the Core to generative AI risks. I did not read it, so the risks it lists are not summarized here.

### Relationship to other frameworks

| Framework | Relationship |
| --- | --- |
| [NIST CSF 2.0](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md) | CSF 2.0 cites the AI RMF as a sibling that also uses Functions, Categories and Subcategories, and says treating AI risks alongside other enterprise risks yields a more integrated outcome. Cybersecurity and privacy risk management considerations apply to the design, development, deployment, evaluation and use of AI systems |
| [NIST Privacy Framework](../privacy-and-data-protection/nist-privacy-framework.md) | Privacy-enhanced is one of the seven characteristics |
| [SSDF](../application-security/supply-chain/nist-secure-software-development-framework.md) | SP 800-218A applies the SSDF to generative AI model development |
| [Google SAIF](google-secure-ai-framework.md) | A security-focused framework from a vendor. The AI RMF is broader than security and vendor neutral |
| [Enterprise risk management](../governance-and-compliance/risk-management/information-risk-management.md) | AI risk is one of the risks that CSF 2.0 Govern (GV.RM-03) routes into enterprise risk management |

## Worked example

The scenario: Example Corp (`example.com`) deploys a customer support chatbot built on a third-party language model. The task is to use the AI RMF functions to produce a first, small risk register and a prioritization. The ratings are invented for the lab, and a real assessment needs evidence.

**Govern.** The company records the chatbot in its AI system inventory (GOVERN 1.6), names an executive accountable for AI risk decisions (GOVERN 2.3), and requires a contingency process if the model vendor has an incident (GOVERN 6.2).

**Map.** MAP 1.1: purpose is answering refund and shipping questions for customers in three languages. MAP 2.2: knowledge limits are documented (policy changes weekly, the model may not know). MAP 4.1: components include a hosted model, a retrieval index of policy documents, and logging. MAP 5.1: impacts include wrong answers, privacy exposure and unequal service quality.

**Measure.** For each mapped risk the team picks a measurement (MEASURE 1.1) and documents it (MEASURE 2.1). Prioritization comes next (MANAGE 1.2). Tested with Python 3.10.12, standard library only:

```python
risks = [
    # (id, risk, likelihood 1-5, impact 1-5, measure used, treatment)
    ("R1", "Chatbot states a wrong refund policy (confabulation)", 4, 3, "weekly eval set of 200 policy questions", "retrieve answers from approved policy text, show source"),
    ("R2", "Customer personal data pasted into prompts is retained", 3, 5, "log scan for PII patterns", "redaction before logging, 30 day retention"),
    ("R3", "Prompt injection makes the bot reveal internal instructions", 4, 2, "red team prompts, 50 attacks", "no secrets in prompts, output filter"),
    ("R4", "Third-party model update changes behavior silently", 2, 4, "regression run on each vendor version", "pin model version, contract notice clause"),
    ("R5", "Biased handling of non-native speakers (fairness)", 3, 4, "error rate by language group", "human handoff, retrain prompts, monitor gap"),
]
ranked = sorted(risks, key=lambda r: r[2] * r[3], reverse=True)
print(f"{'id':3s} {'L':>1s} {'I':>1s} {'L*I':>3s}  risk -> treatment")
for rid, risk, l, i, measure, treat in ranked:
    print(f"{rid:3s} {l:1d} {i:1d} {l*i:3d}  {risk} -> {treat}")
```

Output:

```text
id  L I L*I  risk -> treatment
R2  3 5  15  Customer personal data pasted into prompts is retained -> redaction before logging, 30 day retention
R1  4 3  12  Chatbot states a wrong refund policy (confabulation) -> retrieve answers from approved policy text, show source
R5  3 4  12  Biased handling of non-native speakers (fairness) -> human handoff, retrain prompts, monitor gap
R3  4 2   8  Prompt injection makes the bot reveal internal instructions -> no secrets in prompts, output filter
R4  2 4   8  Third-party model update changes behavior silently -> pin model version, contract notice clause
```

**Manage.** MANAGE 1.2 prioritizes by impact, likelihood and resources: R2 first. MANAGE 4.1 sets post-deployment monitoring (feedback channel, override to a human agent, incident process). MANAGE 3.2 means the pre-trained model is monitored as a component, which is why R4 asks for pinned versions and a regression run.

What the example shows, and its limits:

1. The framework yields **a documented chain**: context, risk, measurement, treatment and monitoring. The scoring method (likelihood times impact) is a common convention, not part of the AI RMF, and ties and ordinal scales hide uncertainty. Revisit ratings when the system changes.
2. R3 (prompt injection) ranks lower because its impact here is low, as no secrets are in the prompt. That is a design decision from the treatment, not a guarantee. For security-specific risks such as prompt injection, data poisoning and model extraction, use security guidance and testing (see the planned topics in [AI security](README.md)).
3. R5 is a fairness risk. A pure security register would miss it, which is the reason for a wider framework.
4. `MANAGE 1.1` still applies. If R2 could not be reduced to an acceptable level, the answer may be not to deploy the feature.

## Trade offs and when to use it

### Benefits

- Covers risks that security frameworks do not (bias, explainability, human-AI configuration, societal harm).
- Familiar shape for anyone who knows the CSF, so it integrates with existing risk programs.
- Voluntary and use-case agnostic, so it scales from a single feature to an enterprise program.
- Free, with a playbook of suggested actions.

### Costs and limits

- **Outcome-level and non-prescriptive.** It does not say how to measure fairness or reliability for your system, and expert methods are needed.
- **Measurement is hard.** NIST says many AI risks are difficult to measure, and an unmeasured risk is not a low risk.
- **Not a security control catalog.** For secure engineering of AI systems use security guidance such as the SSDF community profile (SP 800-218A) and threat catalogs.
- **Fast-moving field.** Techniques, risks and related NIST profiles change quickly. Check for updates and profiles.
- **Voluntary.** Regulation, such as laws on AI, may impose obligations that the framework does not cover or meet by itself.

### Alternatives and companions

| Need | Option |
| --- | --- |
| Security of AI systems | [Google SAIF](google-secure-ai-framework.md), secure development practices (SP 800-218A) |
| Certifiable management system for AI | ISO/IEC 42001, mentioned from memory and not reviewed here |
| Regulation-driven obligations | The applicable AI law, with legal advice |
| Program-wide risk view | [NIST CSF 2.0](../governance-and-compliance/frameworks/nist-cybersecurity-framework.md) with GV.RM-03 |

## Common mistakes

| Mistake | Why it is wrong | Fix |
| --- | --- | --- |
| Treating the AI RMF as an AI security checklist | Security is only one of seven characteristics | Cover all characteristics, and add security testing |
| Skipping Map and starting with metrics | Without context you measure the wrong things | Document purpose, users, settings and impacts first |
| Assuming an unmeasured risk is small | NIST explicitly warns against it | Record unmeasurable risks and manage them with other controls |
| Running Govern once | It is meant to be ongoing | Review roles, policies and inventory as systems change |
| Evaluating once before launch | AI behavior changes with data, updates and use | Plan post-deployment monitoring (MANAGE 4.1) and tracking (MEASURE 3.1) |
| Ignoring third-party models and data | Third-party risk appears in Govern, Map and Manage | Inventory components, pin versions, set contractual notice and contingency |
| No option to stop | MANAGE 1.1 includes deciding not to proceed | Define go and no-go criteria in advance |
| Treating trade-offs as defects | NIST says trade-offs between characteristics are normal | Decide and document trade-offs per context |

## Practice

1. Name the four AI RMF functions and say which one is cross-cutting.
2. List the seven trustworthy AI characteristics. Which one is the base for the others, and which relates to all?
3. In the worked example, which function handles "decide whether to deploy at all", and which subcategory states it?
4. Why can "we could not measure it" not be reported as "low risk"?
5. Map two AI RMF categories to CSF 2.0 Functions.
6. A team wants to use a third-party language model. List the AI RMF subcategories you would check.

Hints and answers:

1. Govern, Map, Measure, Manage. Govern is cross-cutting.
2. Valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, fair with harmful bias managed. Valid and reliable is the base, and accountable and transparent relates to all.
3. Manage. MANAGE 1.1 (determine whether the system achieves its intended purposes and whether development or deployment should proceed).
4. NIST states that the inability to measure a risk does not imply a high or low risk. It only means the risk is not understood.
5. For example, GOVERN categories correspond in spirit to CSF Govern, and MANAGE 4 (response and recovery) corresponds to CSF Respond and Recover. These are interpretations, since the frameworks are not formally mapped in the documents I read.
6. GOVERN 6.1 and 6.2 (third-party risks and contingency), MAP 4.1 and 4.2 (components and third-party data and software), MANAGE 3.1 and 3.2 (monitoring third-party and pre-trained models).

## Further reading

- NIST, Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1 (January 2023). The primary source for everything stated as verified: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- NIST AI Risk Management Framework website, with the Playbook and related resources: https://www.nist.gov/itl/ai-risk-management-framework
- NIST, AI 600-1, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (July 2024). Not read for this note.
- NIST, The NIST Cybersecurity Framework (CSF) 2.0 (2024), for the relationship to AI risk: https://doi.org/10.6028/NIST.CSWP.29
