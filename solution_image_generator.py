class Solution_image:
    def __init__(self, im):
        # Output a solved image
        self.im = im.convert("RGB")
        self.pixels = self.im.load()

    def draw_depth(self, dead_ends, shortest_path_dist, longest_path_dist):
        # Color all dead end routes
        def color(progress, path_dist): 
            r = int(255*(progress/path_dist))
            g = int(255*(1 - progress/path_dist))
            b = 0
            return (r, g, b)

        for path in dead_ends.values():
            progress = 0
            for i in range(len(path) - 1):
                this_node = path[i]
                next_node = path[i + 1]

                for x in range(this_node.x, next_node.x, -1 if this_node.x > next_node.x else 1):
                    self.pixels[x, this_node.y] = color(progress, longest_path_dist)
                    progress += 1

                for y in range(this_node.y, next_node.y, -1 if this_node.y > next_node.y else 1):
                    self.pixels[this_node.x, y] = color(progress, longest_path_dist)
                    progress += 1

        self.pixels[path[-1].x, path[-1].y] = color(progress, shortest_path_dist)

    def draw_sol(self, path, color=(0, 0, 255)):
        # Paints shortest path solution
        progress = 0
        for i in range(len(path) - 1):
            this_node = path[i]
            next_node = path[i + 1]

            for x in range(this_node.x, next_node.x, -1 if this_node.x > next_node.x else 1):
                self.pixels[x, this_node.y] = color
                progress += 1

            for y in range(this_node.y, next_node.y, -1 if this_node.y > next_node.y else 1):
                self.pixels[this_node.x, y] = color
                progress += 1

        self.pixels[path[-1].x, path[-1].y] = color
    
    def save(self, filename):
        self.im.save("maze_solutions/" + filename)
        print("Image saved as maze_solutions/" + filename + "\n")