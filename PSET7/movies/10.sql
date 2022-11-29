SELECT DISTINCT people.name
FROM movies, directors, ratings, people
WHERE movies.id = ratings.movie_id
AND ratings.rating >= 9
AND ratings.movie_id = directors.movie_id
AND directors.person_id = people.id;
