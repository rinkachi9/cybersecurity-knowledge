# VirusTotal

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**VirusTotal** is a **threat intelligence and malware analysis platform** that aggregates:

- Antivirus engines
- Sandboxes
- Threat intelligence feeds

to analyze:

- Files
- URLs
- IP addresses
- Domains

> VirusTotal = multi-engine threat analysis + intelligence correlation platform

## Core Purpose

> Provide rapid, aggregated insight into whether an artifact is malicious or suspicious.

It answers:

- Is this file malicious?
- Has this URL been flagged?
- Is this IP associated with attacks?
- What do other security vendors think?

## How it works

### Multi-Engine Scanning

When you submit an artifact:

1. It is scanned by:
   - 60+ antivirus engines
   - Multiple detection systems
2. Results are aggregated:

```text
Detected: 12 / 70 engines
```

#### Key Insight

> VirusTotal does NOT replace antivirus - it aggregates them.

### Static Analysis

- File hashing (MD5, SHA1, SHA256)
- Signature matching
- Metadata extraction

### Dynamic Analysis (Sandbox)

- Executes file in controlled environment
- Observes:
  - File system changes
  - Network activity
  - Process behavior

### Threat Intelligence Correlation

- Links artifacts via:
  - IPs
  - domains
  - file relationships
- Builds a graph of related threats

### Supported Artifacts

#### Files

- Executables
- Scripts
- Documents

#### URLs

- Phishing pages
- Malware delivery sites

#### IP Addresses

- C2 servers
- Botnet nodes

#### Domains

- Malicious hosting
- Typosquatting

## Core Features

### Detection Aggregation

- Combines results from multiple engines
- Reduces false negatives

### VirusTotal Graph

- Visualizes relationships
- Enables threat hunting

### Behavior Analysis

- Shows runtime activity
- Detects:
  - Persistence
  - Network connections

### API Access

- Automate:
  - File scanning
  - IOC enrichment
  - Threat intelligence ingestion

## DevSecOps Integration

### CI/CD Pipeline Security

Example use case:

```text
Build Artifact → VirusTotal Scan → Evaluate Risk → Deploy / Block
```

#### Example (C# pseudocode)

```cs
var client = new HttpClient();
client.DefaultRequestHeaders.Add("x-apikey", "YOUR_API_KEY");

var content = new MultipartFormDataContent();
content.Add(new ByteArrayContent(File.ReadAllBytes("artifact.exe")), "file", "artifact.exe");

var response = await client.PostAsync("https://www.virustotal.com/api/v3/files", content);
```

### Threat Intelligence Enrichment

- Enrich logs:
  - IPs
  - domains
- Integrate with:
  - SIEM
  - SOC workflows

### Supply Chain Security

- Scan:
  - dependencies
  - binaries
  - third-party artifacts

## Security Considerations (CRITICAL)

### Data Exposure Risk

> Anything uploaded to VirusTotal may become accessible to other users (especially in public tier).

#### Implications:

- Do NOT upload:
  - proprietary code
  - internal binaries
  - sensitive documents

### False Positives / Negatives

- Not all detections are accurate
- Requires analyst interpretation

### Not a Prevention Tool

- VirusTotal is:
  - analysis tool
- NOT:
  - runtime protection

## Threat Intelligence Use Cases

### Incident Response

- Analyze suspicious file
- Identify malware family
- Extract indicators

#### Threat Hunting

- Pivot on:
  - hashes
  - domains
- Discover related campaigns

#### SOC Operations

- Enrich alerts
- Prioritize incidents

## Advanced Analysis

### Graph-Based Investigation

- Link artifacts
- Identify attack infrastructure

#### Behavior Analysis

- Detect:
  - persistence mechanisms
  - registry changes
  - suspicious processes

#### Reputation Scoring

- Based on:
  - detection count
  - historical data

## Common pitfalls

### Operational

- Blindly trusting detection count
- Ignoring context

#### Security

- Uploading sensitive data
- Over-reliance on VirusTotal

#### DevSecOps

- No integration into pipeline
- No automated decision logic

## Best Practices

### Usage

- Use for:
  - external artifacts
  - suspicious files

#### Automation

- Integrate via API
- Define thresholds:

```text
> 5 detections → block
1-5 → review
0 → allow (with caution)
```

#### SOC Integration

- Combine with:
  - SIEM
  - EDR
  - threat intelligence feeds

#### Privacy

- Use:
  - private scanning (enterprise)
  - internal sandbox for sensitive data

## Comparison

| Feature | VirusTotal | Sandbox (Cuckoo) | EDR |
| --- | --- | --- | --- |
| Multi-engine | Yes | No | No |
| Behavior analysis | Yes | Yes | Yes |
| Real-time protection | No | No | Yes |
| Threat intelligence | High | Medium | Medium |

## Real-World Scenario

### Suspicious File in CI/CD

1. Developer uploads dependency
2. Pipeline scans via VirusTotal
3. Result:
   - 15/70 detections → flagged
4. Pipeline blocks deployment
5. Security team investigates

## Summary

VirusTotal is:

- A **threat intelligence aggregator**
- A **malware analysis platform**
- A **critical tool for SOC and DevSecOps**

It provides:

- Multi-engine detection
- Behavioral insights
- Threat correlation

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
