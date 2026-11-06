# Feature versions

Source: Terraform changelogs and docs for v1.17. Latest stable when built: 1.17.1 (October 2026).

| Version | Added |
|---|---|
| 0.15 | `sensitive` on variables and outputs |
| 1.1 | `moved` blocks |
| 1.4 | `terraform_data` |
| 1.5 | `import` blocks, `check` blocks, `-generate-config-out` (experimental) |
| 1.6 | `terraform test` |
| 1.7 | `removed` blocks, `for_each` on `import`, test mocking |
| 1.8 | Provider-defined functions |
| 1.9 | Variable validation can reference other objects |
| 1.10 | Ephemeral variables, outputs, and `ephemeral` blocks |
| 1.11 | Write-only arguments, S3 `use_lockfile` GA, DynamoDB locking deprecated |
| 1.13 | `terraform stacks` command; `variable` blocks in test files |
| 1.14 | `terraform query`, `list` blocks, `action` blocks, `lifecycle.action_trigger` |
| 1.15 | Variables in module `source` and `version`; `deprecated` on variables and outputs; `convert()`; output `type`; `validate` checks the `backend` block |
| 1.16 | `import` inside modules; `lifecycle { destroy = false }` on resources; `terraform_data` `store` block; `graph -format=mermaid`; `state show -json`; `console -scope`; action `on_failure` modes and destroy events |
| 1.17 | Variables and locals in provider requirements; `-minimal-refresh`; Terraform Policy GA with `-policies`; `mock_provider` for ephemeral resources |

## Experimental, not in stable releases

Experiments only work in alpha builds: `-allow-deferral` (unknown `count` and `for_each`), `terraform test cleanup`, and `backend` blocks and `skip_cleanup` in tests. Don't recommend them for production.

## Upgrade notes

- **1.10:** Run `terraform init -reconfigure` for the S3 backend. Root assume-role arguments moved into the `assume_role` block. `moved` addresses that clash with reserved keywords need a `resource.` prefix.
- **1.11:** S3 `use_lockfile` needs IAM access to the `.tflock` object.
- **1.13:** Declare external test variables in the test file. It's optional, but complex types can otherwise error.
- **1.14:** Parallelism may drop in containers, based on the CPU limit.
- **1.15:** S3 `AWS_USE_FIPS_ENDPOINT` and `AWS_USE_DUALSTACK_ENDPOINT` accept only `true` or `false`.
- **1.16:** `bastion_host_key` is now applied by provisioners, so check the key is correct before upgrading.

Terraform 1.x follows the v1.0 compatibility promises. Upgrade one minor version at a time in non-production first, and run a plan to confirm no unexpected changes.
