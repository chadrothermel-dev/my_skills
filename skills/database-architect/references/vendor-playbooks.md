# Vendor Playbooks (SQL Server, Oracle, PostgreSQL, MySQL, NoSQL)

> Reference file for the `database-architect` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## Vendor Playbooks

### Microsoft SQL Server & Azure SQL
- **Instance setup:** set max server memory (leave room for the OS and other services); multiple equal-sized tempdb data files (setup configures this in current versions); MAXDOP sized to cores per NUMA node; raise cost threshold for parallelism from the default 5 to a tested starting point (often 30–50).
- **Query Store** is on by default for new databases in SQL Server 2022 and later; use it for plan regression and plan forcing. Intelligent query processing features (parameter-sensitive plan optimization, memory grant feedback) depend on the compatibility level.
- **HA:** availability groups (contained AGs since 2022 include logins and jobs); Basic AG in Standard edition is limited to two replicas and one database per AG. Failover cluster instances protect the instance, not storage.
- **SQL Server 2025 highlights:** native `vector` data type and vector functions (vector indexes and `VECTOR_SEARCH` are preview in SQL Server 2025, GA in Azure SQL), native `json` type, regular-expression functions, optimized locking, calling REST endpoints, change event streaming (preview), and mirroring to Microsoft Fabric. Preview features need the `PREVIEW_FEATURES` database-scoped configuration and aren't for production.
- **Tools:** SQL Server Management Studio for administration and SQL Server Agent; VS Code with the MSSQL extension for development (Azure Data Studio was retired February 28, 2026); `sqlcmd`; SqlPackage; PowerShell `SqlServer` module and dbatools.
- **Azure SQL:** Azure SQL Database (single database, elastic pools, Hyperscale, serverless) versus Managed Instance (near-full SQL Server surface: Agent, cross-database queries, CLR). Managed Instance update policy (SQL Server 2025 or Always-up-to-date) determines feature availability.
- **Licensing reminders:** editions differ in limits and features; Express is for small workloads only. Check the editions page for the exact version, because limits change between releases.

### Oracle Database
- **Architecture:** multitenant container databases (CDB) with pluggable databases (PDB); non-CDB architecture is desupported from 21c onward. Memory is SGA plus PGA; manage storage with ASM where possible.
- **Releases:** Oracle AI Database 26ai is the current long-term release (October 2025). It succeeds 23ai, and 23ai systems moved to 26ai through a release update rather than a full upgrade. 19c is the widely deployed long-term release; plan 19c-to-26ai upgrades with AutoUpgrade.
- **26ai / 23ai developer features:** `BOOLEAN` data type, JSON Relational Duality views, AI Vector Search (included at no extra charge per Oracle), SQL domains, schema-level privileges, `IF [NOT] EXISTS` in DDL, and `SELECT` without `FROM DUAL`.
- **HA/DR:** RAC (EE option) for node failure; Data Guard (included with EE) for site failure; Active Data Guard (extra license) for read-only standby use and automatic block repair; GoldenGate (separate license) for logical replication and zero-downtime migrations; Flashback for human error.
- **Performance:** AWR, ASH, and ADDM require the **Diagnostics Pack**; SQL Tuning Advisor and SQL Profiles require the **Tuning Pack**. Without those licenses, use Statspack and `DBMS_XPLAN`. Gather optimizer statistics with `DBMS_STATS`; stabilize critical plans with SQL Plan Management baselines.
- **Licensing risk:** options and packs are easy to enable by accident. Check `DBA_FEATURE_USAGE_STATISTICS`, and set `CONTROL_MANAGEMENT_PACK_ACCESS` to match what's licensed. Oracle's policies on virtualization (including VMware) and cloud core counting are strict; tell the user to confirm with their Oracle license specialist before deploying.
- **Cloud:** Autonomous Database (self-tuning and self-patching), Exadata Database Service, and Oracle Database@Azure, @AWS, and @Google Cloud for running Oracle inside other clouds.

### PostgreSQL
- **Connections:** each connection is an operating-system process, so use a pooler (PgBouncer, or the cloud provider's built-in pooler) instead of raising `max_connections` into the thousands.
- **Memory starting points:** `shared_buffers` about 25% of RAM, `effective_cache_size` about 50–75%, and `work_mem` set carefully, because it applies per sort or hash operation per connection.
- **MVCC and vacuum:** updates and deletes leave dead row versions; autovacuum cleans them and prevents transaction ID wraparound. Tune per-table autovacuum thresholds for large, busy tables, and alert on long-running transactions that block cleanup.
- **HA:** streaming replication plus Patroni for automatic failover; logical replication for selective replication and low-downtime major upgrades; `pg_upgrade --link` for fast in-place upgrades.
- **Versions:** a new major release ships each year and each is supported for five years. PostgreSQL 18 (2025) added asynchronous I/O, `uuidv7()`, virtual generated columns, and OAuth authentication, and deprecated MD5 passwords. PostgreSQL 19 is in release candidate as of October 2026.
- **Extensions:** `pg_stat_statements` (always), `pgvector` (vectors), PostGIS (spatial), `pg_partman` (partition management), `pgAudit` (auditing), TimescaleDB (time-series), Citus (scale-out). Managed services support a curated subset; confirm before designing around one.

### MySQL & MariaDB
- **Engine:** InnoDB for everything; MyISAM is legacy. Set `innodb_buffer_pool_size` to roughly 50–75% of RAM on a dedicated server; use `utf8mb4`; use row-based binary logging with GTIDs.
- **Releases:** long-term support releases (8.4 LTS; 9.7 LTS, April 2026) versus quarterly Innovation releases supported only until the next one ships. MySQL 8.0 is end-of-life. After 9.7, MySQL uses calendar versioning (YY.M). Run LTS in production unless you need a newer feature.
- **HA:** InnoDB Cluster (Group Replication + MySQL Router), InnoDB ClusterSet for cross-region DR, or managed equivalents.
- **Security:** `caching_sha2_password` is the default; `mysql_native_password` is disabled by default in 8.4 and removed in 9.x.
- **MariaDB** is a separate fork with its own features (Galera Cluster, MaxScale) and has diverged from MySQL. Don't assume features or upgrade paths transfer between them.

### NoSQL & Specialty Platforms
- **MongoDB:** replica sets for HA, sharding for scale, a shard key chosen carefully because it is hard to change; Atlas for managed service and vector search.
- **Azure Cosmos DB:** multiple APIs (NoSQL, MongoDB, Cassandra, Gremlin, Table, PostgreSQL); cost and throughput are measured in request units (RUs); the partition key choice determines scale; five consistency levels from strong to eventual.
- **Cassandra and DynamoDB:** design one table per query pattern around the partition key; avoid scans; plan secondary indexes deliberately.
- **Redis and Valkey:** cache and fast data structures with TTLs and eviction policies; persistence is optional, so it's not a system of record by default. Redis licensing changed in 2024 and Valkey is the Linux Foundation fork; confirm current licensing for the user's use case.
- **Search engines and SIEM data stores** (Elasticsearch, Azure Data Explorer for logs) are covered by the `elastic-stack` and `microsoft-sentinel` skills.
