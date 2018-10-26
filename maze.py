from math import inf

class Maze:
    def __init__(self, im):
        width, height = im.size
        self.node_count = 0

        # Find starting node
        for x in range(width):
            if im.getpixel((x, 0)):
                self.start_node = self.Node(x, 0)
                break
        
        # Find end node
        for x in range(width):
            if im.getpixel((x, height - 1)):
                self.end_node = self.Node(x, height - 1)
                break

        # Maintain a record of the reachable nodes in rows above
        nodes_above = [None] * width
        nodes_above[self.start_node.x] = self.start_node

        # Iterate through pixels in image
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Current pixel not wall
                if im.getpixel((x, y)):
                    # Left pixel==wall
                    if not im.getpixel((x - 1, y)):
                        # Wall on the left <=> no neighbors to the right of last_node
                        last_node = None

                        # The only scenario without node is 
                        # up==path and down==path and right==wall
                        if not(im.getpixel((x, y - 1)) and 
                                im.getpixel((x, y + 1)) and 
                                not im.getpixel((x + 1, y))):
                            new_node = self.Node(x, y)
                                
                            # If up==path, set neighbors
                            if im.getpixel((x, y - 1)):
                                nodes_above[x].add_neighbor(new_node)
                                new_node.add_neighbor(nodes_above[x])

                            nodes_above[x] = new_node
                            last_node = new_node

                    # Left pixel==path
                    else:
                        # The only scenario without node is 
                        # up==wall, down==wall, right==path
                        if not(not im.getpixel((x, y - 1)) and 
                                not im.getpixel((x, y + 1)) and 
                                im.getpixel((x + 1, y))):
                            new_node = self.Node(x, y)

                            # If up==path, set neighbors
                            if im.getpixel((x, y - 1)):
                                nodes_above[x].add_neighbor(new_node)
                                new_node.add_neighbor(nodes_above[x])

                            # new_node must be neighbor to last_node because left==path
                            last_node.add_neighbor(new_node)
                            new_node.add_neighbor(last_node)

                            nodes_above[x] = new_node
                            last_node = new_node

                # Current pixel==wall
                else:
                    nodes_above[x] = None

        # Connect end_node
        self.end_node.add_neighbor(nodes_above[self.end_node.x])
        nodes_above[self.end_node.x].add_neighbor(self.end_node)

    class Node:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.neighbors = []
            return

        def distance(self, other):
            if other in self.neighbors:
                return abs(self.x - other.x) + abs(self.y - other.y)
            else:
                return inf
        
        def add_neighbor(self, other):
            self.neighbors.append(other)

        def __repr__(self):
            return str((self.x, self.y))

        # For use in dicts and heaps
        def __hash__(self):
            return hash((self.x, self.y))

        # # These methods are needed in order to use nodes in heaps.
        def __eq__(self, other):
            return self.x == other.x

        def __lt__(self, other):
            return self.x < other.x

        def __le__(self, other):
            return self.x <= other.x

        def __gt__(self, other):
            return self.x > other.x

        def __ge__(self, other):
            return self.x >= other.x