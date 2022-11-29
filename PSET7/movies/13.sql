SELECT DISTINCT people.name
FROM people, stars, movies
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND movies.id IN
(SELECT movies.id
FROM movies, stars, people
WHERE people.name = "Kevin Bacon"
AND people.birth = 1958
AND people.id = stars.person_id
AND stars.movie_id = movies.id)
AND people.name != "Kevin Bacon";