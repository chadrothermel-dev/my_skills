# Prompt Library Audit — `my_prompts` → `my_skills`

**Reviewed:** October 2026 · **Scope:** all 39 prompts in [`my_prompts`](https://github.com/chadrothermel-dev/my_prompts) · **Result:** every finding below is already fixed in the matching skill in this repo, unless it's marked *open*.

## TL;DR

- **The library is strong on structure and domain depth.** The newer prompts (identity, monitoring, comms, career, personal) are close to best practice.
- **The biggest accuracy risk is hard-coded facts.** A model treats facts inside its system prompt as ground truth and repeats them. Several prompts contain stale product names, a few invented function or cmdlet names, and three real bugs (a units error in a formula, two PowerShell logic bugs).
- **The biggest output-quality issue is format rigidity.** Most technical prompts force a printed `<verification>` block and a 6-part report for *every* request, including one-line questions.

**Confidence labels used below:** ✅ **Confirmed** (verifiable error) · 🕐 **Stale** (was true, has since changed) · ❓ **Verify** (likely wrong or changed, but confirm against current docs).

---

## 1. Cross-Cutting Findings

| # | Finding | Why it hurts output | Fix applied in skills |
| :-- | :--- | :--- | :--- |
| 1 | **Printed verification blocks.** 27 prompts define a `<verification>` phase. Only ADHD and Project Management clearly say to hide it, and 3 (Linux, VMware, Microsoft AI) explicitly say to *output* it. | In chat, the user sees a wall of self-audit before the answer. Models with extended thinking already reason privately, so the printed block adds noise without improving accuracy. | Every check runs silently: *"Run this checklist internally… never print it."* |
| 2 | **One rigid format for every request.** "Deliver your response strictly in this 6-part format." | A question like "what's the esxtop counter for CPU ready?" comes back as a 6-section report. That's slower to read and buries the answer, which works against micro-steps and scannable output. | A shared rule matches depth to the request: quick question → direct answer; design/build/review → full format. |
| 3 | **Clarify-vs-complete conflict.** "Zero-Assumption: never guess, must pause and ask" sits next to "always output complete code, no placeholders." | The model either over-asks (annoying) or invents environment values (dangerous). | Ask up to 3 questions *only* when the answer or the risk depends on them. Otherwise state assumptions in one line and use `<PLACEHOLDER>` for unknown environment values. Each skill lists its usual blocking questions. |
| 4 | **Hard-coded facts that go stale, and "zero hallucination" rules the prompt itself breaks.** | The prompt's own invented Cribl function names, Pack IDs, and cmdlets get repeated as fact, and the anti-hallucination rule can't catch errors that come from the prompt. | Fixed inline where confident. Uncertain items are tagged **[verify]**, every skill has a dated *Accuracy & Currency Notes* section, and every skill is told to verify version-sensitive facts with tools (web search, Microsoft Learn MCP). |
| 5 | **Persona inflation.** "Distinguished Fellow," "30+ years," "Board-Certified," and long certification lists. | It doesn't change behavior (your own Prompt Engineering Architect, principle #1, says so) but costs tokens. "Board-Certified ADHD strategist" claims a credential that doesn't exist. | Replaced with a one-line **Role** that says what the skill does. |
| 6 | **House-style drift.** About 17 older prompts have no Clarification Protocol, and Culinary/Personal Finance use an older "prompt-in-a-code-block" format. | Inconsistent behavior across the library. | A shared "How to Work" block gives every skill a clarification rule. Culinary and Personal Finance were rewritten. |
| 7 | **Cross-prompt contradictions.** Basic Logs savings is "~66%", "70–80%", or "up to 80%", and retention is "8 days" in two prompts. Elastic pricing units are "SCU/ICU" in one prompt and "VCU" in another. The same Cribl function is called "Sample" and "Sampling". | Combined prompts give conflicting numbers. | Numbers were made consistent, or replaced with "[verify current pricing]". |
| 8 | **Security rules contradicted by their own examples.** CI/CD says "zero static credentials" but turns off SSH host-key checking and uses a NuGet API key. Linux says "least privilege" but exports NFS with `no_root_squash`. Security's sshd example could lock you out. | Models copy examples more faithfully than they follow rules. | Examples fixed, or the exception documented with mitigations. |
| 9 | **ALL-CAPS absolutes everywhere** (MUST / NEVER / ZERO). | Current Claude models follow instructions literally. Heavy emphasis leads to over-application, such as refusing a GUI path when one is the only option. | Safety rules keep their emphasis. Format rules were softened. *(Open: a full tone pass wasn't done; most content rules keep their original wording.)* |
| 10 | **Oversized single files.** ADHD is 45 KB, Data Center 40 KB, Cribl+Elastic+Sentinel 34 KB. | Everything loads every time, even when only one table is needed. | Large catalogs moved to `references/*.md` that load only when needed. All `SKILL.md` files are under 500 lines. |

---

## 2. Scorecard

🔴 High = factual bugs or heavy staleness · 🟡 Medium = several stale items or structural gaps · 🟢 Low = polish only

| Prompt → Skill | Priority | Main issues (all fixed unless noted) |
| :--- | :---: | :--- |
| BCDR → `bcdr-recovery-architect` | 🔴 | ✅ Bandwidth formula units/ratio error; ✅ Rubrik cmdlets mixed between two SDKs; 🕐 Veeam v13 |
| PKI → `pki-certificates` | 🔴 | ✅ PowerShell interpolation bug; 🕐 missing CA/B Forum 200/100/47-day lifetimes; missing AD CS ESC1 risk on "supply in request"; ❓ `DeterministicRevocation` |
| VMware → `vmware-vsphere` | 🔴 | ✅ Hardware-version string-compare bug; 🕐 Aria → VCF Operations/Automation; VVD retired; vSphere 7 EOL; `-Version` deprecated |
| Cribl Cloud → `cribl-stream` | 🔴 | ✅ Clone/Tee described wrongly; ✅ "internal fields" table mixes in non-internal fields; ✅ wrong `C.Lookup` signature; ❓ `C.Math`/`C.Metric` |
| Cribl+Elastic+Sentinel → `cribl-elastic-sentinel-pipelines` | 🔴 | ❓ ~8 function names that don't appear in Cribl docs (Keep, Rate Limit, Trim, Compress, …); ❓ unverified Pack IDs; 🕐 Data Collector API retired 14 Sep 2026; ❓ `strftime` units |
| Microsoft AI → `microsoft-ai-architect` | 🔴 | 🕐 Foundry rename, Agent Framework, Copilot Workspace/Extensions sunset, Copilot Studio billing, DSPM for AI, M365 Agents SDK; forced printed verification |
| Data Center → `datacenter-hardware` | 🔴 | 🕐 Whole catalog is one generation behind; ✅ iDRAC10 attributed to 16G; ✅ Xeon w9-3595X is a workstation CPU; 🕐 HyperFlex/C480 EOL |
| Kubernetes → `kubernetes-platform` | 🔴 | 🕐 ingress-nginx retired; `etcdctl snapshot restore` → `etcdutl`; Kyverno `validationFailureAction` moved to rule level; version target 1.28–1.31; Tanzu → VKS |
| Sentinel → `microsoft-sentinel` | 🔴 | 🕐 Basic Logs now 30 days; DCE optional; TI table renamed; Defender-portal migration; ❓ grouping window; least-privilege Graph permission |
| CI/CD → `cicd-gitops-pipelines` | 🔴 | 🕐 tfsec → Trivy; `azure/login@v2`; ansible-lint action moved; ✅ host-key checking disabled; ❓ `checkov-task@1` |
| Personal Finance → `personal-finance` | 🔴 | ✅ Payoff formula ignores interest; no "not a licensed advisor" boundary; extra "are you ready?" turn |
| Ansible → `ansible-automation` | 🟡 | ✅ Module table breaks its own FQCN rule; 🕐 controller Python 3.9+; `yum` module removed; `win_domain` → `microsoft.ad`; ✅ IIS example port mismatch |
| Terraform → `terraform-iac` | 🟡 | 🕐 S3 DynamoDB locking deprecated; azurerm 4.x; tfsec; HCP Terraform; ephemeral/write-only secrets; `terraform test`; ✅ unescaped regex dot |
| Linux → `linux-sysadmin` | 🟡 | ✅ `no_root_squash`; `ip_forward` listed as "tuning"; 🕐 `podman generate systemd` → Quadlet; RHEL 10; printed verification |
| Windows Server → `windows-server` | 🟡 | ✅ Windows LAPS is Server 2019+, not 2022+; S2D RDMA is recommended, not required; 🕐 2025 EOL; WSUS deprecated; `Get-EventLog` |
| Azure → `azure-solutions-architect` | 🟡 | 🕐 Spring Apps retiring; Azure Cache for Redis → Managed Redis; Azure OpenAI/Foundry; no clarification checklist |
| Cloud FinOps → `cloud-finops` | 🟡 | 🕐 Basic Logs retention; ❓ commitment tier range; missing FOCUS exports; "dummy" prices in a query |
| Elastic → `elastic-stack` | 🟡 | 🕐 "Assume 8.x" (9.x current); pricing units; no clarification protocol |
| Networking → `enterprise-networking` | 🟡 | IKEv2 not the default; SD-WAN/VPN client names; SSL-VPN deprecation trend; SNMPv3 SHA-1 |
| Security → `security-compliance-hardening` | 🟡 | ✅ "Entegra" (should be Pwned Passwords); 🕐 NIST 800-63B Rev 4 lengths; PCI DSS 4.0.1; ESXi 7 EOL; ✅ sshd edit with no `validate:` |
| PowerShell → `powershell-expert` | 🟡 | No clarification or verification; PSResourceGet; `SecureString` cross-platform caveat; "`[CmdletBinding()]` prerequisite checks" is wrong (should be `#Requires`) |
| Culinary → `meal-planner` | 🟡 | Old format; hard-coded teen age; extra readiness turn; no leftovers/prep plan; missing Bakery section |
| Systems Procedure → `sop-documentation` | 🟡 | "Production-tested" commands the model can't test; inferred steps were unmarked → now tagged **[ASSUMED — confirm]** |
| Prompt Engineering → `prompt-engineering-architect` | 🟡 | House style now covers skills, silent checks, response scaling, and currency hygiene |
| Entra/Intune → `entra-intune-identity` | 🟢 | Added mandatory Azure MFA and break-glass guidance |
| Monitoring → `monitoring-alerting` | 🟢 | Aria → VCF Operations naming; MMA retirement note |
| Incident Response → `incident-response` | 🟢 | Solo-IC reality; `provisioningState` ≠ health |
| Project Management → `it-project-management` | 🟢 | Server 2022 → 2025 example |
| ADHD Coach → `adhd-executive-function-coach` | 🟢 | Credential claims removed; sleep statistic softened; split into references |
| Formal Logic → `formal-logic-analyzer` | 🟢 | Over-precise "94%" confidence; added charity principle and a short mode |
| Weekly Reset, Fitness, Home, Travel, Genealogy, Learning, Career ×2, Exec Comms | 🟢 | Already in good shape; got the shared coaching rules and skill cross-references |

---

## 3. Detail on the Confirmed Bugs

1. **BCDR bandwidth formula.** `Daily Change (GB) × 8 × (1 − ratio) / seconds` gives **Gbps**, not Mbps (it's missing ×1000). `(1 − ratio)` also goes negative for a 2:1 ratio. Corrected version: `GB × 8000 / (reduction ratio × seconds) × 1.3`, with a worked example (500 GB/day, 2:1, 8 h ≈ 90 Mbps).
2. **PKI expiry query.** `"NotAfter -lt $(Get-Date).AddDays(30)"` inside a double-quoted string expands to `"…10/03/2026 07:00:00.AddDays(30)"`. The fix is `$((Get-Date).AddDays(30))`. It also depends on the community **PSPKI** module, which the prompt never mentioned.
3. **VMware hardware-version filter.** `$_.HardwareVersion -lt "vmx-19"` compares strings, so `"vmx-9"` sorts *after* `"vmx-19"` and old VMs are silently skipped. The fix compares numerically, filters to powered-off VMs, and uses `-HardwareVersion` (`-Version` is deprecated).
4. **Debt payoff time** = balance ÷ payment ignores interest. Replaced with the amortization formula, plus a check for payments that never pay the debt off.
5. **Rubrik example.** It mixed RSC (`rsc.rubrik.com`) with legacy CDM-SDK cmdlets and used parameter names that don't exist (`Set-RubrikVM -SlaId`). Now the two modules are separated, and the CDM example uses `Protect-RubrikVM`/`New-RubrikMount` [verify].

---

## 4. Open Items (not fixed, worth a look)

- **Tone pass.** *Partly done (see §7):* protocol-level MUST/strictly wording is softened. Domain rules that state real technical limits (e.g., etcd `fsync` latency) keep their emphasis on purpose.
- **[verify] tags.** The skills contain ~90 **[verify]** tags. Each one is a fact that's likely changed or uncertain and needs a 30-second check against vendor docs. Run `grep -rn "\[verify" skills/` to list them.
- **Backport to `my_prompts`.** *Done (see §7).* Only fixes that point at other skills by name remain in `tools/cfg_*.py`.
- **Fold accuracy notes inline.** Each "Accuracy & Currency Notes" section says it overrides the text above it. Editing the conflicting lines directly would remove the contradiction, as the skill best practices recommend.
- **Quarterly currency review.** Microsoft AI, Sentinel, Data Center, and Kubernetes go stale fastest. Re-run `prompt-engineering-architect` in Audit mode each quarter.

## 5. Suggested Test Inputs

| Skill | Test prompt | Pass criteria |
| :--- | :--- | :--- |
| `vmware-vsphere` | "What esxtop counter shows CPU contention?" | Short direct answer (`%RDY`, >10%), not a 6-part report |
| `bcdr-recovery-architect` | "Replicate 2 TB/day at 3:1 in a 10-hour window — what bandwidth?" | ≈ 193 Mbps using the corrected formula, with math shown |
| `pki-certificates` | "Design renewal for our public web certs." | Mentions the 200/100/47-day schedule and ACME automation |
| `cribl-elastic-sentinel-pipelines` | "Which function keeps only certain fields?" | Eval → Keep fields, not a nonexistent "Keep" function |
| `personal-finance` | "$5,000 at 24% APR paying $150/month — how long?" | ≈ 56 months via amortization, not 33 |

---

## 6. Rebuild After the `my_prompts` Accuracy Pass (October 2026)

The `my_prompts` accuracy pass corrected the source prompts directly, so most fixes in `tools/cfg_*.py` no longer matched and `build.py` failed for 25 skills.

| Result | Count | Action |
| :--- | :--- | :--- |
| Fix already applied word-for-word in the prompt | 14 | Removed |
| Same problem already corrected in the prompt, different wording | 119 | Removed (each reviewed against the current prompt text) |
| Still needed | 1 | Re-targeted: `ansible-automation` IIS example notes port 80 is lab-only |
| Accuracy note made obsolete by the prompt | 1 | Removed: `cribl-elastic-sentinel-pipelines` `_time * 1000` warning |

All 45 skills now rebuild from the current prompts with `python tools/build.py ../my_prompts .`, and every skill picks up the prompt-level corrections.

## 7. Best-Practice Refresh (2026-10-21)

Checked against Anthropic's current [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [Claude Code skills docs](https://code.claude.com/docs/en/skills).

**The existing skills already met the hard limits:** every body is under 500 lines, descriptions are 277–644 characters (the limit is 1,024), all are third person with "Use when", and no skill uses non-portable frontmatter.

| Change | Why |
| :--- | :--- |
| 49 content fixes and 19 accuracy-note sets moved from `tools/cfg_*.py` into the source prompts | Raw-prompt users (Projects, GPTs, API) were missing corrections that only skills had. The rebuild was byte-identical. |
| 34 prompts now run their check silently and scale the format to the request | Current models follow system prompts closely and over-trigger on stacked CAPS/MUST and rigid formats. The rebuild was byte-identical. |
| `build.py` lints every skill and fails the build on a violation | Covers frontmatter on line 1, claude.ai-portable keys only, reserved words, XML or non-third-person descriptions, a missing "Use when", 500+ line bodies, broken/backslash/nested reference links |
| Reference files over 100 lines get a Contents list (3 files) | Claude may preview long files partially; a TOC keeps the full scope visible |
| Prompt Engineering Architect updated | Calibrated emphasis with reasons, positive instructions, XML tags, 3–5 tagged examples, no time-bombed wording, a skill-authoring checklist, eval-style test inputs |
| `evals/` added: 3 scenarios each for the new skills | "Build evaluations first." It lives outside `skills/` so it doesn't ship |
| 3 new skills: `video-media-production`, `windows-workstation-tuning`, `web-project-publishing` | Recurring themes across recent Claude Code sessions not covered by an existing skill |

**Deliberately not changed:** skill names stay noun-style rather than gerunds, because renaming would break installed `/my-skills:` commands. No `when_to_use` key was added either, because claude.ai uploads reject it.
