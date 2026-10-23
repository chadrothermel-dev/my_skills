# My Skills Repository

A curated library of **52** Claude skills for enterprise systems engineering, identity, observability, security, communication, and personal productivity. Each skill is a converted and audited version of a prompt from [`my_prompts`](https://github.com/chadrothermel-dev/my_prompts) — see **[AUDIT.md](AUDIT.md)** for what was fixed and why.

---

## Quick Start

**Option A — Claude Code plugin (all skills, auto-updates):**

```bash
/plugin marketplace add chadrothermel-dev/my_skills
```

```bash
/plugin install my-skills@my-skills
```

Skills are then available as `/my-skills:<skill-name>` and load automatically when your request matches a skill's description.

**Option B — copy into your personal skills folder (Windows):**

```powershell
git clone https://github.com/chadrothermel-dev/my_skills.git; cd my_skills; ./install.ps1
```

Install a subset with `./install.ps1 -Skills vmware-vsphere,windows-server`. On macOS/Linux use `./install.sh` (optionally followed by skill names).

**Option C — claude.ai:** run `./install.ps1 -Zip` to build `dist/<skill>.zip` files, then upload one under **Settings → Capabilities → Skills**.

> [!TIP]
> **Combine skills for maximum impact.** Claude can load several skills in one conversation — see [Recommended Skill Combinations](#recommended-skill-combinations).

---

## 🏗️ Infrastructure & Platform Engineering

Core datacenter, virtualization, compute, networking, and operating system skills.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[VMware vSphere & VCF Virtualization Architect](skills/vmware-vsphere/SKILL.md)** | `/vmware-vsphere` | Senior Principal Virtualization Architect | ESXi/vCenter/VCF, HA/DRS/FT, vMotion, vSAN OSA/ESA, Distributed Switches, NSX, VCF Operations, HCX, PowerCLI |
| **[Windows Server Platform Architect](skills/windows-server/SKILL.md)** | `/windows-server` | Senior Principal Windows Platform Architect | AD DS/FSMO, GPO (LSDOU), DNS/DHCP, Failover Clustering, Hyper-V, IIS, Storage Spaces Direct, PKI, LAPS |
| **[Linux Systems Architect (RHEL & Ubuntu)](skills/linux-sysadmin/SKILL.md)** | `/linux-sysadmin` | Senior Principal Linux Systems Architect | systemd, dnf/apt, LVM, SELinux/AppArmor, SSH hardening, Bash scripting, performance tuning, Podman/Docker |
| **[Enterprise Network Architect](skills/enterprise-networking/SKILL.md)** | `/enterprise-networking` | Senior Principal Network Architect | VLANs/STP/LACP, OSPF/BGP routing, Palo Alto/Fortinet firewalls, IPSec/SSL VPN, F5, SD-WAN, 802.1X NAC |
| **[Data Center Hardware Architect](skills/datacenter-hardware/SKILL.md)** | `/datacenter-hardware` | Hardware Architect | Lenovo/HPE/Dell/Cisco server portfolios, storage arrays, CPU/RAM/NIC selection matrices, workload blueprints |
| **[Kubernetes & Container Platform Architect](skills/kubernetes-platform/SKILL.md)** | `/kubernetes-platform` | Senior Principal Kubernetes Architect (CKA/CKS) | Control plane HA, etcd/etcdutl, Cilium/Calico CNI, vSphere CSI, MetalLB, Gateway API, ArgoCD/Flux GitOps, Helm, Kyverno |
| **[Windows Workstation Performance & Cleanup Engineer](skills/windows-workstation-tuning/SKILL.md)** | `/windows-workstation-tuning` | Senior Windows Endpoint Engineer | Read-only assessment first, 4-tier findings report (startup / bloatware / review / junk), restore point + reversible changes, Docker/WSL/VM disk reclaim, never-remove list, Docker Desktop repair |

---

## ☁️ Cloud, IaC & Automation

Azure cloud services, infrastructure as code, configuration management, and scripting.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Azure Cloud Solutions Architect](skills/azure-solutions-architect/SKILL.md)** | `/azure-solutions-architect` | Senior Principal Azure Architect | Full Azure service catalog, Zero-Trust, Well-Architected Framework (WAF), Landing Zones (CAF), Bicep/Terraform |
| **[Terraform & OpenTofu IaC Architect](skills/terraform-iac/SKILL.md)** | `/terraform-iac` | Senior Principal IaC Architect | HCL, multi-provider (Azure/AWS/VMware), state & locking, modules, terraform test, ephemeral secrets, Terragrunt, Sentinel/OPA |
| **[Ansible Automation Architect](skills/ansible-automation/SKILL.md)** | `/ansible-automation` | Senior Principal Automation Architect | Playbooks, Roles/Collections, AWX/AAP, Jinja2, variable precedence, Vault, Windows/Linux modules, Molecule |
| **[PowerShell Automation Architect](skills/powershell-expert/SKILL.md)** | `/powershell-expert` | PowerShell Principal Engineer | Enterprise scripting, PSScriptAnalyzer, pipeline architecture, PSGallery module integration |
| **[Infrastructure CI/CD & GitOps Pipeline Engineer](skills/cicd-gitops-pipelines/SKILL.md)** | `/cicd-gitops-pipelines` | Senior Principal DevSecOps Architect | Azure DevOps YAML, GitHub Actions OIDC, quality gates (tflint/Trivy/checkov/Pester), plan-artifact promotion, Atlantis, drift detection |
| **[Cloud FinOps & Cost Optimization Architect](skills/cloud-finops/SKILL.md)** | `/cloud-finops` | Principal Cloud FinOps Architect | Reservations vs. Savings Plans, Azure Hybrid Benefit, storage tiering math, waste hunting scripts, tagging |
| **[Microsoft Enterprise AI Architect & Mentor](skills/microsoft-ai-architect/SKILL.md)** | `/microsoft-ai-architect` | Enterprise AI Architect | M365 Copilot agents, Copilot Studio, Microsoft Foundry, Agent Framework / Semantic Kernel, Azure AI Search RAG, MCP, Purview DSPM for AI |
| **[Personal Web Project Builder & Publisher](skills/web-project-publishing/SKILL.md)** | `/web-project-publishing` | Senior Full-Stack Engineer | Local HTTP/Docker run, hosting matrix (GitHub Pages, Cloudflare, Netlify, Azure SWA), large-media strategy, web-safe video, maps & 3D libraries, Pages Actions deploy, works-locally-broken-online fixes |

---

## 🔐 Identity, Security, Compliance & Cryptography

Identity and endpoint management, security hardening, regulatory compliance, PKI, and certificate lifecycle management.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Entra ID, Intune & Modern Workplace Identity Architect](skills/entra-intune-identity/SKILL.md)** | `/entra-intune-identity` | Senior Principal Identity & Endpoint Architect | Hybrid identity (Cloud Sync/Connect, PHS), Conditional Access baselines, passkeys/phishing-resistant MFA, PIM, Intune/Autopilot, Windows LAPS, Graph PowerShell, Microsoft365DSC |
| **[Security & Compliance Hardening Architect](skills/security-compliance-hardening/SKILL.md)** | `/security-compliance-hardening` | Senior Principal Security Architect | CIS/NIST/STIG/ISO 27001/SOC 2, Zero-Trust, IAM/PAM/PIM, vulnerability/patch management, hardening checklists |
| **[PKI, TLS & Certificate Lifecycle Architect](skills/pki-certificates/SKILL.md)** | `/pki-certificates` | Senior Principal PKI Architect | AD CS hierarchy & templates (ESC risks), CRL/OCSP, ACME/SCEP, 200→47-day public cert lifetimes, Key Vault/Vault PKI, OpenSSL, TLS hardening |

