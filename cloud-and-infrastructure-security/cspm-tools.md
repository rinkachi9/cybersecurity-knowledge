# CSPM tools: Prisma Cloud, CrowdStrike Falcon Cloud Security, Orca, Check Point CloudGuard and Netskope

## Summary

Cloud security posture management is sold today mostly as one module of a larger platform called a CNAPP (cloud-native application protection platform). This note describes how five such products implement the CSPM part, based on their own documentation, and gives a method to compare them without trusting anyone's feature matrix, including mine. The five products share the same core: they connect to cloud accounts with a role, collect configuration through provider APIs, evaluate rules and benchmarks, rank findings with context and push them to a workflow. They differ in rule language, how "agentless" is achieved, how remediation is performed, which clouds and standards they cover, and how they are priced. Those differences decide fit, and none of them can be judged from a brochure.

Checked against vendor documentation and pages fetched in 2026-10: docs.prismacloud.io and a Palo Alto Networks press release (2025-02-13), CrowdStrike product and blog pages, the Orca SideScanning technical brief (2024 edition), Check Point CloudGuard documentation and docs.netskope.com. I did not install or run any of the products. Marketing claims (return on investment figures, "only", "first") are not repeated. Product names change often, and several already did.

## Prerequisites

- [Cloud security posture management](cloud-security-posture-management.md): the mechanism that every product below implements.
- [Multicloud CSPM](multicloud-cspm.md): normalization, connectors and operating model across clouds.
- [Security posture management](security-posture-management.md) for the terms CIEM, CWPP, DSPM and CNAPP.

## Core concepts

### How to read this note

Each product section follows the same template: what the vendor says it is, how its CSPM works according to the documentation, what is documented about rules, remediation and coverage, what is documented as a limit, and what I could not verify. The comparison matrix after the sections uses only documented statements. An empty cell means "not verified", not "not supported".

### Names and lineage

| Product | Current naming in the sources | Note |
| --- | --- | --- |
| Palo Alto Networks | Prisma Cloud (documentation site still named Prisma Cloud) and Cortex Cloud | The press release of 2025-02-13 describes Cortex Cloud as "the next version of Prisma Cloud", bringing together cloud detection and response and CNAPP on the Cortex platform. Documentation for Cortex Cloud has a "Cloud Posture Security" area that includes CSPM. Secondary sources describe a migration of existing customers during 2025. Check which edition and documentation set applies to your contract |
| CrowdStrike | Falcon Cloud Security | The CSPM capability was documented earlier under the name Falcon Horizon (a 2020 datasheet), and CrowdStrike's current pages present CSPM as one module of Falcon Cloud Security |
| Orca Security | Orca Cloud Security Platform | Technical brief 2024 edition |
| Check Point | CloudGuard (CNAPP). The documentation URLs still contain "Dome9", the name of the posture management product that Check Point acquired (the acquisition is from my memory and was not checked) | CSPM, CSNS and CWPP are named as the three core capabilities |
| Netskope | Netskope Public Cloud Security (CSPM is a service in it). The platform is marketed under the Netskope One name | Netskope also has SaaS security posture management (SSPM) under the same umbrella |

### What "agentless" means

This word hides three different things, and the difference changes your risk review.

| Meaning | How it works | Example in the documentation | What is deployed in your account |
| --- | --- | --- | --- |
| API-based | The tool calls provider APIs with a read role and reads configuration and metadata | CSPM in every product here. Check Point: Posture Management "accesses your environments directly through cloud platform APIs" | A role, and optionally event or log subscriptions |
| Snapshot-based workload scanning | The tool snapshots disks and scans the copy outside the workload | Prisma Cloud agentless scanning creates snapshots of each host, creates scanner instances and networking in each region, scans, reports and cleans up, by default every 24 hours. Orca SideScanning "reads workloads through the cloud providers' shared storage" using snapshots of block storage | Roles with snapshot permissions. In Prisma Cloud's model also temporary scanner instances and network resources in your account (unless you provide the network yourself). Orca offers a SaaS mode and an in-account mode |
| Agent-based runtime | A sensor runs on the workload | Falcon Cloud Security: agent-based runtime protection together with agentless visibility. Prisma Cloud: Defenders | An agent on the host |

For a pure CSPM purpose, the first row is what you need. The second row adds vulnerability and secrets visibility inside workloads. The third is outside the CSPM scope but is part of the platform.

