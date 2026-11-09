# Egress filtering

## Summary

Egress filtering controls what traffic may leave a network, in contrast to the usual focus on what may enter. It matters because almost every stage of an attack after the initial foothold reaches outward: malware downloading its payload, calling home to command-and-control, and exfiltrating data all require outbound connections. A default-deny egress policy that permits only known, necessary destinations and protocols breaks these steps and turns outbound attempts into high-fidelity alerts. Most networks filter ingress carefully and allow almost any egress, which is exactly the gap attackers rely on. Egress filtering also stops a compromised host being used for spoofing and reflection against others.

## Prerequisites

- [Firewalls](firewalls.md) and [firewall rule design](firewall-rule-design/README.md).
- [Command and control traffic](../network-attacks/command-and-control-traffic.md) and [data exfiltration](../network-attacks/data-exfiltration.md): what egress filtering disrupts.
- [IP spoofing and source address validation](../core-protocols/ip-spoofing-and-source-validation.md).

## Core concepts

### Definition

*Egress filtering* is the enforcement of policy on traffic leaving a network or host: which internal sources may reach which external destinations, on which protocols and ports, and the default denial of everything else. It is the outbound counterpart to ingress filtering.

### Analogy

Most buildings guard who comes in but let anyone leave with anything. Egress filtering is checking what goes out the door: a thief who got inside still cannot walk out with the safe, cannot signal accomplices outside, and cannot use the building's phone to call unknown numbers. The checks at the exit catch the parts of a crime that happen after the break-in, which is most of it.

The analogy holds well; it breaks in that network egress can be disguised (tunneling inside allowed protocols), so exit checks must look at protocol and destination, not just "is the door open".

### Why outbound is where attacks live

The stages of a typical intrusion after initial access are almost all outbound:

- *Tool download*: the initial foothold fetches the real payload from the internet.
- *Command and control*: the implant connects out to receive instructions ([beaconing](../monitoring-and-detection/beaconing-detection/README.md)).
- *Exfiltration*: stolen data is sent out.
- *Pivoting and reflection*: a compromised host attacks others or spoofs traffic outward.

A permissive egress policy ("internal hosts may connect anywhere on any port") allows all of these. A restrictive one forces the attacker to work within the few allowed paths, each of which can be monitored.

### What a default-deny egress policy looks like

- Only specific internal hosts may make outbound connections, and only to needed destinations and ports.
- General user web traffic goes through a [proxy or secure web gateway](proxies-and-secure-web-gateways.md), not directly; direct outbound 80/443 from arbitrary hosts is blocked.
- DNS goes only to controlled resolvers; direct outbound port 53 to the internet is blocked (see [protective DNS](../dns-security/protective-dns.md) and the DoH bypass concern in [encrypted DNS](../dns-security/encrypted-dns.md)).
- Servers egress only to the specific updates, APIs and services they require; a database server usually needs almost no outbound internet access.
- Anti-spoofing: outbound packets with a source address not belonging to the network are dropped (BCP 38).
- Denied egress is logged, because an internal host trying to reach a blocked destination is a strong indicator of compromise or misconfiguration.

### Egress filtering as detection

Beyond prevention, egress filtering is a detection goldmine. When the baseline is "only these flows are allowed", any blocked outbound attempt stands out: a workstation trying to reach an unknown IP on a high port, a server suddenly connecting to the internet, a host querying an external DNS resolver directly. These are far higher-fidelity signals than trying to spot malicious traffic in a sea of permitted outbound connections.

## Worked example

This uses the [network security lab](../foundations/network-security-lab/README.md). The baseline firewall policy already includes an egress rule: the internal web server may initiate connections only to the DNS resolver, and nothing else:

```
iifname "eth1" ip saddr 198.51.100.20 ip daddr 192.0.2.53 udp dport 53 ct state new accept comment "server dns"
# everything else outbound from the server hits the default drop + log
```

Tested behavior (nftables 1.0.2, 2026-10): the server's permitted flow works, and any other outbound connection from the server is dropped and counted by the default-policy counter on the forward chain. In the port-probe test, outbound attempts from the inside that are not in the allow list are blocked, and the drop counter increments:

```text
counter packets 4 bytes 240 comment "dropped by default policy"
```

Reading it: the server is constrained to exactly the outbound flow it needs. If that server were compromised, the implant could not download tools from an arbitrary internet host, could not beacon to an external C2 address, and could not exfiltrate over an arbitrary port; it would be confined to DNS to one resolver, and every blocked attempt would be logged as an alert. This is the containment and detection value of egress filtering in miniature.

## Trade offs and when to use it

- **Security vs operational friction.** Default-deny egress is powerful but requires knowing every legitimate outbound dependency; undiscovered ones break when the policy tightens. Use observe-then-enforce, as with [microsegmentation](../architecture/microsegmentation.md).
- **Servers vs user networks.** Servers have well-defined, limited egress needs and should be filtered strictly. User networks have broad, changing needs and are usually filtered via a proxy/SWG with category policy rather than a static allow list.
- **Proxy-based vs firewall-based.** A proxy gives per-URL and per-category control and logging for web traffic; firewall egress rules give coarse destination/port control. Use both: proxy for user web, firewall default-deny for everything else.
- **Encrypted DNS and tunneling** can evade egress rules if not addressed; pair egress filtering with resolver control and content inspection where needed.

## Common mistakes

- **Allowing all outbound by default.** The single most common gap; it permits download, C2 and exfiltration. Fix: default-deny egress, allow by exception.
- **Filtering servers like users.** Servers need little egress; leaving them open is a large exfiltration and C2 path. Fix: strict per-destination egress for servers.
- **Allowing direct outbound DNS and web from any host.** Bypasses protective DNS and proxies, enables tunneling. Fix: force DNS through resolvers and web through the proxy; block direct 53/80/443 from general hosts.
- **Not logging denied egress.** Loses a high-fidelity detection source. Fix: log and alert on blocked outbound attempts.
- **Enforcing without discovery.** Breaks legitimate flows. Fix: observe real egress first, then tighten.

## Practice

1. Why are the stages of an attack after initial access mostly outbound, and how does egress filtering disrupt them?
2. Why is a blocked outbound attempt a higher-fidelity alert than trying to spot malicious traffic among allowed outbound connections?
3. Why should servers be egress-filtered more strictly than user workstations?
4. How does egress filtering contribute to protecting other organizations, not just your own?
5. What is the risk of enabling default-deny egress without first discovering legitimate flows?

### Answers

1. Tool download, command and control, and exfiltration all require the compromised host to connect outward; a default-deny egress policy permits only known flows, so these outbound steps are blocked or forced onto monitored paths.
2. With a default-deny baseline, any blocked outbound attempt is by definition unexpected, so it stands out clearly, whereas malicious traffic hidden among broadly permitted outbound connections is hard to distinguish from normal activity.
3. Servers have narrow, well-defined outbound needs, so strict filtering rarely disrupts them and closes a major C2/exfiltration path, whereas leaving them open gives an attacker a wide outbound channel.
4. Anti-spoofing egress (BCP 38) stops a compromised host sending spoofed-source packets used in reflection and spoofing attacks against others, so it protects the wider internet.
5. Legitimate but undocumented outbound dependencies will be broken when the policy denies them, causing outages; observe-then-enforce avoids this.

## Further reading

- SANS, Egress Filtering FAQ and guidance on outbound traffic control.
- BCP 38 / RFC 2827, Network Ingress Filtering (the anti-spoofing egress component): https://www.rfc-editor.org/rfc/rfc2827
- MITRE ATT&CK, Exfiltration (TA0010) and Command and Control (TA0011) tactics, which egress filtering disrupts: https://attack.mitre.org/tactics/TA0011/
- NSA, Network Infrastructure Security Guide (2022): https://media.defense.gov/2022/Jun/15/2003018261/-1/-1/0/CTR_NSA_NETWORK_INFRASTRUCTURE_SECURITY_GUIDE_20220615.PDF