---

## 📊 Observability, Monitoring, SIEM & Log Engineering

Metrics and alerting, log pipelines, SIEM platforms, and observability architecture.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Infrastructure Monitoring, Metrics & Alerting Architect](skills/monitoring-alerting/SKILL.md)** | `/monitoring-alerting` | Senior Principal Monitoring Architect | USE/RED/Golden Signals, symptom-based alerting, SLO burn-rate alerts, Azure Monitor/AMBA, Prometheus/Grafana/Alertmanager, Zabbix, SCOM, VCF Operations |
| **[Microsoft Sentinel Architect & SecOps Engineer](skills/microsoft-sentinel/SKILL.md)** | `/microsoft-sentinel` | Senior Principal Microsoft Sentinel Architect | Workspace design, DCR/DCE, AMA, CCF, Logs Ingestion API, cost optimization (Analytics/Basic/Auxiliary/Archive), Commitment Tiers, ASIM, SOAR Logic Apps |
| **[Cribl Stream, Edge, Lake & Search Expert](skills/cribl-stream/SKILL.md)** | `/cribl-stream` | Senior Observability Pipeline Architect | All pipeline functions, Source/Destination catalog, C.* expressions, volume reduction, Pack-first design, Lake & Search |
| **[Cribl Pipeline Architect for Elastic & Microsoft Sentinel](skills/cribl-elastic-sentinel-pipelines/SKILL.md)** | `/cribl-elastic-sentinel-pipelines` | Dual-SIEM Pipeline Specialist | Pack-first design, ECS compliance, Sentinel DCR/DCE & ASIM mapping, Clone/Output Router, SIEM cost reduction |
| **[Elastic Stack & Elastic Cloud Serverless Architect](skills/elastic-stack/SKILL.md)** | `/elastic-stack` | Senior Security Analytics Architect | Elasticsearch, KQL/ES\|QL/EQL, ingest pipelines, Elastic Agent/Fleet, SIEM detection rules, MITRE ATT&CK, APM |

