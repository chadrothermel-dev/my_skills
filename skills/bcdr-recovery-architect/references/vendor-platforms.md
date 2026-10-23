# Backup, Replication & Storage Platform Deep Dives

> Reference file for the `bcdr-recovery-architect` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

## Contents

- 2. Rubrik Security Cloud (RSC) Deep Dive
- 3. Zerto Continuous Data Protection (CDP) & Journaling
- 4. Cohesity DataProtect & Cyber Recovery
- 5. Veeam Backup & Replication (v12+) Deep Dive
- 6. Enterprise Storage-Native Replication & Active-Active BCDR
- 7. Cloud-Native Disaster Recovery: Azure Site Recovery & AWS DRS

## 2. Rubrik Security Cloud (RSC) Deep Dive

You command complete architectural and operational mastery of **Rubrik Security Cloud**, understanding its zero-trust data protection model, metadata architecture, and API-first ecosystem.

### Architectural Framework
- **Zero-Trust Architecture:** Data written to Rubrik is stored on an immutable, proprietary append-only file system (**Atlas**). No client or protocol (SMB, NFS) has direct access to raw storage blocks. Storage cannot be modified, encrypted, or deleted by external network commands.
- **Rubrik Cluster (Brik / Cloud Cluster):** Clustered nodes utilizing shared-nothing distributed architecture with a distributed metadata store. Available as physical appliances, software-defined nodes, or native Cloud Clusters in AWS, Azure, and GCP.
- **Rubrik Backup Service (RBS):** Lightweight client agent installed on Windows/Linux hosts providing application consistency (VSS integration), incremental changed block tracking, and log truncation (SQL Server, Oracle RAC).
- **Control Plane:** SaaS-managed **Rubrik Security Cloud (RSC)** management console providing centralized policy orchestration, global search, and telemetry across all on-prem clusters and cloud subscriptions.

### SLA Domains vs. Traditional Jobs
Rubrik eliminates legacy backup job management in favor of declarative **SLA Domains**:
- **Declarative Governance:** Define *RPO frequency* (e.g., take snapshot every 15 minutes, retain for 2 days; take daily, retain for 30 days; take monthly, retain for 12 months), *archival location* (Azure Blob, AWS S3 with Object Lock), and *replication target* (secondary Rubrik cluster).
- **Inheritance Engine:** Assign SLAs at vCenter, Datacenter, Cluster, VM folder, or individual VM level with automated inheritance rules.
- **Continuous Ingestion:** Rubrik orchestrates snapshot schedules dynamically to balance cluster I/O, eliminating snapshot storms and storage controller saturation.

### Live Mount & Instant Recovery Mechanics
- **Live Mount for VMs & Databases:** Instantly exposes a point-in-time snapshot as an active NFS datastore to VMware vSphere, or mounts a SQL Server/Oracle database directly to the host without data movement.
- **Near-Zero RTO:** Production reads/writes execute directly against the Rubrik cluster (performance is lower than primary storage) while Storage vMotion migrates data to tier-1 production SAN in the background.

### Threat Intelligence, Anomaly Detection & Cyber Resilience
- **Anomaly Detection (formerly Radar; RSC module names change — verify current naming):** Machine learning models inspect filesystem metadata and block entropy changes across successive snapshots to detect mass file modifications, unexpected encryption, or bulk deletions indicative of ransomware.
- **Threat Monitoring & Hunting:** Compares snapshots against threat intelligence feeds, known file hashes, and custom **YARA rules** to determine exact blast radius, initial infection date, and patient zero.
- **Data Security Posture / Sensitive Data Discovery (formerly Sonar):** Discovers and classifies sensitive data (PII, PCI, HIPAA, credentials) across backups to assess exfiltration risk and regulatory liability without production workload impact.
- **Orchestrated Recovery & Quarantine:** Quarantines infected snapshots to prevent accidental restoration of malware, and orchestrates clean-state recovery sequences.

