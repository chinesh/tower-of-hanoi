from Tkinter import *  # * import everytihng in tkinter

class Disc:
    """creating movable disc"""
    def __init__(self,cv,pos,length,height,colour):
        """creates a canvas cv at agiven position"""
        x0,y0 = pos
        x1,x2 = x0-length/2.0,x0+length/2.0
        y1,y2=y0-height,y0
        self.cv = cv
        self.item = cv.create_rectangle(x1,y1,x2,y2,fill="#%02x%02x%02x" % colour)

    def move_to(self,x,y,speed):
        #move the bottom centre of the disc to x,y and the speed defines at which they move.

        x1,y1,x2,y2 = self.cv.coords(self.item)             #inheriting the coordinates
        x0,y0=(x1+x2)/2 , y2                                    #defining the cordinates of the bottom centre of the disc
        dx,dy = x-x0,y-y0                                       # x,y are the final coordinates after each steps
                                                                # dx , dy tells the distance they need to move
        d = (dx**2+dy**2)**0.5                                  #distance that centre bottom of the disc move
        steps = int(d/(10*speed-5)) + 1                         #always be greater than 1
        dx , dy = dx/steps,dy/steps                             #tells the distance moves per unit step
        for i in range(steps):
            self.cv.move(self.item,dx,dy)
            self.cv.update()                                    #append
            self.cv.after(20)                                  #time delay

class Tower(list):
    def __init__(self,x,y,h):
        self.x = x
        self.y = y
        self.h = h                                              #(x,y) tells the coordinates and h tells the height
    def top(self):
            return self.x, self.y - len(self)*self.h

class HanoiEngine:
    """play the game on the canvas"""


    def __init__(self,canvas,nrOfDiscs,speed,moveCntDisplay=None):
        self.cv = canvas
        self.nrOfDiscs = nrOfDiscs
        self.speed = speed
        self.moveDisplay = moveCntDisplay
        self.running = False
        self.moveCnt = 0
        self.discs = []
        self.towerA = Tower( 80, 190, 15)
        self.towerB = Tower(220, 190, 15)
        self.towerC = Tower(360, 190, 15)
        self.reset()

    def hanoi(self,n,src,dest,temp):
        """recurssive loop"""
        if(n>0):
            for x in self.hanoi(n-1,src,temp,dest):yield None
            yield self.move(src,dest)
            for x in self.hanoi(n-1,temp,dest,src):yield None

    def move(self, src_tower, dest_tower):
        """moves uppermost disc of source tower to top of destination
        tower."""
        self.moveCnt += 1
        self.moveDisplay(self.moveCnt)
        disc = src_tower.pop()              #The method pop() removes and returns last object or obj from the list.
        x1, y1 = src_tower.top()
        x2, y2 = dest_tower.top()
        disc.move_to(x1,20,self.speed)      # move disc to the height
        disc.move_to(x2,20,self.speed)      # move disc horrizontally
        disc.move_to(x2,y2,self.speed)      # move disc to the final postion
        dest_tower.append(disc)

    def reset(self):
        """to setup a new game"""
        self.moveCnt=0
        self.moveDisplay(self.moveCnt)
        while self.towerA:self.towerA.pop()
        while self.towerB:self.towerB.pop()
        while self.towerC:self.towerC.pop()
        for s in self.discs:
            self.cv.delete(s.item)          #deleting discs form the tower
        """coloring different discs"""
        if self.nrOfDiscs>1:
            colour_diff = 250//(self.nrOfDiscs-1)
        else:
            colour_diff = 0
        """setting up tower A"""
        for i in range(self.nrOfDiscs):
            length_diff = 100 // self.nrOfDiscs
            length = 120 - i * length_diff
            s = Disc( self.cv, self.towerA.top(), length, 13,
                         (255-i*colour_diff, 0, i*colour_diff))
            self.discs.append(s)
            self.towerA.append(s)
        self.HG = self.hanoi(self.nrOfDiscs,self.towerA,self.towerC,self.towerB)



    def run(self):
        """run games and return true if it is over"""
        self.running=True
        try:
            while self.running:
                result = self.step()
            return result                   #true if done
        except StopIteration:               # Raised when the next() method of an iterator does not point to any object.
            return True

    def step(self):
        """performs one single step and returns true after each step"""
        try:
            self.HG.next()
            return 2**self.nrOfDiscs-1 == self.moveCnt
        except TclError:
            return False

    def stop(self):
        """ ;-) """
        self.running = False

