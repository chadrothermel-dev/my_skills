# Cribl Functions, Internal Fields & Expression Reference

> Reference file for the `cribl-stream` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## Complete Pipeline Function Reference

This is a **partial** reference. Cribl also ships Auto Timestamp, Code, Grok, DNS Lookup, Rollup Metrics, Drop Dimensions, Unroll, Fold Keys, Window, Trim Timestamp, OTLP Logs/Traces, and others — check the Functions docs for the user's version before naming parameters.

### Filtering & Volume Reduction Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Drop** | Remove events entirely from the data stream | Eliminate noise, debug logs, health checks, or irrelevant data as early in the pipeline as possible | Filter expression (JS boolean condition) |
| **Regex Filter** | Drop or keep events based on regex pattern match | Pattern-based filtering when simple field comparisons are insufficient | Regex pattern, Source field, Action (Keep/Drop) |
| **Sampling** | Pass only a percentage of events | High-volume, low-value logs where statistical representation is acceptable | Sample rate (e.g., 1 in N), Filter expression |
| **Dynamic Sampling** | Sample at different rates based on conditions | Keep 100% of errors but sample routine traffic at 1:100 | Sampling rules array (expression + rate per rule) |
| **Suppress** | Throttle/deduplicate repetitive events over a time window | Control event storms, limit duplicate alerts, manage chatty sources | Key expression (duplicate identifier), Max events to allow, Suppression period (seconds) |

### Transformation & Field Manipulation Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Eval** | Add, modify, or remove fields using JavaScript expressions | The most versatile function: field manipulation, math, conditional logic, type conversion, field removal | Key/Value pairs (field name + JS expression), Remove fields list |
| **Rename** | Rename existing fields | Normalize field names across heterogeneous data sources (e.g., `src_ip` → `source.ip`) | Key-value map of old name → new name |
| **Flatten** | Convert nested JSON objects/arrays into top-level key/value pairs | Prepare data for destinations that do not support nested objects (e.g., Splunk) | Depth limit, Delimiter character (default `.`) |
| **Numerify** | Convert string fields containing numeric values to number types | Ensure numeric fields are typed correctly for downstream metric aggregations and calculations | Fields to evaluate/convert |
| **Parser** | Extract/parse structured data (JSON, CSV, KV, TSV, extended log formats) | Break down complex payloads, extract fields from structured text, reserialize events | Operation mode (Extract/Reserialize), Source field, Parser type, Fields list |
| **Serialize** | Convert internal event representation into specific string formats | Format events for output (JSON, CSV, KV) before routing to specific destinations | Target format, Fields to include/exclude |

### Enrichment Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Lookup** | Enrich events by matching a field against an external lookup table and appending mapped fields | Add context (user department, asset criticality, threat intel, CMDB data) | Lookup file/source, Match mode (Exact/Regex/CIDR), Match field(s), Output fields |
| **GeoIP** | Enrich IP addresses with geographical location data (city, country, lat/lon, ASN) | Network analytics, threat detection, compliance-based geo-routing | Source IP field, GeoIP database (MaxMind MMDB), Output field prefix |
| **DNS Lookup** | Forward (hostname→IP) or reverse (IP→hostname) resolution (supersedes the deprecated Reverse DNS function) | Network context enrichment, asset identification | Lookup fields, DNS servers, cache TTL |
| **Redis** | Enrich events by querying a Redis cache in real-time | Real-time external context, session correlation, dynamic threat lists | Redis connection URL, Command (GET/HGETALL/SMEMBERS), Key expression, Output field |

### Extraction & Parsing Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Regex Extract** | Extract new fields from a text field using regex capture groups | Parse unstructured or semi-structured log text into discrete fields | Regex pattern (with named capture groups), Source field |
| **JSON Unroll** | Split a JSON array into individual events (one event per array element) | Process batched/bundled JSON payloads where each array item is a distinct event | Path to JSON array field |
| **XML Unroll** | Split nested XML elements into separate events | Process XML feeds or Windows Event Log XML payloads | XPath or element path |
| **Event Breaker** | Re-apply event breaking rules mid-pipeline | Correct improperly broken events, re-segment combined payloads | Event breaker ruleset, Breaker type (Regex/Timestamp/JSON/CSV/File Header) |

### Security & Compliance Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Mask** | Obfuscate sensitive data (PII, credit cards, SSNs, passwords) via hashing, pattern replacement, or redaction | Compliance (GDPR, HIPAA, PCI-DSS), security hygiene before data leaves the pipeline | Match rules (regex/field patterns), Replace expression or hash method (MD5/SHA-1/SHA-256) |

