# Language

## Contents

- The `terraform` block
- `count` or `for_each`
- Lifecycle
- Expressions
- Dependencies
- Providers
- Variables
- Avoid provisioners

## The `terraform` block

Holds `required_version`, `required_providers`, `backend` or `cloud` (mutually exclusive), and `experiments`. Since 1.17, provider requirements can use `const` variables and locals.

```hcl
terraform {
  required_version = ">= 1.11.0, < 2.0.0"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}
```

Commit `.terraform.lock.hcl`, and pin versions in root modules.

## `count` or `for_each`

- `count` suits identical instances or an on/off switch: `count = var.enabled ? 1 : 0`.
- `for_each` suits distinct instances, and takes a map or set of strings. Removing one item doesn't renumber the others.
- They're mutually exclusive.
- Their values must be known at plan time. Don't derive them from attributes that are only known after apply.
- HashiCorp's style guide says to use both sparingly.

```hcl
variable "storage_accounts" {
  type = map(object({
    tier = string
  }))
  description = "Accounts to create, by name."
}

resource "terraform_data" "account" {
  for_each = var.storage_accounts

  input = each.value.tier
}
```

## Lifecycle

| Rule | Effect |
|---|---|
| `create_before_destroy` | Creates the replacement first |
| `prevent_destroy` | Rejects plans that destroy it, but not if the block is removed from code |
| `destroy = false` (1.16+) | Resource isn't destroyed |
| `ignore_changes` | Ignores listed attributes |
| `replace_triggered_by` | Replaces when referenced items change |
| `precondition`, `postcondition` | Custom checks |
| `action_trigger` (1.14+) | Runs provider actions on lifecycle events |

Lifecycle arguments accept literal values only, because Terraform processes them early.

## Expressions

- Conditional: `var.prod ? 3 : 1`. Both results should be the same type.
- For: `{ for k, v in var.tags : lower(k) => v }`, with `if` to filter.
- Splat: `aws_instance.web[*].id`.
- `try()` returns the first expression that works. `can()` turns that into true or false.
- `convert(value, type)` (1.15+) converts inline.
- Use `dynamic` blocks sparingly, because they reduce readability.

```hcl
variable "rules" {
  type = map(object({
    port = number
  }))
  description = "Firewall rules, by name."
  default     = {}
}

locals {
  open_ports = [for name, rule in var.rules : rule.port if rule.port != 22]
}

output "open_ports" {
  type        = list(number)
  description = "Ports other than SSH."
  value       = local.open_ports
}
```

## Dependencies

Terraform infers order from references. Use `depends_on` only for hidden dependencies it can't see. Reference an attribute instead wherever possible.

## Providers

- Keep provider configuration in the root module. Pass aliases to child modules with `providers = {}`.
- Always include a default provider configuration, and define it first.
- Put `alias` first in non-default provider blocks.

## Variables

`variable` supports `type`, `default`, `description`, `validation`, `sensitive`, `nullable`, `ephemeral`, `const`, and `deprecated`.

Later sources win:
1. Environment variables (`TF_VAR_name`)
2. `terraform.tfvars`
3. `terraform.tfvars.json`
4. `*.auto.tfvars` and `*.auto.tfvars.json`, in lexical order
5. `-var` and `-var-file`, in the order given

Reserved variable names: `source`, `version`, `providers`, `count`, `for_each`, `lifecycle`, `depends_on`, `locals`.

## Avoid provisioners

HashiCorp recommends configuration management or other tools over provisioners. They don't sanitize input, so pass values through `environment` rather than interpolating into `local-exec` commands, which risks shell injection. For post-apply work on 1.14+, check whether the provider offers an action.
