# Secrets

Start with this question: should the value be hidden from output, or never stored?

| Method | Kept out of state and plan | Version |
|---|---|---|
| `sensitive = true` | **No, it only redacts output** | 0.15 |
| `ephemeral = true` on variables and child outputs | Yes | 1.10 |
| `ephemeral` block | Yes | 1.10 |
| Write-only argument (`*_wo`) | Yes | 1.11 |

Use `sensitive` and `ephemeral` together to redact a value and avoid storing it. `terraform output -json` and `-raw` show sensitive values in plain text.

## Where ephemeral values can go

- Write-only arguments
- Other `ephemeral` blocks
- `locals`
- `variable` and child `output` blocks with `ephemeral = true`
- `provider` blocks
- Provisioner and `connection` blocks

Anywhere else fails at plan. Root module outputs can't be ephemeral.

```hcl
variable "api_token" {
  type        = string
  description = "Short-lived token for the provider."
  sensitive   = true
  ephemeral   = true
}
```

## Write-only arguments

- Providers define them, and they usually end in `_wo` with a matching `_wo_version`.
- Check the Registry for support.
- Terraform can't detect a changed value, so increment the version argument to rotate it.
- They accept non-ephemeral values too, but a literal string defeats the purpose.

## Azure pattern

HashiCorp's example generates a password with ephemeral `random_password`, stores it with `value_wo` on `azurerm_key_vault_secret`, then reads it with ephemeral `azurerm_key_vault_secret` into `administrator_password_wo`. Check these arguments against your azurerm version.

## Keeping a generated value

Ephemeral values aren't saved. Capture one in a secret store, or in a `terraform_data` `store` block (1.16+) if you accept storing it in state.

## Other rules

- Use workload identity or OIDC instead of long-lived keys.
- Set credentials through environment variables or the provider's auth flow.
- If a secret reached state, rotate it. Removing it from code doesn't remove it from old state versions.
- `terraform_remote_state` exposes state data to readers, so prefer publishing specific values.
