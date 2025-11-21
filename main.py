import random
import sys
import heapq

class Graph:
    def __init__(self):
        #nodes contain all roads from themselves
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
                self.places.update({values[1]: values[0]})     

        with open(roadsFile, 'r') as file:
            for line in file:
                line = line.strip()
                values = line.split(",")
                #weight multiplied by 100 so it can be int
                self.add_edge(float(values[0]), float(values[1]), float(values[2]))

    #TODO: implement Dijsktras
    def getPath(self, srcName, destName):
        srcID = int(self.places.get(srcName))
        destID = int(self.places.get(destName))

        pq = []
        dist = [sys.maxsize] * len(self.nodes)
        parent = {node: None for node in self.nodes}
        
        dist[self.getIndex(srcID)] = 0
        heapq.heappush(pq, (0, srcID))

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue

            for v, w in self.nodes.get(u).items():
                new_dist = dist[self.getIndex(u)] + w
                if new_dist < dist[int(v)]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))
        
        path = []
        node = destID
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()

        return path, dist, parent

        """
        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue

            print(self.nodes.get(u))
            for v, w in self.nodes.get(u).items():
                if dist[u] + float(w) < dist[self.getIndex(v)]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        print(dist[5])
        """

    
    def getIndex(self, target):
        """
        input: node ID
        return: index of node in places and dist
        """
        index = 0
        for ID in self.nodes:
            if target == int(ID):
                return index
            index+=1



        




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
                self.roadList.append([float(values[0]), float(values[1]), float(values[2])])

    def ranRouteCheck(self, n=5):
        """
        Randomly selects 5 roads from the roadlist and test
        that the route is present on the src node
        Returns count of road misses
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
    test = UnitTest("USRoads/Place.txt", "USRoads/Road.txt")
    print("Graph gen errors: " + str(test.ranRouteCheck(5)))

    graph = Graph()
    graph.gen("USRoads/Place.txt", "USRoads/Road.txt")
    path, dist, parent = graph.getPath("ALBRIDGEPORT", "MDWASHINGTON GROVE")

    print("Path:", path)
    print("Detailed steps:")
    total = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        w = graph[u][v]
        print(f"{u} -> {v} (weight {w})")
        total += w

    print("Total distance:", total)


if __name__ == "__main__":
    main()