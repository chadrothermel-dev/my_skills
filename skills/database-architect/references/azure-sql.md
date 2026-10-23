# Azure SQL Deep Dive (Database, Managed Instance, VMs, Fabric)

> Reference file for the `database-architect` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## Contents

- 1. Choose the Deployment Option
- 2. Azure SQL Database Purchasing Models & Service Tiers
- 3. Serverless & Free Options
- 4. Managed Instance Specifics
- 5. High Availability & Disaster Recovery
- 6. Backups & Restore
- 7. Security
- 8. Performance & Monitoring
- 9. Azure SQL Database T-SQL Differences (vs. SQL Server)
- 10. Cost Optimization
- 11. Migration Paths

## Azure SQL Deep Dive

> Tier limits, retention ranges, and preview status below were checked on Microsoft Learn in October 2026. Azure SQL changes monthly; confirm limits on the resource-limits pages before sizing.

### 1. Choose the Deployment Option
| Option | What it is | Choose it when | Watch out for |
| :--- | :--- | :--- | :--- |
| **Azure SQL Database** (single database) | Fully managed database on a logical server | New cloud apps; scaling and paying per database | No SQL Server Agent, no cross-database queries, no `USE`, no CLR, no Windows authentication |
| **Elastic pool** (Azure SQL Database) | Many databases share one pool of compute | Many databases with variable, non-overlapping peaks (SaaS per-tenant designs) | A noisy database can starve others; set per-database min/max limits |
| **Azure SQL Managed Instance** | Near-complete SQL Server instance inside your virtual network | Lift-and-shift apps needing SQL Agent, cross-database queries, CLR, Service Broker, linked servers, or Database Mail | Subnet and network planning; management operations (create, scale) take longer; choose the update policy deliberately |
| **SQL Server on Azure VMs** | Full SQL Server on an IaaS VM | OS access, features PaaS lacks, a specific SQL Server version, third-party agents | You own patching, HA, and backups (the SQL IaaS Agent extension automates some of it) |
| **SQL database in Microsoft Fabric** | SaaS SQL database inside Fabric, replicated to OneLake | Operational data that feeds Fabric analytics | Fabric capacity billing; feature set differs, so verify required features |

**Default:** Azure SQL Database for new applications; Managed Instance when an existing app depends on instance-level features; VMs only when PaaS can't meet a hard requirement.

### 2. Azure SQL Database Purchasing Models & Service Tiers
- **vCore model (recommended):** choose compute, hardware, and storage separately; required for Hyperscale and serverless; eligible for Azure Hybrid Benefit and reserved capacity.
- **DTU model:** bundled compute, storage, and I/O in the Basic, Standard, and Premium tiers. Simple for small, predictable databases; no Hyperscale or serverless.

| vCore tier | General Purpose | Business Critical | Hyperscale |
| :--- | :--- | :--- | :--- |
| Best for | Budget-balanced workloads | High-transaction, low-latency OLTP; In-Memory OLTP; fastest failover | Microsoft's recommended default for new OLTP and HTAP workloads; large databases; fast backup and restore |
| Compute | 2–128 vCores | 2–128 vCores | 2–192 vCores |
| Storage | 1 GB–4 TB, remote premium storage | 1 GB–4 TB, local SSD | 10 GB–128 TB, grows automatically, billed on allocated space |
| HA and read scale | One replica; zone redundancy optional | Three replicas, one readable; zone redundancy optional | Configurable HA replicas (up to 4 readable) plus up to 30 named replicas |
| Backups | Full, differential, and log backups | Full, differential, and log backups | Storage snapshots: near-instant backup and fast restore at any size |

Restoring between Hyperscale and the other tiers isn't supported, so moving off Hyperscale later means an export or data migration. Confirm current conversion options before committing.

### 3. Serverless & Free Options
- **Serverless** (General Purpose and Hyperscale, vCore model, standard-series hardware): compute scales between a minimum and maximum vCore setting and is billed per second.
  - **Auto-pause** stops compute charges after a period of inactivity: General Purpose default 60 minutes, minimum 15. Hyperscale auto-pause is in preview, with a minimum of 60 minutes.
  - The first connection after a pause waits while the database resumes.
  - Geo-replication, failover groups, long-term retention, and DNS aliases prevent auto-pause, and so do open idle connections from tools like SSMS.
  - Use it for intermittent, unpredictable workloads, not steady or latency-sensitive ones.
- **Azure SQL Database free tier:** up to 10 free General Purpose serverless databases per subscription, each with 100,000 vCore seconds, 32 GB of data, and 32 GB of backup storage per month. No SLA, so use it for development and proofs of concept.
- **Managed Instance free offer:** one General Purpose instance per subscription for 12 months (720 vCore hours per month, 64 GB of storage), with no SLA and no failover groups or long-term retention.

### 4. Managed Instance Specifics
| Tier | Max vCores | Max storage | Max databases | Readable replica |
| :--- | :--- | :--- | :--- | :--- |
| General Purpose | 80 | 16 TB | 100 | No |
| Next-gen General Purpose | 128 | 32 TB | 500 | No (IOPS configurable and billed above the free quota) |
| Business Critical | 128 | 16 TB | 100 | Yes (one) |

- **Update policy:** **SQL Server 2022**, **SQL Server 2025**, or **Always-up-to-date**. It controls which engine features you get and whether you can move databases back to SQL Server or fail back over the Managed Instance link. Always-up-to-date gets features first but closes the path back to boxed SQL Server.
- **Managed Instance link:** near-real-time replication between SQL Server and Managed Instance, built on distributed availability groups.
  - **SQL Server 2016–2019:** one-way only.
  - **SQL Server 2022 and 2025:** two-way disaster recovery with failback, when the instance's update policy matches the SQL Server version.
  - Gives the lowest-downtime online migration, and offers a hybrid failover benefit for a license-free passive DR replica.
