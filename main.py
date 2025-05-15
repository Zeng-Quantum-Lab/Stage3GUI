import instruments as ik
import instruments.units as u
from ctypes import WinDLL, create_string_buffer
import clr
import os
import sys
import time
from tkinter import *

# Window declaration
root = Tk() 

#Variable declaration
global T_current, T_set
T_current = 0
T_set = IntVar()


#Update functions
def update_T_current(*args):
    global T_current
    T_current += 1
    T_current_string.set(T_current)
    root.after(1000, update_T_current)

def update_T_set(value):
    global T_set
    T_set_string.set(value)
    T_set = value
    print("T_set = " + T_set)

# GUI Setting
T_current_string = StringVar()
T_current_string.set(T_current)
T_set_string = StringVar()
T_set_string.set("0")

root.title("test1")
T_current_label = Label(root, text="T_Current")
T_current_textblock = Entry(root, textvariable=T_current_string)
T_set_label = Label(root, text="T_Set")
T_set_text = Label(root, textvariable=T_set_string)
T_set_slider = Scale(root, from_=0, to=150, orient="horizontal", variable=T_set, command=update_T_set)


#GUI Placement
T_current_label.grid(column=0, row=0)
T_current_textblock.grid(column=1, row=0)
T_set_label.grid(column=0, row=1)
T_set_text.grid(column=1, row=1)
T_set_slider.grid(columnspan=2, column=0, row=2)

#Variable update call 
root.after(1000, update_T_current)

#Calling Tk mainloop
root.mainloop()
