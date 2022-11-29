SELECT ROUND(AVG(rating), 2)
FROM ratings, movies
WHERE movies.year = 2012
AND movies.id = ratings.movie_id;