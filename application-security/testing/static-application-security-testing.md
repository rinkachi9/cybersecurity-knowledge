---
title: Static Application Security Testing (SAST)
area: application security
level: unrated
status: draft
last_verified: unverified
tags: [migrated, sast]
migrated_from: Security.html, page 64
---

# Static Application Security Testing (SAST)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Static Application Security Testing (SAST)** is a **white-box** security testing method that analyzes application source code, bytecode, or binaries **without executing the program**.

Its main goal is to identify **security vulnerabilities early in the development lifecycle** by scanning the codebase for insecure patterns, logic flaws, and non-compliance with security standards.

- Think of SAST as “**security linting**” for code, but with deep analysis capabilities.
- It’s part of the **Shift Left** security approach - integrating security checks into development before the software is built and deployed.

## Purpose

SAST helps:

- **Identify vulnerabilities early:** Fixing bugs during development is cheaper and faster than post-deployment.
- **Enforce secure coding standards:** Ensures compliance with frameworks like OWASP ASVS, CERT Secure Coding, or company-specific guidelines.
- **Reduce attack surface:** Eliminates insecure code paths before they can be exploited.
- **Meet compliance requirements:** Some standards (e.g., PCI DSS) mandate code reviews or SAST for certain applications.

## How it works

SAST tools work by:

1. **Parsing the Source or Binary:**
   - The tool scans code files or compiled binaries to understand the application’s structure.
2. **Building a Model:**
   - It creates an abstract representation of code flows, functions, variables, and dependencies.
3. **Data Flow & Control Flow Analysis:**
   - Traces how data moves through the application (data flow) and how execution paths are structured (control flow).
4. **Rule-Based Analysis:**
   - Uses predefined vulnerability rules to detect insecure coding patterns (e.g., unsanitized input reaching a database query → SQL Injection risk).
5. **Reporting:**
   - Generates reports categorizing findings by severity, vulnerability type, and remediation suggestions.

## Common vulnerabilities detected by SAST

SAST is effective at finding:

- **Injection Flaws:** SQL Injection, LDAP Injection, OS Command Injection.
- **Cross-Site Scripting (XSS).**
- **Insecure Cryptographic Use:** Weak algorithms, hardcoded keys.
- **Authentication & Authorization Issues:** Missing or flawed checks.
- **Buffer Overflows & Memory Issues** (in languages like C/C++).
- **Insecure API Usage:** Functions known for security risks.
- **Hardcoded Secrets:** API keys, passwords in code.

## Advantages

- **Early Detection:** Catches issues before runtime.
- **No Execution Needed:** Works without deploying or running the app.
- **Comprehensive Coverage:** Can analyze all code paths, even rare ones.
- **Automatable:** Fits into CI/CD pipelines for continuous scanning.
- **Compliance-Friendly:** Provides documented evidence for audits.

## Limitations

- **False Positives:** May flag non-exploitable code.
- **No Runtime Context:** Can’t detect issues dependent on environment or actual data flows in production.
- **Language/Framework Specificity:** Needs rule sets tailored for the language and libraries in use.
- **Limited in Detecting Configuration Issues:** These are often found by other methods (e.g., DAST or IAST).

## Best practices

1. **Integrate Early:** Run scans in local dev environments and in CI/CD pipelines.
2. **Use Incremental Scans:** Avoid full scans on every commit - scan only changed code to speed up builds.
3. **Prioritize Findings:** Triage results based on risk and exploitability.
4. **Tune Rules:** Customize rulesets to reduce false positives and align with project tech stack.
5. **Developer Training:** Teach developers how to interpret findings and fix issues.
6. **Combine with Other Testing:** Use DAST (Dynamic Application Security Testing) or IAST (Interactive Application Security Testing) for runtime coverage.

## SAST Tools

- **Commercial:**
  - Checkmarx
  - Fortify Static Code Analyzer
  - Veracode SAST
  - SonarQube (commercial edition for security rules)
- **Open Source:**
  - SonarQube (community edition - limited security rules)
  - Semgrep
  - Bandit (Python)
  - ESLint security plugins (JavaScript/TypeScript)
  - Brakeman (Ruby on Rails)

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
