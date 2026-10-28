# Certified Information Systems Security Professional (CISSP)

## Summary

The CISSP is a professional certification issued by ISC2 for people who design, engineer and manage the security of an organization. It combines an adaptive exam over eight knowledge domains with a work experience requirement, so passing the exam alone does not make someone a CISSP. It is a broad, vendor-neutral and management-oriented credential. It says that a person has seen enough of the field to make sound decisions across domains. It does not say that the person is an expert in any single technology.

## Prerequisites

- [ISC2](isc2.md) for the organization that issues the credential.
- [CISSP security domains](cissp-security-domains.md) for the content of the exam.

## Core concepts

### Definition

The *Certified Information Systems Security Professional* is a credential from ISC2. ISC2 describes it as validating "deep technical and managerial knowledge and experience to effectively design, engineer, and manage the overall security posture of an organization" (ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024). The credential has three parts that must all be satisfied: passing the exam, meeting the experience requirement and agreeing to the ISC2 Code of Ethics. After certification, holders must maintain it through continuing professional education.

ISC2 states that the CISSP was the first information security credential to meet the requirements of ANSI/ISO/IEC Standard 17024, the international standard for bodies that certify persons.

### Analogy

Compare it to a driving licence with a theory test and a logbook of supervised hours. The theory test (the exam) shows that you know the rules and can reason about unfamiliar situations. The logbook (the experience requirement) shows that you have driven. Neither says that you can race. The analogy breaks in one place: a driving licence is a legal permission, while the CISSP is a private credential that employers, and in some jurisdictions procurement rules, choose to recognize.

### Why it exists

Security work spans technology, process and law, and employers could not compare candidates by degree titles alone. A common outline of the field, tested in a standard way and tied to years of practice, gives hiring managers and contracting parties a shared reference. ISC2 keeps the outline current by running a Job Task Analysis at regular intervals, a survey of tasks that practicing professionals perform. The results change the exam.

### Exam format (outline of April 15, 2024)

Checked against the *CISSP Certification Exam Outline*, 2026-10.

| Item | Value |
| --- | --- |
| Test style | Computerized adaptive testing (CAT) for English, German, Spanish (Modern), Japanese and Simplified Chinese |
| Length | 3 hours |
| Number of items | 100 to 150 |
| Item format | Multiple choice and advanced innovative items |
| Passing grade | 700 out of 1000 points |
| Languages | Chinese, English, German, Japanese, Spanish |
| Delivery | Pearson VUE testing centers (ISC2 authorized PPC and PVTC select) |

*Computerized adaptive testing* means the next item is chosen from the candidate's earlier answers, so the number of items varies. The exam ends when the system is statistically confident about the result, or at the item or time limit. Because of this, two candidates do not see the same exam, and a long exam is not necessarily a sign of failing. I did not verify the details of the scoring algorithm. ISC2 does not publish it in the outline.

