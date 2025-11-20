class Graph:
    def __init__(self):
        #nodes contain all roads from themself
        self.nodes = {}
        self.places = {}
    
    def add_node(self, nodeID):
        self.nodes.update({nodeID: {}})

    def add_edge(self, ID1, ID2, weight):
        if ID1 in self.nodes:
            self.nodes[ID1].update({ID2: weight})
        else:
            self.add_node(ID1)
            self.nodes[ID1].update({ID2: weight})
        
        if ID2 in self.nodes:
            self.nodes[ID2].update({ID1: weight})
        else:
            self.add_node(ID2)
            self.nodes[ID2].update({ID1: weight})

    #TODO: write tests to check graph is populated correctly
    def gen(self, placesFile, roadsFile):
        """
        method to read data into graph
        Input: Places, Roads
        Returns: None, populates nodes
        """

        with open(placesFile, 'r') as file:
            for line in file:
                line = line.strip()
                values = line.split(',')
                self.places.update({values[0]: values[1]})
                self.add_node(values[0])      

        with open(roadsFile, 'r') as file:
            for line in file:
                line = line.strip()
                values = line.split(",")
                self.add_edge(values[0], values[1], values[2])
    
    #TODO: implement Dijsktras
    def getPath(self, srcName, destName):
        print("null")
                
    

def main():
    print("boob")
    graph = Graph()
    graph.gen("USRoads/Place.txt", "USRoads/Road.txt")
    print(graph.nodes.get('396'))


if __name__ == "__main__":
    main()