WITH

-- 1. Filter to only the stores we care about (WA, OR, CA)
--    This reduces the dataset early and avoids unnecessary joins later
relevant_stores AS (
SELECT
store_id,
store_name,
city,
state
FROM stores
WHERE state IN ('Washington', 'California', 'Oregon')
),

-- 2. Aggregate line items directly to store × sale_date level
--    Early aggregation reduces the 85M line_items down to a much smaller dataset
--    Also precomputes the "treated" flag here to avoid extra computation later
daily_revenue AS (
SELECT
t.store_id,
t.sale_date AS date,
SUM(l.price * l.quantity) AS revenue,
MAX(CASE
WHEN t.store_id = 1630 AND t.sale_date >= DATE '2024-01-01'
THEN 1 ELSE 0
END) AS treated
FROM transactions t
INNER JOIN relevant_stores rs
ON t.store_id = rs.store_id           -- filter transactions to relevant stores
INNER JOIN line_items l
ON l.transaction_id = t.transaction_id -- attach line items
GROUP BY t.store_id, t.sale_date          -- final aggregation: store × day
),

-- 3. Collect all distinct sale dates that exist anywhere
--    Needed to create a balanced store × day panel
all_dates AS (
SELECT DISTINCT sale_date AS date
FROM transactions
),

-- 4. Build the balanced panel of all stores × all dates
--    Ensures every store has a row for every date, even if no sales occurred
--    `treated` is included here as well for completeness, though daily_revenue already has it
panel AS (
SELECT
rs.store_id,
rs.store_name,
rs.city,
rs.state,
d.date,
CASE
WHEN rs.store_id = 1630 AND d.date >= DATE '2024-01-01'
THEN 1 ELSE 0
END AS treated
FROM relevant_stores rs
CROSS JOIN all_dates d  -- produces store × date combinations
)

-- 5. Left join the aggregated daily revenue to the balanced panel
--    Use COALESCE to fill 0 for dates with no sales
SELECT
p.store_id,
p.store_name,
p.city,
p.state,
p.date,
p.treated,
COALESCE(dr.revenue, 0) AS daily_revenue
FROM panel p
LEFT JOIN daily_revenue dr
ON p.store_id = dr.store_id
AND p.date     = dr.date
ORDER BY p.store_id, p.date;