### Product: Palo Alto Networks Prisma Cloud and Cortex Cloud

**What the vendor says it is.** Prisma Cloud is a cloud native application protection platform. Its documentation says it is available as a SaaS edition (Prisma Cloud Enterprise Edition) and a self-hosted edition (Prisma Cloud Compute Edition), and that usage is measured in Credits, a universal capacity unit consumed by product features. It starts from a "Cloud Security Foundations" feature set with agentless visibility and compliance across code, build, deploy and runtime, with threat and misconfiguration detection for IaaS and PaaS, compliance management, workload vulnerability scanning, IaC misconfiguration detection and least-privileged access enforcement. Cortex Cloud is the next version of the platform, merging CNAPP with cloud detection and response.

**How CSPM works.**

- **Onboarding.** Cloud accounts are connected by roles. For AWS, the onboarding workflow generates a CloudFormation template whose permissions follow the capabilities you select: Misconfigurations (scan assets, ingest metadata), Identity Security (net effective permissions), Agentless Workload Scanning, Threat Detection (DNS, network and identity threats), Serverless Function Scanning, and Agent-Based Workload Protection. The trust policy uses an external ID. Optional remediation grants the role read-write access. Prisma Cloud publishes the list of APIs it ingests per cloud (AWS, Azure, GCP, Oracle Cloud Infrastructure and Alibaba Cloud have onboarding documentation).
- **Policies.** Custom policy types are Attack Path, Audit Event, Config, Data, IAM and Network. Config policies have two subtypes. **Run** policies scan deployed resources and use RQL (Resource Query Language). **Build** policies scan IaC templates and repositories and use a JSON query instead of RQL. Build policies do not support remediation by CLI or UI.
- **RQL.** A Config query takes the shape `config from cloud.resource where ...` with at least `api.name` combined with `json.rule`, or a completion attribute, or two `api.name` attributes with a `filter`. Documented example: `config from cloud.resource where cloud.type = 'azure' AND api.name = 'azure-network-usage' AND json.rule = StaticPublicIPAddresses.currentValue greater than 1`. The documentation recommends not including `cloud.account`, `cloud.accountgroup`, `cloud.region`, `resource.status` or tag attributes in a custom policy query, because they are ignored there.
- **Attack path policies.** They are out-of-the-box and enabled by default. They correlate overly permissive identities, permissions, network exposure, misconfiguration and vulnerabilities. The documentation's example is a VM that is network-exploitable, internet-exposed and has permissive access to sensitive data, and an alert is generated when all rules of an attack path policy match. Some attack path policies require the IAM Security (CIEM) subscription.
- **Compliance.** Built-in standards are listed per cloud: for example CIS benchmarks of several versions, CSA CCM v3.0.1 and v4.0.1, GDPR, HIPAA, HITRUST, ISO 27001:2013, MITRE ATT&CK, NIST 800-53 Rev. 4 and 5 and NIST CSF v1.1 (the list differs per cloud). A custom compliance standard can be created. The documentation states that compliance standards only show results for resources matching the policies in the standard, unlike the asset inventory.
- **Remediation.** Config Run policies can carry CLI remediation commands, and auto-remediation requires write access to the cloud platform.
- **Agentless workload scanning.** Described above, for AWS, Azure, GCP and OCI. Documented limit: Azure virtual machines with Trusted Launch enabled are not supported in agentless mode.

**What I could not verify.** Real detection coverage and false positive rates, the latency from change to finding, the current edition mapping between Prisma Cloud and Cortex Cloud for a given customer, and the pricing in Credits per feature set (the documentation says each feature set needs a specific number of Credits and that Credits are sold in 100 unit increments).

### Product: CrowdStrike Falcon Cloud Security

**What the vendor says it is.** A CNAPP combining agent-based runtime protection, agentless visibility and threat intelligence. Its product page lists these modules: CSPM, cloud workload protection, cloud detection and response (CDR), CIEM, container and Kubernetes security, application security posture management (ASPM), IaC scanning, AI security posture management and DSPM.

**How CSPM works.**

