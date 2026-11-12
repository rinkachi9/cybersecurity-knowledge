# Web application firewalls

## Summary

A web application firewall (WAF) inspects HTTP and HTTPS traffic to a web application and blocks requests that match attack patterns or violate policy, such as SQL injection, cross-site scripting and known exploit attempts. Unlike a network firewall, which decides on addresses and ports, a WAF understands the application protocol and the structure of requests, so it defends at layer 7. It is a valuable layer in [defense in depth](../../../security-architecture-and-engineering/design-principles/defense-in-depth.md) for web applications and a standard way to apply virtual patching while real fixes are developed, but it is not a substitute for secure code: a WAF reduces exposure, it does not remove vulnerabilities.

## Prerequisites

- [Firewalls](firewalls.md): the network-firewall contrast.
- [OWASP Top 10](../../../software-development-security/application-security/owasp/owasp-top-10.md) and [XSS](../../../software-development-security/application-security/vulnerabilities/cross-site-scripting/README.md): the attacks a WAF targets.
- [TLS in network security](../secure-transport/tls-in-network-security.md): a WAF must see decrypted traffic.

## Core concepts

### Definition

A *web application firewall* is a security control that inspects the content of HTTP(S) requests and responses to a web application and enforces rules to block malicious or policy-violating traffic. It typically runs as a reverse proxy in front of the application, as a cloud service, or as a module in the web server.

### Analogy

A network firewall is a guard who checks each visitor's ID and which floor they are going to (address and port). A WAF is a guard who also reads the actual forms visitors fill in and refuses any form containing a hidden instruction to the filing clerk, such as "and also hand over every other file" (an injection). The WAF guard understands the language of the forms, not just who is entering.

The analogy holds well; it breaks in that attackers constantly rephrase the hidden instruction to evade the guard's pattern list, and a determined, novel phrasing can slip through, which is why the WAF is a layer, not the whole defense.

### How a WAF decides

WAFs use two complementary models:

- *Negative model (blocklist / signatures)*: block requests matching known attack patterns (SQL injection strings, XSS payloads, known exploit signatures). Easy to deploy, but misses novel or obfuscated attacks and can be evaded.
- *Positive model (allowlist)*: define what valid requests look like (expected parameters, types, lengths) and block anything else. Stronger but requires knowing the application well and more tuning.

Mature WAFs combine both, often with scoring (a request accumulates an anomaly score and is blocked past a threshold), as in the widely used OWASP Core Rule Set for ModSecurity-compatible WAFs.

### What a WAF defends against

- Injection attacks (SQLi, command injection) and cross-site scripting, the staples of the [OWASP Top 10](../../../software-development-security/application-security/owasp/owasp-top-10.md).
- Known exploit attempts against web frameworks and plugins (signatures for specific CVEs).
- Automated abuse: scraping, credential stuffing, some bot traffic (often with rate limiting).
- Protocol anomalies and malformed requests.

### Virtual patching

A particularly valuable use is *virtual patching*: when a vulnerability is discovered in the application but a code fix will take time to develop, test and deploy, a WAF rule can block the specific exploit pattern immediately, reducing exposure during the window. This is mitigation, not remediation, the vulnerability still exists, but it buys time and is sometimes the only fast option for third-party or legacy applications that cannot be changed quickly.

### Limits

- **Not a substitute for secure code.** A WAF reduces the chance a given attack reaches the flaw; it does not fix the flaw. Relying on it instead of fixing vulnerabilities is a common and dangerous mistake.
- **Evasion.** Attackers obfuscate payloads (encoding, case, comments, fragmentation) to bypass signatures; the positive model and good tuning help but nothing catches everything.
- **False positives.** Aggressive rules block legitimate requests, so WAFs need tuning per application and a monitor-only phase first.
- **Needs decrypted traffic.** A WAF must see plaintext HTTP, so it sits where TLS is terminated (often a reverse proxy or the CDN), inheriting the termination considerations from [TLS in network security](../secure-transport/tls-in-network-security.md).
- **Layer 7 only.** It does not defend non-web services; those need their own controls.

## Worked example

An e-commerce site runs a WAF in front of its application:

