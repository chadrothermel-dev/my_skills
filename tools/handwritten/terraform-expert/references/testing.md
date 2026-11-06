# Testing

| Tool | When it runs | Blocks the run? | Use for |
|---|---|---|---|
| `validation` | Plan | Yes | Input rules |
| `precondition` | Before an object changes | Yes | Assumptions |
| `postcondition` | After an object changes | Yes | Guarantees |
| `check` | End of plan and apply | No, it warns | Ongoing health |
| `terraform test` | On demand | Yes | Module behavior |

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment."

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Use dev, test, or prod."
  }
}

check "environment_named" {
  assert {
    condition     = length(var.environment) > 0
    error_message = "Environment is empty."
  }
}

output "name" {
  description = "Application name."
  value       = "app-${var.environment}"
}
```

## `terraform test`

Tests live in `*.tftest.hcl`, in the root or `tests/`. Each `run` block plans or applies.

- `command = apply` is the default. It creates **real infrastructure**, then destroys it.
- `command = plan` is faster and suits unit tests.
- Runs execute in order, and later runs can use `run.<name>.<output>`.
- `expect_failures` tests that a validation or check fails.

```hcl
variables {
  environment = "dev"
}

run "name_is_set" {
  command = plan

  assert {
    condition     = output.name == "app-dev"
    error_message = "Unexpected name."
  }
}

run "rejects_bad_environment" {
  command = plan

  variables {
    environment = "qa"
  }

  expect_failures = [var.environment]
}
```

## Mocks

Mocks avoid real infrastructure and credentials.

```hcl
mock_provider "aws" {
  mock_resource "aws_s3_bucket" {
    defaults = {
      arn = "arn:aws:s3:::example"
    }
  }
}
```

- `override_resource`, `override_data`, and `override_module` set specific values.
- `override_during = plan` uses mock values during plan.
- `-junit-xml` writes a CI report (GA in 1.11).
- Filter with `terraform test -filter=tests/basic.tftest.hcl`.

Mocks only prove your logic, not that a provider accepts the configuration. Keep at least one real apply test for important modules.
