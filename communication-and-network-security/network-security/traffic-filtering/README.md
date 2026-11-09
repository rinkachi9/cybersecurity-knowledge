# Traffic filtering

Deciding which traffic may pass: the firewalls that enforce it, how to write rules that do what they mean, controlling what leaves the network, and the proxies and application firewalls that filter at higher layers.

Read [firewalls](firewalls.md) first, then [firewall rule design](firewall-rule-design/README.md) for the hands-on, tested rules.

## Notes

- [Firewalls](firewalls.md): stateless, stateful and next-generation firewalls, the policy model, with a tested lab policy.
- [Firewall rule design](firewall-rule-design/README.md): rule order, state, anti-spoofing, and auditing a rule set for anomalies, with tested scripts.
- [Egress filtering](egress-filtering.md): controlling outbound traffic to break download, C2 and exfiltration.
- [Proxies and secure web gateways](proxies-and-secure-web-gateways.md): forward proxies that filter, scan and log web traffic.
- [Web application firewalls](web-application-firewalls.md): layer-7 filtering for web applications and virtual patching.

Scripts: under [firewall-rule-design/scripts](firewall-rule-design/scripts/), an nftables baseline policy and an ACL anomaly auditor.

Back to [Network security](../README.md).
