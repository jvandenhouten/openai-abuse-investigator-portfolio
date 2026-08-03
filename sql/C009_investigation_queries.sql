-- C-009 Deep-Dive Investigation Pack
-- Synthetic data only. SQLite compatible.
-- Each output is an investigative lead requiring contextual human review.

-- Q1. What accounts are assigned to C-009, and what roles do they perform?
SELECT ca.account_id,
       a.role,
       a.prior_enforcement,
       a.risk_tier,
       a.geo_region,
       a.language
FROM case_accounts ca
JOIN accounts a ON a.account_id = ca.account_id
WHERE ca.case_id = 'C-009'
ORDER BY a.role, ca.account_id;

-- Q2. Which C-009 accounts also appear in another investigation?
SELECT ca.account_id,
       COUNT(DISTINCT ca.case_id) AS case_count,
       GROUP_CONCAT(DISTINCT ca.case_id) AS cases,
       a.role,
       a.prior_enforcement,
       a.risk_tier
FROM case_accounts ca
JOIN accounts a ON a.account_id = ca.account_id
WHERE ca.account_id IN (
    SELECT account_id
    FROM case_accounts
    WHERE case_id = 'C-009'
)
GROUP BY ca.account_id, a.role, a.prior_enforcement, a.risk_tier
HAVING COUNT(DISTINCT ca.case_id) > 1
ORDER BY case_count DESC, ca.account_id;

-- Q3. Which devices link C-009 accounts to other cases?
SELECT s.device_id,
       COUNT(DISTINCT e.case_id) AS case_count,
       GROUP_CONCAT(DISTINCT e.case_id) AS cases,
       COUNT(DISTINCT s.account_id) AS account_count
FROM sessions s
JOIN events e ON e.session_id = s.session_id
WHERE s.device_id IN (
    SELECT DISTINCT s2.device_id
    FROM sessions s2
    JOIN case_accounts ca ON ca.account_id = s2.account_id
    WHERE ca.case_id = 'C-009'
)
GROUP BY s.device_id
HAVING COUNT(DISTINCT e.case_id) > 1
ORDER BY case_count DESC, account_count DESC;

-- Q4. Which content templates or hashes recur across C-009 and another case?
SELECT c.content_hash,
       COUNT(DISTINCT c.case_id) AS case_count,
       GROUP_CONCAT(DISTINCT c.case_id) AS cases,
       COUNT(*) AS content_count,
       MIN(c.normalized_text) AS safe_example
FROM content c
WHERE c.content_hash IN (
    SELECT content_hash
    FROM content
    WHERE case_id = 'C-009'
)
GROUP BY c.content_hash
HAVING COUNT(DISTINCT c.case_id) > 1
ORDER BY case_count DESC, content_count DESC;

-- Q5. What is the event volume and average risk by synthetic network role?
SELECT a.role,
       COUNT(*) AS event_count,
       ROUND(AVG(CAST(e.raw_risk_score AS REAL)), 3) AS avg_risk,
       COUNT(DISTINCT e.account_id) AS account_count
FROM events e
JOIN accounts a ON a.account_id = e.account_id
WHERE e.case_id = 'C-009'
GROUP BY a.role
ORDER BY event_count DESC;

-- Q6. Which three-hour periods contain the highest event volume?
SELECT substr(timestamp, 1, 13) AS hour_bucket,
       COUNT(*) AS event_count,
       ROUND(AVG(CAST(raw_risk_score AS REAL)), 3) AS avg_risk
FROM events
WHERE case_id = 'C-009'
GROUP BY hour_bucket
ORDER BY event_count DESC, avg_risk DESC
LIMIT 20;

-- Q7. Which accounts combine high activity, high risk, and prior enforcement?
SELECT e.account_id,
       a.role,
       a.prior_enforcement,
       COUNT(*) AS event_count,
       ROUND(AVG(CAST(e.raw_risk_score AS REAL)), 3) AS avg_risk,
       ROUND(MAX(CAST(e.raw_risk_score AS REAL)), 3) AS max_risk,
       COUNT(DISTINCT NULLIF(e.pattern_id, '')) AS distinct_patterns,
       COUNT(DISTINCT NULLIF(e.target_id, '')) AS target_count
FROM events e
JOIN accounts a ON a.account_id = e.account_id
WHERE e.case_id = 'C-009'
GROUP BY e.account_id, a.role, a.prior_enforcement
ORDER BY a.prior_enforcement DESC, avg_risk DESC, event_count DESC;

-- Q8. What are C-009's strongest direct links to other cases?
SELECT CASE
           WHEN case_id_a = 'C-009' THEN case_id_b
           ELSE case_id_a
       END AS linked_case,
       link_type,
       CAST(strength AS REAL) AS strength,
       CAST(evidence_count AS INTEGER) AS evidence_count,
       analyst_confidence
FROM case_links
WHERE case_id_a = 'C-009' OR case_id_b = 'C-009'
ORDER BY strength DESC, evidence_count DESC;

-- Q9. What enforcement and triage activity is recorded for C-009?
SELECT action_id,
       account_id,
       report_source,
       CAST(triage_minutes AS INTEGER) AS triage_minutes,
       action_type,
       human_validated,
       action_timestamp
FROM reports_enforcement
WHERE case_id = 'C-009'
ORDER BY CAST(triage_minutes AS INTEGER), action_timestamp;

-- Q10. What evidence could contradict the coordinated-network hypothesis?
-- This query surfaces accounts with low risk, no prior enforcement, and limited pattern diversity.
SELECT e.account_id,
       a.role,
       a.prior_enforcement,
       COUNT(*) AS event_count,
       ROUND(AVG(CAST(e.raw_risk_score AS REAL)), 3) AS avg_risk,
       COUNT(DISTINCT NULLIF(e.pattern_id, '')) AS distinct_patterns
FROM events e
JOIN accounts a ON a.account_id = e.account_id
WHERE e.case_id = 'C-009'
GROUP BY e.account_id, a.role, a.prior_enforcement
HAVING AVG(CAST(e.raw_risk_score AS REAL)) < 0.60
    OR COUNT(DISTINCT NULLIF(e.pattern_id, '')) <= 2
ORDER BY avg_risk, distinct_patterns;
