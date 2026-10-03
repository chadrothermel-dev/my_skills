# Cribl Pack Dispensary — Pack-First Design

> Reference file for the `cribl-elastic-sentinel-pipelines` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## 4. Cribl Pack Dispensary — Mandatory Pack-First Design

Before building any custom pipeline, you **MUST** check the Cribl Pack Dispensary for pre-built, community-validated Packs. Packs accelerate deployment, reduce custom code, and are maintained by Cribl and the community.

> ⚠️ Pack IDs below are illustrative and unverified. Search the Dispensary by vendor/product and confirm the exact Pack ID and maintainer before recommending one.

### Destination-Specific Packs

| Pack Name | Purpose | Use When |
| :--- | :--- | :--- |
| **`cribl-microsoft-sentinel`** | Converts vendor logs to CommonSecurityLog format for Sentinel | Routing firewall, IDS/IPS, or network appliance logs to Sentinel's `CommonSecurityLog` table |
| **`cribl-microsoft-sentinel-syslog-dest`** | Formats data for Sentinel's `Syslog` table | Routing standard syslog data to Sentinel's built-in `Syslog` table |
| **`cribl-azure-sentinel-csl-dest`** | Post-processing for CommonSecurityLog destination | Ensuring CEF field mappings are correct for Sentinel ingestion |
| **`cribl-elastic-output`** | Routing post-processor for Elastic Data Streams | Dynamically setting `_index` to the correct data stream name based on log type |

### Source-Specific Packs

| Pack Name | Log Source | What It Does |
| :--- | :--- | :--- |
| **`cribl-palo-alto-networks`** | Palo Alto PAN-OS | Parses traffic, threat, system, and authentication logs; extracts all PAN-OS fields; normalizes field names |
| **`cribl-crowdstrike-fdr`** | CrowdStrike Falcon Data Replicator | Processes massive FDR JSON bundles; extracts event types; normalizes timestamps |
| **`cribl-crowdstrike-rest`** | CrowdStrike REST API events | Handles event stream and detection data from Falcon API |
| **`cribl-windows-events`** | Windows Event Logs (via Cribl Edge) | Parses Windows Security/System/Application event XML; extracts EventID, account, logon type |
| **`cribl-edge-for-windows`** | Windows endpoint collection | Comprehensive Windows log collection and normalization for Edge agents |
| **`cribl-cef-source`** | CEF-formatted syslog | Parses ArcSight Common Event Format into structured fields |
| **`cribl-cisco-asa`** | Cisco ASA/Firepower | Parses ASA syslog messages; extracts ACL actions, NAT translations, VPN events |
| **`cribl-fortinet`** | Fortinet FortiGate (FortiOS) | Parses FortiGate key-value logs; extracts policy actions, UTM events |
| **`cribl-office365`** | Microsoft 365 Management Activity API | Processes O365 audit logs (Exchange, SharePoint, Azure AD, DLP) |
| **`cribl-aws-vpc-flow`** | AWS VPC Flow Logs | Parses VPC flow log fields; enriches with action (ACCEPT/REJECT) and protocol names |

### Pack Evaluation & Modification Protocol

When evaluating a Pack for use:

1. **Install the Pack** from the Dispensary and examine its pipelines, routes, and lookup tables.
2. **Review each pipeline function** — verify that the Pack's transformations align with your ECS (Elastic) or ASIM (Sentinel) requirements.
3. **Check the Pack's output fields** against the destination schema:
   - For Elastic: Do the output fields comply with ECS? Are `data_stream.*`, `event.*`, `@timestamp`, and `related.*` fields set?
   - For Sentinel: Do the output fields match the DCR schema? For CommonSecurityLog, are CEF header fields (`DeviceVendor`, `DeviceProduct`, `DeviceAction`, etc.) correctly mapped?
4. **Extend, don't replace:** If the Pack is 80% correct, **Chain** to a custom post-processing pipeline that adds the missing fields rather than rebuilding from scratch.
5. **Document modifications:** Add a Comment function at the top of any customized Pack pipeline noting what was changed and why.
