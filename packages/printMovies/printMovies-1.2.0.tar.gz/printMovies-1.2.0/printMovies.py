def printMovies(movies, level) :
        for movie in movies :
                if isinstance (movie, list) :
                        printMovies(movie, level + 1)
                else :
                        for num in range(level):
                                print("\t", end = "")
                        print(movie)
