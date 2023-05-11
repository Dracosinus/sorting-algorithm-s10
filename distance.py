#/usr/bin python3

import math

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
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
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

A = [1,2,3,4]
B = [2,3,4,5]

def euclid(a,b):
    """
    Returns euclidian distance between vectors a and b
    """
    euclid_dist = 0
    for i,_ in enumerate(a):     
        euclid_dist += (b[i]-a[i])**2
    return math.sqrt(euclid_dist)

#print(euclid(A,B))

def euclid_on_maps_normalized(map_a, map_b):
    """
    Returns euclidian distance between maps map_a and map_b
    """
    euclid_dist = 0
    for key in map_b.keys():
        if key in map_a:
            euclid_dist += (map_b[key]-map_a[key])**2
    return 1/(1+math.sqrt(euclid_dist))

def get_friends_map(a,distance_function):
    friends = {}
    for key in critics.keys():
        if key != a:
            friends.update({key:distance_function(critics[a],critics[key])})
    return friends

# print(friends_map('Lisa Rose',euclid_on_maps_normalized))

def rank_friends(a,distance_function):
    """
    rank friends 
    """
    friends_map = get_friends_map(a,distance_function)
    print('--------------------')
    print(f'Using {distance_function.__name__}, person {a} is close with')
    for i,key in enumerate(sorted(friends_map, key=friends_map.get, reverse=True)):
        print(f'  rank {i+1} : {key} with distance {friends_map[key]}')
    print('--------------------')

def pearson_on_maps(map_a, map_b):
    """
    pearson distance with maps
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
    else:
        numerator = common_films*sum_axb - sum_a*sum_b
        denominator = math.sqrt((common_films*sum_square_a - sum_a**2) * (common_films*sum_square_b - sum_b**2))
    return numerator/denominator
    
#print(pearson_on_maps(critics['Lisa Rose'],critics['Gene Seymour']))
rank_friends('Lisa Rose',pearson_on_maps)
rank_friends('Lisa Rose',euclid_on_maps_normalized)