- **Two kinds of detection policy.** CrowdStrike documents indicators of attack (IOAs), behavior-based detections such as an action taken by a user, and indicators of misconfiguration (IOMs), detections based on static configuration settings. This split is the cleanest statement in the sources of the difference between detection and posture.
- **Example policies.** In a 2022 blog post about Azure Blob Storage, CrowdStrike lists policies with a type, severity and description. IOMs include "Storage Account blob container configured with public access" (critical), "Storage Account configured to allow access from all networks" (high), and encryption-at-rest checks such as "SQL db has transparent data encryption disabled" (informational). An IOA in the same table, "Storage Account Networking changed to All Networks", fires when a user changes the network rules to default allow. The pair shows state and behavior detections of the same risk.
- **Agentless.** CrowdStrike describes its CSPM as agentless, cloud-native monitoring that "continuously monitors your environment for misconfigurations" and compares configurations to industry and organizational benchmarks. Per the definition above this is API-based collection.
- **Context.** The product page says CSPM detects and remediates misconfigurations "with graph-based context and adversary intelligence". Details of the graph and the intelligence are not given on the pages I read.

**What I could not verify.** The rule language and the ability to write custom rules, the list of supported clouds beyond "all major clouds", the compliance standards list, remediation mechanics, and pricing. The documentation portal of CrowdStrike requires a login, so product documentation was not read.

### Product: Orca Security

**What the vendor says it is.** An agentless cloud security platform, described in the technical brief as the "Orca Cloud Security Platform", for AWS, Azure, Google Cloud, Kubernetes, Oracle Cloud and Alibaba Cloud. Its website lists capabilities including CSPM, workload protection, CIEM, API security, DSPM, vulnerability management and AI security in one platform.

**How CSPM works.**

- **SideScanning.** Orca's technical brief explains the method. Onboarding is a one-time process: create an IAM role and policy that establish trust between your account and Orca's account (for AWS through a CloudFormation template), then paste the ARN into Orca. The role "has a few permissions, the most important being read-only permissions to the block storage layer", and an optional fourth step enables auto remediation with additional resources. Orca creates snapshots of block storage for all machines, scans the snapshots, and tags the snapshots for deletion as soon as scanning completes. It states that these snapshots can only be accessed from your account and that, because the credentials are read-only, scanning cannot change workloads.
- **Deployment modes.** SaaS mode by default, or an in-account mode called Orca Pod.
- **Asset discovery.** From the scanned snapshots Orca enumerates assets such as virtual machines, containers, Kubernetes, serverless functions, cloud storage, databases, VPCs, cryptographic keys, secrets, images, managed services, load balancers, security groups, users, roles, policies and AI models.
- **Control plane and data plane.** Orca analyzes the cloud control plane through provider APIs (configuration, networking, IAM roles, security groups, logs) and the data plane through the workload scan (vulnerabilities, secrets, sensitive data at risk). Both feed a unified data model that also takes in CI/CD scans, authentication data from identity providers, cloud events and audit logs, and network probing for internet-facing assets. The model is what the brief says drives alert prioritization.
- **Handling of sensitive data.** The brief states that sensitive data discovered in an alert, such as PII at risk, is masked before display.

**What I could not verify.** The rule language and custom rules, the standards list, detection latency, how well workloads without block storage visibility (such as some managed services or serverless) are covered, and pricing. The technical brief is a vendor document and makes comparative claims that I did not test.

### Product: Check Point CloudGuard

**What the vendor says it is.** CloudGuard CNAPP is "a SaaS platform that provides unified cloud-native security across your applications, workloads, and network", with Cloud Security Posture Management (CSPM), Cloud Service Network Security (CSNS) and Cloud Workload Protection Platform (CWPP) as core capabilities.

**How CSPM works.**

- **Collection.** Posture Management "accesses your environments directly through cloud platform APIs", and the platform uses notification services such as SNS for AWS. Supported platforms in the documentation are AWS, Azure, GCP, Alibaba Cloud and Kubernetes.
- **Rules in GSL.** Rules use the Governance Specification Language, a user-readable syntax of the form `Target should Condition`, with an optional `where` filter. Documented examples: `SecurityGroup should not have inboundRules contain [port=22 and scope='0.0.0.0/0']`, `Instance should not have launchTime before(-3,'months')`, and `S3Bucket should have logging.enabled=true`. GSL has domain-specific functions for IP networking, cloud entities, strings and time, and a GSL Builder sandbox for writing and testing rules.
- **Rulesets.** Two kinds. CloudGuard-managed rulesets developed by its research team test best practices and standards such as PCI-DSS, HIPAA and CIS Foundations, and cannot be changed. Customer-managed rulesets are clones of managed ones, or your own. CloudGuard-managed rulesets have designated versions since January 2024. Each finding gets one of five severities: Informational, Low, Medium, High, Critical, based on infrastructure exposure, information disclosure and other criteria described in the documentation.
- **Remediation and history.** The documentation lists automatic remediation with CloudBots and assessment history for point-in-time review. It notes that after a remediation is applied the assessment has to be run again to verify it.
- **Pre-deployment.** One use case in the documentation is to analyze a proposed cloud design (a CloudFormation template) before deployment.
- **Other.** The overview mentions threat intelligence, container security with Kubernetes anomaly detection, Terraform and CloudFormation integration, and CIEM for least-privilege entitlements.

