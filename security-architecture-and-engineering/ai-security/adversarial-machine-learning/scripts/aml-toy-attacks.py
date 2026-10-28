# Python 3.10, standard library only.
# Run: python3 aml-toy-attacks.py
# Four attack classes of the NIST AI 100-2 E2025 taxonomy on a toy logistic regression model, synthetic 2-D data:
# evasion (adversarial example), data poisoning (label flipping), model extraction (query-only surrogate)
# and membership inference (confidence gap between training and unseen points).
import math
import random

random.seed(11)

def make(n):
    pts = []
    for _ in range(n):
        y = random.random() < 0.5
        cx = 1.5 if y else -1.5
        pts.append(((random.gauss(cx, 1.0), random.gauss(cx, 1.0)), int(y)))
    return pts

def sigmoid(z): return 1 / (1 + math.exp(-max(min(z, 30), -30)))

def train(data, epochs=300, lr=0.1):
    w, b = [0.0, 0.0], 0.0
    for _ in range(epochs):
        gw, gb = [0.0, 0.0], 0.0
        for (x1, x2), y in data:
            e = sigmoid(w[0] * x1 + w[1] * x2 + b) - y
            gw[0] += e * x1; gw[1] += e * x2; gb += e
        n = len(data)
        w = [w[0] - lr * gw[0] / n, w[1] - lr * gw[1] / n]; b -= lr * gb / n
    return w, b

def prob(m, x): return sigmoid(m[0][0] * x[0] + m[0][1] * x[1] + m[1])
def acc(m, data): return sum((prob(m, x) > 0.5) == bool(y) for x, y in data) / len(data)

train_set, test_set = make(200), make(1000)
model = train(train_set)
print(f"baseline               : test accuracy {acc(model, test_set):.3f}")

# 1. Evasion (integrity violation at deployment time): move each test point by eps in the direction that raises the loss.
def evade(m, x, y, eps):
    s = -1 if y == 1 else 1                  # for a linear model the loss gradient sign is sign(w) times (+/-)
    return (x[0] + s * eps * math.copysign(1, m[0][0]), x[1] + s * eps * math.copysign(1, m[0][1]))
for eps in (0.5, 1.0, 2.0):
    adv = [(evade(model, x, y, eps), y) for x, y in test_set]
    print(f"1 evasion eps={eps:<4}     : accuracy {acc(model, adv):.3f}")

# 2. Data poisoning (integrity violation at training time): flip labels of a fraction of training points.
for frac in (0.1, 0.3, 0.45):
    poisoned = [(x, 1 - y) if i < frac * len(train_set) else (x, y) for i, (x, y) in enumerate(train_set)]
    print(f"2 label flipping {frac:<4}  : accuracy of retrained model {acc(train(poisoned), test_set):.3f}")

# 3. Model extraction (privacy/IP): the attacker only sees predicted labels from an API and trains a surrogate.
queries = [((random.uniform(-4, 4), random.uniform(-4, 4))) for _ in range(300)]
stolen_labels = [(q, int(prob(model, q) > 0.5)) for q in queries]
surrogate = train(stolen_labels)
agree = sum((prob(surrogate, x) > 0.5) == (prob(model, x) > 0.5) for x, _ in test_set) / len(test_set)
print(f"3 extraction (300 q)   : surrogate agrees with the victim on {agree:.3f} of test inputs")

# 4. Membership inference (privacy compromise): an overfit model is more confident on its training points.
tiny = make(12)
overfit = train(tiny, epochs=5000, lr=0.5)
def conf(m, x, y): p = prob(m, x); return p if y == 1 else 1 - p
members = sum(conf(overfit, x, y) for x, y in tiny) / len(tiny)
others = [p for p in make(500)]
non_members = sum(conf(overfit, x, y) for x, y in others) / len(others)
print(f"4 membership signal    : mean confidence members {members:.3f} vs non-members {non_members:.3f}")
