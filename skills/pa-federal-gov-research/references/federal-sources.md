# Federal Source Map

> Reference file for the `pa-federal-gov-research` skill. Reviewed 2026-10.

## Federal Source Map

| Need | Primary source (Tier A) | Notes |
| :--- | :--- | :--- |
| Bills, status, text versions, actions, cosponsors, summaries | **congress.gov** | Search by number or keyword; filter by Congress. CRS bill summaries can lag introduction by weeks |
| Bill and law text, Congressional Record, hearings, committee reports, Federal Register, CFR | **govinfo.gov** (GPO) | Official, authenticated PDFs |
| Roll-call votes | **clerk.house.gov** (House), **senate.gov** (Senate) | Also linked from congress.gov actions |
| U.S. Code (current law) | **uscode.house.gov** | Note the "current through" Public Law |
| Cost of a bill | **cbo.gov** cost estimates | Not every bill gets one |
| Nonpartisan background | **CRS reports** (congress.gov) and **GAO** (gao.gov) | Excellent explainers; check publish date |
| Regulations: proposed and final rules, notices, executive orders | **federalregister.gov** | Shows comment deadlines and effective dates |
| Current regulations | **ecfr.gov** | Updated daily; the annual CFR on govinfo is the official edition |
| Rulemaking dockets and public comments | **regulations.gov** | Where to read and submit comments |
| Presidential actions | **whitehouse.gov** (presidential actions) | Confirm the official text in the Federal Register |
| Members, committees, contact info | congress.gov member pages, **house.gov**, **senate.gov** | House "Find Your Representative" works by ZIP+4 or address |
| Federal spending, grants, contracts | **usaspending.gov** | By agency, recipient, or location (including PA counties) |
| Debt, deficit, Treasury statements | **fiscaldata.treasury.gov** | Daily and monthly Treasury data |
| President's budget | **whitehouse.gov/omb** | A proposal; Congress appropriates |
| Population, income, housing, business | **census.gov** / **data.census.gov** | ACS 1-year vs. 5-year estimates have margins of error |
| Jobs, unemployment, wages, CPI | **bls.gov** | Note seasonal adjustment and revisions |
| GDP, personal income by state/county | **bea.gov** | |
| Energy prices and production | **eia.gov** | |
| Economic time series (many agencies in one place) | **FRED** (fred.stlouisfed.org) | Aggregator from the St. Louis Fed; cite the original agency |
| Dataset catalog | **data.gov** | |
| Federal elections and campaign finance | **fec.gov** | |
| Supreme Court opinions, dockets, argument calendar | **supremecourt.gov** | |
| Federal court cases | **PACER** (fees) via **uscourts.gov**; **CourtListener** (free, nonprofit, Tier B) | |
| Records requests | **foia.gov** | Use the `public-records-requests` skill |

**APIs (for repeat lookups or scripts):** Federal Register and USAspending need no key. Congress.gov, GovInfo, Regulations.gov, and FEC use a free **api.data.gov** key. Census allows 500 queries/day per IP without a key. BLS v2 needs a free registration key (renewed yearly). **Retired, don't recommend:** the ProPublica Congress API and the GovTrack API (the GovTrack website still works).
