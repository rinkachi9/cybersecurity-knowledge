# Python 3.10, standard library only.
# Run: python3 dspm-sampling-risk.py
# Two ideas behind data security posture management on synthetic data stores:
# 1 sampling: how likely is a sampled scan to find sensitive records, and how many are missed;
# 2 posture: combine sensitivity, exposure, access and encryption into one ranked list.
import random

random.seed(5)

# 1. A store with 10,000 objects. Sensitive objects are either clustered (a sensitive folder) or scattered.
def make_store(n, sensitive, clustered):
    objs = [False] * n
    if clustered:
        start = random.randrange(0, n - sensitive)
        for i in range(start, start + sensitive):
            objs[i] = True
    else:
        for i in random.sample(range(n), sensitive):
            objs[i] = True
    return objs

def sampled_detects(objs, sample_size):
    sample = random.sample(range(len(objs)), sample_size)
    return any(objs[i] for i in sample)

trials = 2000
print("1 probability that a sample finds at least one sensitive object (10,000 objects)")
for sensitive in (5, 50, 500):
    for sample in (100, 500):
        for clustered in (False, True):
            hits = sum(sampled_detects(make_store(10000, sensitive, clustered), sample) for _ in range(trials))
            print(f"   sensitive={sensitive:3} sample={sample:3} {'clustered' if clustered else 'scattered':9} -> {hits / trials:.2f}")

# 2. Posture: rank stores by what could actually hurt.
stores = [
    # name, sensitivity (0-3), public, accessible identities, encrypted with customer key, has backup copy outside policy
    ("orders-db",        3, False,  12, True,  False),
    ("marketing-assets", 0, True,    4, False, False),
    ("hr-exports",       3, True,   60, False, True),
    ("ml-training-set",  2, False, 300, True,  True),
    ("logs-archive",     1, False,   9, False, False),
]
def risk(sens, public, who, cmk, stray):
    score = sens * 10
    score += 30 if public else 0
    score += min(who, 100) * 0.2
    score += 0 if cmk else 5
    score += 10 if stray else 0
    return score * (1 if sens else 0.2)          # public but non-sensitive data is a different problem
print("2 posture ranking (higher means look first)")
for name, sens, pub, who, cmk, stray in sorted(stores, key=lambda s: -risk(*s[1:])):
    print(f"   {name:17} risk={risk(sens, pub, who, cmk, stray):5.1f} sensitivity={sens} public={str(pub):5} identities={who:3} cmk={cmk} stray_copy={stray}")
