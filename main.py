import instruments as ik
import instruments.units as u
from ctypes import WinDLL, create_string_buffer
import clr
import os
import sys
import time
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random #debug
import prior

#Machine variable initialization (Change COM port here)
# tc = ik.thorlabs.TC200.open_serial("COM3", 115200)
# pr = prior(5, r"D:\Projects\App\PriorThorLabGUI\PriorSDK1.9.2\PriorSDK 1.9.2\PriorSDK 1.9.2\x64\PriorScientificSDK.dll")

#Constant declaration
Temperature_PID_Max = 100
Temperature_PID_Min = -100

Pos_max = 1000000
Pos_min = -1000000

Step_size_max = 10000
Step_size_min = -10000

Acceleration_max = 10000
Acceleration_min = -10000

Speed_max = 10000
Speed_min = -10000

# Window declaration
root = Tk() 
fig = Figure(figsize=(5,2), dpi = 70)

#Variable declaration ##################################
##TC200
T_current = 20

start_plot = False
curr_time = 0
time_list = [0]
T_current_list = [T_current]
plot1 = fig.add_subplot(111)
plot1.plot(time_list, T_current_list)

T_set = IntVar()
T_set.set(20)

P_value = 0
I_value = 0
D_value = 0

##KIM101
X_pos = 0 #debug variable 
Y_pos = 0 #debug variable

XY_Step_size = 1
XY_Speed = 1
XY_Acceleration = 1

Z_pos = 0 #debug variable

Z_Step_size = 1
Z_Speed = 1
Z_Acceleration = 1

Angle = 0 #debug variable

Angle_Step_size = 1
Angle_Speed = 1
Angle_Acceleration = 1

##Prior
Prior_X_pos = 0 #debug variable 
Prior_Y_pos = 0 #debug variable

Prior_XY_Step_size = 1
Prior_XY_Speed = 1
Prior_XY_Acceleration = 1

Prior_Z_Step_size = 1
Prior_Z_Speed = 1
Prior_Z_Acceleration = 1

Prior_Z_pos = 0 #debug variable
#Update functions ################################

## TC200
def update_T_current(*args):
    global T_current, T_set, time_list, plot1, T_current_list, canvas, curr_time, start_plot
    T_current = random.randint(20, 150)
    T_current_string.set(T_current)
    if start_plot:
        curr_time += 1
        time_list.append(curr_time)
        T_current_list.append(T_current)
        plot1.plot(time_list, T_current_list)
        canvas.draw()
    else:
        T_current_list[-1] = T_current
    root.after(1000, update_T_current)

def update_T_set(value):
    global T_set, T_set_string
    T_set.set(int(value))
    T_set_string.set(T_set.get())
    print("T_set slider = ", T_set.get()) #debug

def update_T_set_text(*args):
    global T_set, T_set_string
    print("T_set_string = " + T_set_string.get()) #debug
    if (T_set_string.get() != ""):
        T_set.set(int(T_set_string.get()))

def update_P_value():
    global P_value
    # P_value_string.set(P_value_spinbox.get())
    # print(P_value_string)
    if (P_value_spinbox.get() != ""):
        P_value = int(P_value_spinbox.get())
    print("P_value = ", P_value) #debug

def update_P_value_text(*args):
    global P_value, P_value_string
    print("P_value string = ", P_value_string.get()) #debug
    if (P_value_string.get() != ""):
        P_value = int(P_value_string.get())
    print("P_value text = ", P_value) #debug

def update_I_value():
    global I_value
    I_value_string.set(I_value_spinbox.get())
    if (I_value_spinbox.get() != ""):
        I_value = int(I_value_spinbox.get())
    print("I_value = ", I_value) #debug

def update_I_value_text(*args):
    global I_value, I_value_string
    print("I_value string = " + I_value_string.get()) #debug
    if (I_value_string.get() != ""):
        I_value = int(I_value_string.get())
    print("I_value text = ", I_value) #debug

def update_D_value():
    global D_value
    D_value_string.set(D_value_spinbox.get())
    if (D_value_spinbox.get() != ""):
        D_value = int(D_value_spinbox.get())
    print("D_value = ", D_value) #debug

def update_D_value_text(*args):
    global D_value, D_value_string
    print("D_value string = ", D_value_string.get()) #debug
    if (D_value_string.get() != ""):
        D_value = int(D_value_string.get())
    print("D_value text = ", D_value) #debug

def start_temp(*args):
    global start_plot
    reset_plot()
    start_plot = True

def stop_temp(*args):
    global start_plot
    start_plot = False

def reset_plot(*args):
    global start_plot, time_list, T_current, T_current_list, fig
    plot1.clear()
    start_plot = False
    time_list = [0]
    T_current_list = [T_current]
    plot1.plot(time_list, T_current_list)
    canvas.draw()
    

## KIM101
def update_X_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global X_pos
    X_pos_string.set(X_pos)
    root.after(250, update_X_pos_string)

def update_Y_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Y_pos
    Y_pos_string.set(Y_pos)
    root.after(250, update_Y_pos_string)

def update_XY_Step_size():
    global XY_Step_size
    XY_Step_size_string.set(XY_Step_size_spinbox.get())
    if (XY_Step_size_spinbox.get() != ""):
        XY_Step_size = int(XY_Step_size_spinbox.get())
    print("XY_Step_size = ", XY_Step_size) #debug