**What I could not verify.** The permission model of the connector (the overview page does not say whether access is read-only), detection latency, pricing, and the current relation between the CloudGuard Dome9 naming and the CNAPP product line in your contract.

### Product: Netskope Public Cloud Security (CSPM)

**What the vendor says it is.** CSPM is "a Netskope service that provides an organization insight into the security posture of their public cloud resources". It "utilizes Netskope's API-enabled controls and real-time protection capabilities" to continuously assess deployments for policy violations, monitor compliance with standards (CIS, PCI-DSS, NIST, HIPAA and more) and discover misconfigurations with remediations. The Public Cloud Security documentation lists three components: CSPM, Storage Scan (visibility into DLP violations and malware threats) and Forensics (capture of DLP incident metadata). It supports AWS, Azure and GCP.

**How CSPM works.**

- **Continuous Security Assessment.** You configure each AWS account, Azure tenant and GCP organization for security posture, using multi-account setup (a list of accounts, an AWS CLI generated CSV, and a permission configuration step), then assign administrator roles and set up security assessment policies.
- **Policy, profile, rule.** A security posture policy uses profiles, and a profile holds rules. Netskope documents custom rules written in a domain specific language, and predefined rules per supported IaaS entity. CIS benchmarks such as CIS AWS Foundations and CIS Microsoft Azure Foundations are named as standards to assess against, and you can use your own framework.
- **Results.** The Security Posture page shows raw findings, rules and resources. Rule status is defined per resource: a rule fails if any resource fails, passes if all pass, and is unknown if all are unknown. Findings can be muted. This is a useful definition to check in any tool, since it explains why a "failed rule" count and a "failed resource" count are different numbers.
- **Automation.** The documentation lists REST API endpoints for introspection instances and security assessment violations of the latest scan, and a documentation summary mentions a Cloud Ticket Orchestrator and auto remediation templates.
- **SSPM.** Netskope extends the same posture idea to SaaS applications under SaaS security posture management.

**What I could not verify.** The connector permissions and the use of write access for remediation, the DSL syntax for custom rules, cross-resource context and attack path features (the Public Cloud Security page does not mention workload protection, IaC scanning, CIEM or DSPM modules), and pricing.

### Native services in the comparison

For a fair baseline, any evaluation should include the native tools: AWS Security Hub CSPM (needs AWS Config for most controls, free trial of 30 days, charged by checks and findings, can now monitor Azure too), Microsoft Defender CSPM (free Foundational plan and a paid plan with attack path analysis, risk prioritization, agentless scanning, governance and more, supporting Azure, AWS and GCP), and Google Security Command Center (Standard, Premium and a deprecated Enterprise tier that is announced to shut down on 2027-05-21). See [CSPM](cloud-security-posture-management.md).

### Comparison matrix (documented statements only)

An empty cell means that I did not verify it.

