import heapq as hq
import matplotlib.pyplot as plt


class Node:
    def __init__(self, x=None, y=None, z=None, g=None, h=None, p=None):
        self.x = x
        self.y = y
        self.z = z
        self.gCost = g
        self.hCost = h
        self.previousNode = p

    def getfCost(self):
        if self.gCost is not None and self.hCost is not None:
            return self.gCost + self.hCost
        else:
            return None

    def __str__(self) -> str:
        return "("+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'

    def isWithin(self, limits): #[xMin, xMax, yMin, yMax, zMin, zMax]
        if len(limits) == 6:
            return limits[0] < self.x < limits[1] and limits[2] < self.y < limits[3] and limits[4] < self.z < limits[5]  
        else:
            return None

    def __eq__(self, other: object) -> bool:
        return other is not None and (self.x == other.x and self.y == other.y and self.z == other.z)

    def __hash__(self) -> int:
        return hash(self.x, self.y, self.z)

    def __lt__(self, other: object) -> bool:
        return self.getfCost() < other.getfCost() or (self.getfCost() == other.getfCost() and self.hCost < other.hCost)


def dist(node1: Node, node2: Node):
    return ((node2.x-node1.x)**2 + (node2.y-node1.y)**2 + (node2.z-node1.z)**2) ** (1/2)


def getNeighbours(node: Node, obstacles, limits, closedList) -> list:
    result = []
    invalidNodes = obstacles + closedList + [node]
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                new = Node(x + node.x, y + node.y, z + node.z)
                if new not in invalidNodes and new.isWithin(limits):
                    result.append(new)
    
    return result


def aStar(start: Node, end: Node, obstacles: list, limits: list = [-30, 30, -30, 30, -30, 30]):
    start.hCost = dist(start, end)
    if not (start.isWithin(limits) and end.isWithin(limits) and all([i.isWithin(limits) for i in obstacles])):
        print("one or more nodes outside bounds")
        return None
    else:
        openList = []
        closedList = []
        hq.heappush(openList, start)

        while len(openList) > 0:
            currentNode = hq.heappop(openList)
            closedList.append(currentNode)

            if currentNode == end:
                return currentNode

            for neighbour in getNeighbours(currentNode, obstacles, limits, closedList):
                newMoveCost = currentNode.gCost + dist(currentNode, neighbour)

                neighbour.gCost = newMoveCost
                neighbour.hCost = dist(neighbour, end)
                neighbour.previousNode = currentNode

                hq.heappush(openList, neighbour)

    return start


def retrace(node: Node):
    print(f"Total cost: {node.getfCost()}")
    current = node
    result_x = []
    result_y = []
    result_z = []
    while current is not None:
        result_x.append(current.x)
        result_y.append(current.y)
        result_z.append(current.z)
        current = current.previousNode

    return result_x, result_y, result_z


def plot(start, end, obs):
    x, y, z = retrace(aStar(start, end, obs))
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(end.x, end.y, end.z, marker="*", color="red", s=100)
    ax.scatter3D(start.x, start.y, start.z, marker="*", color="blue", s=100)

    for ob in obs:
        ax.scatter3D(ob.x, ob.y, ob.z, marker="x", color="black", s=100)

    ax.plot3D(x, y, z, color="pink")
    plt.show()


if __name__ == "__main__":
    start = Node(0, -4, 0, 0)
    end = Node(-3, 4, 0)
    obstacles = [Node(5, 5, 5), Node(7, 8, 9), Node(-2, 1, 0), Node(-3, 1, 0), Node(-3, 3, 0), Node(-2, 3, 0), Node(-2, 4, 0)]
    plot(start, end, obstacles)
