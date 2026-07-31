-- 1. Top 5 Funds by AUM

SELECT
    scheme_name,
    aum_crore
FROM "07_scheme_performance"
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. Average NAV per Month

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav),2) AS average_nav
FROM "02_nav_history"
GROUP BY month
ORDER BY month;


-- 3. Monthly SIP Inflows

SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM "04_monthly_sip_inflows"
ORDER BY month;


-- 4. Transactions by State

SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM "08_investor_transactions"
GROUP BY state
ORDER BY total_amount DESC;


-- 5. Funds with Expense Ratio Less Than 1%

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM "07_scheme_performance"
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


-- 6. Top 10 Performing Funds (3-Year Return)

SELECT
    scheme_name,
    return_3yr_pct
FROM "07_scheme_performance"
ORDER BY return_3yr_pct DESC
LIMIT 10;


-- 7. Fund House Wise AUM

SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM "03_aum_by_fund_house"
GROUP BY fund_house
ORDER BY total_aum DESC;


-- 8. Average Return by Category

SELECT
    category,
    ROUND(AVG(return_3yr_pct),2) AS avg_return
FROM "07_scheme_performance"
GROUP BY category
ORDER BY avg_return DESC;


-- 9. Transaction Type Distribution

SELECT
    transaction_type,
    COUNT(*) AS total_transactions
FROM "08_investor_transactions"
GROUP BY transaction_type
ORDER BY total_transactions DESC;


-- 10. Highest Rated Funds

SELECT
    scheme_name,
    morningstar_rating
FROM "07_scheme_performance"
WHERE morningstar_rating = 5
ORDER BY scheme_name;