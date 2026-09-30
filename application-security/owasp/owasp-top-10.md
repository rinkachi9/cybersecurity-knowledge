# OWASP Top 10

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

The **OWASP Top 10** is a globally recognized list of the **10 most critical web application security risks**, published by the **Open Worldwide Application Security Project (OWASP)**.

OWASP is a nonprofit organization that works to improve the security of software by providing free, open resources to developers, testers, and security professionals.

### Purpose

The OWASP Top 10 is designed to:

- Raise **awareness** about the most common and severe web application vulnerabilities.
- Help developers and organizations **prioritize security risks** in their software.
- Provide **guidance** on how to test for and prevent these vulnerabilities.
- Encourage the adoption of **secure coding and design practices**.

### Structure of OWASP Entry

Each item in the Top 10 includes:

- **Risk description** (what it is and how it works)
- **Impact level** (e.g., data breach, system takeover)
- **Prevalence** (how common it is)
- **Examples and attack scenarios**
- **Mitigation strategies**

### Importance

- It's widely used in **security standards**, audits, and development policies.
- **Compliance**: Many organizations require developers to address OWASP Top 10 risks.
- **Real-world relevance**: These are the most **commonly exploited** weaknesses in live applications.

## Vulnerabilities

| # | Name | Summary |
| --- | --- | --- |
| **A01** | **Broken Access Control** | Users can access data or functions without proper authorization. |
| **A02** | **Cryptographic Failures** | Weak or missing encryption leads to data exposure. |
| **A03** | **Injection** | Attackers inject malicious code (e.g., SQL, NoSQL, OS commands). |
| **A04** | **Insecure Design** | Fundamental design flaws that lead to security issues. |
| **A05** | **Security Misconfiguration** | Improperly configured systems or frameworks (e.g., default passwords, open S3 buckets). |
| **A06** | **Vulnerable and Outdated Components** | Use of components with known vulnerabilities (e.g., old libraries). |
| **A07** | **Identification and Authentication Failures** | Broken login systems, session hijacking, brute force risks. |
| **A08** | **Software and Data Integrity Failures** | Trusting unsigned or unverified software/data updates. |
| **A09** | **Security Logging and Monitoring Failures** | Lack of visibility into attacks or delayed detection. |
| **A10** | **Server-Side Request Forgery (SSRF)** | Abusing the server to send requests to unintended locations (internal systems or cloud metadata). |

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
