# Python 3.10, standard library only.
# Run: python3 evaluate-cluster-posture.py
# A small KSPM engine over a synthetic cluster snapshot (plain dicts shaped like Kubernetes API objects).
# It evaluates Pod Security Standards (subset), RBAC risks and namespace guardrails, ranks findings by
# context (exposure x privilege x secret access), and reports drift between two snapshots.
import copy
import json

BASELINE_CAPS = {"AUDIT_WRITE", "CHOWN", "DAC_OVERRIDE", "FOWNER", "FSETID", "KILL", "MKNOD",
                 "NET_BIND_SERVICE", "SETFCAP", "SETGID", "SETPCAP", "SETUID", "SYS_CHROOT"}

snapshot = {
    "namespaces": {
        "shop":  {"labels": {"pod-security.kubernetes.io/enforce": "restricted"}, "netpol_default_deny": True},
        "batch": {"labels": {}, "netpol_default_deny": False},
    },
    "pods": [
        {"ns": "shop", "name": "web-1", "sa": "web", "exposed": True,
         "spec": {"containers": [{"name": "web", "image": "registry.example.com/web@sha256:" + "a" * 64,
                  "securityContext": {"allowPrivilegeEscalation": False, "runAsNonRoot": True,
                                      "capabilities": {"drop": ["ALL"]},
                                      "seccompProfile": {"type": "RuntimeDefault"}}}]}},
        {"ns": "batch", "name": "etl-7", "sa": "etl", "exposed": True,
         "spec": {"hostNetwork": True,
                  "volumes": [{"name": "h", "hostPath": {"path": "/var/run"}}],
                  "containers": [{"name": "etl", "image": "registry.example.com/etl:latest",
                                  "securityContext": {"privileged": True}}]}},
    ],
    "bindings": [
        {"ns": None, "subject": "sa:batch/etl", "role": "cluster-admin"},
        {"ns": "shop", "subject": "sa:shop/web", "role": "web-reader"},
    ],
    "roles": {
        "cluster-admin": [{"verbs": ["*"], "resources": ["*"]}],
        "web-reader": [{"verbs": ["get", "list"], "resources": ["configmaps"]}],
    },
}


def pod_findings(p):
    out, spec = [], p["spec"]
    if spec.get("hostNetwork") or spec.get("hostPID") or spec.get("hostIPC"):
        out.append(("PSS-BASELINE-host-namespaces", "high"))
    if any("hostPath" in v for v in spec.get("volumes", [])):
        out.append(("PSS-BASELINE-hostpath", "high"))
    for c in spec["containers"]:
        sc = c.get("securityContext", {})
        if sc.get("privileged"):
            out.append(("PSS-BASELINE-privileged", "critical"))
        if set(sc.get("capabilities", {}).get("add", [])) - BASELINE_CAPS:
            out.append(("PSS-BASELINE-capabilities", "high"))
        if sc.get("seccompProfile", {}).get("type") == "Unconfined":
            out.append(("PSS-BASELINE-seccomp-unconfined", "medium"))
        if sc.get("allowPrivilegeEscalation") is not False:
            out.append(("PSS-RESTRICTED-privilege-escalation", "medium"))
        if sc.get("runAsNonRoot") is not True:
            out.append(("PSS-RESTRICTED-run-as-non-root", "medium"))
        if "ALL" not in sc.get("capabilities", {}).get("drop", []):
            out.append(("PSS-RESTRICTED-drop-all-capabilities", "low"))
        if sc.get("seccompProfile", {}).get("type") not in ("RuntimeDefault", "Localhost"):
            out.append(("PSS-RESTRICTED-seccomp", "low"))
        if "@sha256:" not in c["image"]:
            out.append(("IMAGE-not-pinned-by-digest", "low"))
    return out


def rbac_findings(snap):
    out = []
    for b in snap["bindings"]:
        for rule in snap["roles"].get(b["role"], []):
            wild = "*" in rule["verbs"] or "*" in rule["resources"]
            if wild and b["subject"].startswith("sa:"):
                out.append((f"RBAC-wildcard-for-workload:{b['subject']}", "critical"))
            if {"escalate", "bind", "impersonate"} & set(rule["verbs"]):
                out.append((f"RBAC-escalation-verb:{b['subject']}", "high"))
    return out


def ns_findings(snap):
    out = []
    for name, ns in snap["namespaces"].items():
        if "pod-security.kubernetes.io/enforce" not in ns["labels"]:
            out.append((f"NS-no-pod-security-enforce:{name}", "medium"))
        if not ns["netpol_default_deny"]:
            out.append((f"NS-no-default-deny-networkpolicy:{name}", "medium"))
    return out


def evaluate(snap):
    findings = [(f"{p['ns']}/{p['name']}", rule, sev) for p in snap["pods"] for rule, sev in pod_findings(p)]
    findings += [("rbac", rule, sev) for rule, sev in rbac_findings(snap)]
    findings += [("namespace", rule, sev) for rule, sev in ns_findings(snap)]
    return findings


def toxic_combinations(snap):
    """Context a flat rule list misses: exposed + escapable + powerful identity on one workload."""
    wild = {b["subject"] for b in snap["bindings"] for r in snap["roles"].get(b["role"], [])
            if "*" in r["verbs"] and b["role"] == "cluster-admin"}
    result = []
    for p in snap["pods"]:
        escapable = any(r.startswith("PSS-BASELINE") for r, _ in pod_findings(p))
        powerful = f"sa:{p['ns']}/{p['sa']}" in wild
        if p["exposed"] and escapable and powerful:
            result.append(f"{p['ns']}/{p['name']}: exposed + node-escape primitives + cluster-admin identity")
    return result


first = evaluate(snapshot)
print("findings (resource, rule, severity):")
for f in first:
    print("  ", f)
print("toxic combinations:", toxic_combinations(snapshot))

# Drift: a later snapshot after one fix and one regression.
later = copy.deepcopy(snapshot)
later["namespaces"]["batch"]["netpol_default_deny"] = True            # fix
later["pods"][0]["spec"]["containers"][0]["securityContext"]["privileged"] = True   # regression
now = evaluate(later)
key = lambda f: (f[0], f[1])
old, new = {key(f) for f in first}, {key(f) for f in now}
print("fixed    :", sorted(old - new))
print("new      :", sorted(new - old))
