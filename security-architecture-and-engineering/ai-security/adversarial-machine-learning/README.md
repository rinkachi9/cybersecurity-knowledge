# Adversarial artificial intelligence

## Summary

Adversarial machine learning (AML) is the study of attacks that exploit the statistical, data-driven nature of AI systems, and of defenses against them. The attacker does not need a software bug. They feed inputs that look normal to a person but push the model across a decision boundary, plant a few corrupted training examples, ask the model enough questions to copy it or reconstruct what it was trained on, or hide instructions in content that a language model will read. NIST AI 100-2 E2025 (March 2025) is the common vocabulary: attacks are classified by system type, life cycle stage, attacker goal, capability and knowledge. This note uses that taxonomy, runs four toy attacks with real numbers and states the limits of current defenses. Offensive material is for study, labs and authorized testing.

## Prerequisites

- [CIA triad](../../../security-and-risk-management/foundations/cia-triad/README.md): the taxonomy maps attacker goals to availability, integrity and privacy.
- [NIST AI Risk Management Framework](../../../security-and-risk-management/governance-and-compliance/frameworks/nist-ai-risk-management-framework.md) and [Google Secure AI Framework](../google-secure-ai-framework.md) for the governance and design context.
- [Threat modeling](../../../security-and-risk-management/threat-modeling/threat-modeling.md), because AML attacks are best placed on a model of the whole system.
- Basic machine learning: training data, a model, inference, a decision boundary.

## Core concepts

### Definition

NIST AI 100-2 E2025, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations* (final, March 2025, corrected PDF of April 2025), defines the field as the study of "attacks against ML systems that exploit the statistical, data-based nature of ML systems". It separates two system classes:

- **Predictive AI (PredAI)**: classifiers, detectors and regressors, for example image recognition or fraud scoring.
- **Generative AI (GenAI)**: models that produce text, images or code, often deployed with access to private data or tools that act in the world.

The report excludes flaws that cause failures outside adversarial use, such as plain inaccuracy. An accuracy bug is a quality issue, an AML attack requires an adversary.

### Analogy

A spam filter is a customs officer trained on past smuggling cases. An attacker can (1) disguise a parcel so it looks like a harmless one (evasion), (2) slip mislabeled examples into the officer's training binder so that a type of parcel is waved through (poisoning), (3) send many parcels to learn the officer's rules and open a rival checkpoint with the same rules (extraction), or (4) infer who was in the training binder from how the officer reacts (membership inference). The analogy breaks because a human officer understands what a parcel is. A model only follows learned statistics, so a small, targeted change that is meaningless to a person can flip its answer.

### Classification used by NIST

NIST classifies each attack along five dimensions.

| Dimension | Values (from the report) |
| --- | --- |
| System type | Predictive AI, generative AI |
| Life cycle stage | Training stage, deployment stage |
| Attacker goal | Availability breakdown (NISTAML.01), integrity violation (NISTAML.02), privacy compromise (NISTAML.03), and for GenAI misuse enablement (NISTAML.04) |
| Attacker capability | Control of training data, control of the model, query access, control of resources the model reads, label control, source code control and others |
| Attacker knowledge | White-box, gray-box, black-box |

The three goals are the CIA triad applied to ML. The report's classes of attack map to them:

| Class | Stage | Typical goal | Section of the report |
| --- | --- | --- | --- |
| Evasion (adversarial examples) | Deployment | Integrity | 2.2 |
| Poisoning (availability, targeted, backdoor, model poisoning) | Training | Integrity or availability | 2.3 |
| Privacy attacks (data reconstruction, membership inference, property inference, model extraction) | Deployment | Privacy | 2.4 |
| Supply chain attacks on data and models (GenAI, NISTAML.05) | Training or deployment | Integrity | 3.2 |
| Direct prompting (jailbreaks, information extraction) | Deployment | Integrity, privacy, misuse | 3.3 |
| Indirect prompt injection | Deployment | Availability, integrity, privacy | 3.4 |
| Attacks on agents | Deployment | All | 3.5 |

### Mechanism by class

**Evasion.** A trained model is fixed. The attacker modifies an input `x` by a small perturbation so the prediction changes while the input stays close to the original under some distance metric. With white-box access the attacker follows the gradient of the loss. For a linear model the best perturbation is `eps * sign(w)`, the idea behind the fast gradient sign method. With only query access (black-box) the attacker estimates the gradient from outputs, or uses a surrogate model and relies on *transferability*: adversarial examples often fool other models trained on similar data. Real-world versions are physical (stickers on road signs) and digital (malware features tweaked to avoid a classifier).

