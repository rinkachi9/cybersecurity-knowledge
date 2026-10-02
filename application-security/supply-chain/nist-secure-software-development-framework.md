# NIST Secure Software Development Framework (SSDF)

## Summary

The NIST Secure Software Development Framework (SSDF, SP 800-218) is a short list of secure development practices that a software producer should perform regardless of its language, methodology or tooling. It groups 19 practices into four areas: prepare the organization, protect the software, produce well-secured software, and respond to vulnerabilities. It became widely known because U.S. Executive Order 14028 (2021) tied software supply chain security to it, so many software suppliers now document SSDF conformance for customers. The SSDF says what outcomes a secure development program needs, and leaves the tools and methods to you.

Checked against NIST SP 800-218 version 1.1 (February 2022), the NIST SSDF project and SP 800-218A publication pages, 2026-10. A draft revision (version 1.2) is reported by secondary sources and was not verified.

## Prerequisites

- [SLSA](slsa.md): build integrity levels for the supply chain.
- [OWASP security principles](../owasp/owasp-security-principles.md) and [OWASP](../owasp/owasp.md): the principles and verification standards the SSDF practices point to.
- [Software composition analysis](../testing/software-composition-analysis.md), [static application security testing](../testing/static-application-security-testing.md) and [dynamic application security testing](../testing/dynamic-application-security-testing.md).

## Core concepts

### Definition

SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*, describes "fundamental, sound, and secure recommended practices based on established secure software development practice documents". It is a **practice framework**: each practice has a name and ID, tasks (actions that may be needed), notional implementation examples and references to other standards. The examples are illustrative, and no example or combination is required.

The SSDF is intended to be added to any software development life cycle model. It does not replace the life cycle, and it helps in three ways that NIST states: reduce the number of vulnerabilities in released software, reduce the potential impact of undetected or unaddressed vulnerabilities, and address root causes to prevent recurrences.

### Analogy

Think of food safety rules in a restaurant kitchen. The rules do not say which stove to buy. They say that staff are trained, raw and cooked food are kept apart, ingredients come from known suppliers, dishes are checked before they leave, and when a customer complains someone finds the cause and fixes the process. The SSDF is the same kind of rule set for a software kitchen.

The analogy breaks in one place. A kitchen inspector can watch a cook at work. Software producers mostly prove conformance through records and artifacts, so evidence design is part of the job.

### Structure: four groups, 19 practices, 42 tasks

| Group | Purpose | Practices |
| --- | --- | --- |
| **PO** Prepare the Organization | People, processes and technology are ready for secure development | PO.1 Define security requirements for software development, PO.2 Implement roles and responsibilities, PO.3 Implement supporting toolchains, PO.4 Define and use criteria for software security checks, PO.5 Implement and maintain secure environments for software development |
| **PS** Protect the Software | Protect all components of the software from tampering and unauthorized access | PS.1 Protect all forms of code from unauthorized access and tampering, PS.2 Provide a mechanism for verifying software release integrity, PS.3 Archive and protect each software release |
| **PW** Produce Well-Secured Software | Releases have minimal security vulnerabilities | PW.1 Design software to meet security requirements and mitigate security risks, PW.2 Review the software design, PW.4 Reuse existing, well-secured software when feasible, PW.5 Create source code by adhering to secure coding practices, PW.6 Configure compilation, interpreter and build processes to improve executable security, PW.7 Review and/or analyze human-readable code, PW.8 Test executable code, PW.9 Configure software to have secure settings by default |
| **RV** Respond to Vulnerabilities | Identify residual vulnerabilities and respond, and prevent similar ones | RV.1 Identify and confirm vulnerabilities on an ongoing basis, RV.2 Assess, prioritize and remediate vulnerabilities, RV.3 Analyze vulnerabilities to identify their root causes |

The practice count (19) and task count (42) were derived from the SP 800-218 text. Identifier PW.3 (verify third-party software complies with security requirements) was moved, and its task is now PO.1.3, and some tasks under PW.4 and PW.5 were moved into other tasks. The document keeps the old identifiers with a "Moved to" note.

