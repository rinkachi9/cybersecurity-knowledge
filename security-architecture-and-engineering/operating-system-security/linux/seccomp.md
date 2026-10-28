# Seccomp

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Seccomp** (short for *Secure Computing Mode*) is a Linux kernel feature that allows a process to restrict the system calls it can make.

It is primarily used to reduce the kernel’s attack surface by **whitelisting** or **blacklisting** system calls, limiting what a process can do even if it becomes compromised.

- Introduced in Linux 2.6.12 (2005) in a very minimal form.
- Extended in later versions (notably with **seccomp-bpf** in Linux 3.5) to allow fine-grained filtering.

## Purpose

From a **security** perspective, seccomp is used to:

- **Minimize Attack Surface:** Many kernel vulnerabilities are exposed through rarely used syscalls. Restricting them reduces potential exploitation.
- **Contain Exploits:** Even if an attacker gains remote code execution inside an application, seccomp can prevent them from using dangerous syscalls (e.g., `execve`, `mount`, `ptrace`).
- **Sandbox Applications:** Common in container runtimes (Docker, Podman), browsers (Chrome, Firefox), and network services.

It aligns with the **principle of least privilege** - processes only get the exact syscalls they need.

## How it works

Seccomp operates by:

1. **Enabling Filtering Mode**
   - Once enabled for a process, seccomp rules cannot be removed (only tightened).
   - Child processes inherit seccomp restrictions.
2. **Defining Filters**
   - Filters are implemented using **BPF (Berkeley Packet Filter)** programs in *seccomp-bpf* mode.
   - These filters decide the action for each syscall:
     - `SECCOMP_RET_ALLOW` - allow the syscall.
     - `SECCOMP_RET_ERRNO` - deny the syscall and return an error.
     - `SECCOMP_RET_KILL_PROCESS` - kill the process if it tries to call it.
     - `SECCOMP_RET_LOG` - log the syscall attempt.
     - `SECCOMP_RET_TRAP` - send a SIGSYS signal to the process.
3. **Intercepting Syscalls**
   - When a process tries to invoke a syscall, the kernel checks the seccomp filter.
   - If the syscall is allowed, execution continues.
   - If not, the kernel applies the specified action.

## Modes of operation

There are two primary modes:

1. **Strict Mode**
   - The original, legacy mode.
   - Only allows **four syscalls**: `read()`, `write()`, `exit()`, and `sigreturn()`.
   - Useful for very specialized processes, but rarely practical for general applications.
2. **Filter Mode (seccomp-bpf)**
   - Allows defining **custom rules** for allowed syscalls.
   - Much more flexible and widely used today.

## Practical usage

### Containers

- Docker, Kubernetes, and Podman use seccomp profiles to restrict containers to a minimal syscall set.
- Example: The **default Docker seccomp profile** blocks 44+ potentially dangerous syscalls.
- Prevents container escape through kernel exploits.

#### Browsers

- Chromium/Chrome use seccomp filters to sandbox rendering processes, restricting them to only basic I/O syscalls.
- Limits damage from vulnerabilities in JavaScript engines.

##### Security tools

- Used alongside **AppArmor** or **SELinux** for defense-in-depth.
- Often paired with **namespaces** and **cgroups** for container isolation.

## Example

A C example using `libseccomp` to only allow `read`, `write`, and `exit`:

```cpp
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL); // Default: kill process

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);

    seccomp_load(ctx);
    seccomp_release(ctx);

    printf("Seccomp filter applied.\n");
    return 0;
}
```

Any other syscall will terminate the process.

## Benefits

- **Attack Surface Reduction:** Eliminates unnecessary syscalls.
- **Mitigation of Kernel Exploits:** Even if an attacker controls execution, dangerous syscalls are unavailable.
- **Immutable Security:** Restrictions are irreversible for the process once applied.
- **Performance-Friendly:** Filtering syscalls via BPF is fast and efficient.

## Limitations & considerations

- **Requires Syscall Knowledge:** Must know exactly which syscalls the application needs.
- **Application-Specific:** Too restrictive filters may break functionality.
- **Does Not Stop All Attacks:** Memory corruption inside allowed syscalls can still be exploited.
- **Maintenance Overhead:** Kernel updates can introduce new syscalls that need review.

## Best practices

1. **Start with Known Profiles:** Use existing seccomp profiles for containers or applications and refine them.
2. **Least Privilege:** Allow only essential syscalls.
3. **Combine with Other Security Layers:** Use with AppArmor/SELinux, namespaces, and capabilities.
4. **Testing Before Deployment:** Always run applications in test environments with the seccomp profile enabled before production.
5. **Logging Denied Calls:** In development, log denied syscalls to adjust rules.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
