# Network incident response

## Summary

Network incident response is the network-specific side of handling a security incident: using network data to detect and scope an intrusion, containing it at the network level, preserving network evidence, and recovering connectivity safely. The general incident-response lifecycle is covered in the defensive-operations area; this note focuses on what the network team does within it. The network is often where an incident is first seen (anomalous traffic, a detection alert) and where fast containment is possible (isolate a host, block a destination, cut a segment), and network data (flows, logs, captures) is central to understanding what happened. The recurring tension is containment speed versus evidence preservation and versus tipping off the attacker.

## Prerequisites

- [NIST incident response lifecycle (SP 800-61)](../../../security-operations/defensive-operations/operations/nist-incident-response/README.md): the overall process this fits into.
- [Network security monitoring](../monitoring-and-detection/network-security-monitoring.md) and [flow monitoring](../monitoring-and-detection/flow-monitoring.md): the data used.
- [Network segmentation](../architecture/network-segmentation.md) and [management plane security](../architecture/management-plane-security.md): what enables containment.

## Core concepts

### Definition

*Network incident response* is the set of network-focused activities within incident handling: network-based detection and scoping, network containment (isolation and blocking), network evidence preservation, and safe recovery of connectivity. It operates inside the full lifecycle (preparation, detection and analysis, containment/eradication/recovery, post-incident), not as a separate process.

### Analogy

If an incident is a fire in a building, the network team runs the compartment doors, the sensors and the floor plan. They see where the smoke is (detection), close specific fire doors to stop it spreading (network containment), keep the sensor logs for the investigation (evidence), and decide when it is safe to reopen each area (recovery), all while the overall incident commander runs the response. Shutting every door at once stops the fire but also traps information about how it started.

The analogy holds well; it carries the containment-versus-evidence tension that defines network IR decisions.

### The network team's role in each phase

| Phase | Network-specific activity |
| --- | --- |
| Preparation | Visibility (sensors, [flow](../monitoring-and-detection/flow-monitoring.md)/[Zeek](../monitoring-and-detection/zeek.md) logs, retention), out-of-band management, pre-planned isolation methods, runbooks |
| Detection and analysis | Network detection (alerts, [beaconing](../monitoring-and-detection/beaconing-detection/README.md), anomalies); scope the intrusion by pivoting through flow/DNS/connection logs |
| Containment | Isolate hosts (NAC quarantine, switch port, host firewall), block C2 destinations ([egress](../traffic-filtering/egress-filtering.md), [protective DNS](../dns-security/protective-dns.md) sinkhole), cut or tighten a segment |
| Eradication and recovery | Remove network footholds (rogue accounts/rules on devices), restore connectivity in stages, verify the threat is gone before reopening |
| Post-incident | Turn findings into new detections and segmentation/rule changes; update runbooks |

### Scoping with network data

A core network-IR task is answering "how far did it get?" Network data is uniquely suited to this because it records communication regardless of what happened on each host:

- [Flow records](../monitoring-and-detection/flow-monitoring.md): every host the compromised system talked to, and how much, over the retention window, revealing [lateral movement](../network-attacks/lateral-movement.md) and [exfiltration](../network-attacks/data-exfiltration.md).
- [Zeek](../monitoring-and-detection/zeek.md) logs: the domains resolved, certificates seen, files transferred.
- This is why long retention of compact network data (flows, logs) is a preparation decision that pays off during an incident discovered weeks later.

### Network containment options

The network offers fast, powerful containment:

- *Isolate the host*: NAC quarantine VLAN, disable the switch port, or host-firewall isolation (via EDR). Stops the host communicating while preserving it for forensics.
- *Block the destination*: egress rule or [protective DNS](../dns-security/protective-dns.md) sinkhole cuts [C2](../network-attacks/command-and-control-traffic.md) across all hosts and reveals others reaching it.
- *Tighten or cut a segment*: restrict or sever a [segment](../architecture/network-segmentation.md) to stop spread, at the cost of disrupting legitimate traffic there.

### The three tensions

Network IR decisions balance three things:

1. *Speed vs evidence*: pulling a host's network cable stops the bleeding but can lose volatile evidence and tip the attacker; isolating it (still powered, network-quarantined) usually preserves more.
2. *Containment vs business*: cutting a segment stops spread but halts legitimate work there; scope containment as narrowly as the threat allows.
3. *Act vs observe*: immediately blocking C2 stops the attack but tells the attacker they are detected; a mature response may briefly observe (contained) to scope fully before cutting. The choice depends on the threat's severity and the maturity of the response.

Out-of-band [management access](../architecture/management-plane-security.md) matters here: containment and recovery often require reconfiguring devices exactly when the production network is compromised or disrupted, and the OOB path lets the team act without relying on the affected network.

## Worked example

