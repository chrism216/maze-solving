from collections import defaultdict
from math import inf
import heapq


class Dijkstra:
    def __init__(self, source_node, end_node, early_exit = True):
        # Tracking variables
        self.shortest_paths_dist = {}
        self.shortest_paths_dist[source_node] = 0
        
        self.shortest_paths = {}
        self.shortest_paths[source_node] = [source_node]
        
        self.dead_ends = {}

        explored = set()
        explored.add(source_node)

        # Init heap with neighbors of source node
        heap = []
        for tail in source_node.neighbors:
            heapq.heappush(heap, (source_node.distance(tail), source_node, tail))

        # Loop until heap is empty
        while heap:
            # Pop items from heap until an unexplored node is found
            while True:
                dist, head, tail = heapq.heappop(heap)
                if tail not in explored or not heap:
                    break
            
            # Book keeping
            self.shortest_paths_dist[tail] = dist
            self.shortest_paths[tail] = self.shortest_paths[head] + [tail]
            self.longest_path_dist = dist # Last popped item will be deepest dead-end node
            explored.add(tail)

            # Check if dead-end
            if all(node in explored for node in tail.neighbors):
                self.dead_ends[tail] = self.shortest_paths[tail]
            
            # Push neighboring nodes into heap
            for new_node in tail.neighbors:
                if new_node not in explored:
                    new_dist = dist + new_node.distance(tail)
                    heapq.heappush(heap, (new_dist, tail, new_node))

        self.shortest_path = self.shortest_paths[end_node]
        self.shortest_path_dist = self.shortest_paths_dist[end_node]
