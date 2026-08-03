-- OpenAI Abuse Investigator Portfolio
-- Synthetic dataset only. No real users, identifiers, or harmful content.
-- SQLite-compatible queries.

-- 1. Cross-case accounts
SELECT account_id,
       COUNT(DISTINCT case_id) AS case_count,
       GROUP_CONCAT(DISTINCT case_id) AS cases
FROM case_accounts
GROUP BY account_id
HAVING COUNT(DISTINCT case_id) > 1
ORDER BY case_count DESC;

-- 2. Shared infrastructure across cases
SELECT s.device_id,
       COUNT(DISTINCT e.case_id) AS case_count,
       GROUP_CONCAT(DISTINCT e.case_id) AS cases,
       COUNT(DISTINCT s.account_id) AS account_count
FROM sessions s
JOIN events e ON e.session_id = s.session_id
GROUP BY s.device_id
HAVING COUNT(DISTINCT e.case_id) > 1
ORDER BY case_count DESC, account_count DESC;

-- 3. Temporal bursts by case and hour
SELECT case_id,
       substr(timestamp,1,13) AS hour_bucket,
       COUNT(*) AS event_count
FROM events
GROUP BY case_id, hour_bucket
HAVING COUNT(*) >= 12
ORDER BY event_count DESC;

-- 4. Repeated target focus
SELECT case_id, target_id,
       COUNT(DISTINCT account_id) AS accounts,
       COUNT(*) AS events
FROM events
WHERE target_id <> ''
GROUP BY case_id, target_id
HAVING COUNT(DISTINCT account_id) >= 3
ORDER BY accounts DESC, events DESC;

-- 5. Template reuse across cases
SELECT content_hash,
       COUNT(DISTINCT case_id) AS case_count,
       GROUP_CONCAT(DISTINCT case_id) AS cases,
       COUNT(*) AS content_count
FROM content
GROUP BY content_hash
HAVING COUNT(DISTINCT case_id) > 1
ORDER BY case_count DESC, content_count DESC;

-- 6. Potential post-enforcement evasion
SELECT a.account_id, a.prior_enforcement,
       COUNT(DISTINCT s.device_id) AS device_count,
       COUNT(DISTINCT ca.case_id) AS case_count,
       GROUP_CONCAT(DISTINCT ca.case_id) AS cases
FROM accounts a
JOIN sessions s ON s.account_id=a.account_id
JOIN case_accounts ca ON ca.account_id=a.account_id
WHERE a.prior_enforcement='Yes'
GROUP BY a.account_id, a.prior_enforcement
ORDER BY case_count DESC, device_count DESC;

-- 7. Role differentiation inside coordinated networks
SELECT ca.case_id, a.role, COUNT(*) AS account_count
FROM case_accounts ca
JOIN accounts a ON a.account_id=ca.account_id
GROUP BY ca.case_id, a.role
ORDER BY ca.case_id, account_count DESC;

-- 8. Critical-case triage metrics
SELECT r.case_id,
       MIN(CAST(r.triage_minutes AS INTEGER)) AS fastest_triage,
       ROUND(AVG(CAST(r.triage_minutes AS REAL)),1) AS avg_triage,
       COUNT(*) AS action_count
FROM reports_enforcement r
JOIN cases c ON c.case_id=r.case_id
WHERE c.severity='Critical'
GROUP BY r.case_id
ORDER BY avg_triage;

-- 9. False-positive control comparison
SELECT e.case_id,
       ROUND(AVG(CAST(e.raw_risk_score AS REAL)),3) AS avg_risk,
       COUNT(*) AS event_count,
       c.ground_truth_label
FROM events e
JOIN cases c ON c.case_id=e.case_id
WHERE e.case_id IN ('C-005','C-007','C-010')
GROUP BY e.case_id, c.ground_truth_label
ORDER BY avg_risk DESC;

-- 10. Cross-case graph edge list
SELECT case_id_a AS source_case,
       case_id_b AS target_case,
       link_type,
       CAST(strength AS REAL) AS strength,
       CAST(evidence_count AS INTEGER) AS evidence_count,
       analyst_confidence
FROM case_links
ORDER BY strength DESC;
