import random


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



class UnitTest:
    """
    Usage: Create Unittest Object, use methods to run test
    """
    def __init__(self, places, roads):
        """
        Makes a gens a graph object
        Generates a road list to test graph is populating correctly
        """
        self.graph = Graph()
        self.graph.gen(places, roads)
        self.roadList = []
        self.genRoadList(roads)

    def genRoadList(self, roads):
        """
        Populates road list with the complete set of routes
        """
        with open(roads, 'r') as file:
            for line in file:
                line = line.strip()
                values = line.split(",")
                self.roadList.append(values)

    def ranRouteCheck(self, n=5):
        """
        Randomly selects 5 roads from the roadlist and test
        that the route is present on the src node
        """
        count = 0
        err = 0
        while count < n:
            testID = random.randint(0, len(self.roadList))
            test = self.roadList[testID]
            src = self.graph.nodes.get(test[0])
            if (test[1] in src):
                if src.get(test[1]) != test[2]:
                    err+=1
            else:
                err+=1
            count+=1
        return err
        



def main():
    print("boob")
    test = UnitTest("USRoads/Place.txt", "USRoads/Road.txt")
    print("Graph gen errors: " + str(test.ranRouteCheck(5)))


if __name__ == "__main__":
    main()