1. **Blocking a live attack.** A scanner sends `GET /product?id=1' OR '1'='1` attempting SQL injection. The WAF's rules match the injection pattern, block the request with a 403, and log it with the source and payload. The application never sees it.
2. **Virtual patching.** A critical vulnerability is announced in a plugin the site uses, exploited by a specific request pattern. A code fix will take a week. The team deploys a WAF rule that blocks that exact pattern within an hour, closing the exposure window while the real fix is prepared and tested.
3. **Tuning for false positives.** A legitimate product-search feature uses characters the WAF's SQLi rules flag, causing false blocks. The team runs the rule in monitor-only mode, observes the false positives, and adjusts the rule's scope for that endpoint rather than disabling it globally.
4. **The limit.** A novel, heavily obfuscated injection bypasses the signatures and reaches the application; because the application also uses parameterized queries ([the real fix](../../../software-development-security/application-security/owasp/owasp-top-10.md)), the injection fails anyway. The WAF reduced exposure; secure code was the actual defense.

The example shows the right posture: the WAF is a strong, fast-acting layer and a virtual-patching tool, backed by, not replacing, secure development.

## Trade offs and when to use it

- **Defense in depth vs false confidence.** A WAF meaningfully reduces exposure and buys time, but treating it as a reason not to fix code is how breaches happen behind WAFs. Use it as a layer.
- **Negative vs positive model.** Signatures are easy but evadable; allowlisting is stronger but labor-intensive. Combine, with anomaly scoring.
- **Cloud WAF vs on-premises/module.** Cloud WAFs (often bundled with CDN and DDoS protection) scale and absorb volume; on-premises or module WAFs keep traffic local. Choose by architecture and where TLS terminates.
- **Tuning cost.** WAFs require per-application tuning and ongoing rule maintenance; an untuned WAF either blocks legitimate traffic or runs so permissively it adds little.

## Common mistakes

- **Treating the WAF as a reason not to fix vulnerabilities.** The flaw remains and determined attackers evade signatures. Fix: remediate code; use the WAF as a layer and for virtual patching.
- **Deploying in blocking mode without tuning.** False positives break the application. Fix: monitor-only first, tune, then enforce.
- **Relying only on signatures.** Obfuscated and novel attacks pass. Fix: add positive-model rules and anomaly scoring.
- **Placing the WAF where it cannot see decrypted traffic.** It then inspects nothing useful. Fix: deploy at the TLS termination point.
- **Set-and-forget.** Applications and attacks change. Fix: maintain and update rules, review blocked and allowed traffic.

## Practice

1. How does a WAF differ from a network firewall in what it inspects and decides on?
2. What is the difference between the negative and positive security models, and why combine them?
3. What is virtual patching, and why is it mitigation rather than remediation?
4. Why must a WAF be placed where TLS is terminated?
5. Why is relying on a WAF instead of fixing code dangerous?

### Answers

1. A network firewall decides on addresses, ports and connection state (layers 3-4); a WAF inspects the content and structure of HTTP(S) requests and responses (layer 7), so it can recognize application attacks like injection and XSS.
2. The negative model blocks known attack patterns (easy, but misses novel/obfuscated attacks); the positive model allows only requests matching a defined valid shape (stronger, but labor-intensive); combining them, often with anomaly scoring, balances coverage and effort.
3. Blocking a specific exploit pattern with a WAF rule to reduce exposure while a code fix is developed; it is mitigation because the underlying vulnerability still exists and could be reached by a different pattern.
4. A WAF must inspect plaintext HTTP content, so it has to sit where the TLS session is decrypted (a reverse proxy, CDN or the server), otherwise it sees only ciphertext.
5. The vulnerability remains and attackers continually obfuscate payloads to evade WAF signatures, so sooner or later an attack reaches the unfixed flaw; the WAF reduces but does not remove the risk.

## Further reading

- OWASP, Web Application Firewall and the OWASP Core Rule Set: https://owasp.org/www-project-modsecurity-core-rule-set/
- OWASP Top 10, the vulnerability classes WAFs target: https://owasp.org/www-project-top-ten/
- [XSS](../../../software-development-security/application-security/vulnerabilities/cross-site-scripting/README.md) and the application-security area for the real fixes a WAF complements.
- NIST SP 800-41 Rev. 1 for firewall context: https://doi.org/10.6028/NIST.SP.800-41r1
