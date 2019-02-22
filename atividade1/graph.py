import graphviz
import json
import os
import time
import copy
from tree import Tree
class Graph :

    _title = "Mapa da Romênia simplificado"

    def __init__(self, fileName):
        graph_json = json.load(open(fileName)) 

        self._straight_line_distance = graph_json["straight_line_distance"]
        self._graph = graphviz.Graph(self._title)
        self._createTable(graph_json["edges"])

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
        self._graph.attr(rankdir="LR", size="15")
        self._graph.attr("node",shape="circle")

    def _graphToDOT(self):
        self._addGraphvizAttribute()
        self._nodesToDOT()
        self._edgesToDOT()


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
    def interativeDeepeningSearch(self,origin,goal_node,limit_max):
       
        for depth in range(limit_max):
            found, remaining = self.depthLimitedSearch(origin,goal_node,depth,origin)
            if found is not None:
                print("level",depth)
                return found
            elif not remaining:
                return None



    def depthLimitedSearch(self,node,goal_node,depth,father):
        if depth == 0: 
            self.changeNodeColor(node,"red") # visualização
            if node == goal_node:
                return 0 , True

            else:
                return None ,True #( Not found, but may have children )
        
        elif depth > 0:
            any_remaining = False
            neighbors = self.getNeighbors(node)
            
            try: # permitir somente a Ida. De Pai para filho. Nunca filho não pode voltar para o pai
                self._table[node][father]
                neighbors.remove(father)
                father = node
            except:
                pass
            
            for neighbor in neighbors:
                found , remaining = self.depthLimitedSearch(neighbor,goal_node,depth-1,father)
                if found is not None:
                    return found + self._table[node][neighbor],True
                if remaining:
                    any_remaining = True
                
            return None , any_remaining

    def Astar(self):
        pass
        