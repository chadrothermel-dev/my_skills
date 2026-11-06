# Platform features

Check licensing and availability for HCP Terraform and Terraform Enterprise features, because they vary by plan.

## HCP Terraform connection

```hcl
terraform {
  cloud {
    organization = "example_corp"

    workspaces {
      tags = {
        layer = "app"
      }
    }
  }
}
```

- `cloud` and `backend` are mutually exclusive.
- `workspaces` takes `tags` or `name`, plus optional `project`.
- Don't put `token` in code. Use `terraform login`.
- Environment options include `TF_CLOUD_ORGANIZATION`, `TF_CLOUD_PROJECT`, `TF_WORKSPACE`, and `TF_CLOUD_HOSTNAME`.

## Stacks

An HCP Terraform layer for deploying the same components across many environments. Stacks run in HCP Terraform.

- `<name>.tfcomponent.hcl` holds `component` blocks, each sourcing a module.
- `<name>.tfdeploy.hcl` holds `deployment` blocks.
- `.terraform-version` sets the Terraform version.
- Stacks can sit beside workspaces in a project.

Consider them when one set of components repeats across many regions or accounts. Keep workspaces for simple, independent configurations. If you joined the beta, follow the GA update guide.

## Terraform Policy

GA in 1.17. The `-policies` flag works on `plan`, `apply`, and `query`, and selects policy-set directories. HCP Terraform and Terraform Enterprise also support policy enforcement. Read the policy enforcement docs before writing policies, as this skill doesn't cover the policy language.

## `terraform query` (1.14+)

Finds existing infrastructure through `list` blocks in `*.tfquery.hcl` files. Provider support varies.

```hcl
list "aws_instance" "web" {
  provider = aws

  limit = 50
}
```

- `terraform query` shows results.
- `terraform query -generate-config-out=generated.tf` writes `import` and `resource` blocks to review.
- `-json` gives machine-readable results.
- `limit` defaults to 100.
- `include_resource = true` returns full resource data.
- `terraform validate -query` checks query files offline.

## Actions (1.14+)

Provider-defined operations that don't change resource state, such as invoking a Lambda or running a playbook.

```hcl
action "aws_lambda_invoke" "notify" {
  config {
    function_name = "my_function"
    payload       = jsonencode({ source = "terraform" })
  }
}

resource "terraform_data" "release" {
  lifecycle {
    action_trigger {
      events  = [after_create, after_update]
      actions = [action.aws_lambda_invoke.notify]
    }
  }
}
```

Run one from the CLI with `terraform apply -invoke=action.aws_lambda_invoke.notify`.

- Events: `before_create`, `after_create`, `before_update`, `after_update`, `before_destroy`, `after_destroy`.
- `on_failure`: `halt` (default), `continue`, or `taint`.
- The `caller` symbol exposes the triggering resource inside `config`.
- Stacks need `action_trigger`, because `-invoke` doesn't work there.
