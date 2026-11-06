# CLI and automation

## Daily workflow

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform show tfplan
terraform apply tfplan
```

Applying a saved plan runs exactly what was reviewed. Plan files can contain secrets, so protect pipeline artifacts.

## Useful options

| Need | Option |
|---|---|
| Replace one object | `plan -replace=ADDRESS` (prefer over `taint`) |
| Review drift only | `plan -refresh-only` |
| Fewer API calls | `plan -minimal-refresh` (1.17+) |
| Skip refresh, accepting stale data | `plan -refresh=false` |
| Run an action | `plan -invoke=action.TYPE.LABEL` |
| JSON plan for tooling | `terraform show -json tfplan` |
| Preview destroy | `plan -destroy` |
| Expressions in a module | `console -scope=module.name` (1.16+) |
| Dependency diagram | `graph -format=mermaid` (1.16+) |
| Lock for other platforms | `providers lock -platform=linux_amd64 -platform=windows_amd64` |
| Stop lock file changes in CI | `init -lockfile=readonly` |

## Pipeline design

1. On pull request: `fmt -check`, `init -backend=false`, `validate`, TFLint, a security scanner, and `terraform test`.
2. Run `plan -out`, publish a readable summary, and keep the plan as a protected artifact.
3. Require human approval for production.
4. Apply that saved plan with the same Terraform version and providers.
5. Allow only one apply per state at a time.
6. Run a scheduled `plan -detailed-exitcode` for drift. Exit code 2 means changes are present.

Authenticate with OIDC or workload identity, and scope permissions per environment.

## Automation environment variables

| Variable | Purpose |
|---|---|
| `TF_IN_AUTOMATION` | Adjusts output for automation |
| `TF_INPUT=0` | Disables prompts |
| `TF_CLI_ARGS`, `TF_CLI_ARGS_plan` | Adds default arguments |
| `TF_VAR_name` | Sets a variable |
| `TF_LOG`, `TF_LOG_PATH` | Debug logging |

Debug logs can include sensitive data, so don't publish them.

## Common errors

| Symptom | Likely cause | Fix |
|---|---|---|
| `Duplicate variable declaration` | Same name declared twice in a module | Keep one |
| `Invalid for_each argument` | Keys unknown until apply | Use known keys, usually from variables |
| Error acquiring the state lock | Another run, or a stale lock | Confirm none is running, then consider `force-unlock` |
| `Inconsistent dependency lock file` | Lock file doesn't match requirements | `terraform init -upgrade`, then review and commit |
| `Backend configuration changed` | Backend settings differ | `init -reconfigure`, or `-migrate-state` to move state |
| Resource already exists | Object created outside Terraform | Import it |
| Unexpected replacement | Change to a force-new argument | Read the `# forces replacement` line, then check `moved` or the provider docs |
| Cycle error | Circular references | Inspect `terraform graph`, then break the dependency |
| Plan keeps showing changes | Provider normalizes a value, or another system edits it | Match the normalized form, or use `ignore_changes` if it's externally owned |
| Provider auth failure | Wrong context or expired credentials | Check environment variables and identity, then read the provider's auth docs |
