---
title: Authentication vs Authorization
area: identity and access
level: unrated
status: draft
last_verified: unverified
tags: [migrated, authentication, authorization]
migrated_from: Security.html, page 99
---

# Authentication vs Authorization

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## Introduction

### Authentication

- **Definition:** The process of verifying the identity of a user or system.
- **Purpose:** Ensures that the user is who they claim to be.
- **Example:** Entering a username and password, scanning a fingerprint, or using a multi-factor authentication code.
- **Role:** Establishes **identity**.

### Authorization

- **Definition:** The process of determining what actions or resources a verified user or system is permitted to access.
- **Purpose:** Defines what an authenticated user is allowed to do.
- **Example:** Granting a user permission to access specific files, modify data, or perform administrative tasks.
- **Role:** Establishes **permissions**.

### Comparison

#### Comparison

| Aspect | Authentication | Authorization |
| --- | --- | --- |
| **Question Answered** | "Who are you?" | "What are you allowed to do?" |
| **Focus** | Identity verification | Permission and access control |
| **Timing** | Occurs first | Follows authentication |
| **Data Involved** | Credentials (e.g., passwords, biometrics) | Access rights and policies |
| **Example in Action** | Logging into a system | Accessing a restricted dashboard |
| **Implementation** | Techniques like passwords, OTP, biometrics | Role-based or policy-based access control |

## Key differences

### Verification vs. Permission

As previously stated, authentication and authorization serve distinct functions inside the security system. Authentication is used to confirm the identity of a user or process. Consider it as a way to verify yourself at the door by showing your ID. Authorization, on the other hand, focuses on ensuring that specific users have specific permissions after they enter. Think of it as the key card that allows you access to specific locations or resources depending on your position.

#### Sequential Process

Authentication always comes before authorization. You could think of it as a 2-step process with authentication always coming first. The system always has to verify who enters it before it can determine what these verified users are permitted to do once they're in.

#### Integrated Security Approach

They work together quite well despite their differences. You can think of them as two sides of the same coin: authentication ensures that only valid users can access the program, whereas authorization ensures that those users can only access the resources they are authorized to. It's a team effort from both ends that ensures the security of the entire application is not compromised.

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
