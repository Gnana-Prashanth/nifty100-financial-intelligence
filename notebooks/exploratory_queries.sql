SELECT COUNT * FROM companies;


SELECT COUNT * FROM profitandloss;


SELECT company_name
FROM companies
LIMIT 10;


SELECT company_id,
        year,
        sales,
        net_profit
FROM profitandloss
LIMIT 10;


SELECT company_id,
        matket_cap_store
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;


SELECT company_id,
       return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;


SELECT broad_sector,
       COUNT(*)
FROM sectors
GROUP BY broad_sector;


SELECT company_id,
       COUNT(DISTINCT year)
FROM profitandloss
GROUP BY company_id
ORDER BY COUNT(DISTINCT year);


SELECT *
FROM peer_groups
LIMIT 10;


SELECT company_id,
       close_price
FROM stock_prices
ORDER BY date DESC
LIMIT 10;
