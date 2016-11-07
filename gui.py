from tkinter import *
from tkinter import font
import RPi.GPIO as GPIO
import time
import os
from gpiozero import MotionSensor

pir_start = MotionSensor(15)
pir_stop = MotionSensor(14)

class Stopwatch(Frame):
    
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._lapTime=0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()      

    def makeWidgets(self):                         
        """ Make the time label. """
        myFont11 = font.Font(family = 'Haveltica', size =56, weight = 'bold')
        myFont21 = font.Font(family = 'Haveltica', size =24, weight = 'bold')
        l = Label(self, textvariable=self.timestr, font=myFont11)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)

    def _update(self):
        global gstring
        global startButton
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
        if not pir_stop.motion_detected:
            print("Finish : Time Stoped")
            self.Stop()
            playMusic(1)
            hai()

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        

    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

lapke = 1

class Lapwatch(Frame):
    global lapke
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._lapTime=0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgetsLap()    

    def makeWidgetsLap(self):                         
        """ Make the time label. """
        myFont11 = font.Font(family = 'Haveltica', size =56, weight = 'bold')
        myFont21 = font.Font(family = 'Haveltica', size =24, weight = 'bold')
        l = Label(self, textvariable=self.timestr, font=myFont21)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)                      

    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set("Lap " + '%02d' % (lapke) + " : " + '%02d:%02d:%02d' % (minutes, seconds, hseconds))
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0

    def Lap(self):
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1 
win = Tk()
gstring = StringVar()
gstring.set("GET READY")
typesounds = ["start","finish"]

myFont = font.Font(family = 'Haveltica', size =36, weight = 'bold')
myFont1 = font.Font(family = 'Haveltica', size =56, weight = 'bold')
myFont2 = font.Font(family = 'Haveltica', size =24, weight = 'bold')

sw=Stopwatch(win)
lap1=Lapwatch(win)
lap2=Lapwatch(win)
lap3=Lapwatch(win)
lap4=Lapwatch(win)

def playMusic(n):
    _sound = "aplay /home/pi/Desktop/" + typesounds[n] + ".wav -R 1"
    os.system(_sound)

def startTimer():
    global pir_start
    global pir_stop
    if startButton["text"] == "GET READY":
        while True:
            if not pir_start.motion_detected:
                print("Time Started")
                break
        startButton["text"] = "RUNNING"
        lapButton['state']='normal'
        sw.Start()
        lap1.Lap()
        playMusic(0)
    elif startButton["text"] == "FINISH":
        startButton["text"] = "GET READY"
        sw.Reset()
        lapButton['state']='disabled'
             
def lapTimer():
    global lapke
    if lapke == 1:
        lap1.place(relx=0.5, rely=0.45, anchor=CENTER)
        lap1.Stop()
        lapke+=1
        lap2.Lap()
        lap2.place(relx=0.5, rely=0.60, anchor=CENTER)
    elif lapke == 2:
        lap2.Stop()
        lapke+=1
        lap3.Lap()
        lap3.place(relx=0.5, rely=0.75, anchor=CENTER)
    elif lapke == 3:
        lap3.Stop()
        lapke+=1
        lap4.Lap()
        lap4.place(relx=0.5, rely=0.90, anchor=CENTER) 
    elif lapke == 4:
        lap4.Stop()
           
def resetTimer():
    global lapke
    lapke = 1;
    sw.Reset()
    sw.Stop()
    lap1.Reset()
    lap2.Reset()
    lap3.Reset()
    lap4.Reset()
    lap1.destroy()
    lap2.destroy()
    lap3.destroy()
    lap4.destroy()
    startButton["text"]="GET READY"
            
startButton = Button(win, text = "GET READY", font = myFont, command = startTimer, height = 2, width = 9)
lapButton = Button(win, text = "LAP", font = myFont, state = DISABLED,command = lapTimer, height = 2, width = 6)
def hai():
    startButton["text"]="FINISH"
    lap1.Stop()
    lap2.Stop()
    lap3.Stop()
    lap4.Stop()

def main():
    global gstring
    lapke = 1
    tulisan = StringVar()
    tulisan.set("IBIKK - PENS")
    

    win.title("STOPWATCH AUTO TIMER - PENS")
    win.geometry('1024x768')
    
    startButton.place(relx=0.25, rely=0.1, anchor=CENTER)
    
    lapButton.place(relx=0.53, rely=0.1, anchor=CENTER)
    resetButton = Button(win, text = "RESET", font = myFont, command = resetTimer, height = 2, width = 6)
    resetButton.place(relx=0.76, rely=0.1, anchor=CENTER)
    #lblTime = Label(win, textvariable=strTime, relief=RAISED, font=myFont1)
    #lblTime.place(relx=0.5, rely=0.30, anchor=CENTER)
    sw.place(relx=0.5, rely=0.30, anchor=CENTER)
    
    lblTulis = Label(win, textvariable=tulisan, relief=RAISED, font=myFont2)
    lblTulis.place(relx=1, rely=1, anchor=SE)


    win.mainloop()
if __name__ == '__main__':
    main()
