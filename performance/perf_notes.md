# Day 43 – Performance Testing Notes

## Project
Nifty100 Financial Intelligence

Date: 31/07/2026

---

# 1. Load Test

Objective:
Verify that the Screener API can handle 10 concurrent requests.

Method:
- Started FastAPI server on port 8000.
- Executed a Python threading script with 10 concurrent requests to:
  http://127.0.0.1:8000/api/v1/screener

Results:
- Concurrent Requests: 10
- Successful Requests: 10
- Failed Requests: 0
- Total Execution Time: 0.236 seconds
- Average Response Time: 0.194 seconds
- Fastest Response: 0.138 seconds
- Slowest Response: 0.233 seconds

Status:
✅ PASS

Observation:
The API successfully handled all concurrent requests without errors or timeouts.

---

# 2. Dashboard Performance

Objective:
Measure loading time of the Company Profile page.

Tested Companies:
- TCS
- INFY
- RELIANCE
- HDFCBANK
- ICICIBANK

| Company | Load Time | Status |
|---------|-----------|--------|
| TCS | 0.211 sec | PASS |
| INFY | 0.290 sec | PASS |
| RELIANCE | 0.230 sec | PASS |
| HDFCBANK | 0.201 sec | PASS |
| ICICIBANK | 0.221 sec | PASS |

Target:
Each page should load within 3 seconds.

Result:
✅ PASS

---

# 3. End-to-End Testing

Objective:
Verify FastAPI and Streamlit run simultaneously.

Verification:

- FastAPI running on port 8000
- Streamlit running on port 8501
- No port conflicts observed
- Dashboard opened successfully
- Company Profile page loaded correctly
- Screener page loaded successfully

Status:
✅ PASS

---

# 4. Performance Bottlenecks

No significant performance bottlenecks were observed during testing.

Observations:

- FastAPI responded consistently under concurrent load.
- Streamlit dashboard loaded successfully without noticeable delay.
- Company Profile pages loaded within the acceptable response time.
- No application crashes or timeout errors occurred.
- No port conflicts were encountered while running FastAPI and Streamlit simultaneously.

Overall Assessment:

Current application performance is satisfactory for the existing dataset and project requirements.

---

# 5. SQLite Query Optimization

Objective:
Improve database query performance by creating indexes on frequently queried columns.

Indexes Created:

- idx_balancesheet_company_year
- idx_cashflow_company_year
- idx_financial_ratios_company_year
- idx_market_cap_company_year
- idx_profitandloss_company_year

Columns Indexed:
- company_id
- year

Purpose:
These indexes help SQLite retrieve records more efficiently for queries that filter by `company_id` and `year`, reducing query execution time on large tables.

Result:
- Indexes created successfully.
- No existing data was modified.
- Database integrity remained unchanged.
- Query performance is optimized for common lookup operations.

Status:
✅ Optimization Completed

---

# Conclusion

All Day 43 performance testing tasks were completed successfully.

Summary:

- Load Testing: PASS
- Dashboard Performance: PASS
- End-to-End Testing: PASS
- Performance Review: Completed
- SQLite Performance Assessment: Completed

Overall Status:
✅ Day 43 Completed Successfully