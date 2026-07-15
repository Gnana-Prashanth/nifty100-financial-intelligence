# Sprint 2 Retrospective

## Completed
- Implemented profitability ratios
- Implemented leverage ratios
- Built CAGR engine
- Built cash flow KPI engine
- Populated financial_ratios table
- Generated capital_allocation.csv
- Generated ratio_edge_cases.log

## Challenges
- Duplicate IDs during merge
- SQLite IntegrityErrors
- Different headers in supporting datasets
- Financial ratios merge conflicts
- CAGR edge cases

## Fixes
- Normalized data
- Removed duplicate IDs
- Added ROCE column
- Cleaned financial_ratios table

## Lessons Learned
- Reusable functions simplify integration.
- Verify intermediate outputs before updating the database.
- Handle edge cases before production calculations.