# Command and control traffic

## Summary

Command and control (C2) is the channel an attacker uses to direct compromised hosts: the implant on a victim connects out to the attacker's infrastructure to receive instructions and send back results or stolen data. Detecting and disrupting C2 is one of the highest-value defensive activities, because it sits between the initial compromise and the attacker's objective, and breaking it strands the attacker. On the network, C2 shows up as [beaconing](../monitoring-and-detection/beaconing-detection/README.md) (regular check-ins), traffic to suspicious or new destinations, and protocols chosen to blend in (HTTPS, DNS) or to hide (domain fronting). The defenses are egress control, protective DNS, beaconing and encrypted-traffic analysis, and threat-intelligence matching.

## Prerequisites

- [Beaconing detection](../monitoring-and-detection/beaconing-detection/README.md): the main timing signal, with a tested detector.
- [Egress filtering](../traffic-filtering/egress-filtering.md) and [protective DNS](../dns-security/protective-dns.md): the main disruptions.
- [DNS tunneling](../dns-security/dns-tunneling/README.md) and [encrypted traffic analysis](../monitoring-and-detection/encrypted-traffic-analysis.md).

Authorized use only. Framed for detection and defense.

## Core concepts

### Definition

*Command and control* (MITRE ATT&CK tactic TA0011) is the communication between an attacker and the malware or implants they have placed, used to issue commands, update tooling, and relay results and stolen data. The *C2 channel* is how that communication is carried; the *C2 infrastructure* is the attacker-controlled servers and domains it talks to.

### Analogy

An implant is a planted agent in a building who must receive orders from, and report back to, a handler outside. The handler cannot walk in, so the agent calls out at agreed times. A disciplined agent calls at regular intervals using an ordinary-looking phone line so as not to attract attention. Detecting C2 is noticing that one desk makes a short call to the same outside number every few minutes around the clock, which no real employee does. Cutting the phone line (egress control) strands the agent with no orders.

The analogy is close; it breaks in that the "phone line" is chosen to look exactly like normal traffic (HTTPS to a cloud service), so detection relies on behavior (timing, destination reputation) rather than content.

### How C2 blends in

Attackers choose channels that evade network controls:

- *HTTPS* to attacker servers or compromised sites: encrypted, on port 443, looks like web browsing. The content is hidden, so detection uses metadata and behavior.
- *DNS*: almost always allowed out; used for C2 and exfiltration ([DNS tunneling](../dns-security/dns-tunneling/README.md)).
- *Domain fronting*: the implant connects to a high-reputation CDN domain (in the TLS SNI / HTTP Host) but the request is routed internally to the attacker's service on the same CDN, so the visible destination is a trusted domain. Providers have curtailed it, but the technique illustrates the evasion goal.
- *Legitimate services as C2*: using cloud storage, collaboration or social platforms as dead drops, so traffic goes to a trusted, allowed destination.
- *Non-standard ports and custom protocols* (MITRE T1571, T1095): less stealthy but used where egress is permissive.

### The detectable signatures

Despite blending in, C2 leaves patterns:

- *Beaconing*: regular check-ins, the strongest timing signal, detectable even over TLS because it is metadata (see the tested [beaconing detector](../monitoring-and-detection/beaconing-detection/README.md)).
- *Destination reputation*: new, rare, or known-bad domains and IPs; newly registered domains; mismatches between SNI and certificate.
- *TLS fingerprints*: the implant's TLS client often has a distinctive fingerprint (JA3/JA4) different from browsers, detectable by [encrypted traffic analysis](../monitoring-and-detection/encrypted-traffic-analysis.md).
- *Volume and direction*: small regular outbound with occasional larger uploads (exfiltration) to one destination.

### Why disrupting C2 is high-value

C2 sits in the middle of the attack: after the foothold, before the objective is fully achieved (data staged and exfiltrated, ransomware coordinated). Breaking C2 strands the implant, buying time and preventing the attacker from directing the next steps. Because the implant must reach out, the defender's outbound controls (egress filtering, protective DNS) are exactly the choke points, which is why controlling egress is disproportionately valuable.

## Worked example

Detecting a C2 beacon with the tested [beaconing detector](../monitoring-and-detection/beaconing-detection/README.md) (Python 3.10, fixed seed, 2026-10) over a day of connection logs:

```text
source       destination     port conns median gap  skew   mad  size hours  score
192.0.2.23   203.0.113.80     443   290       299s  0.98  0.90  0.95  1.00  0.96
```

Reading it: host `192.0.2.23` connects to `203.0.113.80:443` every ~300 seconds, round the clock, with near-constant small sizes, a strong beacon score despite the traffic being HTTPS and therefore opaque to content inspection. The timing and destination, not the payload, give it away. The analyst then checks the destination's reputation: a new or unknown domain confirms suspicion; a known update service would be an allow-list entry.