### All tasks

Task wording is NIST's (shortened). Moved tasks are omitted.

| Task | Action |
| --- | --- |
| PO.1.1 | Identify and document security requirements for development infrastructures and processes, and maintain them |
| PO.1.2 | Identify and document security requirements for the software the organization develops |
| PO.1.3 | Communicate requirements to third parties who provide commercial components for reuse |
| PO.2.1 | Create roles and alter responsibilities to cover all parts of the SDLC |
| PO.2.2 | Provide role-based training and review proficiency |
| PO.2.3 | Obtain upper management or authorizing official commitment and convey it |
| PO.3.1 | Specify which tools or tool types each toolchain must include and how they integrate |
| PO.3.2 | Follow recommended security practices to deploy, operate and maintain tools |
| PO.3.3 | Configure tools to generate artifacts that show support of secure development practices |
| PO.4.1 | Define criteria for software security checks and track them through the SDLC |
| PO.4.2 | Gather and safeguard the information that supports the criteria |
| PO.5.1 | Separate and protect each environment involved in development |
| PO.5.2 | Secure and harden development endpoints using a risk-based approach |
| PS.1.1 | Store all forms of code under least privilege so only authorized personnel can change it |
| PS.2.1 | Make software integrity verification information available to acquirers |
| PS.3.1 | Securely archive the files and supporting data kept for each release |
| PS.3.2 | Collect, safeguard, maintain and share provenance data for all components of each release (for example in an SBOM) |
| PW.1.1 | Use risk modeling such as threat modeling, attack modeling or attack surface mapping |
| PW.1.2 | Track and maintain security requirements, risks and design decisions |
| PW.1.3 | Build in support for standardized security features and services |
| PW.2.1 | Have a qualified reviewer not involved in the design, or automated processes, review the design against requirements |
| PW.4.1 | Acquire and maintain well-secured third-party components |
| PW.4.2 | Create and maintain well-secured components in-house for common needs |
| PW.4.4 | Verify that acquired components comply with the organization's requirements throughout their life cycles |
| PW.5.1 | Follow secure coding practices appropriate to the language and environment |
| PW.6.1 | Use compiler, interpreter and build tools that offer features to improve executable security |
| PW.6.2 | Decide which features to use and implement approved configurations |
| PW.7.1 | Decide whether code review and/or code analysis is needed and which types |
| PW.7.2 | Perform the review or analysis against secure coding standards, record and triage findings |
| PW.8.1 | Decide whether executable code testing is needed, and which types |
| PW.8.2 | Scope, design, perform and document the testing, and triage issues |
| PW.9.1 | Define a secure baseline so default settings are secure |
| PW.9.2 | Implement the defaults and document each setting for administrators |
| RV.1.1 | Gather information on potential vulnerabilities in the software and its components from acquirers, users and public sources |
| RV.1.2 | Review, analyze and/or test code to find previously undetected vulnerabilities |
| RV.1.3 | Have a vulnerability disclosure and remediation policy with roles and processes |
| RV.2.1 | Analyze each vulnerability to gather risk information |
| RV.2.2 | Plan and implement risk responses |
| RV.3.1 | Analyze identified vulnerabilities for root causes |
| RV.3.2 | Analyze root causes over time to find patterns |
| RV.3.3 | Look for similar vulnerabilities to eradicate a class of vulnerability proactively |
| RV.3.4 | Review the SDLC process and update it to prevent recurrence |

Notice the pattern. PO sets up the system (requirements, roles, tools, criteria), PW is where code is designed, written and tested, PS protects the result, and RV closes the loop through root cause analysis (RV.3.3 and RV.3.4 are the "fix the class, not the instance" tasks, comparable to the fail-secure thinking in [OWASP security principles](../owasp/owasp-security-principles.md)).

### The SSDF and Executive Order 14028

