Select r.id,r.name
FROM rooms r LEFT JOIN students s
ON r.id=s.room
GROUP BY r.id,r.name
HAVING COUNT(DISTINCT s.sex)=2