| Dimension | Prisma Cloud / Cortex Cloud | Falcon Cloud Security | Orca | CloudGuard | Netskope Public Cloud Security |
| --- | --- | --- | --- | --- | --- |
| Clouds in the sources | AWS, Azure, GCP, OCI, Alibaba Cloud (onboarding docs) | "all major clouds" (marketing) | AWS, Azure, Google Cloud, Kubernetes, Oracle Cloud, Alibaba Cloud | AWS, Azure, GCP, Alibaba Cloud, Kubernetes | AWS, Azure, GCP |
| CSPM collection | Provider APIs through a role with an external ID | Agentless, cloud-native | Provider APIs plus snapshot-based SideScanning | Provider APIs plus notification services | API-enabled controls |
| Workload scanning without agents | Yes, snapshot-based on AWS, Azure, GCP, OCI | Agentless visibility plus agent-based runtime | Yes, SideScanning (SaaS or in-account Pod) | | Storage scan (DLP and malware) |
| Rule language | RQL (Run) and JSON query (Build) | | | GSL | Domain specific language for custom rules |
| Custom rules | Yes, with policy types and compliance mapping | | | Yes, GSL Builder, cloned rulesets | Yes, profiles and rules |
| Built-in standards named | CIS (several versions), CSA CCM, NIST 800-53 and CSF, MITRE ATT&CK, GDPR, HIPAA and more | | | PCI-DSS, HIPAA, CIS Foundations and more | CIS, PCI-DSS, NIST, HIPAA and more |
| Context and attack path | Attack path policies | "graph-based context" (marketing) | Unified data model and prioritization | | |
| IaC or pre-deploy | Build policies for IaC and repositories | IaC scanning module | CI/CD scans in the data model | CloudFormation template analysis | |
| Remediation | CLI remediation, needs write access | | Optional auto remediation resources | CloudBots, re-run to verify | Auto remediation templates, ticket orchestration |
| Identity (CIEM) | IAM Security, net effective permissions | CIEM module | Listed on the website | CIEM in the overview | Not on the Public Cloud Security page |
| Pricing model in the sources | Credits per feature set | | | | |
| Documented limit | Trusted Launch Azure VMs not supported in agentless scanning | | | | |

The matrix shows the main thing: public documentation is uneven. Where a cell is empty, the answer comes from a proof of concept or a written statement from the vendor, not from this note.

## Worked example

The scenario: Example Corp (`example.com`) has to choose a CSPM product for an estate in AWS and Azure and a small GCP footprint. The method is a weighted proof of concept with a seeded test environment, so that the answer comes from measured results and not from documents.

**Step 1: shortlist by gates, not by features.** Three questions eliminate products early:

1. Does it cover the clouds and the 30 services you use most (documented support matrix)?
2. What does the connector need? Read the role or template. Compare with the features you will use. Prefer external ID or federation, and read-only by default (compare the documented behaviors above).
3. Can you export your rules, findings and 90 days of history?

**Step 2: seed a sandbox.** In a dedicated, authorized sandbox account per cloud, create the 24 test cases in the [seeded misconfiguration list](../_assets/cloud-and-infrastructure-security/cspm-poc-seeded-misconfigurations.csv). They include public storage in each cloud, open management ports, a missing public access guardrail, unencrypted data with a PII tag, a toxic combination (open SSH on an instance with an admin role), identity hygiene, disabled logging, a drift case, an exception case, an IaC case and a connector failure case. Use synthetic data and placeholder values only.

**Step 3: run all candidate tools for the same period and fill the [scorecard](../_assets/cloud-and-infrastructure-security/cspm-poc-scorecard.csv).** Record, for each tool, which seeded cases it detected, how long each took, how it ranked the toxic combinations, and how long it took to write the same three custom rules.

**Step 4: score and test the result for sensitivity.** The following script applies weights to PoC scores and shows how the winner changes when the weights change. The scores here are invented for the exercise and the products are called A, B and C on purpose. Tested with Python 3.10.12, standard library only.

```python
criteria = {   # weight, meaning of a 3 (0 = missing, 1 = weak, 2 = adequate, 3 = strong, measured in the PoC)
    "detection_coverage": 25,    # share of the seeded misconfigurations found
    "false_positive_rate": 15,
    "time_to_detect": 10,        # minutes from change to finding
    "context_prioritization": 15,
    "custom_rule_effort": 10,
    "connector_least_privilege": 10,
    "integration_workflow": 10,  # ticketing, SIEM, API, IaC pipeline
    "cost_predictability": 5,
}
scores = {
    "A": dict(detection_coverage=3, false_positive_rate=2, time_to_detect=2, context_prioritization=3,
              custom_rule_effort=1, connector_least_privilege=2, integration_workflow=3, cost_predictability=1),
    "B": dict(detection_coverage=2, false_positive_rate=3, time_to_detect=3, context_prioritization=2,
              custom_rule_effort=3, connector_least_privilege=3, integration_workflow=2, cost_predictability=2),
    "C": dict(detection_coverage=3, false_positive_rate=1, time_to_detect=1, context_prioritization=2,
              custom_rule_effort=2, connector_least_privilege=1, integration_workflow=2, cost_predictability=3),
}


def total(tool, weights):
    return sum(weights[c] * scores[tool][c] for c in weights) / (3 * sum(weights.values())) * 100


def show(title, weights):
    ranked = sorted(scores, key=lambda t: -total(t, weights))
    print(f"{title:38s}", "  ".join(f"{t}={total(t, weights):5.1f}" for t in ranked), "-> winner", ranked[0])


show("baseline weights", criteria)
heavy_detect = dict(criteria, detection_coverage=45)                       # detection matters most
heavy_ops = dict(criteria, integration_workflow=25, custom_rule_effort=20)  # operations matter most
show("detection weight 45", heavy_detect)
show("integration 25, custom rules 20", heavy_ops)
gates = {"connector_least_privilege": 2}   # hard gate: a 1 or 0 on least privilege disqualifies
ok = [t for t in scores if all(scores[t][c] >= m for c, m in gates.items())]
print("passes the least-privilege gate:", ok)
```