Executive Order 14028, *Improving the Nation's Cybersecurity*, was issued on 2021-05-12. Section 4 directed NIST to solicit input and identify standards, tools and best practices to enhance software supply chain security. SP 800-218 includes a table that maps the subsections of Section 4e of the order to SSDF practices and tasks, and states that NIST also published guidance on how producers and acquirers can communicate about attestation of conformance with EO 14028 Section 4e. The details of current U.S. procurement requirements (for example attestation forms) change with policy, and are not covered here, so check the current policy source.

### Companion and related documents

- **SP 800-218A** (July 2024), *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile*. It augments SP 800-218 with practices, tasks, recommendations and considerations specific to AI model development.
- **SSDF version 1.2.** Secondary sources report an initial public draft (SP 800-218 Revision 1) in December 2025. I did not confirm this from a NIST page, so treat it as unverified.
- **SP 800-161** covers supply chain risk management at the organization level (see the [NIST overview](../../governance-and-compliance/frameworks/nist-frameworks-overview.md)).
- The task text in SP 800-218 carries references to NICE Framework task and knowledge IDs, to SP 800-161, to OWASP, and to other standards.

### How the SSDF relates to other frameworks

| Framework | Relationship |
| --- | --- |
| [NIST CSF 2.0](../../governance-and-compliance/frameworks/nist-cybersecurity-framework.md) | Outcome `PR.PS-06` (secure software development practices integrated and monitored through the SDLC) is the natural CSF anchor for the SSDF. `GV.SC` covers suppliers, and `ID.RA-09` covers assessing the authenticity and integrity of software before acquisition |
| [SP 800-53](../../governance-and-compliance/frameworks/nist-sp-800-53/README.md) | The SA family (system and services acquisition) and SR (supply chain) carry the control form. SA-15 (development process), SA-24 (design for cyber resiliency, added in release 5.2.0) |
| [OWASP SAMM and ASVS](../owasp/owasp.md) | SAMM measures maturity of the same practices. ASVS gives verification requirements for PW.7, PW.8 |
| [SLSA](slsa.md) | Gives graded build integrity levels that support PS.1, PS.2 and PS.3 |
| CycloneDX and Dependency-Track (OWASP) | Provide SBOM format and tooling for PS.3.2 and RV.1.1 |

The SSDF text itself lists, among its references, OWASP's Software Component Verification Standard and the NIST supply chain document, according to the SSDF project page change notes. The mapping of PW.7 and PW.8 to ASVS and WSTG above is this note's suggestion.

## Worked example

The scenario: Example Corp (`example.com`) ships a small service and wants to show PS.2.1 (integrity verification information for acquirers) and PS.3.2 (provenance data, as an SBOM) in its release process. This is a toy lab with synthetic components. Tested with Python 3.10.12, standard library only.

```python
# Illustrates SSDF PS.2.1 (integrity verification info) and PS.3.2 (provenance data, SBOM).
import hashlib
import json
import pathlib
import tarfile

root = pathlib.Path("app")
root.mkdir(exist_ok=True)
(root / "main.py").write_text("print('hello from example.com service')\n")

# 1. Build the release artifact. Tar header fields are fixed so the digest is reproducible.
with tarfile.open("release-1.0.0.tar", "w", format=tarfile.PAX_FORMAT) as tar:
    info = tar.gettarinfo(str(root / "main.py"), arcname="app/main.py")
    info.mtime, info.uid, info.gid, info.uname, info.gname = 0, 0, 0, "", ""
    with open(root / "main.py", "rb") as f:
        tar.addfile(info, f)

digest = hashlib.sha256(pathlib.Path("release-1.0.0.tar").read_bytes()).hexdigest()

# 2. Minimal CycloneDX 1.5 SBOM for the release (PS.3.2): what it is made of.
sbom = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "version": 1,
    "metadata": {"component": {"type": "application", "name": "example-service", "version": "1.0.0"}},
    "components": [
        {"type": "library", "name": "requests", "version": "2.32.3", "purl": "pkg:pypi/requests@2.32.3"},
        {"type": "library", "name": "urllib3", "version": "2.2.3", "purl": "pkg:pypi/urllib3@2.2.3"},
    ],
}
pathlib.Path("sbom.cdx.json").write_text(json.dumps(sbom, indent=2) + "\n")

# 3. Publish the checksum next to the release (PS.2.1), then verify like an acquirer would.
pathlib.Path("release-1.0.0.tar.sha256").write_text(f"{digest}  release-1.0.0.tar\n")
published = pathlib.Path("release-1.0.0.tar.sha256").read_text().split()[0]
actual = hashlib.sha256(pathlib.Path("release-1.0.0.tar").read_bytes()).hexdigest()
print("sha256:", actual)
print("verification:", "OK" if published == actual else "MISMATCH")
print("components in SBOM:", [c["purl"] for c in json.loads(pathlib.Path("sbom.cdx.json").read_text())["components"]])

# 4. Tamper with the artifact and verify again.
data = bytearray(pathlib.Path("release-1.0.0.tar").read_bytes())
data[100] ^= 1
pathlib.Path("release-1.0.0.tar").write_bytes(bytes(data))
tampered = hashlib.sha256(pathlib.Path("release-1.0.0.tar").read_bytes()).hexdigest()
print("after tampering:", "OK" if published == tampered else "MISMATCH")
```