---

## 🛡️ Backup, Disaster Recovery & Business Continuity

Enterprise data protection, replication, cyber recovery, and DR orchestration.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Enterprise BCDR & Cyber Recovery Architect](skills/bcdr-recovery-architect/SKILL.md)** | `/bcdr-recovery-architect` | BCDR Architect | Rubrik (Atlas/Radar/Sonar), Zerto CDP journaling, Veeam v12+ (HLR/SOBR/CDP), Cohesity FortKnox, NetApp MetroCluster, Pure ActiveCluster, ASR, 3-2-1-1-0, Clean Room |

---

## 📋 Operations, Communication & Documentation

Incident management, project delivery, stakeholder communication, procedure documentation, and knowledge transfer.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Incident Commander & SRE Troubleshooter](skills/incident-response/SKILL.md)** | `/incident-response` | Senior Principal SRE & Incident Commander | P1-P4 severity, 5 Whys/Ishikawa RCA, runbook templates, blameless post-mortems, SLI/SLO/SLA, diagnostics |
| **[IT Infrastructure Project Manager & ITIL Practitioner](skills/it-project-management/SKILL.md)** | `/it-project-management` | Senior IT Project Management Architect | Agile/Scrum/Kanban, ITIL 4, Change/Incident/Problem management, RACI, risk registers, EVM, Azure DevOps Boards |
| **[Systems & Procedure Documentation Architect](skills/sop-documentation/SKILL.md)** | `/sop-documentation` | Principal Documentation Architect | Zero-Excuse SOPs, tacit knowledge extraction (shorthand expansion, interview, legacy refactor), runbooks, SAD, tribal gotchas, escalation gates |
| **[Enterprise Technical Trainer & Instructional Designer](skills/enterprise-trainer/SKILL.md)** | `/enterprise-trainer` | Principal Enterprise Technical Trainer & Instructional Designer | Ready-to-teach timed lesson plans, verified subject mastery map, ABCD objectives & Bloom's, hands-on sandbox labs, VILT/ILT timing, assessments & rubrics, Kirkpatrick L1–L4, rollout & train-the-trainer |
| **[Technical Communication & Executive Translator](skills/executive-communication/SKILL.md)** | `/executive-communication` | Principal Technical Communications Strategist | BLUF writing, audience translation matrix, exec status updates, outage notifications, CAB summaries, business cases, vendor escalations |

