from PIL import Image
from maze import Maze
import maze_solvers
import solution_image_generator
import time


def solve(filename):
    im = Image.open("maze_images/" + filename)

    t_total0 = time.time()
    # Generate Maze
    print("Generating maze...")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Done. Time elapsed:", t1 - t0, "\n")

    # Solve maze
    print("Solving maze...")
    t0 = time.time()
    sol = maze_solvers.Dijkstra(maze.start_node, maze.end_node)
    t1 = time.time()
    print("Done. Time elapsed:", t1 - t0, "\n")

    # Generate solution image
    print("Generating image...")
    t0 = time.time()
    solution_image_generator.Solution_image(im, sol, filename)
    t1 = time.time()
    print("Done. Time elapsed:", t1 - t0, "\n")

    t_total1 = time.time()
    print("Total time:", t_total1 - t_total0)

if __name__ == "__main__":
    # Keep in mind: Algorithms like Dijkstra are much more memory-intensive
    # than depth-first search. For really large mazes, RAM becomes an issue
    solve("braid200.png")