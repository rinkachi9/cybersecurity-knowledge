---
title: Software Composition Analysis (SCA)
area: application security
level: unrated
status: draft
last_verified: unverified
tags: [migrated, sca]
migrated_from: Security.html, page 62
---

# Software Composition Analysis (SCA)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.

## Motivation

TODO: describe the problem this topic solves and what goes wrong without it.

## What it is?

**Software Composition Analysis (SCA)** is the process of **identifying, analyzing, and managing open-source and third-party components** used in software projects.

It detects:

- **Known vulnerabilities** in libraries and dependencies.
- **License compliance issues**.
- **Outdated components** that may pose security or stability risks.

Since modern applications often include **60-90% open-source code**, SCA is essential for securing the **supply chain**.

## Purpose

SCA focuses on:

- **Detecting vulnerable components** before they reach production.
- **Preventing supply chain attacks** (e.g., malicious package injections).
- **Maintaining license compliance** to avoid legal risks.
- **Reducing technical debt** by identifying outdated dependencies.

It aligns with **Shift Left Security** principles by addressing risks early in the development lifecycle.

## How it works

Typical SCA workflow:

1. **Inventory Generation:**
   - Scans your codebase, build files, and package managers (e.g., `npm`, `pip`, `maven`, `nuget`) to create a **Software Bill of Materials (SBOM)** - a complete list of all dependencies.
2. **Vulnerability Mapping:**
   - Cross-references identified components with public vulnerability databases (e.g., **NVD**, **OSV**, vendor advisories).
3. **License Analysis:**
   - Detects component licenses (MIT, GPL, Apache, etc.) and flags compliance risks.
4. **Risk Prioritization:**
   - Assigns severity levels (CVSS score) and suggests fixes (e.g., upgrade to a patched version).
5. **Continuous Monitoring:**
   - Watches for new vulnerabilities in components already in production.

## Key security risks addressed

- **Known CVEs:** Publicly disclosed vulnerabilities in dependencies.
- **Dependency Confusion:** Malicious package uploads to public repositories with the same name as internal packages.
- **Typosquatting:** Fake packages mimicking popular ones.
- **Outdated Libraries:** Unpatched security flaws.
- **License Violations:** Legal and compliance issues from incompatible licenses.

## Advantages

- **Early Detection:** Identifies issues before deployment.
- **Automated Process:** Integrates into CI/CD for continuous checks.
- **License Compliance:** Avoids legal issues.
- **Transparency:** Generates SBOMs for audits.
- **Supply Chain Security:** Prevents indirect compromise via dependencies.

## Limitations

- **No Zero-Day Detection:** Only works for vulnerabilities with known CVEs.
- **False Positives:** Some flagged vulnerabilities may not be exploitable in your context.
- **Transitive Dependency Risk:** Vulnerabilities deep in dependency chains may be harder to fix.
- **Requires Timely Updates:** Even if SCA finds issues, action must be taken quickly.

## Best practices

1. **Integrate into CI/CD:** Run scans automatically on pull requests or builds.
2. **Fail on Critical Vulnerabilities:** Block deployments until patched.
3. **Use Trusted Sources:** Pull dependencies from verified repositories.
4. **Manage Transitive Dependencies:** Audit not just direct, but also indirect dependencies.
5. **Maintain an SBOM:** Keep an up-to-date inventory of all third-party components.
6. **Automated Updates:** Use tools like Dependabot or Renovate to apply upgrades.

## Common SCA Tools

- **Commercial:**
  - Snyk
  - Black Duck (Synopsys)
  - WhiteSource (Mend)
  - Veracode SCA
  - FOSSA
- **Open Source:**
  - OWASP Dependency-Check
  - Trivy
  - Syft + Grype
  - osv-scanner

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