---

## ⚡ Daily Productivity & Workflow

Short, repeatable skills for every workday: start and end the day, clear the inbox, process meetings, make decisions, and digest reading.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Daily Kickoff & Shutdown Ritual Coach](skills/daily-kickoff-shutdown/SKILL.md)** | `/daily-kickoff-shutdown` | Daily Operations Coach (ADHD-aware) | 5-min morning kickoff (one win, real focus time, < 2-min first step), midday re-anchor, end-of-day shutdown, work log & brag capture, standup generation, Floor Day mode |
| **[Inbox & Message Triage Assistant](skills/inbox-triage/SKILL.md)** | `/inbox-triage` | Executive Assistant & Comms Triage Specialist | 6-bucket triage, consequence ranking, hidden-ask & deadline detection, phishing red flags, BLUF reply drafts, "no" templates |
| **[Meeting Notes, Decisions & Action Item Extractor](skills/meeting-notes/SKILL.md)** | `/meeting-notes` | Program Coordinator & Meeting Scribe | Decision vs. discussion separation, owner/due-date enforcement, "your actions" list, CAB/incident/design/vendor/1:1 add-ons, follow-up email draft |
| **[Everyday Decision Coach & Decision-Fatigue Breaker](skills/decision-coach/SKILL.md)** | `/decision-coach` | Decision Strategist (ADHD-aware) | Two-way vs. one-way door sizing, default rules, satisficing, weighted matrix, pre-mortem, research-loop breaker, always-recommend output |
| **[Rapid Research & Briefing Analyst](skills/research-briefing/SKILL.md)** | `/research-briefing` | Senior Research Analyst | 2-minute layered briefings, "does this affect me?" impact checks, source credibility ladder, fact/claim/inference labeling, compare & explain modes |

---

## 🏠 Personal, Career & Lifestyle

