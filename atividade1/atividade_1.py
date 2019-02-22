from graph import Graph

if __name__ == "__main__":
    graph = Graph("graph.json")
    depth = 5
    total_cost = graph.iterativeDeepeningSearch("Arad","Bucharest",depth)
    graph.print()
    print("custo total",total_cost)
    
   