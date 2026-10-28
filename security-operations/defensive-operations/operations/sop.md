# SOP

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

A Standard Operating Procedure is a documented, step-by-step set of instructions designed to help analysts carry out complex routine operations.

In cybersecurity, SOPs aim to achieve:

- Efficiency: Reducing the "thinking time" during a crisis.
- Quality Output: Ensuring no critical steps (like evidence preservation) are missed.
- Uniformity: Making sure Analyst A and Analyst B handle the same threat in the same way.
- Compliance: Providing an audit trail to prove the company follows its own security policies.

## SOP vs. Playbook

These terms are often used interchangeably, but in a mature SecOps environment, they differ:

| **Feature** | **SOP (The Strategy)** | **Playbook (The Execution)** |
| --- | --- | --- |
| Focus | High-level "What" and "Why." | Tactical "How-To." |
| Audience | Humans (Analysts, Managers, Auditors). | Humans + Machines (SOAR). |
| Content | Roles, responsibilities, legal requirements, escalation paths. | Specific commands, API calls, tool-click sequences. |
| Example | *Incident Response SOP for Data Breach.* | *Playbook for Brute Force Detection.* |

## Key components

A "concrete" SOP should contain the following sections to be effective:

### A. Identification & Scope

- Objective: What is this SOP trying to solve? (e.g., "Handling Lost/Stolen Devices").
- Scope: Does this apply to all employees or just the IT department?
- Roles: Who is the Incident Commander? Who is the Lead Analyst?

#### B. The "Trigger"

- What event starts this process? (e.g., A "High" severity alert in the SIEM or an email from the CEO).

#### C. The Workflow (The Meat)

The step-by-step actions, usually divided into the NIST or SANS incident phases:

1. Identification: How do we confirm the threat is real?
2. Containment: How do we stop the bleeding?
3. Eradication: How do we remove the threat?
4. Recovery: How do we get back to business?

#### D. Escalation Matrix

This is the "Who do I call?" section. It defines at what point the security team needs to involve:

- Legal/Compliance (for data privacy issues).
- Public Relations (for external breaches).
- The CISO or Board of Directors.

#### E. Evidence & Documentation

- Instructions on how to save logs, take screenshots, and document the timeline for forensic purposes.

## Practical example

*Shortened for brevity:*

1. Verification: Check the SIEM for multiple failed logins followed by a success from an unusual geo-location.
2. Immediate Action: Reset the user's password in Active Directory and revoke all active O365 sessions.
3. Communication: Call the user via a trusted channel (e.g., phone) to verify their activity.
4. Forensics: Review the last 24 hours of the user’s file access logs.
5. Reporting: Log the incident in the ticketing system and tag it as "Identity Theft - Resolved."

## Why SOPs Fail

Documentation is only useful if it’s alive. SOPs fail when:

- They are too long: An 80-page PDF won't be read during a ransomware attack.
- They are "Shelfware": Written once for an auditor and never updated.
- Lack of Training: If the team hasn't practiced the SOP in a Tabletop Exercise (TTX), it won't work in reality.

## Continuous Improvement: Post-Mortem

Every time an SOP is used, the final step should be a Lessons Learned meeting.

- *Did the SOP help?*
- *Was a step confusing?*
- *Do we need a new tool to automate part of it?*

The answers to these questions are used to update the SOP, creating a "feedback loop" that constantly hardens the organization's defense.

## Summary

The SOP is the organizational memory of the SecOps team. It ensures that the knowledge of your best analyst is available to your newest hire, and it provides the logical foundation upon which your SOAR automation is built.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
