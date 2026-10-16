# Cribl Native Function Catalog (by Pipeline Stage)

> Reference file for the `cribl-elastic-sentinel-pipelines` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

> ⚠️ Entries marked [verify] may not be real Cribl function names. Field keep/remove is done with Eval's *Keep fields* / *Remove fields*; XML/CSV parsing via Parser or XML Unroll. Confirm against Cribl's Functions docs for the user's version.

### Complete Native Function Catalog (Organized by Pipeline Stage)

#### Stage 1: Filter & Reduce (Always First)
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Drop** | Remove events matching a filter expression | You need to discard entire events (noise, health checks, debug logs) |
| **Sampling** / **Dynamic Sampling** | Pass only 1-in-N events (Dynamic Sampling adjusts the rate by volume) | You need statistical volume reduction on homogeneous data |
| **Suppress** | Deduplicate/throttle events by key over a time window | You need to limit repetitive events (alert storms, duplicate syslog) |
| **Eval** (Keep fields / Remove fields) | Retain only named fields, or remove wildcard-matched fields | You need aggressive field reduction (there is no standalone "Keep" function) |

#### Stage 2: Parse & Extract
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Auto Timestamp** | Discover and normalize timestamps into `_time` | You need automatic timestamp extraction without writing regex |
| **Parser** | Parse structured formats (JSON, KV, CSV, Syslog, CLF, Extended Log) | You need to break down structured payloads into fields |
| **Regex Extract** | Extract fields using named capture groups | You need to parse semi-structured or unstructured log text |
| **Grok** | Parse unstructured logs using predefined Grok patterns | You need common log parsing (Apache, Syslog, Cisco) without writing regex |
| **JSON Unroll** | Split a JSON array into individual events | You need to explode batched/bundled JSON payloads |
| **XML Unroll** | Split XML arrays into individual events | You need to explode batched XML payloads (parse single XML docs with Parser/Eval) |
| **Event Breaker** | Re-apply event breaking rules mid-pipeline | You need to re-segment combined payloads |

> CSV parsing is a Parser type; RFC 3164/5424 syslog headers are parsed by the Syslog Source (or a Pack) — there are no standalone "CSV" or "Syslog" functions.

#### Stage 3: Enrich & Transform
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Eval** | Add, modify, or remove fields using JavaScript expressions | The most versatile function — use for field math, conditionals, type conversion, renaming, and C.* method calls |
| **Rename** | Rename fields by name or pattern | You need bulk field renaming (e.g., vendor fields to ECS or ASIM) |
| **Lookup** | Enrich from CSV/KV store (asset inventory, threat intel, user context) | You need static enrichment from a reference table |
| **GeoIP** | Add geographic data from IP addresses (city, country, ASN, lat/lon) | You need geo-enrichment for network logs (uses MaxMind MMDB) |
| **DNS Lookup** | Forward or reverse DNS resolution | You need hostname-to-IP or IP-to-hostname enrichment |
| **Redis** | Query Redis for real-time enrichment | You need dynamic external context (session state, threat feeds, CMDB) |
| **Flatten** | Convert nested JSON to top-level dot-notation fields | Target destination does not support nested objects |
| **Numerify** | Convert string fields to numeric types | Downstream aggregations or metrics require numeric types |
| **Fold Keys** | Convert dot-notation fields back into nested objects | Destination expects nested JSON (e.g., ECS objects) |

#### Stage 4: Secure & Comply
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Mask** | Obfuscate PII via hash, pattern replacement, or redaction | You need GDPR/HIPAA/PCI compliance (SSNs, credit cards, emails, passwords) |

#### Stage 5: Aggregate & Convert
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Aggregations** | Statistical rollups (count, sum, avg, min, max, percentile) over time windows | You need logs-to-metrics conversion or volume summarization |
| **Publish Metrics** | Convert events to time-series metrics format | You need to emit metrics to Prometheus, Datadog, Graphite, InfluxDB |
| **Rollup Metrics** | Roll metrics up to a coarser time granularity | You need to cut metric volume |
| **OTLP Metrics** | Process OpenTelemetry metric formats | You are working with OTel-instrumented applications |

#### Stage 6: Route & Output
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Chain** | Execute another pipeline as a sub-routine | You need modular reusable processing (e.g., chain to a Pack pipeline) |
| **Clone** | Duplicate events within the pipeline (optionally adding fields) | You need a tagged copy; to reach two destinations, pair with an Output Router or use non-final Routes |
| **Serialize** | Convert events to a specific string format (JSON, CSV, KV) | You need to control the exact output serialization |
