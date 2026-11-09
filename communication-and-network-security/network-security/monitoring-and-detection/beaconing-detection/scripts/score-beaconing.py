# Python 3.10, standard library only. Run: python3 score-beaconing.py conn.tsv
# Scores every (source, destination, port) pair in a Zeek-style conn log for beaconing.
# The idea follows the statistical approach used by tools such as RITA: a program that
# sleeps and calls home produces connection intervals and sizes that are far more regular
# than human activity. Each sub-score is between 0 (irregular) and 1 (machine-like).
import collections
import statistics
import sys

MIN_CONNECTIONS = 20  # fewer points than this make the statistics meaningless


def bowley_score(values):
    # Bowley (quartile) skewness is 0 for a symmetric distribution. Jittered sleep timers are
    # symmetric around their mean, human gaps are strongly right-skewed.
    q1, q2, q3 = statistics.quantiles(values, n=4)
    if q3 == q1:
        return 1.0
    return 1 - abs((q3 + q1 - 2 * q2) / (q3 - q1))


def mad_score(values):
    # Median absolute deviation relative to the median: robust against a few missed check-ins.
    med = statistics.median(values)
    mad = statistics.median(abs(v - med) for v in values)
    return max(0.0, 1 - mad / med) if med else 0.0


def size_score(values):
    # Check-ins of an implant often have nearly constant size. Use the spread of the middle half.
    q1, _, q3 = statistics.quantiles(values, n=4)
    return max(0.0, 1 - (q3 - q1) / max(statistics.median(values), 1))


def coverage_score(times):
    # Beacons run around the clock. Count how many clock hours of the day saw traffic.
    hours = {int(t // 3600) % 24 for t in times}
    return min(1.0, len(hours) / 24)


pairs = collections.defaultdict(list)
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith("#"):
            continue
        ts, src, dst, port, ob, _ = line.rstrip("\n").split("\t")
        pairs[(src, dst, int(port))].append((float(ts), int(ob)))

results = []
for (src, dst, port), conns in pairs.items():
    if len(conns) < MIN_CONNECTIONS:
        continue
    conns.sort()
    times = [t for t, _ in conns]
    gaps = [b - a for a, b in zip(times, times[1:]) if b - a > 1]  # ignore bursts within one second
    if len(gaps) < MIN_CONNECTIONS - 1:
        continue
    scores = {
        "skew": bowley_score(gaps),
        "mad": mad_score(gaps),
        "size": size_score([b for _, b in conns]),
        "hours": coverage_score(times),
    }
    total = sum(scores.values()) / len(scores)
    results.append((total, src, dst, port, len(conns), statistics.median(gaps), scores))

print(f"{'source':<12} {'destination':<15} {'port':>4} {'conns':>5} {'median gap':>10}  skew   mad  size hours  score")
for total, src, dst, port, n, med, s in sorted(results, reverse=True):
    print(f"{src:<12} {dst:<15} {port:>4} {n:>5} {med:>9.0f}s  {s['skew']:.2f}  {s['mad']:.2f}  {s['size']:.2f}  {s['hours']:.2f}  {total:.2f}")
print(f"\npairs below {MIN_CONNECTIONS} connections were skipped: "
      f"{sum(1 for v in pairs.values() if len(v) < MIN_CONNECTIONS)}")
