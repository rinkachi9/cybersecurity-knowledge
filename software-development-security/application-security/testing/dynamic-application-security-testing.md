# Dynamic Application Security Testing (DAST)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Dynamic Application Security Testing (DAST)** is a **black-box** security testing method that examines an application **in its running state** to identify vulnerabilities exploitable during normal operation.

Unlike SAST, DAST does not require access to the source code - it interacts with the application like an external user or attacker would, sending inputs and analyzing responses.

- Think of DAST as **"penetration testing by automation"**.
- Commonly used for **web, API, and mobile applications**.

## Purpose

DAST is used to:

- **Detect runtime vulnerabilities:** Finds issues that only appear when the app is deployed and running.
- **Simulate real-world attacks:** Mimics how attackers exploit applications over the network.
- **Validate security controls:** Confirms whether implemented protections actually work in production-like environments.
- **Catch environment-specific flaws:** Detects misconfigurations and issues in deployed environments.

## How it works

DAST tools operate by:

1. **Crawling the Application:**
   - Automatically mapping all reachable endpoints (links, forms, APIs).
2. **Sending Malicious Payloads:**
   - Testing for vulnerabilities using known attack patterns (e.g., SQL injection strings, XSS scripts).
3. **Analyzing Responses:**
   - Checking HTTP responses, error messages, and behavior changes for indicators of vulnerabilities.
4. **Reporting:**
   - Documenting discovered vulnerabilities with severity ratings and remediation suggestions.

## Common vulnerabilities

DAST is particularly effective at finding:

- **Injection Flaws:** SQL, LDAP, OS command injections.
- **Cross-Site Scripting (XSS).**
- **Authentication Weaknesses:** Weak login mechanisms, session handling flaws.
- **Insecure Direct Object References (IDOR).**
- **Security Misconfigurations:** Directory listing, verbose error messages.
- **Cross-Site Request Forgery (CSRF).**
- **Open Redirects.**
- **SSL/TLS Issues:** Weak ciphers, expired certificates.

## Advantages

- **No Source Code Required:** Useful for testing third-party apps or legacy systems.
- **Environment Coverage:** Finds issues in production-like setups.
- **Language Agnostic:** Works regardless of programming language or framework.
- **Real-World Relevance:** Simulates actual attack vectors.

## Limitations

- **Limited Code Path Coverage:** Only tests what it can access through exposed endpoints.
- **No Code Insight:** Cannot pinpoint the exact line of code causing a vulnerability.
- **False Negatives:** May miss vulnerabilities hidden behind complex user flows or authentication.
- **Slower Feedback Loop:** Typically used later in the development process compared to SAST.

## Best practices

1. **Run in a Test/Staging Environment:** Avoid disrupting production systems.
2. **Combine with SAST:** Get both code-level insight and runtime coverage.
3. **Configure Authentication:** Provide the scanner with valid credentials to test protected areas.
4. **Tune Payloads & Rules:** Customize tests for the application’s technology stack.
5. **Schedule Regular Scans:** Include DAST in CI/CD to detect regressions.
6. **Manual Verification:** Have security engineers review findings to eliminate false positives.

## Common DAST Tools

- **Commercial:**
  - Burp Suite Professional
  - IBM AppScan
  - Acunetix
  - Netsparker
- **Open Source:**
  - OWASP ZAP (Zed Attack Proxy)
  - w3af
  - Nikto
  - Arachni

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
