# State and refactoring

## Contents

- State basics
- Azure backend
- S3 backend
- Refactor declaratively
- Import
- Drift
- State commands

## State basics

- State maps configuration to real objects. It holds sensitive values in plain text, so treat it as a secret.
- Exclude from Git: `*.tfstate`, `*.tfstate.*`, `.terraform/`, saved plans, and `.tfvars` with secrets.
- Commit `.terraform.lock.hcl`.
- For teams, use a remote backend with locking, encryption at rest, access control, and audit logs.

## Azure backend

Prefer Entra ID. The principal needs `Storage Blob Data Contributor` on the container.

```hcl
terraform {
  backend "azurerm" {
    use_azuread_auth     = true
    tenant_id            = "00000000-0000-0000-0000-000000000000"
    storage_account_name = "sttfstate001"
    container_name       = "tfstate"
    key                  = "prod/network.tfstate"
  }
}
```

`tenant_id` can come from `ARM_TENANT_ID`. Partial configuration is fine: leave settings out, then pass `-backend-config` at init.

## S3 backend

```hcl
terraform {
  backend "s3" {
    bucket       = "example-tfstate"
    key          = "prod/network.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

`use_lockfile` is GA from Terraform 1.11. DynamoDB locking is deprecated, but the two can run together during migration. Grant object access to the `.tflock` file too.

`validate` has checked the `backend` block since 1.15.

## Refactor declaratively

Keep these blocks until every state has applied them, and longer for shared modules.

```hcl
moved {
  from = terraform_data.old_name
  to   = terraform_data.new_name
}

resource "terraform_data" "new_name" {}

removed {
  from = terraform_data.retired

  lifecycle {
    destroy = false
  }
}
```

| Goal | Use |
|---|---|
| Rename or move into a module | `moved` |
| Stop managing but keep the object | `removed` with `destroy = false` |
| Stop managing and delete | Delete the code, or `removed` with `destroy = true` |
| Adopt existing objects | `import` |
| Keep a resource from being destroyed | `lifecycle { destroy = false }` (1.16+) |

## Import

`import` supports `to`, `id` or `identity` (mutually exclusive), `for_each`, and `provider`.

```hcl
locals {
  buckets = {
    logs = "example-logs"
    data = "example-data"
  }
}

import {
  for_each = local.buckets

  to = terraform_data.bucket[each.key]
  id = each.value
}

resource "terraform_data" "bucket" {
  for_each = local.buckets
}
```

Workflow:
1. Add the `import` block.
2. Write the resource, or generate it with `terraform plan -generate-config-out=generated.tf`. That option is still marked experimental in the docs.
3. Edit the generated code, because it's a starting point.
4. Plan until it shows imports and no unexpected changes, then apply.

To find resources in bulk, use `terraform query` (1.14+), covered in `platform-features.md`. `import` works inside modules from 1.16.

## Drift

- `terraform plan` shows drift.
- `terraform plan -refresh-only` reviews it without proposing configuration changes.
- Decide whether code or reality is correct. Update code to accept it, or apply to revert it.
- Use `ignore_changes` only for attributes another system legitimately owns.

## State commands

`state list`, `state show`, `state mv`, `state rm`, `state pull`, `state push`, `state replace-provider`, `state identities`.

Prefer blocks over `mv` and `rm`. Before manual surgery, save a copy with `terraform state pull > backup.tfstate`.

**Use `terraform force-unlock` only after confirming no other run holds the lock.** It can corrupt state if one does.