Non-technical skills for personal productivity, career growth, finance, and daily life.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Adult ADHD Executive Function Coach & Behavioral Analyst](skills/adhd-executive-function-coach/SKILL.md)** | `/adhd-executive-function-coach` | ADHD Life Strategist & Executive Function Coach (not a clinician) | Behavioral decoding (ABC model), 10 ADHD behavioral archetypes (Waiting Mode, Restraint Collapse, Urgency Addiction), 7 executive functions, task initiation, time blindness, working memory, RSD, workplace strategies for IT pros, parenting, habit formation |
| **[Weekly Reset & Life Operating System Coach](skills/weekly-reset-planner/SKILL.md)** | `/weekly-reset-planner` | Personal Operations Coach (GTD + ADHD scaffolding) | 20–30 min weekly reset, brain dump → sort buckets, Big 3 priorities, time-blindness padding, daily/monthly check-ins |
| **[Health, Fitness & Sustainable Habit Coach](skills/fitness-habit-coach/SKILL.md)** | `/fitness-habit-coach` | Personal Trainer & Habit Coach (non-medical) | Minimum-effective-dose strength plans, "Floor" plans for bad weeks, sleep & energy, desk-worker correctives, habit stacking |
| **[Home Maintenance & Household Operations Manager](skills/home-maintenance-ops/SKILL.md)** | `/home-maintenance-ops` | Household Ops Manager ("Home as Infrastructure") | Home asset inventory, seasonal PM schedules, DIY vs. pro decisions, contractor vetting, chore matrix, capital replacement forecast |
| **[Family Travel & Trip Logistics Planner](skills/family-trip-planner/SKILL.md)** | `/family-trip-planner` | Travel Logistics Planner | Day trips to week-long vacations, pacing rules, teen buy-in, booking priority, weather backups, packing & prep timelines, Game Day mode |
| **[Genealogy & Local History Research Assistant](skills/genealogy-research/SKILL.md)** | `/genealogy-research` | Professional Genealogist & Local Historian | Genealogical Proof Standard, PA/Mid-Atlantic record map, PA German church records, brick-wall strategies, archive naming & metadata |
| **[Learning Strategist & Skill Acquisition Coach](skills/learning-coach/SKILL.md)** | `/learning-coach` | Learning Scientist & Skill Coach | Project-first learning plans, retrieval & spaced repetition, Anki flashcards, teach & quiz modes, ADHD-friendly 20–30 min sessions |
| **[Career Interest Discovery & Occupational Fit Assessment](skills/career-interest-assessment/SKILL.md)** | `/career-interest-assessment` | Career Assessment Specialist & Vocational Counselor | Step-by-step RIASEC (Holland Code) interest inventory, O\*NET work values, strengths & peak experiences, work style, constraints, ranked occupation matches, 30-day exploration plan; works for teens through career changers |
| **[Infrastructure Career Strategist & Interview Coach](skills/career-interview-coach/SKILL.md)** | `/career-interview-coach` | Career Strategist & Former Infrastructure Hiring Manager | Brag document/XYZ bullets, resume & LinkedIn tailoring, STAR-L story bank, mock interviews, cert roadmap, negotiation scripts, ADHD-aware job search |
| **[Formal Logic Engine & Argument Analyzer](skills/formal-logic-analyzer/SKILL.md)** | `/formal-logic-analyzer` | Analytical Philosophy Evaluator | Syllogistic mapping, enthymeme extraction, fallacy & bias matrix, countermodels, epistemic crux analysis |
| **[Investing Mentor & Market Strategist for Beginners](skills/investing-mentor/SKILL.md)** | `/investing-mentor` | Veteran Investing Mentor & Educator (not a licensed adviser) | One-question-at-a-time beginner intake, investing order of operations, index funds & allocation templates, stock deep-dive method, high-risk & scam warnings, fiduciary referrals |
| **[End-of-Life Planning & Legacy Organizer](skills/end-of-life-planning/SKILL.md)** | `/end-of-life-planning` | Compassionate Planning Guide (estate paralegal + hospice social worker + organizer; not an attorney) | Gentle module-by-module interview, will/trust/POA/advance directive, beneficiary checks, asset & digital-life inventory (no secrets in chat), final wishes, prioritized to-do plan, Letter of Instruction |
| **[Video & Media Production Engineer](skills/video-media-production/SKILL.md)** | `/video-media-production` | Senior Post-Production Engineer & Media Archivist | Archival/stock footage sourcing with rights notes, 4:3-to-16:9 options, FFmpeg trim/join/encode recipes, PowerPoint & VLC kiosk loops, soundtrack rights, YouTube & web publishing |
| **[Tire Evaluation & Best-Value Buying Research Analyst](skills/tire-research/SKILL.md)** | `/tire-research` | Veteran Tire Specialist & Consumer Research Analyst | Vehicle & fitment intake (size, load, speed), sidewall & wear-pattern diagnosis, tire categories incl. 3PMSF/EV, out-the-door cost per 10k miles, deep research loop with stop rule, mandatory double-check pass |
| **[Culinary Logistics & Meal Planner](skills/meal-planner/SKILL.md)** | `/meal-planner` | Meal Planning Agent | 7-day budget meal plans, editable household profile, teen portion scaling, leftovers & prep plan, store-section grocery list |
| **[Personal Finance Planner](skills/personal-finance/SKILL.md)** | `/personal-finance` | Personal Finance Agent | Budget dashboard, debt avalanche/snowball with real payoff math, emergency fund, goal tracking (educational, not investment advice) |
| **[Everyday Computer Help Desk Technician](skills/everyday-computer-help-desk/SKILL.md)** | `/everyday-computer-help-desk` | Patient Help Desk Technician for non-technical users | One-action-per-step fix guides, plain-language clarifying questions, "what you should see" checks, OS identification, Wi-Fi/printer/email/password/slow PC fixes, scam pop-up safety, when to call a pro |

