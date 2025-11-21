import random
import sys
import heapq

class Graph:
    def __init__(self):
        #nodes contain all roads from themselves
        self.nodes = {}
        self.places = {}
        self.placesByID = {}
    
    def add_node(self, nodeID):
        self.nodes.update({nodeID: {}})

    def add_edge(self, ID1, ID2, weight, desc):
        if ID1 not in self.nodes:
            self.nodes[ID1] = {}
        if ID2 not in self.nodes:
            self.nodes[ID2] = {}

        self.nodes[ID1][ID2] = (weight, desc)
        self.nodes[ID2][ID1] = (weight, desc)



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
                place_id = int(values[0])
                place_name = values[1]

                self.places[place_name] = place_id
                self.placesByID[place_id] = place_name    

        with open(roadsFile, 'r') as file:
            for line in file:
                line = line.strip()
                values = line.split(",")

                ID1 = int(values[0])
                ID2 = int(values[1])
                dist = float(values[2])
                desc = values[3] if len(values) > 3 else ""
                self.add_edge(ID1, ID2, dist, desc)

    def getPath(self, srcName, destName):
        srcID = int(self.places.get(srcName))
        destID = int(self.places.get(destName))

        # distance and parent dictionaries
        dist = {node: sys.maxsize for node in self.nodes}
        parent = {node: None for node in self.nodes}

        dist[srcID] = 0
        pq = [(0, srcID)]   # (distance, nodeID)

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue

            for v, (w, desc) in self.nodes[u].items():
                newdist = dist[u] + w
                if newdist < dist[v]:
                    dist[v] = newdist
                    parent[v] = u
                    heapq.heappush(pq, (newdist, v))

        if dist[destID] == sys.maxsize:
            return None, dist, parent

        # reconstruct path
        path = []
        node = destID
        while node is not None:
            path.append(node)
            node = parent[node]

        return list(reversed(path)), dist, parent


    def input(self):
        # loop until valid source is entered
        while True:
            src = input("Enter starting location: ").strip()
            if src in self.places:
                break
            print(f"Unknown place '{src}'. Try again.")

        # loop until valid destination is entered
        while True:
            dest = input("Enter destination location: ").strip()
            if dest in self.places:
                break
            print(f"Unknown place '{dest}'. Try again.")

        print("\nCalculating shortest path...\n")

        # run dijkstra
        path, dist, parent = self.getPath(src, dest)

        if path is None:
             print(f"No possible path exists between {src} and {dest}.")
             return None
        # print the path nicely
        print("Shortest Path:")
        total = 0

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]

            name_u = self.placesByID.get(u, f"Unnamed({u})")
            name_v = self.placesByID.get(v, f"Unnamed({v})")

            w, desc = self.nodes[u][v]
            if not desc:
                desc = "No description"

            print(f"{u} ({name_u}) -> {v} ({name_v}), {desc}, {w}")
            total += w

        print(f"\nTotal distance: {total}")
        print(f"Path (IDs): {path}\n")

        return path

#Depracated
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
                self.roadList.append([int(values[0]), int(values[1]), float(values[2])])

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
    graph.input()



if __name__ == "__main__":
    main()