A network team responds to a detected C2 beacon (building on the [C2](../network-attacks/command-and-control-traffic.md) and [beaconing](../monitoring-and-detection/beaconing-detection/README.md) notes):

1. **Detection.** The [beaconing detector](../monitoring-and-detection/beaconing-detection/README.md) flags host `192.0.2.23` beaconing to `203.0.113.80`; a malicious [JA3/JA4](../monitoring-and-detection/encrypted-traffic-analysis.md) confirms C2.
2. **Scope.** Before acting, the team queries [flow](../monitoring-and-detection/flow-monitoring.md) and [Zeek](../monitoring-and-detection/zeek.md) data: which other hosts contacted `203.0.113.80` (other infections), and what `192.0.2.23` talked to internally (lateral movement) and uploaded (exfiltration). They find two more hosts beaconing to the same destination.
3. **Contain.** They sinkhole the C2 domain via [protective DNS](../dns-security/protective-dns.md) and add an [egress](../traffic-filtering/egress-filtering.md) block, cutting all three hosts' C2 at once, and NAC-quarantine the three hosts (network-isolated but powered, for forensics). They deliberately contain all known infected hosts together so the attacker does not notice one dropping and burrow deeper from the others.
4. **Preserve evidence.** Retained flow and Zeek logs plus a targeted packet capture are saved for the investigation; the quarantined hosts are imaged by the forensics team.
5. **Recover.** After eradication (hosts rebuilt), connectivity is restored in stages, with monitoring watching for re-beaconing before full reopening.
6. **Post-incident.** The beacon pattern and fingerprint become a standing detection; an [egress](../traffic-filtering/egress-filtering.md) gap that allowed the C2 is closed.

The example shows the network team scoping before containing, containing all infected hosts together, preserving evidence, and feeding the lessons back, inside the overall incident process.

## Trade offs and when to use it

- **Speed vs evidence/stealth.** Fast containment stops damage but can lose evidence and tip the attacker; isolation (quarantine, not cable-pull) and contained observation balance this. Decide by severity.
- **Narrow vs broad containment.** Isolating specific hosts and blocking specific destinations is least disruptive; cutting segments is stronger but halts legitimate work. Scope to the threat.
- **Contain all at once vs piecemeal.** Containing all known-infected hosts together prevents the attacker reacting to a partial takedown; it requires having scoped first.
- **Preparation pays off.** Visibility, retention, OOB access and runbooks decided in calm times are what make fast, correct IR possible under pressure.

## Common mistakes

- **Containing before scoping.** Blocking one host while missing two others, and tipping the attacker. Fix: scope with network data first, then contain known-infected together.
- **Cable-pull destroying evidence.** Loses volatile data and alerts the attacker. Fix: network-quarantine while preserving the host.
- **No retained network data.** Cannot scope an intrusion found late. Fix: keep flows and logs for months (a preparation decision).
- **No out-of-band access.** Cannot reconfigure devices when the network is down or compromised. Fix: OOB management path.
- **No feedback loop.** The same intrusion recurs undetected. Fix: convert findings into detections and segmentation/egress fixes post-incident.

## Practice

1. Why is the network often both where an incident is first seen and where fast containment is possible?
2. Why scope an intrusion with network data before containing it?
3. What are the three tensions in network containment decisions?
4. Why isolate a host (network quarantine) rather than pull its cable?
5. Why is long retention of flow and Zeek data a preparation decision that matters during an incident?

### Answers

1. Network detection (alerts, beaconing, anomalies) frequently surfaces an intrusion, and the network offers fast, powerful containment levers (isolate a host, block a destination, cut a segment) that can stop communication immediately.
2. To find all infected hosts and the attacker's reach (lateral movement, exfiltration) so containment covers everything at once; containing piecemeal misses hosts and warns the attacker.
3. Speed vs evidence preservation, containment vs business disruption, and acting (blocking) vs observing to scope without tipping off the attacker.
4. Quarantining keeps the host powered and its volatile evidence intact for forensics and avoids abruptly signalling the attacker, whereas a cable-pull loses evidence and tips them off.
5. An intrusion is often discovered weeks after it began; retained compact network data is what lets the team reconstruct what happened and scope the full extent, which is impossible if the data was not kept.

## Further reading

- [NIST incident response lifecycle (SP 800-61)](../../../security-operations/defensive-operations/operations/nist-incident-response/README.md): the full process.
- NIST SP 800-61 Rev. 3 (2025) and SP 800-86, Guide to Integrating Forensic Techniques into Incident Response: https://doi.org/10.6028/NIST.SP.800-86
- [Network security monitoring](../monitoring-and-detection/network-security-monitoring.md) and [flow monitoring](../monitoring-and-detection/flow-monitoring.md) for the data that drives scoping.
- SANS incident-handling materials for network containment and evidence handling.
