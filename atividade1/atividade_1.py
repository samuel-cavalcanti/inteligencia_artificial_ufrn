from graph import Graph

if __name__ == "__main__":
    graph = Graph("graph.json")
    depth = 5
    total_cost = graph.interativeDeepeningSearch("Arad","Craiova",depth)
    graph.print()
    print(total_cost)
    
   