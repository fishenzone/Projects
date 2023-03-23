SELECT
    DATE_FORMAT(user.installed_at, '%Y-%m') AS month,
    COUNT(DISTINCT user.user_id) AS total_users,
    COUNT(DISTINCT CASE WHEN DATEDIFF(client_session.created_at, user.installed_at) = 1 THEN user.user_id END) AS retention_1_day,
    COUNT(DISTINCT CASE WHEN DATEDIFF(client_session.created_at, user.installed_at) = 3 THEN user.user_id END) AS retention_3_day,
    COUNT(DISTINCT CASE WHEN DATEDIFF(client_session.created_at, user.installed_at) = 7 THEN user.user_id END) AS retention_7_day
FROM user
LEFT JOIN client_session ON user.user_id = client_session.user_id
WHERE user.installed_at >= '2022-01-01'
GROUP BY month;