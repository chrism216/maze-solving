from collections import defaultdict, deque
from math import inf
from sys import setrecursionlimit
from random import choice
import heapq



class Dijkstra:
    def __init__(self, source_node, end_node, early_exit=True, heuristic=None):
        # Use heuristic="astar" to use A* algorithm
        # Tracking variables
        self.shortest_paths_dist = {}
        self.shortest_paths_dist[source_node] = 0
        
        self.shortest_paths = {}
        self.shortest_paths[source_node] = [source_node]
        
        self.dead_ends = {}

        explored = set()
        explored.add(source_node)

        # Heuristic for astar algorithm
        heuristic_dist = lambda node: node.distance(end_node) if heuristic == "astar" else 0

        # Init heap with neighbors of source node
        heap = []
        for neighbor in source_node.neighbors:
            heapq.heappush(heap, 
                (heuristic_dist(neighbor) + source_node.distance(neighbor), 
                source_node.distance(neighbor), 
                source_node, 
                neighbor)
            )

        # Loop until heap is empty
        while heap:
            # Pop items from heap until an unexplored node is found
            while True:
                hdist, dist, head, tail = heapq.heappop(heap)
                if tail not in explored or not heap:
                    break
            
            # Book keeping
            self.shortest_paths_dist[tail] = dist
            self.shortest_paths[tail] = self.shortest_paths[head] + [tail]
            self.longest_path_dist = dist # Last popped item will be deepest dead-end node
            explored.add(tail)

            # Check if dead-end. Only useful if not exiting early. 
            # Dead ends useful for drawing maze depth
            if all(node in explored for node in tail.neighbors) and not early_exit:
                self.dead_ends[tail] = self.shortest_paths[tail]
            
            # Push neighboring nodes into heap
            for new_node in tail.neighbors:
                if new_node not in explored:
                    new_dist = dist + new_node.distance(tail)
                    heapq.heappush(heap, 
                        (heuristic_dist(new_node) + new_dist, 
                        new_dist, 
                        tail, 
                        new_node)
                    )

        self.shortest_path = self.shortest_paths[end_node]
        self.shortest_path_dist = self.shortest_paths_dist[end_node]


class Depth_first_search:
    def __init__(self, source_node, end_node, heuristic="greedy"):
        
        def choose_node(available_neighbors, heuristic="greedy"):
            # Greedy (default): add neighbor closest to end_node
            if heuristic == "greedy":
                min_dist, min_neighbor = inf, None
                for neighbor in available_neighbors:
                    dist = neighbor.distance(end_node)
                    if dist < min_dist:
                        min_dist, min_neighbor = dist, neighbor
                return min_neighbor

            # Random: add a random neighbor
            elif heuristic == "random":
                if available_neighbors:
                    return choice(available_neighbors)

            # Naive: choose first non-visited neighbor in list
            elif heuristic == "naive":
                return available_neighbors[0]
                
        visited = set([source_node])
        stack = deque([source_node])
        
        while stack:
            node = stack.pop()
            available_neighbors = [neighbor for neighbor in node.neighbors if neighbor not in visited]
            if available_neighbors:
                stack.append(node)
                new_node = choose_node(available_neighbors)
                stack.append(new_node)
                visited.add(new_node)

                if new_node is end_node:
                    self.path = list(stack)
                    break


        