Select r.id,r.name
FROM rooms r LEFT JOIN students s
ON r.id=s.room
GROUP BY r.id,r.name
ORDER BY AVG(AGE(s.birthday))
LIMIT 5