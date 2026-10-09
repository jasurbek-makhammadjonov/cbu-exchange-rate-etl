-- 1. Latest USD rate
SELECT rate_date, rate_per_unit AS usd_uzs
FROM exchange_rates
WHERE currency = 'USD'
ORDER BY rate_date DESC
LIMIT 1;

-- 2. Monthly average rate per currency
SELECT substr(rate_date, 1, 7) AS month, currency,
       ROUND(AVG(rate_per_unit), 2) AS avg_rate
FROM exchange_rates
GROUP BY month, currency
ORDER BY month, currency;

-- 3. Day-over-day change using a window function
SELECT rate_date, currency, rate_per_unit,
       rate_per_unit - LAG(rate_per_unit) OVER (
           PARTITION BY currency ORDER BY rate_date
       ) AS change_vs_prev_day
FROM exchange_rates
WHERE currency = 'USD'
ORDER BY rate_date;

-- 4. Most volatile currencies (relative range, excluding very small rates)
SELECT currency,
       ROUND((MAX(rate_per_unit) - MIN(rate_per_unit)) / AVG(rate_per_unit) * 100, 2) AS range_pct
FROM exchange_rates
GROUP BY currency
HAVING COUNT(*) > 1 AND AVG(rate_per_unit) >= 1
ORDER BY range_pct DESC
LIMIT 10;
