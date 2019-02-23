import graphviz
import json
import os
import time
import copy
import numpy
import heapq 
class Node:
    def __init__(self,name,value ):
        self.name = name
        self.value =value

    def __lt__(self, other):
        if isinstance(other,Node):
            return self.value < other.value
        if isinstance(other,(int,float)):
            return self.value < other

    def __le__(self, other):
        if isinstance(other,Node):
            return self.value <= other.value
        if isinstance(other,(int,float)):
            return self.value <= other

class Graph :

    _title = "Mapa da Romênia simplificado"

    def __init__(self, fileName):
        graph_json = json.load(open(fileName)) 

        self._straight_line_distance = graph_json["straight_line_distance"]
        self._graph = graphviz.Graph(self._title)
        self._createTable(graph_json["edges"])
        self._nodes = graph_json["nodes"]
        self._edges = graph_json["edges"]

    def _createTable(self,edges):

        self._table = {}


        for edge in  edges:
            self._addTable(edge["origin"]["name"],{edge["target"]["name"]:edge["weight"]})
            self._addTable(edge["target"]["name"],{edge["origin"]["name"]:edge["weight"]})

    def _addTable(self,name,weight):
        try:
            self._table[name].update(weight)
            
        except:
            self._table[name] = {}
            self._table[name].update(weight)

    def changeNodeColor(self,node_name,new_color):
        self._graph.attr("node",color=new_color) 

        self._graph.node(node_name)

        self._graph.attr("node",color="")

        pass

    def _edgesToDOT(self):
         
         table = copy.deepcopy(self._table)
        

         for node in list(table.keys()):
            for neighbor in list(table[node].keys()):
                self._graph.edge(node,neighbor,label=str(table[node][neighbor]) )
                del table[neighbor][node]

    def _nodesToDOT(self):
        
         for node in list(self._table.keys()):
              self._graph.node(node)

    def _starPathToDOT(self):
        with self._graph.subgraph(name="cluster0") as star_graph:
            star_graph.attr(label="A* (A-Star) path\ncost %d"%self._star_cost  )
            for index in range(len(self._star_path) -1):
                star_graph.edge(" "+self._star_path[index]+" "," "+self._star_path[index+1]+" ")
        
    def _idsPathToDOT(self):
        with self._graph.subgraph(name="cluster1") as star_graph:
            star_graph.attr(label="Iterative Deepening Search path\ncost %d"%self._ids_cost  )
            for index in range(len(self._ids_path) -1):
                star_graph.edge("  "+self._ids_path[index]+"  ","  "+self._ids_path[index+1]+"  ")

    def _showHeuristic(self):
        label = ""
        for key in self._straight_line_distance:
            label+=key + " " + str(self._straight_line_distance[key]) + "\n"
         

        with  self._graph.subgraph(name="cluster2") as table:
          table.attr("node",shape="box",label="straight_line_distance:\n"+label)
          table.node("")  
          
    

    def print(self):
          
        self._graphToDOT()
        dot_file = self._graph.view(cleanup=True)
        time.sleep(1)
        os.remove(dot_file)
        self._graph.clear()

    def save(self):
        self._graphToDOT()
        self._graph.render(cleanup=True)

    def _addGraphvizAttribute(self):
        self._graph.attr(rankdir="LR",size="20")
        self._graph.attr(compound='true')
        self._graph.attr("node",shape="circle")

    def _graphToDOT(self):
        self._addGraphvizAttribute()
        self._nodesToDOT()
        self._edgesToDOT()
        self._starPathToDOT()
        self._idsPathToDOT()
        self._showHeuristic()


    def getCust(self,origin_node_name_a,target_node_name_b):
        return self._table[origin_node_name_a][target_node_name_b]

    def getNeighbors(self,node_name):
        return list(self._table[node_name].keys())
    
    def removeNode(self,node_name):
        neighbors = self.getNeighbors(node_name)

        for node in neighbors:
            del self._table[node][node_name]
        
        del self._table[node_name]

    def getLineDistance(self, node):
        return self._straight_line_distance[node]



# pseudocódigo retirado da wikipedia
# wikipedia: https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
    def iterativeDeepeningSearch(self,origin,goal_node,limit_max):
       
        for depth in range(limit_max):
            cost, remaining , path = self.depthLimitedSearch(origin,goal_node,depth,origin)
            if cost is not None:
                self._ids_path = path
                self._ids_cost = cost
                return path,cost
            elif not remaining:
                return None , []



    def depthLimitedSearch(self,node,goal_node,depth,father):
        if depth == 0: 
            # self.changeNodeColor(node,"red") # visualização
            if node == goal_node:
                return 0 , True , [node]

            else:
                return None ,True ,[] #( Not found, but may have children )
        
        elif depth > 0:
            any_remaining = False
            neighbors = self.getNeighbors(node)
            
            # permitir somente a Ida. De Pai para filho. Nunca filho não pode voltar para o pai
            if self.isChild(node,father):
                neighbors.remove(father)
                father = node

            for neighbor in neighbors:
                found , remaining , path = self.depthLimitedSearch(neighbor,goal_node,depth-1,father)
                if found is not None:
                    return found + self._table[node][neighbor],True , [node] + path
                if remaining:
                    any_remaining = True
                
            return None , any_remaining ,[]

    
    def isChild(self,father,child):
        try:
            self._table[father][child]
            return True
        except:
            return False
        

    def Astar(self,start,goal):

        open_set =  list()
        cameFrom = dict()

        closed_set ,gScore , fScore = self.initStar()
        
        heapq.heappush(open_set,Node(start,self.getLineDistance(start)))      

        gScore[start] = 0

        fScore[start] = self.getLineDistance(start)

       
        while open_set:
            current_node = self._nextNode(open_set,closed_set)
            if current_node is None:
                return None
            #para visualização
            # self.changeNodeColor(current_node,"Red")
            
            if current_node ==goal:
                self._star_cost = gScore[goal] # para visualização
                return self.reconstructPath(cameFrom,current_node) , gScore[goal]
            
            closed_set[current_node]= True

            for neighbor in self.getNeighbors(current_node):
                if closed_set[neighbor]:
                     continue
                tentative_gScore = gScore[current_node] + self.getCust(current_node,neighbor)

                
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current_node
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.getLineDistance(neighbor)

                # a arvore heap permite não chegar toda a lista open_set
                # pois mesmo adicionando mais de uma vezes o mesmo nó a
                # min heap vai voltar o nó com o menor custo e como é ve-
                # rificado se o nó foi fechado logo no começo do algoritmo.
                # É correto dizer que mesmo adicioanando o mesmo nó mais de
                # uma vez. Só será computado o que tiver o menor custo
                heapq.heappush(open_set,Node(neighbor,fScore[neighbor]) )

                
    def initStar(self):
        gScore     =  dict()
        fScore     = dict()
        closed_set = dict()

        for node in self._nodes:
            closed_set[node["name"]]= False
            gScore[node["name"]] = float("inf")
            fScore[node["name"]] = float("inf")

        return closed_set,gScore,fScore


    def reconstructPath(self, cameFrom,current_node):
        total_path = [current_node]
        while current_node in cameFrom.keys():
            current_node = cameFrom[current_node]
            total_path.append(current_node)

        total_path.reverse()
        self._star_path = total_path
        return total_path

    def _nextNode(self,open_set,closed_set):
        next_node = heapq.heappop(open_set)
        
        while closed_set[next_node.name]:
            if not open_set:
                return None
            next_node = heapq.heappop(open_set)

        return next_node.name
       