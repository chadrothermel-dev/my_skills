# Vendor Hardware Catalog (Servers, Storage, Vendor Selection, Support)

> Reference file for the `datacenter-hardware` skill. Reviewed 2026-10. Version-sensitive details (models, SKUs, limits, prices, names) change — verify before relying on them.

> ⚠️ This catalog is a **circa-2024 generation snapshot**. By 2026 current generations include HPE ProLiant Gen12 (iLO 7), Dell PowerEdge 17G (e.g., R670/R770, iDRAC10), Lenovo ThinkSystem V4, Cisco UCS M8, AMD EPYC 9005 (Turin), and Intel Xeon 6 [verify each via the vendor configurator]. Treat models below as prior-generation unless confirmed current, and check End-of-Sale status before recommending.

## 2. Server Hardware Product Line Mastery

You possess encyclopedic knowledge of the current and recent-generation server portfolios from all four major enterprise vendors. When recommending servers, you must specify the exact product family, form factor, processor generation, and intended workload class.

### A. Lenovo ThinkSystem Server Portfolio

| Product Family | Form Factor | Processor Support | Primary Workload Class |
| :--- | :--- | :--- | :--- |
| **ThinkSystem SR630 V3** | 1U rack | Dual Intel Xeon Scalable 4th/5th Gen (Sapphire Rapids / Emerald Rapids) | General-purpose compute, virtualization (VMware/Hyper-V), database, web/app tier |
| **ThinkSystem SR650 V3** | 2U rack | Dual Intel Xeon Scalable 4th/5th Gen | GPU-accelerated AI/ML (up to 6x GPUs), large memory footprint databases, VDI |
| **ThinkSystem SR645 V3** | 1U rack | Dual AMD EPYC 9004 (Genoa) | Core-dense virtualization, HPC, cloud-native, software-defined storage |
| **ThinkSystem SR665 V3** | 2U rack | Dual AMD EPYC 9004 (Genoa) | GPU compute (up to 8x GPUs), AI training, scientific computing |
| **ThinkSystem SR850 V3** | 2U rack | Quad Intel Xeon Scalable | Mission-critical SAP HANA, large in-memory databases, Oracle RAC |
| **ThinkSystem ST650 V3** | 4U tower/rack | Dual Intel Xeon Scalable | Remote/branch office, edge, workstation-class GPU rendering |
| **ThinkSystem SD530 V3** | Half-width 1U (2-per-tray) | Dual Intel Xeon Scalable | High-density compute, HPC clusters, cloud service provider |
| **ThinkSystem SD650 V3** | Neptune liquid-cooled | Dual Intel Xeon Scalable | Extreme-density HPC, AI supercomputing, direct water cooling |
| **ThinkSystem SE350 V2** | Short-depth edge | Single Intel Xeon D / Xeon Scalable | Edge computing, retail, manufacturing floor, rugged environments |
| **ThinkAgile Series** | Varies | Intel/AMD | Hyperconverged (HCI) with VMware vSAN, Nutanix, or Azure Local (formerly Azure Stack HCI) |

**Lenovo Differentiators:** XClarity Administrator (centralized fleet management), XClarity Controller (BMC), Lenovo Capacity Planner, AnyBay drive flexibility (NVMe/SAS/SATA in same bay), Neptune liquid cooling leadership, consistent top rankings in ITIC reliability surveys.

### B. Hewlett Packard Enterprise (HPE) ProLiant & Synergy Portfolio

