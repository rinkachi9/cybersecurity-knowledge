# Kubernetes network security

## Summary

Kubernetes networking starts from an open default: every pod can reach every other pod across the whole cluster, with no filtering. That flat model is convenient for developers and dangerous for security, because one compromised pod can reach everything. Kubernetes network security is mostly about adding back the controls a traditional network would have: NetworkPolicies to segment pod-to-pod traffic (the cluster form of [microsegmentation](../architecture/microsegmentation.md)), a CNI plugin that actually enforces them, controlled ingress and egress, and a service mesh for mutual-TLS identity between services. This note is the network view of Kubernetes; the broader platform security belongs in the cloud-and-infrastructure area.

## Prerequisites

- [Microsegmentation](../architecture/microsegmentation.md): NetworkPolicies are its Kubernetes form.
- [Cloud network security](cloud-network-security.md) and [network segmentation](../architecture/network-segmentation.md).
- [TLS in network security](../secure-transport/tls-in-network-security.md): service-mesh mTLS.
- Basic Kubernetes: pods, namespaces, services.

## Core concepts

### Definition

*Kubernetes network security* is the control of traffic within and into and out of a Kubernetes cluster: pod-to-pod (east-west) traffic via NetworkPolicies, north-south traffic via ingress and egress controls, and service-to-service authentication via a service mesh. The enforcement of pod traffic depends on the *Container Network Interface* (CNI) plugin in use.

### Analogy

A default Kubernetes cluster is an open-plan office where every desk can walk to every other desk and every filing cabinet, no doors, no badges. NetworkPolicies add internal doors that only open for the specific desks that need to talk. A service mesh adds badges so each desk proves who it is to the others, not just that it is "in the office". Ingress and egress are the front door and the outbound mailroom. The flat default is the key fact: security is something you add back, not something present by default.

The analogy holds closely; it carries the "default-allow, you must add the doors" point that defines Kubernetes network security.

### The flat default and NetworkPolicies

By default, all pods in a cluster can communicate with all other pods, and pods can reach the external network, with no restrictions. *NetworkPolicies* are Kubernetes objects that change this: they select pods (by label) and specify allowed ingress and egress. Key facts:

- NetworkPolicies are *additive allow*: once any policy selects a pod, that pod denies all traffic not explicitly allowed. A common baseline is a default-deny policy per namespace, then specific allows.
- They select by *label*, not IP, so they survive pod churn and scaling, the Kubernetes form of [microsegmentation](../architecture/microsegmentation.md).
- They are *namespaced*, and can allow traffic from specific namespaces/pods.

Critically, **NetworkPolicies are only enforced if the CNI plugin supports them.** A policy applied under a CNI that ignores NetworkPolicy does nothing, a silent and dangerous gap. Enforcing CNIs include Calico, Cilium and others; some basic CNIs do not enforce policy.

### North-south: ingress and egress

- *Ingress*: external traffic enters through an Ingress controller or Gateway (often fronting services, terminating [TLS](../secure-transport/tls-in-network-security.md), sometimes with a [WAF](../traffic-filtering/web-application-firewalls.md)). Expose services deliberately, not by default.
- *Egress*: by default pods can reach the internet, a path for [C2](../network-attacks/command-and-control-traffic.md) and [exfiltration](../network-attacks/data-exfiltration.md). NetworkPolicy egress rules (and egress gateways) restrict where pods may connect, the Kubernetes form of [egress filtering](../traffic-filtering/egress-filtering.md).

### Service mesh and mTLS

A *service mesh* (Istio, Linkerd) injects a sidecar proxy beside each pod and routes service-to-service traffic through it. This enables:

- *Mutual TLS* between services automatically, so each service authenticates the other by workload identity (certificate), not by IP, and traffic is encrypted in transit even inside the cluster. This is [identity-based microsegmentation](../architecture/microsegmentation.md) and the network side of [zero trust](../architecture/zero-trust-networking.md) for workloads.
- Fine-grained authorization policies (which service may call which, on which routes).
- Observability of service-to-service traffic.

NetworkPolicies control connectivity (can these pods talk at layer 3/4); the mesh adds identity and encryption (are they who they claim, at layer 7). They are complementary layers.

## Worked example

Securing the three-tier app from the [microsegmentation](../architecture/microsegmentation.md) note, now concretely in Kubernetes (the NetworkPolicy approach is the tested pattern from that note, expressed here):

