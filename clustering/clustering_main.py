#!/usr/bin/env python3

import math
from wiki_reader import FILE_DICTS
from typing import Dict, List
from node import Node
import json


def pearson_on_maps(map_a: Dict[str, int], map_b: Dict[str, int]) -> float:
    """computes pearson distance between the maps of two persons
    the higher the score the closer the person

    Args:
        map_a (hashmap str:int): frequency of each important word in article a
        map_b (hashmap str:int): frequency of each important word in article b

    Returns:
        float: the pearson distance, float between -1 and 1, 1 is closest
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
    if denominator == 0:
        return 0
    return numerator/denominator


def get_closest_members(node_list: List[Node]) -> Node:
    """get the two members of a node list with the closest distance

    Args:
        node_list (List[Node]):

    Returns:
        Node: a new Node formed with the two nodes it comes from as children
    """
    assert len(node_list) >= 2
    node_a: Node = node_list[0]
    node_b: Node = node_list[1]
    distance_ab = pearson_on_maps(
        node_a.dictionary, node_b.dictionary)
    closest_node = Node(
        distance=distance_ab, right_child=node_a, left_child=node_b)
    for node_a in node_list:
        for node_b in node_list:
            if node_a != node_b:
                distance_ab = pearson_on_maps(
                    node_a.dictionary, node_b.dictionary)
                if distance_ab > closest_node.distance:
                    closest_node = Node(
                        distance=distance_ab, right_child=node_a, left_child=node_b)
    return closest_node


def clustering_main() -> Node:
    node_list = []
    for file, dictonary in FILE_DICTS.items():
        node_list.append(Node(dictionary=dictonary, name=file))
    while len(node_list) > 1:
        closest_node = get_closest_members(node_list)
        node_list.remove(closest_node.right_child)
        node_list.remove(closest_node.left_child)
        node_list.append(closest_node)
    return node_list[0]

def node_to_dict(node):
    if node is None:
        return None

    if node.left_child is None and node.right_child is None:
        return {"name": node.name}
    else:
        return {
            "value": node.distance,
            "children": [node_to_dict(node.left_child), node_to_dict(node.right_child)]
        }

tree_dict = node_to_dict(clustering_main())

with open('tree.json', 'w') as f:
    json.dump(tree_dict, f, indent=2)

