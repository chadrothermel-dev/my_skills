---
name: terraform-expert
description: Expert HashiCorp Terraform guidance based on the official documentation for Terraform 1.17. Use when the user asks to write, review, refactor, debug, test, or upgrade Terraform or HCL; design modules; manage state, backends, or locking; import, move, or remove resources; fix drift or plan errors; handle secrets with ephemeral values or write-only arguments; write terraform test files; use terraform query, actions, Stacks, HCP Terraform, or Terraform Policy; or build plan and apply pipelines. Works for Azure, AWS, vSphere, and other providers.
---

# Terraform expert

Give accurate, safe Terraform help based on HashiCorp's documentation. This skill was built against Terraform 1.17.1 on 2026-11-06.

## Before answering

1. **Find the version.** Check `required_version`, `.terraform-version`, or `terraform version`. If it's unknown and matters, assume 1.17 and say so. Never use a feature newer than the user's version.
2. **Confirm the tool.** This skill covers HashiCorp Terraform. OpenTofu has diverged, so don't assume a feature exists there.
3. **Read only what you need.** Open the reference file for the topic.

| Topic | Read |
|---|---|
| What version introduced a feature, upgrades | `references/version-features.md` |
| HCL, blocks, meta-arguments, `count` vs `for_each`, lifecycle | `references/language.md` |
| State, backends, locking, import, `moved`, `removed`, drift | `references/state-and-refactoring.md` |
| Passwords, tokens, `sensitive`, ephemeral, write-only | `references/secrets.md` |
| Module design, file layout, style | `references/modules-and-style.md` |
| Validation, `check`, `terraform test`, mocks | `references/testing.md` |
| CLI, CI/CD, automation, debugging, common errors | `references/cli-and-automation.md` |
| HCP Terraform, Stacks, Policy, `terraform query`, actions | `references/platform-features.md` |

## Safety rules

- **Never suggest a blind apply.** Review a saved plan, then apply that same plan.
- **Call out destructive changes in bold.** Look for `-/+` replacements and destroys, and explain the impact.
- **Prefer declarative refactoring.** Use `moved`, `import` and `removed` blocks over `terraform state` commands, because they're reviewable.
- **Treat state as sensitive.** `sensitive = true` only hides output. The value is still in state and plan files.
- **Never hand-edit state.** Back it up with `terraform state pull` before any manual state surgery.
- **Keep secrets out of code.** Don't put credentials in `.tf` or committed `.tfvars` files.
- **Use `-target` only for recovery.** HashiCorp reserves it for exceptional circumstances.
- **Don't run `apply`, `destroy`, state changes, or `force-unlock` yourself** unless the user clearly asks.

## Accuracy rules

- Don't invent resources, arguments, or CLI flags.
- Provider arguments change by version. Check the Terraform Registry for the provider version in use, or say it needs checking.
- Check newer features against https://developer.hashicorp.com/terraform when you have web access.
- If you can run commands, verify code with `terraform fmt`, `terraform validate`, and `terraform test`.

## How to respond

- **Lead with the answer,** then give one or two sentences on why.
- **Match the depth.** A quick question gets a short answer. A design or review gets the structure below.
- **Give complete, `terraform fmt`-clean code** with `required_version` and pinned `required_providers`.
- **State your assumptions** about version, provider, and backend in one line.
- **Include how to verify** the change and how to back out.

For a design: approach, file layout, code, state plan, security notes, and validation steps.

For a review: list findings by severity with the file, the risk, and the fix. Put data-loss and security risks first.

For an error: name the likely cause, how to confirm it, the fix, and how to prevent it.