### Rubrik PowerShell SDK & REST API Reference
```powershell

---

## 3. Zerto Continuous Data Protection (CDP) & Journaling

You command deep expertise in **Zerto** for low-RPO/low-RTO enterprise replication and disaster recovery.

### Architecture & Data Path
- **Zerto Virtual Manager (ZVM):** Central management appliance communicating with vCenter, Hyper-V, and cloud APIs (Zerto 10+ uses the Linux-based ZVM appliance; Windows ZVM is legacy — confirm Hyper-V support for the customer's Zerto version).
- **Virtual Replication Appliance (VRA):** Lightweight virtual appliance deployed on every protected host that captures writes via a hypervisor-level I/O filter/driver (mechanism varies by Zerto and vSphere version — verify).
- **Hypervisor-Based Continuous Replication:** Intercepts write I/O before it reaches storage and streams changes asynchronously over WAN to target VRAs with zero reliance on hypervisor snapshots.

### The Continuous Journal & Granular Point-in-Time Recovery
- **Journal Architecture:** Maintains every write delta in an append-only journal for a configurable retention period (1 hour up to 30 days).
- **Ransomware Rollback to the Exact Second:** Unlike traditional hourly snapshots where hours of data are lost, Zerto allows rewinding a multi-VM application stack to seconds before the encryption event occurred.
- **Checkpoints:** Automatic checkpoints inserted every few seconds, with manual and VSS-consistent tags.

### Virtual Protection Groups (VPGs)
- **Multi-VM Consistency Groups:** Groups interdependent VMs (e.g., 2 Web servers, 2 App servers, 2 Clustered DBs) to share a synchronized journal.
- **Write-Order Fidelity:** Guarantees that write operations across all VMs in the VPG are committed in the exact sequence they occurred, eliminating database corruption during failover.
- **Boot Order & Network Orchestration:** Built-in boot groups, startup delays, and automated IP reconfiguration (re-IP) for isolated test networks vs. live failover networks.

### Failover Testing Without Production Impact
- **Failover Test:** Instantiates VMs on target hosts using scratch journal disks connected to an isolated test bubble network. Zero downtime to production, zero interruption to ongoing replication.

---

## 4. Cohesity DataProtect & Cyber Recovery

You understand the **Cohesity** hyperconverged secondary data architecture.

### SpanFS Distributed Architecture
- **SpanFS File System:** Scale-out distributed file system built for unstructured data and backup streams, providing unlimited snapshots, source/inline deduplication, and compression.
- **SnapTree Architecture:** Redirect-on-write B-tree structure where snapshots are treated as first-class citizens. Creating, retaining, or deleting thousands of snapshots incurs zero performance penalty or I/O consolidation pause (stun).

### Cyber Vaulting (Cohesity FortKnox)
- **Isolated SaaS Vault:** Managed cloud vault providing a virtual air-gap. Backups replicated to FortKnox are protected by strict WORM policies and multi-party quorum authorization (dual-custody approval requiring two distinct administrators to authorize changes or deletions).
- **DataHawk Threat Scanning:** Integration with anomaly detection, vulnerability scanners (Tenable), and YARA signatures to evaluate snapshot integrity.

---

## 5. Veeam Backup & Replication (v12+) Deep Dive

### Architectural Blueprint
- **Veeam Backup Server:** Master scheduler, catalog manager, and job orchestration engine.
- **Veeam Proxies:** High-performance data movers. Transport modes:
  - *Direct Storage Access (SAN):* Direct read over FC/iSCSI fabric, zero ESXi host CPU/network overhead.
  - *Virtual Appliance (HotAdd):* Proxy VM mounts target VMDKs directly to its SCSI controller.
  - *Network Mode (NBD/NBDSSL):* Management network fallback.
- **Scale-Out Backup Repository (SOBR):** Multi-tier storage architecture combining local Performance Tier (NVMe/XFS/ReFS), Capacity Tier (S3/Blob with Object Lock/immutability), and Archive Tier (S3 Glacier/Azure Archive).

### Hardened Linux Repository (HLR) Engineering
- **Architecture:** Physical server running Ubuntu LTS or RHEL with XFS filesystem formatted with `-m reflink=1`.
- **Immutability Enforcement:** The Veeam Data Mover runs as a dedicated non-root account (added with single-use credentials), while a separate root-level Veeam immutability service sets the Linux immutable attribute (`chattr +i`) until the lock expires. SSH disabled post-deployment. (v13 also offers a pre-hardened Veeam appliance/ISO — verify options for the customer's version.)
- **Attack Resistance:** Even a compromised Domain Admin or compromised Veeam Backup Server cannot delete, truncate, or overwrite backup files on the HLR before the retention lock expires.

### Continuous Data Protection (CDP) & SureBackup
- **Veeam CDP:** Uses a vSphere VAIO I/O filter to stream block changes to replica VMs, delivering seconds-level RPOs without VM snapshots (vSphere-only; confirm VAIO support for the target vSphere/VCF version).
- **SureBackup Automated Verification:** Spins up VMs in an isolated Virtual Lab using Instant VM Recovery, verifies OS boot (heartbeat), tests networking (ping), and executes application scripts (e.g., verifying SQL database integrity via DBCC CHECKDB or testing LDAP queries against a domain controller).

---

## 6. Enterprise Storage-Native Replication & Active-Active BCDR

When sub-second RTO and zero RPO are mandatory, software-based backup must be paired with storage array replication:

### NetApp SnapMirror & MetroCluster
- **SnapMirror Synchronous (SM-S):** Zero-RPO block replication between ONTAP arrays.
- **NetApp MetroCluster:** Geographically separated stretch cluster providing zero-RPO, zero-RTO active-active storage infrastructure across campus or metro distances (<10ms RTT) with automated tiebreaker failover.

### Pure Storage ActiveCluster & SafeMode
- **ActiveCluster:** Fully synchronous, bidirectional active-active replication between FlashArray systems with transparent multi-site failover mediated by the cloud-based Pure1 quorum mediator.
- **SafeMode Snapshots:** Array-enforced snapshot protection. Snapshots cannot be deleted, modified, or shortened in retention period by any administrator; changes require out-of-band PIN verification with Pure Storage Support.

### Dell PowerProtect Data Domain & Retention Lock
- **DD Boost:** Proprietary client-side deduplication protocol reducing network throughput requirements up to 99%.
- **Retention Lock Compliance Mode:** Hardware-enforced immutable storage adhering to SEC 17a-4(f) regulations, requiring strict security officer authorization.

---

## 7. Cloud-Native Disaster Recovery: Azure Site Recovery & AWS DRS

### Azure Site Recovery (ASR)
- **Continuous Block Replication:** Azure-to-Azure uses the Mobility service extension with a cache storage account in the source region; VMware/physical uses the modernized ASR replication appliance (the classic configuration-server architecture retired on March 30, 2026 — migrate any remaining classic replications).
- **Automated Recovery Plans:** Defines multi-VM startup order, injects PowerShell runbooks for network peering and DNS registration, and configures post-failover NSG rules.
- **Test Failover:** Spins up isolated test VNets for validation without impacting live replication.

### AWS Elastic Disaster Recovery (AWS DRS)
- **Continuous Replication:** Replicates on-prem or cloud block storage into a low-cost staging area in AWS (EBS gp3 volumes).
- **Automated Conversion:** On failover, AWS DRS automatically launches production EC2 instances with converted drivers and firmware.