def update_XY_Step_size_text(*args):
    global XY_Step_size, XY_Step_size_string
    print("XY_Step_size string = " + XY_Step_size_string.get()) #debug
    if (XY_Step_size_string.get() != ""):
        XY_Step_size = int(XY_Step_size_string.get())
    print("Step size text = ", XY_Step_size) #debug

def update_XY_Speed():
    global XY_Speed, XY_Speed_spinbox
    XY_Speed_string.set(XY_Speed_spinbox.get())
    if (XY_Speed_spinbox.get() != ""):
        XY_Speed = int(XY_Speed_spinbox.get())
    print("XY_Speed = ", XY_Speed) #debug

def update_XY_Speed_text(*args):
    global XY_Speed, XY_Speed_string
    print("XY_Speed string = " + XY_Speed_string.get()) #debug
    if (XY_Speed_string.get() != ""):
        XY_Speed = int(XY_Speed_string.get())
    print("XY_Speed text = ", XY_Speed) #debug

def update_XY_Acceleration():
    global XY_Acceleration, XY_Acceleration_spinbox
    XY_Acceleration_string.set(XY_Acceleration_spinbox.get())
    if (XY_Acceleration_spinbox.get() != ""):
        XY_Acceleration = int(XY_Acceleration_spinbox.get())
    print("XY_Acceleration = ", XY_Acceleration) #debug

def update_XY_Acceleration_text(*args):
    global XY_Acceleration, XY_Acceleration_string
    print("XY_Acceleration string = " + XY_Acceleration_string.get()) #debug
    if (XY_Acceleration_string.get() != ""):
        XY_Acceleration = int(XY_Acceleration_string.get())
    print("XY_Acceleration text = ", XY_Acceleration) #debug

def up_Y_pos(*args):
    global Y_pos, XY_Step_size
    Y_pos += XY_Step_size

def down_Y_pos(*args):
    global Y_pos, XY_Step_size
    Y_pos -= XY_Step_size

def right_X_pos(*args):
    global X_pos, XY_Step_size
    X_pos += XY_Step_size

def left_X_pos(*args):
    global X_pos, XY_Step_size
    X_pos -= XY_Step_size

def update_XY_pos(*args):
    global X_pos, Y_pos
    if ((Im_X_pos_string.get() != "") & (Im_Y_pos_string.get() != "")):
        X_pos = int(Im_X_pos_string.get())
        Y_pos = int(Im_Y_pos_string.get())

def update_Z_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Z_pos
    Z_pos_string.set(Z_pos)
    root.after(250, update_Z_pos_string)

def update_Z_Step_size():
    global Z_Step_size
    Z_Step_size_string.set(Z_Step_size_spinbox.get())
    if (Z_Step_size_spinbox.get() != ""):
        Z_Step_size = int(Z_Step_size_spinbox.get())
    print("Z_Step_size = ", Z_Step_size) #debug

def update_Z_Step_size_text(*args):
    global Z_Step_size, Z_Step_size_string
    print("Z_Step_size string = " + Z_Step_size_string.get()) #debug
    if (Z_Step_size_string.get() != ""):
        Z_Step_size = int(Z_Step_size_string.get())
    print("Step size text = ", Z_Step_size) #debug

def update_Z_Speed():
    global Z_Speed, Z_Speed_spinbox
    Z_Speed_string.set(Z_Speed_spinbox.get())
    if (Z_Speed_spinbox.get() != ""):
        Z_Speed = int(Z_Speed_spinbox.get())
    print("Z_Speed = ", Z_Speed) #debug

def update_Z_Speed_text(*args):
    global Z_Speed, Z_Speed_string
    print("Z_Speed string = " + Z_Speed_string.get()) #debug
    if (Z_Speed_string.get() != ""):
        Z_Speed = int(Z_Speed_string.get())
    print("Z_Speed text = ", Z_Speed) #debug

def update_Z_Acceleration():
    global Z_Acceleration, Z_Acceleration_spinbox
    Z_Acceleration_string.set(Z_Acceleration_spinbox.get())
    if (Z_Acceleration_spinbox.get() != ""):
        Z_Acceleration = int(Z_Acceleration_spinbox.get())
    print("Z_Acceleration = ", Z_Acceleration) #debug

def update_Z_Acceleration_text(*args):
    global Z_Acceleration, Z_Acceleration_string
    print("Z_Acceleration string = " + Z_Acceleration_string.get()) #debug
    if (Z_Acceleration_string.get() != ""):
        Z_Acceleration = int(Z_Acceleration_string.get())
    print("Z_Acceleration text = ", Z_Acceleration) #debug

def up_Z_pos(*args):
    global Z_pos, Z_Step_size
    Z_pos += Z_Step_size

def down_Z_pos(*args):
    global Z_pos, Z_Step_size
    Z_pos -= Z_Step_size

def update_Z_pos(*argss):
    global Z_pos
    if (Im_Z_pos_string.get() != ""):
        Z_pos = int(Im_Z_pos_string.get())

def update_Angle_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Angle
    Angle_string.set(Angle)
    root.after(250, update_Angle_string)

def update_Angle_Step_size():
    global Angle_Step_size
    Angle_Step_size_string.set(Angle_Step_size_spinbox.get())
    if (Angle_Step_size_spinbox.get() != ""):
        Angle_Step_size = int(Angle_Step_size_spinbox.get())
    print("Angle_Step_size = ", Angle_Step_size) #debug

def update_Angle_Step_size_text(*args):
    global Angle_Step_size, Angle_Step_size_string
    print("Angle_Step_size string = " + Angle_Step_size_string.get()) #debug
    if (Angle_Step_size_string.get() != ""):
        Angle_Step_size = int(Angle_Step_size_string.get())
    print("Angle Step size text = ", Angle_Step_size) #debug

def update_Angle_Speed():
    global Angle_Speed, Angle_Speed_spinbox
    Angle_Speed_string.set(Angle_Speed_spinbox.get())
    if (Angle_Speed_spinbox.get() != ""):
        Angle_Speed = int(Angle_Speed_spinbox.get())
    print("Angle_Speed = ", Angle_Speed) #debug

def update_Angle_Speed_text(*args):
    global Angle_Speed, Angle_Speed_string
    print("Angle_Speed string = " + Angle_Speed_string.get()) #debug
    if (Angle_Speed_string.get() != ""):
        Angle_Speed = int(Angle_Speed_string.get())
    print("Angle_Speed text = ", Angle_Speed) #debug

def update_Angle_Acceleration():
    global Angle_Acceleration, Angle_Acceleration_spinbox
    Angle_Acceleration_string.set(Angle_Acceleration_spinbox.get())
    if (Angle_Acceleration_spinbox.get() != ""):
        Angle_Acceleration = int(Angle_Acceleration_spinbox.get())
    print("Angle_Acceleration = ", Angle_Acceleration) #debug

def update_Angle_Acceleration_text(*args):
    global Angle_Acceleration, Angle_Acceleration_string
    print("Angle_Acceleration string = " + Angle_Acceleration_string.get()) #debug
    if (Angle_Acceleration_string.get() != ""):
        Angle_Acceleration = int(Angle_Acceleration_string.get())
    print("Angle_Acceleration text = ", Angle_Acceleration) #debug

def up_Angle(*args):
    global Angle, Angle_Step_size
    Angle += Angle_Step_size

def down_Angle(*args):
    global Angle, Angle_Step_size
    Angle -= Angle_Step_size

def update_Angle(*args):
    global Angle
    if (Im_Angle_string.get() != ""):
        Angle = int(Im_Angle_string.get())

##Prior
def Prior_update_X_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_X_pos
    Prior_X_pos_string.set(Prior_X_pos)
    root.after(250, Prior_update_X_pos_string)

def Prior_update_Y_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_Y_pos
    Prior_Y_pos_string.set(Prior_Y_pos)
    root.after(250, Prior_update_Y_pos_string)

def Prior_update_XY_Step_size():
    global Prior_XY_Step_size
    Prior_XY_Step_size_string.set(Prior_XY_Step_size_spinbox.get())
    if (Prior_XY_Step_size_spinbox.get() != ""):
        Prior_XY_Step_size = int(Prior_XY_Step_size_spinbox.get())
    print("Prior_XY_Step_size = ", Prior_XY_Step_size) #debug

def Prior_update_XY_Step_size_text(*args):
    global Prior_XY_Step_size, Prior_XY_Step_size_string
    print("Prior_XY_Step_size string = " + Prior_XY_Step_size_string.get()) #debug
    if (Prior_XY_Step_size_string.get() != ""):
        Prior_XY_Step_size = int(Prior_XY_Step_size_string.get())
    print("Prior Step size text = ", Prior_XY_Step_size) #debug

def Prior_update_XY_Speed():
    global Prior_XY_Speed, Prior_XY_Speed_spinbox
    Prior_XY_Speed_string.set(Prior_XY_Speed_spinbox.get())
    if (Prior_XY_Speed_spinbox.get() != ""):
        Prior_XY_Speed = int(Prior_XY_Speed_spinbox.get())
    print("Prior_XY_Speed = ", Prior_XY_Speed) #debug

def Prior_update_XY_Speed_text(*args):
    global Prior_XY_Speed, Prior_XY_Speed_string
    print("Prior_XY_Speed string = " + Prior_XY_Speed_string.get()) #debug
    if (Prior_XY_Speed_string.get() != ""):
        Prior_XY_Speed = int(Prior_XY_Speed_string.get())
    print("Prior_XY_Speed text = ", Prior_XY_Speed) #debug

def Prior_update_XY_Acceleration():
    global Prior_XY_Acceleration, Prior_XY_Acceleration_spinbox
    Prior_XY_Acceleration_string.set(Prior_XY_Acceleration_spinbox.get())
    if (Prior_XY_Acceleration_spinbox.get() != ""):
        Prior_XY_Acceleration = int(Prior_XY_Acceleration_spinbox.get())
    print("Prior_XY_Acceleration = ", Prior_XY_Acceleration) #debug

def Prior_update_XY_Acceleration_text(*args):
    global Prior_XY_Acceleration, Prior_XY_Acceleration_string
    print("Prior_XY_Acceleration string = " + Prior_XY_Acceleration_string.get()) #debug
    if (Prior_XY_Acceleration_string.get() != ""):
        Prior_XY_Acceleration = int(Prior_XY_Acceleration_string.get())
    print("Prior_XY_Acceleration text = ", Prior_XY_Acceleration) #debug

def Prior_up_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size
    Prior_Y_pos += Prior_XY_Step_size

def Prior_down_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size
    Prior_Y_pos -= Prior_XY_Step_size

def Prior_right_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size
    Prior_X_pos += Prior_XY_Step_size

def Prior_left_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size
    Prior_X_pos -= Prior_XY_Step_size

def Prior_update_XY_pos(*args):
    global Prior_X_pos, Prior_Y_pos
    if ((Prior_Im_X_pos_string.get() != "") & (Prior_Im_Y_pos_string.get() != "")):
        Prior_X_pos = int(Prior_Im_X_pos_string.get())
        Prior_Y_pos = int(Prior_Im_Y_pos_string.get())

def Prior_update_Z_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_Z_pos
    Prior_Z_pos_string.set(Prior_Z_pos)
    root.after(250, Prior_update_Z_pos_string)

def Prior_update_Z_Step_size():
    global Prior_Z_Step_size
    Prior_Z_Step_size_string.set(Prior_Z_Step_size_spinbox.get())
    if (Prior_Z_Step_size_spinbox.get() != ""):
        Prior_Z_Step_size = int(Prior_Z_Step_size_spinbox.get())
    print("Prior_Z_Step_size = ", Prior_Z_Step_size) #debug

def Prior_update_Z_Step_size_text(*args):
    global Prior_Z_Step_size, Prior_Z_Step_size_string
    print("Prior_Z_Step_size string = " + Prior_Z_Step_size_string.get()) #debug
    if (Prior_Z_Step_size_string.get() != ""):
        Prior_Z_Step_size = int(Prior_Z_Step_size_string.get())
    print("Prior_Step size text = ", Prior_Z_Step_size) #debug

def Prior_update_Z_Speed():
    global Prior_Z_Speed, Prior_Z_Speed_spinbox
    Prior_Z_Speed_string.set(Prior_Z_Speed_spinbox.get())
    if (Prior_Z_Speed_spinbox.get() != ""):
        Prior_Z_Speed = int(Prior_Z_Speed_spinbox.get())
    print("Prior_Z_Speed = ", Prior_Z_Speed) #debug

def Prior_update_Z_Speed_text(*args):
    global Prior_Z_Speed, Prior_Z_Speed_string
    print("Prior_Z_Speed string = " + Prior_Z_Speed_string.get()) #debug
    if (Prior_Z_Speed_string.get() != ""):
        Prior_Z_Speed = int(Prior_Z_Speed_string.get())
    print("Prior_Z_Speed text = ", Prior_Z_Speed) #debug

def Prior_update_Z_Acceleration():
    global Prior_Z_Acceleration, Prior_Z_Acceleration_spinbox
    Prior_Z_Acceleration_string.set(Prior_Z_Acceleration_spinbox.get())
    if (Prior_Z_Acceleration_spinbox.get() != ""):
        Prior_Z_Acceleration = int(Prior_Z_Acceleration_spinbox.get())
    print("Prior_Z_Acceleration = ", Prior_Z_Acceleration) #debug

def Prior_update_Z_Acceleration_text(*args):
    global Prior_Z_Acceleration, Prior_Z_Acceleration_string
    print("Prior_Z_Acceleration string = " + Prior_Z_Acceleration_string.get()) #debug
    if (Prior_Z_Acceleration_string.get() != ""):
        Prior_Z_Acceleration = int(Prior_Z_Acceleration_string.get())
    print("Prior_Z_Acceleration text = ", Prior_Z_Acceleration) #debug

def Prior_up_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size
    Prior_Z_pos += Prior_Z_Step_size

def Prior_down_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size
    Prior_Z_pos -= Prior_Z_Step_size

def Prior_update_Z_pos(*argss):
    global Prior_Z_pos
    if (Prior_Im_Z_pos_string.get() != ""):
        Prior_Z_pos = int(Prior_Im_Z_pos_string.get())

# GUI Variable ################################
##TC200
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

T_current_string = StringVar()
T_current_string.set(T_current)

T_set_string = StringVar()
T_set_string.set(T_set.get())

P_value_string = StringVar()
P_value_string.set(P_value)
I_value_string = StringVar()
I_value_string.set(I_value)
D_value_string = StringVar()
D_value_string.set(D_value)

##KIM101
X_pos_string = StringVar()
X_pos_string.set(X_pos)
Y_pos_string = StringVar()
Y_pos_string.set(X_pos)

XY_Step_size_string = StringVar()
XY_Step_size_string.set(XY_Step_size)

XY_Speed_string = StringVar()
XY_Speed_string.set(XY_Speed)

XY_Acceleration_string = StringVar()
XY_Acceleration_string.set(XY_Acceleration)

Im_X_pos_string = StringVar()
Im_X_pos_string.set(0)

Im_Y_pos_string = StringVar()
Im_Y_pos_string.set(0)

Z_pos_string = StringVar()
Z_pos_string.set(Z_pos)

Z_Step_size_string = StringVar()
Z_Step_size_string.set(Z_Step_size)

Z_Speed_string = StringVar()
Z_Speed_string.set(Z_Speed)

Z_Acceleration_string = StringVar()
Z_Acceleration_string.set(Z_Acceleration)

Im_Z_pos_string = StringVar()
Im_Z_pos_string.set(0)

Angle_string = StringVar()
Angle_string.set(Z_pos)

Angle_Step_size_string = StringVar()
Angle_Step_size_string.set(Z_Step_size)

Angle_Speed_string = StringVar()
Angle_Speed_string.set(Z_Speed)

Angle_Acceleration_string = StringVar()
Angle_Acceleration_string.set(Z_Acceleration)

Im_Angle_string = StringVar()
Im_Angle_string.set(0)

##Prior
Prior_X_pos_string = StringVar()
Prior_X_pos_string.set(X_pos)
Prior_Y_pos_string = StringVar()
Prior_Y_pos_string.set(X_pos)

Prior_XY_Step_size_string = StringVar()
Prior_XY_Step_size_string.set(XY_Step_size)

Prior_XY_Speed_string = StringVar()
Prior_XY_Speed_string.set(XY_Speed)

Prior_XY_Acceleration_string = StringVar()
Prior_XY_Acceleration_string.set(XY_Acceleration)

Prior_Im_X_pos_string = StringVar()
Prior_Im_X_pos_string.set(0)

Prior_Im_Y_pos_string = StringVar()
Prior_Im_Y_pos_string.set(0)

Prior_Z_pos_string = StringVar()
Prior_Z_pos_string.set(Z_pos)

Prior_Z_Step_size_string = StringVar()
Prior_Z_Step_size_string.set(Z_Step_size)

Prior_Z_Speed_string = StringVar()
Prior_Z_Speed_string.set(Z_Speed)

Prior_Z_Acceleration_string = StringVar()
Prior_Z_Acceleration_string.set(Z_Acceleration)

Prior_Im_Z_pos_string = StringVar()
Prior_Im_Z_pos_string.set(0)
# GUI Setting ###################################################
root.title("PriorThorLab")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)
root.columnconfigure(7, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.rowconfigure(9, weight=1)
root.rowconfigure(10, weight=1)
root.rowconfigure(11, weight=1)
root.rowconfigure(12, weight=1)
root.rowconfigure(13, weight=1)
root.rowconfigure(14, weight=1)
root.rowconfigure(15, weight=1)
root.rowconfigure(16, weight=1)
root.rowconfigure(17, weight=1)
root.rowconfigure(18, weight=1)
root.rowconfigure(19, weight=1)
root.rowconfigure(20, weight=1)
root.rowconfigure(21, weight=1)
root.rowconfigure(22, weight=1)
root.rowconfigure(23, weight=1)
root.rowconfigure(24, weight=1)
root.rowconfigure(25, weight=1)
root.rowconfigure(26, weight=1)
root.rowconfigure(27, weight=1)
root.rowconfigure(28, weight=1)
root.rowconfigure(29, weight=1)
root.rowconfigure(30, weight=1)
root.rowconfigure(31, weight=1)

##TC200
T_title = Label(root, text="TC200 CONTROLLER", font=5)

T_current_label = Label(root, text="T_Current")
T_current_textblock = Label(root, textvariable=T_current_string, borderwidth=1, relief="groove")

T_set_label = Label(root, text="T_Set")
T_set_text = Entry(root, textvariable=T_set_string, validate="focusout", validatecommand=update_T_set_text)
T_set_string.trace_add("write", update_T_set_text)
T_set_slider = Scale(root, from_=20, to=150, orient="horizontal", variable=T_set, command=update_T_set, length=300)

P_value_label = Label(root, text="P")
P_value_spinbox = Spinbox(root, textvariable=P_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_P_value)
P_value_string.trace_add("write", update_P_value_text)

I_value_label = Label(root, text="I")
I_value_spinbox = Spinbox(root, textvariable=I_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_I_value)
I_value_string.trace_add("write", update_I_value_text)

D_value_label = Label(root, text="D")
D_value_spinbox = Spinbox(root, textvariable=D_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_D_value)
D_value_string.trace_add("write", update_D_value_text)

Start_plot_button = Button(root, text="Start Plot", command=start_temp)
Stop_plot_button = Button(root, text="Stop Plot", command=stop_temp)
# Reset_plot_button = Button(root, text="Reset Plot", command=reset_plot)

temp_KIM_seperator = ttk.Separator(root, orient="vertical")

##KIM 101
KIM_title = Label(root, text="KIM101 CONTROLLER", font=5)

XY_control_label = Label(root, text="XY AXIS CONTROL", height=2)
X_pos_label = Label(root, text="X Position")
X_pos_textblock = Label(root, textvariable=X_pos_string, borderwidth=1, relief="groove")

Y_pos_label = Label(root, text="Y Position")
Y_pos_textblock = Label(root, textvariable=Y_pos_string, borderwidth=1, relief="groove")

XY_Step_size_label = Label(root, text="Step Size (um)")
XY_Step_size_spinbox = Spinbox(root, textvariable=XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_XY_Step_size)
XY_Step_size_string.trace_add("write", update_XY_Step_size_text)

XY_Speed_label = Label(root, text="Speed (um/s)")
XY_Speed_spinbox = Spinbox(root, textvariable=XY_Speed_string, from_=Speed_min, to=Speed_max, command=update_XY_Speed)
XY_Speed_string.trace_add("write", update_XY_Speed_text)

XY_Acceleration_label = Label(root, text="Acceleration (um/s2)")
XY_Acceleration_spinbox = Spinbox(root, textvariable=XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_XY_Acceleration)
XY_Acceleration_string.trace_add("write", update_XY_Acceleration_text)

Left_button = Button(root, text="<", command=left_X_pos)
Right_button = Button(root, text=">", command=right_X_pos)
Up_button = Button(root, text="^", command=up_Y_pos)
Down_button = Button(root, text="v", command=down_Y_pos)

Im_X_pos_label = Label(root, text="Go to X pos (um)")
Im_X_pos_spinbox = Spinbox(root, textvariable=Im_X_pos_string, from_=Pos_min, to=Pos_max)

Im_Y_pos_label = Label(root, text="Go to Y pos (um)")
Im_Y_pos_spinbox = Spinbox(root, textvariable=Im_Y_pos_string, from_=Pos_min, to=Pos_max)

Go_to_XY_button = Button(root, text="Go to determined position", command=update_XY_pos)

Z_control_label = Label(root, text="Z AXIS CONTROL", height=2)
Z_pos_label = Label(root, text="Z Position")
Z_pos_textblock = Label(root, textvariable=Z_pos_string, borderwidth=1, relief="groove")

Z_Up_button = Button(root, text="^", command=up_Z_pos)
Z_Down_button = Button(root, text="v", command=down_Z_pos)

Z_Step_size_label = Label(root, text="Step Size (um)")
Z_Step_size_spinbox = Spinbox(root, textvariable=Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Z_Step_size)
Z_Step_size_string.trace_add("write", update_Z_Step_size_text)

Z_Speed_label = Label(root, text="Speed (um/s)")
Z_Speed_spinbox = Spinbox(root, textvariable=Z_Speed_string, from_=Speed_min, to=Speed_max, command=update_Z_Speed)
Z_Speed_string.trace_add("write", update_Z_Speed_text)

Z_Acceleration_label = Label(root, text="Acceleration (um/s2)")
Z_Acceleration_spinbox = Spinbox(root, textvariable=Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_Z_Acceleration)
Z_Acceleration_string.trace_add("write", update_Z_Acceleration_text)

Im_Z_pos_label = Label(root, text="Go to Z pos (um)")
Im_Z_pos_spinbox = Spinbox(root, textvariable=Im_Z_pos_string, from_=Pos_min, to=Pos_max)

Go_to_Z_button = Button(root, text="Go to determined position", command=update_Z_pos)

Angle_control_label = Label(root, text="ANGLE CONTROL")

Angle_label = Label(root, text="Angle Degree")
Angle_textblock = Label(root, textvariable=Angle_string, borderwidth=1, relief="groove")

Angle_Up_button = Button(root, text="^", command=up_Angle)
Angle_Down_button = Button(root, text="v", command=down_Angle)

Angle_Step_size_label = Label(root, text="Step Size (um)")
Angle_Step_size_spinbox = Spinbox(root, textvariable=Angle_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Angle_Step_size)
Angle_Step_size_string.trace_add("write", update_Angle_Step_size_text)

Angle_Speed_label = Label(root, text="Speed (um/s)")
Angle_Speed_spinbox = Spinbox(root, textvariable=Angle_Speed_string, from_=Speed_min, to=Speed_max, command=update_Angle_Speed)
Angle_Speed_string.trace_add("write", update_Angle_Speed_text)

Angle_Acceleration_label = Label(root, text="Acceleration (um/s2)")
Angle_Acceleration_spinbox = Spinbox(root, textvariable=Angle_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_Angle_Acceleration)
Angle_Acceleration_string.trace_add("write", update_Angle_Acceleration_text)

Im_Angle_label = Label(root, text="Go to Angle (degree)")
Im_Angle_spinbox = Spinbox(root, textvariable=Im_Angle_string, from_=Pos_min, to=Pos_max)

Go_to_Angle_button = Button(root, text="Go to determined position", command=update_Angle)

Filler1 = Label(root, text="")
Filler2 = Label(root, text="")

KIM_Prior_seperator = ttk.Separator(root, orient="vertical")
##Prior
Prior_title = Label(root, text="PRIOR CONTROLLER", font=5)

Prior_XY_control_label = Label(root, text="XY AXIS CONTROL", height=2)
Prior_X_pos_label = Label(root, text="X Position")
Prior_X_pos_textblock = Label(root, textvariable=Prior_X_pos_string, borderwidth=1, relief="groove")

Prior_Y_pos_label = Label(root, text="Y Position")
Prior_Y_pos_textblock = Label(root, textvariable=Prior_Y_pos_string, borderwidth=1, relief="groove")

Prior_XY_Step_size_label = Label(root, text="Step Size (um)")
Prior_XY_Step_size_spinbox = Spinbox(root, textvariable=Prior_XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_XY_Step_size)
Prior_XY_Step_size_string.trace_add("write", Prior_update_XY_Step_size_text)

Prior_XY_Speed_label = Label(root, text="Speed (um/s)")
Prior_XY_Speed_spinbox = Spinbox(root, textvariable=Prior_XY_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_XY_Speed)
Prior_XY_Speed_string.trace_add("write", Prior_update_XY_Speed_text)

Prior_XY_Acceleration_label = Label(root, text="Acceleration (um/s2)")
Prior_XY_Acceleration_spinbox = Spinbox(root, textvariable=Prior_XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_XY_Acceleration)
Prior_XY_Acceleration_string.trace_add("write", Prior_update_XY_Acceleration_text)

Prior_Left_button = Button(root, text="<", command=Prior_left_X_pos)
Prior_Right_button = Button(root, text=">", command=Prior_right_X_pos)
Prior_Up_button = Button(root, text="^", command=Prior_up_Y_pos)
Prior_Down_button = Button(root, text="v", command=Prior_down_Y_pos)

Prior_Im_X_pos_label = Label(root, text="Go to X pos (um)")
Prior_Im_X_pos_spinbox = Spinbox(root, textvariable=Prior_Im_X_pos_string, from_=Pos_min, to=Pos_max)

Prior_Im_Y_pos_label = Label(root, text="Go to Y pos (um)")
Prior_Im_Y_pos_spinbox = Spinbox(root, textvariable=Prior_Im_Y_pos_string, from_=Pos_min, to=Pos_max)

Prior_Go_to_XY_button = Button(root, text="Go to determined position", command=Prior_update_XY_pos)

Prior_Z_control_label = Label(root, text="Z AXIS CONTROL", height=2)
Prior_Z_pos_label = Label(root, text="Z Position")
Prior_Z_pos_textblock = Label(root, textvariable=Prior_Z_pos_string, borderwidth=1, relief="groove")

Prior_Z_Up_button = Button(root, text="^", command=Prior_up_Z_pos)
Prior_Z_Down_button = Button(root, text="v", command=Prior_down_Z_pos)

Prior_Z_Step_size_label = Label(root, text="Step Size (um)")
Prior_Z_Step_size_spinbox = Spinbox(root, textvariable=Prior_Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_Z_Step_size)
Prior_Z_Step_size_string.trace_add("write", Prior_update_Z_Step_size_text)

Prior_Z_Speed_label = Label(root, text="Speed (um/s)")
Prior_Z_Speed_spinbox = Spinbox(root, textvariable=Prior_Z_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_Z_Speed)
Prior_Z_Speed_string.trace_add("write", Prior_update_Z_Speed_text)

Prior_Z_Acceleration_label = Label(root, text="Acceleration (um/s2)")
Prior_Z_Acceleration_spinbox = Spinbox(root, textvariable=Prior_Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_Z_Acceleration)
Prior_Z_Acceleration_string.trace_add("write", Prior_update_Z_Acceleration_text)

Prior_Im_Z_pos_label = Label(root, text="Go to Z pos (um)")
Prior_Im_Z_pos_spinbox = Spinbox(root, textvariable=Prior_Im_Z_pos_string, from_=Pos_min, to=Pos_max)

Prior_Go_to_Z_button = Button(root, text="Go to determined position", command=Prior_update_Z_pos)

#GUI Placement ######################################################
root.grid_propagate(True)

##TC200
T_title.grid(column=0, row=0, columnspan=2, sticky="nsew")

canvas.get_tk_widget().grid(column=0, row=1, columnspan=2, sticky="nsew")
# canvas.get_tk_widget().grid_propagate(False)

T_current_label.grid(column=0, row=2, sticky="ew")
T_current_textblock.grid(column=1, row=2,sticky="ew")

T_set_label.grid(column=0, row=3, sticky="nsew")
T_set_text.grid(column=1, row=3, sticky="nsew")
T_set_slider.grid(columnspan=2, column=0, row=4)

P_value_label.grid(column=0, row=5, sticky="nsew")
P_value_spinbox.grid(column=1, row=5, sticky="nsew")

I_value_label.grid(column=0, row=6, sticky="nsew")
I_value_spinbox.grid(column=1, row=6, sticky="nsew")

D_value_label.grid(column=0, row=7, sticky="nsew")
D_value_spinbox.grid(column=1, row=7, sticky="nsew")

Start_plot_button.grid(column=0, row=8, sticky="nsew")
Stop_plot_button.grid(column=1, row=8, sticky="nsew")
# Reset_plot_button.grid(column=0, columnspan=2, row=9, sticky="nsew")

temp_KIM_seperator.grid(column=2, row=0, padx=5, rowspan=30, sticky="ns")

##KIM101
KIM_title.grid(column=3, row=0, columnspan=2, sticky="nsew")

XY_control_label.grid(column=3, row=1, columnspan=2, sticky="ew")

X_pos_label.grid(column=3, row=2, sticky="nsew")
X_pos_textblock.grid(column=4, row=2, sticky="nsew")

Y_pos_label.grid(column=3, row=3, sticky="ew")
Y_pos_textblock.grid(column=4, row=3, sticky="ew")

Im_X_pos_label.grid(column=3, row=4, sticky="nsew")
Im_X_pos_spinbox.grid(column=4, row=4, sticky="nsew")

Im_Y_pos_label.grid(column=3, row=5, sticky="nsew")
Im_Y_pos_spinbox.grid(column=4, row=5, sticky="nsew")

Go_to_XY_button.grid(column=3, row=6, columnspan=2, sticky="nsew")

Up_button.grid(column=3, row=7, sticky="nsew")
Down_button.grid(column=3, row=8, sticky="nsew")
Right_button.grid(column=4, row=7, sticky="nsew")
Left_button.grid(column=4, row=8, sticky="nsew")

XY_Step_size_label.grid(column=3, row=9, sticky="nsew")
XY_Step_size_spinbox.grid(column=4, row=9, sticky="nsew")

XY_Speed_label.grid(column=3, row=10, sticky="nsew")
XY_Speed_spinbox.grid(column=4, row=10, sticky="nsew")

XY_Acceleration_label.grid(column=3, row=11, sticky="nsew")
XY_Acceleration_spinbox.grid(column=4, row=11, sticky="nsew")

Z_control_label.grid(column=3, row=12, columnspan=2, sticky="nsew")

Z_pos_label.grid(column=3, row=13, sticky="nsew")
Z_pos_textblock.grid(column=4, row=13, sticky="nsew")

Im_Z_pos_label.grid(column=3, row=14, sticky="nsew")
Im_Z_pos_spinbox.grid(column=4, row=14, sticky="nsew")

Go_to_Z_button.grid(column=3, row=15, columnspan=2, sticky="nsew")

Z_Up_button.grid(column=3, row=16, columnspan=2, sticky="nsew")
Z_Down_button.grid(column=3, row=17, columnspan=2, sticky="nsew")

Z_Step_size_label.grid(column=3, row=18, sticky="nsew")
Z_Step_size_spinbox.grid(column=4, row=18, sticky="nsew")

Z_Speed_label.grid(column=3, row=19, sticky="nsew")
Z_Speed_spinbox.grid(column=4, row=19, sticky="nsew")

Z_Acceleration_label.grid(column=3, row=20, sticky="nsew")
Z_Acceleration_spinbox.grid(column=4, row=20, sticky="nsew")

Angle_control_label.grid(column=3, row=21, columnspan=2, sticky="nsew")

Angle_label.grid(column=3, row=22, sticky="nsew")
Angle_textblock.grid(column=4, row=22, sticky="nsew")

Im_Angle_label.grid(column=3, row=23, sticky="nsew")
Im_Angle_spinbox.grid(column=4, row=23, sticky="nsew")

Go_to_Angle_button.grid(column=3, row=24, columnspan=2, sticky="nsew")

Angle_Up_button.grid(column=3, row=25, columnspan=2, sticky="nsew")
Angle_Down_button.grid(column=3, row=26, columnspan=2, sticky="nsew")

Angle_Step_size_label.grid(column=3, row=27, sticky="nsew")
Angle_Step_size_spinbox.grid(column=4, row=27, sticky="nsew")

Angle_Speed_label.grid(column=3, row=28, sticky="nsew")
Angle_Speed_spinbox.grid(column=4, row=28, sticky="nsew")

Angle_Acceleration_label.grid(column=3, row=29, sticky="nsew")
Angle_Acceleration_spinbox.grid(column=4, row=29, sticky="nsew")

Filler1.grid(column=3, row=30)
Filler2.grid(column=3, row=31)

KIM_Prior_seperator.grid(column=5, row=0, padx=5, rowspan=30, sticky="ns")

##Prior
Prior_title.grid(column=6, row=0, columnspan=2, sticky="nsew")

Prior_XY_control_label.grid(column=6, row=1, columnspan=2, sticky="nsew")
Prior_XY_control_label.grid_propagate(False)

Prior_X_pos_label.grid(column=6, row=2, sticky="nsew")
Prior_X_pos_textblock.grid(column=7, row=2, sticky="nsew")

Prior_Y_pos_label.grid(column=6, row=3, sticky="ew")
Prior_Y_pos_textblock.grid(column=7, row=3, sticky="ew")

Prior_Im_X_pos_label.grid(column=6, row=4, sticky="nsew")
Prior_Im_X_pos_spinbox.grid(column=7, row=4, sticky="nsew")

Prior_Im_Y_pos_label.grid(column=6, row=5, sticky="nsew")
Prior_Im_Y_pos_spinbox.grid(column=7, row=5, sticky="nsew")

Prior_Go_to_XY_button.grid(column=6, row=6, columnspan=2, sticky="nsew")

Prior_Up_button.grid(column=6, row=7, sticky="nsew")
Prior_Down_button.grid(column=6, row=8, sticky="nsew")
Prior_Right_button.grid(column=7, row=7, sticky="nsew")
Prior_Left_button.grid(column=7, row=8, sticky="nsew")

Prior_XY_Step_size_label.grid(column=6, row=9, sticky="nsew")
Prior_XY_Step_size_spinbox.grid(column=7, row=9, sticky="nsew")

Prior_XY_Speed_label.grid(column=6, row=10, sticky="nsew")
Prior_XY_Speed_spinbox.grid(column=7, row=10, sticky="nsew")

Prior_XY_Acceleration_label.grid(column=6, row=11, sticky="nsew")
Prior_XY_Acceleration_spinbox.grid(column=7, row=11, sticky="nsew")

Prior_Z_control_label.grid(column=6, row=12, columnspan=2, sticky="nsew")

Prior_Z_pos_label.grid(column=6, row=13, sticky="nsew")
Prior_Z_pos_textblock.grid(column=7, row=13, sticky="nsew")

Prior_Im_Z_pos_label.grid(column=6, row=14, sticky="nsew")
Prior_Im_Z_pos_spinbox.grid(column=7, row=14, sticky="nsew")

Prior_Go_to_Z_button.grid(column=6, row=15, columnspan=2, sticky="nsew")

Prior_Z_Up_button.grid(column=6, row=16, columnspan=2, sticky="nsew")
Prior_Z_Down_button.grid(column=6, row=17, columnspan=2, sticky="nsew")

Prior_Z_Step_size_label.grid(column=6, row=18, sticky="nsew")
Prior_Z_Step_size_spinbox.grid(column=7, row=18, sticky="nsew")

Prior_Z_Speed_label.grid(column=6, row=19, sticky="nsew")
Prior_Z_Speed_spinbox.grid(column=7, row=19, sticky="nsew")

Prior_Z_Acceleration_label.grid(column=6, row=20, sticky="nsew")
Prior_Z_Acceleration_spinbox.grid(column=7, row=20, sticky="nsew")

#Variable update call 
root.after(1000, update_T_current)

root.after(250, update_X_pos_string)
root.after(250, update_Y_pos_string)
root.after(250, update_Z_pos_string)
root.after(250, update_Angle_string)


root.after(250, Prior_update_X_pos_string)
root.after(250, Prior_update_Y_pos_string)
root.after(250, Prior_update_Z_pos_string)

#Calling Tk mainloop
root.mainloop()