# Beaconing detection

## Summary

Beaconing is the regular check-in of an implanted agent to its command-and-control (C2) server: the agent sleeps, calls home to ask for instructions, and sleeps again. Because software keeps time far more regularly than a human clicks, beaconing shows up as connections at suspiciously even intervals to one destination, often with near-constant sizes and around the clock. This note explains how to detect it statistically from connection logs, and provides a scored detector run on a synthetic log containing human browsing, a software updater and an implant. The central lesson is that regularity alone is not malice: a legitimate updater beacons too, so detection ranks candidates for an analyst rather than deciding guilt.

## Prerequisites

- [Command and control traffic](../../network-attacks/command-and-control-traffic.md): what beaconing is part of (MITRE ATT&CK tactic TA0011).
- [Flow monitoring](../flow-monitoring.md) and [network security monitoring](../network-security-monitoring.md): the data this uses.
- Basic statistics: median, quartiles, skewness.

## Core concepts

### Definition

*Beaconing* is periodic, automated communication from a compromised host to a controller. Detecting it means finding destination pairs whose connection *timing* and *size* are far more regular than human-driven traffic, over a long enough window to be sure.

### Analogy

Imagine listening to footsteps in a corridor. A person walking to the coffee machine makes irregular trips: clustered in the morning, none at lunch, varying lengths. A metronome in a closet ticks at exactly the same interval all day and night. Beaconing is the metronome. The catch is that a legitimate wall clock also ticks regularly, so hearing a steady tick tells you to open the closet and look, not that you have found an intruder.

The analogy breaks because attackers know you listen for metronomes, so they add *jitter* (random variation in the sleep interval) to sound more like footsteps. Detection therefore cannot require perfect regularity; it must measure degrees of it.

### What makes beaconing detectable

| Signal | Beacon | Human browsing |
| --- | --- | --- |
| Interval between connections | Nearly constant, or constant plus bounded jitter | Highly variable, bursty, clustered in working hours |
| Distribution of intervals | Symmetric around the mean | Strongly right-skewed (many short gaps, a few long ones) |
| Connection size | Often near-constant small check-ins | Varies widely with content |
| Time-of-day coverage | All 24 hours | Concentrated in working hours |
| Destination | One, long-lived | Many, changing |

### Turning signals into scores

The detector [scripts/score-beaconing.py](scripts/score-beaconing.py) computes, per source-destination-port triple with enough connections, four sub-scores between 0 and 1:

- **Skew score** from Bowley (quartile) skewness of the intervals. Jittered sleep timers are symmetric (score near 1); human gaps are right-skewed (score near 0).
- **Dispersion score** from the median absolute deviation of the intervals relative to their median. Robust against a few missed check-ins.
- **Size score** from the spread of the middle half of connection sizes. Constant-size check-ins score high.
- **Coverage score** from how many of the 24 clock hours saw traffic. Round-the-clock scores high.

The total is their mean. This mirrors the approach of open-source tools such as RITA (Real Intelligence Threat Analytics), which score beacons on interval and size consistency.

## Worked example

[scripts/generate-conn-log.py](scripts/generate-conn-log.py) writes 24 hours of synthetic connection records for three hosts: a human browsing in working hours, an updater polling every hour, and an implant beaconing every 300 seconds with 20 percent jitter. Tested with Python 3.10, fixed seed, 2026-10:

```bash
python3 scripts/generate-conn-log.py conn.tsv
python3 scripts/score-beaconing.py conn.tsv
```

Output:

```text
source       destination     port conns median gap  skew   mad  size hours  score
192.0.2.22   198.51.100.40    443    24      3600s  0.93  1.00  1.00  1.00  0.98
192.0.2.23   203.0.113.80     443   290       299s  0.98  0.90  0.95  1.00  0.96
192.0.2.21   198.51.100.13    443   129        49s  0.18  0.22  0.40  0.46  0.31
192.0.2.21   198.51.100.11    443   130        41s  0.17  0.25  0.31  0.46  0.30
192.0.2.21   198.51.100.12    443   123        40s  0.12  0.26  0.25  0.46  0.27
192.0.2.21   198.51.100.10    443   132        41s  0.17  0.15  0.16  0.46  0.23
```

The two automated destinations score far above the human browsing (0.9+ versus 0.3 and below). The detector works. But notice the ordering: the hourly *updater* (0.98) scores slightly higher than the *implant* (0.96), because the implant's 20 percent jitter makes its intervals a little less regular than the updater's near-exact hour. This is the key lesson: the score finds automation, not malice. An analyst must then ask the question the statistics cannot: is this destination a known-good updater, or an unknown host? That triage uses asset inventory, [threat intelligence](../../../../security-operations/threat-intelligence/threat-intelligence.md) and the destination's reputation, not the timing alone.

## Trade offs and when to use it

- **Window length.** A short window (an hour) cannot distinguish a beacon from a burst of activity. A long window (a day or more) is needed, which means beaconing detection is a batch job over stored flows, not a real-time alert.
- **Jitter arms race.** More jitter defeats simple interval checks but also slows the attacker's control and still leaves destination and coverage signals. Detectors combine several signals for this reason.
- **Allow-listing.** The only practical way to cut false positives is to maintain a list of known automated destinations (update services, telemetry, certificate checks). This list is maintenance work but turns a noisy detector into a useful one.
- **Encrypted traffic.** Beaconing detection works on metadata (time, size, destination), so TLS does not hide it. This is a reason it remains useful as more traffic encrypts.

## Common mistakes

- **Treating a high score as a verdict.** Fix: rank for triage, then confirm the destination's identity and reputation.
- **Too-short window.** Fix: score over at least a full day; prefer several days.
- **No allow list.** Fix: build and maintain a list of known-good beacons, or the analyst drowns in updater traffic.
- **Scoring only interval, ignoring size and coverage.** A beacon with heavy jitter can still be caught by constant size and 24-hour coverage. Fix: combine signals.
- **Ignoring destinations with few connections.** A very slow beacon (daily) produces few data points. Fix: complement timing analysis with reputation and intelligence for low-volume destinations.

## Practice

1. Why does beaconing detection need a window of a day or more rather than a few minutes?
2. The implant uses jitter, yet still scores high. Which signals catch it despite the jitter?
3. Why does a legitimate software updater score as high as, or higher than, an implant?
4. Why does TLS not defeat beaconing detection?
5. What single piece of operational data most reduces false positives?

### Answers

1. Over a few minutes, a beacon and a short burst of human activity look alike; regularity is only visible over many intervals spanning the daily cycle.
2. Constant connection size, round-the-clock coverage, and still-bounded interval dispersion keep its score high even though the interval varies by 20 percent.
3. The detector measures automation (regular timing, constant size, all-day coverage), which an updater also exhibits; it does not measure whether the destination is malicious.
4. It uses only metadata (timing, size, destination), which is visible regardless of payload encryption.
5. An allow list of known-good automated destinations, so updaters and telemetry do not appear as findings.

## Further reading

- MITRE ATT&CK, Command and Control tactic (TA0011) and Application Layer Protocol (T1071): https://attack.mitre.org/tactics/TA0011/
- Active Countermeasures, RITA (Real Intelligence Threat Analytics), an open-source beacon analyzer: https://www.activecountermeasures.com/free-tools/rita/
- Zeek `conn.log` documentation, the real-world source of the fields the detector uses: https://docs.zeek.org/en/master/logs/conn.html
- MITRE ATT&CK, Non-Standard Port (T1571) and Data Encoding (T1132), related evasions.
