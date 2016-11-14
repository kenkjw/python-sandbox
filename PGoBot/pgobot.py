import Tkinter
import os
from subprocess import call,Popen,PIPE
from PIL import Image
import tempfile
from enum import Enum
import time
import random
import threading
import StringIO
import ADB

class State(Enum):
    UNKNOWN = 0
    MAIN = 1
    POKESTOP = 2
    ENCOUNTER = 3
    CAUGHT = 4
    INFO = 5

class Encounter:
    def __init__(self,coords):
        self._x1 = coords[0]-5
        self._y1 = coords[1]-5
        self._x2 = coords[0]+5
        self._y2 = coords[1]+5
        self._last = 0

    def inBounds(self,x,y):
        return x > self._x1 and x < self._x2 and y > self._y1 and y < self._y2

    def isReady(self):
        return time.time() - self._last > 95

    def tap(self):
        self._last = time.time()
        ADB.tap((self._x1+self._x2)/2,(self._y1+self._y2)/2)

class Pokestop:
    def __init__(self,coords):
        self._x1 = coords[0]-10
        self._y1 = coords[1]-10
        self._x2 = coords[0]+10
        self._y2 = coords[1]+10
        self._last = 0

    def inBounds(self,x,y):
        return x > self._x1 and x < self._x2 and y > self._y1 and y < self._y2

    def isReady(self):
        return time.time() - self._last > 310

    def tap(self):
        self._last = time.time()
        ADB.tap((self._x1+self._x2)/2,(self._y1+self._y2)/2)


def colour_diff(c1,c2):
    return (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 +(c1[2]-c2[2])**2

def coordSStoEmu(x,y):
    return (x,y)

def getState():
    img = ADB.screencap()
    pix = img.load()
    p1,p2,p3,p4 = pix[625,1145],pix[360,1170],pix[680,400],pix[315,290]
    img.close()
    #455,640
    #encounterp1 = 235,243,237
    #main     p2 = 185,185,185
    #pokestop p4 = 244,252,244
    #caught   p3 = 244,255,244
    #info     p2 = 28,135,150
    state = State.UNKNOWN
    if colour_diff(p1,(235,243,237)) < 100:
        state = State.ENCOUNTER
    elif colour_diff(p2,(185,185,185)) < 100:
        state = State.MAIN
    elif colour_diff(p4,(244,252,244)) < 100:
        state = State.POKESTOP
    elif colour_diff(p3,(245,255,244)) < 100:
        state = State.CAUGHT
    elif colour_diff(p2,(28,135,150)) < 100:
        state = State.INFO
    else:
        print p1,p2,p3,p4
    print state
    return state

class ActionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = False
        self._x = 0
        self._y = 0
        self._lastState = State.UNKNOWN
        self._encounterCount = 0
        self.Pokestops = []
        self.Pokestops.append(Pokestop(coordSStoEmu(427,236)))
        self.Pokestops.append(Pokestop(coordSStoEmu(507,368)))
        self.Pokestops.append(Pokestop(coordSStoEmu(525,468)))
        self.Encounters = []

    def toggle(self):
        self._running = not self._running

    def doAction(self):
        state = getState()
        self.dispatchAction(state)
    def dispatchAction(self,state):
        if state == State.MAIN:
            self.doMain()
        elif state == State.POKESTOP:
            self.doPokestop()
        elif state == State.ENCOUNTER:
            self.doEncounter()
        elif state == State.CAUGHT:
            self.doCaught()
        elif state == State.INFO:
            self.doInfo()

    def doUnknown(self):
        ADB.tap(715,1265)

    def doMain(self):
        for stop in self.Pokestops:
            if stop.isReady():
                self._lastState = State.POKESTOP
                stop.tap()
                return
        xmax = 540
        xmin = 170
        ymax = 980
        ymin = 735
        xnum = 10
        ynum = 6
        xdiv = (xmax-xmin) // xnum
        ydiv = (ymax-ymin) // ynum
        x = random.randint(0,xnum) * xdiv + xmin
        y = random.randint(0,ynum) * ydiv + ymin
        self._lastState = State.MAIN
        self._lastTap = (x,y)
        ADB.tap(x,y)
        
    def doPokestop(self):
        ADB.swipe(200,600,600,600,100)
        time.sleep(1)
        ADB.tap(400,1230)

    def doEncounter(self):
        if self._lastState != State.ENCOUNTER:
            self._encounterCount = 0
        else:
            self._encounterCount += 1

        if self._lastState == State.MAIN:
            x = self._lastTap[0]
            y = self._lastTap[1]
            found = False
            for e in self.Encounters:
                if e.inBounds(x,y):
                    found = True
                    break
            if not found:
                self.Encounters.append(Encounter((x,y)))
        self._lastState = State.ENCOUNTER
        if self._encounterCount > 5:
            ADB.tap(45,80)
            return
        t = random.randint(0,50) + 75
        ADB.swipe(400,1000,400,600,t)


    def doCaught(self):
        ADB.tap(400,950) 

    def doInfo(self):
        ADB.tap(400,1230)

    def run(self):
        while True:
            if self._running:
                self.doAction()
            time.sleep(2)

class Main(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.initWidgets()
        self.initThread()
        self._threadRunning = False

    def initWidgets(self):
        self._buttonText = Tkinter.StringVar()
        self._buttonText.set("Start")
        self._actionButton = Tkinter.Button(self, textvariable = self._buttonText, command = self.actionCallBack)
        self._actionButton.pack()
        self._screencapButton = Tkinter.Button(self, text = "Take Screenshot", command = self.screencapCallBack)
        self._screencapButton.pack()
    
    def initThread(self):
        self._actionThread = ActionThread()
        self._actionThread.start()

    def actionCallBack(self):
        self._actionThread.toggle()
        self._threadRunning = not self._threadRunning
        if self._threadRunning:
            self._buttonText.set("Pause")
        else:
            self._buttonText.set("Start")
        
    def screencapCallBack(self):
        ADB.screencap().show()

def main():
    ADB.init()
    my_app = Main()
    my_app.mainloop()

if __name__ == "__main__":
    main()