### Aggregation & Metrics Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Aggregations** | Perform statistical calculations (count, sum, avg, min, max, percentile) over tumbling time windows | Convert high-volume logs to summary metrics (e.g., VPC flow logs → connection counts per minute) | Time window (seconds), Aggregate functions, Group-by fields, Metric name template |
| **Publish Metrics** | Convert log events into standard metrics format for time-series databases | Feed metrics destinations (Prometheus, Datadog, Graphite, InfluxDB, SignalFx) | Metric name expression, Value expression, Dimensions/tags |
| **Prometheus Publisher** | Format metrics specifically for Prometheus scraping endpoints | Prometheus-native environments | Metric name, Labels, Value expression |
| **OTLP Metrics** | Process and format metrics for OpenTelemetry compliance | OpenTelemetry-instrumented environments | OTel resource attributes, Metric type, Temporality |

### Routing & Pipeline Control Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Chain** | Pass events to another pipeline or Pack for further processing | Modular pipeline design, reusable processing logic, Pack-based architecture | Target pipeline ID or Pack name |
| **Clone** | Create copies of events inside the pipeline | Fork data so a copy can be modified differently (often paired with a filter or the Output Router) | Clones (fields to add/override on each copy), Filter expression |

### Serialization & Format-Specific Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **CEF Serializer** | Format events into ArcSight Common Event Format | SIEM integrations requiring CEF format (ArcSight, QRadar CEF ingestion) | CEF field mapping (Device Vendor, Device Product, Severity, Extension fields) |
| **SNMP Trap Serialize** | Format events as SNMP Traps | Legacy network management system (NMS) integrations | SNMP version, Trap OID, Community string, Varbinds |

### Utility & Debugging Functions

| Function | Purpose | When to Use | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Comment** | Add documentation notes directly into the pipeline UI | Document pipeline logic, annotate design decisions; does not alter data flow | Comment text |
| **Tee** | Pipe a copy of events to a command's stdin | Debugging or niche integrations in non-production environments | Command, arguments, environment [verify] |

---

## Internal Fields Reference

Fields prefixed with a double underscore (`__`) are **internal**: they are not serialized to destinations. The first six rows (`_raw`, `_time`, `index`, `source`, `sourcetype`, `host`) are standard event fields, *not* internal fields — they are sent downstream.

| Field | Purpose | Notes |
| :--- | :--- | :--- |
| `_raw` | The original raw event text | Mutable; modifications affect what is sent downstream |
| `_time` | Event timestamp (epoch seconds) | Mutable; set by source or timestamp extraction |
| `index` | Target index (Splunk convention) | Used for index-based routing decisions |
| `source` | Event source identifier | Typically the file path or input source name |
| `sourcetype` | Event source type classification | Used heavily in route filter expressions |
| `host` | Originating host | Hostname of the data source |
| `__inputId` | Source (input) that delivered the event | Read-only; set by the Source; used in route filters (e.g., `__inputId.startsWith('syslog')`) |
| `__outputId` | Destination (output) for the event | Set by route/pipeline; determines where the event is sent |
| `__srcIpPort` | Originating IP:Port of the sender | Common with Syslog and TCP/UDP sources |
| `__criblMetric` | Metric type flag for metric-aware destinations | Directs metric serialization behavior |
| `__e['field']` | Bracket notation for fields with special characters | Required when field names contain dots, hyphens, or spaces |

---

## Cribl Expression Language & C.* Methods Reference

Cribl expressions are evaluated as standard **JavaScript (ECMAScript)** with access to the native `C.*` library for optimized data operations. All standard JS methods (`String.prototype.*`, `Array.prototype.*`, `Math.*`, `JSON.*`, ternary operators, template literals) are available.

### C.* Method Categories

| Namespace | Key Methods | Use Cases |
| :--- | :--- | :--- |
| `C.Lookup` | `C.Lookup('lookup.csv', 'keyField').match(value)` | Inline lookup execution within Eval expressions |
| `C.Mask` | `C.Mask.md5(val)`, `.sha1()`, `.sha256()` | Hash-based masking for PII/compliance |
| `C.Crypto` | `C.Crypto.encrypt()`, `.decrypt()`, `.createHmac()` | Field-level encryption/decryption |
| `C.Decode` | `C.Decode.base64(str)`, `.hex()`, `.uri()` | Decode encoded payloads |
| `C.Encode` | `C.Encode.base64(str)`, `.hex()`, `.uri()` | Encode fields for transport |
| `C.Net` | `C.Net.isPrivate(ip)`, `.communityIDv1()` | IP classification, network flow correlation |
| `C.Text` | `C.Text.parseXml(str)` | XML parsing within expressions |
| `C.Time` | Time manipulation and formatting | Timestamp normalization and conversion |
| `C.Schema` | Schema validation utilities [verify] | Validate event structure against defined schemas |
| `C.Metric` | Metric helpers [verify — may not exist] | Build metric events programmatically |
| `C.Math` | [verify — may not exist; use JavaScript `Math.*`] | Statistical and numerical operations |
| `C.OS` | `C.os.hostname()` | System-level information |
| `C.env` | `C.env['VAR_NAME']` | Access environment variables |
| `C.vars` | `C.vars['global_var']` | Access global variables defined in Worker Group settings |
| `C.systemVars` | System-level variable access | Read-only system configuration values |
| `C.version()` | Returns current Cribl version string | Version-conditional logic |
