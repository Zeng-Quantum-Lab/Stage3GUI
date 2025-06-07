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
try:
    tc = ik.thorlabs.TC200.open_serial("COM3", 115200)
except:
    print("Cannot find TC200 Controller")

try:
    pr = prior(5, r"C:\Users\zengl\Downloads\PriorThorLabGUI\PriorSDK1.9.2\PriorSDK 1.9.2\PriorSDK 1.9.2\examples\python\PriorScientificSDK.dll")
except:
    print("Cannot find Prior Controller")

try:
    kim_obj = kim("97251106")
except:
    print("Cannot find KIM101 Controller")

#Constant declaration
Temperature_PID_Max = 500
Temperature_PID_Min = -500

Pos_max = 1000000000
Pos_min = -1000000000

Step_size_max = 10000000
Step_size_min = -10000000

Acceleration_max = 10000000
Acceleration_min = -10000000

Speed_max = 10000000
Speed_min = -10000000

Coeff_size_max = 1000000000
Coeff_size_min = 0

Backlash_Dist_min = -1000000000
Backlash_Dist_max = 1000000000

# Window declaration
root = Tk() 
fig = Figure(figsize=(3,2), dpi = 85)

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
T_set_scale = IntVar()
T_set_scale.set(T_set.get())

T_set_List = [T_set.get()]

PID_displacement = 3

P_value = tc.p
I_value = tc.i
D_value = tc.d

##KIM101
XY_is_Con = False
Z_is_Con = False
Angle_is_Con = False

X_pos = kim_obj.x
Y_pos = kim_obj.y

XY_Step_size = 1
XY_coeff = 1
XY_More_Setting_displacement = 2

XY_Speed = kim_obj.xy_velocity
XY_Acceleration = kim_obj.xy_acceleration

left_X_isHold = False
right_X_isHold = False
up_Y_isHold = False
down_Y_isHold = False

Z_pos = kim_obj.z

Z_Step_size = 1
Z_coeff = 1
Z_More_Setting_displacement = 2

Z_Speed = kim_obj.z_velocity
Z_Acceleration = kim_obj.z_acceleration

up_Z_isHold = False
down_Z_isHold = False

Angle = kim_obj.angle

Angle_Step_size = 1
Angle_coeff = 1
Angle_More_Setting_displacement = 2

Angle_Speed = kim_obj.angle_velocity
Angle_Acceleration = kim_obj.angle_acceleration

up_Angle_isHold = False
down_Angle_isHold = False

##Prior
Prior_XY_is_Con = False
Prior_Z_is_Con = False

Prior_XY_Step_size = 1
Prior_XY_coeff = 1
Prior_XY_More_Setting_displacement = 2

Prior_X_pos = pr.x
Prior_Y_pos = pr.y
Prior_XY_Speed = pr.velocity
Prior_XY_Acceleration = pr.acceleration
Prior_XY_Backlash_EN = IntVar(value=pr.backlash_en)
print("Prior_XY_Backlash_EN = ", Prior_XY_Backlash_EN)
Prior_XY_Backlash_Dist = pr.backlash_dist


Prior_left_X_isHold = False
Prior_right_X_isHold = False
Prior_up_X_isHold = False
Prior_down_X_isHold = False

Prior_Z_Step_size = 1
Prior_Z_coeff = 1
Prior_Z_More_Setting_displacement = 2
Prior_Z_Speed = pr.z_velocity
Prior_Z_Acceleration = pr.z_acceleration
Prior_Z_Backlash_EN = IntVar(value=pr.backlash_en)
Prior_Z_Backlash_Dist = pr.backlash_dist

Prior_Z_pos = 0 #debug variable

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

def update_T_set(*args):
    global T_set, T_set_string, tc, T_set_scale
    print("T_set_scale = ", T_set_scale.get())
    T_set.set(T_set_scale.get())
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

def show_PID(*args):
    global PID_displacement, TC_PID_frame, Start_plot_button, Stop_plot_button
    PID_displacement = 0
    TC_PID_frame.grid(column=0, row=5, columnspan=2, rowspan=3)
    Start_plot_button.grid(column=0, row=8-PID_displacement, sticky="nsew")
    Stop_plot_button.grid(column=1, row=8-PID_displacement, sticky="nsew")
    canvas.get_tk_widget().grid(column=0, row=1, columnspan=4, rowspan=7, sticky="nsew")

def hide_PID(*args):
    global PID_displacement, TC_PID_frame, Start_plot_button, Stop_plot_button
    PID_displacement = 3
    TC_PID_frame.grid_forget()
    Start_plot_button.grid(column=0, row=8-PID_displacement, sticky="nsew")
    Stop_plot_button.grid(column=1, row=8-PID_displacement, sticky="nsew")
    canvas.get_tk_widget().grid(column=0, row=1, columnspan=4, rowspan=7, sticky="nsew")

def hide_show_PID(*args):
    if PID_displacement == 3:
        show_PID()
    else:
        hide_PID()

## KIM101
def update_X_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global X_pos
    if (XY_is_Con):
        time.sleep(0.25)
    X_pos = kim_obj.get_x_pos()
    X_pos_string.set(X_pos)

def update_Y_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Y_pos, Y_pos_string
    if (XY_is_Con):
        time.sleep(0.25)
    Y_pos = kim_obj.get_y_pos()
    Y_pos_string.set(Y_pos)

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
    print("Step (μm) size text = ", XY_Step_size) #debug

def update_XY_coeff():
    global XY_coeff, XY_coeff_spinbox
    XY_coeff_string.set(XY_coeff_spinbox.get())
    if (XY_coeff_spinbox.get() != ""):
        XY_coeff = int(XY_coeff_spinbox.get())
    print("XY_coeff = ", XY_coeff) #debug

def update_XY_coeff_text(*args):
    global XY_coeff, XY_coeff_string
    print("XY_coeff string = " + XY_coeff_string.get()) #debug
    if (XY_coeff_string.get() != ""):
        XY_coeff = int(XY_coeff_string.get())
    print("XY_coeff text = ", XY_coeff) #debug

def update_XY_Speed():
    global XY_Speed, XY_Speed_spinbox
    XY_Speed_string.set(XY_Speed_spinbox.get())
    if (XY_Speed_spinbox.get() != ""):
        XY_Speed = int(XY_Speed_spinbox.get())
        kim_obj.set_xy_velocity(XY_Speed)
    print("XY_Speed = ", XY_Speed) #debug

def update_XY_Speed_text(*args):
    global XY_Speed, XY_Speed_string
    print("XY_Speed string = " + XY_Speed_string.get()) #debug
    if (XY_Speed_string.get() != ""):
        XY_Speed = int(XY_Speed_string.get())
        kim_obj.set_xy_velocity(XY_Speed)
    print("XY_Speed text = ", XY_Speed) #debug

def update_XY_Acceleration():
    global XY_Acceleration, XY_Acceleration_spinbox
    XY_Acceleration_string.set(XY_Acceleration_spinbox.get())
    if (XY_Acceleration_spinbox.get() != ""):
        XY_Acceleration = int(XY_Acceleration_spinbox.get())
        kim_obj.set_xy_acceleration(XY_Acceleration)
    print("XY_Acceleration = ", XY_Acceleration) #debug

def update_XY_Acceleration_text(*args):
    global XY_Acceleration, XY_Acceleration_string
    print("XY_Acceleration string = " + XY_Acceleration_string.get()) #debug
    if (XY_Acceleration_string.get() != ""):
        XY_Acceleration = int(XY_Acceleration_string.get())
        kim_obj.set_xy_acceleration(XY_Acceleration)
    print("XY_Acceleration text = ", XY_Acceleration) #debug

def up_Y_pos(*args):
    global Y_pos, XY_Step_size, XY_coeff
    Y_pos += XY_Step_size * XY_coeff
    kim_obj.go_to_Ypos(Y_pos)
    update_Y_pos_string()

def x10_up_Y_pos(*args):
    global Y_pos, XY_Step_size, XY_coeff
    Y_pos += XY_Step_size * XY_coeff * 10
    kim_obj.go_to_Ypos(Y_pos)
    update_Y_pos_string()

def hold_right_X_pos(*args):
    kim_obj.start_forward_x_motor()
    update_X_pos_string()

def release_X_pos(*args):
    kim_obj.stop_x_motor()
    update_X_pos_string()

def hold_left_X_pos(*args):
    kim_obj.start_backward_x_motor()
    update_X_pos_string()

def hold_up_Y_pos(*args):
    kim_obj.start_forward_y_motor()
    update_Y_pos_string()

def release_Y_pos(*args):
    kim_obj.stop_y_motor()
    update_Y_pos_string()

def hold_down_Y_pos(*args):
    kim_obj.start_backward_y_motor()
    update_Y_pos_string()

def continuous_setup(*args):
    #x1 Button Setup
    global Up_button, Down_button, Right_button, Left_button
    Up_button.unbind("<ButtonRelease-1>")
    Up_button.bind("<Button-1>", hold_up_Y_pos)
    Up_button.bind("<ButtonRelease-1>", release_Y_pos)

    Down_button.unbind("<ButtonRelease-1>")
    Down_button.bind("<Button-1>", hold_down_Y_pos)
    Down_button.bind("<ButtonRelease-1>", release_Y_pos)

    Right_button.unbind("<ButtonRelease-1>")
    Right_button.bind("<Button-1>", hold_right_X_pos)
    Right_button.bind("<ButtonRelease-1>", release_X_pos)

    Left_button.unbind("<ButtonRelease-1>")
    Left_button.bind("<Button-1>", hold_left_X_pos)
    Left_button.bind("<ButtonRelease-1>", release_X_pos)

    #x10 Button Setup
    global Up_x10_button, Down_x10_button, Right_x10_button, Left_x10_button
    Up_x10_button.unbind("<ButtonRelease-1>")
    Up_x10_button.bind("<Button-1>", hold_up_Y_pos)
    Up_x10_button.bind("<ButtonRelease-1>", release_Y_pos)

    Down_x10_button.unbind("<ButtonRelease-1>")
    Down_x10_button.bind("<Button-1>", hold_down_Y_pos)
    Down_x10_button.bind("<ButtonRelease-1>", release_Y_pos)

    Right_x10_button.unbind("<ButtonRelease-1>")
    Right_x10_button.bind("<Button-1>", hold_right_X_pos)
    Right_x10_button.bind("<ButtonRelease-1>", release_X_pos)

    Left_x10_button.unbind("<ButtonRelease-1>")
    Left_x10_button.bind("<Button-1>", hold_left_X_pos)
    Left_x10_button.bind("<ButtonRelease-1>", release_X_pos)


