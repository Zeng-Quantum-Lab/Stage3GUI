import os
from tkinter import *
from tkinter import ttk

def on_close():
    file = open("port.config", "w")
    
    tc_args_final = 0 if tc_args.get() == "" else tc_args.get()
    pr_args_final = 0 if pr_args.get() == "" else pr_args.get()
    kim_args_final = 0 if kim_args.get() == "" else kim_args.get()

    file.write(f"{tc_args_final}\n")
    file.write(f"{pr_args_final}\n")
    file.write(f"{kim_args_final}")
    file.close()

    root.destroy()
    os.system(f"python Sources\main.py {tc_args_final} {pr_args_final} {kim_args_final}")

file = open("port.config", "r")

root = Tk()
root.title("Setup")
TC_Label = Label(root, text="TC200 COM Port:")
Kim_Label = Label(root, text="KIM101 Serial No.:")
Prior_Label = Label(root, text="Prior COM Port:")

tc_args = StringVar(value=file.readline()[:-1])
pr_args = StringVar(value=file.readline()[:-1])
kim_args = StringVar(value=file.readline())

TC_Textbox = Entry(root, textvariable=tc_args)
Kim_Textbox = Entry(root, textvariable=kim_args)
Pr_Textbox = Entry(root, textvariable=pr_args)

file.close()

Confirm_Button = Button(root, text="Confirm Setting", command=on_close)

TC_Label.grid(column=0, row=0, sticky="nsew")
Kim_Label.grid(column=0, row=2, sticky="nsew")
Prior_Label.grid(column=0, row=1, sticky="nsew")

TC_Textbox.grid(column=1, row=0, sticky="nsew")
Kim_Textbox.grid(column=1, row=2, sticky="nsew")
Pr_Textbox.grid(column=1, row=1, sticky="nsew")

Confirm_Button.grid(column=0, row=3, columnspan=2)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

