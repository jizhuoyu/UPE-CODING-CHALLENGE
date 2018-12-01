import requests
width = 0
height = 0
token = ""
mazeMap = []
baseURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"


def getToken():
    UIDdata = {"uid": "204997291"}
    tokenReceived = requests.post(baseURL + "/session", data=UIDdata).json()
    return tokenReceived["token"]


def getStatus(token):
    return requests.get(baseURL + "/game?token=" + token).json()


def main():
    global width, height, token, mazeMap
    for i in range(5):
        token = getToken()
        statusReceived = getStatus(token)
        startPoint = statusReceived["current_location"]
        width = statusReceived["maze_size"][0]
        height = statusReceived["maze_size"][1]
        mazeMap = [[" "] * width for _ in range(height)]
        mazeMap[startPoint[1]][startPoint[0]] = "."
        mazeHelper([startPoint[0], startPoint[1]])
    statusReceived = getStatus(token)
    print("status is:", statusReceived["status"])


def outOfBounds(point):
    if (point[0] < 0 or point[0] >= width) or (point[1] < 0 or point[1] >= height):
        return True
    return False


def isDiscoveredOrWall(point):
    global mazeMap
    xcol, ycol = point[0], point[1]
    return mazeMap[ycol][xcol] is "W" or mazeMap[ycol][xcol] is "."


def reverseDirection(original):
    if original is "UP":
        return "DOWN"
    if original is "DOWN":
        return "UP"
    if original is "LEFT":
        return "RIGHT"
    if original is "RIGHT":
        return "LEFT"


def updatedCoordinate(currPoint, dir):
    if dir is "UP":
        return [currPoint[0], currPoint[1]-1]
    if dir is "DOWN":
        return [currPoint[0], currPoint[1]+1]
    if dir is "LEFT":
        return [currPoint[0]-1, currPoint[1]]
    if dir is "RIGHT":
        return [currPoint[0]+1, currPoint[1]]


def mazeHelper(currPoint):
    global width, height, token, mazeMap
    for dir in ["UP", "DOWN", "LEFT", "RIGHT"]:
        newPoint = updatedCoordinate(currPoint, dir)
        if (not outOfBounds(newPoint)) and (not isDiscoveredOrWall(newPoint)):
            result = requests.post(baseURL + "/game?token=" + token, data={"action": dir}).json()
            value = result["result"]
            if value == "WALL":
                mazeMap[newPoint[1]][newPoint[0]] = "W"
            elif value == "END":
                return True
            elif value == "SUCCESS":
                mazeMap[newPoint[1]][newPoint[0]] = "."
                if mazeHelper(newPoint):
                    return True
                else:
                    requests.post(baseURL + "/game?token=" + token, data={"action": reverseDirection(dir)})
    return False


if __name__ == "__main__":
    main()