def discreet_setup(*args):
    #x1 Button Setup
    global Up_button, Down_button, Right_button, Left_button, Up_x10_button, Down_x10_button, Right_x10_button, Left_x10_button
    Up_button.unbind("<Button-1>")
    Up_button.unbind("<ButtonRelease-1>")
    Up_button.bind("<ButtonRelease-1>", up_Y_pos)

    Down_button.unbind("<Button-1>")
    Down_button.unbind("<ButtonRelease-1>")
    Down_button.bind("<ButtonRelease-1>", down_Y_pos)

    Right_button.unbind("<Button-1>")
    Right_button.unbind("<ButtonRelease-1>")
    Right_button.bind("<ButtonRelease-1>", right_X_pos)

    Left_button.unbind("<Button-1>")
    Left_button.unbind("<ButtonRelease-1>")
    Left_button.bind("<ButtonRelease-1>", left_X_pos)
    
    #x10 Button setup
    Up_x10_button.unbind("<Button-1>")
    Up_x10_button.unbind("<ButtonRelease-1>")
    Up_x10_button.bind("<ButtonRelease-1>", x10_up_Y_pos)

    Down_x10_button.unbind("<Button-1>")
    Down_x10_button.unbind("<ButtonRelease-1>")
    Down_x10_button.bind("<ButtonRelease-1>", x10_down_Y_pos)

    Right_x10_button.unbind("<Button-1>")
    Right_x10_button.unbind("<ButtonRelease-1>")
    Right_x10_button.bind("<ButtonRelease-1>", x10_right_X_pos)

    Left_x10_button.unbind("<Button-1>")
    Left_x10_button.unbind("<ButtonRelease-1>")
    Left_x10_button.bind("<ButtonRelease-1>", x10_left_X_pos)

def down_Y_pos(*args):
    global Y_pos, XY_Step_size, XY_coeff
    Y_pos -= XY_Step_size * XY_coeff
    kim_obj.go_to_Ypos(Y_pos)
    update_Y_pos_string()

def x10_down_Y_pos(*args):
    global Y_pos, XY_Step_size, XY_coeff
    Y_pos -= XY_Step_size * XY_coeff * 10
    kim_obj.go_to_Ypos(Y_pos)
    update_Y_pos_string()

def right_X_pos(*args):
    global X_pos, XY_Step_size, XY_coeff
    X_pos += XY_Step_size * XY_coeff
    kim_obj.go_to_Xpos(X_pos)
    update_X_pos_string()

def x10_right_X_pos(*args):
    global X_pos, XY_Step_size, XY_coeff
    X_pos += XY_Step_size * XY_coeff * 10
    kim_obj.go_to_Xpos(X_pos)
    update_X_pos_string()

def left_X_pos(*args):
    global X_pos, XY_Step_size, XY_coeff
    X_pos -= XY_Step_size * XY_coeff
    kim_obj.go_to_Xpos(X_pos)
    update_X_pos_string()

def left_hold_X_pos(*args):
    global X_pos, XY_Step_size, XY_coeff
    X_pos -= XY_Step_size * XY_coeff
    kim_obj.go_to_Xpos(X_pos)
    update_X_pos_string()

def x10_left_X_pos(*args):
    global X_pos, XY_Step_size, XY_coeff
    X_pos -= XY_Step_size * XY_coeff * 10
    kim_obj.go_to_Xpos(X_pos)
    update_X_pos_string()

def update_Z_pos_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Z_pos, kim_obj
    if Z_is_Con:
        time.sleep(0.25)
    Z_pos = kim_obj.get_z_pos()
    Z_pos_string.set(Z_pos)

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
    print("Step (μm) size text = ", Z_Step_size) #debug

def update_Z_coeff():
    global Z_coeff, Z_coeff_spinbox
    Z_coeff_string.set(Z_coeff_spinbox.get())
    if (Z_coeff_spinbox.get() != ""):
        Z_coeff = int(Z_coeff_spinbox.get())
    print("Z_coeff = ", Z_coeff) #debug

def update_Z_coeff_text(*args):
    global Z_coeff, Z_coeff_string
    print("Z_coeff string = " + Z_coeff_string.get()) #debug
    if (Z_coeff_string.get() != ""):
        Z_coeff = int(Z_coeff_string.get())
    print("Z_coeff text = ", Z_coeff) #debug

def update_Z_Speed():
    global Z_Speed, Z_Speed_spinbox
    Z_Speed_string.set(Z_Speed_spinbox.get())
    if (Z_Speed_spinbox.get() != ""):
        Z_Speed = int(Z_Speed_spinbox.get())
        kim_obj.set_z_velocity(Z_Speed)
    print("Z_Speed = ", Z_Speed) #debug

def update_Z_Speed_text(*args):
    global Z_Speed, Z_Speed_string
    print("Z_Speed string = " + Z_Speed_string.get()) #debug
    if (Z_Speed_string.get() != ""):
        Z_Speed = int(Z_Speed_string.get())
        kim_obj.set_z_velocity(Z_Speed)
    print("Z_Speed text = ", Z_Speed) #debug

def update_Z_Acceleration():
    global Z_Acceleration, Z_Acceleration_spinbox
    Z_Acceleration_string.set(Z_Acceleration_spinbox.get())
    if (Z_Acceleration_spinbox.get() != ""):
        Z_Acceleration = int(Z_Acceleration_spinbox.get())
        kim_obj.set_z_acceleration(Z_Acceleration)
    print("Z_Acceleration = ", Z_Acceleration) #debug

def update_Z_Acceleration_text(*args):
    global Z_Acceleration, Z_Acceleration_string
    print("Z_Acceleration string = " + Z_Acceleration_string.get()) #debug
    if (Z_Acceleration_string.get() != ""):
        Z_Acceleration = int(Z_Acceleration_string.get())
        kim_obj.set_z_acceleration(Z_Acceleration)
    print("Z_Acceleration text = ", Z_Acceleration) #debug

def up_Z_pos(*args):
    global Z_pos, Z_Step_size, Z_coeff
    Z_pos -= Z_Step_size * Z_coeff
    kim_obj.go_to_Zpos(Z_pos)
    update_Z_pos_string()

def x10_up_Z_pos(*args):
    global Z_pos, Z_Step_size, Z_coeff
    Z_pos -= Z_Step_size * Z_coeff * 10
    kim_obj.go_to_Zpos(Z_pos)
    update_Z_pos_string()

def down_Z_pos(*args):
    global Z_pos, Z_Step_size, Z_coeff
    Z_pos += Z_Step_size * Z_coeff
    kim_obj.go_to_Zpos(Z_pos)
    update_Z_pos_string()

def x10_down_Z_pos(*args):
    global Z_pos, Z_Step_size, Z_coeff
    Z_pos += Z_Step_size * Z_coeff * 10
    kim_obj.go_to_Zpos(Z_pos)
    update_Z_pos_string()

def hold_up_Z_pos(*args):
    kim_obj.start_forward_z_motor()
    update_Z_pos_string()

def release_Z_pos(*args):
    kim_obj.stop_z_motor()
    update_Z_pos_string()

def hold_down_Z_pos(*args):
    kim_obj.start_backward_z_motor()
    update_Z_pos_string()

def Z_continuous_setup(*args):
    global Z_Up_button, Z_Down_button
    Z_Up_button.unbind("<ButtonRelease-1>")
    Z_Up_button.bind("<Button-1>", hold_up_Z_pos)
    Z_Up_button.bind("<ButtonRelease-1>", release_Z_pos)

    Z_Down_button.unbind("<ButtonRelease-1>")
    Z_Down_button.bind("<Button-1>", hold_down_Z_pos)
    Z_Down_button.bind("<ButtonRelease-1>", release_Z_pos)

    global Z_Up_x10_button, Z_Down_x10_button
    Z_Up_x10_button.unbind("<ButtonRelease-1>")
    Z_Up_x10_button.bind("<Button-1>", hold_up_Z_pos)
    Z_Up_x10_button.bind("<ButtonRelease-1>", release_Z_pos)

    Z_Down_x10_button.unbind("<ButtonRelease-1>")
    Z_Down_x10_button.bind("<Button-1>", hold_down_Z_pos)
    Z_Down_x10_button.bind("<ButtonRelease-1>", release_Z_pos)

def Z_discreet_setup(*args):
    global Z_Up_button, Z_Down_button
    Z_Up_button.unbind("<Button-1>")
    Z_Up_button.unbind("<ButtonRelease-1>")
    Z_Up_button.bind("<ButtonRelease-1>", up_Z_pos)

    Z_Down_button.unbind("<Button-1>")
    Z_Down_button.unbind("<ButtonRelease-1>")
    Z_Down_button.bind("<ButtonRelease-1>", down_Z_pos)

    global Z_Up_x10_button, Z_Down_x10_button
    Z_Up_x10_button.unbind("<Button-1>")
    Z_Up_x10_button.unbind("<ButtonRelease-1>")
    Z_Up_x10_button.bind("<ButtonRelease-1>", x10_up_Z_pos)

    Z_Down_x10_button.unbind("<Button-1>")
    Z_Down_x10_button.unbind("<ButtonRelease-1>")
    Z_Down_x10_button.bind("<ButtonRelease-1>", x10_down_Z_pos)


def update_Angle_string(*args): #Check with KIM101 API, not global variable (i.e unfinished)
    global Angle, kim_obj
    if Angle_is_Con:
        time.sleep(0.25)
    Angle = kim_obj.get_angle_pos()
    Angle_string.set(Angle)

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
    print("Angle Step (μm) size text = ", Angle_Step_size) #debug

def update_Angle_coeff():
    global Angle_coeff, Angle_coeff_spinbox
    Angle_coeff_string.set(Angle_coeff_spinbox.get())
    if (Angle_coeff_spinbox.get() != ""):
        Angle_coeff = int(Angle_coeff_spinbox.get())
    print("Angle_coeff = ", Angle_coeff) #debug

