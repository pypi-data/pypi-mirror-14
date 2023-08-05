import distance

from subfind.movie import MovieScoring


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


class MovieScoringAlice(MovieScoring):
    def sort(self, params, movies):
        query = params['title_query']

        for movie in movies:
            movie['d'] = distance.levenshtein(query, movie['title'].lower()),

        def movie_cmp(a, b):
            if a['d'] < b['d']:
                # smaller distances is better
                return -1
            elif a['d'] > b['d']:
                return 1

            if a['year'] > b['year']:
                # larger year is better
                return -1
            elif a['year'] < b['year']:
                return 1

            return 0

        movies.sort(key=cmp_to_key(movie_cmp))
