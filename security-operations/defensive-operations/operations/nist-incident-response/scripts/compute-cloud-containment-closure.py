# Python 3.10, standard library only. Run: python3 compute-cloud-containment-closure.py
# Expert case: a stolen CI/CD token is used to reach a cloud account. Containment must remove EVERY path
# the attacker can use, not only the stolen credential. The model is synthetic.
from collections import deque

# Edges: identity -> identities it can become (assume-role trust, token exchange, key creation rights).
CAN_BECOME = {
    "ci-token":          ["role/deploy"],                    # the stolen credential
    "role/deploy":       ["role/artifact-write", "user/ci-admin"],   # deploy role may assume a writer role and manage the ci-admin user
    "role/artifact-write": [],
    "user/ci-admin":     ["role/data-read"],                 # ci-admin user trusted by the data-read role
    "role/data-read":    [],
    "role/audit-reader": [],                                 # unrelated, no path from the token
}
ACCESS = {
    "role/deploy": ["bucket/build-artifacts"],
    "role/artifact-write": ["bucket/release-signing-keys"],
    "user/ci-admin": ["iam:CreateAccessKey"],
    "role/data-read": ["bucket/customer-exports"],
    "role/audit-reader": ["logs/audit"],
}
# Findings from the audit log review: things the attacker created (persistence).
ATTACKER_CREATED = [("user/ci-admin", "access-key AKIA-EXAMPLE-0001"), ("role/deploy", "trust policy edited to trust external account 999999999999 (placeholder)")]


def closure(start):
    seen, q = {start}, deque([start])
    while q:
        for nxt in CAN_BECOME.get(q.popleft(), []):
            if nxt not in seen:
                seen.add(nxt); q.append(nxt)
    return seen


def reach(ids):
    return sorted({r for i in ids for r in ACCESS.get(i, [])})


full = closure("ci-token")
print("identities reachable from the stolen token:", sorted(full - {"ci-token"}))
print("resources reachable:", reach(full))

# Naive containment: delete the stolen credential only
after_naive = closure("role/deploy") | {i for i, _ in ATTACKER_CREATED}   # attacker keeps the key on ci-admin and the trust edit
print("\nnaive containment (rotate the CI token only):")
print("  attacker can still become:", sorted(after_naive - {"role/deploy"}))
print("  data the attacker can still read:", [r for r in reach(after_naive) if "customer" in r])

# Planned containment: derive the steps from the closure and the persistence list
plan = []
plan.append("1 freeze changes to IAM in the account (so the picture stops moving)")
for ident, what in ATTACKER_CREATED:
    plan.append(f"2 remove persistence on {ident}: {what}")
for ident in sorted(full - {"ci-token"}):
    plan.append(f"3 revoke active sessions of {ident} (deny tokens issued before now)")
plan.append("4 rotate the CI secret and every secret the CI runner could read")
plan.append("5 verify with a fresh closure computation, then re-enable changes")
print("\ncontainment plan derived from the closure:")
for step in plan:
    print("  ", step)