def update_Angle_coeff_text(*args):
    global Angle_coeff, Angle_coeff_string
    print("Angle_coeff string = " + Angle_coeff_string.get()) #debug
    if (Angle_coeff_string.get() != ""):
        Angle_coeff = int(Angle_coeff_string.get())
    print("Angle_coeff text = ", Angle_coeff) #debug

def update_Angle_Speed():
    global Angle_Speed, Angle_Speed_spinbox
    Angle_Speed_string.set(Angle_Speed_spinbox.get())
    if (Angle_Speed_spinbox.get() != ""):
        Angle_Speed = int(Angle_Speed_spinbox.get())
        kim_obj.set_Angle_velocity(Angle_Speed)
    print("Angle_Speed = ", Angle_Speed) #debug

def update_Angle_Speed_text(*args):
    global Angle_Speed, Angle_Speed_string
    print("Angle_Speed string = " + Angle_Speed_string.get()) #debug
    if (Angle_Speed_string.get() != ""):
        Angle_Speed = int(Angle_Speed_string.get())
        kim_obj.set_Angle_velocity(Angle_Speed)
    print("Angle_Speed text = ", Angle_Speed) #debug

def update_Angle_Acceleration():
    global Angle_Acceleration, Angle_Acceleration_spinbox
    Angle_Acceleration_string.set(Angle_Acceleration_spinbox.get())
    if (Angle_Acceleration_spinbox.get() != ""):
        Angle_Acceleration = int(Angle_Acceleration_spinbox.get())
        kim_obj.set_Angle_acceleration(Angle_Acceleration)
    print("Angle_Acceleration = ", Angle_Acceleration) #debug

def update_Angle_Acceleration_text(*args):
    global Angle_Acceleration, Angle_Acceleration_string
    print("Angle_Acceleration string = " + Angle_Acceleration_string.get()) #debug
    if (Angle_Acceleration_string.get() != ""):
        Angle_Acceleration = int(Angle_Acceleration_string.get())
        kim_obj.set_Angle_acceleration(Angle_Acceleration)
    print("Angle_Acceleration text = ", Angle_Acceleration) #debug

def up_Angle(*args):
    global Angle, Angle_Step_size, Angle_coeff
    Angle += Angle_Step_size * Angle_coeff
    kim_obj.go_to_Angle(Angle)
    update_Angle_string()

def x10_up_Angle(*args):
    global Angle, Angle_Step_size, Angle_coeff
    Angle += Angle_Step_size * Angle_coeff * 10
    kim_obj.go_to_Angle(Angle)
    update_Angle_string()

def down_Angle(*args):
    global Angle, Angle_Step_size, Angle_coeff
    Angle -= Angle_Step_size * Angle_coeff
    kim_obj.go_to_Angle(Angle)
    update_Angle_string()

def x10_down_Angle(*args):
    global Angle, Angle_Step_size, Angle_coeff
    Angle -= Angle_Step_size * Angle_coeff * 10
    kim_obj.go_to_Angle(Angle)
    update_Angle_string()

def hold_up_Angle_pos(*args):
    kim_obj.start_forward_angle_motor()
    update_Angle_string()

def release_Angle_pos(*args):
    kim_obj.stop_angle_motor()
    update_Angle_string()

def hold_down_Angle_pos(*args):
    kim_obj.start_backward_angle_motor()
    update_Angle_string()

def Angle_continuous_setup(*args):
    global Angle_Up_button, Angle_Down_button
    Angle_Up_button.unbind("<ButtonRelease-1>")
    Angle_Up_button.bind("<Button-1>", hold_up_Angle_pos)
    Angle_Up_button.bind("<ButtonRelease-1>", release_Angle_pos)

    Angle_Down_button.unbind("<ButtonRelease-1>")
    Angle_Down_button.bind("<Button-1>", hold_down_Angle_pos)
    Angle_Down_button.bind("<ButtonRelease-1>", release_Angle_pos)

def Angle_discreet_setup(*args):
    global Angle_Up_button, Angle_Down_button
    Angle_Up_button.unbind("<Button-1>")
    Angle_Up_button.unbind("<ButtonRelease-1>")
    Angle_Up_button.bind("<ButtonRelease-1>", up_Angle)

    Angle_Down_button.unbind("<Button-1>")
    Angle_Down_button.unbind("<ButtonRelease-1>")
    Angle_Down_button.bind("<ButtonRelease-1>", down_Angle)

