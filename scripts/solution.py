import re

from room import Room
from lineparser import LineParser

'''
Author: Adrian Valero Gimeno
Contact e-mail: adrianval96@gmail.com
Github: https://github.com/Adrianval96
'''



'''
This first part of the code will include the regex patterns used
throughout the code to identify the different elements of the map.

ChairPattern does not consider multiple chairs right next to each other 
(w/o spaces in-between) but is sufficient for the given example
'''

roomNamePattern = re.compile("\([a-z ]*\)", re.IGNORECASE)

chairPattern = re.compile("([CWPS])+")

#There is a problem with shiftingWallsPattern. This feature will not work in our implementation.
shiftingWallsPattern = re.compile(r"[\\/]+")
lowerWallPattern = re.compile("[\+\-*\+]+")
wallEdgesPattern = re.compile("\+")

parser = LineParser()



def parse_file(filepath):
    """
    Parse the map of the house at a given filepath

    Parameters
    -----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    A string with rooms information as well as total chairs
    """
    lineIndex = 1

    with open(filepath, 'r') as file_object:
        line = file_object.readline()

        initialiseRoomsOnTop(line)

        while line:
            parser.setLastLine(line)
            lineIndex += 1
            line = file_object.readline()

            # This method updates the room list in case there were any other rooms closing in last line
            parser.liberateQueue(line)

            # This checks if the line contains the name of any rooms and updates the dataset accordingly
            parser.updateNamesFromLine(findRoomNamesInLine(line))
            parser.updateChairsFromLine(findChairsInLine(line))

            # This feature does not work
            checkforWallShifts(line)

            # This updates the wall structure of the rooms to accomodate for changes in the map
            adjustFromLowerWalls(line, lineIndex)

    return houseSummary()


def newRoom(lb, rb):
    return Room(lb, rb)

def createNewRoom(lb, rb):
    parser.addRoomToLists(newRoom(lb, rb))

# Initial parsing to check how many rooms there are on top of the map, equal to the number of '+' elements minus 1
# These initial rooms are added to our room list, without a name for now.
def initialiseRoomsOnTop(line):
    wall_positions = []
    for match in re.finditer('\+', line):
        wall_positions.append(match.start())

    rooms_being_parsed = len(wall_positions) - 1
    for i in range(rooms_being_parsed):
        createNewRoom(wall_positions[i], wall_positions[i + 1])


# N^2
def adjustFromLowerWalls(line, lineIndex):
    if lineIndex <= 2:
        return

    for match in re.finditer(lowerWallPattern, line):

        if len(re.findall('\+', match.group())) <= 2:
            # Lower walls standard case (+----------+)
            checkWallEdgesAndTransform(match.start(), match.end() - 1, lineIndex)
        else:
            # Lower walls composite case (+----------+----------+)
            # If code finds more than a plus sign in the same wall match it will launch a different transform for each pair.
            plusPositions = []
            for plusSign in re.finditer('\+', match.group()):
                plusPositions.append(match.start() + plusSign.start())

            for i in range(len(plusPositions) - 1):
                checkWallEdgesAndTransform(plusPositions[i], plusPositions[i+1], lineIndex)


def checkWallEdgesAndTransform(start, end, lineIndex):
    for room in parser.getOpenRooms():
        lb, rb = room.getRoomBounds()

        # If the bounds match that means the room needs to be closed. If a new one must be open depends on next line
        if start == lb and end == rb:
            # room.setParseFinish()
            parser.removeFromOpenRooms(room)

            # this is a necessary condition to prevent further rooms to be created outside the bounds of the map
            if lineIndex >= parser.getLineLimit():
                break
            parser.addToQueue(newRoom(start, end))
            break

        # If bounds DO NOT match means that:
        # The wall shifts from a '+' symbol position to another
        # This is reflected in the next two 'elif' statements
        elif start == lb and end < rb:
            neighbor = parser.findAdjacentRoom("left", room)
            print("Case 2 for lower wall. Moving to the right and updating neighbor / creating new room.")
            room.setLeftWall(end)
            if neighbor:
                neighbor.setRightWall(end)
            else:
                # New neighbor is added to queue. It will be added when we move on to next line.
                parser.addToQueue(newRoom(start, end))
            break

        elif start < lb and end == rb:
            neighbor = parser.findAdjacentRoom("right", room)
            print("Case 3 for lower wall. Moving to the left and updating neighbor / creating new room.")
            room.setRightWall(start)
            if neighbor:
                neighbor.setLeftWall(start)
            else:
                parser.addToQueue(newRoom(start, end))
            break
        else:
            # print("Room not found in this iteration.")
            pass



def findRoomNamesInLine(line):
    matches = []
    for match in re.finditer(roomNamePattern, line):
        obj = [match.group(), match.start()]
        matches.append(obj)
    return matches


# With this we will find the index in which each chair is positioned
# We will return a data object 'matches' containing the text (type of chair) as well as this index.
def findChairsInLine(line):
    matches = []
    for match in re.finditer(chairPattern, line):
        obj = [match.group(), match.start()]
        matches.append(obj)
    return matches



# These methods are meant to check for the wall shifts (i.e line 32-34), but the regular expression does not match.
def checkforWallShifts(line):
    # print("Checking wall for shifts...")
    if re.match(shiftingWallsPattern, line):
        # print("EUREKA")
        return updateWallPositionsOnShift(line)
    return None


# This method would update the wall positions of the room objects
def updateWallPositionsOnShift(line):
    for match in re.finditer(shiftingWallsPattern, line):
        if match.group() == '\\':
            shiftRoomWalls(1, parser.getRoomFromPosition(match.start()), parser.getRoomFromPosition(match.end()))
        elif match.group() == '\/':
            shiftRoomWalls(-1, parser.getRoomFromPosition(match.start()), parser.getRoomFromPosition(match.end()))



def shiftRoomWalls(shift, lr, rr):
    lr.setRightWall(lr.getRightWall() + shift)
    rr.setLeftWall(rr.getRightWall() + shift)

    print("Walls shifted!")


def houseSummary():
    roomList = []
    for room in parser.getInHouseRooms():
        roomList.append(room)
    roomList = sorted(roomList, key=lambda k: k.getRoomName())
    totals = parser.getChairsInHouseByType()
    totalCount = "total: \nW: {}, P: {}, S: {}, C: {}\n".format(totals[0], totals[1], totals[2], totals[3])
    return totalCount + '\n'.join(map(str, roomList))



def __main__():
    print(parse_file("maps/rooms_noShifting.txt"))

    # Unfortunately the standard map will not work correctly due to the lack of wall shifting procedures
    #print(parse_file("./maps/rooms.txt"))


__main__()
