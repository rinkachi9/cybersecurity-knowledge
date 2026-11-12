# Application security

Securing software: standards, testing approaches, common vulnerabilities and the software supply chain.

## Notes

### Owasp

OWASP material.

Entry point: [owasp](owasp/README.md).

- [OWASP](owasp/owasp.md): The OWASP foundation, its flagship projects and how they fit together.
- [OWASP security principles](owasp/owasp-security-principles.md): The 16 design principles of the OWASP Developer Guide.
- [OWASP Top 10](owasp/owasp-top-10.md): The list of the ten most critical web application security risks.

### Vulnerabilities

Vulnerability classes.

Entry point: [vulnerabilities](vulnerabilities/README.md).

- [Cross-site scripting (XSS)](vulnerabilities/cross-site-scripting/README.md): Types (stored, reflected, DOM-based), impact, defense layers and a tested local lab.

### Testing

Automated security testing approaches.

Entry point: [testing](testing/README.md).

- [Static Application Security Testing (SAST)](testing/static-application-security-testing.md): White-box analysis of source code without running it.
- [Dynamic Application Security Testing (DAST)](testing/dynamic-application-security-testing.md): Black-box testing of a running application.
- [Software Composition Analysis (SCA)](testing/software-composition-analysis.md): Finding known-vulnerable open-source and third-party components.

### Supply chain

Software supply chain integrity.

Entry point: [supply-chain](supply-chain/README.md).

- [Supply-chain Levels for Software Artifacts (SLSA)](supply-chain/slsa.md): Supply-chain Levels for Software Artifacts: a framework for build integrity.

## Planned topics

These topics are not written yet. They are listed so the scope of the area is visible.

- Secure coding practices
- Injection flaws
- API security
- Content Security Policy
- Secrets management in code
- Secure SDLC

Back to the [table of contents](../../ToC.md).
