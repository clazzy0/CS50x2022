SELECT movies.title
FROM movies, stars, people
WHERE people.name = "Johnny Depp"
AND people.id = stars.person_id
AND stars.movie_id = movies.id
INTERSECT
SELECT movies.title
FROM movies, stars, people
WHERE people.name = "Helena Bonham Carter"
AND people.id = stars.person_id
AND stars.movie_id = movies.id;