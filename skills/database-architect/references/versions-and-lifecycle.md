# Versions, Lifecycle & Deprecated Technology

> Reference file for the `database-architect` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## Versions, Lifecycle & Deprecated Technology

> As of October 2026. SQL Server, Azure, and PostgreSQL rows were checked against official pages; the Oracle 19c and MySQL dates come from vendor announcements and release reporting. These dates change, so confirm with the official page before planning.

### Current Releases and Support Windows
| Platform | Current release | Support notes |
| :--- | :--- | :--- |
| SQL Server | **2025 (17.x)** | 2022: mainstream ends Jan 11, 2028 · 2019: extended ends Jan 8, 2030 · 2017: extended ends Oct 12, 2027 · **2016: extended support ended Jul 14, 2026** (paid Extended Security Updates available until 2029) · 2014 and earlier: out of support |
| Oracle Database | **AI Database 26ai** (long-term release) | 19c: Premier Support to Dec 31, 2029, Extended Support to Dec 31, 2032 (per Oracle's 2025 announcement; confirm in MOS note 742060.1) · 21c was an innovation release with short support |
| PostgreSQL | **18**; 19 in release candidate | Each major supported 5 years · **14 reaches end of life Nov 12, 2026** |
| MySQL | **9.7 LTS** and **8.4 LTS** | 8.0 is end-of-life (April 2026) · Innovation releases are supported only until the next one ships · releases after 9.7 use calendar versioning (YY.M) (confirm on the MySQL releases page) |
| Azure Data Studio | Retired Feb 28, 2026 | Use VS Code + MSSQL extension; SSMS for administration |

### Deprecated or Retired → Use Instead
| Platform | Deprecated or retired | Use instead |
| :--- | :--- | :--- |
| SQL Server | Database mirroring | Always On availability groups |
| SQL Server | SQL Trace and Profiler | Extended Events (XEvent Profiler in SSMS, Query Profiler in VS Code) |
| SQL Server | `text`, `ntext`, `image` data types | `varchar(max)`, `nvarchar(max)`, `varbinary(max)` |
| SQL Server | Big Data Clusters (retired 2025), Stretch Database | Microsoft Fabric, PolyBase, Azure SQL |
| Oracle | Non-CDB architecture (desupported from 21c) | Multitenant CDB/PDB |
| Oracle | Original `exp` / `imp` | Data Pump (`expdp` / `impdp`) |
| Oracle | Oracle Streams | GoldenGate |
| Oracle | `LONG` data type | `CLOB` / `BLOB` |
| PostgreSQL | `recovery.conf` (removed in 12) | `standby.signal` / `recovery.signal` plus settings in `postgresql.conf` |
| PostgreSQL | `SERIAL` for new tables | `GENERATED ... AS IDENTITY` |
| PostgreSQL | MD5 password authentication (deprecated in 18) | SCRAM-SHA-256 |
| MySQL | MyISAM tables | InnoDB |
| MySQL | Query cache (removed in 8.0) | Proper indexing, application caching, ProxySQL caching |
| MySQL | `mysql_native_password` | `caching_sha2_password` |
| MySQL | `utf8` (alias of 3-byte `utf8mb3`) | `utf8mb4` |
| Azure | Azure Database for PostgreSQL Single Server and Azure Database for MySQL Single Server (retired) | The flexible server offerings |
| Azure | Azure Cosmos DB for PostgreSQL (retirement path; new deployments blocked) | Elastic Clusters in Azure Database for PostgreSQL flexible server; Azure Cosmos DB for NoSQL for NoSQL workloads |