Disruption follows detection:

1. **Protective DNS** sinkholes the C2 domain if it resolves by name, immediately cutting the channel and revealing which internal hosts beacon to it.
2. **Egress filtering** blocks the outbound connection to the destination; on a default-deny egress the beacon never succeeds in the first place.
3. **Encrypted traffic analysis** flags the implant's non-browser TLS fingerprint on 443 even without decryption.

The combination detects the beacon by behavior and cuts it at the egress, stranding the implant.

## Detection and mitigation

- **Egress filtering** (default-deny outbound) is the primary disruption: the implant cannot reach its C2 if the destination is not allowed. See [egress filtering](../traffic-filtering/egress-filtering.md).
- **Protective DNS** blocks and sinkholes known and heuristically-bad C2 domains, cutting name-based channels and revealing infected hosts. See [protective DNS](../dns-security/protective-dns.md).
- **Beaconing detection** finds the regular check-in pattern even over TLS, from flow metadata. See [beaconing detection](../monitoring-and-detection/beaconing-detection/README.md).
- **Encrypted traffic analysis** (JA3/JA4, SNI, certificate metadata) flags non-browser C2 clients without decryption. See [encrypted traffic analysis](../monitoring-and-detection/encrypted-traffic-analysis.md).
- **Threat intelligence** matching of destinations against known C2 infrastructure.
- **Block known evasions**: restrict DNS to controlled resolvers (DNS C2 and DoH bypass), and be aware of domain fronting and legitimate-service C2 in detection logic.

## Trade offs and when to use it

- **Block vs observe.** Immediately blocking C2 stops the attack but tips off the attacker; in a mature response, defenders sometimes observe a sinkholed or contained channel to scope the intrusion before cutting it. Decide per incident.
- **Egress strictness.** Default-deny egress is the strongest C2 disruptor but requires knowing legitimate outbound flows; the payoff against C2 and exfiltration is large.
- **Behavior vs content.** Since C2 is usually encrypted, invest in behavioral and metadata detection (beaconing, reputation, fingerprints) rather than content inspection, which TLS defeats.
- **False positives.** Legitimate software beacons too (updaters, telemetry); allow-listing known-good destinations is required to make beacon detection usable.

## Common mistakes

- **Permissive egress.** Lets implants reach any C2. Fix: default-deny egress, allow by exception.
- **Relying on content inspection for C2.** C2 is mostly encrypted. Fix: behavioral and metadata detection (beaconing, reputation, TLS fingerprints).
- **Allowing direct outbound DNS.** Enables DNS C2 and DoH bypass of protective DNS. Fix: force DNS through controlled resolvers.
- **No destination reputation or intel.** Misses connections to new/known-bad infrastructure. Fix: integrate threat intelligence and newly-registered-domain heuristics.
- **No allow list for beaconing.** Updater traffic floods the analyst. Fix: maintain known-good beacon destinations.

## Practice

1. Why is disrupting C2 described as high-value in the attack lifecycle?
2. Why does beaconing detection still work when the C2 channel is HTTPS?
3. What is domain fronting, and what does it try to hide?
4. Which outbound controls are the main choke points for C2, and why?
5. Why must beaconing detection be paired with an allow list?

### Answers

1. C2 sits between the initial compromise and the attacker achieving their objective; breaking it strands the implant so the attacker cannot direct further actions, preventing or delaying the real damage.
2. Beaconing is a timing-and-metadata signal (regular check-ins, constant sizes, round-the-clock) that is visible regardless of payload encryption, so TLS does not hide it.
3. Connecting to a high-reputation CDN domain in the visible fields (SNI/Host) while the request is routed internally to the attacker's service on that CDN, hiding the true destination behind a trusted domain.
4. Egress filtering and protective DNS, because the implant must reach outward to its C2, so controlling and blocking outbound connections and name resolution cuts the channel at its necessary choke point.
5. Legitimate software (updaters, telemetry) also beacons and scores highly; without an allow list of known-good destinations, the detector overwhelms analysts with benign findings.

## Further reading

- MITRE ATT&CK, Command and Control tactic (TA0011), Application Layer Protocol (T1071), Protocol Tunneling (T1572): https://attack.mitre.org/tactics/TA0011/
- [Beaconing detection](../monitoring-and-detection/beaconing-detection/README.md) and [encrypted traffic analysis](../monitoring-and-detection/encrypted-traffic-analysis.md) for the detection methods.
- Active Countermeasures RITA and similar open-source C2-detection tooling.
- CISA advisories on specific C2 frameworks and infrastructure.