class Hanoi:
    """GUI for 10 towers"""
    def displayMove(self,move):
        """count the number of moves"""
        self.moveCntLbl.configure(text = "move:\n%d" % move)


    def adjust_nr_of_discs(self,e):
        """callback function for nr-of-discs-scale-widget"""
        self.hEngine.nrOfDiscs = self.discs.get()
        self.reset()

    def adjust_speed(self,e):
        """callback function for speeds-scale-widget"""
        self.hEngine.speed = self.tempo.get()

    def setState(self, STATE):
        """simple representation of a finite state machine same as artificial intelligance (ON/OFF bulb) """
        self.state = STATE
        try:
            if STATE == "START":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(text="start", state=NORMAL)
                self.stepBtn.configure(state=NORMAL)
            elif STATE == "RUNNING":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray70")
                self.discsLbl.configure(fg="gray70")
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(text="pause", state=NORMAL)
                self.stepBtn.configure(state=DISABLED)
            elif STATE == "PAUSE":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)
                self.startBtn.configure(text="resume", state=NORMAL)
                self.stepBtn.configure(state=NORMAL)
            elif STATE == "DONE":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)
                self.startBtn.configure(text="start", state=DISABLED)
                self.stepBtn.configure(state=DISABLED)
            elif STATE == "TIMEOUT":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray")
                self.discsLbl.configure(fg="gray")
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(state=DISABLED)
                self.stepBtn.configure(state=DISABLED)
        except TclError:
            pass

    def reset(self):
        self.hEngine.reset()
        self.setState("START")


    def start(self):
        """callback function for start button, which also serves as
        pause button. Makes hEngine running until done or interrupted"""
        if self.state in ["START","PAUSE"]:
            self.setState("RUNNING")
            if self.hEngine.run():
                self.setState("DONE")
            else:
                self.setState("PAUSE")
        elif self.state == "RUNNING":
            self.setState("TIMEOUT")
            self.hEngine.stop()

    def step(self):
        """callback function for step button.
        makes hEngine perform a single step"""
        self.setState("TIMEOUT")
        if self.hEngine.step():
            self.setState("DONE")
        else:
            self.setState("PAUSE")

    def __init__(self,nrOfDiscs,speed):
        """making GUI and setting the variables using scals"""
        root = Tk()
        root.title = "Tower of Hanoi"
        cv = Canvas(root,width=450,height=250,bg="gray")
        cv.pack()

        fnt = ("Arial",12,"bold")

        attrFrame = Frame(root)                             #contains scales to adjust game's attributes
        self.discsLbl = Label(attrFrame, width=7, height=2, font=fnt,
                              text="discs:\n")
        self.discs = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=75, showvalue=1, repeatinterval=10,
                           command=self.adjust_nr_of_discs)
        self.discs.set(nrOfDiscs)    #we can not directly assign the value because int can not be pack inside the frame.
        self.tempoLbl = Label(attrFrame, width=8,  height=2, font=fnt,
                              text = "   speed:\n")
        self.tempo = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=100, showvalue=1,repeatinterval=10,
                           command = self.adjust_speed)
        self.tempo.set(speed)
        self.moveCntLbl= Label(attrFrame, width=10, height=2, font=fnt,
                               padx=20, text=" move:\n0", anchor=CENTER)

        for widget in ( self.discsLbl, self.discs, self.tempoLbl, self.tempo,
                                                             self.moveCntLbl ):
            widget.pack(side=LEFT)
        attrFrame.pack(side=TOP)

        ctrlFrame = Frame(root) # contains Buttons to control the game
        self.resetBtn = Button(ctrlFrame, width=11, text="reset", font=fnt,
                               state = DISABLED, padx=15, command = self.reset)
        self.stepBtn  = Button(ctrlFrame, width=11, text="step", font=fnt,
                               state = NORMAL,  padx=15, command = self.step)
        self.startBtn = Button(ctrlFrame, width=11, text="start", font=fnt,
                               state = NORMAL,  padx=15, command = self.start)
        for widget in self.resetBtn, self.stepBtn, self.startBtn:
            widget.pack(side=LEFT)
        ctrlFrame.pack(side=TOP)

        # setup of the scene
        peg1 = cv.create_rectangle(  75,  40,  85, 190, fill='darkgreen')
        peg2 = cv.create_rectangle( 215,  40, 225, 190, fill='darkgreen')
        peg3 = cv.create_rectangle( 355,  40, 365, 190, fill='darkgreen')
        floor = cv.create_rectangle( 10, 191, 430, 200, fill='black')

        self.hEngine = HanoiEngine(cv, nrOfDiscs, speed, self.displayMove)
        self.state = "START"

        root.mainloop()




if __name__=="__main__":
    Hanoi(4,5)


