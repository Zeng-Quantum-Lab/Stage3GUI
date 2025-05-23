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
from prior import prior
from kim import kim
import instruments as ik
import instruments.units as u

#Machine variable initialization (Change COM port here)
tc = ik.thorlabs.TC200.open_serial("COM3", 115200)
pr = prior(5, r"C:\Users\zengl\Downloads\PriorThorLabGUI\PriorSDK1.9.2\PriorSDK 1.9.2\PriorSDK 1.9.2\examples\python\PriorScientificSDK.dll")

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
fig = Figure(figsize=(3,2.5), dpi = 85)

#Variable declaration ##################################
##TC200
T_current = 20.0

start_plot = False
curr_time = 0
time_list = [0]
T_current_list = [T_current]
plot1 = fig.add_subplot(111)
plot1.plot(time_list, T_current_list, "red")

T_set = IntVar()
T_set.set(20)

T_set_List = [T_set.get()]

P_value = 0
I_value = 0
D_value = 0

##KIM101
X_pos = 0 #debug variable 
Y_pos = 0 #debug variable

XY_Step_size = 1
XY_More_Setting_displacement = 2

XY_Speed = 1
XY_Acceleration = 1

Z_pos = 0 #debug variable

Z_Step_size = 1
Z_More_Setting_displacement = 2

Z_Speed = 1
Z_Acceleration = 1

Angle = 0 #debug variable

Angle_Step_size = 1
Angle_More_Setting_displacement = 2

Angle_Speed = 1
Angle_Acceleration = 1

##Prior
Prior_XY_Step_size = 1
Prior_XY_More_Setting_displacement = 2

try:
    Prior_X_pos = pr.x
    Prior_Y_pos = pr.y
    Prior_XY_Speed = pr.velocity
    Prior_XY_Acceleration = pr.acceleration
except Exception as e:
    print(e)

Prior_Z_Step_size = 1
Prior_Z_More_Setting_displacement = 2
Prior_Z_Speed = 1
Prior_Z_Acceleration = 1

Prior_Z_pos = 0 #debug variable
##Initialized Setting
try:
    pr.set_velocity(Prior_XY_Speed)
    pr.set_acceleration(Prior_XY_Acceleration)
except Exception as e:
    print(e)
#Update functions ################################

## TC200
def update_T_current(*args):
    global T_current, T_set, time_list, plot1, T_current_list, canvas, curr_time, start_plot,tc
    temp = f"{tc.temperature}"
    T_current = float(temp[:-5])
    T_current_string.set(T_current)
    if start_plot:
        curr_time += 1
        time_list.append(curr_time)
        T_current_list.append(T_current)
        T_set_List.append(T_set.get())
        plot1.plot(time_list, T_current_list, "red")
        plot1.plot(time_list, T_set_List, "blue")
        canvas.draw()
    else:
        T_current_list[-1] = T_current
        T_set_List[-1] = T_set.get()
    root.after(1000, update_T_current)

def update_T_set(value):
    global T_set, T_set_string, tc
    T_set.set(int(value))
    tc.temperature_set = T_set.get() * u.degC
    T_set_string.set(T_set.get())
    print("T_set slider = ", T_set.get()) #debug

def update_T_set_text(*args):
    global T_set, T_set_string
    print("T_set_string = " + T_set_string.get()) #debug
    if (T_set_string.get() != ""):
        T_set.set(int(T_set_string.get()))
        tc.temperature_set = T_set.get()

def update_P_value():
    global P_value
    # P_value_string.set(P_value_spinbox.get())
    # print(P_value_string)
    if (P_value_spinbox.get() != ""):
        P_value = int(P_value_spinbox.get())
        tc.p = P_value
    print("P_value = ", P_value) #debug

def update_P_value_text(*args):
    global P_value, P_value_string
    print("P_value string = ", P_value_string.get()) #debug
    if (P_value_string.get() != ""):
        P_value = int(P_value_string.get())
        tc.p = P_value
    print("P_value text = ", P_value) #debug

def update_I_value():
    global I_value
    I_value_string.set(I_value_spinbox.get())
    if (I_value_spinbox.get() != ""):
        I_value = int(I_value_spinbox.get())
        tc.i = I_value
    print("I_value = ", I_value) #debug

def update_I_value_text(*args):
    global I_value, I_value_string
    print("I_value string = " + I_value_string.get()) #debug
    if (I_value_string.get() != ""):
        I_value = int(I_value_string.get())
        tc.i = I_value
    print("I_value text = ", I_value) #debug

def update_D_value():
    global D_value
    D_value_string.set(D_value_spinbox.get())
    if (D_value_spinbox.get() != ""):
        D_value = int(D_value_spinbox.get())
        tc.d = D_value
    print("D_value = ", D_value) #debug

def update_D_value_text(*args):
    global D_value, D_value_string
    print("D_value string = ", D_value_string.get()) #debug
    if (D_value_string.get() != ""):
        D_value = int(D_value_string.get())
        tc.d = D_value
    print("D_value text = ", D_value) #debug

def start_temp(*args):
    global start_plot
    reset_plot()
    start_plot = True

def stop_temp(*args):
    global start_plot
    start_plot = False

def reset_plot(*args):
    global start_plot, time_list, T_current, T_current_list, fig, T_set, T_set_List
    plot1.clear()
    start_plot = False
    time_list = [0]
    T_current_list = [T_current]
    T_set_List = [T_set.get()]
    plot1.plot(time_list, T_current_list, "red")
    plot1.plot(time_list, T_set_List, "blue")
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

# def update_XY_pos(*args):
#     global X_pos, Y_pos
#     if ((Im_X_pos_string.get() != "") & (Im_Y_pos_string.get() != "")):
#         X_pos = int(Im_X_pos_string.get())
#         Y_pos = int(Im_Y_pos_string.get())

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

def XY_hide_Setting(*args):
    global XY_More_Setting_displacement, XY_More_Setting_frame, Z_More_Setting_displacement
    XY_More_Setting_displacement = 2
    XY_More_Setting_frame.grid_forget()
    Z_Label_frame.grid(column=0, row=18-XY_More_Setting_displacement, columnspan=2)
    Z_pos_label.grid(column=0, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=20-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=22-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_control_label.grid(column=0, row=25-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Up_button.grid(column=1, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Down_button.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Setting_frame.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")


def XY_show_Setting(*args):
    global XY_More_Setting_displacement, XY_More_Setting_frame, Z_More_Setting_displacement
    XY_More_Setting_displacement = 0
    XY_More_Setting_frame.grid(column=0, row=16, columnspan=2, rowspan=2, sticky="ns")
    Z_Label_frame.grid(column=0, row=18-XY_More_Setting_displacement, columnspan=2)
    Z_pos_label.grid(column=0, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=20-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=22-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_control_label.grid(column=0, row=25-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Up_button.grid(column=1, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Down_button.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Setting_frame.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")


def XY_hide_show_Setting(*args):
    global XY_More_Setting_displacement
    if (XY_More_Setting_displacement == 0):
        XY_hide_Setting()
    else:
        XY_show_Setting()

def Z_hide_Setting(*args):
    global Z_More_Setting_displacement, Z_More_Setting_frame
    Z_More_Setting_displacement = 2
    Z_More_Setting_frame.grid_forget()
    Z_Label_frame.grid(column=0, row=18-XY_More_Setting_displacement, columnspan=2)
    Z_pos_label.grid(column=0, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=20-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=22-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    Angle_control_label.grid(column=0, row=25-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Up_button.grid(column=1, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Down_button.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Setting_frame.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")


def Z_show_Setting(*args):
    global Z_More_Setting_displacement, Z_More_Setting_frame, XY_More_Setting_displacement
    Z_More_Setting_displacement = 0
    ##Literally regrid the entire half of the GUI
    Z_Label_frame.grid(column=0, row=18-XY_More_Setting_displacement, columnspan=2)
    Z_pos_label.grid(column=0, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=19-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=20-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=22-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    Z_More_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_control_label.grid(column=0, row=25-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Up_button.grid(column=1, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Down_button.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_Setting_frame.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def Z_hide_show_Setting(*args):
    global Z_More_Setting_displacement
    if (Z_More_Setting_displacement == 0):
        Z_hide_Setting()
    else:
        Z_show_Setting()

def Angle_hide_Setting(*args):
    global Angle_More_Setting_displacement, Angle_More_Setting_frame
    Angle_More_Setting_displacement = 2
    Angle_More_Setting_frame.grid_forget()

def Angle_show_Setting(*args):
    global Angle_More_Setting_displacement, Angle_More_Setting_frame
    Angle_More_Setting_displacement = 0
    Angle_More_Setting_frame.grid(column=0, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def Angle_hide_show_Setting(*args):
    global Angle_More_Setting_displacement
    if (Angle_More_Setting_displacement == 0):
        Angle_hide_Setting()
    else:
        Angle_show_Setting()

##Prior
def Prior_update_X_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_X_pos, pr
    pr.get_curr_pos()
    Prior_X_pos_string.set(pr.x)
    # root.after(250, Prior_update_X_pos_string)

def Prior_update_Y_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_Y_pos, pr
    pr.get_curr_pos()
    Prior_Y_pos_string.set(pr.y)
    # root.after(250, Prior_update_Y_pos_string)

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
        pr.set_velocity(Prior_XY_Speed)
    print("Prior_XY_Speed = ", Prior_XY_Speed) #debug

def Prior_update_XY_Speed_text(*args):
    global Prior_XY_Speed, Prior_XY_Speed_string
    print("Prior_XY_Speed string = " + Prior_XY_Speed_string.get()) #debug
    if (Prior_XY_Speed_string.get() != ""):
        Prior_XY_Speed = int(Prior_XY_Speed_string.get())
        pr.set_velocity(Prior_XY_Speed)
    print("Prior_XY_Speed text = ", Prior_XY_Speed) #debug

def Prior_update_XY_Acceleration():
    global Prior_XY_Acceleration, Prior_XY_Acceleration_spinbox
    Prior_XY_Acceleration_string.set(Prior_XY_Acceleration_spinbox.get())
    if (Prior_XY_Acceleration_spinbox.get() != ""):
        Prior_XY_Acceleration = int(Prior_XY_Acceleration_spinbox.get())
        pr.set_acceleration(Prior_XY_Acceleration)
    print("Prior_XY_Acceleration = ", Prior_XY_Acceleration) #debug

def Prior_update_XY_Acceleration_text(*args):
    global Prior_XY_Acceleration, Prior_XY_Acceleration_string
    print("Prior_XY_Acceleration string = " + Prior_XY_Acceleration_string.get()) #debug
    if (Prior_XY_Acceleration_string.get() != ""):
        Prior_XY_Acceleration = int(Prior_XY_Acceleration_string.get())
        pr.set_acceleration(Prior_XY_Acceleration)
    print("Prior_XY_Acceleration text = ", Prior_XY_Acceleration) #debug

def Prior_up_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos
    Prior_Y_pos -= Prior_XY_Step_size
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_down_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos
    Prior_Y_pos += Prior_XY_Step_size
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_right_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos
    Prior_X_pos += Prior_XY_Step_size
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_left_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos
    Prior_X_pos -= Prior_XY_Step_size
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

# def Prior_update_XY_pos(*args):
#     global Prior_X_pos, Prior_Y_pos
#     if ((Prior_Im_X_pos_string.get() != "") & (Prior_Im_Y_pos_string.get() != "")):
#         Prior_X_pos = int(Prior_Im_X_pos_string.get())
#         Prior_Y_pos = int(Prior_Im_Y_pos_string.get())

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

# def Prior_update_Z_pos(*argss):
#     global Prior_Z_pos
#     if (Prior_Im_Z_pos_string.get() != ""):
#         Prior_Z_pos = int(Prior_Im_Z_pos_string.get())

def Prior_XY_hide_Setting(*args):
    global Prior_XY_More_Setting_displacement, Prior_XY_More_Setting_frame
    Prior_XY_More_Setting_displacement = 2
    Prior_XY_More_Setting_frame.grid_forget()
    Prior_Z_Label_frame.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2)

    Prior_Z_pos_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")
    Prior_Z_pos_textblock.grid(column=4, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")

    Prior_Z_button_frame.grid(column=3, row=20- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)

    Prior_Z_Setting_frame.grid(column=3, row=22-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_More_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")

    Prior_Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
    Prior_Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
    Prior_Z_Setting_button.grid(column=2, columnspan=2, row=0, sticky="nsew")
    
    Prior_Z_Speed_label.grid(column=0, row=0, sticky="nsew")
    Prior_Z_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

    Prior_Z_Acceleration_label.grid(column=0, row=1, sticky="nsew")
    Prior_Z_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")
    

def Prior_XY_show_Setting(*args):
    global Prior_XY_More_Setting_displacement, Prior_XY_More_Setting_frame
    Prior_XY_More_Setting_displacement = 0
    Prior_XY_More_Setting_frame.grid(column=3, row=16, columnspan=2, rowspan=2, sticky="ns")
    Prior_Z_Label_frame.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2)

    Prior_Z_pos_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")
    Prior_Z_pos_textblock.grid(column=4, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")

    Prior_Z_button_frame.grid(column=3, row=20- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)
    Prior_Z_Setting_frame.grid(column=3, row=22-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_More_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")

    Prior_Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
    Prior_Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
    Prior_Z_Setting_button.grid(column=2, columnspan=2, row=0, sticky="nsew")
    
    Prior_Z_Speed_label.grid(column=0, row=0, sticky="nsew")
    Prior_Z_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

    Prior_Z_Acceleration_label.grid(column=0, row=1, sticky="nsew")
    Prior_Z_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")

def Prior_XY_hide_show_Setting(*args):
    global Prior_XY_More_Setting_displacement
    if (Prior_XY_More_Setting_displacement == 0):
        Prior_XY_hide_Setting()
    else:
        Prior_XY_show_Setting()

def Prior_Z_hide_Setting(*args):
    global Prior_Z_More_Setting_displacement, Prior_Z_More_Setting_frame
    Prior_Z_More_Setting_displacement = 2
    Prior_Z_More_Setting_frame.grid_forget()

def Prior_Z_show_Setting(*args):
    global Prior_Z_More_Setting_displacement, Prior_Z_More_Setting_frame
    Prior_Z_More_Setting_displacement = 0
    Prior_Z_More_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")

def Prior_Z_hide_show_Setting(*args):
    global Prior_Z_More_Setting_displacement
    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_hide_Setting()
    else:
        Prior_Z_show_Setting()

def on_close():
    pr.disconnect()
    root.destroy()

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
Prior_X_pos_string.set(Prior_X_pos)
Prior_Y_pos_string = StringVar()
Prior_Y_pos_string.set(Prior_Y_pos)

Prior_XY_Step_size_string = StringVar()
Prior_XY_Step_size_string.set(Prior_XY_Step_size)

Prior_XY_Speed_string = StringVar()
Prior_XY_Speed_string.set(Prior_XY_Speed)

Prior_XY_Acceleration_string = StringVar()
Prior_XY_Acceleration_string.set(Prior_XY_Acceleration)

Prior_Z_pos_string = StringVar()
Prior_Z_pos_string.set(Prior_Z_pos)

Prior_Z_Step_size_string = StringVar()
Prior_Z_Step_size_string.set(Prior_Z_Step_size)

Prior_Z_Speed_string = StringVar()
Prior_Z_Speed_string.set(Prior_Z_Speed)

Prior_Z_Acceleration_string = StringVar()
Prior_Z_Acceleration_string.set(Prior_Z_Acceleration)

# GUI Setting ###################################################
root.title("PriorThorLab")
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=8)
root.columnconfigure(2, weight=0)
root.columnconfigure(3, weight=10)
root.columnconfigure(4, weight=1)

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
root.rowconfigure(32, weight=1)

##TC200

TC_frame = Frame(root)

TC_frame.columnconfigure(0, weight=1)
TC_frame.columnconfigure(1, weight=1)

TC_frame.rowconfigure(0, weight=1)
TC_frame.rowconfigure(1, weight=1)
TC_frame.rowconfigure(2, weight=1)
TC_frame.rowconfigure(3, weight=1)
TC_frame.rowconfigure(4, weight=1)
TC_frame.rowconfigure(5, weight=1)
TC_frame.rowconfigure(6, weight=1)
TC_frame.rowconfigure(7, weight=1)

normal_font = "Helvetica 11"

T_title = Label(TC_frame, text="TC200 CONTROLLER", font="Helvetica 13")

T_current_label = Label(TC_frame, text="T_Current", font=normal_font)
T_current_textblock = Label(TC_frame, textvariable=T_current_string, borderwidth=1, relief="groove")

T_set_label = Label(TC_frame, text="T_Set", font=normal_font)
T_set_text = Entry(TC_frame, textvariable=T_set_string, validate="focusout", validatecommand=update_T_set_text)
T_set_string.trace_add("write", update_T_set_text)
T_set_slider = Scale(TC_frame, from_=20, to=150, orient="horizontal", variable=T_set, command=update_T_set, length=200)

P_value_label = Label(TC_frame, text="P", font=normal_font)
P_value_spinbox = Spinbox(TC_frame, textvariable=P_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_P_value)
P_value_string.trace_add("write", update_P_value_text)

I_value_label = Label(TC_frame, text="I", font=normal_font)
I_value_spinbox = Spinbox(TC_frame, textvariable=I_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_I_value)
I_value_string.trace_add("write", update_I_value_text)

D_value_label = Label(TC_frame, text="D",font=normal_font)
D_value_spinbox = Spinbox(TC_frame, textvariable=D_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_D_value)
D_value_string.trace_add("write", update_D_value_text)

Start_plot_button = Button(TC_frame, text="Start Plot", command=start_temp)
Stop_plot_button = Button(TC_frame, text="Stop Plot", command=stop_temp)
# Reset_plot_button = Button(root, text="Reset Plot", command=reset_plot)

temp_KIM_seperator = ttk.Separator(root, orient="vertical")

##KIM 101
KIM_title = Label(root, text="KIM101 CONTROLLER", font="Helvetica 13")
XY_control_label = Label(root, text="XY AXIS CONTROL", height=2, font=normal_font)
X_pos_label = Label(root, text="X Position", font=normal_font)
X_pos_textblock = Label(root, textvariable=X_pos_string, borderwidth=1, relief="groove")

Y_pos_label = Label(root, text="Y Position", font=normal_font)
Y_pos_textblock = Label(root, textvariable=Y_pos_string, borderwidth=1, relief="groove")

XY_Setting_frame = Frame(root)
XY_Step_size_label = Label(XY_Setting_frame, text="Step", font=normal_font)
XY_Step_size_spinbox = Spinbox(XY_Setting_frame, textvariable=XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_XY_Step_size, width=10)
XY_Step_size_string.trace_add("write", update_XY_Step_size_text)
Hide_button = Button(XY_Setting_frame, text="Speed Setting", command=XY_hide_show_Setting)

XY_More_Setting_frame = Frame(root)

XY_Speed_label = Label(XY_More_Setting_frame, text="Speed (μm/s)")
XY_Speed_spinbox = Spinbox(XY_More_Setting_frame, textvariable=XY_Speed_string, from_=Speed_min, to=Speed_max, command=update_XY_Speed)
XY_Speed_string.trace_add("write", update_XY_Speed_text)

XY_Acceleration_label = Label(XY_More_Setting_frame, text="Accel (μm/s²)")
XY_Acceleration_spinbox = Spinbox(XY_More_Setting_frame, textvariable=XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_XY_Acceleration)
XY_Acceleration_string.trace_add("write", update_XY_Acceleration_text)

KIM_button_frame = Frame(root)

Left_button = Button(KIM_button_frame, text="◄", command=left_X_pos, font=5, width=3, height=1)
Right_button = Button(KIM_button_frame, text="►", command=right_X_pos, font=5, width=3, height=1)
Up_button = Button(KIM_button_frame, text="▲", command=up_Y_pos, font=5, width=3, height=1)
Down_button = Button(KIM_button_frame, text="▼", command=down_Y_pos, font=5, width=3, height=1)

Left_forward_button = Button(KIM_button_frame, text="⏪")
Right_forward_button = Button(KIM_button_frame, text="⏩")
Up_forward_button = Button(KIM_button_frame, text="⏫")
Down_forward_button = Button(KIM_button_frame, text="⏬")


Z_Label_frame = Frame(root)

XY_Z_seperator = ttk.Separator(Z_Label_frame, orient="horizontal")

Z_control_label = Label(Z_Label_frame, text="Z AXIS CONTROL", height=2,font=normal_font)
Z_pos_label = Label(root, text="Z Position",font=normal_font)
Z_pos_textblock = Label(root, textvariable=Z_pos_string, borderwidth=1, relief="groove")

Z_button_frame = Frame(root)

Z_Up_button = Button(Z_button_frame, text="▲", command=up_Z_pos, width=4, height=2)
Z_Down_button = Button(Z_button_frame, text="▼", command=down_Z_pos, width=4, height=2)

Z_Up_forward_button = Button(Z_button_frame, text="⏫", width=4, height=2)
Z_Down_forward_button = Button(Z_button_frame, text="⏬", width=4, height=2)

Z_Setting_frame = Frame(root)

Z_Step_size_label = Label(Z_Setting_frame, text="Step",font=normal_font)
Z_Step_size_spinbox = Spinbox(Z_Setting_frame, textvariable=Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Z_Step_size, width=10)
Z_Step_size_string.trace_add("write", update_Z_Step_size_text)

Z_Setting_button = Button(Z_Setting_frame, text="Speed Setting", command=Z_hide_show_Setting)

Z_More_Setting_frame = Frame(root)

Z_Speed_label = Label(Z_More_Setting_frame, text="Speed (μm/s)")
Z_Speed_spinbox = Spinbox(Z_More_Setting_frame, textvariable=Z_Speed_string, from_=Speed_min, to=Speed_max, command=update_Z_Speed)
Z_Speed_string.trace_add("write", update_Z_Speed_text)

Z_Acceleration_label = Label(Z_More_Setting_frame, text="Accel (μm/s2)")
Z_Acceleration_spinbox = Spinbox(Z_More_Setting_frame, textvariable=Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_Z_Acceleration)
Z_Acceleration_string.trace_add("write", update_Z_Acceleration_text)

Angle_control_label = Label(root, text="ANGLE CONTROL",font=normal_font)

Angle_label = Label(root, text="Angle Degree",font=normal_font)
Angle_textblock = Label(root, textvariable=Angle_string, borderwidth=1, relief="groove")

Angle_Up_button = Button(root, text="↷", command=up_Angle)
Angle_Down_button = Button(root, text="↶", command=down_Angle)

Angle_Setting_frame = Frame(root)

Angle_Step_size_label = Label(Angle_Setting_frame, text="Step",font=normal_font)
Angle_Step_size_spinbox = Spinbox(Angle_Setting_frame, textvariable=Angle_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Angle_Step_size, width=10)
Angle_Step_size_string.trace_add("write", update_Angle_Step_size_text)

Angle_Setting_button = Button(Angle_Setting_frame, text="Speed Setting", command=Angle_hide_show_Setting)

Angle_More_Setting_frame = Frame(root)

Angle_Speed_label = Label(Angle_More_Setting_frame, text="Speed (μm/s)")
Angle_Speed_spinbox = Spinbox(Angle_More_Setting_frame, textvariable=Angle_Speed_string, from_=Speed_min, to=Speed_max, command=update_Angle_Speed)
Angle_Speed_string.trace_add("write", update_Angle_Speed_text)

Angle_Acceleration_label = Label(Angle_More_Setting_frame, text="Accel (μm/s2)")
Angle_Acceleration_spinbox = Spinbox(Angle_More_Setting_frame, textvariable=Angle_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_Angle_Acceleration)
Angle_Acceleration_string.trace_add("write", update_Angle_Acceleration_text)

Filler1 = Label(root, text="")
Filler2 = Label(root, text="")

KIM_Prior_seperator = ttk.Separator(root, orient="vertical")
##Prior
Prior_title = Label(root, text="ProScan III CONTROLLER", font="Helvetica 13")

Prior_XY_control_label = Label(root, text="XY AXIS CONTROL",font=normal_font)
Prior_X_pos_label = Label(root, text="X Position",font=normal_font)
Prior_X_pos_textblock = Label(root, borderwidth=1,textvariable=Prior_X_pos_string, relief="groove")

Prior_Y_pos_label = Label(root, text="Y Position",font=normal_font)
Prior_Y_pos_textblock = Label(root, borderwidth=1,textvariable=Prior_Y_pos_string, relief="groove")

Prior_XY_Setting_frame = Frame(root)

Prior_Setting_button = Button(Prior_XY_Setting_frame, text="Speed Setting", command=Prior_XY_hide_show_Setting)
Prior_XY_Step_size_label = Label(Prior_XY_Setting_frame, text="Step",font=normal_font)
Prior_XY_Step_size_spinbox = Spinbox(Prior_XY_Setting_frame, textvariable=Prior_XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_XY_Step_size, width=10)
Prior_XY_Step_size_string.trace_add("write", Prior_update_XY_Step_size_text)

Prior_XY_More_Setting_frame = Frame(root)

Prior_XY_Speed_label = Label(Prior_XY_More_Setting_frame, text="Speed (μm/s)")
Prior_XY_Speed_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_XY_Speed)
Prior_XY_Speed_string.trace_add("write", Prior_update_XY_Speed_text)

Prior_XY_Acceleration_label = Label(Prior_XY_More_Setting_frame, text="Accel (μm/s2)")
Prior_XY_Acceleration_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_XY_Acceleration)
Prior_XY_Acceleration_string.trace_add("write", Prior_update_XY_Acceleration_text)

Prior_button_frame = Frame(root)

Prior_Left_button = Button(Prior_button_frame, text="◄", command=Prior_left_X_pos, font=5, width=3, height=1)
Prior_Right_button = Button(Prior_button_frame, text="►", command=Prior_right_X_pos, font=5, width=3, height=1)
Prior_Up_button = Button(Prior_button_frame, text="▲", command=Prior_up_Y_pos, font=5, width=3, height=1)
Prior_Down_button = Button(Prior_button_frame, text="▼", command=Prior_down_Y_pos, font=5, width=3, height=1)

Prior_Left_forward_button = Button(Prior_button_frame, text="⏪")
Prior_Right_forward_button = Button(Prior_button_frame, text="⏩")
Prior_Up_forward_button = Button(Prior_button_frame, text="⏫")
Prior_Down_forward_button = Button(Prior_button_frame, text="⏬")

Prior_Z_Label_frame = Frame(root)
Prior_Z_Label_seperator = ttk.Separator(Prior_Z_Label_frame, orient="horizontal")
Prior_Z_control_label = Label(Prior_Z_Label_frame, text="Z AXIS CONTROL",font=normal_font)

Prior_Z_pos_label = Label(root, text="Z Position",font=normal_font)
Prior_Z_pos_textblock = Label(root, borderwidth=1, textvariable=Prior_Z_pos_string, relief="groove")

Prior_Z_button_frame = Frame(root)

Prior_Z_Up_button = Button(Prior_Z_button_frame, text="▲", command=Prior_up_Z_pos, width=4, height=2)
Prior_Z_Down_button = Button(Prior_Z_button_frame, text="▼", command=Prior_down_Z_pos, width=4, height=2)

Prior_Z_Up_forward_button = Button(Prior_Z_button_frame, text="⏫",width=4, height=2)
Prior_Z_Down_forward_button = Button(Prior_Z_button_frame, text="⏬",width=4, height=2)

Prior_Z_Setting_frame = Frame(root)

Prior_Z_Step_size_label = Label(Prior_Z_Setting_frame, text="Step",font=normal_font)
Prior_Z_Step_size_spinbox = Spinbox(Prior_Z_Setting_frame, textvariable=Prior_Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_Z_Step_size, width=10)
Prior_Z_Step_size_string.trace_add("write", Prior_update_Z_Step_size_text)
Prior_Z_Setting_button = Button(Prior_Z_Setting_frame, text="Speed Setting", command=Prior_Z_hide_show_Setting)

Prior_Z_More_Setting_frame = Frame(root)

Prior_Z_Speed_label = Label(Prior_Z_More_Setting_frame, text="Speed (μm/s)")
Prior_Z_Speed_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_Z_Speed)
Prior_Z_Speed_string.trace_add("write", Prior_update_Z_Speed_text)

Prior_Z_Acceleration_label = Label(Prior_Z_More_Setting_frame, text="Accel (μm/s2)")
Prior_Z_Acceleration_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_Z_Acceleration)
Prior_Z_Acceleration_string.trace_add("write", Prior_update_Z_Acceleration_text)

#GUI Placement ######################################################
root.grid_propagate(True)

##TC200
canvas.get_tk_widget().grid(column=0, row=1, columnspan=4, rowspan=6, sticky="nsew")

TC_frame.grid(column=4,row=0, sticky="nsew", rowspan=7, columnspan=1)

T_title.grid(column=0, row=0, columnspan=2, sticky="nsew")

T_current_label.grid(column=0, row=1, sticky="nsew")
T_current_textblock.grid(column=1,row=1,sticky="nsew")

T_set_label.grid(column=0, row=2, sticky="nsew")
T_set_text.grid(column=1, row=2, sticky="nsew")
T_set_slider.grid(columnspan=2, column=0, row=3)

P_value_label.grid(column=0, row=4, sticky="nsew")
P_value_spinbox.grid(column=1, row=4, sticky="nsew")

I_value_label.grid(column=0, row=5, sticky="nsew")
I_value_spinbox.grid(column=1, row=5, sticky="nsew")

D_value_label.grid(column=0, row=6, sticky="nsew")
D_value_spinbox.grid(column=1, row=6, sticky="nsew")

Start_plot_button.grid(column=0, row=7, sticky="nsew")
Stop_plot_button.grid(column=1, row=7, sticky="nsew")
# Reset_plot_button.grid(column=0, columnspan=2, row=9, sticky="nsew")

# temp_KIM_seperator.grid(column=2, row=0, padx=5, rowspan=30, sticky="ns")

##KIM101
KIM_title.grid(column=0, row=9, columnspan=2, sticky="nsew")

XY_control_label.grid(column=0, row=10, columnspan=2, sticky="ew")

X_pos_label.grid(column=0, row=11, sticky="nsew")
X_pos_textblock.grid(column=1, row=11, sticky="nsew")

Y_pos_label.grid(column=0, row=12, sticky="nsew")
Y_pos_textblock.grid(column=1, row=12, sticky="nsew")


KIM_button_frame.grid(column=0, row=13, rowspan=2, columnspan=2, sticky="ns")

Up_forward_button.grid(column=2, row=0, sticky="nsew")
Up_button.grid(column=2, row=1, sticky="nsew")

Down_forward_button.grid(column=2, row=4, sticky="nsew")
Down_button.grid(column=2, row=3, sticky="nsew")

Right_button.grid(column=3, row=2, sticky="nsew")
Right_forward_button.grid(column=4, row=2, sticky="nsew")

Left_forward_button.grid(column=0, row=2, sticky="nsew")
Left_button.grid(column=1, row=2, sticky="nsew")

XY_Setting_frame.grid(column=0, row=15, columnspan=2, sticky="ns")

XY_Step_size_label.grid(column=0, row=0, sticky="nsew")
XY_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Hide_button.grid(column=2, columnspan=2, row=0, sticky="nsew")

# XY_More_Setting_frame.grid(column=0, row=16, columnspan=2, rowspan=2, sticky="ns")

XY_Speed_label.grid(column=0, row=0, sticky="nsew")
XY_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

XY_Acceleration_label.grid(column=0, row=1, sticky="nsew")
XY_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")

Z_Label_frame.grid(column=0, row=18-XY_More_Setting_displacement, columnspan=2)

XY_Z_seperator.grid(column=0, columnspan=2, row=0, sticky="nsew")
Z_control_label.grid(column=0, columnspan=2, row=1, sticky="nsew")

Z_pos_label.grid(column=0, row=19-XY_More_Setting_displacement, sticky="nsew")
Z_pos_textblock.grid(column=1, row=19-XY_More_Setting_displacement, sticky="nsew")

Z_button_frame.grid(column=0, row=20-XY_More_Setting_displacement, rowspan=2, columnspan=2)

Z_Up_forward_button.grid(column=1, row=0)
Z_Up_button.grid(column=0, row=0)
Z_Down_button.grid(column=0, row=1)
Z_Down_forward_button.grid(column=1, row=1)

Z_Setting_frame.grid(column=0, row=22-XY_More_Setting_displacement, columnspan=2, sticky="ns")

Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Z_Setting_button.grid(column=2, row=0, sticky="nsew", columnspan=2)

Z_Speed_label.grid(column=0, row=0, sticky="nsew")
Z_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

Z_Acceleration_label.grid(column=0, row=1, sticky="nsew")
Z_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")

Angle_control_label.grid(column=0, row=25-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")

Angle_label.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
Angle_textblock.grid(column=1, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")

Angle_Up_button.grid(column=1, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
Angle_Down_button.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")

Angle_Setting_frame.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")

Angle_Step_size_label.grid(column=0, row=0, sticky="nsew")
Angle_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Angle_Setting_button.grid(column=2, row=0, columnspan=2, sticky="nsew")

# Angle_More_Setting_frame.grid(column=0, row=29, rowspan=2, columnspan=2, sticky="ns")
Angle_Speed_label.grid(column=0, row=0, sticky="nsew")
Angle_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

Angle_Acceleration_label.grid(column=0, row=1, sticky="nsew")
Angle_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")

# Filler1.grid(column=0, row=31, sticky="nsew")
# Filler2.grid(column=1, row=32, sticky="nsew")

KIM_Prior_seperator.grid(column=2, row=9, padx=5, rowspan=31, sticky="ns")

##Prior
Prior_title.grid(column=3, row=9, columnspan=2, sticky="nsew")

Prior_XY_control_label.grid(column=3, row=10, columnspan=2, sticky="nsew")

Prior_X_pos_label.grid(column=3, row=11, sticky="nsew")
Prior_X_pos_textblock.grid(column=4, row=11, sticky="nsew")

Prior_Y_pos_label.grid(column=3, row=12, sticky="nsew")
Prior_Y_pos_textblock.grid(column=4, row=12, sticky="nsew")

# Prior_Im_X_pos_label.grid(column=3, row=4, sticky="nsew")
# Prior_Im_X_pos_spinbox.grid(column=4, row=4, sticky="nsew")

# Prior_Im_Y_pos_label.grid(column=3, row=5, sticky="nsew")
# Prior_Im_Y_pos_spinbox.grid(column=4, row=5, sticky="nsew")

# Prior_Go_to_XY_button.grid(column=3, row=3, columnspan=2, sticky="nsew")

# Prior_button_frame.rowconfigure(0, weight=1)
# Prior_button_frame.rowconfigure(1, weight=1)
# Prior_button_frame.rowconfigure(2, weight=1)

# Prior_button_frame.columnconfigure(0, weight=1)
# Prior_button_frame.columnconfigure(1, weight=1)
# Prior_button_frame.columnconfigure(2, weight=1)

Prior_button_frame.grid(column=3, row=13, rowspan=2, columnspan=2)

Prior_Up_button.grid(column=2, row=1, sticky="nsew")
Prior_Up_forward_button.grid(column=2, row=0, sticky="nsew")

Prior_Down_button.grid(column=2, row=3, sticky="nsew")
Prior_Down_forward_button.grid(column=2, row=4, sticky="nsew")

Prior_Right_button.grid(column=3, row=2, sticky="nsew")
Prior_Right_forward_button.grid(column=4, row=2, sticky="nsew")

Prior_Left_button.grid(column=1, row=2, sticky="nsew")
Prior_Left_forward_button.grid(column=0, row=2, sticky="nsew")

Prior_XY_Setting_frame.grid(column=3, row=15, columnspan=2, sticky="ns")

Prior_Setting_button.grid(column=2, row=0, columnspan=2, sticky="nsew")
Prior_XY_Step_size_label.grid(column=0, row=0, sticky="nsew")
Prior_XY_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")

# Prior_XY_More_Setting_frame.grid(column=3, row=16, columnspan=2, rowspan=2, sticky="ns")

Prior_XY_Speed_label.grid(column=0, row=0, sticky="nsew")
Prior_XY_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

Prior_XY_Acceleration_label.grid(column=0, row=1, sticky="nsew")
Prior_XY_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")

Prior_Z_Label_frame.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2)
Prior_Z_Label_seperator.grid(column=0, row=0, columnspan=2, sticky="nsew")
Prior_Z_control_label.grid(column=0, row=1, columnspan=2, sticky="nsew")

Prior_Z_pos_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")
Prior_Z_pos_textblock.grid(column=4, row=19-Prior_XY_More_Setting_displacement, sticky="nsew")

Prior_Z_button_frame.grid(column=3, row=20- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)

Prior_Z_Up_button.grid(column=0, row=0)
Prior_Z_Down_button.grid(column=0, row=1)

Prior_Z_Up_forward_button.grid(column=1, row=0)
Prior_Z_Down_forward_button.grid(column=1, row=1)

Prior_Z_Setting_frame.grid(column=3, row=22-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

Prior_Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
Prior_Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Prior_Z_Setting_button.grid(column=2, columnspan=2, row=0, sticky="nsew")

# Prior_Z_More_Setting_frame.grid(column=3, row=23, columnspan=2, rowspan=2, sticky="ns")

Prior_Z_Speed_label.grid(column=0, row=0, sticky="nsew")
Prior_Z_Speed_spinbox.grid(column=1, row=0, sticky="nsew")

Prior_Z_Acceleration_label.grid(column=0, row=1, sticky="nsew")
Prior_Z_Acceleration_spinbox.grid(column=1, row=1, sticky="nsew")


#Variable update call
root.after(1000, update_T_current)

root.after(250, update_X_pos_string)
root.after(250, update_Y_pos_string)
root.after(250, update_Z_pos_string)
root.after(250, update_Angle_string)

Prior_update_X_pos_string()
Prior_update_Y_pos_string()
root.after(250, Prior_update_Z_pos_string)

#Calling Tk mainloop
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
