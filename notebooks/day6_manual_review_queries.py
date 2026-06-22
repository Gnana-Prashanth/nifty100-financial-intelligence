import pandas as pd
import sqlite3
conn = sqlite3.connect("nifty100.db")


#Task 1: Review 5 Random Companies
query = """
SELECT DISTINCT id
FROM companies
ORDER BY RANDOM()
LIMIT 5
"""

df = pd.read_sql(query, conn)
print(df)


#Task 2: Year Coverage
query = """
SELECT company_id,
        COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
ORDER BY years
"""

df = pd.read_sql(query, conn)
print("\n",df)


#Task 3: Companies with <5 yearsTask 3: Companies with <5 years
query = """
SELECT company_id,
       COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5
ORDER BY years
"""

df = pd.read_sql(query, conn)
print("\n",df)
