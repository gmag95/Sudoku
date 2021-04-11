#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
import numpy as np
import datetime

#Gui object, it creates the board and contains various methods to update it

class Gui:
    
    def __init__(self):
        
        global ws, hs, i
        
        #initialization of the board
        
        self.box=[[0 for x in range(9)] for row in range(9)]
        
        self.flagdf=[[0 for x in range(9)] for row in range(9)]

        self.root = tk.Tk()
        self.root.title("Sudoku solver")
        
        #code necessary to center the window
        
        w=522
        h=556
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        
        #the four rectangles create the black bar needed to create a sudoku board
        
        self.frame2 = tk.Canvas(self.root, width=520, height=520)
        self.frame2.create_rectangle(171, 0, 174, 521, fill="black")
        self.frame2.create_rectangle(346, 0, 349, 521, fill="black")
        self.frame2.create_rectangle(0, 171, 521, 174, fill="black")
        self.frame2.create_rectangle(0, 346, 521, 349, fill="black")
        self.frame2.grid(columnspan=9, rowspan=9)
        
        #mouse click binding
        
        self.root.bind("<Button-1>", getxy)
        for i in range(1,10):
            self.root.bind(f"{i}", getkey)
            
        #initialization of the 81 boxes
        
        self.i=tk.PhotoImage()
        
        for x in range(9):
            for y in range(9):

                if data[x][y]==0:
                    self.box[x][y]=tk.Label(self.root, text=" ", image=self.i, relief="solid", width=50, height=50, compound="center", bg="white")
                else:
                    self.box[x][y]=tk.Label(self.root, text=data[x][y], image=self.i, relief="solid", width=50, height=50, compound="center", bg="white")
                    self.box[x][y].config(font=("Calibri", 18, "bold"))
                self.box[x][y].grid(row=x, column=y, padx=1, pady=1)
        
        #initialization of the bottom interface
        
        self.bottomframe=tk.LabelFrame(self.root, pady=2, relief="flat")
        self.bottomframe.grid(row=10, columnspan=9)
        
        self.clear_button=tk.Button(self.bottomframe, text="Clear inputs", command=reset)
        self.clear_button.grid(row=1, column=1, padx=35)
        self.start_button=tk.Button(self.bottomframe, text="Solve the sudoku", command=start)
        self.start_button.grid(row=1, column=2, padx=35)
        self.myclock=tk.Label(self.bottomframe, font = ('calibri', 12)) 
        self.myclock.grid(row=1, column=3, padx=35)
        self.start_time=datetime.datetime.now()
        self.timefunc()
        
    def mainloop(self):
        
        self.root.mainloop()
   
    def insert(self, new_x, new_y, num):
        
        #code used by the solver
        #insert a new number in a box
        
        self.box[new_x][new_y].grid_forget()
        self.box[new_x][new_y]=tk.Label(self.root, text=num, image=self.i, relief="solid", width=50, height=50, compound="center", bg="PaleGreen3")
        self.box[new_x][new_y].config(font=("Calibri", 18, "bold"))
        self.box[new_x][new_y].grid(row=new_x, column=new_y, padx=1, pady=1)
        self.root.after(10, self.root.update())
        
    def delete(self, new_x, new_y):
        
        #code used by the solver
        #delete a number in a box
        
        self.box[new_x][new_y].grid_forget()
        self.box[new_x][new_y]=tk.Label(self.root, text=" ", image=self.i, relief="solid", width=50, height=50, compound="center", bg="white")
        self.box[new_x][new_y].config(font=("Calibri", 18, "bold"))
        self.box[new_x][new_y].grid(row=new_x, column=new_y, padx=1, pady=1)
        self.root.after(10, self.root.update())
    
    def deactivate(self):
        
        #it deactivates the two bottom buttons while solving the sudoku
        
        self.start_button.grid_forget()
        self.start_button=tk.Button(self.bottomframe, text="Solve the sudoku", command=start, state="disabled")
        self.start_button.grid(row=1, column=2, padx=35)
        self.clear_button.grid_forget()
        self.clear_button=tk.Button(self.bottomframe, text="Clear inputs", command=reset, state="disabled")
        self.clear_button.grid(row=1, column=1, padx=35)
    
    def timefunc(self):
        
        #code that manages the clock
    
        current_time=datetime.datetime.now()
        seconds=(current_time-self.start_time).seconds
        minutes=int(seconds/60)
            
        if seconds-60*minutes<10:
            seconds="0"+str(seconds-60*minutes)

        elif seconds>=60:
            seconds=seconds-60*minutes
                
        self.myclock.config(text = str(minutes)+":"+str(seconds))
        if timestop==False:
            self.myclock.after(1000, self.timefunc)

