class Solution_image:
    def __init__(self, im, sol, filename, draw_depth=False):
        # Output a solved image
        im = im.convert("RGB")
        pixels = im.load()

        if draw_depth:
            self.__draw_depth(sol, pixels)

        self.__draw_sol(sol, pixels)
        im.save("maze_solutions/" + filename)

    def __draw_depth(self, sol, pixels):
        # Color all dead end routes
        def color(progress, path_dist): 
            r = int(255*(progress/path_dist))
            g = int(255*(1 - progress/path_dist))
            b = 0
            return (r, g, b)

        for path in sol.dead_ends.values():
            progress = 0
            for i in range(len(path) - 1):
                this_node = path[i]
                next_node = path[i + 1]

                for x in range(this_node.x, next_node.x, -1 if this_node.x > next_node.x else 1):
                    pixels[x, this_node.y] = color(progress, sol.longest_path_dist)
                    progress += 1

                for y in range(this_node.y, next_node.y, -1 if this_node.y > next_node.y else 1):
                    pixels[this_node.x, y] = color(progress, sol.longest_path_dist)
                    progress += 1

        pixels[path[-1].x, path[-1].y] = color(progress, sol.shortest_path_dist)

    def __draw_sol(self, sol, pixels):
        # Paints shortest path solution
        progress = 0
        color = (0, 0, 255)
        for i in range(len(sol.shortest_path) - 1):
            this_node = sol.shortest_path[i]
            next_node = sol.shortest_path[i + 1]

            for x in range(this_node.x, next_node.x, -1 if this_node.x > next_node.x else 1):
                pixels[x, this_node.y] = color
                progress += 1

            for y in range(this_node.y, next_node.y, -1 if this_node.y > next_node.y else 1):
                pixels[this_node.x, y] = color
                progress += 1

        pixels[sol.shortest_path[-1].x, sol.shortest_path[-1].y] = color