Output:

```text
baseline weights                       B= 81.7  A= 78.3  C= 65.0 -> winner B
detection weight 45                    A= 81.9  B= 79.2  C= 70.8 -> winner A
integration 25, custom rules 20        B= 81.3  A= 77.3  C= 65.3 -> winner B
passes the least-privilege gate: ['A', 'B']
```

What to notice:

1. **The winner depends on the weights.** With detection weighted at 45, tool A wins. At the baseline weights, tool B wins by 3.4 points. When the margin is that small, the weights are the decision, so agree them before the PoC and write down why.
2. **Gates beat weights for non-negotiables.** Tool C scores well on detection and cost but has a 1 on connector privilege. A weighted sum lets that be offset. A gate removes it. Least privilege of the connector, data handling and exit are gate criteria in the scorecard.
3. **Scores come from measurement.** Detection coverage is the share of seeded cases found, time to detect is measured with a clock. Subjective scores (a demo's "feel") should be limited to criteria where measurement is impossible.
4. **The same method works for any product**, including the native tools. Always include them as a baseline.

**Step 5: negotiate and plan the exit.** Ask for the connector permission list in writing, the data flow and retention description, the export format for rules and findings, and the pricing unit at twice the estate size.

## Trade offs and when to use it

### When a third-party platform is justified

- Multiple clouds with a central team (see [multicloud CSPM](multicloud-cspm.md)).
- Need for context that native tools do not provide, such as attack paths across identity, network and data, or a single workflow across clouds.
- Existing platform in the SOC that the CSPM data should join.

### When native tools are enough

- One dominant cloud, mature IaC and guardrails, and a small team that can handle the native console.
- Early stage: start with the native free tier (for example Microsoft's Foundational CSPM, AWS Security Hub CSPM trial) to learn the findings before buying.

### Costs and limits common to all of them

- **Another privileged integration.** The product reads configuration of all your accounts. Treat it as a high-risk vendor connection.
- **Different units of pricing.** Resources, checks and findings, Credits per feature set, workloads. Estate growth and seeded noise change the bill.
- **Platform sprawl.** CNAPP bundles tempt you into modules (workload, data, AI, identity) before the CSPM basics work.
- **Vendor-specific rule languages.** RQL, GSL and others lock your custom policy to a vendor unless you keep intents and tests in your own repository.
- **Marketing language.** "Agentless", "context-aware" and "attack path" mean different things in different products. Test, do not assume.

### Alternatives

| Need | Option |
| --- | --- |
| Free baseline | Native services and the CIS benchmarks |
| Open source scanners | Several exist for cloud configuration, not covered here and not verified |
| Managed service | Provider or integrator services, with the same connector and data handling questions |

## Common mistakes

| Mistake | Why it is wrong | Fix |
| --- | --- | --- |
| Choosing from a feature matrix | Vendors' matrices are marketing and uneven | Run a seeded PoC and measure |
| Reading "agentless" as "nothing deployed in my account" | Snapshot scanning creates snapshots, and some products create scanner resources | Ask what is created, where, for how long, and with which permissions |
| Enabling every module on day one | Alert volume without ownership | Start with CSPM and the top three exposure rules, then add modules |
| Not testing the vendor's connector failure behavior | A broken connector can look like a clean estate | Include a connector failure case (S24 in the seeded list) |
| Ignoring the data handling question | Configuration and metadata can contain sensitive values | Get the data flow, retention and regional processing in writing |
| Accepting a compliance percentage as a result | It covers only the checks in the standard | Ask for coverage, risk-ranked findings and drift |
| Believing the rename changes nothing | Prisma Cloud and Cortex Cloud, Falcon Horizon and Falcon Cloud Security: documentation, licensing and features move | Confirm the exact edition and the documentation set in the contract |
| Evaluating only on detection | A tool nobody can operate gives no benefit | Score integration, custom rules and workflow too |
| Skipping the exit plan | Rules and history can be trapped | Test export during the PoC |

## Practice

1. Explain the three meanings of "agentless" and give a product example for each from this note.
2. Why does Check Point's rule `SecurityGroup should not have inboundRules contain [port=22 and scope='0.0.0.0/0']` need a different implementation in Azure or GCP?
3. In Netskope's results model, rule X is checked against 100 resources and 99 pass. What is the rule status, and what is the number to report to an executive?
4. What is the difference between a Prisma Cloud Run policy and a Build policy, and which supports remediation?
5. CrowdStrike lists an IOA and an IOM for the same Azure storage risk. Describe both, and say which one a CSPM program owns.
6. Redo the PoC sensitivity check with your own weights. Which criteria would you make gates?
7. Draft five questions you would put in a request for information about the connector of a CSPM vendor.

Hints and answers:

1. API-based (CSPM collection in every product, for example CloudGuard Posture Management through provider APIs), snapshot-based (Prisma Cloud agentless scanning, Orca SideScanning), agent-free visibility combined with agents for runtime (Falcon Cloud Security).
2. The rule targets an AWS entity (`SecurityGroup`, `inboundRules`). Azure uses network security groups and GCP uses firewall rules, with different fields and semantics, so the intent needs an implementation per cloud.
3. The rule fails, because Netskope's rule status fails if any resource fails. The executive number is the resource-level failure (1 of 100) plus the risk of the failed resource, not the "failed rule".
4. Run policies scan deployed resources and use RQL. Build policies scan IaC templates and repositories using a JSON query. Run policies can carry CLI remediation. Build policies do not support remediation by CLI or UI.
5. The IOM is "storage account configured to allow access from all networks" (a static setting). The IOA is "storage account networking changed to all networks" (a user action). CSPM owns the IOM, and detection and response owns the IOA, though a platform shows both.
6. Typical gates: connector least privilege, data handling, exit and export, and coverage of the clouds and services you use. Weights are for the rest.
7. For example: What exact permissions does the connector role need per capability? Is access read-only by default, and which features need write? Does it use an external ID or federated credentials? What configuration data and metadata are stored, where, for how long? How do you notify us if the connector loses permissions or a scan fails?

## Further reading

- Prisma Cloud documentation: welcome and platform overview, Create a Custom Policy (Run, Build, RQL), Attack Path Policies, Agentless Scanning, Built-in Compliance Standards and Onboard AWS Account: https://docs.prismacloud.io/content-collections/get-started/welcome-to-prisma-cloud.md
- Palo Alto Networks, press release introducing Cortex Cloud (2025-02-13): https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-introduces-cortex-cloud--the-future-of-real-time-cloud-security
- CrowdStrike, How CrowdStrike Detects Cloud Storage Misconfigurations (2022), with the IOA and IOM policy table: https://www.crowdstrike.com/en-us/blog/how-crowdstrike-detects-cloud-storage-misconfigurations/
- CrowdStrike, Falcon Cloud Security CNAPP page (module list): https://www.crowdstrike.com/en-us/platform/cloud-security/cnapp/
- Orca Security, SideScanning Technical Brief (2024 edition): https://orca.security/wp-content/uploads/2024/11/Orca-SideScanning-Technical-Brief-Digital.pdf
- Check Point, CloudGuard documentation: Cloud Security Posture Management, Rules and Rulesets, and Governance Specification Language: https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/PostureManagement/GSL.htm
- Netskope documentation: Cloud Security Posture Management, Getting Started with CSPM for Public Cloud, View Security Posture Compliance: https://docs.netskope.com/en/cloud-security-posture-management
- The PoC scorecard and seeded misconfiguration list used in this note: [scorecard](../_assets/cloud-and-infrastructure-security/cspm-poc-scorecard.csv) and [seeded cases](../_assets/cloud-and-infrastructure-security/cspm-poc-seeded-misconfigurations.csv).
