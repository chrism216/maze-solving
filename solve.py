from PIL import Image
from maze import Maze
import maze_solvers
from solution_image_generator import *
import time


def solve(filename, draw_depth=True, solution_algorithm="depth_first_search"):
    im = Image.open("maze_images/" + filename)
    sol_image = Solution_image(im)
    
    t_total0 = time.time()

    # Generate Maze
    print("Generating maze...")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Done. Time elapsed:", t1 - t0, "\n")

    if draw_depth:
        t0 = time.time()
        print("Calculating maze Depth (Dijkstra)...")
        sol_dij = maze_solvers.Dijkstra(maze.start_node, maze.end_node, early_exit=False, heuristic="astar")
        sol_image.draw_depth(sol_dij.dead_ends, sol_dij.shortest_path_dist, sol_dij.longest_path_dist)
        t1 = time.time()
        if solution_algorithm != "dijkstra":
            del sol_dij
        t1 = time.time()
        print("Done. Time elapsed:", t1 - t0, "\n")

    
    t0 = time.time()
    if solution_algorithm == "depth_first_search":
        print("Solving maze (DFS)...")
        sol_dfs = maze_solvers.Depth_first_search(maze.start_node, maze.end_node, heuristic="greedy")
        sol_image.draw_sol(sol_dfs.path)

    elif solution_algorithm == "dijkstra":
        print("Solving maze (Dijkstra)...")
        sol_image.draw_sol(sol_dij.path)

    t1 = time.time()
    print("Done. Time elapsed:", t1 - t0, "\n")
    
    sol_image.save(filename)

    t_total1 = time.time()
    print("Total time:", t_total1 - t_total0)

if __name__ == "__main__":
    solve("braid200.png", draw_depth=True, solution_algorithm="depth_first_search")
    # Careful with drawing depth on larger images. You could very quickly run out of RAM.