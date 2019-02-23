from graph import Graph

if __name__ == "__main__":
    graph = Graph("graph.json")
    depth = 5
    ids_path,ids_cost = graph.iterativeDeepeningSearch("Arad","Bucharest",depth)
    star_path, star_cost = graph.Astar("Arad","Bucharest")

    print("IDS path",ids_path)
    print("IDS cost",ids_cost)
    print("A* path",star_path)
    print("A* cost",star_cost)
    graph.print()