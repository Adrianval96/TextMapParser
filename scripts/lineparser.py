import utils
import re
from room import Room

simpleWallPattern = re.compile("([\|])")
lowerWallPattern = re.compile(r"[\+\-*\+]+")
multipleLowerWallPattern = re.compile("\+\-*\+\-*\+")

class LineParser:
    def __init__(self):
        self.last_line = ""
        self.in_house_rooms = []
        # Only rooms being parsed
        self.open_rooms = []
        self.enqueued_rooms = []

        self.room_count = 0
        self.lineLimit = 50

        self.lines_in_file = utils.file_len("maps/rooms.txt")

    def getInHouseRooms(self):
        return self.in_house_rooms

    def getLastLine(self):
        return self.last_line

    def setLastLine(self, line):
        self.last_line = line

    def getOpenRooms(self):
        return self.open_rooms

    def getEnqueuedRooms(self):
        return self.enqueued_rooms

    def getRoomCount(self):
        return self.room_count

    def getLineLimit(self):
        return self.lineLimit

    def add_in_house(self, room):
        self.in_house_rooms.append(room)

    def add_open(self, room):
        self.open_rooms.append(room)

    def addToQueue(self, room):
        self.enqueued_rooms.append(room)

    def resetQueue(self):
        self.enqueued_rooms = []

    def addRoomToLists(self, room):
        self.add_in_house(room)
        self.add_open(room)
        self.room_count += 1

    def removeFromOpenRooms(self, room):
        room.setParseFinish()
        self.open_rooms.remove(room)

    def newRoom(self, lb, rb):
        return Room(lb, rb)

    def createNewRoom(self, lb, rb):
        self.addRoomToLists(Room.newRoom(lb, rb))

    def liberateQueue(self, currentLine):
        for room in self.enqueued_rooms:

            wallPositions = []
            for match in re.finditer(simpleWallPattern, currentLine):
                wallPositions.append(match.start())

            # Case 1. Walls fit and room is created.
            if room.getLeftWall() in wallPositions and room.getRightWall() in wallPositions:
                self.addRoomToLists(room)
                # print("Created new Room: " + room.__str__())

            # Case 2. We find a matching left wall and set our right-side neighbour wall to this left wall.
            elif room.getLeftWall() in wallPositions and room.getRightWall() not in wallPositions:
                neighbour = self.findAdjacentRoom("right", room)
                if neighbour:
                    self.findAdjacentRoom("right", room).setLeftWall(room.getLeftWall())

            # Case 3. We find a matching right wall and set our left-side neighbour wall to this right wall.
            elif room.getLeftWall() not in wallPositions and room.getRightWall() in wallPositions:
                neighbour = self.findAdjacentRoom("left", room)
                if neighbour:
                    self.findAdjacentRoom("left", room).setRightWall(room.getRightWall())

        self.resetQueue()


    def getPositionOfVerticalWalls(self, line):
        list = []
        for match in re.finditer(simpleWallPattern, line):
            list.append(match.start())
        return list

    def getRoomFromPosition(self, pos):
        for room in self.getOpenRooms():
            if room.getLeftWall() <= pos < room.getRightWall():
                return room
        return -1

    def findAdjacentRoom(self, direction, room):
        for candidate in self.getOpenRooms():
            if direction == "left":
                if room.getLeftWall() == candidate.getRightWall():
                    return candidate
            if direction == "right":
                if room.getRightWall() == candidate.getLeftWall():
                    return candidate
        # print("No adjacent room found.")
        return None


    def updateNamesFromLine(self, names):
        if len(names) > 0:
            for name, index in names:
                name = name.strip("(")
                name = name.strip(")")

                this_room = self.getRoomFromPosition(index)
                if this_room != -1:
                    this_room.setRoomName(name)


    def updateChairsFromLine(self, chairs):
        if (len(chairs) > 0):
            for chair, index in chairs:
                this_room = self.getRoomFromPosition(index)
                if this_room != -1:
                    this_room.addChairToRoom(chair)

    def findLowerWallOnPosition(self, left, right, line):
        matches = []
        for match in re.finditer('\+', line):
            matches.append(match.start())

        for match in re.finditer(lowerWallPattern, line):
            if match.start() == left and match.end() == right + 1:
                return True

    def getChairsInHouseByType(self):
        count = [0, 0, 0, 0]
        for r in self.getInHouseRooms():
            count[0] += r.getChairsByType("W")
            count[1] += r.getChairsByType("P")
            count[2] += r.getChairsByType("S")
            count[3] += r.getChairsByType("C")
        return count

    def getTotalChairCount(self):
        count = 0
        for r in self.getInHouseRooms():
            count += r.getTotalChairsInRoom()
        return count

