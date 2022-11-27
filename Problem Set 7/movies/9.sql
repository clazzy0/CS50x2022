SELECT DISTINCT people.name
FROM people, movies, stars
WHERE movies.year = "2004"
AND movies.id = stars.movie_id
AND stars.person_id = people.id
ORDER BY people.birth;