The domain weights are in [CISSP security domains](cissp-security-domains.md#the-eight-domains-and-their-weights).

### Experience requirement

From the outline and the ISC2 experience requirements page (checked 2026-10):

- A candidate needs five years of cumulative, full-time experience in two or more of the eight domains.
- A bachelor's or master's degree in computer science, information technology or a related field can replace up to one year. An additional credential from the ISC2 approved list (the page names CCSP, CISM and SSCP as examples) can also replace up to one year. The outline reads "or", which I interpret as a one year maximum in total. ISC2 should be asked if a case depends on this.
- Part-time work and internships can count.
- A candidate who passes without the experience becomes an *Associate of ISC2* and has six years to earn the required experience.

### Ethics

Strict adherence to the ISC2 Code of Ethics is a condition of certification. The four canons, as worded by ISC2 (checked 2026-10):

1. Protect society, the common good, necessary public trust and confidence, and the infrastructure.
2. Act honorably, honestly, justly, responsibly, and legally.
3. Provide diligent and competent service to principals.
4. Advance and protect the profession.

The order matters. The canons are listed in priority order, and a conflict between serving an employer (canon III) and protecting society (canon I) is resolved in favor of the earlier canon. This is a point the exam tests: the "best" answer is often the one that follows the code, not the one that is fastest or cheapest. I did not find ISC2 text that states the priority rule in those words on the page I read, so treat it as widely taught practice and not as a verified quotation.

### Endorsement and maintenance

ISC2 requires endorsement of the application by a certified professional and continuing professional education (CPE) to keep the credential. I did not verify the number of credits, the cycle length or the annual maintenance fee from a primary ISC2 page during this check.

TODO: record the CPE credits per cycle, the annual minimum and the endorsement process from the ISC2 member pages.

### How the CISSP relates to other credentials

| Credential | Issuer | Relation |
| --- | --- | --- |
| Certified in Cybersecurity (CC) | ISC2 | Entry level, see [ISC2](isc2.md). |
| SSCP | ISC2 | Practitioner level, narrower and more hands-on. |
| CCSP | ISC2 | Cloud specialization. ISC2 lists it as able to replace one year of CISSP experience. |
| CISM | ISACA | Management focused. ISC2 lists it as able to replace one year of CISSP experience. |
| Security+ | CompTIA | Lower level and vendor neutral. Not on the list I read. |
| GIAC certifications | GIAC, SANS | Narrower and technically deeper per topic, see [SANS](../organizations/sans.md). |

The first three rows come from the [ISC2 notes](isc2.md) and the ISC2 experience page. The last rows describe the usual landscape and are not verified against the issuers here.

## Worked example

The experience rule is easy to misapply, so this example encodes it. It uses Python 3.10 and no libraries. The model assumes that the degree and the credential together can waive at most 12 months.

```python
BASE_MONTHS = 60  # five years, full-time, in two or more domains

def required_months(degree=False, credential=False):
    # "up to one year" from a degree OR an approved credential: maximum 12 months in total
    waiver = 12 if (degree or credential) else 0
    return BASE_MONTHS - waiver

cases = [
    ("A: 5 y in domains 3 and 7", 60, False, False),
    ("B: 4 y, bachelor degree", 48, True, False),
    ("C: 4 y, degree and approved credential", 48, True, True),
    ("D: 3 y, degree", 36, True, False),
]
for name, months, degree, credential in cases:
    need = required_months(degree, credential)
    status = ("endorsement path open" if months >= need
              else f"Associate of ISC2 after passing, gap {need - months} months")
    print(f"{name}: need {need} months, have {months} -> {status}")
```

Output:

```text
A: 5 y in domains 3 and 7: need 60 months, have 60 -> endorsement path open
B: 4 y, bachelor degree: need 48 months, have 48 -> endorsement path open
C: 4 y, degree and approved credential: need 48 months, have 48 -> endorsement path open
D: 3 y, degree: need 48 months, have 36 -> Associate of ISC2 after passing, gap 12 months
```

Case C is the one that is easy to get wrong: stacking a degree and a credential does not give two years of waiver under the reading used here. Case D shows the Associate route: the candidate may take the exam, and then has six years to earn the missing 12 months. This script is a model of the published rule, not an eligibility decision. ISC2 decides.

## Trade offs and when to use it

**Value.** The CISSP is a recognized signal for roles that mix security design, risk and management, such as security architect, security manager or consultant. It forces breadth. A practitioner who works in one domain for years learns the other seven in a structured way.

**Costs and limits.**

- Time and money for preparation, the exam, and ongoing fees and CPE. I did not verify current fee amounts.
- It is a breadth credential. An exam answer that picks the best management response is not the same skill as investigating an intrusion.
- Outlines change. The exam changes to a new outline on April 15, 2027 according to ISC2. Study material for 2024 may still be partly valid and partly out of date after that.
- It can be misread by employers as proof of hands-on depth. That is a hiring practice problem, not a property of the credential.

**Alternatives.** Choose a narrower and more technical credential (for example GIAC) when the role is an analyst or penetration tester. Choose CISM when the role is mostly governance and the employer values ISACA. Choose CCSP for a cloud security architecture role. These are common suggestions, not verified rules.

## Common mistakes

- **Thinking passing the exam makes you a CISSP.** Without the experience requirement the result is Associate of ISC2.
- **Studying a single domain deeply and skipping others.** The exam is adaptive over all eight domains, and the outline lists 62 sections.
- **Answering as an engineer.** Many items test the best managerial decision under the Code of Ethics, not the fastest technical fix.
- **Studying from an old outline.** Check the effective date of the outline behind any book or course.
- **Relying on this note for fees and CPE.** Those numbers are marked unverified here.

## Practice

1. A candidate has 4 years of experience in Domain 5 only. Do they meet the experience requirement if they hold a relevant degree?
2. What is the difference between a CAT exam and a fixed-form exam, and why does the number of items vary?
3. A manager asks you to hide a breach from customers. Which canon applies first, and why?
4. Why does a vendor-neutral credential matter for an architect who works with several cloud providers?

**Answers and hints**

1. No. The requirement is experience in two or more domains. The degree waives at most one year, and the remaining 48 months are in one domain only.
2. A CAT picks items from the candidate's earlier answers and can stop early. A fixed form has the same items for everyone.
3. Canon I (protect society, the common good, public trust) is listed first. Legal obligations to notify also apply, see [privacy regulations](../../privacy-regulations/README.md).
4. The knowledge is portable across vendors. It also means the credential does not teach any product.

## Further reading

- ISC2, *CISSP Certification Exam Outline*, effective April 15, 2024 ([PDF](https://edge.sitecorecloud.io/internationf173-xmc4e73-prodbc0f-9660/media/Project/ISC2/Main/Media/documents/exam-outlines/CISSP-Exam-Outline-April-2024-English.pdf)): exam format, weights, experience rule and sections.
- ISC2, [CISSP certification](https://www.isc2.org/certifications/cissp): current status, including the new outline effective April 15, 2027.
- ISC2, [CISSP experience requirements](https://www.isc2.org/certifications/cissp/cissp-experience-requirements): the rules behind the worked example.
- ISC2, [Code of Ethics](https://www.isc2.org/ethics): the preamble and four canons.
