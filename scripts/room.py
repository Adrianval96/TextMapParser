class Room:
    def __init__(self, lw, rw, name=""):
        self.id = id(self)
        self.name = name
        self.leftWall = lw
        self.rightWall = rw
        self.P = 0
        self.S = 0
        self.W = 0
        self.C = 0
        self.parseFinish = False

    def getId(self):
        return self.id

    def setRoomName(self, name):
        self.name = name

    def getRoomName(self):
        return self.name

    def setParseFinish(self):
        self.parseFinish = True

    def getParseFinish(self):
        return self.parseFinish

    def setLeftWall(self, lw):
        self.leftWall = lw

    def getLeftWall(self):
        return self.leftWall

    def setRightWall(self, rw):
        self.rightWall = rw

    def getRightWall(self):
        return self.rightWall

    def getRoomBounds(self):
        return self.getLeftWall(), self.getRightWall()

    def getP(self):
        return self.P

    def getS(self):
        return self.S

    def getC(self):
        return self.C

    def getW(self):
        return self.W

    def getTotalChairsInRoom(self):
        return self.getP() + self.getS() + self.getC() + self.getW()

    def getChairsByType(self, type):
        if type == "P":
            return self.getP()
        elif type == "S":
            return self.getS()
        elif type == "C":
            return self.getC()
        elif type == "W":
            return self.getW()

    def addChairToRoom(self, str):
        if str == "P":
            self.P += 1
        elif str == "S":
            self.S += 1
        elif str == "W":
            self.W += 1
        elif str == "C":
            self.C += 1

    def __str__(self):
        return "{}: \n W: {}, P: {}, S: {}, C: {}".format(self.getRoomName(), self.getW(), self.getP(), self.getS(), self.getC())


    # Deprecated __str__() method.
    #def __str__(self):
        #args = {'id': self.id, 'name': self.name, 'lw': self.leftWall, 'rw': self.rightWall,
        #        'p': self.P, 's': self.S, 'w': self.W, 'c': self.C, 'st': self.parseFinish}

        #return '''\nId: {id}
        #Name: {name}
        #Left Wall position: {lw}
        #Right Wall position: {rw}
        #P: {p}
        #S: {s}
        #W: {w}
        #C: {c}
        #Closed: {st}'''.format(**args)