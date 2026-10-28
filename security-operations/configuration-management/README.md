# Configuration management

Provisioning, baselining, change control and automation of system configuration so that systems stay in a known and secure state.

Status: scaffold.

## Scope

- Belongs here: secure configuration baselines, benchmarks, drift detection, change control for configuration, configuration automation.
- Belongs elsewhere: the asset inventory is in [asset management](../../asset-security/asset-management/README.md), cloud and Kubernetes posture checks are in [CSPM](../../security-architecture-and-engineering/cloud-and-infrastructure-security/cloud-security-posture-management.md) and [KSPM](../../security-architecture-and-engineering/cloud-and-infrastructure-security/kubernetes-security-posture-management/README.md), and vendor patch cycles are in [vulnerability remediation](../vulnerability-management/vulnerability-remediation/README.md).

## CISSP sections

7.3 and 7.9, with related sections 3.3 and 7.8 of the ISC2 CISSP Exam Outline effective April 15, 2024.

## Notes

- [Secure configuration](secure-configuration/README.md): Baselines, benchmarks, SCAP, exceptions and drift, with a tested checker.

## To complete

- [ ] Introduction that covers the whole configuration management discipline.
- [ ] Reading order with one line per note.
- [ ] Planned topics (change management, infrastructure as code security, immutable infrastructure, golden images).
- [ ] Sidecar relations to the CM controls in the SP 800-53 note.

Back to [Security operations](../README.md).
