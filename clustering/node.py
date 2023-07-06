from __future__ import annotations
from typing import Dict, Optional


class Node:
    distance: float
    name: Optional[str]
    left_child: Optional[Node]
    right_child: Optional[Node]
    dictionary: Dict[str, int]

    def __init__(self, distance: float = 1, right_child: Optional[Node] = None, left_child: Optional[Node] = None, dictionary: Optional[Dict[str, int]] = None, name: Optional[str] = None):
        self.distance = distance
        self.name = name
        self.left_child = left_child
        self.right_child = right_child
        if dictionary is None and left_child is not None and right_child is not None:
            self.dictionary = self.fuse_dictionaries(left_child, right_child)
        else:
            if dictionary is not None:
                self.dictionary = dictionary
            else:
                self.dictionary = {}

    def fuse_dictionaries(self, left_child: Node, right_child: Node) -> Dict[str, int]:
        dictionary = left_child.dictionary
        for key, value in right_child.dictionary.items():
            if key not in dictionary.keys():
                dictionary[key] = value
            else:
                dictionary[key] += value
        return dictionary

    def add_left_child(self, node):
        if not isinstance(node, Node):
            raise ValueError('Left child must be an instance of Node class')
        self.left_child = node

    def add_right_child(self, node):
        if not isinstance(node, Node):
            raise ValueError('Right child must be an instance of Node class')
        self.right_child = node

    def print_leaf_nodes(self):
        if self.left_child is None and self.right_child is None:  # If this is a leaf node
            print(self.name.encode('utf-8', errors='replace').decode('utf-8'))
        if self.left_child is not None:  # If there's a left child, recursively print its leaf nodes
            self.left_child.print_leaf_nodes()
        if self.right_child is not None:  # If there's a right child, recursively print its leaf nodes
            self.right_child.print_leaf_nodes()