Output:

```text
sha256: f9d3718a69c632b21ea37e6d775d37eb1ef3070d75bdbdbe8d01cb1baa7e9e6d
verification: OK
components in SBOM: ['pkg:pypi/requests@2.32.3', 'pkg:pypi/urllib3@2.2.3']
after tampering: MISMATCH
```

What the example shows, and what it leaves out:

1. **PS.2.1** is met only in the weak sense that a checksum exists. As the [CIA triad](../../foundations/cia-triad/README.md) note explains, a checksum stored next to the artifact on the same server does not protect against an attacker who can replace both. In practice, publish the digest or a digital signature through a separate trusted channel, and sign with a key held in a protected signing service. SLSA provenance goes further by attesting how the artifact was built.
2. **PS.3.2** needs the SBOM to be generated from the real build, not written by hand as in this toy. Use a build-integrated generator (CycloneDX tools) and keep the SBOM with the archived release (PS.3.1).
3. **RV.1.1** is where the SBOM pays off. When a new vulnerability is published, you can query which releases contain the affected component (for example with Dependency-Track), instead of searching code by hand.
4. The tar is fixed so the digest is the same on repeated runs on this machine. The digest can differ with other Python versions because tar header details can differ.
5. The SSDF also expects the surrounding practices. Who may change the code (PS.1.1, least privilege), who reviewed it (PW.2.1, PW.7.2), and which tests ran (PW.8.2) are evidence an acquirer may ask for.

### An evidence plan