#function that reads the mouse input abd highlights the pressed box

def getxy(event):
    
    global mou_x, mou_y, working, click_hist
    
    if working==False:
        mou_y = (myboard.root.winfo_pointerx() - myboard.root.winfo_rootx())/58
        mou_x = (myboard.root.winfo_pointery() - myboard.root.winfo_rooty())/58
        click_hist.append([int(mou_x), int(mou_y)])
        click_hist.pop(0)
        
        myboard.root.bind("<BackSpace>", deletion)
        
        #this part of the code resets the previous box if the enter key was not pressed
        
        if click_hist[0][0]!="X" and mou_x<9 and mou_y<9:
            if myboard.flagdf[click_hist[0][0]][click_hist[0][1]]==0 and myboard.box[click_hist[0][0]][click_hist[0][1]]["bg"]=="light grey":
                myboard.box[click_hist[0][0]][click_hist[0][1]].config(bg="white", image=myboard.i, text=" ")

        if mou_x<9 and mou_y<9 and myboard.box[int(mou_x)][int(mou_y)]["text"]==" ":
            myboard.box[int(mou_x)][int(mou_y)].config(bg="light grey", image=myboard.i)

#this function grabs the number key and puts it in the box previously selected

def getkey(event):
    
    if working==False:
        global char
        char=event.char
        myboard.box[int(mou_x)][int(mou_y)].config(text = char, image=myboard.i)
        myboard.box[int(mou_x)][int(mou_y)].config(font=("Calibri", 18, "bold"))
        myboard.root.bind("<Return>", change)

#this function finalizes the insertion, if the number is correct, or leaves a blank box if it is not

def change(event):
    
    global timestop
    
    if int(char) in findnum(int(mou_x), int(mou_y)):
        dfvar[int(mou_x)][int(mou_y)]=char
        myboard.box[int(mou_x)][int(mou_y)].config(bg="light grey", image=myboard.i)
        myboard.flagdf[int(mou_x)][int(mou_y)]=1
        
    else:
        myboard.box[int(mou_x)][int(mou_y)].config(bg="white", image=myboard.i, text=" ")
    
    #this part of code stops the time and pops up a window if the user has completed the sudoku
    
    if wincheck()==0:
        
        timestop=True
        
        w=200
        h=79
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        
        top=tk.Toplevel()
        top.title("")
        top.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        top.overrideredirect(True)
        popframe=tk.LabelFrame(top)
        popframe.place(relx=0.5, rely=0.06, anchor="n")
        tk.Label(popframe, text="Victory!").pack(pady=5)
        tk.Button(popframe, text="Close this window", command=top.destroy).pack(pady=5, padx=20)

#function that allows the user to delete a box previously filled

def deletion(event):
    
    if myboard.box[int(mou_x)][int(mou_y)]["bg"]=="light grey":
        myboard.box[int(mou_x)][int(mou_y)].config(bg="white", image=myboard.i, text=" ")

#this function checks whether all the boxes have been filled or not

def wincheck():
    
    nullcount=0
    
    for x in range(9):
        for y in range(9):
            if myboard.box[x][y]["text"]==" ":
                nullcount+=1
    return nullcount

#this function restores the sudoku to the starting condition

def reset():
    
    global dfvar, curr_x, curr_y, working, timestop, click_hist
    
    dfvar=np.array(data)
        
    curr_x=0
    curr_y=0
    
    click_hist=[["X", "X"], ["X", "X"]]
    
    myboard.start_time=datetime.datetime.now()
    
    myboard.flagdf=[[0 for x in range(9)] for row in range(9)]
    
    working=False
    timestop=False
    myboard.timefunc()
    
    myboard.i=tk.PhotoImage()
        
    for x in range(9):
        for y in range(9):

            if data[x][y]==0:
                myboard.box[x][y]=tk.Label(myboard.root, text=" ", image=myboard.i, relief="solid", width=50, height=50, compound="center", bg="white")
            else:
                myboard.box[x][y]=tk.Label(myboard.root, text=data[x][y], image=myboard.i, relief="solid", width=50, height=50, compound="center", bg="white")
                myboard.box[x][y].config(font=("Calibri", 18, "bold"))
            myboard.box[x][y].grid(row=x, column=y, padx=1, pady=1)
    
    #this part of code makes the automatic solver button active again
    
    myboard.start_button.grid_forget()
    myboard.start_button=tk.Button(myboard.bottomframe, text="Solve the sudoku", command=start)
    myboard.start_button.grid(row=1, column=2, padx=35)

