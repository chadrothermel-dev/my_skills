# Per-skill configuration for technical skills.
# fixes: (old, new[, replace_all]) exact-match replacements applied to the source prompt.

TECH = [
# ---------------------------------------------------------------- Infrastructure
dict(
    src="vmware_virtualization_expert_prompt.md", name="vmware-vsphere", category="infra",
    title="VMware vSphere & VCF Virtualization Architect",
    role="Senior VMware virtualization architect (VCDX-level) for vSphere, vSAN, NSX, and VMware Cloud Foundation. Designs, troubleshoots, and automates with PowerCLI and ESXCLI, defaulting to CLI and code over GUI walkthroughs.",
    description="VMware vSphere, vCenter, ESXi, vSAN, NSX, and VMware Cloud Foundation (VCF) architecture, troubleshooting, and PowerCLI automation. Use when the user asks about ESXi/vCenter design or upgrades, HA/DRS/FT, vMotion, datastores and storage protocols, vDS networking, snapshots, esxtop performance analysis, host hardening, HCX migrations, VCF Operations/Aria, or wants a PowerCLI script for a vSphere task.",
    clarify=["vSphere/VCF version and licensing edition", "cluster size and storage type (vSAN OSA/ESA, VMFS, NFS, vVols)", "whether the change can tolerate VM downtime or host maintenance mode"],
    fixes=[
        ("Your solutions must adhere to VMware Validated Designs (VVD) and CIS/DISA STIG hardening guidelines.",
         "Your solutions align with VMware Cloud Foundation reference architectures (VMware Validated Designs are retired) and CIS/DISA STIG hardening guidelines."),
        ("- **Host Profiles:** Centralized ESXi configuration management. Best practice: extract profile from a hardened reference host.",
         "- **Host Profiles:** Legacy centralized ESXi configuration. On vSphere 8+ clusters managed by a vLCM image, prefer **vSphere Configuration Profiles** (cluster-level desired-state configuration)."),
        ("**NSX-T Overview:**", "**NSX Overview (formerly NSX-T):**"),
        ("**Aria Operations (vROps):**", "**VCF Operations (formerly Aria Operations / vROps):**"),
        ("**Aria Automation (vRA):**", "**VCF Automation (formerly Aria Automation / vRA):**"),
        ("- **Upgrades:** Always follow the VMware Update Sequence: Aria Suite -> vCenter -> ESXi -> VMware Tools -> VM Hardware Version.",
         "- **Upgrades:** Follow the published update sequence for your release (generally management/operations tooling -> vCenter -> ESXi -> VMware Tools -> VM hardware version). In VCF, lifecycle is orchestrated by SDDC Manager / VCF Operations — follow its bill of materials."),
        ("""$VMs = Get-Cluster "Prod-Cluster" | Get-VM | Where-Object {$_.HardwareVersion -lt "vmx-19"}
foreach ($vm in $VMs) {
    Set-VM -VM $vm -Version v20 -Confirm:$false
}""",
         """# Compare numerically: as strings, "vmx-9" sorts AFTER "vmx-19" and would be skipped.
$TargetVersion = 20
$VMs = Get-Cluster "Prod-Cluster" | Get-VM |
    Where-Object { [int]($_.HardwareVersion -replace '\\D') -lt $TargetVersion -and $_.PowerState -eq 'PoweredOff' }
foreach ($vm in $VMs) {
    Set-VM -VM $vm -HardwareVersion "vmx-$TargetVersion" -Confirm:$false   # -Version is deprecated
}"""),
        ("1. Determine the vSphere version context (if not specified, default to vSphere 8.x).",
         "1. Determine the vSphere/VCF version context. If not specified, ask — vSphere 8 and VCF 9 are current; vSphere 7 reached end of general support on 2 Oct 2025."),
        ("- **Use Official Terminology:** Refer to products by their current names (e.g., *Aria Operations* instead of *vROps*, *vSphere Lifecycle Manager (vLCM)* instead of *VUM*).",
         "- **Use Official Terminology:** Refer to products by their current names (e.g., *VCF Operations* in VCF 9 / *Aria Operations* in VCF 5.x instead of *vROps*; *vSphere Lifecycle Manager (vLCM)* instead of *VUM*)."),
    ],
    notes=[
        "Broadcom licensing: vSphere is now sold primarily as VCF / vSphere Foundation subscriptions; confirm the customer's entitlement before recommending features (e.g., vSAN capacity, NSX).",
        "PowerCLI is distributed as **VCF.PowerCLI** (9.x) alongside the older VMware.PowerCLI 13.x — the core cmdlets live in `VMware.VimAutomation.Core` in both [verify module name for the user's install].",
        "The compatibility list is now the **Broadcom Compatibility Guide** (formerly VMware HCL).",
    ],
),
dict(
    src="windows_server_expert_prompt.md", name="windows-server", category="infra",
    title="Windows Server Platform Architect",
    role="Senior Windows platform architect for AD DS, Group Policy, DNS/DHCP, failover clustering, Hyper-V, S2D, IIS, and hardening — PowerShell-first, security-by-default.",
    description="Windows Server architecture, administration, and PowerShell automation. Use when the user asks about Active Directory (FSMO, replication, restore), Group Policy design or troubleshooting, DNS/DHCP, failover clustering and quorum, Hyper-V, Storage Spaces Direct, IIS, WSUS/patching, LAPS/gMSA/tiered admin hardening, or Windows Server version and edition choices.",
    clarify=["Windows Server version(s) and edition", "domain/forest functional level and number of sites", "on-prem only, Azure Arc–connected, or Azure Local"],
    fixes=[
        ("| **2025** | Hotpatching, Next-Gen AD, SMB over QUIC (all editions), NVMe optimization | TBD |",
         "| **2025** | Hotpatching (Azure Arc), Next-Gen AD (32k DB pages), SMB over QUIC (all editions), NVMe optimization | Nov 2034 [verify] |"),
        ("- Hyper-converged infrastructure. Requires Datacenter edition. Minimum 2 nodes (needs witness), scales to 16. Requires RDMA (RoCEv2 or iWARP) network cards.",
         "- Hyper-converged infrastructure. Requires Datacenter edition. Minimum 2 nodes (needs witness), scales to 16. 10 GbE+ networking required; RDMA (RoCEv2 or iWARP) strongly recommended [verify current requirements]. For Azure Local, follow its validated-node catalog."),
        ("- **Architecture:** Autonomous (upstream manages updates, downstream syncs and manages approvals independently) vs Replica (upstream manages updates AND approvals).",
         "- **Status:** WSUS is deprecated (no new features, still supported). Plan toward Azure Update Manager, Windows Autopatch / Windows Update for Business, or MECM.\n- **Architecture:** Autonomous (upstream manages updates, downstream syncs and manages approvals independently) vs Replica (upstream manages updates AND approvals)."),
        ("- **LAPS:** Local Administrator Password Solution. Rotates local admin passwords and stores securely in AD. (Windows LAPS native in Server 2022+ / Windows 11).",
         "- **LAPS:** Windows LAPS rotates local admin passwords and stores them in AD or Entra ID. It is built into Windows Server 2019+ and Windows 10/11 (April 2023 updates); legacy Microsoft LAPS is deprecated.\n- **Server 2025 security defaults:** SMB signing required by default, LDAP signing/channel-binding hardening, NTLMv1 removed, RC4 Kerberos being phased out — test application compatibility before upgrading [verify]."),
        ("5. **Monitoring:** All event logs (Security, System) must be forwarded to a central SIEM (e.g., Azure Sentinel, Splunk) via Windows Event Forwarding (WEF).",
         "5. **Monitoring:** Forward Security and System event logs to a central SIEM (e.g., Microsoft Sentinel via Azure Monitor Agent, Splunk) or via Windows Event Forwarding (WEF)."),
        ("(e.g., `Test-Connection`, `Get-EventLog`, `dcdiag`)", "(e.g., `Test-NetConnection`, `Get-WinEvent`, `dcdiag`)"),
    ],
    notes=[
        "Use `Get-WinEvent` (not the deprecated `Get-EventLog`) in all scripts; `Get-EventLog` doesn't exist in PowerShell 7.",
        "Windows Server 2016 extended support ends 12 Jan 2027 — flag it as a migration priority.",
    ],
),
dict(
    src="linux_systems_administration_prompt.md", name="linux-sysadmin", category="infra",
    title="Linux Systems Architect (RHEL & Ubuntu)",
    role="Senior Linux systems architect (RHCE-level) for RHEL-family and Ubuntu/Debian: systemd, storage/LVM, networking, SELinux/AppArmor, performance, and robust Bash.",
    description="Linux systems administration, troubleshooting, hardening, and Bash scripting for RHEL, Rocky, Alma, Ubuntu, and Debian. Use when the user asks about systemd units or timers, dnf/apt packages, LVM and filesystems, NFS/iSCSI, nmcli/netplan networking, firewalld/ufw, SSH hardening, SELinux or AppArmor denials, performance tuning, Podman/Docker containers, or wants a production-safe shell script.",
    clarify=["distribution and major version", "whether the host is production and how it is managed (Ansible, Satellite, manual)", "root vs sudo access"],
    fixes=[
        ("| **Default Firewall** | `firewalld` | `ufw` |", "| **Default Firewall** | `firewalld` | `ufw` (Ubuntu; installed but inactive by default) / `nftables` (Debian) |"),
        ("| **Release Cycle** | 10-year enterprise lifecycle | 5-year LTS releases (Ubuntu) |",
         "| **Release Cycle** | 10-year lifecycle (RHEL 9/10) | 5-year standard LTS; up to 10–12 years with Ubuntu Pro [verify] |"),
        ("- **NFS Server**: `/etc/exports` (`/data 192.168.1.0/24(rw,sync,no_root_squash)`). Apply with `exportfs -arv`.",
         "- **NFS Server**: `/etc/exports` (`/data 192.168.1.0/24(rw,sync,root_squash)`). Apply with `exportfs -arv`. Never use `no_root_squash` unless a specific workload requires it — it lets client root act as server root."),
        ("- **Sysctl Tuning** (`/etc/sysctl.conf`):\n  ```ini\n  net.ipv4.ip_forward = 1\n  vm.swappiness = 10",
         "- **Sysctl Tuning** (drop-in file such as `/etc/sysctl.d/90-tuning.conf`; apply with `sysctl --system`). Tune only from measurements. `net.ipv4.ip_forward` is a routing/security decision, not a performance knob — enable it only on routers/container hosts that need it:\n  ```ini\n  vm.swappiness = 10"),
        ("- **Podman**: Daemonless, rootless. Commands mirror Docker (`alias docker=podman`). Generates systemd unit files natively: `podman generate systemd --new --name myapp > /etc/systemd/system/myapp.service`.",
         "- **Podman**: Daemonless, rootless. Commands mirror Docker (`alias docker=podman`). Run containers as services with **Quadlet** (`.container` files in `/etc/containers/systemd/` or `~/.config/containers/systemd/`, Podman 4.4+); `podman generate systemd` is deprecated."),
    ],
    notes=["RHEL 10 is generally available (2025); default new RHEL guidance to 9 or 10 and Ubuntu to 24.04 LTS unless the user states otherwise."],
),
dict(
    src="networking_infrastructure_expert_prompt.md", name="enterprise-networking", category="infra",
    title="Enterprise Network Architect",
    role="Senior network architect (CCIE-level) across switching, routing, firewalls, VPN, load balancing, wireless, and SD-WAN — configuration-ready, multi-vendor, security-first.",
    description="Enterprise network design, configuration, and troubleshooting. Use when the user asks about VLANs/STP/LACP, OSPF/BGP/EIGRP routing, VRFs, Palo Alto or Fortinet firewall policy and NAT, IPsec/IKEv2 or remote-access VPN, F5/HAProxy load balancing, 802.1X NAC, Wi-Fi design, SD-WAN, DNS/DHCP infrastructure, packet captures, or wants Cisco IOS/NX-OS or PAN-OS configuration.",
    clarify=["vendor, platform, and OS version", "current topology and what must not go down during the change", "change window and out-of-band access availability"],
    fixes=[
        ("  - *Phase 1 (IKE):* Authenticate and secure the management channel. Main vs Aggressive mode. (AES-256-GCM, SHA-384, DH Group 14/19/20+).",
         "  - *Phase 1 (IKE):* Use **IKEv2** by default. IKEv1 (Main vs Aggressive mode) only for legacy peers — never Aggressive mode with pre-shared keys. Prefer AES-256-GCM, SHA-384, DH Group 19/20/21 (Group 14 minimum)."),
        ("- **SSL VPN / Remote Access:** Clientless (web portal) or thick client (AnyConnect, GlobalProtect, FortiClient). Uses TLS.",
         "- **SSL VPN / Remote Access:** Clientless (web portal) or thick client (Cisco Secure Client, GlobalProtect, FortiClient). Several vendors are de-emphasizing SSL-VPN tunnel mode after repeated critical CVEs (e.g., FortiOS removed SSL-VPN tunnel mode in 7.6.x [verify]) — prefer IPsec/IKEv2 or ZTNA for new remote-access designs."),
        ("controlled by central orchestrator (Cisco vManage, SilverPeak, VeloCloud).",
         "controlled by a central orchestrator (Cisco Catalyst SD-WAN Manager, HPE Aruba EdgeConnect, VeloCloud, Fortinet, Prisma SD-WAN) [verify current product names/ownership]."),
        ("- **Architecture:** Separation of Control Plane (Smartbrain) and Data Plane (Forwarding).",
         "- **Architecture:** Separation of Control Plane (controllers/orchestrator) and Data Plane (forwarding edges)."),
        ("- **SNMP:** Always mandate SNMPv3 (AuthPriv: SHA auth, AES encryption).",
         "- **SNMP:** Always mandate SNMPv3 authPriv (SHA-256 or stronger auth, AES-128/256 privacy where supported)."),
    ],
    notes=["Cisco IOS-XE 802.1X: the example uses legacy IBNS 1.0 `authentication` commands; on current IOS-XE prefer IBNS 2.0 (`access-session` + policy-maps / C3PL) [verify for platform]."],
),
dict(
    src="datacenter_hardware_expert_prompt.md", name="datacenter-hardware", category="infra",
    title="Data Center Hardware Architect",
    role="Senior data center hardware architect across Dell, HPE, Lenovo, and Cisco servers, storage, NICs, power, and cooling — specific BoMs, TCO-driven, certification-aware.",
    description="Server, storage, and data center hardware selection and sizing across Dell PowerEdge, HPE ProLiant/Alletra, Lenovo ThinkSystem, and Cisco UCS. Use when the user asks what hardware to buy for a workload (VMware, SQL, SAP HANA, VDI, Kubernetes, backup, AI/GPU), CPU/RAM/drive/RAID/NIC choices, rack power and cooling math, vendor comparisons, warranty tiers, or a bill of materials.",
    fixes=[
        ("**Dell Differentiators:** iDRAC10 (integrated Dell Remote Access Controller)",
         "**Dell Differentiators:** iDRAC9 (16G) / iDRAC10 (17G) (integrated Dell Remote Access Controller)"),
        ("| AI/ML Training | AMD EPYC 9654 (96-core) **or** Intel Xeon w9-3595X |",
         "| AI/ML Training | AMD EPYC 9004/9005 high-core SKUs **or** Intel Xeon 6 server SKUs (note: Xeon w9-3595X is a workstation part, not a server CPU) |"),
        ("- **Never use RAID 5 with drives >2TB.**", "- **Never use RAID 5 with large HDDs (>2TB).**"),
        ("2. **Never mix drive types within a RAID group or vSAN disk group** (e.g., do not mix NVMe and SAS SSD in the same group).",
         "2. **Never mix drive types within a RAID group or vSAN OSA disk group** (vSAN ESA has no disk groups — it uses a single NVMe storage pool)."),
        ("(SAP HANA Hardware Directory, VMware HCL, Microsoft SVVP, Oracle certification matrix, Red Hat HCL)",
         "(SAP HANA Hardware Directory, Broadcom Compatibility Guide (formerly VMware HCL), Microsoft SVVP / Azure Local catalog, Oracle certification matrix, Red Hat HCL)"),
        ("Hyperconverged (HCI) with VMware vSAN, Nutanix, or Microsoft Azure Stack HCI", "Hyperconverged (HCI) with VMware vSAN, Nutanix, or Azure Local (formerly Azure Stack HCI)"),
        ("| **HyperFlex HX** (HX220c/HX240c) |", "| **HyperFlex HX** (HX220c/HX240c) — end-of-sale, avoid for new builds [verify] |"),
        ("| **UCS C480 M5 ML** |", "| **UCS C480 M5 ML** (EOL — use a current-gen GPU platform) |"),
        ("**Golden Rule:** If the customer already has", "*Star ratings are subjective heuristics — never present them as measured data.*\n\n**Golden Rule:** If the customer already has"),
    ],
    splits=[dict(
        file="hardware-catalog.md", title="Vendor Hardware Catalog (Servers, Storage, Vendor Selection, Support)",
        headings=["## 2. Server Hardware Product Line Mastery", "## 3. Storage Hardware Product Line Mastery",
                  "## 7. Vendor Selection Decision Framework", "## 8. Warranty, Support & Lifecycle Management"],
        pointer="Vendor server/storage portfolios, vendor-selection scoring, and support tiers",
        warning="This catalog is a **circa-2024 generation snapshot**. By 2026 current generations include HPE ProLiant Gen12 (iLO 7), Dell PowerEdge 17G (e.g., R670/R770, iDRAC10), Lenovo ThinkSystem V4, Cisco UCS M8, AMD EPYC 9005 (Turin), and Intel Xeon 6 [verify each via the vendor configurator]. Treat models below as prior-generation unless confirmed current, and check End-of-Sale status before recommending.",
    )],
    notes=[
        "Before naming a model, confirm it is current with web search or the vendor configurator (Dell Product Selector, HPE iQuote / One Config, Lenovo DCSC, Cisco Commerce). If tools are unavailable, recommend the *family* and mark the model **[verify]**.",
        "Intel 4th/5th Gen Xeon provide 80 PCIe Gen5 lanes per socket; Xeon 6 and EPYC 9005 change lane and memory-channel counts — verify per SKU.",
    ],
),
dict(
    src="kubernetes_container_platform_prompt.md", name="kubernetes-platform", category="infra",
    title="Kubernetes & Container Platform Architect",
    role="Senior Kubernetes architect (CKA/CKS-level) for on-prem, vSphere, and managed clusters: control plane HA, CNI/CSI, GitOps, policy, and Day-2 operations.",
    description="Kubernetes cluster design, operations, and troubleshooting across kubeadm, RKE2, OpenShift, vSphere Kubernetes Service, AKS, and EKS. Use when the user asks about control-plane/etcd HA and backup, CNI (Cilium/Calico) or CSI storage choices, ingress and Gateway API, MetalLB, ArgoCD/Flux GitOps, Helm/Kustomize, Kyverno/Gatekeeper policy, Pod Security, secrets, node upgrades, or debugging CrashLoopBackOff/OOMKilled/NotReady.",
    clarify=["Kubernetes version and distribution", "on-prem/vSphere/cloud and existing CNI/CSI", "GitOps and policy tooling already in place"],
    fixes=[
        ("| **VMware Tanzu (TKG)** | vSphere, Multi-Cloud | Native vSphere CNS (Storage) and NSX-T integration. ClusterAPI lifecycle management. |",
         "| **vSphere Kubernetes Service (VKS, formerly Tanzu Kubernetes Grid)** | vSphere / VCF | Native vSphere CNS storage and NSX integration. ClusterAPI lifecycle management. |"),
        ("| **Rancher RKE2** | Government, Edge, Enterprise | FIPS-140-2 compliant,", "| **Rancher RKE2** | Government, Edge, Enterprise | FIPS 140-validated crypto modules [verify current validation],"),
        ("- **OS Distributions:** Ubuntu 22.04 LTS, RHEL 8/9,", "- **OS Distributions:** Ubuntu 24.04 LTS, RHEL 9/10,"),
        ("- **Kubelet:** Must configure `systemd` cgroup driver (`cgroupfs` is deprecated/unsupported). `failSwapOn: true` (unless explicitly testing alpha swap features in K8s 1.28+).",
         "- **Kubelet:** Use the `systemd` cgroup driver on cgroup v2. Keep `failSwapOn: true` unless you deliberately adopt node swap (`LimitedSwap`, cgroup v2 required) — check the feature's maturity for your version [verify]."),
        ("ETCDCTL_API=3 etcdctl", "etcdctl", True),
        ("etcdctl --write-out=table snapshot status", "etcdutl --write-out=table snapshot status"),
        ("# etcd restore (Single node example)\netcdctl snapshot restore", "# etcd restore (Single node example) — etcdctl snapshot restore is deprecated; use etcdutl\netcdutl snapshot restore"),
        ("  - **NGINX Ingress:** Standard, robust, Lua-based routing.",
         "  - **ingress-nginx:** The community controller was retired by Kubernetes SIG Network (maintenance ended March 2026 [verify]). Do not choose it for new clusters; migrate existing ones to a Gateway API implementation or a maintained controller."),
        ("spec:\n  validationFailureAction: Enforce\n  rules:", "spec:\n  rules:"),
        ("    validate:\n      message: \"Running as root is not allowed.\"",
         "    validate:\n      failureAction: Enforce   # Kyverno 1.13+ rule-level setting; older versions use spec.validationFailureAction\n      message: \"Running as root is not allowed.\""),
        ("- **HashiCorp Vault Injector:**", "- **Secrets Store CSI Driver:** Mounts secrets from Key Vault / Vault / AWS directly as volumes.\n- **HashiCorp Vault Injector:**"),
        ("2. **Explicit Resource Allocation:** Every container MUST have `resources.requests` and `resources.limits` defined. Guaranteed QoS requires Requests == Limits.",
         "2. **Explicit Resource Allocation:** Every container has CPU and memory `requests` and a memory `limit`. CPU limits are a deliberate choice (they cause CFS throttling); add them when policy or Guaranteed QoS (requests == limits) requires it."),
        ("- **Version Awareness:** All API versions must target Kubernetes 1.28-1.31+ (e.g., `networking.k8s.io/v1` for Ingress, not `v1beta1`).",
         "- **Version Awareness:** Ask for the cluster version; default to currently supported upstream releases (see kubernetes.io/releases) and never use removed APIs (e.g., `networking.k8s.io/v1` for Ingress, not `v1beta1`)."),
        ("- **Resource Limits:** All provided pod specs MUST include `resources.requests` and `resources.limits`.",
         "- **Resources:** All provided pod specs include CPU/memory requests and a memory limit (CPU limit where policy requires)."),
    ],
),
# ---------------------------------------------------------------- Cloud, IaC & Automation
dict(
    src="azure_cloud_solutions_architect_prompt.md", name="azure-solutions-architect", category="cloud",
    title="Azure Cloud Solutions Architect",
    role="Senior Azure solutions architect: turns requirements into secure, resilient, cost-aware Azure architectures with Bicep/Terraform and CI/CD, aligned to CAF landing zones and the Well-Architected Framework.",
    description="Microsoft Azure architecture and service selection with production IaC. Use when the user asks which Azure service to use (Container Apps vs AKS vs App Service vs Functions, Cosmos DB vs Azure SQL, Service Bus vs Event Grid, Front Door vs App Gateway), landing zones and hub-spoke networking, Private Endpoints and Zero Trust, WAF reviews, RPO/RTO design, or wants Bicep, Terraform, Azure CLI, or Az PowerShell for an Azure deployment.",
    clarify=["workload type, scale, and concurrency", "RPO/RTO and compliance requirements (e.g., HIPAA, PCI)", "existing landing zone and IaC tool preference (Bicep vs Terraform)"],
    fixes=[
        ("* **Azure Spring Apps:** Best for enterprise Java/Spring Boot microservices needing managed lifecycle, Eureka discovery, Config Server, and distributed tracing.",
         "* **Azure Spring Apps:** **Retiring (retirement announced 2025) — do not recommend for new workloads.** Run Spring Boot on Azure Container Apps (Java components) or App Service instead [verify retirement date]."),
        ("* **Azure Cache for Redis (Standard / Premium / Enterprise):** High-speed in-memory data cache, session state store, Redis streams, and RedisSearch modules.",
         "* **Azure Managed Redis** (successor to Azure Cache for Redis, which has an announced retirement — use Azure Managed Redis for new builds [verify]): in-memory cache, session state, streams, and search modules."),
        ("* **Azure Event Hubs & Apache Kafka on HDInsight:**", "* **Azure Event Hubs (Kafka-compatible endpoint; prefer over HDInsight Kafka for new builds):**"),
        ("* **Azure OpenAI Service:** Enterprise-grade foundation models (GPT-4o, embeddings, reasoning models)",
         "* **Azure OpenAI in Microsoft Foundry:** Enterprise-grade foundation models (current GPT and reasoning model families plus embeddings — the catalog changes frequently; check Foundry's model list)"),
        ("* **Azure Synapse Analytics & Azure Databricks:**", "* **Azure Synapse Analytics & Azure Databricks** (Microsoft's strategic direction for new analytics is Fabric; Synapse remains supported):"),
        ("* **Azure Key Vault & Managed HSM:** FIPS 140-2 Level 2/3 cryptographic storage", "* **Azure Key Vault & Managed HSM:** FIPS 140-validated cryptographic storage (Managed HSM: FIPS 140-3 Level 3 [verify])"),
        ("1. **Clarify Ambiguity When Necessary:** If a user request lacks crucial non-functional parameters (e.g., expected concurrency, RTO/RPO requirements, budget limits, compliance standards like HIPAA/PCI), highlight reasonable production assumptions while requesting clarification.",
         "1. **Clarify Ambiguity When Necessary:** If a request lacks crucial non-functional parameters (concurrency, RTO/RPO, budget, compliance), state reasonable production assumptions and ask only the questions that would change the design."),
    ],
    splits=[dict(
        file="service-catalog.md", title="Azure Service Catalog & Scenario Decision Engine",
        headings=["## 2. Universal Azure Service Catalog & Scenario Decision Engine"],
        pointer="When choosing between Azure services (compute, networking, data, analytics, AI, messaging, identity, hybrid)",
    )],
    notes=["Use the Microsoft Learn MCP server (if connected) to confirm SKU limits, regional availability, and retirement notices before finalizing a design."],
),
dict(
    src="terraform_infrastructure_expert_prompt.md", name="terraform-iac", category="cloud",
    title="Terraform & OpenTofu IaC Architect",
    role="Senior IaC architect for Terraform and OpenTofu across Azure, AWS, vSphere, and network providers — state safety, modular design, policy-as-code, and CI/CD.",
    description="Terraform and OpenTofu infrastructure-as-code design, review, and debugging. Use when the user asks to write or refactor HCL, design modules, set up remote state and locking, import or move resources, fix drift, use for_each/dynamic blocks, pin providers, write terraform tests, add policy-as-code (Sentinel/OPA), use Terragrunt, or build a plan/apply pipeline.",
    clarify=["Terraform or OpenTofu version and providers in use", "backend/state location and team workflow (CLI, HCP Terraform, Atlantis, pipelines)", "greenfield vs refactoring existing state"],
    fixes=[
        ("    *   **State Encryption:** Essential for protecting sensitive data (passwords, keys) stored in plain text within the state file. Handled via backend encryption (e.g., S3 SSE, Azure Storage encryption).",
         "    *   **State Encryption:** Essential for protecting sensitive data stored in plain text within state. Use backend encryption (S3 SSE, Azure Storage encryption); OpenTofu 1.7+ adds native client-side state encryption.\n    *   **Keeping secrets out of state:** Terraform 1.10+ **ephemeral values/resources** and 1.11+ **write-only arguments** avoid persisting secrets where providers support them."),
        ("    *   `s3`: AWS S3. Supports locking via DynamoDB.", "    *   `s3`: AWS S3. Native lock files via `use_lockfile = true` (Terraform 1.10+); DynamoDB-based locking is deprecated."),
        ("    *   `cloud`: Terraform Cloud / Enterprise.", "    *   `cloud`: HCP Terraform (formerly Terraform Cloud) / Terraform Enterprise."),
        ("    *   `tfsec` / `checkov`: Scans for security misconfigurations (e.g., open security groups, unencrypted storage).",
         "    *   `trivy config` (tfsec is now part of Trivy) / `checkov`: Scans for security misconfigurations (e.g., open security groups, unencrypted storage).\n*   **Testing:** `terraform test` (1.6+) with `.tftest.hcl` files for module unit and integration tests; Terratest for complex end-to-end cases."),
        ('can(regex("^t[23].(micro|small)$", var.instance_type))', 'can(regex("^t[23]\\\\.(micro|small)$", var.instance_type))'),
        ("1.  **Syntax Check:** Ensure all provided HCL is syntactically valid for Terraform >= 1.0.", "1.  **Syntax Check:** Ensure all provided HCL is valid for the user's pinned Terraform/OpenTofu version (default: a currently supported 1.x release)."),
        ('      version = "~> 3.80.0"', '      version = "~> 4.0"   # azurerm 4.x requires subscription_id (provider block or ARM_SUBSCRIPTION_ID)'),
        ('      version = "~> 3.30.0"', '      version = "~> 3.0"'),
        ('    key                  = "aks-datadog.tfstate"\n  }', '    key                  = "aks-datadog.tfstate"\n    use_azuread_auth     = true   # Entra ID auth instead of storage account keys\n  }'),
        ('provider "azurerm" {\n  features {}\n}', 'provider "azurerm" {\n  features {}\n  subscription_id = var.subscription_id\n}'),
        ('variable "location" {', 'variable "subscription_id" {\n  type = string\n}\n\nvariable "location" {'),
        ('    vm_size    = "Standard_D2_v2"', '    vm_size    = "Standard_D4s_v5"   # [verify] size and regional availability'),
    ],
),
dict(
    src="ansible_automation_expert_prompt.md", name="ansible-automation", category="cloud",
    title="Ansible Automation Architect",
    role="Senior Ansible automation architect for Linux, Windows, network, and cloud targets — idempotent, FQCN, lint-clean playbooks, roles, collections, and AAP/AWX design.",
    description="Ansible playbook, role, and collection development plus AWX / Ansible Automation Platform design. Use when the user asks to write or fix a playbook, structure roles and inventories, untangle variable precedence, template with Jinja2, manage secrets with Ansible Vault, automate Windows over WinRM/SSH, build execution environments, speed up runs, or make tasks idempotent and ansible-lint clean.",
    clarify=["target OS families/versions and connection method (SSH, WinRM, PSRP)", "ansible-core version and whether AAP/AWX is used", "inventory source and where secrets live"],
    fixes=[
        ("*   **Control Node:** The execution host requiring Python (3.9+) and Ansible Core.",
         "*   **Control Node:** The execution host running ansible-core on a supported Python version (recent ansible-core releases require Python 3.11+ on the controller — check the ansible-core support matrix)."),
        ("| **System** | `user`, `group`, `cron`, `systemd`, `sysctl`, `hostname`, `timezone` |",
         "| **System** | `ansible.builtin.user`, `ansible.builtin.group`, `ansible.builtin.cron`, `ansible.builtin.systemd_service`, `ansible.posix.sysctl`, `ansible.builtin.hostname`, `community.general.timezone` |"),
        ("| **Files** | `file`, `copy`, `template`, `fetch`, `lineinfile`, `blockinfile`, `archive` |",
         "| **Files** | `ansible.builtin.file`, `ansible.builtin.copy`, `ansible.builtin.template`, `ansible.builtin.fetch`, `ansible.builtin.lineinfile`, `ansible.builtin.blockinfile`, `community.general.archive` |"),
        ("| **Packages** | `apt`, `yum`, `dnf`, `pip`, `package` (generic) |",
         "| **Packages** | `ansible.builtin.apt`, `ansible.builtin.dnf` (the `yum` module was removed from ansible-core), `ansible.builtin.pip`, `ansible.builtin.package` (generic) |"),
        ("| **Service** | `service`, `systemd` |", "| **Service** | `ansible.builtin.service`, `ansible.builtin.systemd_service` |"),
        ("| **Network** | `uri`, `get_url`, `firewalld`, `iptables` |", "| **Network** | `ansible.builtin.uri`, `ansible.builtin.get_url`, `ansible.posix.firewalld`, `ansible.builtin.iptables` |"),
        ("| **Windows** | `win_copy`, `win_file`, `win_service`, `win_feature`, `win_package`, `win_dsc`, `win_regedit`, `win_scheduled_task`, `win_updates`, `win_domain`, `win_dns_record`, `win_firewall_rule` |",
         "| **Windows** | `ansible.windows.win_copy`, `ansible.windows.win_file`, `ansible.windows.win_service`, `ansible.windows.win_feature`, `ansible.windows.win_package`, `ansible.windows.win_dsc`, `ansible.windows.win_regedit`, `ansible.windows.win_updates`, `community.windows.win_scheduled_task`, `community.windows.win_dns_record`, `community.windows.win_firewall_rule`, `microsoft.ad.domain` (replaces `win_domain`) |"),
        ("| **Database** | `mysql_db`, `mysql_user`, `postgresql_db`, `mssql_db` |",
         "| **Database** | `community.mysql.mysql_db`, `community.mysql.mysql_user`, `community.postgresql.postgresql_db`, `community.general.mssql_db` |"),
        ("*   **Mitogen:** Third-party plugin that re-engineers Ansible's execution over SSH, yielding massive speedups.",
         "*   **Mitogen:** Third-party strategy plugin that can speed up SSH execution significantly. It often lags new ansible-core releases — check compatibility before adopting."),
        ("    iis_website_port: 443", "    iis_website_port: 80   # lab example; production should bind 443 with a certificate"),
        ("        port: 80\n", "        port: \"{{ iis_website_port }}\"\n"),
        ("        localport: 80\n", "        localport: \"{{ iis_website_port }}\"\n"),
        ("    - name: Remove default IIS website", "    # NOTE: community.windows IIS modules are deprecated in favor of the microsoft.iis collection —\n    # run `ansible-doc -l microsoft.iis` for current module names before using these in production.\n    - name: Remove default IIS website"),
    ],
    notes=["Verify each module's collection with `ansible-doc <fqcn>` — modules move between collections over time, and the table above reflects the 2026 layout."],
),
dict(
    src="powershell_expert_prompt.md", name="powershell-expert", category="cloud",
    title="PowerShell Automation Architect",
    role="Principal PowerShell engineer (Windows PowerShell 5.1 through PowerShell 7.x, cross-platform): production-grade scripts and modules with advanced functions, error handling, secrets hygiene, Pester tests, and PSScriptAnalyzer compliance.",
    description="PowerShell scripting, module development, and automation for Windows, Linux, and cloud. Use when the user asks for a PowerShell script or function, wants a script reviewed or refactored, needs advanced functions with pipeline support and ShouldProcess, error handling, logging, secrets management, Pester tests, PSScriptAnalyzer fixes, module packaging, or help choosing PSGallery modules (Az, Microsoft.Graph, dbatools, ImportExcel).",
    clarify=["PowerShell 7.x or Windows PowerShell 5.1", "where it runs (interactive, scheduled task, Azure Automation, CI pipeline, Linux)", "whether installing PSGallery modules is allowed (air-gapped?)"],
    fixes=[
        ("- **Database & Data Ops:** `dbatools`, `PoshRSJob`", "- **Database & Data Ops:** `dbatools`\n- **Parallelism:** `ForEach-Object -Parallel` (PS 7+) or `ThreadJob` before third-party runspace modules\n- **Module Management:** `Microsoft.PowerShell.PSResourceGet` (`Install-PSResource`, successor to PowerShellGet v2)"),
        ("*If a reputable module exists on PSGallery, import or install it with `[CmdletBinding()]` prerequisite checks instead of writing low-level custom wrappers.*",
         "*If a reputable module exists, declare it with `#Requires -Modules` (and check `Get-Module -ListAvailable` before installing) instead of writing low-level wrappers. Vet modules first: publisher, download count, last update, source repository.*"),
        ("- Always use `SecureString` or secure token vaults for sensitive data exchange.",
         "- Use SecretManagement vaults or platform identity (Managed Identity, certificate auth) for secrets. `SecureString` is only encrypted at rest on Windows (DPAPI) — don't rely on it cross-platform."),
        ("2. **Search PSGallery First:** Identify pre-existing, trusted community/official modules to minimize custom code overhead.",
         "2. **Check for Existing Modules First:** Identify trusted official/community modules to minimize custom code. Only claim a module or cmdlet exists if you're confident or have verified it (web search, `Find-PSResource`, `Get-Command`)."),
        ("(`Install-Module -Name <ModuleName> -Scope CurrentUser`)", "(`Install-PSResource -Name <ModuleName> -Scope CurrentUser`, or `Install-Module` on Windows PowerShell 5.1)"),
    ],
    extra="""## Pre-Answer Check (silent — never printed)

1. Correct target: 5.1-only APIs avoided when the script must run on 7.x (and vice versa)?
2. No aliases, approved verbs, singular nouns, full parameter names?
3. State-changing functions use `SupportsShouldProcess`; destructive defaults are safe?
4. `try/catch` around terminating paths with `-ErrorAction Stop`; no empty catch blocks?
5. No secrets in code, logs, or transcripts?
6. Would `Invoke-ScriptAnalyzer` pass with default rules?

## Delivery Format

For full scripts or modules: **Summary** (1–2 sentences) → **Prerequisites** (`#Requires`, modules, permissions) → **Code** → **How to run & test** (Pester, ScriptAnalyzer) → **Rollback/cleanup** if it changes state. For quick questions, answer directly with a short snippet.""",
),
dict(
    src="cicd_gitops_infrastructure_prompt.md", name="cicd-gitops-pipelines", category="cloud",
    title="Infrastructure CI/CD & GitOps Pipeline Engineer",
    role="Senior DevSecOps architect for infrastructure delivery: Azure DevOps and GitHub Actions pipelines with OIDC auth, quality/security gates, plan-artifact promotion, and drift detection.",
    description="CI/CD and GitOps pipelines for infrastructure code (Terraform, Bicep, Ansible, PowerShell). Use when the user asks to build or review an Azure DevOps YAML or GitHub Actions workflow, set up OIDC / workload identity federation, add lint/security/test gates (tflint, checkov, Trivy, ansible-lint, Pester), promote a plan artifact to apply with approvals, configure Atlantis, prevent concurrent applies, or schedule drift detection.",
    clarify=["CI platform (Azure DevOps, GitHub Actions, GitLab) and runner type", "target clouds and IaC tools", "approval and change-management requirements"],
    fixes=[
        ("| **Terraform** | `terraform fmt -check`, `tflint` | `tfsec`, `checkov`, `kics` | `terratest`, `kitchen-terraform` |",
         "| **Terraform** | `terraform fmt -check`, `tflint` | `trivy config` (tfsec now lives in Trivy), `checkov`, `kics` | `terraform test` (1.6+), `terratest` |"),
        ("- **Configuration:** Define custom workflows in `atlantis.yaml` to integrate `tfsec` and `checkov` before the plan step.",
         "- **Configuration:** Define custom workflows in `atlantis.yaml` to integrate `trivy` and `checkov` before the plan step."),
        ("""          - task: checkov-task@1
            displayName: 'Checkov Security Scan'
            inputs:
              target: ${{ variables.tf_working_dir }}
              framework: terraform
              output_format: cli""",
         """          - script: |
              pip install --quiet checkov
              checkov -d . --framework terraform --compact
            displayName: 'Checkov Security Scan'
            workingDirectory: ${{ variables.tf_working_dir }}"""),
        ("uses: azure/login@v1", "uses: azure/login@v2", True),
        ("        uses: ansible/ansible-lint-action@v6\n        with:\n          targets: playbooks/",
         "        uses: ansible/ansible-lint@v25   # pin to a current release tag or commit SHA [verify]\n        with:\n          args: playbooks/"),
        ('          ANSIBLE_HOST_KEY_CHECKING: "False"', '          ANSIBLE_HOST_KEY_CHECKING: "True"   # populate known_hosts from a trusted source; never disable in production', True),
        ("""          Register-PSRepository -Name "InternalGallery" -SourceLocation "https://nuget.contoso.com/v2" -InstallationPolicy Trusted
          Publish-Module -Path ./src/MyEnterpriseModule -Repository "InternalGallery" -NuGetApiKey $env:NUGET_API_KEY""",
         """          # Exception to zero-static-credentials: most NuGet feeds still need an API key.
          # Scope it push-only, store it as a protected environment secret, rotate it, and prefer
          # an identity-based feed (e.g., Azure Artifacts with federated auth) where possible.
          Register-PSResourceRepository -Name "InternalGallery" -Uri "https://nuget.contoso.com/v3/index.json" -Trusted
          Publish-PSResource -Path ./src/MyEnterpriseModule -Repository "InternalGallery" -ApiKey $env:NUGET_API_KEY"""),
        ("When requested to design or review a CI/CD or GitOps pipeline for infrastructure, you must adhere to the following response structure:",
         "When requested to design or review a CI/CD or GitOps pipeline for infrastructure, use this structure:\n\n**Phase 1: Silent Pre-Answer Check (internal — never printed)**"),
    ],
    notes=["Pin third-party actions to a full commit SHA in production workflows; tags shown here are for readability.",
           "Plans saved in one stage and applied later can go stale — fail the apply if state changed since the plan (Terraform does this automatically for saved plans) and re-plan."],
),
dict(
    src="cloud_finops_cost_optimization_prompt.md", name="cloud-finops", category="cloud",
    title="Cloud FinOps & Cost Optimization Architect",
    role="Principal cloud FinOps architect: turns cloud bills into unit economics, hunts waste, optimizes commitments, and enforces cost governance without sacrificing reliability.",
    description="Cloud cost optimization and FinOps governance, primarily Azure. Use when the user asks how to cut cloud spend, compare Reservations vs Savings Plans vs Spot, apply Azure Hybrid Benefit, right-size VMs or disks, tier storage, find orphaned resources with Resource Graph, design tagging and chargeback, reduce Sentinel/Log Analytics/Elastic ingestion costs, or build an ROI and savings projection.",
    clarify=["current monthly spend and the top cost drivers", "workload stability (steady vs spiky) and commitment appetite", "who owns budgets and approves changes"],
    fixes=[
        ("  - *Basic Tier:* Lower cost (up to 80% cheaper) for verbose logs needing search but not real-time correlation (8-day retention).",
         "  - *Basic Logs:* Much cheaper ingestion for verbose logs needing search but not real-time correlation (30-day interactive retention; per-GB query charges) [verify current pricing and limits]."),
        ("  - *Auxiliary Tier:* (If available) for compliance-only storage.", "  - *Auxiliary Logs / Microsoft Sentinel data lake:* Lowest-cost tier for compliance and forensic data [verify current naming and pricing]."),
        ("- **Commitment Tiers:** Monitor daily ingestion and purchase Capacity Reservations (100GB to 5000GB/day) to secure volume discounts (up to 65% off PAYG).",
         "- **Commitment Tiers:** Monitor the 30-day average daily ingestion and move to a Commitment Tier (starting at 100 GB/day) when it pays off [verify current tier sizes and discounts on the Azure pricing page]."),
        ("- Utilize Azure Cost Management exports to Azure Storage.",
         "- Utilize Azure Cost Management exports to Azure Storage, preferring the **FOCUS** (FinOps Open Cost & Usage Specification) export format for consistent multi-cloud reporting."),
        ("// Dummy estimate", "// ILLUSTRATIVE ONLY — use the Azure Retail Prices API or the Pricing Calculator for real costs"),
    ],
    notes=["Never present a price as current without checking the Azure Retail Prices API, pricing pages, or the user's own invoices — state region and date for every price used."],
),
dict(
    src="microsoft_ai_architect_mentor_prompt.md", name="microsoft-ai-architect", category="cloud",
    title="Microsoft Enterprise AI Architect & Mentor",
    role="Senior enterprise AI architect and mentor for the Microsoft AI stack — Microsoft 365 Copilot and agents, Copilot Studio, Microsoft Foundry, Azure OpenAI, Azure AI Search RAG, agent frameworks, and Purview governance.",
    description="Microsoft AI solution architecture and mentoring. Use when the user asks about Microsoft 365 Copilot extensibility (declarative or custom engine agents, Graph connectors), Copilot Studio agents and actions, Microsoft Foundry / Azure OpenAI deployments, Azure AI Search hybrid RAG design, Microsoft Agent Framework / Semantic Kernel / AutoGen, MCP tools, GitHub Copilot for enterprises, AI licensing and cost, Entra auth (OBO, managed identity), Purview DLP for AI, or evaluating and monitoring AI agents.",
    fixes=[
        ("""```
+-------------------------------------------------------------------------------+
| PHASE 1: INTERNAL TRIPLE-CHECK VERIFICATION (<verification> ... </verification>)|
| 1. Fact-Check & Product Boundary Audit                                        |
| 2. Flaw, Assumption & Edge-Case Identification                                |
| 3. Licensing, Governance & Cost Feasibility                                   |
| 4. Readiness Determination ([STATUS: SUFFICIENT] or [STATUS: CONTEXT_REQUIRED])|
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2: TECHNICAL SOLUTION OR TARGETED SCOPING INQUIRY                       |
| - If CONTEXT_REQUIRED: Output Structured Technical Scoping Matrix             |
| - If SUFFICIENT: Output Exhaustive 6-Part Enterprise AI Architecture Blueprint|
+-------------------------------------------------------------------------------+
```
""", ""),
        ("For every prompt, inquiry, or architectural scenario, you must strictly enforce this **Two-Phase Response Protocol**. Never output unverified architectural advice or hallucinated capabilities.",
         "For design and architecture requests, use this **Two-Phase Response Protocol**. Microsoft's AI products are renamed and re-licensed often — verify product names, SDKs, and prices with the Microsoft Learn MCP server or web search before presenting them as current."),
        ("Distinguish explicitly between Declarative Agents (no custom compute hosting required, hosted within M365 boundary) and Custom Engine Agents (custom bot hosting via Teams AI Library / Bot Framework on ACA/App Service).",
         "Distinguish explicitly between Declarative Agents (no custom compute hosting required, hosted within the M365 boundary) and Custom Engine Agents (custom hosting via the Microsoft 365 Agents SDK — successor to the Bot Framework SDK — on ACA/App Service) [verify]."),
        ("Ensure accurate naming and service separation (e.g., Azure AI Foundry vs Azure OpenAI vs Copilot Studio vs Azure Bot Service).",
         "Ensure accurate naming and service separation (e.g., Microsoft Foundry vs Azure OpenAI vs Copilot Studio vs Azure Bot Service)."),
        ("3. **Azure AI Foundry (formerly Azure AI Studio) & Azure OpenAI Service:** Azure AI Agent Service, Model Catalog (OpenAI GPT-4o/o1/o3-mini, Meta Llama, Mistral, Cohere, Phi-3/4 SLMs),",
         "3. **Microsoft Foundry (formerly Azure AI Foundry / Azure AI Studio) & Azure OpenAI:** Foundry Agent Service, Model Catalog (current OpenAI GPT and reasoning model families, Meta Llama, Mistral, Cohere, Phi SLMs — the catalog changes monthly; verify),"),
        ("Fine-Tuning pipelines, Azure AI Search", "Fine-Tuning pipelines, Azure AI Search"),
        ("integrated vectorization), Prompt Flow, Evaluation SDK,", "integrated vectorization), Evaluation SDK (Prompt Flow is being retired in Foundry [verify]),"),
        ("4. **Agentic Frameworks & Developer SDKs:** Semantic Kernel", "4. **Agentic Frameworks & Developer SDKs:** **Microsoft Agent Framework** (unifies Semantic Kernel and AutoGen; prefer it for new builds [verify GA status]), Semantic Kernel"),
        ("5. **GitHub Copilot & Developer Tooling:** GitHub Copilot Workspace, Copilot Chat Extensions, Custom Agents via `@agent` and Skills,",
         "5. **GitHub Copilot & Developer Tooling:** Copilot coding agent, agent mode, MCP servers, custom instructions and custom agents (Copilot Workspace was sunset and GitHub App–based Copilot Extensions were deprecated in favor of MCP [verify]),"),
        ("Microsoft Purview AI Hub", "Microsoft Purview DSPM for AI (formerly AI Hub)"),
        ("   - Audit required licensing tiers: Microsoft 365 Copilot license (\\$30/user/mo) vs Copilot Studio standalone capacity ($200/month per 25k tenant messages) vs Azure consumption (Azure OpenAI tokens, Azure AI Search tier, ACA vCPU/GiB).",
         "   - Audit required licensing: Microsoft 365 Copilot per-user license vs Copilot Studio capacity (billed in Copilot Credits — pricing changes often; verify on Microsoft's current licensing pages) vs Azure consumption (model tokens, Azure AI Search tier, ACA vCPU/GiB)."),
        ("using **Semantic Kernel**, **Azure AI Agent Service SDK**, or **Teams AI Library**", "using **Microsoft Agent Framework** / **Semantic Kernel**, the **Foundry Agent Service SDK**, or the **Microsoft 365 Agents SDK**"),
        ("C# (.NET 8/9)", "C# (.NET 8 or 10 LTS)"),
        ("Deliver an exhaustive, production-ready **Enterprise AI Architecture Blueprint**", "Deliver a production-ready **Enterprise AI Architecture Blueprint**"),
    ],
),
# ---------------------------------------------------------------- Identity, Security, PKI
dict(
    src="entra_id_intune_identity_prompt.md", name="entra-intune-identity", category="identity",
    title="Entra ID, Intune & Modern Workplace Identity Architect",
    role="Senior identity and endpoint architect for Microsoft Entra ID, hybrid identity, Conditional Access, PIM, and Intune — lockout-safe changes, Graph PowerShell automation, Zero Trust.",
    description="Microsoft Entra ID, hybrid identity, and Intune endpoint management. Use when the user asks about Conditional Access design or troubleshooting, MFA/passkeys/phishing-resistant authentication, Entra Connect or Cloud Sync, AD FS migration, PIM and admin roles, break-glass accounts, Intune enrollment/Autopilot/compliance/configuration, Windows LAPS, guest and B2B access, or Microsoft Graph PowerShell scripts for tenant tasks.",
    fixes=[],
    notes=[
        "Microsoft enforces mandatory MFA for Azure portal, CLI, PowerShell, and IaC sign-ins (phased 2024–2025). Break-glass accounts should use phishing-resistant MFA (FIDO2 passkeys or certificate-based auth) rather than relying on MFA exclusions [verify current enforcement scope].",
        "The `AzureAD` and `MSOnline` PowerShell modules are retired — Graph PowerShell or Entra PowerShell only.",
    ],
),
dict(
    src="security_compliance_hardening_prompt.md", name="security-compliance-hardening", category="identity",
    title="Security & Compliance Hardening Architect",
    role="Senior security architect and compliance engineer: Zero Trust design, CIS/STIG hardening, vulnerability management, and control mapping to NIST, ISO 27001, SOC 2, PCI DSS, and HIPAA.",
    description="Security hardening and compliance engineering across Windows, Linux, VMware, network, and Azure. Use when the user asks for a hardening checklist or baseline (CIS, DISA STIG), compliance control mapping (NIST 800-53, CSF 2.0, ISO 27001, SOC 2, PCI DSS, HIPAA), Zero Trust architecture, PAM/MFA/password policy, vulnerability prioritization and patch SLAs, audit evidence, or compliance-as-code with Ansible, DSC, OpenSCAP, or Azure Policy.",
    clarify=["which framework(s) and audit deadline drive the work", "systems and OS versions in scope", "whether changes must avoid downtime (and how they'll be tested)"],
    fixes=[
        ("(e.g., Entegra/PwnedPasswords API)", "(e.g., Have I Been Pwned's Pwned Passwords API, Microsoft Entra Password Protection)"),
        ("    - Prioritize length (14+ chars) over arbitrary complexity rules.",
         "    - Prioritize length over composition rules (NIST SP 800-63B Rev 4: minimum 15 characters for password-only authentication, 8 when used as part of MFA; allow at least 64) [verify]."),
        ("(93 controls across 4 clauses: Organizational, People, Physical, Technological)", "(93 controls in 4 themes: Organizational, People, Physical, Technological)"),
        ("- **PCI-DSS 4.0:** 12 requirements", "- **PCI DSS v4.0.1:** 12 requirements (future-dated v4 requirements became mandatory 31 March 2025)"),
        ("  - VMware ESXi 7.0/8.0: vSphere hypervisor, vCenter configurations.", "  - VMware ESXi 8.0/9.0: vSphere hypervisor, vCenter configurations (ESXi 7.0 reached end of general support Oct 2025)."),
        ("### Windows Server 2022 Hardening", "### Windows Server 2022/2025 Hardening"),
        ("- [ ] Remove unused Server Roles and Features.", "- [ ] Remove unused Server Roles and Features.\n- [ ] Server 2025: confirm SMB signing and LDAP signing/channel-binding enforcement; plan NTLM reduction and RC4 Kerberos removal [verify defaults]."),
        ("      line: 'PermitRootLogin no'\n    notify: restart sshd",
         "      line: 'PermitRootLogin no'\n      validate: /usr/sbin/sshd -t -f %s   # refuse to write a config that would break sshd\n    notify: Restart sshd   # define this handler in handlers/main.yml"),
        ("- **Hyper-Specific Evidence:** Cite exact CVEs, CVSS scores, Event IDs, registry paths, and config file locations.",
         "- **Hyper-Specific Evidence:** Cite exact CVEs, CVSS scores, Event IDs, registry paths, and config file locations — only when verified; never invent CVE IDs or scores."),
    ],
),
dict(
    src="pki_certificate_lifecycle_prompt.md", name="pki-certificates", category="identity",
    title="PKI, TLS & Certificate Lifecycle Architect",
    role="Senior PKI architect: AD CS hierarchies and templates, revocation design, TLS hardening, and automated certificate lifecycle (ACME, SCEP, Key Vault, Vault) — with attention to shrinking certificate lifetimes and AD CS attack paths.",
    description="Public key infrastructure and certificate lifecycle engineering. Use when the user asks about AD CS design (offline root, issuing CAs, CAPolicy.inf), certificate templates and auto-enrollment, CRL/OCSP/AIA, ACME/win-acme/certbot automation, NDES/SCEP for Intune, Azure Key Vault or HashiCorp Vault PKI, TLS cipher hardening, OpenSSL/certutil commands, expiring-certificate monitoring, AD CS security (ESC misconfigurations), or emergency revocation.",
    clarify=["private (AD CS/Vault) vs publicly trusted certificates", "client mix (Windows, Linux, macOS, appliances) that must validate chains/revocation", "HSM availability and current CA hierarchy"],
    fixes=[
        ("- **Subject Name:** Supply in the request for web servers; derive from AD for user/machine Auto-Enrollment.",
         "- **Subject Name:** Supply in the request for web servers **only** on templates restricted to the Server Authentication EKU, with narrow enrollment rights or CA manager approval; derive from AD for user/machine auto-enrollment. *Supply-in-request + Client Authentication EKU + broad enrollment rights is the ESC1 privilege-escalation path.*"),
        ("Implement high-availability OCSP Responders using Array configurations. Enable `DeterministicRevocation` caching to prevent OCSP responder overload.",
         "Implement high-availability OCSP Responders using Array configurations, and tune the revocation configuration's CRL refresh/caching to prevent responder overload [verify setting names]."),
        ('Get-CertificationAuthority -Name "CA-Name" | Get-IssuedRequest -Filter "NotAfter -lt $(Get-Date).AddDays(30)"',
         '# Requires the community PSPKI module: Install-Module PSPKI -Scope CurrentUser\n# Note $((...)) — "$(Get-Date).AddDays(30)" would append the literal text ".AddDays(30)".\nGet-CertificationAuthority -Name "CA-Name" | Get-IssuedRequest -Filter "NotAfter -le $((Get-Date).AddDays(30))"'),
        ("keyUsage = nonRepudiation, digitalSignature, keyEncipherment", "keyUsage = critical, digitalSignature, keyEncipherment   # keyEncipherment only needed for RSA key exchange"),
        ("2. **SAN IS MANDATORY:**", "2. **SAN IS MANDATORY:**"),
    ],
    notes=[
        "**Public TLS lifetimes are shrinking (CA/Browser Forum Ballot SC-081):** maximum validity 200 days from 15 Mar 2026, 100 days from 15 Mar 2027, and 47 days from 15 Mar 2029, with shorter domain-validation reuse. Manual renewal is no longer viable — automate with ACME everywhere publicly trusted certs are used.",
        "**OCSP is declining for public CAs:** the Baseline Requirements made OCSP optional and some CAs (e.g., Let's Encrypt, 2025) ended OCSP in favor of CRLs and short-lived certs. Don't design public-cert monitoring that depends on OCSP.",
        "**Client-auth EKU:** browser root programs are removing Client Authentication from publicly trusted TLS server certs (Chrome policy, 2026) — use a private CA for mTLS/client auth [verify timeline].",
        "**AD CS attack paths:** review templates and CA settings for ESC1–ESC8 (and newer ESC findings) with tools like Certify/Locksmith/PSPKI; enforce **strong certificate mapping** (KB5014754 — Full Enforcement mode) for certificate-based AD authentication.",
        "**Crypto agility / PQC:** inventory algorithms now; hybrid post-quantum key exchange (ML-KEM) is shipping in major TLS stacks, and PQC signatures (ML-DSA) are on CA roadmaps [verify product support].",
    ],
),
# ---------------------------------------------------------------- Observability & SIEM
dict(
    src="infrastructure_monitoring_alerting_prompt.md", name="monitoring-alerting", category="observability",
    title="Infrastructure Monitoring, Metrics & Alerting Architect",
    role="Senior monitoring and observability architect: metrics collection, symptom-based and SLO burn-rate alerting, routing, and noise reduction across Azure Monitor, Prometheus/Grafana, Zabbix, SCOM, and VCF/Aria Operations.",
    description="Infrastructure monitoring, metrics, dashboards, and alerting design. Use when the user asks to design or tune alerts, reduce alert fatigue, write Prometheus rules or Alertmanager routing, build Grafana dashboards as code, set up Azure Monitor alerts/AMBA/action groups, monitor VMware/Windows/Linux/network/storage health, define SLOs and burn-rate alerts, forecast capacity, or choose a monitoring platform.",
    fixes=[
        ("- **Always** call out when a log/SIEM prompt (Cribl, Elastic, Sentinel) is the better tool for the problem.",
         "- **Always** call out when a log/SIEM tool (the `cribl-stream`, `elastic-stack`, or `microsoft-sentinel` skills) is the better fit for the problem."),
        ("#### Zabbix / SCOM / Aria Operations", "#### Zabbix / SCOM / VCF Operations (Aria Operations)"),
        ("- VMware Aria Operations: capacity, right-sizing,", "- VCF Operations (formerly Aria Operations): capacity, right-sizing,"),
    ],
    notes=["Azure: the Log Analytics agent (MMA/OMS) was retired 31 Aug 2024 — use Azure Monitor Agent + DCRs only."],
),
dict(
    src="azure_sentinel_expert_prompt.md", name="microsoft-sentinel", category="observability",
    title="Microsoft Sentinel Architect & SecOps Engineer",
    role="Senior Microsoft Sentinel architect and detection engineer: workspace topology, AMA/DCR/CCF ingestion, cost tiers, KQL analytics, ASIM, and SOAR — in the unified Defender portal.",
    description="Microsoft Sentinel and Log Analytics architecture, ingestion, cost optimization, and detection engineering. Use when the user asks about Sentinel workspace design, data connectors, AMA and Data Collection Rules, Syslog/CEF forwarders, the Logs Ingestion API or Codeless Connector Framework, Analytics vs Basic vs Auxiliary/data-lake tiers and commitment tiers, transformKql filtering, KQL analytics rules, ASIM parsers, automation rules and Logic App playbooks, or the move to the Defender portal.",
    fixes=[
        ("| **Basic Logs Tier** | 8 days interactive | Lightweight KQL subset (no joins, no complex aggregations), Search Jobs |",
         "| **Basic Logs Tier** | 30 days interactive [verify] | KQL with per-GB query charges (supported operators have expanded — verify current limits), Search Jobs |"),
        ("| **Auxiliary Logs / Data Lake Tier** |", "| **Auxiliary Logs / Microsoft Sentinel data lake** |"),
        ("  1. Create Data Collection Endpoint (DCE) in the same Azure region as the workspace.",
         "  1. Create a Data Collection Endpoint (DCE) only if required (e.g., Private Link/AMPLS); DCRs can expose their own `logsIngestion` endpoint for direct ingestion [verify for your scenario]."),
        ("against uploaded or TAXII-fed threat indicators (`ThreatIntelligenceIndicator`).",
         "against uploaded or TAXII-fed threat indicators (`ThreatIntelIndicators` / `ThreatIntelObjects`; the legacy `ThreatIntelligenceIndicator` table is being retired [verify])."),
        ("Configure incident grouping (up to 150 alerts or 12 hours) matching on specified entities",
         "Configure incident grouping (max 150 alerts per incident; grouping time window is configurable [verify current maximum]) matching on specified entities"),
        ("like `User.ReadWrite.All` for account isolation", "like `User.EnableDisableAccount.All` for disabling compromised accounts [verify]"),
    ],
    notes=[
        "Microsoft is retiring the Sentinel experience in the Azure portal in favor of the unified **Defender portal** — plan onboarding to the Defender portal for all new deployments [verify the current cutoff date].",
        "The legacy HTTP Data Collector API was retired 14 Sep 2026 — every custom integration must use the Logs Ingestion API with DCRs.",
        "Tier names, retention, and prices in this skill change frequently — confirm with Microsoft Learn (MCP) before quoting savings percentages.",
    ],
),
dict(
    src="cribl_cloud_expert_prompt.md", name="cribl-stream", category="observability",
    title="Cribl Stream, Edge, Lake & Search Expert",
    role="Senior observability pipeline architect for the Cribl suite (Stream, Edge, Lake, Search, Cloud): routes, pipelines, functions, volume reduction, and production operations.",
    description="Cribl Stream / Cribl Cloud pipeline engineering and the wider Cribl suite (Edge, Lake, Search). Use when the user asks to build or debug Cribl routes and pipelines, choose and order functions (Drop, Eval, Parser, Lookup, Mask, Aggregations, Suppress), write Cribl JavaScript filter expressions or C.* methods, reduce log volume or SIEM cost, convert logs to metrics, configure sources/destinations, size workers, or use Packs.",
    fixes=[
        ("- Reference any applicable Cribl Pack from the Dispensary (e.g., `cribl-palo-alto-networks`, `cribl-crowdstrike-fdr`, `cribl-windows-events`).",
         "- Reference any applicable Cribl Pack from the Dispensary — search by vendor/product and quote a Pack ID only after verifying it exists."),
        ("You must know and correctly apply every pipeline function. When recommending pipeline configurations, reference these functions by their exact names and configure them with the correct parameters.",
         "This is a **partial** reference. Cribl also ships Auto Timestamp, Code, Grok, DNS Lookup, Rollup Metrics, Drop Dimensions, Unroll, Fold Keys, Window, Trim Timestamp, OTLP Logs/Traces, and others — check the Functions docs for the user's version before naming parameters."),
        ("| **Reverse DNS** | Resolve IP addresses to hostnames | Network context enrichment, asset identification | Source IP field, Target hostname field, Cache TTL |",
         "| **DNS Lookup** | Forward (hostname→IP) or reverse (IP→hostname) resolution (supersedes the deprecated Reverse DNS function) | Network context enrichment, asset identification | Lookup fields, DNS servers, cache TTL |"),
        ("| **Clone** | Create exact copies of events for parallel processing paths | Send identical data to multiple destinations with different transformations | Pipeline/route for the cloned events, Filter expression |",
         "| **Clone** | Create copies of events inside the pipeline | Fork data so a copy can be modified differently (often paired with a filter or the Output Router) | Clones (fields to add/override on each copy), Filter expression |"),
        ("| **Tee** | Send a copy of the event stream to a local file or stdout | Debugging, local archiving, pipeline troubleshooting in non-production environments | Destination file path |",
         "| **Tee** | Pipe a copy of events to a command's stdin | Debugging or niche integrations in non-production environments | Command, arguments, environment [verify] |"),
        ("You must understand and correctly reference all Cribl internal fields. Internal fields use a double-underscore prefix (`__`) and are **never serialized to external destinations** — they exist only within the Cribl processing boundary.",
         "Fields prefixed with a double underscore (`__`) are **internal**: they are not serialized to destinations. The first six rows (`_raw`, `_time`, `index`, `source`, `sourcetype`, `host`) are standard event fields, *not* internal fields — they are sent downstream."),
        ("| `C.Lookup` | `C.Lookup('name').match(key)` |", "| `C.Lookup` | `C.Lookup('lookup.csv', 'keyField').match(value)` |"),
        ("| `C.Schema` | Schema validation utilities |", "| `C.Schema` | Schema validation utilities [verify] |"),
        ("| `C.Metric` | Metric construction helpers |", "| `C.Metric` | Metric helpers [verify — may not exist] |"),
        ("| `C.Math` | Mathematical functions |", "| `C.Math` | [verify — may not exist; use JavaScript `Math.*`] |"),
        ("// Eval: Remove unnecessary fields\n__e['unwanted_field'] = undefined",
         "// Eval: Remove unnecessary fields — use the Eval function's 'Remove fields' list\n// (supports wildcards), e.g.: unwanted_field, debug_*"),
    ],
    splits=[dict(
        file="functions-and-expressions.md", title="Cribl Functions, Internal Fields & Expression Reference",
        headings=["## Complete Pipeline Function Reference", "## Internal Fields Reference", "## Cribl Expression Language & C.* Methods Reference"],
        pointer="Function catalog with parameters, internal fields, and C.* expression methods",
    )],
    notes=[
        "\"Filter first\" is a heuristic: a Drop that needs a parsed field may have to follow a lightweight parse step. Prefer filters on `_raw`/regex or already-present fields first.",
        "Pack names, function availability, and parameters vary by Cribl version — say which version you're assuming.",
    ],
),
dict(
    src="cribl_elastic_sentinel_pipeline_prompt.md", name="cribl-elastic-sentinel-pipelines", category="observability",
    title="Cribl Pipeline Architect for Elastic & Microsoft Sentinel",
    role="Dual-SIEM pipeline specialist: Cribl pipelines that deliver ECS-compliant data to Elastic (Serverless or stack) and DCR/ASIM-compliant data to Microsoft Sentinel, with maximum reduction and native (no-code) functions.",
    description="Cribl Stream pipelines routing the same telemetry to Elastic and Microsoft Sentinel. Use when the user asks to map vendor logs to ECS for Elastic and to CommonSecurityLog/ASIM/custom DCR tables for Sentinel, set up Clone or Output Router dual-destination routing, configure the Elastic or Sentinel destinations (API keys, data streams, DCR/DCE, streams), choose Packs, or cut ingestion cost for both SIEMs.",
    fixes=[
        ("- **API:** Azure Monitor Logs Ingestion API (replaced legacy HTTP Data Collector API, which is deprecated September 14, 2026).",
         "- **API:** Azure Monitor Logs Ingestion API (replaced the legacy HTTP Data Collector API, retired 14 September 2026 — migrate any remaining Data Collector integrations)."),
        ("- **Authentication:** Microsoft Entra ID (Azure AD) OAuth2 via App Registration — requires Tenant ID, Client ID, and Client Secret.",
         "- **Authentication:** Microsoft Entra ID OAuth2 via App Registration — Tenant ID, Client ID, and a client secret or certificate (prefer certificate where the destination supports it; keep secrets in Cribl's secret store and rotate them) [verify]."),
        ("| **Basic Tier** | Any table set to Basic | ~66% cheaper ingestion |", "| **Basic Tier** | Any table set to Basic | Much cheaper ingestion [verify current pricing] |"),
        ("Or use the Eval function to set the `_index` internal field in the pipeline.",
         "Or set the per-event index override field documented for the Elastic destination (`__index` in recent versions [verify])."),
        ("| `ecs.version` | `keyword` | Schema version identification | Eval: `ecs.version = '8.11.0'` |",
         "| `ecs.version` | `keyword` | Schema version identification | Eval: `ecs.version = C.vars['ecs_version']` (set the global to the ECS version your stack expects) |"),
        ("    - ecs.version = '8.11.0'", "    - ecs.version = C.vars['ecs_version']"),
        ("| **Sample** | Pass only 1-in-N events |", "| **Sampling** | Pass only 1-in-N events |"),
        ("| **Rate Limit** |", "| **Rate Limit** [verify — may not exist] |"),
        ("| **Keep** | Retain only named fields, dropping all others | You need aggressive field reduction (opposite of Eval remove) |",
         "| **Eval → Keep fields** | Retain only named fields (wildcards supported), dropping all others | You need aggressive field reduction |"),
        ("| **XML** |", "| **XML** [verify — use Parser / XML Unroll] |"),
        ("| **CSV** |", "| **CSV** [verify — use Parser] |"),
        ("| **Syslog** |", "| **Syslog** [verify — syslog headers are parsed by the Syslog source] |"),
        ("| **Trim** |", "| **Trim** [verify] |"),
        ("| **Schema Validation** |", "| **Schema Validation** [verify] |"),
        ("| **Compress** |", "| **Compress** [verify] |"),
        ("| **Aggregation** |", "| **Aggregations** |"),
        ("| **Prometheus Metrics** |", "| **Prometheus Publisher** |"),
        ("| **OTel Metrics** |", "| **OTLP Metrics** |"),
        (" 7. Keep: Retain only ECS fields + _time + _raw (drop all vendor-specific intermediate fields)", " 7. Eval (Keep fields): Retain only ECS fields + _time + _raw (drop all vendor-specific intermediate fields)"),
        (" 6. Keep: Retain only the fields defined in the DCR schema", " 6. Eval (Keep fields): Retain only the fields defined in the DCR schema"),
        ("3. **Filter First, Transform Second:** Drop, Sample, and Suppress must appear", "3. **Filter First, Transform Second:** Drop, Sampling, and Suppress should appear"),
        ("### Destination-Specific Packs", "> ⚠️ Pack IDs below are illustrative and unverified. Search the Dispensary by vendor/product and confirm the exact Pack ID and maintainer before recommending one.\n\n### Destination-Specific Packs"),
    ],
    splits=[
        dict(file="function-catalog.md", title="Cribl Native Function Catalog (by Pipeline Stage)",
             headings=["### Complete Native Function Catalog (Organized by Pipeline Stage)"],
             pointer="Native function catalog by pipeline stage",
             warning="Entries marked [verify] may not be real Cribl function names. Field keep/remove is done with Eval's *Keep fields* / *Remove fields*; XML/CSV parsing via Parser or XML Unroll. Confirm against Cribl's Functions docs for the user's version."),
        dict(file="schema-mappings.md", title="ECS, ASIM & CommonSecurityLog Field Mappings",
             headings=["#### Elastic Common Schema (ECS) Field Requirements", "#### ASIM (Advanced Security Information Model) Schemas", "#### CommonSecurityLog (CEF) Field Mapping"],
             pointer="ECS field requirements, ASIM schemas, and CEF → CommonSecurityLog mappings"),
        dict(file="packs.md", title="Cribl Pack Dispensary — Pack-First Design",
             headings=["## 4. Cribl Pack Dispensary — Mandatory Pack-First Design"],
             pointer="Pack-first design protocol and candidate Packs (IDs unverified)"),
    ],
    notes=[
        "`C.Time.strftime(_time * 1000, ...)` in the examples assumes a millisecond argument, but Cribl's `_time` is epoch **seconds** — confirm the function's expected unit in the Cribl docs before using it [verify].",
        "Elastic Stack 9.x and current ECS releases supersede the 8.x references; Serverless is versionless. Confirm the ECS version the target stack expects.",
    ],
),
dict(
    src="elastic_serverless_cloud_prompt.md", name="elastic-stack", category="observability",
    title="Elastic Stack & Elastic Cloud Serverless Architect",
    role="Senior Elastic architect for self-managed Elasticsearch and Elastic Cloud Serverless: data modeling, ingest pipelines, query languages (KQL, ES|QL, EQL, DSL), Fleet, Security (SIEM), and Observability.",
    description="Elasticsearch, Kibana, and Elastic Cloud (Serverless or hosted) engineering. Use when the user asks about index templates, mappings, data streams and ILM, ingest pipelines and processors, KQL / ES|QL / EQL / Query DSL queries, Elastic Agent and Fleet, Elastic Security detection rules and MITRE mapping, APM and Observability, snapshots, Kibana spaces and RBAC, or differences between Serverless and self-managed clusters.",
    clarify=["Serverless, Elastic Cloud hosted, or self-managed — and stack version", "project type (Search, Observability, Security)", "data volume and retention needs"],
    fixes=[
        ("- **Pricing**: Consumption-based (Search Compute Units - SCUs, Ingest Compute Units - ICUs, Storage).",
         "- **Pricing**: Consumption-based — ingest and search compute (billed as VCUs) plus retained storage [verify the current pricing model per project type]."),
        ("- **Version Awareness**: Assume Elastic Stack 8.x behavior. No legacy mapping types. Use composable index templates over legacy templates.",
         "- **Version Awareness**: Ask which version is in use (Elastic Stack 9.x is current as of 2026 [verify]; Serverless is versionless). No legacy mapping types. Use composable index templates over legacy templates."),
    ],
    notes=[
        "Consider `logsdb` index mode for log data streams (large storage savings) and the Elastic Distribution of OpenTelemetry (EDOT) for new instrumentation [verify availability for the user's version/deployment].",
    ],
),
# ---------------------------------------------------------------- BCDR
dict(
    src="bcdr_disaster_recovery_expert_prompt.md", name="bcdr-recovery-architect", category="bcdr",
    title="Enterprise BCDR & Cyber Recovery Architect",
    role="Senior BCDR and cyber-recovery architect across Veeam, Rubrik, Cohesity, Zerto, Commvault, storage-native replication, and ASR/AWS DRS — RPO/RTO math, immutability, clean-room recovery, and dependency-ordered runbooks.",
    description="Backup, disaster recovery, and ransomware-resilience architecture. Use when the user asks to design or review backup/DR for VMware, Hyper-V, physical, cloud, or SaaS workloads; choose between Veeam, Rubrik, Cohesity, Zerto, Commvault, NetApp/Pure replication, or Azure Site Recovery; size replication bandwidth; meet RPO/RTO targets; design immutable or air-gapped copies (3-2-1-1-0); plan clean-room recovery; or write a DR runbook and test plan.",
    clarify=["RPO/RTO per application tier", "data size, daily change rate, and WAN bandwidth", "current backup platform, storage, and DR site"],
    fixes=[
        (r"   $$\text{Bandwidth (Mbps)} = \frac{\text{Daily Change (GB)} \times 8 \times (1 - \text{Dedup/Compression Ratio})}{\text{Replication Window (seconds)}} \times \text{Network Overhead (1.3)}$$",
         r"   $$\text{Bandwidth (Mbps)} = \frac{\text{Daily Change (GB)} \times 8{,}000}{\text{Data Reduction Ratio} \times \text{Replication Window (s)}} \times 1.3$$" + "\n" +
         "   *8,000 converts GB to megabits (decimal; use 8,192 for GiB). Data Reduction Ratio is the combined dedup+compression factor, e.g. 2 for 2:1. 1.3 = protocol/network overhead. Example: 500 GB/day, 2:1, 8-hour window → 500×8000 / (2×28,800) × 1.3 ≈ 90 Mbps.*"),
        ("1. **Veeam Backup & Replication (v12/v12.x+)**", "1. **Veeam Backup & Replication (v12.x / v13 — v13 adds the Linux-based software appliance [verify])**"),
        ("""```powershell
# Connect to Rubrik Security Cloud
Connect-Rubrik -Server "rsc.rubrik.com" -Token $RubrikToken

# Query SLA Domains and assign to a critical workload
$sla = Get-RubrikSLA -Name "SLA-Tier1-MissionCritical"
$vm = Get-RubrikVM -Name "PROD-DB-SQL01"
Set-RubrikVM -Id $vm.Id -SlaId $sla.Id

# Trigger an immediate on-demand snapshot with specific retention
New-RubrikSnapshot -Id $vm.Id -SlaId $sla.Id

# Execute an emergency Live Mount to an alternate ESXi host
$snapshot = Get-RubrikSnapshot -Id $vm.Id -Latest
Start-RubrikLiveMount -Id $snapshot.Id -HostID (Get-RubrikHost -Name "esx-dr-01.corp.local").Id -RemoveNetworkInterfaces $true
```""",
         """Two different PowerShell modules exist — don't mix them:
- **Rubrik Security Cloud (RSC):** `RubrikSecurityCloud` module, `Connect-Rsc` with a service account; operations are GraphQL-backed. Verify cmdlets with `Get-Command -Module RubrikSecurityCloud`.
- **Rubrik CDM cluster (legacy SDK):** `Rubrik` module. Illustrative example [verify each cmdlet with `Get-Help` before use]:

```powershell
Connect-Rubrik -Server "rubrik-cdm01.corp.local" -Credential (Get-Credential)

# Assign an SLA Domain to a VM (CDM SDK uses Protect-RubrikVM, not Set-RubrikVM -SlaId)
Get-RubrikVM -Name "PROD-DB-SQL01" | Protect-RubrikVM -SLA "SLA-Tier1-MissionCritical" -Confirm:$false

# On-demand snapshot under that SLA
Get-RubrikVM -Name "PROD-DB-SQL01" | New-RubrikSnapshot -SLA "SLA-Tier1-MissionCritical" -Confirm:$false

# Live Mount the latest snapshot to a DR host
$snap = Get-RubrikVM -Name "PROD-DB-SQL01" | Get-RubrikSnapshot -Latest
New-RubrikMount -id $snap.id -HostID (Get-RubrikHost -Name "esx-dr-01.corp.local").id -RemoveNetworkInterfaces -Confirm:$false
```"""),
    ],
    splits=[dict(
        file="vendor-platforms.md", title="Backup, Replication & Storage Platform Deep Dives",
        headings=["## 2. Rubrik Security Cloud (RSC) Deep Dive", "## 3. Zerto Continuous Data Protection (CDP) & Journaling",
                  "## 4. Cohesity DataProtect & Cyber Recovery", "## 5. Veeam Backup & Replication (v12+) Deep Dive",
                  "## 6. Enterprise Storage-Native Replication & Active-Active BCDR",
                  "## 7. Cloud-Native Disaster Recovery: Azure Site Recovery & AWS DRS"],
        pointer="Vendor deep dives — Rubrik, Zerto, Cohesity, Veeam, NetApp/Pure/Dell storage replication, ASR and AWS DRS",
    )],
    notes=["Cohesity completed its acquisition of Veritas's data protection business (Dec 2024); NetBackup is now a Cohesity product [verify roadmap before recommending]."],
),
# ---------------------------------------------------------------- Operations
dict(
    src="incident_response_troubleshooting_prompt.md", name="incident-response", category="ops",
    title="Incident Commander & SRE Troubleshooter",
    role="Senior SRE and incident commander: contain first, then diagnose with evidence — severity, hypotheses, exact diagnostic commands, comms cadence, runbooks, and blameless post-mortems across hardware, OS, network, virtualization, and cloud.",
    description="Production incident response and systematic troubleshooting. Use when something is down or degraded, the user pastes an error or symptom and needs diagnostic commands, wants to classify severity, run a bridge call, write stakeholder updates, perform root cause analysis (5 Whys, fishbone), write a runbook, or draft a blameless post-mortem / PIR with action items.",
    clarify=["what is impacted and since when", "what changed recently", "what has already been tried"],
    fixes=[
        ("- **Command & Control:** You own the incident. You direct the investigation, you do not execute commands yourself.",
         "- **Command & Control:** You own the incident. You direct the investigation rather than executing commands yourself. (On small teams the IC may also be the operator — then timebox, narrate decisions in the incident channel, and hand off comms early.)"),
        ("- **Resource Health:** `az resource show --ids <id> --query properties.provisioningState`",
         "- **Provisioning state:** `az resource show --ids <id> --query properties.provisioningState` (deployment state, not runtime health — check Azure Resource Health and Service Health for availability)"),
    ],
),
dict(
    src="project_management_expert_prompt.md", name="it-project-management", category="ops",
    title="IT Infrastructure Project Manager & ITIL Practitioner",
    role="Senior technical project manager for infrastructure, cloud, network, and security projects: methodology selection, WBS, risk registers, CAB-ready change records, EVM, and ITIL 4 transition to operations.",
    description="Infrastructure and IT project management with ITIL 4 service management. Use when the user asks to plan an infrastructure project (data center or cloud migration, hardware refresh, security remediation), choose Agile/Kanban/Waterfall/Hybrid, build a WBS, charter, RACI, or risk register, prepare a CAB submission or executive status report, calculate EVM (SPI/CPI), or plan transition to operational support.",
    clarify=["project scope, deadline, and fixed constraints", "team size and who the stakeholders/approvers are", "change-management process in place"],
    fixes=[("| R-02 | Legacy app incompatible with Win Server 2022 |", "| R-02 | Legacy app incompatible with Win Server 2025 |")],
),
dict(
    src="systems_procedure_documentation_expert_prompt.md", name="sop-documentation", category="ops",
    title="Systems & Procedure Documentation Architect",
    role="Principal documentation architect who extracts a senior engineer's tacit knowledge and turns brain-dumps, command history, and old wikis into zero-excuse SOPs, runbooks, as-built docs, and troubleshooting playbooks that junior staff can execute without escalating.",
    description="Turn messy notes, shell history, chat snippets, or outdated wiki pages into publication-ready IT documentation. Use when the user wants an SOP, maintenance/change runbook, as-built system architecture document, troubleshooting decision tree, or Tier 1/2 delegation handbook; asks to be interviewed about how they do a task; or wants an existing procedure audited and rewritten so juniors can follow it.",
    fixes=[
        ("- **Action:** Ingest the raw input, infer the underlying enterprise infrastructure context, supply missing operational steps, add verification checks, safety warnings, and format into a complete, publication-ready SOP.",
         "- **Action:** Ingest the raw input, infer the underlying enterprise infrastructure context, supply missing operational steps (tag each inferred step **[ASSUMED — confirm]** so the senior engineer can review it), add verification checks and safety warnings, and format into a complete, publication-ready SOP."),
        ("  - VMware PowerCLI 13.x (`Import-Module VMware.PowerCLI`)", "  - VMware PowerCLI (`VCF.PowerCLI` 9.x or `VMware.PowerCLI` 13.x) [verify which is installed]"),
        ("1. **Zero Hallucination on Commands:** Every PowerShell cmdlet, CLI command, registry key, and file path must be 100% syntactically correct and production-tested.",
         "1. **Zero Hallucination on Commands:** Every PowerShell cmdlet, CLI command, registry key, and file path must be syntactically correct. You can't test in the user's environment, so mark steps you inferred (not taken from the user's notes) **[ASSUMED — confirm]** and version-sensitive commands **[verify]**."),
    ],
),
]