- **SQL Agent** is always on, but some job step types (such as CmdExec) and alerts aren't supported. Database Mail must use the profile named `AzureManagedInstance_dbmail_profile`.

### 5. High Availability & Disaster Recovery
| Need | Use | Notes |
| :--- | :--- | :--- |
| Survive a node or zone failure | Built-in HA + **zone redundancy** | Enable zone redundancy where the region supports availability zones |
| Readable copy in another region, single database | **Active geo-replication** | Any region; secondary must use the same service tier; manual failover; connection string changes on failover |
| Fail over many databases together with stable connection strings | **Failover groups** | Read-write and read-only listener endpoints survive failover. On Managed Instance, one failover group covers all user databases. Prefer a customer-managed failover policy, because a Microsoft-managed policy can force failover with data loss |
| Cheapest regional DR | **Geo-restore** from geo-redundant backups | Recovery point up to about an hour; restore time grows with database size |
| Hybrid DR with on-premises SQL Server | **Managed Instance link** | See section 4 |

Secondaries created by a failover group for non-Hyperscale databases don't inherit zone redundancy; enable it on them afterward. Run DR drills with planned (no-data-loss) failovers.

### 6. Backups & Restore
- **Automatic:** full, differential (every 12 hours by default in vCore), and log backups. **Point-in-time restore** covers 1–35 days (default 7; Basic tier 1–7).
- **Long-term retention (LTR):** weekly, monthly, or yearly full backups kept for up to 10 years. LTR backups can be made **immutable** in Azure SQL Database. Managed Instance can't do this yet; the workaround is copy-only backups to your own immutable storage.
- **Backup storage redundancy:** locally redundant, zone-redundant, or geo-redundant. Geo-restore requires geo-redundant backups. Changing the setting applies only to new backups.
- **Deleting a logical server deletes its databases and their point-in-time backups**; only LTR backups survive. Protect production servers with Azure resource locks.
- **Native `BACKUP`/`RESTORE`:** Managed Instance supports copy-only backups to URL and restores from URL; Azure SQL Database doesn't (use database copy, point-in-time restore, or BACPAC export).

### 7. Security
- **Identity:** Microsoft Entra authentication, and **Entra-only authentication** to turn off SQL logins; managed identities for applications. Windows authentication isn't available in Azure SQL Database.
- **Network:** private endpoints with public network access disabled for Azure SQL Database; Managed Instance is deployed into your virtual network.
- **Data protection:** TDE is on by default (customer-managed keys in Azure Key Vault are optional); Always Encrypted (with secure enclaves); Ledger; row-level security; dynamic data masking.
- **Threat protection and audit:** Microsoft Defender for SQL (vulnerability assessment and threat detection); auditing to Log Analytics, Storage, or Event Hubs, then into Microsoft Sentinel.
- **Permissions:** Azure SQL Database has no server-level `GRANT`; use database roles and contained database users.

### 8. Performance & Monitoring
- **Query Store** is on by default, and automatic tuning can force the last good plan after a regression. Index create and drop recommendations are opt-in.
- **Resource governance is the usual surprise.** Each tier caps log write rate, IOPS, and workers. Check `sys.dm_db_resource_stats` (recent, 15-second samples) and `sys.resource_stats` in `master` (longer history) before blaming queries.
- **Tools:**
  - Query Performance Insight (top resource consumers).
  - Database watcher (preview; in-depth monitoring into Azure Data Explorer or Fabric).
  - Database Hub in Microsoft Fabric (preview; free, estate-wide view).
  - Azure Monitor metrics and alerts.
  - SQL Insights was retired in December 2024.
- **Scaling** changes service objectives online but drops connections briefly at the end. Applications need transient-fault retry logic.

### 9. Azure SQL Database T-SQL Differences (vs. SQL Server)
Not supported in Azure SQL Database (Managed Instance supports most of these):
- `USE` to switch databases (open a new connection instead).
- Cross-database three- and four-part names and linked servers. Elastic query (preview) allows read-only cross-database access.
- SQL Server Agent and `msdb` jobs (use **Elastic Jobs**).
- CLR, server-level permissions, and server or logon triggers.
- `sp_configure` (use `ALTER DATABASE SCOPED CONFIGURATION`) and trace flags.
- `BACKUP` / `RESTORE` statements, Windows logins, and `EXECUTE AS LOGIN` (use `EXECUTE AS USER`).

### 10. Cost Optimization
- **Right-size first:** vCore metrics, then serverless for intermittent use and elastic pools for many small databases.
- **Reserved capacity** (1 or 3 years) for steady provisioned compute.
- **Azure Hybrid Benefit** for existing SQL Server licenses with Software Assurance.
- Watch backup storage (retention length, LTR, geo-redundancy) and unused readable or named replicas.
- Use start/stop schedules for General Purpose Managed Instances in dev/test.
- Quote prices only with region, currency, and date, and send the user to the Azure pricing calculator.

### 11. Migration Paths
| Target | Methods |
| :--- | :--- |
| Azure SQL Database | Assess with SQL Server enabled by Azure Arc migration assessment or Azure Database Migration Service; migrate with DMS, BACPAC (small databases), or transactional replication (minimal downtime) |
| Azure SQL Managed Instance | Managed Instance link (online, minimal downtime), Log Replay Service, native restore from URL, or DMS |
| SQL Server on Azure VMs | Backup and restore, log shipping, availability groups, or Azure Migrate |

Pick the target by feature dependency: anything in section 9 points to Managed Instance; OS access or unsupported features point to VMs.
