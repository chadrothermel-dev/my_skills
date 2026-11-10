#!/usr/bin/env python3
"""Compare wireless plans on true monthly cost.

Usage:
    python compare.py plans.json

Input JSON:
{
  "current": {"name": "Verizon Unlimited Plus", "monthly": 240, "device_payments": 40},
  "lines": 4,
  "default_tax_rate": 0.15,          # applied when a plan's price excludes taxes/fees
  "plans": [
    {
      "name": "Example Plan", "network": "T-Mobile",
      "monthly": 140,                 # total for all lines, with autopay
      "taxes_included": false,        # optional; default false
      "tax_rate": 0.12,               # optional override of default_tax_rate
      "one_time_fees": 140,           # activation etc.
      "switching_costs": 0,           # device payoffs, new unlocked phones
      "perks_valued": 18,             # $/mo of perks the user would otherwise buy
      "promo_months": 0,              # optional: months at promo_monthly price
      "promo_monthly": 0,
      "note": "Deprioritized data"
    }
  ]
}

Only standard library. Prints a markdown table sorted by all-in monthly cost.
"""
import json
import sys

HORIZON = 24  # months for one-time cost amortization and total cost


def evaluate(plan, lines, default_tax):
    tax = 0.0 if plan.get("taxes_included") else plan.get("tax_rate", default_tax)

    def with_tax(price):
        return price * (1 + tax)

    base = with_tax(plan["monthly"])
    promo_months = min(plan.get("promo_months", 0), HORIZON)
    promo_price = with_tax(plan.get("promo_monthly", plan["monthly"]))
    recurring_24 = promo_price * promo_months + base * (HORIZON - promo_months)
    one_time = plan.get("one_time_fees", 0) + plan.get("switching_costs", 0)
    total_24 = recurring_24 + one_time
    all_in = total_24 / HORIZON  # average monthly over 24 months, incl. one-time costs
    perks = plan.get("perks_valued", 0)
    return {
        "name": plan["name"],
        "network": plan.get("network", ""),
        "all_in": all_in,
        "per_line": all_in / lines,
        "perks": perks,
        "effective": all_in - perks,
        "total_24": total_24,
        "note": plan.get("note", ""),
    }


def main(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    lines = data["lines"]
    cur = data["current"]
    baseline = cur["monthly"] - cur.get("device_payments", 0)
    rows = [evaluate(p, lines, data.get("default_tax_rate", 0.15)) for p in data["plans"]]
    rows.sort(key=lambda r: r["all_in"])

    print(f"Baseline: {cur['name']} = ${baseline:,.2f}/mo for {lines} lines "
          f"(device payments excluded). All-in = 24-month average incl. taxes and one-time costs.\n")
    print("| Plan | Network | All-in $/mo | $/line | Perks valued | Effective $/mo | Saves/yr | 24-mo total | Note |")
    print("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |")
    for r in rows:
        saves = (baseline - r["all_in"]) * 12
        print(f"| {r['name']} | {r['network']} | ${r['all_in']:,.2f} | ${r['per_line']:,.2f} | "
              f"${r['perks']:,.2f} | ${r['effective']:,.2f} | ${saves:,.0f} | ${r['total_24']:,.0f} | {r['note']} |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
