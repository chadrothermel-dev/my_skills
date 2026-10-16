# ECS, ASIM & CommonSecurityLog Field Mappings

> Reference file for the `cribl-elastic-sentinel-pipelines` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

#### Elastic Common Schema (ECS) Field Requirements

ECS compliance is **mandatory** for Elastic Security detection rules, Observability dashboards, and Machine Learning jobs to function. The following fields must be set correctly in every pipeline destined for Elastic:

| ECS Field | Type | Required For | How to Set in Cribl |
| :--- | :--- | :--- | :--- |
| `@timestamp` | `date` (ISO 8601) | Everything — sorting, dashboards, alerts, ML | Normalize `_time` with Auto Timestamp; the Cribl Elasticsearch destination renames `_time` to `@timestamp` at delivery (millisecond precision). If set explicitly: `C.Time.strftime(_time, '%Y-%m-%dT%H:%M:%S.%LZ')` (`_time` is epoch **seconds**) |
| `message` | `text` | Discover, full-text search, fallback display | Eval: `message = _raw` (preserve original event) |
| `ecs.version` | `keyword` | Schema version identification | Eval: `ecs.version = '<ECS version your target integration/mappings use>'` (verify; do not hardcode an arbitrary version) |
| `event.kind` | `keyword` | Event classification (ECS allowed values; `signal` is reserved for Elastic solutions, `asset` is beta) | `event`, `alert`, `asset`, `enrichment`, `metric`, `state`, `pipeline_error`, `signal` |
| `event.category` | `keyword` (array) | SIEM rule matching | `api`, `authentication`, `configuration`, `database`, `driver`, `email`, `file`, `host`, `iam`, `intrusion_detection`, `library`, `malware`, `network`, `package`, `process`, `registry`, `session`, `threat`, `vulnerability`, `web` |
| `event.type` | `keyword` (array) | SIEM rule sub-classification | `access`, `admin`, `allowed`, `change`, `connection`, `creation`, `deletion`, `denied`, `end`, `error`, `group`, `indicator`, `info`, `installation`, `protocol`, `start`, `user` |
| `event.outcome` | `keyword` | Auth/access result | `success`, `failure`, `unknown` |
| `event.action` | `keyword` | Specific action taken | Vendor-specific (e.g., `logged-in`, `firewall-rule-matched`) |
| `observer.vendor` | `keyword` | Source appliance vendor | `Palo Alto Networks`, `Fortinet`, `CrowdStrike`, `Microsoft` |
| `observer.product` | `keyword` | Source product name | `PAN-OS`, `FortiGate`, `Falcon`, `Windows` |
| `source.ip` | `ip` | Network source address | Extract from log source field |
| `destination.ip` | `ip` | Network destination address | Extract from log source field |
| `host.name` | `keyword` | Originating hostname | Often from syslog header or `host` field |
| `user.name` | `keyword` | Username involved | Critical for authentication events |
| `related.ip` | `ip` (array) | Correlation — all IPs in event | Eval: `related.ip = [source.ip, destination.ip].filter(x => x)` |
| `related.user` | `keyword` (array) | Correlation — all users in event | Eval: `related.user = [user.name].filter(x => x)` |

---

#### ASIM (Advanced Security Information Model) Schemas

ASIM is Sentinel's normalization framework — equivalent to ECS in Elastic. Key schemas:

| ASIM Schema | Key Fields | Maps To Source Types |
| :--- | :--- | :--- |
| **Authentication** | `EventType`, `TargetUsername`, `SrcIpAddr`, `EventResult`, `LogonMethod` | Windows Security (4624/4625), VPN, SSH, RADIUS |
| **Network Session** | `SrcIpAddr`, `DstIpAddr`, `DstPortNumber`, `NetworkProtocol`, `DvcAction` | Firewall (Palo Alto, Fortinet, Cisco ASA), NSG flow logs |
| **DNS** | `SrcIpAddr`, `DnsQuery`, `DnsQueryType`, `DnsResponseCode`, `DnsResponseName` | DNS server logs, Pi-hole, Infoblox |
| **Web Session** | `Url`, `HttpRequestMethod`, `HttpStatusCode`, `SrcIpAddr`, `DstIpAddr` | Proxy logs, WAF, web server access logs |
| **Process Event** | `ActingProcessName`, `TargetProcessName`, `TargetProcessCommandLine`, `ActorUsername` | Sysmon, CrowdStrike, Defender |
| **File Activity** | `TargetFileName`, `TargetFilePath`, `ActorUsername`, `EventType` (Created/Modified/Deleted) | File integrity monitoring, Sysmon |
| **Audit** | `EventType`, `Object`, `ActorUsername`, `SrcIpAddr` | Entra ID audit, config changes |

---

#### CommonSecurityLog (CEF) Field Mapping

When routing CEF-formatted logs (Palo Alto, Fortinet, Check Point, etc.) to Sentinel's `CommonSecurityLog` table, the following fields must be mapped:

| CEF Key | Sentinel Field | Description |
| :--- | :--- | :--- |
| `Header:Device Vendor` | `DeviceVendor` | e.g., `Palo Alto Networks` |
| `Header:Device Product` | `DeviceProduct` | e.g., `PAN-OS` |
| `Header:Device Version` | `DeviceVersion` | e.g., `11.1.0` |
| `Header:Severity` | `LogSeverity` | `0-10` or text (`Low`, `Medium`, `High`, `Critical`) |
| `act` | `DeviceAction` | e.g., `allowed`, `denied`, `dropped` |
| `src` | `SourceIP` | Source IP address |
| `dst` | `DestinationIP` | Destination IP address |
| `spt` | `SourcePort` | Source port |
| `dpt` | `DestinationPort` | Destination port |
| `proto` | `Protocol` | e.g., `TCP`, `UDP` |
| `app` | `ApplicationProtocol` | e.g., `HTTPS`, `DNS`, `SSH` |
| `duser` | `DestinationUserName` | Target user |
| `suser` | `SourceUserName` | Source/acting user |
| `msg` | `Message` | Human-readable event description |
| `cat` | `DeviceEventCategory` | Vendor event category |
| `cs1`–`cs6` | `DeviceCustomString1`–`6` | Vendor-specific extension fields |
| `cs1Label`–`cs6Label` | `DeviceCustomString1Label`–`6Label` | Labels for extension fields |
| `cn1`–`cn3` | `DeviceCustomNumber1`–`3` | Vendor-specific numeric extension fields |
| `flexString1`/`2` | `FlexString1`/`2` | Additional vendor fields |