| Product Family | Form Factor | Processor Support | Primary Workload Class |
| :--- | :--- | :--- | :--- |
| **ProLiant DL360 Gen11** | 1U rack | Dual Intel Xeon Scalable 4th/5th Gen | General-purpose, virtualization, edge-to-cloud, dense rack deployments |
| **ProLiant DL380 Gen11** | 2U rack | Dual Intel Xeon Scalable 4th/5th Gen | Enterprise workhorse, databases, GPU workloads (up to 5x GPUs), SAP |
| **ProLiant DL385 Gen11** | 2U rack | Dual AMD EPYC 9004 (Genoa) | Virtualization, cloud-native, VDI, software-defined storage (SDS) |
| **ProLiant DL345 Gen11** | 1U rack | Single AMD EPYC 9004 (Genoa) | Cost-optimized single-socket density, web tier, CDN edge |
| **ProLiant DL560 Gen11** | 2U rack | Quad Intel Xeon Scalable | SAP HANA scale-up, mission-critical OLTP, large in-memory analytics |
| **ProLiant DL580 Gen11** | 4U rack | Quad Intel Xeon Scalable | Maximum memory capacity (12TB+), SAP BW/4HANA, Oracle Exadata alternative |
| **ProLiant ML350 Gen11** | 4U tower/rack | Dual Intel Xeon Scalable | Remote office, SMB, quiet tower deployments, internal GPU expansion |
| **ProLiant MicroServer Plus Gen11** | Ultra-compact tower | Single Intel Xeon E | Small office, home lab, file/print, lightweight edge |
| **Synergy 480 Gen11** | Composable blade | Dual Intel Xeon Scalable | Composable infrastructure, rapid bare-metal provisioning, private cloud |
| **Synergy 660 Gen11** | Composable double-wide blade | Quad Intel Xeon Scalable | Mission-critical composable compute, SAP HANA on blades |
| **Edgeline EL300** | Ruggedized edge | Intel Xeon D | OT/IT convergence, manufacturing, defense, harsh environments |
| **ProLiant RL300 Gen11** | 1U rack | Ampere Altra (ARM) | Cloud-native ARM workloads, energy-efficient microservices |

**HPE Differentiators:** iLO 6 (Integrated Lights-Out — industry-leading BMC with silicon root of trust), HPE OneView (infrastructure automation), HPE GreenLake (as-a-service consumption model), SmartArray/SmartHBA RAID controllers, Persistent Memory (NVDIMM/CXL) support, InfoSight predictive analytics, Silicon Root of Trust (hardware-anchored firmware verification).

### C. Dell Technologies PowerEdge Portfolio

| Product Family | Form Factor | Processor Support | Primary Workload Class |
| :--- | :--- | :--- | :--- |
| **PowerEdge R660** | 1U rack | Dual Intel Xeon Scalable 4th/5th Gen | Dense virtualization, web/app tier, general-purpose |
| **PowerEdge R760** | 2U rack | Dual Intel Xeon Scalable 4th/5th Gen | Enterprise workhorse, databases, moderate GPU (up to 4x GPUs) |
| **PowerEdge R6615** | 1U rack | Single AMD EPYC 9004 (Genoa) | Cost-optimized single-socket, cloud, SDS |
| **PowerEdge R6625** | 1U rack | Dual AMD EPYC 9004 (Genoa) | Core-dense virtualization, HPC, telco NFV |
| **PowerEdge R7615** | 2U rack | Single AMD EPYC 9004 (Genoa) | Storage-dense single-socket, object storage, big data |
| **PowerEdge R7625** | 2U rack | Dual AMD EPYC 9004 (Genoa) | GPU-heavy AI/ML (up to 8x GPUs), scientific computing |
| **PowerEdge R760xa** | 2U rack | Dual Intel Xeon Scalable + 4x DW GPUs | AI inference, deep learning, GPU-accelerated analytics |
| **PowerEdge R960** | 2U rack | Quad Intel Xeon Scalable | Mission-critical SAP HANA, Oracle, SQL Server scale-up |
| **PowerEdge T560** | Tower | Dual Intel Xeon Scalable | Remote/branch office, tower deployments, SMB |
| **PowerEdge MX (Modular)** | Modular blade chassis (MX7000) | Dual Intel/AMD per sled | Composable modular infrastructure, flexible I/O fabric |
| **PowerEdge XE9680** | 4U rack | Dual Intel Xeon + 8x NVIDIA GPUs | AI training at scale, LLM fine-tuning, HPC GPU clusters |
| **PowerEdge XR4000** | Short-depth 1U/2U | Intel Xeon Scalable | Telco edge, retail, rugged edge, NEBS-compliant |

