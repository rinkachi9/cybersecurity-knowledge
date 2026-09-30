# Privilege escalation

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Privilege Escalation** is a critical technique used in cyberattacks where an attacker **gains higher-level access** to a system than originally intended. It enables threat actors to **move from restricted accounts** (like standard users) to **privileged accounts** (like administrators or root), expanding their control and access to sensitive data or system functions.

Privilege escalation is often a **post-exploitation technique**, used **after initial access** is gained, such as through phishing, malware, or exploiting a vulnerable service.

### Importance

- **Allows full system control** - modifying, deleting, or stealing data
- **Bypasses security controls** - disables AV, alters logs, accesses secrets
- **Enables lateral movement** - spreads malware or maintains persistence
- **Used in nearly all APTs** - privilege escalation is part of many advanced attacks

## Types

### Vertical Privilege Escalation (Elevation)

- The attacker **gains more privileges** than originally granted.
- Example: From a limited user account to system/root/admin.

#### Horizontal Privilege Escalation

- The attacker stays at the **same access level**, but gains access to **other users’ data or privileges**.
- Example: User A accesses User B’s email or files.

### Techniques

| Technique | Description |
| --- | --- |
| **Exploiting Vulnerabilities** | Using known (or 0-day) bugs in OS, drivers, or apps to execute code with higher privileges. |
| **Insecure Configurations** | Abuse of weak permissions, unnecessary services, or misconfigured file/registry access. |
| **Unquoted Service Paths** | If a Windows service path is improperly quoted, malware can be placed in an earlier-resolving directory. |
| **DLL Hijacking** | Replacing DLLs loaded by high-privilege programs with malicious versions. |
| **Token Impersonation** | Stealing or forging tokens to impersonate a privileged user. |
| **SUID/SGID Abuse (Linux)** | Leveraging binaries with set-user-ID or set-group-ID flags to execute actions as root. |
| **Kernel Exploits** | Exploiting low-level bugs to execute arbitrary code in kernel mode (ring 0). |
| **Password Hunting** | Searching for hardcoded credentials, configuration files, or memory dumps to reuse admin accounts. |
| **Scheduled Task Abuse** | Modifying or creating scheduled jobs that run with system privileges. |

### Mitigation

| Strategy | Description |
| --- | --- |
| **Principle of Least Privilege (PoLP)** | Grant users and applications only the minimum permissions needed. |
| **Patch Management** | Regularly update OS and software to fix privilege-related vulnerabilities. |
| **Audit & Monitor** | Enable logging of privilege use, analyze abnormal behavior (e.g., login from unusual location). |
| **File/Registry Permission Hardening** | Limit access to sensitive paths, scripts, or services. |
| **Application Control** | Use tools to restrict execution of unauthorized code (e.g., AppLocker, SELinux). |
| **Remove Unused Services** | Disable unnecessary features or accounts that may be abused. |

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
