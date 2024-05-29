Select r.id,r.name,COUNT(s.id) AS number_of_students
FROM rooms r LEFT JOIN students s
ON r.id=s.room
GROUP BY r.id,r.name