**Poisoning.** The attacker controls part of the training data or labels, or the model parameters. The report distinguishes availability poisoning (degrade the model overall), targeted poisoning (misclassify chosen inputs), backdoor poisoning (a trigger pattern makes the model output the attacker's label while behavior is normal otherwise) and model poisoning (corrupt parameters, relevant to federated learning and downloaded models). Clean-label poisoning (NISTAML.012) keeps labels correct so manual review does not catch it.

**Privacy attacks.** An attacker with query access infers information about the training data or the model:

- *Data reconstruction*: recover training samples.
- *Membership inference*: decide whether a specific record was in the training set.
- *Property inference*: learn a global property of the training data.
- *Model extraction*: copy the functionality of the model through queries.

**Generative AI.** GenAI systems add attacks that use natural language as the control channel:

- *Direct prompting*: a user crafts input to bypass restrictions (jailbreaks) or to extract hidden prompts and data. The report lists techniques such as prefix injection, refusal suppression, style injection, role-play and obfuscation such as base64 encoding or character transformations.
- *Indirect prompt injection*: instructions arrive in content the model reads on the user's behalf: a web page, an email, a retrieved document, a tool output. The user never typed the attack. The report places the risk in four places: in-context instructions and system prompts, runtime data ingestion from third-party sources (retrieval-augmented generation), output handling, and agents that act on model output.
- *Agents*: a model with tools turns a text-level attack into actions, such as sending data out or changing records. Least privilege for tools matters more than for chat.

### Why defenses are hard

The report states in section 4 that there are theoretical limitations on adversarial robustness and trade-offs between the attributes of trustworthy AI, and that evaluation of defenses is difficult. In practice:

- *Adversarial training* (training on adversarial examples) improves robustness against known attack types at a cost in accuracy and compute and does not cover new attacks. The report names it with randomized smoothing and formal verification as the main mitigation families for evasion.
- Detecting adversarial inputs is itself a learning problem the attacker can target.
- For prompt injection I know of no single control that removes the risk. This is my summary, not a statement from the report, which has its own mitigation sections 3.3.3 and 3.4.4 that I read only in part. Layers are needed: privilege separation, input and output filtering, human confirmation for sensitive actions, and treating all retrieved content as untrusted.
- Poisoning defenses rely on data provenance, anomaly detection in training data and robust training. They do not remove the need to trust the data source.

### Relation to other frameworks

- **MITRE ATLAS** is an ATT&CK-style matrix of adversary tactics and techniques against AI systems, and **OWASP Top 10 for LLM Applications** lists the main application risks. I know both but did not re-read them for this note.
- **NIST AI RMF** treats "secure and resilient" as one of the characteristics of trustworthy AI, and AI 100-2 states that it adopts the concepts of security, resilience and robustness from it.
- In the CISSP outline, AI appears in section 7.7 (machine learning and AI based tools) and section 1.12 (awareness content on emerging technologies including AI). See [CISSP security domains](../../../security-and-risk-management/reference/certifications/cissp-security-domains.md).

## Worked example

The script `scripts/aml-toy-attacks.py` implements a two-feature logistic regression in plain Python, trained on synthetic data (two Gaussian classes, 200 training points, 1000 test points), then attacks it four ways. Python 3.10, standard library only, fixed random seed. The output is real. It is a toy model: the numbers show the mechanism and the order of magnitude, not the behavior of a deep network.

```bash
python3 scripts/aml-toy-attacks.py
```

Output:

```text
baseline               : test accuracy 0.975
1 evasion eps=0.5      : accuracy 0.917
1 evasion eps=1.0      : accuracy 0.759
1 evasion eps=2.0      : accuracy 0.241
2 label flipping 0.1   : accuracy of retrained model 0.971
2 label flipping 0.3   : accuracy of retrained model 0.966
2 label flipping 0.45  : accuracy of retrained model 0.735
3 extraction (300 q)   : surrogate agrees with the victim on 0.996 of test inputs
4 membership signal    : mean confidence members 0.999 vs non-members 0.977
```

1. **Evasion.** The classes are centered at (+1.5, +1.5) and (-1.5, -1.5), so a shift of 2.0 per feature moves a point across the boundary. Accuracy falls from 97.5% to 91.7%, 75.9% and 24.1% as the perturbation grows, below 50% because the attack is directed against the true label. The attacker knows the model weights (white-box). The defender's view: a perturbation of 2.0 here is large compared to the class spread of 1.0, which is the toy equivalent of the trade-off between imperceptibility and success.
2. **Poisoning.** The retrained model tolerates 10% and 30% flipped labels, because logistic regression averages out noise, and degrades at 45% (73.5%). This illustrates that random label noise is weak. Targeted poisoning, where the attacker picks which points to corrupt, is more efficient than the random flipping shown here, and this script does not implement it.
3. **Extraction.** With 300 label queries the attacker trains a surrogate that agrees with the victim on 99.6% of test inputs. For a simple model, query access is almost a copy. The defender's levers are rate limits, query monitoring, returning labels instead of confidence scores and legal protection of the API.
4. **Membership inference.** A deliberately overfit model (12 training points, 5000 epochs) shows a mean confidence of 0.999 on its training points against 0.977 on fresh points. The gap is small in this toy, but it is the signal an attacker thresholds. Reducing overfitting and limiting confidence output reduce it. Differential privacy gives a formal bound at a cost in accuracy; I did not demonstrate it.

## Trade offs and when to use it

**What to do about it, in order of cost-effectiveness:**

1. Treat the ML system as a software system first: authentication, rate limiting, logging, least privilege for the model's tools and data, secure supply chain for datasets and model files.
2. Control the data: provenance, access control on training pipelines, validation and anomaly checks on new data.
3. Limit what the API reveals: no confidence scores unless needed, rate limits, query anomaly detection, quotas per identity.
4. For GenAI with tools: treat retrieved text and tool output as untrusted, restrict tools, require human confirmation for irreversible actions and keep secrets out of the context window.
5. Test: adversarial evaluation as part of release testing, red teaming of prompts and tools, repeated after model or prompt changes.
6. Add robustness techniques (adversarial training, ensembles, input sanitization) where the threat model justifies the cost.

**Limits and costs.** Robust training lowers accuracy and increases cost. Filters can be bypassed. No defense is known to be complete, which is why the report advises risk management, not a promise of safety. Choose defenses by the attacker capability that is realistic: an external user with query access is a different threat from an insider who can change training data.

**When AML is not the main risk.** A model that makes low-impact suggestions with a human reviewing every output has a smaller AML risk than the plain application risks around it. Do not spend the budget on adversarial robustness when access control on the training bucket is open.

## Common mistakes

| Mistake | Effect | Fix |
| --- | --- | --- |
| Treating model accuracy as security | A high benchmark score says nothing about adversarial inputs | Evaluate against attacks matched to the threat model |
| Trusting retrieved content | Indirect prompt injection | Mark and isolate untrusted content, restrict tools |
| Giving an agent broad tool permissions | A text attack becomes an action | Least privilege, confirmation for sensitive actions |
| Exposing full probability outputs | Easier extraction and membership inference | Return the minimum needed |
| Ignoring the data pipeline | Poisoning and backdoors | Access control and provenance for data and models |
| Downloading model files from unknown sources | Malicious model or backdoor | Verify source and hash, use safe formats, scan |
| One-time testing | New attacks appear, models change | Repeat tests after changes |
| Claiming a filter "solves" prompt injection | False confidence | Defense in depth, see [defense in depth](../../design-principles/defense-in-depth.md) |

Detection and mitigation: monitor query patterns (many near-duplicate queries with small changes suggest evasion search or extraction), log and review model inputs and tool calls, alert on training data drift, and use canary tokens in prompts and documents to detect injection and exfiltration. Incident response for AI systems follows the same [lifecycle](../../../security-operations/defensive-operations/operations/nist-incident-response/README.md), with the added step of retraining or rolling back a model.

## Practice

1. Place each attack on the NIST dimensions: a sticker on a stop sign, a poisoned image set with a hidden trigger, a chatbot that follows instructions found in a web page it summarizes.
2. Why did the toy evasion attack succeed with no knowledge of the data, only the weights? What changes in a black-box setting?
3. In the poisoning results, random label flipping at 30% barely hurt. Why is that not reassuring?
4. Name two controls that reduce model extraction and one that reduces membership inference.
5. An internal assistant can read the company wiki and send emails. Describe an indirect prompt injection and three controls.
6. Extend the script with a targeted poisoning: flip only the labels of points near the boundary. Compare the accuracy with random flipping at the same budget.

**Answers and hints**

1. Sticker: PredAI, deployment, integrity violation, evasion (physical). Poisoned set: PredAI, training, integrity, backdoor poisoning. Web page: GenAI, deployment, integrity or privacy, indirect prompt injection.
2. The attack used the weights, so it was white-box. In black-box, the attacker estimates the gradient from outputs or trains a surrogate and relies on transferability.
3. Because the attacker chooses which samples to corrupt. Targeted or backdoor poisoning needs a small fraction of the data and leaves normal accuracy intact, so average accuracy hides it.
4. Rate limiting and query monitoring, and returning labels without scores. For membership inference, regularization or differential privacy.
5. A wiki page contains hidden text telling the assistant to email the contents of a document to an outside address. Controls: no outbound email to external domains without approval, treat wiki content as untrusted data, least privilege on documents, logging and alerts on sends.
6. Hint: pick the 20% of training points with the smallest `abs(w.x + b)` and flip those.

## Further reading

- NIST, [AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) (March 2025): the taxonomy used in this note. The PDF was downloaded and its table of contents, introduction and attacker goal definitions were read. The detailed sections on each attack were read only in part.
- NIST, [AI Risk Management Framework](../../../security-and-risk-management/governance-and-compliance/frameworks/nist-ai-risk-management-framework.md): the governance context, see the repository note.
- MITRE ATLAS and the OWASP Top 10 for LLM Applications: related catalogs. Not re-read for this note.
- Goodfellow et al. (2015), Explaining and harnessing adversarial examples: the fast gradient sign method. Cited through the NIST report's reference list, not re-read.
