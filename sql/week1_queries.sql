
-- 1. SELECT

-- Display all mutual fund schemes
SELECT *
FROM "01_fund_master";


-- 2. WHERE

-- Display only Equity funds
SELECT *
FROM "01_fund_master"
WHERE category='Equity';


-- Display only Debt funds
SELECT *
FROM "01_fund_master"
WHERE category='Debt';


-- 3. ORDER BY

-- Expense ratio (Highest to Lowest)
SELECT
scheme_name,
expense_ratio_pct
FROM "01_fund_master"
ORDER BY expense_ratio_pct DESC;


-- Expense ratio (Lowest to Highest)
SELECT
scheme_name,
expense_ratio_pct
FROM "01_fund_master"
ORDER BY expense_ratio_pct ASC;


-- 4. GROUP BY

-- Number of schemes in each fund house
SELECT
fund_house,
COUNT(*) AS total_schemes
FROM "01_fund_master"
GROUP BY fund_house;


-- Number of schemes in each category
SELECT
category,
COUNT(*) AS total_funds
FROM "01_fund_master"
GROUP BY category;


-- 5. HAVING

-- Fund houses having more than 3 schemes
SELECT
fund_house,
COUNT(*) AS total_schemes
FROM "01_fund_master"
GROUP BY fund_house
HAVING COUNT(*) > 3;


-- 6. Aggregate Functions

-- Average Expense Ratio
SELECT
AVG(expense_ratio_pct) AS average_expense_ratio
FROM "01_fund_master";


-- Maximum Expense Ratio
SELECT
MAX(expense_ratio_pct) AS maximum_expense_ratio
FROM "01_fund_master";


-- Minimum Expense Ratio
SELECT
MIN(expense_ratio_pct) AS minimum_expense_ratio
FROM "01_fund_master";


-- 7. JOIN

-- Join Fund Master with NAV History
SELECT
f.scheme_name,
n.nav,
n.date
FROM "01_fund_master" f
JOIN "02_nav_history" n
ON f.amfi_code=n.amfi_code;


-- 8. GROUP BY with AVG

-- Average expense ratio for each category
SELECT
category,
AVG(expense_ratio_pct) AS avg_expense
FROM "01_fund_master"
GROUP BY category;


-- 9. GROUP BY Risk Category

SELECT
risk_category,
COUNT(*) AS total_funds
FROM "01_fund_master"
GROUP BY risk_category;


-- 10. DISTINCT

SELECT DISTINCT fund_house
FROM "01_fund_master";


-- 11. LIMIT

-- Top 5 expense ratio funds
SELECT
scheme_name,
expense_ratio_pct
FROM "01_fund_master"
ORDER BY expense_ratio_pct DESC
LIMIT 5;


-- 12. LIKE

-- Search schemes containing Bluechip
SELECT
scheme_name
FROM "01_fund_master"
WHERE scheme_name LIKE '%Bluechip%';


-- 13. BETWEEN

SELECT
scheme_name,
expense_ratio_pct
FROM "01_fund_master"
WHERE expense_ratio_pct
BETWEEN 1.40 AND 1.60;


-- 14. IN

SELECT
scheme_name,
fund_house
FROM "01_fund_master"
WHERE fund_house IN
('SBI Mutual Fund',
'HDFC Mutual Fund');


-- 15. Subquery

-- Funds having expense ratio above average
SELECT
scheme_name,
expense_ratio_pct
FROM "01_fund_master"
WHERE expense_ratio_pct >
(
SELECT AVG(expense_ratio_pct)
FROM "01_fund_master"
);


-- 16. Window Function

SELECT
scheme_name,
expense_ratio_pct,
RANK() OVER
(
ORDER BY expense_ratio_pct DESC
) AS Expense_Rank
FROM "01_fund_master";