---

## 🧰 Meta & Prompt Engineering

Skills for building and maintaining this library.

| Skill | Invoke | Persona | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **[Prompt Engineering Architect & Skill Builder](skills/prompt-engineering-architect/SKILL.md)** | `/prompt-engineering-architect` | Principal Prompt Engineer | Build/audit/refactor/combine prompts and skills, SKILL.md packaging, description triggers, audit rubric, test inputs |

---

## Recommended Skill Combinations

For maximum effectiveness, combine related skills based on your current task:

| Task | Primary Skill | Supporting Skill(s) |
| :--- | :--- | :--- |
| Cloud infrastructure deployment | `/azure-solutions-architect` | `/terraform-iac`, `/security-compliance-hardening` |
| On-prem VM environment management | `/vmware-vsphere` | `/windows-server`, `/powershell-expert` |
| Log pipeline engineering | `/cribl-stream` | `/elastic-stack` |
| Dual-SIEM log routing & optimization | `/cribl-elastic-sentinel-pipelines` | `/elastic-stack`, `/microsoft-sentinel` |
| Infrastructure automation | `/ansible-automation` | `/linux-sysadmin`, `/windows-server`, `/terraform-iac` |
| Security audit & compliance hardening | `/security-compliance-hardening` | `/windows-server`, `/linux-sysadmin`, `/enterprise-networking` |
| Enterprise PKI & certificate management | `/pki-certificates` | `/windows-server`, `/linux-sysadmin`, `/enterprise-networking` |
| Production incident response | `/incident-response` | any technology skill, `/executive-communication` |
| Infrastructure project planning | `/it-project-management` | any technology skill |
| Hardware procurement & DC design | `/datacenter-hardware` | `/vmware-vsphere`, `/windows-server`, `/enterprise-networking` |
| Disaster recovery & backup architecture | `/bcdr-recovery-architect` | `/vmware-vsphere`, `/windows-server`, `/azure-solutions-architect` |
| Container platform & Kubernetes ops | `/kubernetes-platform` | `/linux-sysadmin`, `/ansible-automation`, `/enterprise-networking` |
| Cloud cost reduction & FinOps governance | `/cloud-finops` | `/azure-solutions-architect`, `/terraform-iac` |
| Infrastructure CI/CD & GitOps delivery | `/cicd-gitops-pipelines` | `/terraform-iac`, `/ansible-automation`, `/powershell-expert` |
| Cloud SIEM, detection & SecOps engineering | `/microsoft-sentinel` | `/azure-solutions-architect`, `/cribl-stream`, `/security-compliance-hardening` |
| Operational delegation & SOP generation | `/sop-documentation` | any technology skill for context |
| Entra ID / Conditional Access / Intune rollout | `/entra-intune-identity` | `/security-compliance-hardening`, `/powershell-expert`, `/windows-server` |
| Monitoring & alert-noise cleanup | `/monitoring-alerting` | `/incident-response`, `/vmware-vsphere`, `/azure-solutions-architect` |
| Outage comms, CAB submissions & exec updates | `/executive-communication` | `/incident-response`, `/it-project-management` |
| Training a team, workshop or onboarding course | `/enterprise-trainer` | the matching technical skill for subject depth, `/sop-documentation`, `/learning-coach` |
| Archival video loop or event slideshow | `/video-media-production` | `/web-project-publishing`, `/windows-workstation-tuning` |
| Publishing a map, 3D model or video site | `/web-project-publishing` | `/video-media-production`, `/cicd-gitops-pipelines` |
| Slow PC or full disk on a dev workstation | `/windows-workstation-tuning` | `/powershell-expert`, `/kubernetes-platform` |
| Figuring out what career fits (teen or adult) | `/career-interest-assessment` | `/learning-coach`, `/career-interview-coach` |
| Promotion, resume & interview prep | `/career-interview-coach` | `/executive-communication`, `/adhd-executive-function-coach` |
| Starting and ending the workday | `/daily-kickoff-shutdown` | `/weekly-reset-planner`, `/adhd-executive-function-coach` |
| Clearing a backed-up inbox or Teams | `/inbox-triage` | `/executive-communication` |
| Turning meetings into tracked work | `/meeting-notes` | `/it-project-management`, `/daily-kickoff-shutdown` |
| Stuck on a choice (work or home) | `/decision-coach` | `/personal-finance`, `/home-maintenance-ops`, `/formal-logic-analyzer` |
| Release notes, advisories & long docs | `/research-briefing` | `/security-compliance-hardening`, the matching technical skill |
| Weekly planning that actually sticks | `/weekly-reset-planner` | `/adhd-executive-function-coach` |
| Healthy routines for the whole family | `/fitness-habit-coach` | `/meal-planner`, `/weekly-reset-planner` |
| Starting to invest (complete beginner) | `/investing-mentor` | `/personal-finance`, `/decision-coach` |
| Getting affairs in order for loved ones | `/end-of-life-planning` | `/personal-finance`, `/investing-mentor`, `/sop-documentation` |
| Buying tires (best quality for the price) | `/tire-research` | `/decision-coach`, `/research-briefing` |
| Home repairs, projects & big-expense planning | `/home-maintenance-ops` | `/personal-finance` |
| Family vacations & day trips | `/family-trip-planner` | `/personal-finance` |
| Family tree & local history archive | `/genealogy-research` | sop-documentation (archive SOPs) |
| Learning a new technology or hobby | `/learning-coach` | the matching technical skill, e.g. kubernetes-platform |
| Adding or improving a skill in this repo | `/prompt-engineering-architect` | the skill being created or audited |

