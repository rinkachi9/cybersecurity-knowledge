# Threat modeling

How to think about what can go wrong in a system, and the main methodologies for doing it in a structured way.

## Notes

- [Threat modeling](threat-modeling.md): Definition, the four questions, DFDs and trust boundaries, method selection and a worked example used by all method notes.
- [Threat modeling methodologies](methodologies.md): Comparison of the main methodologies and their strengths and weaknesses.

### Methods

Individual threat modeling methods.

Entry point: [methods](methods/README.md).

- [STRIDE](methods/stride.md): Six threat categories mapped to security properties, applied per DFD element, with a worked example.
- [Attack Trees](methods/attack-trees.md): Representing how an attacker can reach a goal as a tree of steps.
- [Process for Attack Simulation and Threat Analysis (PASTA)](methods/pasta.md): Seven risk-centric stages from business objectives to attack simulation and a risk heat map.
- [Trike](methods/trike.md): Requirements-based audit method: actor-asset-action matrix, generated DoS and EoP threats, exposure scores.
- [VAST](methods/vast.md): Visual, Agile and Simple Threat modeling: application and operational models for large portfolios.
- [Hybrid Threat Modeling Method (hTMM)](methods/hybrid-threat-modeling-method.md): Combining several methodologies in one process.
- [Security Cards](methods/security-cards.md): Card-based, collaborative threat discovery.

## Planned topics

These topics are not written yet. They are listed so the scope of the area is visible.

- Data flow diagrams and trust boundaries
- LINDDUN
- Threat modeling in CI/CD
- Threat model reviews

Back to the [table of contents](../../ToC.md).
