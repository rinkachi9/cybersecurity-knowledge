---
title: Tailgating
area: threats and attacks
level: unrated
status: draft
last_verified: unverified
tags: [migrated, tailgating, social-engineering]
migrated_from: Security.html, page 76
---

# Tailgating

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Tailgating** (also called **piggybacking**) is a **physical security breach** where an unauthorized person gains entry to a restricted area by **closely following an authorized person** without their knowledge or consent.

It exploits **human behavior** - particularly politeness and trust - rather than technical system weaknesses.

### Categorization

- **Vector-Based:** Physical entry.
- **Technique-Based:** Social engineering, physical intrusion.
- **Objective-Based:** Unauthorized physical access to restricted areas, enabling theft, espionage, or sabotage.

## How it works

1. **Target Identification:**
   - Attacker identifies a secured entry point requiring authentication (badge, biometric, keypad).
2. **Positioning:**
   - The attacker waits for an authorized employee to approach and open the door.
3. **Execution:**
   - The attacker follows closely behind, timing entry so the door does not fully close.
4. **Exploitation:**
   - Once inside, the attacker can move freely or attempt further social engineering to escalate access.

## Common scenarios

- **Office Buildings:** Following an employee into a badge-protected elevator or office floor.
- **Data Centers:** Entering a server room behind an IT staff member.
- **Warehouses:** Walking into a restricted loading area with delivery personnel.
- **Events/Conferences:** Accessing VIP or staff-only areas without credentials.

## Variants

| **Type** | **Description** | **Example** |
| --- | --- | --- |
| **Unintentional Tailgating** | Victim is unaware of the intruder following. | Employee holding the door for a stranger. |
| **Intentional Piggybacking** | Victim knowingly allows entry without proper checks. | Letting a “forgot my badge” colleague in without verification. |
| **Forced Entry** | Attacker pressures the victim into letting them in. | Pretending to carry heavy packages and asking for help. |

## Psychological and human factors exploited

- **Politeness Norms:** People hold doors for others.
- **Authority Bias:** Attacker appears as a superior or authority figure.
- **Urgency:** Attacker appears rushed or stressed.
- **Familiarity:** Attacker dresses or behaves like they belong (e.g., wearing similar uniforms).

## Impact

- **Physical Security Breach:** Unauthorized access to offices, server rooms, warehouses.
- **Data Theft:** Stealing sensitive documents or devices.
- **Espionage/Sabotage:** Installing hardware keyloggers, rogue devices, or tampering with systems.
- **Safety Risks:** Potential for violence or property damage.

## Detection and prevention

### Detection

- CCTV and access logs to identify entry anomalies.
- Security personnel trained to spot suspicious entry patterns.

### Prevention

- **Technical:**
  - Install anti-tailgating systems (mantraps, turnstiles).
  - Use access logs with real-time monitoring alerts.
- **Physical:**
  - Require all personnel to badge in individually.
  - Employ security guards at entrances.
- **Behavioral:**
  - Train staff to challenge unfamiliar individuals without visible ID.
  - Promote “No Badge, No Entry” policies.
- **Organizational:**
  - Regular security awareness campaigns.
  - Encourage a culture of security over politeness.

## Tailgating in modern threat landscape

- Increasingly relevant in **hybrid work models** where not all staff know each other personally.
- Can be combined with **insider threats** - attacker gains physical presence and colludes with an employee.
- Plays a **reconnaissance role** in complex attacks, enabling placement of rogue network devices for cyber intrusions.

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
