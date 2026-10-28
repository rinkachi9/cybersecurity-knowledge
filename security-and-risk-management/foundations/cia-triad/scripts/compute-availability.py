# Python 3.10, standard library only. Run: python3 compute-availability.py
# Availability arithmetic: nines to downtime, series and parallel composition, and the effect of correlated failure.
MIN_YEAR = 365 * 24 * 60


def downtime_min(a):
    return (1 - a) * MIN_YEAR


print("target      downtime per year")
for a in (0.99, 0.999, 0.9999, 0.99999):
    print(f"{a*100:8.3f}%  {downtime_min(a):10.1f} min  ({downtime_min(a)/60:7.2f} h)")

# Steady-state availability from failure and repair behavior
mtbf_h, mttr_h = 2000.0, 4.0
a_node = mtbf_h / (mtbf_h + mttr_h)
print(f"\nsingle node: MTBF {mtbf_h:.0f} h, MTTR {mttr_h:.0f} h -> A = {a_node:.5f} ({downtime_min(a_node):.0f} min/year)")

# Series: every component must work. Parallel: at least one must work (independent failures).
series = lambda *xs: __import__("math").prod(xs)
parallel = lambda *xs: 1 - __import__("math").prod(1 - x for x in xs)
web, app, db = 0.9995, 0.999, 0.9995
a_serial = series(web, app, db)
print(f"\nweb {web} x app {app} x db {db} in series       -> {a_serial:.5f} ({downtime_min(a_serial):.0f} min/year)")
a_app2 = series(web, parallel(app, app), db)
print(f"same, app tier duplicated (independent)          -> {a_app2:.5f} ({downtime_min(a_app2):.0f} min/year)")

# Correlated failure: a fraction beta of each node's unavailability is a common cause (same zone, same bad deploy)
beta = 0.2
u = 1 - app
u_pair = beta * u + ((1 - beta) * u) ** 2          # common-cause part is not removed by duplication
a_pair = 1 - u_pair
a_app2c = series(web, a_pair, db)
print(f"app tier duplicated, common-cause share {beta:.0%}      -> {a_app2c:.5f} ({downtime_min(a_app2c):.0f} min/year)")
print(f"redundancy promised {downtime_min(a_serial)-downtime_min(a_app2):.0f} min/year saved, correlated failure delivers {downtime_min(a_serial)-downtime_min(a_app2c):.0f}")
