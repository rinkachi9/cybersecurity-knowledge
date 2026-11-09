# Data exfiltration

## Summary

Data exfiltration is the unauthorized transfer of data out of an organization, the payoff stage of many intrusions. On the network it takes many forms: bulk uploads over HTTPS to attacker or cloud storage, slow trickles hidden in [DNS](../dns-security/dns-tunneling/README.md) or ICMP, staging data and sending it through the [command-and-control channel](command-and-control-traffic.md), or using legitimate file-sharing services as the exit. The defender's leverage is that data must leave the network to be stolen, so outbound controls, [egress filtering](../traffic-filtering/egress-filtering.md), protective DNS, data-loss prevention and volume/anomaly detection, are the choke points. The hard part is distinguishing malicious exfiltration from the large volumes of legitimate outbound data in a cloud-centric world.

## Prerequisites

- [Egress filtering](../traffic-filtering/egress-filtering.md): the main network control.
- [DNS tunneling](../dns-security/dns-tunneling/README.md) and [command and control traffic](command-and-control-traffic.md): common channels.
- [Network security monitoring](../monitoring-and-detection/network-security-monitoring.md) and [flow monitoring](../monitoring-and-detection/flow-monitoring.md).

Authorized use only. Framed for detection and defense.

## Core concepts

### Definition

*Data exfiltration* (MITRE ATT&CK tactic TA0010) is the theft of data by transferring it from a controlled environment to one the attacker controls. It is distinct from the damage of destruction or encryption (ransomware); exfiltration is about copying data out, increasingly paired with ransomware as "double extortion".

### Analogy

Exfiltration is smuggling documents out of a secure facility. A thief might carry out a big box at once (bulk upload, easy to notice at the exit), smuggle a few pages at a time in their lunch (slow trickle over DNS or ICMP), hide them in outgoing mail that is normally allowed (legitimate cloud services), or pass them to an accomplice who was already receiving regular small deliveries (the C2 channel). The guard at the exit who checks what leaves (egress control and DLP) is the defender's best position, because the documents must physically leave to be stolen.

The analogy holds well; the break is that network data can be disguised, compressed and encrypted so the "documents" are unrecognizable at the exit unless the guard inspects deeply or watches volumes and destinations.

### The channels

| Channel | How | Detection angle |
| --- | --- | --- |
| HTTPS upload | Bulk POST/PUT to attacker server or cloud storage | Volume to new/rare destinations; DLP (needs inspection) |
| C2 channel | Data staged then sent through the existing C2 | Beaconing plus larger uploads to the C2 destination |
| DNS tunneling | Encode data in query names | High unique-name volume to one domain ([detector](../dns-security/dns-tunneling/README.md)) |
| ICMP tunneling | Data in echo payloads | Unusual echo size/volume ([ICMP security](../core-protocols/icmp-security.md)) |
| Legitimate services | Cloud storage, email, collaboration, code repos | Allowed destination; needs DLP and anomaly on volume/behavior |
| Physical / out-of-band | USB, printouts | Endpoint/DLP, not network |

The sophistication ranges from a noisy bulk upload to a patient low-and-slow trickle that stays under volume thresholds. Attackers often compress and encrypt data first, so content inspection sees opaque blobs and detection leans on destination and volume.

### Why outbound control is the leverage

Whatever the channel, the data must leave, so the outbound path is where the defender has the advantage:

- [Egress filtering](../traffic-filtering/egress-filtering.md) with default-deny means data can only leave through allowed destinations, shrinking the exit options and making unusual outbound attempts visible.
- [Protective DNS](../dns-security/protective-dns.md) and forced resolvers cut DNS tunneling and name-based exfiltration.
- Blocking direct outbound and routing through a [secure web gateway](../traffic-filtering/proxies-and-secure-web-gateways.md) with DLP inspects and controls web uploads.
- Flow monitoring reveals abnormal upload volumes and destinations.

### The hard part: legitimate traffic

In a cloud-centric organization, huge volumes of data legitimately leave every day (backups, SaaS, cloud sync, collaboration). This makes exfiltration detection hard: the signal hides in a large, noisy baseline. The practical approach is baselining (what is normal for this host/user) and alerting on deviation (a workstation that normally uploads megabytes suddenly uploading gigabytes, or to a new destination), plus DLP matching on sensitive content where inspection is possible, plus controlling which destinations are allowed at all.

## Worked example

An attacker has compromised a host and wants to steal a database. Two channels and their detection:

1. **Bulk HTTPS upload.** The attacker compresses the dump and uploads it to a cloud storage bucket over HTTPS. Detection: flow monitoring shows an abnormally large outbound transfer from a server that normally uploads little, to a destination it has never contacted. Egress policy that allows the server outbound only to specific services would have blocked it outright; DLP at the [secure web gateway](../traffic-filtering/proxies-and-secure-web-gateways.md) could match the sensitive content if inspected.
2. **Low-and-slow DNS tunnel.** To avoid volume alerts, the attacker instead trickles the data out over DNS over hours. Detection: the [DNS tunneling detector](../dns-security/dns-tunneling/README.md) flags one domain receiving a huge number of long, high-entropy unique query names from one host, moving tens of kilobytes into names, far outside normal DNS behavior. Forcing DNS through the controlled resolver (and blocking direct 53) is what makes this visible and blockable.