A conformance attestation is only as good as the records behind it. A simple evidence table for a small team (this note's suggestion):

| Practice | Evidence artifact | Where it lives |
| --- | --- | --- |
| PO.1, PO.2 | Secure development standard, role matrix, training records | Policy repository, learning system |
| PO.3, PO.4 | Toolchain definition, quality gate definitions, gate results | CI configuration and build logs |
| PO.5 | Environment separation diagram, endpoint hardening baseline | Architecture docs, endpoint management |
| PS.1 | Branch protection settings, access reviews | Source host settings export |
| PS.2, PS.3 | Signed release, checksum, SBOM, provenance | Release repository |
| PW.1, PW.2 | Threat models, design review records | Wiki, ticket system |
| PW.4 | Approved component list, dependency policy | Package manager config |
| PW.5 to PW.8 | Coding standard, review and scan reports, test reports | CI artifacts |
| PW.9 | Secure default configuration documentation | Product documentation |
| RV.1 to RV.3 | Disclosure policy, vulnerability tracker, root cause reports | Security site, tracker |

## Trade offs and when to use it

### Benefits

- Small, readable and language-neutral, so teams can map it onto existing methods (agile, DevOps).
- Widely recognized by customers, especially in U.S. government supply chains.
- Practices map to common tooling: SAST, DAST, SCA, SBOM, signing.
- The community profile approach (SP 800-218A) shows it can be extended to new domains.

### Costs and limits

- **Evidence burden.** Attestation requires records for each practice. Without a plan the effort lands on engineers late.
- **Outcome-level wording.** "Follow secure coding practices" needs a coding standard behind it, and a reviewer may ask for it.
- **No grading.** Unlike SLSA levels or SAMM maturity scores, the SSDF has no levels. You either perform a practice or you do not, to the extent your risk assessment requires.
- **Version drift.** A revision is in progress according to secondary sources. Track the current text.
- **U.S. policy dependence.** Attestation requirements stem from U.S. federal procurement policy. Other markets use other schemes.

### Alternatives and companions

| Need | Use |
| --- | --- |
| Maturity measurement | OWASP SAMM, BSIMM (the SSDF text lists BSIMM among related sources) |
| Graded build integrity | [SLSA](slsa.md) |
| Technical verification requirements | OWASP ASVS and the testing guide |
| Certifiable management system | [ISO/IEC 27001](../../governance-and-compliance/standards/iso-iec-27001.md) |

## Common mistakes

| Mistake | Why it is wrong | Fix |
| --- | --- | --- |
| Treating the SSDF as a tool checklist | The SSDF is practice-based and the examples are notional | Pick tools to fit risk, record why |
| Attesting without evidence | A claim with no records cannot be defended | Keep an evidence table per practice |
| Storing the checksum next to the artifact only | Provides no protection against tampering of both | Sign releases or publish digests through a separate channel |
| Skipping RV.3 root cause analysis | The same class of flaw returns | Review the SDLC after each significant vulnerability (RV.3.4) |
| Ignoring development infrastructure | Build systems and developer endpoints are targets (PO.5) | Separate and harden environments, and protect build credentials |
| Handwritten SBOMs | They go stale and miss transitive components | Generate SBOMs in the build |
| Assuming third-party code is covered | PW.4 and PO.1.3 apply to acquired components | Verify components and communicate requirements to suppliers |
| Citing "PW.3" in a version 1.1 assessment | PW.3 was moved to PO.1.3 | Use current task identifiers |

## Practice

1. Name the four SSDF groups and one practice from each.
2. Which task covers providing integrity verification information to acquirers, and which covers SBOMs?
3. Your CI deploys with a shared admin token that every developer knows. Which SSDF practices does this affect?
4. Explain why RV.3.3 asks teams to look for similar vulnerabilities.
5. What is an SSDF community profile, and what does SP 800-218A add?
6. Which CSF 2.0 outcome would you cite for SSDF in a Target Profile?

Hints and answers:

1. PO: PO.1 requirements. PS: PS.2 release integrity. PW: PW.8 test executable code. RV: RV.2 assess, prioritize and remediate vulnerabilities.
2. PS.2.1 and PS.3.2 (provenance data, for example an SBOM).
3. PS.1.1 (least privilege for access to code), PO.5.1 and PO.5.2 (protect environments and endpoints), and PO.3.2 (secure deployment of tools).
4. A vulnerability is usually an instance of a pattern. Fixing one instance leaves the class, so the task asks to proactively find and fix similar ones rather than wait for reports.
5. A community profile adds practices, tasks and recommendations for a specific use. SP 800-218A adds them for generative AI and dual-use foundation model development.
6. PR.PS-06 (secure software development practices are integrated and their performance is monitored throughout the software development life cycle), plus GV.SC outcomes for suppliers.

## Further reading

- NIST, SP 800-218, Secure Software Development Framework (SSDF) Version 1.1 (February 2022). The primary source for the groups, practices, tasks and the EO 14028 mapping: https://doi.org/10.6028/NIST.SP.800-218
- NIST, SP 800-218A, Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile (July 2024): https://csrc.nist.gov/pubs/sp/800/218/a/final
- NIST, Secure Software Development Framework project page, with updates and the revision history: https://csrc.nist.gov/projects/ssdf
- Executive Order 14028, Improving the Nation's Cybersecurity (2021-05-12). The policy context. Referenced in SP 800-218, not read in full for this note.
- OWASP CycloneDX, the SBOM standard used in the example: https://owasp.org/www-project-cyclonedx/.
