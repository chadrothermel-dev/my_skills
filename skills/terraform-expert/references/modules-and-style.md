# Modules and style

## Layout

From HashiCorp's style guide:

| File | Holds |
|---|---|
| `terraform.tf` | `required_version`, `required_providers` |
| `backend.tf` | Backend |
| `providers.tf` | Provider configuration |
| `main.tf` | Resources and data sources |
| `variables.tf` | Variables, alphabetical |
| `outputs.tf` | Outputs, alphabetical |
| `locals.tf` | Locals used across files |

Larger projects can split by function: `network.tf`, `storage.tf`, `compute.tf`.

## Style rules

- Run `terraform fmt` and `terraform validate` before committing, and use a linter such as TFLint.
- Use `#` for comments.
- Name resources with nouns and underscores, without repeating the type.
- Give every variable a `type` and `description`, and every output a `description`.
- Avoid overusing variables and locals.
- Put meta-arguments first, then arguments, then nested blocks.
- Define dependent resources after what they reference.

## Good module design

These are design recommendations rather than language rules:

- Make a module for a real abstraction, not a thin wrapper around one resource.
- Keep provider configuration in the root, and declare `required_providers` with minimum versions in modules.
- Pass values through inputs and outputs rather than reading remote state inside modules.
- Use object types with `optional()` for grouped inputs, and validate them.
- Pin module versions, and keep `moved` blocks when renaming resources in a released module.
- Mark retiring inputs and outputs with `deprecated` (1.15+).

```hcl
variable "network" {
  type = object({
    name          = string
    address_space = list(string)
    dns_servers   = optional(list(string), [])
  })
  description = "Network to create."

  validation {
    condition     = length(var.network.address_space) > 0
    error_message = "Provide at least one address space."
  }
}
```

## Module sources from variables (1.15+)

```hcl
variable "module_source" {
  type        = string
  description = "Location of the network module."
  default     = "./modules/network"
  const       = true
}

module "network" {
  source = var.module_source
}
```

`const` variables must have known values at init, and can't depend on plan results.

## Environments

- Separate directories or Stacks give clear isolation between environments.
- CLI workspaces suit near-identical deployments sharing a backend. They aren't a strong security boundary, because credentials and backend are shared.
- HCP Terraform workspaces are different from CLI workspaces, and each has its own state, variables, and permissions.
- Keep state small. Split by lifecycle and ownership to reduce blast radius and plan time.

## Example repository shape

```text
platform/connectivity/   hub network, firewall, DNS
platform/identity/       shared identity
workloads/<app>/<env>/   spokes and workloads
modules/                 versioned reusable modules
```

Share values between layers through published outputs or data sources, not by reading whole state files.
