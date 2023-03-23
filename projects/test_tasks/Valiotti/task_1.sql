SELECT city FROM city_population
WHERE population = (SELECT MIN(population) FROM city_population);