#this function pops up a different window in case the sudoku was solved or not

def start():
    
    global working, timestop, dfvar
    
    myboard.deactivate()

    dfvar=np.array(data)
    
    w=200
    h=79
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    working=True

    if solver(curr_x, curr_y):
        timestop=True
        top=tk.Toplevel()
        top.title("")
        top.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        top.overrideredirect(True)
        popframe=tk.LabelFrame(top)
        popframe.place(relx=0.5, rely=0.06, anchor="n")
        tk.Label(popframe, text="A solution has been found").pack(padx=10, pady=5)
        tk.Button(popframe, text="Close this window", command=top.destroy).pack(pady=5)
        
    else:
        timestop=True
        top=tk.Toplevel()
        top.title("")
        top.geometry(f"{w}x{h}+{int(x)}+{int(y)}") 
        top.overrideredirect(True)
        popframe=tk.LabelFrame(top)
        popframe.place(relx=0.5, rely=0.06, anchor="n")
        tk.Label(popframe, text="This sudoku has no solution").pack(padx=10, pady=5)
        tk.Button(popframe, text="Close this window", command=top.destroy).pack(pady=5)
    
    myboard.clear_button.grid_forget()
    myboard.clear_button=tk.Button(myboard.bottomframe, text="Clear inputs", command=reset)
    myboard.clear_button.grid(row=1, column=1, padx=35)  


#function for the automatic solver
#this function finds the next blank box in the board

def findnext(x, y):
    
    for m in range(y, 9):
        if dfvar[x, m]==0:
            
            return x, m
    
    for i in range(x+1, 9):
        for l in range(9):
            if dfvar[i, l]==0:
                
                return i, l

#function for the automatic solver
#this function returns a list of valid numbers for a specific blank box

def findnum(x, y):

    if x<3 :
        if y<3:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[0,0:3]).difference(dfvar[1,0:3]).difference(dfvar[2,0:3])))
        elif 3<=y<6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[0,3:6]).difference(dfvar[1,3:6]).difference(dfvar[2,3:6])))
        elif y>=6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[0,6:9]).difference(dfvar[1,6:9]).difference(dfvar[2,6:9])))
    elif 3<=x<6:
        if y<3:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[3,0:3]).difference(dfvar[4,0:3]).difference(dfvar[5,0:3])))
        elif 3<=y<6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[3,3:6]).difference(dfvar[4,3:6]).difference(dfvar[5,3:6])))
        elif y>=6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[3,6:9]).difference(dfvar[4,6:9]).difference(dfvar[5,6:9])))
    elif x>=6:
        if y<3:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[6,0:3]).difference(dfvar[7,0:3]).difference(dfvar[8,0:3])))
        elif 3<=y<6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[6,3:6]).difference(dfvar[7,3:6]).difference(dfvar[8,3:6])))
        elif y>=6:
            return sorted(list(set(rangenum).difference(dfvar[:,y]).difference(dfvar[x,:]).difference(dfvar[6,6:9]).difference(dfvar[7,6:9]).difference(dfvar[8,6:9])))

#this function contains the backtracking algorithm that solves the sudoku

def solver(curr_x, curr_y):
    
    if any(0 in dfvar[i] for i in range(9))==False:
        return True
    
    new_x, new_y = findnext(curr_x, curr_y)
    
    mylist=findnum(new_x, new_y)
    
    if len(mylist)!=0:
        
        for num in mylist:
            
            dfvar[new_x, new_y]=num
            myboard.insert(new_x, new_y, num)
    
            if solver(new_x, new_y):
                return True
            else:
                dfvar[new_x, new_y]=0
                myboard.delete(new_x, new_y)
                
                
        return False
    
    else:
        return False

#main part of the program

data =   [[5,1,7,6,9,8,0,3,4],
          [2,8,9,0,0,4,0,0,0],
          [3,4,6,2,0,5,0,9,0],
          [6,0,2,0,0,0,0,1,0],
          [0,3,8,0,0,6,0,4,7],
          [0,0,0,0,0,0,0,0,0],
          [0,9,0,0,0,0,0,7,8],
          [7,0,3,4,0,0,5,6,0],
          [0,0,0,0,0,0,0,0,0]]

dfvar=np.array(data)

rangenum=[1,2,3,4,5,6,7,8,9]

click_hist=[["X", "X"], ["X", "X"]]

working=False
timestop=False

curr_x=0
curr_y=0

myboard=Gui()

myboard.mainloop()