def XY_hide_Setting(*args):
    global XY_More_Setting_displacement, XY_More_Setting_frame, Z_More_Setting_displacement
    XY_More_Setting_displacement = 2
    XY_More_Setting_frame.grid_forget()
    XY_Z_seperator.grid(column=0, columnspan=2, row=18-XY_More_Setting_displacement, sticky="ew")
    Z_control_label.grid(column=0, row=19-XY_More_Setting_displacement, columnspan=2, sticky="nsew")
    Z_pos_label.grid(column=0, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=21-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=24-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_seperator.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ew")
    Angle_control_label.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_button_frame.grid(column=0, columnspan=2, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement)
    Angle_Setting_frame.grid(column=0, row=30-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=31-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")


def XY_show_Setting(*args):
    global XY_More_Setting_displacement, XY_More_Setting_frame, Z_More_Setting_displacement
    XY_More_Setting_displacement = 0
    XY_More_Setting_frame.grid(column=0, row=16, columnspan=2, rowspan=2, sticky="ns")
    XY_Z_seperator.grid(column=0, columnspan=2, row=18-XY_More_Setting_displacement, sticky="ew")
    Z_control_label.grid(column=0, row=19-XY_More_Setting_displacement, columnspan=2, sticky="nsew")
    Z_pos_label.grid(column=0, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=21-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=24-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_seperator.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ew")
    Angle_control_label.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_button_frame.grid(column=0, columnspan=2, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement)
    Angle_Setting_frame.grid(column=0, row=30-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=31-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def XY_hide_show_Setting(*args):
    global XY_More_Setting_displacement
    if (XY_More_Setting_displacement == 0):
        XY_hide_Setting()
    else:
        XY_show_Setting()

def update_XY_modetoCon(*args):
    global XY_is_Con, Con_button, Dis_button
    if XY_is_Con == False:
        Con_button.configure(relief="sunken")
        Dis_button.configure(relief="raised")
        XY_is_Con = True
        continuous_setup()
    print("XY_is_Con = ", XY_is_Con)

def update_XY_modetoDis(*args):
    global XY_is_Con, Con_button, Dis_button
    if XY_is_Con == True:
        Con_button.configure(relief="raised")
        Dis_button.configure(relief="sunken")
        XY_is_Con = False
        discreet_setup()
    print("XY_is_Con = ", XY_is_Con)

def Z_hide_Setting(*args):
    global Z_More_Setting_displacement, Z_More_Setting_frame
    Z_More_Setting_displacement = 2
    Z_More_Setting_frame.grid_forget()
    XY_Z_seperator.grid(column=0, columnspan=2, row=18-XY_More_Setting_displacement, sticky="ew")
    Z_control_label.grid(column=0, row=19-XY_More_Setting_displacement, columnspan=2, sticky="nsew")
    Z_pos_label.grid(column=0, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=21-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=24-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_seperator.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ew")
    Angle_control_label.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_button_frame.grid(column=0, columnspan=2, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement)
    Angle_Setting_frame.grid(column=0, row=30-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=31-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def Z_show_Setting(*args):
    global Z_More_Setting_displacement, Z_More_Setting_frame, XY_More_Setting_displacement
    Z_More_Setting_displacement = 0
    ##Literally regrid the entire half of the GUI
    XY_Z_seperator.grid(column=0, columnspan=2, row=18-XY_More_Setting_displacement, sticky="ew")
    Z_control_label.grid(column=0, row=19-XY_More_Setting_displacement, columnspan=2, sticky="nsew")
    Z_pos_label.grid(column=0, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_pos_textblock.grid(column=1, row=20-XY_More_Setting_displacement, sticky="nsew")
    Z_button_frame.grid(column=0, row=21-XY_More_Setting_displacement, rowspan=2, columnspan=2)
    Z_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Z_More_Setting_displacement == 0):
        Z_More_Setting_frame.grid(column=0, row=24-XY_More_Setting_displacement,columnspan=2, rowspan=2, sticky="ns")
    Angle_seperator.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ew")
    Angle_control_label.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")
    Angle_label.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_textblock.grid(column=1, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
    Angle_button_frame.grid(column=0, columnspan=2, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement)
    Angle_Setting_frame.grid(column=0, row=30-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")
    if (Angle_More_Setting_displacement == 0):
        Angle_More_Setting_frame.grid(column=0, row=31-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def Z_hide_show_Setting(*args):
    global Z_More_Setting_displacement
    if (Z_More_Setting_displacement == 0):
        Z_hide_Setting()
    else:
        Z_show_Setting()

def update_Z_modetoCon(*args):
    global Z_is_Con, Z_Con_button, Z_Dis_button
    if Z_is_Con == False:
        Z_Con_button.configure(relief="sunken")
        Z_Dis_button.configure(relief="raised")
        Z_is_Con = True
        Z_continuous_setup()
    print("Z_is_Con = ", Z_is_Con)

def update_Z_modetoDis(*args):
    global Z_is_Con, Z_Con_button, Z_Dis_button
    if Z_is_Con == True:
        Z_Con_button.configure(relief="raised")
        Z_Dis_button.configure(relief="sunken")
        Z_is_Con = False
        Z_discreet_setup()
    print("Z_is_Con = ", Z_is_Con)

def Angle_hide_Setting(*args):
    global Angle_More_Setting_displacement, Angle_More_Setting_frame
    Angle_More_Setting_displacement = 2
    Angle_More_Setting_frame.grid_forget()

def Angle_show_Setting(*args):
    global Angle_More_Setting_displacement, Angle_More_Setting_frame
    Angle_More_Setting_displacement = 0
    Angle_More_Setting_frame.grid(column=0, row=31-XY_More_Setting_displacement-Z_More_Setting_displacement, rowspan=2, columnspan=2, sticky="ns")

def Angle_hide_show_Setting(*args):
    global Angle_More_Setting_displacement
    if (Angle_More_Setting_displacement == 0):
        Angle_hide_Setting()
    else:
        Angle_show_Setting()

def update_Angle_modetoCon(*args):
    global Angle_is_Con, Angle_Con_button, Angle_Dis_button
    if Angle_is_Con == False:
        Angle_Con_button.configure(relief="sunken")
        Angle_Dis_button.configure(relief="raised")
        Angle_is_Con = True
        Angle_continuous_setup()
    print("Angle_is_Con = ", Angle_is_Con)

def update_Angle_modetoDis(*args):
    global Angle_is_Con, Angle_Con_button, Angle_Dis_button
    if Angle_is_Con == True:
        Angle_Con_button.configure(relief="raised")
        Angle_Dis_button.configure(relief="sunken")
        Angle_is_Con = False
        Angle_discreet_setup()
    print("Angle_is_Con = ", Angle_is_Con)


##Prior
def Prior_update_X_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_X_pos, pr, Prior_X_pos
    pr.get_curr_pos()
    Prior_X_pos = pr.x
    Prior_X_pos_string.set(pr.x)
    # root.after(250, Prior_update_X_pos_string)

def Prior_update_Y_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_Y_pos, pr, Prior_Y_pos
    pr.get_curr_pos()
    Prior_Y_pos = pr.y
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
    print("Prior Step (μm) size text = ", Prior_XY_Step_size) #debug

def Prior_update_XY_coeff():
    global Prior_XY_coeff, Prior_XY_coeff_spinbox
    Prior_XY_coeff_string.set(Prior_XY_coeff_spinbox.get())
    if (Prior_XY_coeff_spinbox.get() != ""):
        Prior_XY_coeff = int(Prior_XY_coeff_spinbox.get())
    print("Prior_XY_coeff = ", Prior_XY_coeff) #debug

def Prior_update_XY_coeff_text(*args):
    global Prior_XY_coeff, Prior_XY_coeff_string
    print("Prior_XY_coeff string = " + Prior_XY_coeff_string.get()) #debug
    if (Prior_XY_coeff_string.get() != ""):
        Prior_XY_coeff = int(Prior_XY_coeff_string.get())
    print("Prior_XY_coeff text = ", Prior_XY_coeff) #debug

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

def Prior_update_XY_Backlash_Enable():
    global pr, Prior_XY_Backlash_EN
    pr.set_backlash_en(Prior_XY_Backlash_EN.get())

def Prior_update_XY_Backlash_Dist():
    global Prior_XY_Backlash_Dist, Prior_XY_Backlash_Dist_spinbox
    Prior_XY_Backlash_Dist_string.set(Prior_XY_Backlash_Dist_spinbox.get())
    if (Prior_XY_Backlash_Dist_spinbox.get() != ""):
        Prior_XY_Backlash_Dist = int(Prior_XY_Backlash_Dist_spinbox.get())
        pr.set_backlash_dist(Prior_XY_Backlash_Dist)
    print("Prior_XY_Backlash_Dist = ", Prior_XY_Backlash_Dist) #debug

def Prior_update_XY_Backlash_Dist_text(*args):
    global Prior_XY_Backlash_Dist, Prior_XY_Backlash_Dist_string
    print("Prior_XY_Backlash_Dist string = " + Prior_XY_Backlash_Dist_string.get()) #debug
    if (Prior_XY_Backlash_Dist_string.get() != ""):
        Prior_XY_Backlash_Dist = int(Prior_XY_Backlash_Dist_string.get())
        pr.set_backlash_dist(Prior_XY_Backlash_Dist)
    print("Prior_XY_Backlash_Dist text = ", Prior_XY_Backlash_Dist) #debug

def Prior_up_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos, Prior_XY_coeff
    Prior_Y_pos -= Prior_XY_Step_size * Prior_XY_coeff
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_x10_up_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos, Prior_XY_coeff
    Prior_Y_pos -= Prior_XY_Step_size * Prior_XY_coeff * 10
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_down_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos, Prior_XY_coeff
    Prior_Y_pos += Prior_XY_Step_size * Prior_XY_coeff
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_x10_down_Y_pos(*args):
    global Prior_Y_pos, Prior_XY_Step_size, pr, Prior_X_pos, Prior_XY_coeff
    Prior_Y_pos += Prior_XY_Step_size * Prior_XY_coeff * 10
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_right_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos, Prior_XY_coeff
    Prior_X_pos += Prior_XY_Step_size * Prior_XY_coeff
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_x10_right_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos, Prior_XY_coeff
    Prior_X_pos += Prior_XY_Step_size * Prior_XY_coeff * 10
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_left_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos, Prior_XY_coeff
    Prior_X_pos -= Prior_XY_Step_size * Prior_XY_coeff
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_x10_left_X_pos(*args):
    global Prior_X_pos, Prior_XY_Step_size, pr, Prior_Y_pos, Prior_XY_coeff
    Prior_X_pos -= Prior_XY_Step_size * Prior_XY_coeff * 10
    pr.go_to_pos(Prior_X_pos, Prior_Y_pos)
    Prior_update_X_pos_string()
    Prior_update_Y_pos_string()

def Prior_hold_right_X_pos(*args):
    global pr
    pr.start_forward_x_motor()

def Prior_release_X_pos(*args):
    global pr
    pr.stop_x_motor()
    Prior_update_X_pos_string()

def Prior_hold_left_X_pos(*args):
    global pr
    pr.start_backward_x_motor()

def Prior_hold_up_Y_pos(*args):
    global pr
    pr.start_forward_y_motor()

def Prior_release_Y_pos(*args):
    global pr
    pr.stop_y_motor()
    Prior_update_Y_pos_string()

def Prior_hold_down_Y_pos(*args):
    global pr
    pr.start_backward_y_motor()

def Prior_continuous_setup(*args):
    global Prior_Up_button, Prior_Down_button, Prior_Right_button, Prior_Left_button
    Prior_Up_button.unbind("<ButtonRelease-1>")
    Prior_Up_button.bind("<Button-1>", Prior_hold_up_Y_pos)
    Prior_Up_button.bind("<ButtonRelease-1>", Prior_release_Y_pos)

    Prior_Down_button.unbind("<ButtonRelease-1>")
    Prior_Down_button.bind("<Button-1>", Prior_hold_down_Y_pos)
    Prior_Down_button.bind("<ButtonRelease-1>", Prior_release_Y_pos)

    Prior_Right_button.unbind("<ButtonRelease-1>")
    Prior_Right_button.bind("<Button-1>", Prior_hold_right_X_pos)
    Prior_Right_button.bind("<ButtonRelease-1>", Prior_release_X_pos)

    Prior_Left_button.unbind("<ButtonRelease-1>")
    Prior_Left_button.bind("<Button-1>", Prior_hold_left_X_pos)
    Prior_Left_button.bind("<ButtonRelease-1>", Prior_release_X_pos)

    global Prior_Up_x10_button, Prior_Down_x10_button, Prior_Right_x10_button, Prior_Left_x10_button
    Prior_Up_x10_button.unbind("<ButtonRelease-1>")
    Prior_Up_x10_button.bind("<Button-1>", Prior_hold_up_Y_pos)
    Prior_Up_x10_button.bind("<ButtonRelease-1>", Prior_release_Y_pos)

    Prior_Down_x10_button.unbind("<ButtonRelease-1>")
    Prior_Down_x10_button.bind("<Button-1>", Prior_hold_down_Y_pos)
    Prior_Down_x10_button.bind("<ButtonRelease-1>", Prior_release_Y_pos)

    Prior_Right_x10_button.unbind("<ButtonRelease-1>")
    Prior_Right_x10_button.bind("<Button-1>", Prior_hold_right_X_pos)
    Prior_Right_x10_button.bind("<ButtonRelease-1>", Prior_release_X_pos)

    Prior_Left_x10_button.unbind("<ButtonRelease-1>")
    Prior_Left_x10_button.bind("<Button-1>", Prior_hold_left_X_pos)
    Prior_Left_x10_button.bind("<ButtonRelease-1>", Prior_release_X_pos)



def Prior_discreet_setup(*args):
    global Prior_Up_button, Prior_Down_button, Prior_Right_button, Prior_Left_button
    Prior_Up_button.unbind("<Button-1>")
    Prior_Up_button.unbind("<ButtonRelease-1>")
    Prior_Up_button.bind("<ButtonRelease-1>", Prior_up_Y_pos)

    Prior_Down_button.unbind("<Button-1>")
    Prior_Down_button.unbind("<ButtonRelease-1>")
    Prior_Down_button.bind("<ButtonRelease-1>", Prior_down_Y_pos)

    Prior_Right_button.unbind("<Button-1>")
    Prior_Right_button.unbind("<ButtonRelease-1>")
    Prior_Right_button.bind("<ButtonRelease-1>", Prior_right_X_pos)

    Prior_Left_button.unbind("<Button-1>")
    Prior_Left_button.unbind("<ButtonRelease-1>")
    Prior_Left_button.bind("<ButtonRelease-1>", Prior_left_X_pos)

    global Prior_Up_x10_button, Prior_Down_x10_button, Prior_Right_x10_button, Prior_Left_x10_button
    Prior_Up_x10_button.unbind("<Button-1>")
    Prior_Up_x10_button.unbind("<ButtonRelease-1>")
    Prior_Up_x10_button.bind("<ButtonRelease-1>", Prior_x10_up_Y_pos)

    Prior_Down_x10_button.unbind("<Button-1>")
    Prior_Down_x10_button.unbind("<ButtonRelease-1>")
    Prior_Down_x10_button.bind("<ButtonRelease-1>", Prior_x10_down_Y_pos)

    Prior_Right_x10_button.unbind("<Button-1>")
    Prior_Right_x10_button.unbind("<ButtonRelease-1>")
    Prior_Right_x10_button.bind("<ButtonRelease-1>", Prior_x10_right_X_pos)

    Prior_Left_x10_button.unbind("<Button-1>")
    Prior_Left_x10_button.unbind("<ButtonRelease-1>")
    Prior_Left_x10_button.bind("<ButtonRelease-1>", Prior_x10_left_X_pos)

def Prior_update_XY_modetoCon(*args):
    global Prior_XY_is_Con, Prior_Con_button, Prior_Dis_button
    if Prior_XY_is_Con == False:
        Prior_Con_button.configure(relief="sunken")
        Prior_Dis_button.configure(relief="raised")
        Prior_XY_is_Con = True
        Prior_continuous_setup()
    print("Prior_XY_is_Con = ", Prior_XY_is_Con)

def Prior_update_XY_modetoDis(*args):
    global Prior_XY_is_Con, Prior_Con_button, Prior_Dis_button
    if Prior_XY_is_Con == True:
        Prior_Con_button.configure(relief="raised")
        Prior_Dis_button.configure(relief="sunken")
        Prior_XY_is_Con = False
        Prior_discreet_setup()
    print("Prior_XY_is_Con = ", Prior_XY_is_Con)

# def Prior_update_XY_pos(*args):
#     global Prior_X_pos, Prior_Y_pos
#     if ((Prior_Im_X_pos_string.get() != "") & (Prior_Im_Y_pos_string.get() != "")):
#         Prior_X_pos = int(Prior_Im_X_pos_string.get())
#         Prior_Y_pos = int(Prior_Im_Y_pos_string.get())

def Prior_update_Z_modetoCon(*args):
    global Prior_Z_is_Con, Prior_Z_Con_button, Prior_Z_Dis_button
    if Prior_Z_is_Con == False:
        Prior_Z_Con_button.configure(relief="sunken")
        Prior_Z_Dis_button.configure(relief="raised")
        Prior_Z_is_Con = True
        Prior_Z_continuous_setup()
    print("Prior_Z_is_Con = ", Prior_Z_is_Con)

def Prior_update_Z_modetoDis(*args):
    global Prior_Z_is_Con, Prior_Z_Con_button, Prior_Z_Dis_button
    if Prior_Z_is_Con == True:
        Prior_Z_Con_button.configure(relief="raised")
        Prior_Z_Dis_button.configure(relief="sunken")
        Prior_Z_is_Con = False
        Prior_Z_discreet_setup()
    print("Prior_Z_is_Con = ", Prior_Z_is_Con)

def Prior_update_Z_pos_string(*args): #Check with Prior API, not global variable (i.e unfinished)
    global Prior_Z_pos, Prior_Z_pos_string, pr
    Prior_Z_pos = pr.get_curr_z_pos()
    Prior_Z_pos_string.set(Prior_Z_pos)

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

def Prior_update_Z_coeff():
    global Prior_Z_coeff, Prior_Z_coeff_spinbox
    Prior_Z_coeff_string.set(Prior_Z_coeff_spinbox.get())
    if (Prior_Z_coeff_spinbox.get() != ""):
        Prior_Z_coeff = int(Prior_Z_coeff_spinbox.get())
    print("Prior_Z_coeff = ", Prior_Z_coeff) #debug

def Prior_update_Z_coeff_text(*args):
    global Prior_Z_coeff, Prior_Z_coeff_string
    print("Prior_Z_coeff string = " + Prior_Z_coeff_string.get()) #debug
    if (Prior_Z_coeff_string.get() != ""):
        Prior_Z_coeff = int(Prior_Z_coeff_string.get())
    print("Prior_Z_coeff text = ", Prior_Z_coeff) #debug

def Prior_update_Z_Speed():
    global Prior_Z_Speed, Prior_Z_Speed_spinbox
    Prior_Z_Speed_string.set(Prior_Z_Speed_spinbox.get())
    if (Prior_Z_Speed_spinbox.get() != ""):
        Prior_Z_Speed = int(Prior_Z_Speed_spinbox.get())
        pr.set_z_velocity(Prior_Z_Speed)
    print("Prior_Z_Speed = ", Prior_Z_Speed) #debug

def Prior_update_Z_Speed_text(*args):
    global Prior_Z_Speed, Prior_Z_Speed_string
    print("Prior_Z_Speed string = " + Prior_Z_Speed_string.get()) #debug
    if (Prior_Z_Speed_string.get() != ""):
        Prior_Z_Speed = int(Prior_Z_Speed_string.get())
        pr.set_z_velocity(Prior_Z_Speed)
    print("Prior_Z_Speed text = ", Prior_Z_Speed) #debug

def Prior_update_Z_Acceleration():
    global Prior_Z_Acceleration, Prior_Z_Acceleration_spinbox
    Prior_Z_Acceleration_string.set(Prior_Z_Acceleration_spinbox.get())
    if (Prior_Z_Acceleration_spinbox.get() != ""):
        Prior_Z_Acceleration = int(Prior_Z_Acceleration_spinbox.get())
        pr.set_z_acceleration(Prior_Z_Acceleration)
    print("Prior_Z_Acceleration = ", Prior_Z_Acceleration) #debug

def Prior_update_Z_Acceleration_text(*args):
    global Prior_Z_Acceleration, Prior_Z_Acceleration_string
    print("Prior_Z_Acceleration string = " + Prior_Z_Acceleration_string.get()) #debug
    if (Prior_Z_Acceleration_string.get() != ""):
        Prior_Z_Acceleration = int(Prior_Z_Acceleration_string.get())
        pr.set_z_acceleration(Prior_Z_Acceleration)
    print("Prior_Z_Acceleration text = ", Prior_Z_Acceleration) #debug

def Prior_update_Z_Backlash_Enable():
    global pr, Prior_Z_Backlash_EN
    pr.set_z_backlash_en(Prior_Z_Backlash_EN.get())

def Prior_update_Z_Backlash_Dist():
    global Prior_Z_Backlash_Dist, Prior_Z_Backlash_Dist_spinbox
    Prior_Z_Backlash_Dist_string.set(Prior_Z_Backlash_Dist_spinbox.get())
    if (Prior_Z_Backlash_Dist_spinbox.get() != ""):
        Prior_Z_Backlash_Dist = int(Prior_Z_Backlash_Dist_spinbox.get())
        pr.set_z_backlash_dist(Prior_Z_Backlash_Dist)
    print("Prior_Z_Backlash_Dist = ", Prior_Z_Backlash_Dist) #debug

def Prior_update_Z_Backlash_Dist_text(*args):
    global Prior_Z_Backlash_Dist, Prior_Z_Backlash_Dist_string
    print("Prior_Z_Backlash_Dist string = " + Prior_Z_Backlash_Dist_string.get()) #debug
    if (Prior_Z_Backlash_Dist_string.get() != ""):
        Prior_Z_Backlash_Dist = int(Prior_Z_Backlash_Dist_string.get())
        pr.set_z_backlash_dist(Prior_Z_Backlash_Dist)
    print("Prior_Z_Backlash_Dist text = ", Prior_Z_Backlash_Dist) #debug

def Prior_up_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size, Prior_Z_coeff
    Prior_Z_pos += Prior_Z_Step_size * Prior_Z_coeff
    pr.go_to_z_pos(Prior_Z_pos)
    Prior_update_Z_pos_string()


def Prior_x10_up_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size, Prior_Z_coeff
    Prior_Z_pos += Prior_Z_Step_size * Prior_Z_coeff * 10
    pr.go_to_z_pos(Prior_Z_pos)
    Prior_update_Z_pos_string()

def Prior_down_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size, Prior_Z_coeff
    Prior_Z_pos -= Prior_Z_Step_size * Prior_Z_coeff
    pr.go_to_z_pos(Prior_Z_pos)
    Prior_update_Z_pos_string()
    
def Prior_x10_down_Z_pos(*args):
    global Prior_Z_pos, Prior_Z_Step_size, Prior_Z_coeff
    Prior_Z_pos -= Prior_Z_Step_size * Prior_Z_coeff * 10
    pr.go_to_z_pos(Prior_Z_pos)
    Prior_update_Z_pos_string()

def Prior_hold_up_Z_pos(*args):
    global pr
    pr.start_forward_z_motor()

def Prior_release_Z_pos(*args):
    global pr
    pr.stop_z_motor()
    Prior_update_Z_pos_string()

def Prior_hold_down_Z_pos(*args):
    global pr
    pr.start_backward_z_motor()

def Prior_Z_continuous_setup(*args):
    global Prior_Z_Up_button, Prior_Z_Down_button
    Prior_Z_Up_button.unbind("<ButtonRelease-1>")
    Prior_Z_Up_button.bind("<Button-1>", Prior_hold_up_Z_pos)
    Prior_Z_Up_button.bind("<ButtonRelease-1>", Prior_release_Z_pos)

    Prior_Z_Down_button.unbind("<ButtonRelease-1>")
    Prior_Z_Down_button.bind("<Button-1>", Prior_hold_down_Z_pos)
    Prior_Z_Down_button.bind("<ButtonRelease-1>", Prior_release_Z_pos)

    global Prior_Z_Up_x10_button, Prior_Z_Down_x10_button
    Prior_Z_Up_x10_button.unbind("<ButtonRelease-1>")
    Prior_Z_Up_x10_button.bind("<Button-1>", Prior_hold_up_Z_pos)
    Prior_Z_Up_x10_button.bind("<ButtonRelease-1>", Prior_release_Z_pos)

    Prior_Z_Down_x10_button.unbind("<ButtonRelease-1>")
    Prior_Z_Down_x10_button.bind("<Button-1>", Prior_hold_down_Z_pos)
    Prior_Z_Down_x10_button.bind("<ButtonRelease-1>", Prior_release_Z_pos)

def Prior_Z_discreet_setup(*args):
    global Prior_Z_Up_button, Prior_Z_Down_button
    Prior_Z_Up_button.unbind("<Button-1>")
    Prior_Z_Up_button.unbind("<ButtonRelease-1>")
    Prior_Z_Up_button.bind("<ButtonRelease-1>", Prior_up_Z_pos)

    Prior_Z_Down_button.unbind("<Button-1>")
    Prior_Z_Down_button.unbind("<ButtonRelease-1>")
    Prior_Z_Down_button.bind("<ButtonRelease-1>", Prior_down_Z_pos)

    global Prior_Z_Up_x10_button, Prior_Z_Down_x10_button
    Prior_Z_Up_x10_button.unbind("<Button-1>")
    Prior_Z_Up_x10_button.unbind("<ButtonRelease-1>")
    Prior_Z_Up_x10_button.bind("<ButtonRelease-1>", Prior_x10_up_Z_pos)

    Prior_Z_Down_x10_button.unbind("<Button-1>")
    Prior_Z_Down_x10_button.unbind("<ButtonRelease-1>")
    Prior_Z_Down_x10_button.bind("<ButtonRelease-1>", Prior_x10_down_Z_pos)


# def Prior_update_Z_pos(*argss):
#     global Prior_Z_pos
#     if (Prior_Im_Z_pos_string.get() != ""):
#         Prior_Z_pos = int(Prior_Im_Z_pos_string.get())

def Prior_XY_hide_Setting(*args):
    global Prior_XY_More_Setting_displacement, Prior_XY_More_Setting_frame
    Prior_XY_More_Setting_displacement = 2
    Prior_XY_More_Setting_frame.grid_forget()

    Prior_Z_Label_seperator.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ew")
    Prior_Z_control_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, columnspan=2, sticky="nsew")

    Prior_Z_pos_label.grid(column=3, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")
    Prior_Z_pos_textblock.grid(column=4, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")

    Prior_Z_button_frame.grid(column=3, row=21- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)

    Prior_Z_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_More_Setting_frame.grid(column=3, row=24-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")
    

def Prior_XY_show_Setting(*args):
    global Prior_XY_More_Setting_displacement, Prior_XY_More_Setting_frame
    Prior_XY_More_Setting_displacement = 0
    Prior_XY_More_Setting_frame.grid(column=3, row=16, columnspan=2, rowspan=2, sticky="ns")
    Prior_Z_Label_seperator.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ew")
    Prior_Z_control_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, columnspan=2, sticky="nsew")

    Prior_Z_pos_label.grid(column=3, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")
    Prior_Z_pos_textblock.grid(column=4, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")

    Prior_Z_button_frame.grid(column=3, row=21- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)

    Prior_Z_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_More_Setting_frame.grid(column=3, row=24-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")
  
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
    Prior_Z_More_Setting_frame.grid(column=3, row=24-Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2, sticky="ns")

def Prior_Z_hide_show_Setting(*args):
    global Prior_Z_More_Setting_displacement
    if (Prior_Z_More_Setting_displacement == 0):
        Prior_Z_hide_Setting()
    else:
        Prior_Z_show_Setting()

def on_close():
    kim_obj.disconnect()
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
XY_coeff_string = StringVar()
XY_coeff_string.set(XY_coeff)

XY_Speed_string = StringVar()
XY_Speed_string.set(XY_Speed)

XY_Acceleration_string = StringVar()
XY_Acceleration_string.set(XY_Acceleration)

Z_pos_string = StringVar()
Z_pos_string.set(Z_pos)

Z_Step_size_string = StringVar()
Z_Step_size_string.set(Z_Step_size)

Z_coeff_string = StringVar()
Z_coeff_string.set(Z_coeff)

Z_Speed_string = StringVar()
Z_Speed_string.set(Z_Speed)

Z_Acceleration_string = StringVar()
Z_Acceleration_string.set(Z_Acceleration)

Angle_string = StringVar()
Angle_string.set(Z_pos)

Angle_Step_size_string = StringVar()
Angle_Step_size_string.set(Z_Step_size)

Angle_coeff_string = StringVar()
Angle_coeff_string.set(Angle_coeff)

Angle_Speed_string = StringVar()
Angle_Speed_string.set(Z_Speed)

Angle_Acceleration_string = StringVar()
Angle_Acceleration_string.set(Z_Acceleration)

##Prior
Prior_X_pos_string = StringVar()
Prior_X_pos_string.set(Prior_X_pos)
Prior_Y_pos_string = StringVar()
Prior_Y_pos_string.set(Prior_Y_pos)

Prior_XY_Step_size_string = StringVar()
Prior_XY_Step_size_string.set(Prior_XY_Step_size)

Prior_XY_coeff_string = StringVar()
Prior_XY_coeff_string.set(Prior_XY_coeff)

Prior_XY_Speed_string = StringVar()
Prior_XY_Speed_string.set(Prior_XY_Speed)

Prior_XY_Acceleration_string = StringVar()
Prior_XY_Acceleration_string.set(Prior_XY_Acceleration)

Prior_XY_Backlash_Dist_string = StringVar()
Prior_XY_Backlash_Dist_string.set(Prior_XY_Backlash_Dist)

Prior_Z_pos_string = StringVar()
Prior_Z_pos_string.set(Prior_Z_pos)

Prior_Z_Step_size_string = StringVar()
Prior_Z_Step_size_string.set(Prior_Z_Step_size)

Prior_Z_coeff_string = StringVar()
Prior_Z_coeff_string.set(Prior_Z_coeff)

Prior_Z_Speed_string = StringVar()
Prior_Z_Speed_string.set(Prior_Z_Speed)

Prior_Z_Acceleration_string = StringVar()
Prior_Z_Acceleration_string.set(Prior_Z_Acceleration)

Prior_Z_Backlash_Dist_string = StringVar()
Prior_Z_Backlash_Dist_string.set(Prior_Z_Backlash_Dist)

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
T_set_slider = Scale(TC_frame, from_=20, to=205, orient="horizontal", variable=T_set_scale, length=200)
T_set_slider.bind("<ButtonRelease-1>", update_T_set)

TC_PID_button = Button(TC_frame, text="PID Settings", command=hide_show_PID)

TC_PID_frame = Frame(TC_frame)
P_value_label = Label(TC_PID_frame, text="P", font=normal_font)
P_value_spinbox = Spinbox(TC_PID_frame, textvariable=P_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_P_value)
P_value_string.trace_add("write", update_P_value_text)

I_value_label = Label(TC_PID_frame, text="I", font=normal_font)
I_value_spinbox = Spinbox(TC_PID_frame, textvariable=I_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_I_value)
I_value_string.trace_add("write", update_I_value_text)

D_value_label = Label(TC_PID_frame, text="Jog",font=normal_font)
D_value_spinbox = Spinbox(TC_PID_frame, textvariable=D_value_string, from_=Temperature_PID_Min, to=Temperature_PID_Max, command=update_D_value)
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
XY_Step_size_label = Label(XY_Setting_frame, text="Step (μm)", font=normal_font)
XY_Step_size_spinbox = Spinbox(XY_Setting_frame, textvariable=XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_XY_Step_size, width=10)
XY_Step_size_string.trace_add("write", update_XY_Step_size_text)
Hide_button = Button(XY_Setting_frame, text="Speed Setting", command=XY_hide_show_Setting)

XY_More_Setting_frame = Frame(root)

XY_coeff_label = Label(XY_More_Setting_frame, text="Multiplier")
XY_coeff_spinbox = Spinbox(XY_More_Setting_frame, textvariable=XY_coeff_string, from_=Coeff_size_min, to=Coeff_size_max, width=10, command=update_XY_coeff)
XY_coeff_string.trace_add("write", update_XY_coeff_text)

XY_Speed_label = Label(XY_More_Setting_frame, text="Speed (μm/s)")
XY_Speed_spinbox = Spinbox(XY_More_Setting_frame, textvariable=XY_Speed_string, from_=Speed_min, to=Speed_max, command=update_XY_Speed)
XY_Speed_string.trace_add("write", update_XY_Speed_text)

XY_Acceleration_label = Label(XY_More_Setting_frame, text="Accel (μm/s²)")
XY_Acceleration_spinbox = Spinbox(XY_More_Setting_frame, textvariable=XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_XY_Acceleration)
XY_Acceleration_string.trace_add("write", update_XY_Acceleration_text)

KIM_button_frame = Frame(root)

Left_button = Button(KIM_button_frame, text="◄", font=5, width=3, height=1)
Right_button = Button(KIM_button_frame, text="►", font=5, width=3, height=1)
Up_button = Button(KIM_button_frame, text="▲", font=5, width=3, height=1)
Down_button = Button(KIM_button_frame, text="▼", font=5, width=3, height=1)
discreet_setup()

Left_x10_button = Button(KIM_button_frame, text="⏪", command=x10_left_X_pos)
Right_x10_button = Button(KIM_button_frame, text="⏩", command=x10_right_X_pos)
Up_x10_button = Button(KIM_button_frame, text="⏫", command=x10_up_Y_pos)
Down_x10_button = Button(KIM_button_frame, text="⏬", command=x10_down_Y_pos)

Con_button = Button(KIM_button_frame, text="Con", width=3, command=update_XY_modetoCon)
Dis_button = Button(KIM_button_frame, text="Jog", width=3, relief="sunken", command=update_XY_modetoDis)

XY_Z_seperator = ttk.Separator(root, orient="horizontal")

Z_control_label = Label(root, text="Z AXIS CONTROL", font=normal_font)
Z_pos_label = Label(root, text="Z Position",font=normal_font)
Z_pos_textblock = Label(root, textvariable=Z_pos_string, borderwidth=1, relief="groove")

Z_button_frame = Frame(root)

Z_Up_button = Button(Z_button_frame, text="▲", width=4, height=2)
Z_Down_button = Button(Z_button_frame, text="▼", width=4, height=2)

Z_discreet_setup()

Z_Up_x10_button = Button(Z_button_frame, text="⏫", width=4, height=2, command=x10_up_Z_pos)
Z_Down_x10_button = Button(Z_button_frame, text="⏬", width=4, height=2, command=x10_down_Z_pos)

Z_filler = Label(Z_button_frame ,text="")
Z_Con_button = Button(Z_button_frame, text="Con", width=3, command=update_Z_modetoCon)
Z_Dis_button = Button(Z_button_frame, text="Jog", width=3, relief="sunken", command=update_Z_modetoDis)

Z_Setting_frame = Frame(root)

Z_Step_size_label = Label(Z_Setting_frame, text="Step (μm)",font=normal_font)
Z_Step_size_spinbox = Spinbox(Z_Setting_frame, textvariable=Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Z_Step_size, width=10)
Z_Step_size_string.trace_add("write", update_Z_Step_size_text)

Z_Setting_button = Button(Z_Setting_frame, text="Speed Setting", command=Z_hide_show_Setting)

Z_More_Setting_frame = Frame(root)

Z_coeff_label = Label(Z_More_Setting_frame, text="Multiplier")
Z_coeff_spinbox = Spinbox(Z_More_Setting_frame, textvariable=Z_coeff_string, from_=Coeff_size_min, to=Coeff_size_max, width=10, command=update_Z_coeff)
Z_coeff_string.trace_add("write", update_Z_coeff_text)

Z_Speed_label = Label(Z_More_Setting_frame, text="Speed (μm/s)")
Z_Speed_spinbox = Spinbox(Z_More_Setting_frame, textvariable=Z_Speed_string, from_=Speed_min, to=Speed_max, command=update_Z_Speed)
Z_Speed_string.trace_add("write", update_Z_Speed_text)

Z_Acceleration_label = Label(Z_More_Setting_frame, text="Accel (μm/s²)")
Z_Acceleration_spinbox = Spinbox(Z_More_Setting_frame, textvariable=Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=update_Z_Acceleration)
Z_Acceleration_string.trace_add("write", update_Z_Acceleration_text)

Angle_seperator = ttk.Separator(root)
Angle_control_label = Label(root, text="ANGLE CONTROL",font=normal_font)

Angle_label = Label(root, text="Angle Degree",font=normal_font)
Angle_textblock = Label(root, textvariable=Angle_string, borderwidth=1, relief="groove")

Angle_button_frame = Frame(root)

Angle_Up_button = Button(Angle_button_frame, text="↷", width=10, height=2)
Angle_Down_button = Button(Angle_button_frame, text="↶", width=10, height=2)

Angle_discreet_setup()

Angle_Con_button = Button(Angle_button_frame, text="Con", width=3, command=update_Angle_modetoCon)
Angle_Dis_button = Button(Angle_button_frame, text="Jog", width=3, relief="sunken", command=update_Angle_modetoDis)

Angle_Setting_frame = Frame(root)

Angle_Step_size_label = Label(Angle_Setting_frame, text="Step (μm)",font=normal_font)
Angle_Step_size_spinbox = Spinbox(Angle_Setting_frame, textvariable=Angle_Step_size_string, from_=Step_size_min, to=Step_size_max, command=update_Angle_Step_size, width=10)
Angle_Step_size_string.trace_add("write", update_Angle_Step_size_text)

Angle_Setting_button = Button(Angle_Setting_frame, text="Speed Setting", command=Angle_hide_show_Setting)

Angle_More_Setting_frame = Frame(root)

Angle_coeff_label = Label(Angle_More_Setting_frame, text="Multiplier")
Angle_coeff_spinbox = Spinbox(Angle_More_Setting_frame, textvariable=Angle_coeff_string, from_=Coeff_size_min, to=Coeff_size_max, width=10, command=update_Angle_coeff)
Angle_coeff_string.trace_add("write", update_Angle_coeff_text)

Angle_Speed_label = Label(Angle_More_Setting_frame, text="Speed (μm/s)")
Angle_Speed_spinbox = Spinbox(Angle_More_Setting_frame, textvariable=Angle_Speed_string, from_=Speed_min, to=Speed_max, command=update_Angle_Speed)
Angle_Speed_string.trace_add("write", update_Angle_Speed_text)

Angle_Acceleration_label = Label(Angle_More_Setting_frame, text="Accel (μm/s²)")
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
Prior_XY_Step_size_label = Label(Prior_XY_Setting_frame, text="Step (μm)",font=normal_font)
Prior_XY_Step_size_spinbox = Spinbox(Prior_XY_Setting_frame, textvariable=Prior_XY_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_XY_Step_size, width=10)
Prior_XY_Step_size_string.trace_add("write", Prior_update_XY_Step_size_text)

Prior_XY_More_Setting_frame = Frame(root)

Prior_XY_coeff_label = Label(Prior_XY_More_Setting_frame, text="Multiplier")
Prior_XY_coeff_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_coeff_string, from_=Coeff_size_min, to=Coeff_size_max, width=10, command=Prior_update_XY_coeff)
Prior_XY_coeff_string.trace_add("write", Prior_update_XY_coeff_text)

Prior_XY_Speed_label = Label(Prior_XY_More_Setting_frame, text="Speed (μm/s)")
Prior_XY_Speed_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_XY_Speed)
Prior_XY_Speed_string.trace_add("write", Prior_update_XY_Speed_text)

Prior_XY_Acceleration_label = Label(Prior_XY_More_Setting_frame, text="Accel (μm/s²)")
Prior_XY_Acceleration_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_XY_Acceleration)
Prior_XY_Acceleration_string.trace_add("write", Prior_update_XY_Acceleration_text)

Prior_XY_Backlash_EN_checkbox = Checkbutton(Prior_XY_More_Setting_frame, variable=Prior_XY_Backlash_EN, text="Backlash Enable", onvalue=1, offvalue=0, command=Prior_update_XY_Backlash_Enable)

Prior_XY_Backlash_Dist_label = Label(Prior_XY_More_Setting_frame, text="Backlash Dist (μm)")
Prior_XY_Backlash_Dist_spinbox = Spinbox(Prior_XY_More_Setting_frame, textvariable=Prior_XY_Backlash_Dist_string, from_=Backlash_Dist_min, to=Backlash_Dist_max, command=Prior_update_XY_Backlash_Dist)
Prior_XY_Backlash_Dist_string.trace_add("write", Prior_update_XY_Backlash_Dist_text)

Prior_button_frame = Frame(root)

Prior_Left_button = Button(Prior_button_frame, text="◄", font=5, width=3, height=1)
Prior_Right_button = Button(Prior_button_frame, text="►", font=5, width=3, height=1)
Prior_Up_button = Button(Prior_button_frame, text="▲", font=5, width=3, height=1)
Prior_Down_button = Button(Prior_button_frame, text="▼", font=5, width=3, height=1)

Prior_discreet_setup()

Prior_Left_x10_button = Button(Prior_button_frame, text="⏪", command=Prior_x10_left_X_pos)
Prior_Right_x10_button = Button(Prior_button_frame, text="⏩", command=Prior_x10_right_X_pos)
Prior_Up_x10_button = Button(Prior_button_frame, text="⏫", command=Prior_x10_up_Y_pos)
Prior_Down_x10_button = Button(Prior_button_frame, text="⏬", command=Prior_x10_down_Y_pos)

Prior_Con_button = Button(Prior_button_frame, text="Con", width=3, command=Prior_update_XY_modetoCon)
Prior_Dis_button = Button(Prior_button_frame, text="Jog", width=3, relief="sunken",command=Prior_update_XY_modetoDis)

Prior_Z_Label_seperator = ttk.Separator(root, orient="horizontal")
Prior_Z_control_label = Label(root, text="Z AXIS CONTROL",font=normal_font)

Prior_Z_pos_label = Label(root, text="Z Position",font=normal_font)
Prior_Z_pos_textblock = Label(root, borderwidth=1, textvariable=Prior_Z_pos_string, relief="groove")

Prior_Z_button_frame = Frame(root)

Prior_Z_Up_button = Button(Prior_Z_button_frame, text="▲", width=4, height=2)
Prior_Z_Down_button = Button(Prior_Z_button_frame, text="▼", width=4, height=2)

Prior_Z_discreet_setup()

Prior_Z_Up_x10_button = Button(Prior_Z_button_frame, text="⏫",width=4, height=2, command=Prior_x10_up_Z_pos)
Prior_Z_Down_x10_button = Button(Prior_Z_button_frame, text="⏬",width=4, height=2, command=Prior_x10_down_Z_pos)

Prior_Z_filler = Label(Prior_Z_button_frame, text="")

Prior_Z_Con_button = Button(Prior_Z_button_frame, text="Con", width=3, command=Prior_update_Z_modetoCon)
Prior_Z_Dis_button = Button(Prior_Z_button_frame, text="Jog", width=3, relief="sunken", command=Prior_update_Z_modetoDis)

Prior_Z_Setting_frame = Frame(root)

Prior_Z_Step_size_label = Label(Prior_Z_Setting_frame, text="Step (μm)",font=normal_font)
Prior_Z_Step_size_spinbox = Spinbox(Prior_Z_Setting_frame, textvariable=Prior_Z_Step_size_string, from_=Step_size_min, to=Step_size_max, command=Prior_update_Z_Step_size, width=10)
Prior_Z_Step_size_string.trace_add("write", Prior_update_Z_Step_size_text)
Prior_Z_Setting_button = Button(Prior_Z_Setting_frame, text="Speed Setting", command=Prior_Z_hide_show_Setting)

Prior_Z_More_Setting_frame = Frame(root)

Prior_Z_coeff_label = Label(Prior_Z_More_Setting_frame, text="Multiplier")
Prior_Z_coeff_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_coeff_string, from_=Coeff_size_min, to=Coeff_size_max, width=10, command=Prior_update_Z_coeff)
Prior_Z_coeff_string.trace_add("write", Prior_update_Z_coeff_text)

Prior_Z_Speed_label = Label(Prior_Z_More_Setting_frame, text="Speed (μm/s)")
Prior_Z_Speed_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_Speed_string, from_=Speed_min, to=Speed_max, command=Prior_update_Z_Speed)
Prior_Z_Speed_string.trace_add("write", Prior_update_Z_Speed_text)

Prior_Z_Acceleration_label = Label(Prior_Z_More_Setting_frame, text="Accel (μm/s²)")
Prior_Z_Acceleration_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_Acceleration_string, from_=Acceleration_min, to=Acceleration_max, command=Prior_update_Z_Acceleration)
Prior_Z_Acceleration_string.trace_add("write", Prior_update_Z_Acceleration_text)

Prior_Z_Backlash_EN_checkbox = Checkbutton(Prior_Z_More_Setting_frame, variable=Prior_Z_Backlash_EN, text="Backlash Enable", onvalue=1, offvalue=0, command=Prior_update_Z_Backlash_Enable)

Prior_Z_Backlash_Dist_label = Label(Prior_Z_More_Setting_frame, text="Backlash Dist (μm)")
Prior_Z_Backlash_Dist_spinbox = Spinbox(Prior_Z_More_Setting_frame, textvariable=Prior_Z_Backlash_Dist_string, from_=Backlash_Dist_min, to=Backlash_Dist_max, command=Prior_update_Z_Backlash_Dist)
Prior_Z_Backlash_Dist_string.trace_add("write", Prior_update_Z_Backlash_Dist_text)

#GUI Placement ######################################################
root.grid_propagate(True)

##TC200
canvas.get_tk_widget().grid(column=0, row=1, columnspan=4, rowspan=7, sticky="nsew")

TC_frame.rowconfigure(0, weight=1)
TC_frame.rowconfigure(1, weight=1)
TC_frame.rowconfigure(2, weight=1)
TC_frame.rowconfigure(3, weight=1)
TC_frame.rowconfigure(4, weight=1)
TC_frame.rowconfigure(5, weight=1)
TC_frame.rowconfigure(6, weight=1)
TC_frame.rowconfigure(7, weight=1)
TC_frame.rowconfigure(8, weight=1)

TC_frame.grid(column=4, row=0, rowspan=7, columnspan=1, sticky="nsew")

T_title.grid(column=0, row=0, columnspan=2, sticky="nsew")

T_current_label.grid(column=0, row=1, sticky="nsew")
T_current_textblock.grid(column=1,row=1,sticky="nsew")

T_set_label.grid(column=0, row=2, sticky="nsew")
T_set_text.grid(column=1, row=2, sticky="nsew")
T_set_slider.grid(columnspan=2, column=0, row=3)

TC_PID_button.grid(column=0, row=4, columnspan=2)

# TC_PID_frame.grid(column=0, row=5, columnspan=2, rowspan=3)

P_value_label.grid(column=0, row=0)
P_value_spinbox.grid(column=1, row=0, sticky="nsew")

I_value_label.grid(column=0, row=1)
I_value_spinbox.grid(column=1, row=1, sticky="nsew")

D_value_label.grid(column=0, row=2)
D_value_spinbox.grid(column=1, row=2, sticky="nsew")

Start_plot_button.grid(column=0, row=8-PID_displacement, sticky="nsew")
Stop_plot_button.grid(column=1, row=8-PID_displacement, sticky="nsew")
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

Up_x10_button.grid(column=2, row=0, sticky="nsew")
Up_button.grid(column=2, row=1, sticky="nsew")

Down_x10_button.grid(column=2, row=4, sticky="nsew")
Down_button.grid(column=2, row=3, sticky="nsew")

Right_button.grid(column=3, row=2, sticky="nsew")
Right_x10_button.grid(column=4, row=2, sticky="nsew")

Left_x10_button.grid(column=0, row=2, sticky="nsew")
Left_button.grid(column=1, row=2, sticky="nsew")

Con_button.grid(column=3, row=4, sticky="e")
Dis_button.grid(column=4, row=4, sticky="w")

XY_Setting_frame.grid(column=0, row=15, columnspan=2, sticky="ns")

XY_Step_size_label.grid(column=0, row=0, sticky="nsew")
XY_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Hide_button.grid(column=2, columnspan=2, row=0, sticky="nsew")

# XY_More_Setting_frame.grid(column=0, row=16, columnspan=2, rowspan=2, sticky="ns")

XY_coeff_label.grid(column=0, row=0, sticky="nsew")
XY_coeff_spinbox.grid(column=1, row=0, sticky="nsew")

XY_Speed_label.grid(column=0, row=1, sticky="nsew")
XY_Speed_spinbox.grid(column=1, row=1, sticky="nsew")

XY_Acceleration_label.grid(column=0, row=2, sticky="nsew")
XY_Acceleration_spinbox.grid(column=1, row=2, sticky="nsew")

XY_Z_seperator.grid(column=0, columnspan=2, row=18-XY_More_Setting_displacement, sticky="ew")
Z_control_label.grid(column=0, columnspan=2, row=19-XY_More_Setting_displacement, sticky="nsew")

Z_pos_label.grid(column=0, row=20-XY_More_Setting_displacement, sticky="nsew")
Z_pos_textblock.grid(column=1, row=20-XY_More_Setting_displacement, sticky="nsew")

Z_button_frame.grid(column=0, row=21-XY_More_Setting_displacement, rowspan=2, columnspan=2)

Z_Up_x10_button.grid(column=1, row=0)
Z_Up_button.grid(column=0, row=0)

Z_Down_button.grid(column=0, row=1)
Z_Down_x10_button.grid(column=1, row=1)

Z_filler.grid(column=3, row=1, padx=7)

Z_Con_button.grid(column=4, row=1, sticky="s")
Z_Dis_button.grid(column=5, row=1, sticky="s")

Z_Setting_frame.grid(column=0, row=23-XY_More_Setting_displacement, columnspan=2, sticky="ns")

Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Z_Setting_button.grid(column=2, row=0, sticky="nsew", columnspan=2)

Z_coeff_label.grid(column=0, row=0, sticky="nsew")
Z_coeff_spinbox.grid(column=1, row=0, sticky="nsew")

Z_Speed_label.grid(column=0, row=1, sticky="nsew")
Z_Speed_spinbox.grid(column=1, row=1, sticky="nsew")

Z_Acceleration_label.grid(column=0, row=2, sticky="nsew")
Z_Acceleration_spinbox.grid(column=1, row=2, sticky="nsew")

Angle_seperator.grid(column=0, row=26-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ew")
Angle_control_label.grid(column=0, row=27-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="nsew")

Angle_label.grid(column=0, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")
Angle_textblock.grid(column=1, row=28-XY_More_Setting_displacement-Z_More_Setting_displacement, sticky="nsew")

Angle_button_frame.grid(column=0, columnspan=2, row=29-XY_More_Setting_displacement-Z_More_Setting_displacement)

Angle_Up_button.grid(column=1, row=0, sticky="nsew")
Angle_Down_button.grid(column=0, row=0, sticky="nsew")

Angle_Con_button.grid(column=0, row=1, sticky="e", pady=4)
Angle_Dis_button.grid(column=1, row=1, sticky="w", pady=4)

Angle_Setting_frame.grid(column=0, row=30-XY_More_Setting_displacement-Z_More_Setting_displacement, columnspan=2, sticky="ns")

Angle_Step_size_label.grid(column=0, row=0, sticky="nsew")
Angle_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Angle_Setting_button.grid(column=2, row=0, columnspan=2, sticky="nsew")

Angle_coeff_label.grid(column=0, row=0, sticky="nsew")
Angle_coeff_spinbox.grid(column=1, row=0, sticky="nsew")

Angle_Speed_label.grid(column=0, row=1, sticky="nsew")
Angle_Speed_spinbox.grid(column=1, row=1, sticky="nsew")

Angle_Acceleration_label.grid(column=0, row=2, sticky="nsew")
Angle_Acceleration_spinbox.grid(column=1, row=2, sticky="nsew")

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

Prior_button_frame.grid(column=3, row=13, rowspan=2, columnspan=2)

Prior_Up_button.grid(column=2, row=1, sticky="nsew")
Prior_Up_x10_button.grid(column=2, row=0, sticky="nsew")

Prior_Down_button.grid(column=2, row=3, sticky="nsew")
Prior_Down_x10_button.grid(column=2, row=4, sticky="nsew")

Prior_Right_button.grid(column=3, row=2, sticky="nsew")
Prior_Right_x10_button.grid(column=4, row=2, sticky="nsew")

Prior_Left_button.grid(column=1, row=2, sticky="nsew")
Prior_Left_x10_button.grid(column=0, row=2, sticky="nsew")

Prior_Con_button.grid(column=3, row=4, sticky="e")
Prior_Dis_button.grid(column=4, row=4, sticky="w")

Prior_XY_Setting_frame.grid(column=3, row=15, columnspan=2, sticky="ns")

Prior_Setting_button.grid(column=2, row=0, columnspan=2, sticky="nsew")
Prior_XY_Step_size_label.grid(column=0, row=0, sticky="nsew")
Prior_XY_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")

Prior_XY_coeff_label.grid(column=0, row=0 ,sticky="nsew")
Prior_XY_coeff_spinbox.grid(column=1, row=0, sticky="nsew")

Prior_XY_Speed_label.grid(column=0, row=1, sticky="nsew")
Prior_XY_Speed_spinbox.grid(column=1, row=1, sticky="nsew")

Prior_XY_Acceleration_label.grid(column=0, row=2, sticky="nsew")
Prior_XY_Acceleration_spinbox.grid(column=1, row=2, sticky="nsew")

Prior_XY_Backlash_EN_checkbox.grid(column=0, columnspan=2, row=3, sticky="nsew")

Prior_XY_Backlash_Dist_label.grid(column=0, row=4, sticky="nsew")
Prior_XY_Backlash_Dist_spinbox.grid(column=1, row=4, sticky="nsew")

Prior_Z_Label_seperator.grid(column=3, row=18-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ew")
Prior_Z_control_label.grid(column=3, row=19-Prior_XY_More_Setting_displacement, columnspan=2, sticky="nsew")

Prior_Z_pos_label.grid(column=3, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")
Prior_Z_pos_textblock.grid(column=4, row=20-Prior_XY_More_Setting_displacement, sticky="nsew")

Prior_Z_button_frame.grid(column=3, row=21- Prior_XY_More_Setting_displacement, columnspan=2, rowspan=2)

Prior_Z_Up_button.grid(column=0, row=0)
Prior_Z_Down_button.grid(column=0, row=1)

Prior_Z_Up_x10_button.grid(column=1, row=0)
Prior_Z_Down_x10_button.grid(column=1, row=1)

Prior_Z_filler.grid(column=2, row=1, padx=7)
Prior_Z_Con_button.grid(column=3, row=1, sticky="s")
Prior_Z_Dis_button.grid(column=4, row=1, sticky="s")

Prior_Z_Setting_frame.grid(column=3, row=23-Prior_XY_More_Setting_displacement, columnspan=2, sticky="ns")

Prior_Z_Step_size_label.grid(column=0, row=0, sticky="nsew")
Prior_Z_Step_size_spinbox.grid(column=1, row=0, sticky="nsew")
Prior_Z_Setting_button.grid(column=2, columnspan=2, row=0, sticky="nsew")

# Prior_Z_More_Setting_frame.grid(column=3, row=23, columnspan=2, rowspan=2, sticky="ns")
Prior_Z_coeff_label.grid(column=0, row=0, sticky="nsew")
Prior_Z_coeff_spinbox.grid(column=1, row=0, sticky="nsew")

Prior_Z_Speed_label.grid(column=0, row=1, sticky="nsew")
Prior_Z_Speed_spinbox.grid(column=1, row=1, sticky="nsew")

Prior_Z_Acceleration_label.grid(column=0, row=2, sticky="nsew")
Prior_Z_Acceleration_spinbox.grid(column=1, row=2, sticky="nsew")

Prior_Z_Backlash_EN_checkbox.grid(column=0, row=3, columnspan=2, sticky="nsew")

Prior_Z_Backlash_Dist_label.grid(column=0, row=4, sticky="nsew")
Prior_Z_Backlash_Dist_spinbox.grid(column=1, row=4, sticky="nsew")


#Variable update call
update_T_current()

update_X_pos_string()
update_Y_pos_string()
update_Z_pos_string()
update_Angle_string()

Prior_update_X_pos_string()
Prior_update_Y_pos_string()
Prior_update_Z_pos_string()

#Calling Tk mainloop
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
