# Network threat hunting

## Summary

Network threat hunting is the proactive search through network data for threats that automated detection missed. Instead of waiting for an alert, a hunter forms a hypothesis about how an attacker might operate, then queries [network security monitoring](network-security-monitoring.md) data ([flows](flow-monitoring.md), [Zeek](zeek.md) logs, DNS, TLS metadata) to confirm or refute it. Hunting matters because signatures and behavioral tools catch only what they are built to catch; a skilled adversary operating below those thresholds is found only by someone actively looking. Good hunting is hypothesis-driven and repeatable: a successful hunt that finds a pattern becomes a new automated detection.

## Prerequisites

- [Network security monitoring](network-security-monitoring.md), [flow monitoring](flow-monitoring.md) and [Zeek](zeek.md): the data hunted through.
- [Command and control traffic](../network-attacks/command-and-control-traffic.md), [lateral movement](../network-attacks/lateral-movement.md), [data exfiltration](../network-attacks/data-exfiltration.md): what is hunted for.
- [MITRE ATT&CK](../../../security-operations/threat-intelligence/mitre/mitre-attack.md): the hypothesis framework.

## Core concepts

### Definition

*Threat hunting* is the proactive, hypothesis-driven search for threats that have evaded existing detection. *Network* threat hunting does this in network data specifically. It assumes a breach may already be present and undetected, and sets out to find it rather than waiting to be alerted.

### Analogy

Automated detection is a set of tripwires and alarms; threat hunting is a detective who, suspecting a thief slipped past the alarms, walks the building looking for signs, a forced window the sensor missed, muddy footprints, a door left ajar. The detective does not search randomly: they reason about how a thief would move and where they would leave traces, then look there. When they find a new sign of intrusion, they add a tripwire so next time it triggers automatically.

The analogy holds closely; the key point it carries is that hunting is reasoned, not random, and its output feeds back into automation.

### Hypothesis-driven, not random

Effective hunting starts with a hypothesis, usually derived from:

- *Threat intelligence*: a report describes an adversary's technique; the hunter asks "would we see this in our data?"
- *[MITRE ATT&CK](../../../security-operations/threat-intelligence/mitre/mitre-attack.md)*: pick a technique (say T1071, Application Layer Protocol for C2) and hunt for its traces.
- *Knowledge of the environment*: "a database server should never make outbound internet connections, let us check whether any did."
- *Anomalies*: something odd in the data worth pulling on.

The hunter then translates the hypothesis into concrete queries over the network data and investigates the results.

### What network data supports hunting

| Data | Hunts it supports |
| --- | --- |
| [Flow records](flow-monitoring.md) | Beaconing, unusual destinations, volume anomalies, fan-out |
| [Zeek](zeek.md) `conn/dns/http/ssl` logs | Protocol-level patterns, rare domains, odd user agents, certificate anomalies |
| DNS logs | [Tunneling](../dns-security/dns-tunneling/README.md), DGA domains, newly registered domains |
| TLS/cert metadata | Malicious [JA3/JA4](encrypted-traffic-analysis.md), self-signed certs, SNI mismatches |
| Alerts (context) | Pivot points to investigate further |

The behavioral detectors in this subarea (the [beaconing](beaconing-detection/README.md) and [DNS-tunnel](../dns-security/dns-tunneling/README.md) scripts) are essentially encapsulated hunts: they implement a hypothesis ("C2 beacons regularly", "tunnels push data into names") as a repeatable query.

### Hunting feeds detection

The output of a successful hunt is not just a found threat but a *new detection*. When a hunter discovers a pattern that indicates malice, they turn it into an automated rule or analytic so it is caught without a human next time. This is the maturity loop: hunt finds the novel, automation catches the now-known, freeing hunters to look for the next novel thing. A hunting program that never produces new detections is not maturing.

## Worked example

A hunt for C2 that evaded signature detection, using this subarea's data and tools:

1. **Hypothesis.** From a threat report: an adversary uses HTTPS beaconing to a cloud-hosted C2 with jittered intervals. Hypothesis: "a compromised host here beacons over HTTPS with regular-but-jittered timing to a rare destination."
2. **Query.** The hunter runs the [beaconing detector](beaconing-detection/README.md) over a week of [flow](flow-monitoring.md)/`conn.log` data. It ranks destination pairs by regularity; the tested output format:

```text
192.0.2.23   203.0.113.80   443   ...   0.96   <- candidate beacon
192.0.2.22   198.51.100.40  443   ...   0.98   <- known updater (allow-listed)
```

3. **Triage.** The hunter allow-lists the known updater and investigates the remaining high scorer: the destination is a newly registered domain with no business purpose, and [Zeek](zeek.md) `ssl.log` shows a non-browser [JA3/JA4](encrypted-traffic-analysis.md) fingerprint, corroborating C2.
4. **Confirm and respond.** Endpoint data (via [NDR/XDR](network-detection-and-response.md)) confirms a malicious process; the host is contained and the incident scoped by pivoting through flow and DNS logs to find other affected hosts.
5. **Feed back.** The hunter turns the finding into automation: the beacon score threshold plus the malicious fingerprint and newly-registered-domain condition become a standing detection, so the next instance alerts automatically.

The example shows the full loop: hypothesis, query over NSM data, triage with corroborating signals, response, and conversion into a new detection.

## Trade offs and when to use it

- **Proactive vs resource cost.** Hunting finds what automation misses but needs skilled analysts and good data; it is a mature-program activity, worthwhile once basic detection and NSM data exist.
- **Hypothesis-driven vs exploratory.** Hypothesis-driven hunts are efficient and repeatable; purely exploratory "looking around" occasionally finds things but is hard to scale. Favor hypotheses, keep some room for curiosity.
- **Data breadth vs noise.** Rich data (Zeek, flows, DNS, TLS) enables deep hunts but is large; good retention and queryable storage (a SIEM/data lake) are prerequisites.
- **Output discipline.** A hunt that finds nothing still has value (it refutes a hypothesis and may improve data), but a program should regularly convert findings into detections to justify itself.

## Common mistakes

- **Random hunting with no hypothesis.** Inefficient and unrepeatable. Fix: start from threat intel, ATT&CK techniques or environment knowledge.
- **Hunting without the data.** No flows, logs or retention means nothing to query. Fix: build NSM data collection and retention first.
- **Not feeding findings back into automation.** The same threat must be re-hunted. Fix: convert every confirmed pattern into a detection.
- **Ignoring allow-listing.** Benign automation (updaters) buries real findings. Fix: maintain allow lists so hunts surface the unknown.
- **Treating hunting as a substitute for detection.** It complements, not replaces, automated detection and good hygiene. Fix: hunt on top of a solid detection baseline.

## Practice

1. How does threat hunting differ from automated detection?
2. Why is hunting hypothesis-driven rather than random, and where do hypotheses come from?
3. How do the beaconing and DNS-tunnel detectors in this subarea relate to hunting?
4. Why should a hunt's findings be converted into automated detections?
5. What are the prerequisites before a hunting program is worthwhile?

### Answers

1. Automated detection waits for pre-defined patterns to trigger alerts; hunting proactively searches the data for threats that evaded those patterns, assuming a breach may already be present and undetected.
2. Random searching does not scale and is not repeatable; hypotheses (from threat intelligence, MITRE ATT&CK techniques, environment knowledge, or anomalies) focus the search on where an attacker would leave traces and make it repeatable.
3. They are encapsulated hunts: each implements a hypothesis (regular C2 beacons; tunnels pushing data into DNS names) as a repeatable query over NSM data, exactly what a hunter runs.
4. So the same threat is caught automatically next time, freeing hunters to look for the next novel threat; converting findings into detections is how the program matures.
5. Skilled analysts, and collected, retained, queryable NSM data (flows, Zeek logs, DNS, TLS metadata) on top of a solid automated-detection baseline.

## Further reading

- [MITRE ATT&CK](../../../security-operations/threat-intelligence/mitre/mitre-attack.md) as the hypothesis source for technique-based hunts.
- The SANS and Sqrrl threat-hunting maturity models and the hunting loop.
- [Network security monitoring](network-security-monitoring.md), [Zeek](zeek.md) and [flow monitoring](flow-monitoring.md) for the data foundation.
- [Threat intelligence](../../../security-operations/threat-intelligence/threat-intelligence.md) for feeding hunts.
