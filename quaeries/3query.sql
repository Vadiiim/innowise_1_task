Select r.id,r.name
FROM rooms r LEFT JOIN students s
ON r.id=s.room
GROUP BY r.id,r.name
ORDER BY MAX(AGE(s.birthday))-MIN(AGE(s.birthday)) DESC
LIMIT 5
