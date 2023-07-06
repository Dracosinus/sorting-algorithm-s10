# /usr/bin python3

import math

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


def euclid_on_maps_normalized(map_a, map_b):
    """computes euclidian distance normalized between the maps of two persons
    the higher the score the closer the person

    Args:
        map_a (hashmap movie:notes): the score given by a to each movie
        map_b (hashmap movie:notes): the score given by b to each movie

    Returns:
        float: the euclidian distance normalized, float between 0 and 1
    """
    euclid_dist = 0
    for key in map_b.keys():
        if key in map_a:
            euclid_dist += (map_b[key]-map_a[key])**2
    return 1/(1+math.sqrt(euclid_dist))


def get_friends_map(person, distance_function):
    """get friends map 

    Args:
        person (string): the person you want to know similarities with
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two persons

    Returns:
        hashmap person:float : distance with each other persons in the critics
    """
    friends = {}
    for iter_person, movies_notes in critics.items():
        if iter_person != person:
            friends.update({iter_person: distance_function(
                critics[person], movies_notes)})
    return friends


def rank_friends(person, distance_function):
    """pretty print ranking with the other people in the critics order by their similarities with person

    Args:
        person (string): the person you want to know similarities with
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two persons
    """
    friends_map = get_friends_map(person, distance_function)
    print('--------------------')
    print(f'Using {distance_function.__name__}, person {person} is close to')
    for i, key in enumerate(sorted(friends_map, key=friends_map.get, reverse=True)):
        print(f'  rank {i+1} : {key} with distance {friends_map[key]}')
    print('--------------------')


def pearson_on_maps(map_a, map_b):
    """computes pearson distance between the maps of two persons
    the higher the score the closer the person

    Args:
        map_a (hashmap movie:notes): the score given by a to each movie
        map_b (hashmap movie:notes): the score given by b to each movie

    Returns:
        float: the pearson distance, float between -1 and 1
    """
    common_films = sum_a = sum_b = sum_axb = sum_square_a = sum_square_b = 0
    for key in map_b.keys():
        if key in map_a:
            sum_a += map_a[key]
            sum_b += map_b[key]
            sum_axb += map_a[key]*map_b[key]
            sum_square_a += map_a[key]**2
            sum_square_b += map_b[key]**2
            common_films += 1
    if common_films == 0:
        return 0
    numerator = common_films*sum_axb - sum_a*sum_b
    denominator = math.sqrt(
        (common_films*sum_square_a - sum_a**2) * (common_films*sum_square_b - sum_b**2))
    return numerator/denominator


def get_all_films():
    """retrieves all films from the critics
    """
    all_films = []
    for person in critics.values():
        for film in person.keys():
            if not all_films.__contains__(film):
                all_films.append(film)
    return all_films


def get_all_film_unwatched_by(person):
    """retrieves all films the person has not watched

    Args:
        person (string): a key of the critics
    """
    films = get_all_films()
    for film in critics[person].keys():
        films.remove(film)
    return films


def get_recommandation(friend_map, movie):
    """recommends a movie to someone

    Args:
        friend_map (hashmap person : similarity): friend_map of a given person
        movie (string): a movie that person has not watched

    Returns:
        float: recommendation
    """
    sim_sum = sx_sum = 0
    for person in friend_map.keys():
        if critics[person].keys().__contains__(movie) and friend_map[person] >= 0:
            # print(f'person {person} with sim {friend_map[person]} gave note {critics[person][movie]} to {movie}')
            sim_sum += friend_map[person]
            sx_sum += friend_map[person]*critics[person][movie]
    return sx_sum/sim_sum


def get_recommandation_map(person, distance_function):
    """generates a map made of the unwatched movies and recommandations of somebody

    Args:
        person (string): the person you want to recommend a movie to
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two persons

    Returns:
        hashmap movie:recommandation_score
    """
    unwatched_films = get_all_film_unwatched_by(person)
    friend_map = get_friends_map(person, distance_function)
    recommandation_map = {}
    for film in unwatched_films:
        recommandation_map.update({film: get_recommandation(friend_map, film)})
    return recommandation_map


def rank_movies(person, distance_function):
    """pretty prints the recommandation map 

    Args:
        person (string): the person you want to recommend a movie to
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two persons
    """
    recommandation_map = get_recommandation_map(person, distance_function)
    print('--------------------')
    print(
        f'Using {distance_function.__name__}, person {person} may like to watch')
    for i, key in enumerate(sorted(recommandation_map, key=recommandation_map.get, reverse=True)):
        print(
            f'  rank {i+1} : {key} with recommandation {recommandation_map[key]}')
    print('--------------------')


rank_friends('Toby', pearson_on_maps)
rank_movies('Toby', pearson_on_maps)
rank_friends('Toby', euclid_on_maps_normalized)
rank_movies('Toby', euclid_on_maps_normalized)


films_critics: dict = {}
for person, ratings in critics.items():
    for film, rating in ratings.items():
        if film not in films_critics:
            films_critics[film] = {}
        films_critics[film][person] = rating


def get_movies_map(movie, distance_function):
    """get movies map 

    Args:
        movie (string): the movie you want to know similarities with
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two movies

    Returns:
        hashmap movie:float : distance with each other movies in the critics
    """
    similar_movies = {}
    for iter_movie, person_notes in films_critics.items():
        if iter_movie != movie:
            similar_movies.update({iter_movie: distance_function(
                films_critics[movie], person_notes)})
    return similar_movies


def compare_movies(movie, distance_function):
    """pretty print ranking movies by similarities found by persons liking them

    Args:
        movie (string): the movie you want to know similarities with
        distance_function (function hashmap,hashmap): the function you use to compute the distance between the maps of two movies
    """
    friends_map = get_movies_map(movie, distance_function)
    print('--------------------')
    print(f'Using {distance_function.__name__}, movie {movie} is close to')
    for i, key in enumerate(sorted(friends_map, key=friends_map.get, reverse=True)):
        print(f'  rank {i+1} : {key} with distance {friends_map[key]}')
    print('--------------------')


compare_movies('Superman Returns', euclid_on_maps_normalized)
compare_movies('Superman Returns', pearson_on_maps)