**Dell Differentiators:** iDRAC9 (16G) / iDRAC10 (17G) (integrated Dell Remote Access Controller), OpenManage Enterprise (OME) fleet management, BOSS-N1 (Boot Optimized Storage Solution — M.2 NVMe mirrored boot), PERC 12 RAID controllers (HBA355e/H965i), Dell APEX (as-a-service), Cyber Recovery Vault integration, Smart Cooling airflow optimization, Multi-Vector Cooling.

### D. Cisco Unified Computing System (UCS) Portfolio

| Product Family | Form Factor | Processor Support | Primary Workload Class |
| :--- | :--- | :--- | :--- |
| **UCS C220 M7** | 1U rack | Dual Intel Xeon Scalable 4th/5th Gen | General-purpose, virtualization, edge, collaboration (Webex) |
| **UCS C240 M7** | 2U rack | Dual Intel Xeon Scalable 4th/5th Gen | Databases, big data, moderate GPU, SDS |
| **UCS C225 M7** | 1U rack | Single AMD EPYC 9004 (Genoa) | Cost-optimized compute, VDI, cloud |
| **UCS C245 M7** | 2U rack | Dual AMD EPYC 9004 (Genoa) | Core-dense virtualization, GPU-accelerated AI/ML |
| **UCS C480 M5 ML** (EOL — use a current-gen GPU platform) | 4U rack | Dual Intel Xeon + 8x GPUs | AI/ML training, deep learning, inference at scale |
| **UCS X210c M7** | Blade (X-Series chassis) | Dual Intel Xeon Scalable 4th/5th Gen | Next-gen modular computing, cloud-managed via Intersight |
| **UCS X410c M7** | Double-wide blade | Quad Intel Xeon Scalable | Mission-critical scale-up, SAP HANA, Oracle on blades |
| **UCS S3260 M5/M6** | 2U storage server | Dual Intel Xeon | Dense storage (56x 3.5" or 28x NVMe), object storage, backup targets |

**Cisco Differentiators:** Cisco Intersight (cloud-managed infrastructure platform — SaaS-based fleet management, firmware orchestration, workload optimization), Unified Fabric (converged Ethernet + storage over single wire using FCoE), Cisco VIC (Virtual Interface Card — up to 256 virtual NICs/HBAs per card), UCS Manager (domain-based policy-driven provisioning via service profiles), tight integration with Cisco Nexus/ACI networking, HyperFlex HCI platform, Kubernetes integration via Intersight Kubernetes Service (IKS).

---

## 3. Storage Hardware Product Line Mastery

### A. Dell Technologies Storage Portfolio

| Product Family | Architecture | Protocol Support | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **PowerStore** (500T/1200T/3200T/9200T) | Unified block + file, active-active dual controller, NVMe-native | iSCSI, FC (16/32Gb), NVMe-oF (RoCE/FC-NVMe), SMB, NFS | Tier-1 primary storage, VMware VMFS/vVols, databases (SQL, Oracle, SAP), mixed workloads |
| **PowerScale** (F710/F910/H700/H7000/A300/A3000) | Scale-out NAS, OneFS, single namespace | NFS, SMB, HDFS, S3 (via gateway), HTTP | Unstructured data at scale, media/entertainment, genomics, AI data lakes, home directories |
| **PowerFlex** (appliance or software-only) | Software-defined block storage (SDS), scale-out | iSCSI, NVMe-oF, SDC (native client) | Hyper-converged or storage-only, extreme IOPS, DevOps, private cloud, Kubernetes persistent volumes |
| **PowerVault ME5** (ME5012/ME5024/ME5084) | Dual-controller SAN, entry-level | iSCSI, FC (16/32Gb), SAS direct-attach | SMB/ROBO primary storage, backup target, DAS for servers, cost-optimized SAN |
| **PowerProtect DD** (DD6900/DD9400/DD9900) | Purpose-built backup appliance, deduplication | Ethernet (NFS, CIFS, DD Boost), FC | Enterprise backup target, data protection, cyber vault, long-term retention |
| **ObjectScale** | Software-defined object storage | S3 API | Cloud-native object storage, unstructured data, archive |
| **ECS (Elastic Cloud Storage)** | Object storage appliance | S3, Swift, Atmos, CAS, HDFS | Massive-scale archive, compliance retention, cold/warm object tiers |

### B. HPE Storage Portfolio

| Product Family | Architecture | Protocol Support | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Alletra Storage MP** (A9060/A9080) | Mission-critical, disaggregated shared everything | FC (32/64Gb), iSCSI, NVMe-oF, NFS, SMB | Tier-0/Tier-1, zero-downtime, 100% availability guarantee, SAP HANA, Oracle, mission-critical |
| **Alletra 5000** (5010/5020/5050) | Midrange block, unified, NVMe | iSCSI, FC, NVMe-oF, NFS, SMB | General-purpose primary storage, VMware, databases, mixed workloads |
| **Alletra 6000** (6010/6020/6050) | All-NVMe block storage, dual controller | iSCSI, FC, NVMe-oF | Performance-intensive workloads, VDI, latency-sensitive apps |
| **Alletra 9000** (9060/9080) | Tier-0 all-NVMe, triple+ controller scale-out | FC (32Gb), NVMe-oF | Mission-critical tier-0, financial trading, real-time analytics |
| **MSA 2070/1070** | Entry-level SAN, dual controller | iSCSI, FC (16/32Gb), SAS | SMB, ROBO, DAS, cost-constrained environments |
| **StoreOnce** (5260/5660) | Backup appliance, deduplication | Catalyst, NFS, SMB, VTL | Backup target, deduplication, cloud bank integration, long-term retention |
| **StoreEver Tape** (MSL2024/MSL3040/MSL6480) | LTO tape libraries | SAS, FC | Offline archive, air-gapped backup, regulatory compliance, cold storage |

**HPE Storage Differentiators:** InfoSight AI-driven predictive analytics (cross-stack telemetry), Timeless Storage program (technology refresh without data migration), Cloud Data Services (backup/DR to cloud), Zerto acquisition (continuous replication and DR).

### C. Lenovo Storage Portfolio

| Product Family | Architecture | Protocol Support | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **ThinkSystem DE Series** (DE2000H/DE4000H/DE4000F/DE6000H/DE6000F) | Unified hybrid/all-flash SAN (NetApp E-Series OEM) | iSCSI, FC (16/32Gb), SAS, NVMe-oF | Primary block storage, VMware, databases, mid-market SAN |
| **ThinkSystem DM Series** (DM3000H/DM5000H/DM5000F/DM7000H/DM7000F) | Unified NAS+SAN (NetApp ONTAP OEM) | NFS, SMB/CIFS, iSCSI, FC, S3, FCP | Enterprise unified storage, snapshots, replication, tiering, multiprotocol |
| **ThinkSystem DG Series** (DG5000F/DG7000F) | All-flash unified (NetApp ONTAP AFF OEM) | NFS, SMB, iSCSI, FC, NVMe-oF, S3 | Tier-1 all-flash, extreme performance, data management, cloud integration |
| **ThinkSystem DXP** (powered by Weka) | Parallel distributed file system | NFS, SMB, POSIX, S3, GPUDirect Storage | AI/ML training data pipelines, HPC, GPU-attached storage, extreme throughput |

**Lenovo Storage Differentiators:** NetApp ONTAP OEM partnership (DM/DG Series — access to ONTAP data management features: SnapMirror, SnapVault, FabricPool, MetroCluster), competitive pricing vs direct NetApp, XClarity integration for unified server+storage fleet management, DXP/Weka for AI data pipeline acceleration.

### D. Cisco Storage-Relevant Products

| Product Family | Architecture | Protocol Support | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **HyperFlex HX** (HX220c/HX240c) — end-of-sale, avoid for new builds [verify] | Hyperconverged infrastructure (HCI) | iSCSI (internal), NFS (external), FC passthrough | VMware or Microsoft HCI, VDI, ROBO, edge, Intersight-managed |
| **MDS 9000 Series** (9124V/9148V/9396V/9700/9718) | SAN fabric switches | FC (32/64Gb), FCoE, FCIP, NVMe/FC | Enterprise SAN fabric, multi-site SAN extension, VSANs, zoning |
| **UCS S3260** | Storage server (not array) | SAS/SATA/NVMe direct | Dense JBOD for SDS (Ceph, MinIO, HDFS), backup targets, object storage nodes |

**Cisco Storage Differentiators:** Cisco does not manufacture traditional storage arrays — their strength is in **SAN fabric switching** (MDS series is the market leader for FC SAN fabrics) and **HCI** (HyperFlex). Always pair Cisco UCS servers with a third-party storage array (Dell, HPE, NetApp, Pure Storage) connected via Cisco MDS SAN switches.

---

## 7. Vendor Selection Decision Framework

When the user has not specified a vendor, evaluate using these criteria:

| Decision Factor | Lenovo Strength | HPE Strength | Dell Strength | Cisco Strength |
| :--- | :--- | :--- | :--- | :--- |
| **Acquisition cost** | ★★★★★ (typically lowest) | ★★★ | ★★★★ | ★★★ |
| **Reliability/quality** | ★★★★★ (top ITIC rankings) | ★★★★★ | ★★★★ | ★★★★ |
| **Management tools** | ★★★★ (XClarity) | ★★★★★ (iLO + OneView) | ★★★★★ (iDRAC + OME) | ★★★★★ (Intersight) |
| **Storage integration** | ★★★★ (NetApp OEM) | ★★★★★ (native portfolio) | ★★★★★ (largest portfolio) | ★★★ (HCI + MDS fabric) |
| **Networking integration** | ★★★ | ★★★★ (Aruba) | ★★★ | ★★★★★ (Nexus/ACI/UCS unified) |
| **HPC / AI / GPU** | ★★★★★ (Neptune cooling) | ★★★★ | ★★★★★ (XE series) | ★★★ |
| **As-a-Service (OpEx)** | ★★★ (TruScale) | ★★★★★ (GreenLake) | ★★★★ (APEX) | ★★★★ (Intersight + Plus) |
| **Edge computing** | ★★★★ (SE350 V2) | ★★★★ (Edgeline) | ★★★★ (XR series) | ★★★ |
| **Composable / modular** | ★★★ | ★★★★ (Synergy) | ★★★★ (MX series) | ★★★★★ (UCS X-Series) |
| **SAP HANA certified** | ★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| **Existing Cisco network shop** | ★★★ | ★★★ | ★★★ | ★★★★★ (unified fabric) |

*Star ratings are subjective heuristics — never present them as measured data.*

**Golden Rule:** If the customer already has an established vendor relationship with support contracts, parts depot, and trained staff — **default to that vendor** unless there is a compelling technical or financial reason to switch. Vendor diversification introduces operational complexity, training costs, and spare parts inventory fragmentation.

---

## 8. Warranty, Support & Lifecycle Management

### Support Tier Matrix

| Tier | HPE | Dell | Lenovo | Cisco | When to Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Basic / Next Business Day** | Foundation Care NBD | ProSupport NBD | Base Warranty NBD | SNTC NBD | Dev/test, non-production, cost-optimized |
| **24x7 4-Hour Response** | Foundation Care 24x7 | ProSupport Plus 4hr | Premier Support 24x7 | SNTC 24x7x4 | Production servers, standard SLA |
| **Mission-Critical 24x7 6-Hour Fix** | Proactive Care 24x7 | ProSupport Mission Critical | Premier Support + ITSM | Solution Support | Tier-1 production, databases, SAP |
| **Onsite Spares + Dedicated Engineer** | Datacenter Care | ProDeploy Plus + Residency | Custom Managed Services | Cisco CX Level 3 | Hyperscale, financial, healthcare |

**Lifecycle Rules:**
1. **Minimum 3-year warranty on all production hardware.** 5-year for storage arrays and mission-critical servers.
2. **Track vendor End-of-Sale (EoS) and End-of-Support (EoSL) dates.** Plan hardware refresh 12-18 months before EoSL.
3. **Firmware updates are mandatory** — maintain a quarterly firmware update cycle using vendor fleet tools (XClarity, OneView, OME, Intersight).
4. **Maintain a critical spares kit** for each site: PSUs, drives, DIMMs, fans, RAID batteries. Vendor 4-hour response is not instant — have spares on-hand for Sev-1 outages.
5. **Standard refresh cycle:** Servers = 5-7 years. Storage arrays = 5-7 years. Network switches = 7-10 years. UPS batteries = 3-5 years.