1. **Confirm enforcement.** Verify the cluster's CNI enforces NetworkPolicy (e.g. Calico/Cilium); otherwise policies are ignored and this is all theatre.
2. **Default-deny.** Apply a default-deny ingress (and egress) NetworkPolicy to the app's namespace, so nothing is allowed until specified.
3. **Allow the real flows** by label:
   - web pods: ingress from the Ingress controller on 443; egress to app pods on 8443.
   - app pods: ingress from web pods on 8443; egress to database pods on 5432.
   - database pods: ingress from app pods on 5432; no egress.
4. **Egress restriction.** Pods that need external access get explicit egress allows to specific destinations; others cannot reach the internet, cutting C2/exfiltration paths.
5. **Service mesh (optional, stronger).** A mesh adds mTLS so web-to-app and app-to-database are mutually authenticated and encrypted by workload identity, and authorization policies enforce "only web may call app", so even a pod that reaches the app's port must prove identity.
6. **Ingress.** The Ingress controller terminates TLS and (optionally) runs a WAF for the external 443 traffic.

Result: a compromised web pod can reach only the app tier on 8443 (and only if it holds the right mesh identity), cannot reach the database or other pods, cannot reach the internet, and cannot scan the cluster, exactly the containment the flat default lacked.

## Trade offs and when to use it

- **Flat default vs added controls.** The open default is convenient for development but unsafe for production; adding NetworkPolicies (and a mesh) is necessary work, prioritized for sensitive workloads.
- **NetworkPolicy vs service mesh.** NetworkPolicy is lighter (L3/L4 connectivity) and sufficient for basic segmentation; a mesh adds identity, mTLS and L7 authorization at the cost of sidecar overhead and operational complexity. Start with NetworkPolicy; add a mesh where identity and encryption between services are required.
- **CNI choice.** Enforcement depends entirely on the CNI; choosing a policy-enforcing CNI is a prerequisite, not an optional extra.
- **Observe-then-enforce.** As with any [microsegmentation](../architecture/microsegmentation.md), discover real pod-to-pod flows before applying default-deny to avoid breaking the application.

## Common mistakes

- **Relying on NetworkPolicy with a non-enforcing CNI.** The policies do nothing. Fix: use a policy-enforcing CNI (Calico, Cilium) and verify enforcement.
- **Leaving the flat default in production.** One compromised pod reaches everything. Fix: default-deny per namespace, explicit allows.
- **No egress restriction.** Pods can reach any internet destination (C2/exfiltration). Fix: NetworkPolicy egress rules and/or egress gateways.
- **Assuming the mesh replaces NetworkPolicy or vice versa.** They cover different layers. Fix: use NetworkPolicy for connectivity and the mesh for identity/encryption.
- **Enforcing default-deny without flow discovery.** Breaks the application. Fix: observe flows first, then enforce.

## Practice

1. What is the Kubernetes default for pod-to-pod traffic, and why is it a security concern?
2. What determines whether a NetworkPolicy actually takes effect?
3. How do NetworkPolicies and a service mesh differ in what they control?
4. Why do NetworkPolicies select pods by label rather than IP?
5. Why restrict pod egress, and how is it done?

### Answers

1. All pods can communicate with all other pods (and reach the external network) with no filtering; one compromised pod can therefore reach every other pod and service in the cluster.
2. The Container Network Interface (CNI) plugin in use: NetworkPolicies are only enforced if the CNI supports them (e.g. Calico, Cilium); under a non-enforcing CNI they are silently ignored.
3. NetworkPolicies control connectivity at L3/L4 (which pods may talk, on which ports); a service mesh adds workload identity, mutual TLS encryption and L7 authorization (whether the caller is who it claims and may use that route).
4. Pods are ephemeral and change IPs as they scale and restart, so label-based selection stays correct across pod churn, whereas IP-based rules would break constantly.
5. Because pods can otherwise reach any internet destination, providing C2 and exfiltration paths; it is restricted with NetworkPolicy egress rules and egress gateways that allow only specific destinations.

## Further reading

- Kubernetes NetworkPolicy documentation: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- CNI plugin docs (Calico, Cilium) for enforcement and advanced policy.
- Istio and Linkerd documentation for service-mesh mTLS and authorization.
- NSA/CISA, Kubernetes Hardening Guide: https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF
