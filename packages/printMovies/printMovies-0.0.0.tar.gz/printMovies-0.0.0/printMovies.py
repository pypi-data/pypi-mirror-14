def printMovies(movies) :
	for movie in movies :
		if isinstance (movie, list) :
			printMovies(movie)
		else :
			print (movie)
