---
title: Authorization
area: identity and access
level: unrated
status: draft
last_verified: unverified
tags: [migrated, authorization]
migrated_from: Security.html, page 92
---

# Authorization

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Authorization** is the act of allowing or refusing access to resources within an application. It often takes place following authentication and establishes the resources and permissions that an authenticated user is granted access to. Authorization essentially answers the question, "What are you allowed to do?".

Authorization is essential to make sure users have the right amount of access within the application and it does so by guaranteeing that only those with the required permission have access to specific information. Implementation of authorization contributes to the overall **protection of your application** from potential security risks.

There are several ways applications can handle authorization, just to name two:

1. **Role-Based Access Control (RBAC)**: In this case, users are given permissions according to their positions in an organization. Access rights are tied to specific roles so you could imagine a case where an ordinary user position might only have limited access, whereas an admin might have complete access to all resources. Using this method of authorization makes it so that users only have access to the information necessary for their roles while easing management.
2. **Attribute-Based Access Control (ABAC)**: In this method, access is granted according to policies and attributes. User properties (such as department and job title), resource properties, and environmental properties (like access time) can all be considered attributes. ABAC offers you a flexible way to handle authorization Because the decisions made are based on a combination of policies and attributes hence giving you a higher level of control.

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
