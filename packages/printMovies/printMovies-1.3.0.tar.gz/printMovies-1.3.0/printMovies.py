def printMovies(movies, inden = False, level = 0) :
        for movie in movies :
                if isinstance (movie, list) :
                        printMovies(movie, inden, level + 1)
                else :
                        if inden:
                                for num in range(level):
                                        print("\t", end = "")
                        print(movie)