---

## Using These Skills with Claude

| Platform | How |
| :--- | :--- |
| **Claude Code (plugin)** | `/plugin marketplace add chadrothermel-dev/my_skills` → `/plugin install my-skills@my-skills`. Invoke as `/my-skills:<name>` or just describe your task. |
| **Claude Code (personal)** | `./install.ps1` copies skills to `~/.claude/skills/<name>/`. Invoke as `/<name>`. |
| **claude.ai / Desktop** | `./install.ps1 -Zip`, then upload a zip under *Settings → Capabilities → Skills*. |
| **API / agents** | Upload via the Skills API, or use a `SKILL.md` body (minus frontmatter) as the system prompt. |

---

## Skill Anatomy (House Style)

Every skill follows the same skeleton so they're predictable and combinable:

1. **Frontmatter**: `name` (matches the folder) and a `description` that says *what* the skill does and *when* to use it — this is what Claude reads to decide whether to load it
2. **Role**: one line, what it does (no persona inflation)
3. **How to Work**: shared rules — clarify only what changes the answer, match depth to the request, check silently, verify version-sensitive facts, safe by default, scannable output
4. **Core Knowledge Domains**: decision matrices, standards tables, deprecations
5. **Silent Pre-Answer Check → Delivery Format**: the checklist runs internally; the full format is for design/build/review requests
6. **Ground Rules**: one-line *Never/Always* guardrails
7. **Accuracy & Currency Notes**: dated corrections that override older text above
8. **`references/`** *(optional)*: large catalogs that load only when needed

New skills: use [`/prompt-engineering-architect`](skills/prompt-engineering-architect/SKILL.md) in **Build** mode, put the skill in `skills/<kebab-case-name>/SKILL.md`, and add a row to the matching table above.

---

## Keeping Skills Current

Fast-moving facts are tagged **[verify]** and each skill carries a *reviewed* date. List everything that needs a periodic check:

```bash
grep -rn "\[verify" skills/
```

**Rebuilding from `my_prompts`:** `tools/build.py` converts every prompt (shared rules, per-skill fixes in `tools/cfg_*.py`, reference splits) and fails loudly if a fix no longer matches its source:

```bash
python tools/build.py <path-to-my_prompts> . && python tools/gen_readme.py <path-to-my_prompts> .
```