In both cases the data had to leave, and the outbound controls, egress policy, DLP, resolver control, flow baselining, are where it was caught or prevented. The example also shows the attacker's trade-off: fast and noisy versus slow and stealthy, each caught by a different outbound control.

## Detection and mitigation

- **Egress filtering (default-deny outbound)** limits exit destinations and surfaces unusual attempts. The primary control. See [egress filtering](../traffic-filtering/egress-filtering.md).
- **Data-loss prevention (DLP)** inspects outbound content (at the [secure web gateway](../traffic-filtering/proxies-and-secure-web-gateways.md) or endpoint) for sensitive patterns and blocks it; requires inspection, with the usual TLS trade-offs.
- **Protective DNS and resolver control** cut DNS tunneling and name-based exfiltration. See [protective DNS](../dns-security/protective-dns.md).
- **Flow baselining and anomaly detection** catch abnormal upload volumes and new destinations, even for encrypted traffic. See [flow monitoring](../monitoring-and-detection/flow-monitoring.md).
- **Tunneling detectors** for DNS and ICMP channels.
- **Segmentation** so a compromised host can reach and stage less data in the first place.

## Trade offs and when to use it

- **DLP coverage vs inspection cost.** Content-based DLP is powerful but needs decryption (TLS inspection trade-offs) and tuning to avoid false positives; destination and volume controls work without decryption and should be the baseline.
- **Strict egress vs cloud reality.** Default-deny egress is strongest but friction-heavy in a SaaS-heavy environment; apply it strictly to servers and sensitive segments, and use baselining/anomaly detection where broad outbound is unavoidable.
- **Block vs observe.** As with C2, defenders may observe a contained exfiltration attempt to scope an intrusion before cutting it; decide per incident.
- **Fast vs slow attacker.** Volume detection catches bulk transfers; tunnel/behavioral detection catches low-and-slow; you need both because the attacker will pick whichever you lack.

## Common mistakes

- **Permissive egress and no DLP.** Data can leave anywhere unexamined. Fix: default-deny egress for sensitive systems, DLP at the gateway.
- **Only volume-based detection.** Misses low-and-slow tunneling. Fix: add DNS/ICMP tunnel detectors and behavioral analysis.
- **Allowing direct outbound DNS.** Enables DNS exfiltration and bypasses protective DNS. Fix: force DNS through controlled resolvers.
- **No baseline of normal outbound.** Cannot tell abnormal from normal in a noisy cloud environment. Fix: baseline per host/user and alert on deviation.
- **Ignoring legitimate-service exfiltration.** Data leaves via allowed cloud apps. Fix: CASB/DLP on sanctioned services, monitor volume and behavior.

## Practice

1. Why is the outbound path the defender's point of leverage against exfiltration?
2. What is the attacker's trade-off between bulk upload and low-and-slow tunneling, and which control catches each?
3. Why is exfiltration detection especially hard in a cloud-centric organization?
4. Why does controlling DNS resolution matter for exfiltration, not just for C2?
5. Which outbound controls work without decrypting traffic?

### Answers

1. The data must leave the network to be stolen, so outbound connections, destinations and volumes are the necessary choke point where egress filtering, DLP, resolver control and flow monitoring can see and stop it.
2. Bulk upload is fast but creates an abnormal volume spike caught by flow baselining; low-and-slow tunneling stays under volume thresholds but creates a tunnel pattern (many long high-entropy DNS names, odd ICMP) caught by tunnel/behavioral detectors.
3. Large volumes of data legitimately leave every day (backups, SaaS, cloud sync), so malicious exfiltration hides in a noisy baseline and cannot be found by volume alone without per-host/user baselining and destination control.
4. DNS can itself be an exfiltration channel (tunneling data in query names), so forcing DNS through controlled resolvers and blocking direct port 53 both detects and blocks that channel.
5. Egress filtering by destination/port, protective DNS and resolver control, flow volume/destination baselining, and DNS/ICMP tunnel detection all operate on metadata and need no content decryption.

## Further reading

- MITRE ATT&CK, Exfiltration tactic (TA0010), Exfiltration Over Alternative Protocol (T1048), Exfiltration Over C2 Channel (T1041): https://attack.mitre.org/tactics/TA0010/
- [Egress filtering](../traffic-filtering/egress-filtering.md), [DNS tunneling](../dns-security/dns-tunneling/README.md) and [flow monitoring](../monitoring-and-detection/flow-monitoring.md) for the controls.
- NIST SP 800-137, Information Security Continuous Monitoring, for the monitoring foundation: https://doi.org/10.6028/NIST.SP.800-137
- CISA guidance on data exfiltration and double-extortion ransomware.
