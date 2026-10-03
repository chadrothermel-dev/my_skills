# Cribl Native Function Catalog (by Pipeline Stage)

> Reference file for the `cribl-elastic-sentinel-pipelines` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

> ⚠️ Entries marked [verify] may not be real Cribl function names. Field keep/remove is done with Eval's *Keep fields* / *Remove fields*; XML/CSV parsing via Parser or XML Unroll. Confirm against Cribl's Functions docs for the user's version.

### Complete Native Function Catalog (Organized by Pipeline Stage)

#### Stage 1: Filter & Reduce (Always First)
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Drop** | Remove events matching a filter expression | You need to discard entire events (noise, health checks, debug logs) |
| **Sampling** | Pass only 1-in-N events | You need statistical volume reduction on homogeneous data |
| **Suppress** | Deduplicate/throttle events by key over a time window | You need to limit repetitive events (alert storms, duplicate syslog) |
| **Rate Limit** [verify — may not exist] | Hard-cap events per second | You need to protect downstream destinations from burst traffic |
| **Eval → Keep fields** | Retain only named fields (wildcards supported), dropping all others | You need aggressive field reduction |

#### Stage 2: Parse & Extract
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Auto Timestamp** | Discover and normalize timestamps into `_time` | You need automatic timestamp extraction without writing regex |
| **Parser** | Parse structured formats (JSON, KV, CSV, Syslog, CLF, Extended Log) | You need to break down structured payloads into fields |
| **Regex Extract** | Extract fields using named capture groups | You need to parse semi-structured or unstructured log text |
| **Grok** | Parse unstructured logs using predefined Grok patterns | You need common log parsing (Apache, Syslog, Cisco) without writing regex |
| **JSON Unroll** | Split a JSON array into individual events | You need to explode batched/bundled JSON payloads |
| **XML** [verify — use Parser / XML Unroll] | Parse XML payloads into JSON fields | You need to handle Windows Event Log XML or API XML responses |
| **CSV** [verify — use Parser] | Parse or format CSV-structured data | You need to handle CSV log formats or produce CSV output |
| **Syslog** [verify — syslog headers are parsed by the Syslog source] | Parse RFC 3164/5424 syslog headers | You need to extract facility, severity, hostname, app, PID from syslog |
| **Event Breaker** | Re-apply event breaking rules mid-pipeline | You need to re-segment combined/compressed payloads |

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
| **Trim** [verify] | Remove leading/trailing whitespace from field values | Fields contain padding whitespace that causes match failures |
| **Schema Validation** [verify] | Validate events against a JSON schema | You need to ensure structural compliance before routing to Elastic/Sentinel |

#### Stage 4: Secure & Comply
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Mask** | Obfuscate PII via hash, pattern replacement, or redaction | You need GDPR/HIPAA/PCI compliance (SSNs, credit cards, emails, passwords) |
| **Compress** [verify] | Compress/decompress field payloads (gzip, zlib) | You need to handle compressed payloads mid-pipeline |

#### Stage 5: Aggregate & Convert
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Aggregations** | Statistical rollups (count, sum, avg, min, max, percentile) over time windows | You need logs-to-metrics conversion or volume summarization |
| **Publish Metrics** | Convert events to time-series metrics format | You need to emit metrics to Prometheus, Datadog, Graphite, InfluxDB |
| **Prometheus Publisher** | Format metrics for Prometheus scraping | You have a Prometheus-native monitoring stack |
| **OTLP Metrics** | Process OpenTelemetry metric formats | You are working with OTel-instrumented applications |

#### Stage 6: Route & Output
| Function | Purpose | Use Instead Of Code When... |
| :--- | :--- | :--- |
| **Chain** | Execute another pipeline as a sub-routine | You need modular reusable processing (e.g., chain to a Pack pipeline) |
| **Clone** | Fork events for parallel routing to multiple destinations | You need to send one copy to Elastic and a different copy to Sentinel |
| **Serialize** | Convert events to a specific string format (JSON, CSV, KV) | You need to control the exact output serialization |
