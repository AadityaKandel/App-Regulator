from tkinter import *
import subprocess
import tkinter.messagebox as tmsg
import os
import threading
import tkinter.filedialog
from tkinter.simpledialog import askstring
from tkinter import ttk
from datetime import datetime, timedelta
import ctypes
import sys

root = Tk()
# root.geometry("700x500")
root.minsize(700,500)
root.maxsize(900,530)
root.title("App Regulator")
root.config(bg="#ECECEC")
root.iconbitmap('Icon/icon.ico')

# Defining Variables
executable = StringVar() # Destination of Executable
target_text = "Choose your target"
toggle_button1 = IntVar() # Admin or Not
toggle_button2 = IntVar() # Indefinite Attack
toggle_button3 = IntVar() # Timed Attack
toggle_button4 = IntVar() # Hide Window When Attacking
toggle_button5 = IntVar() # Force Kill or Not
minutes = DoubleVar()
target_name = []
exe_name = ''
global_color = root['bg']
options = ['Once Every','After']
dropdown = StringVar()
loop = None
admin_info = '''
This feature is only available for an executable version of this app\n
But you can use this feature by manually launching this script as admin from cmd
'''
abort = False

# Setting Variables
toggle_button2.set(1)
minutes.set(1)
dropdown.set('Once Every')

# Checking One Specific File
if os.path.exists("0000.txt"):
    os.remove('0000.txt')


# Defining Functions
def allow_admin(destination):
    try:
        subprocess.run(
            ['powershell', '-Command', f'Start-Process "{destination}" -Verb RunAs'],
            check=True
        )
        sys.exit()
    except subprocess.CalledProcessError:
        tmsg.showerror('Error', 'Admin Access Not Given')
        toggle_button1.set(0)
    finally:
        pass

def check_admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if is_admin:
        tmsg.showinfo('Info','Admin Activated')
        toggle_button1.set(1)
        ch1.config(text="Admin Activated", fg="green", state=DISABLED)

def toggle_admin():
    tmsg.showinfo('Info',admin_info)
    toggle_button1.set(0)

    # Below Is For While Making An Executable
    # current_location = os.getcwd()
    # app_name = "\\app_regulator.exe"
    # final_location = os.path.join(current_location+app_name)
    # tmsg.showinfo('Admin Attempt','The App Will Now Attempt to Request For Admin Access....')
    # allow_admin(final_location)

def taskkill(app_name, force=False):
    command = ['taskkill','/IM',app_name]
    if force:
        command.append('/F')

    check = subprocess.run(command)

def check_time(target_time):
    global abort
    f=False
    if toggle_button5.get() == 1:
        f=True

    now = datetime.now()
    if now >= target_time:
        for x in target_name:
            taskkill(x, force=f)
        stop_attack()
    else:
        if abort:
            return
        else:
            root.after(100, check_time, target_time)


def spacing(frame_or_root):
    label = Label(frame_or_root,text=' ',bg=global_color).pack(side=LEFT)

def fill_target(position):
    global exe_name
    l1.config(state=NORMAL)
    l1.insert(position, f'{position+1}: '+exe_name)
    l1.config(state=DISABLED)

def choose_target():
    global target_name, exe_name
    question = tmsg.askquestion('Question','Do you want to add custom target')
    if question=="yes":
        custom_target = askstring('Application Name','Enter the Name of the Target Application?')
        try:
            exe_name=custom_target+".exe"
            target_name.append(exe_name)
            fill_target(len(target_name)-1)
        except:
            tmsg.showerror('Error','No Target Given')
            return
    else:
        try:
            a = tkinter.filedialog.askopenfiles(mode='r', title=target_text, filetypes = ['Executable .exe'], initialdir="Desktop")
        except:
            tmsg.showerror("Error","File Doesn't Exist")
            return

        if a =="":
            tmsg.showerror('Error','Target Not Selected')
        else:

            for x in range(len(a)):
                exe_name = a[x].name
                exe_index = exe_name.rindex('e')
                backslash_index = exe_name.rindex('/')
                exe_name=exe_name[backslash_index+1:exe_index+1]
                target_name.append(exe_name)
                fill_target(len(target_name)-1)

def execute_removal(index):
    # This function adjusts the entire listbox by recreating it
    global target_name
    try:
        target_name.pop(index)
    except:
        tmsg.showerror('Error','Invalid Target Number')
        return

    l1.config(state=NORMAL)
    l1.delete(0,END)

    i=0

    for x in target_name:
        l1.insert(i, f'{i+1}: '+x)
        i+=1

    l1.config(state=DISABLED)

    # print(target_name)


def withdraw_target():
    global target_name
    removal = askstring('Remove','Which number of target would you like to remove?')
    try:
        removal=int(removal)
    except:
        tmsg.showerror('Error','Invalid Input')
        return
    execute_removal(removal-1)
    # l1.config(state=NORMAL)
    # l1.delete(removal-1)
    # l1.config(state=DISABLED)
    # target_name.pop(removal-1)
    # print(target_name)

def toggle_attack1(): # Indefinite Attack
    if toggle_button2.get() == 1:
        toggle_button3.set(0)
        en1.config(state=DISABLED)
        choice.config(state=DISABLED)
    else:
        toggle_button3.set(1)
        en1.config(state=NORMAL)
        choice.config(state='readonly')

def toggle_attack2(): # Timed Attack
    # toggle_button2 & 3
    if toggle_button3.get() == 1:
        toggle_button2.set(0)
        en1.config(state=NORMAL)
        choice.config(state='readonly')
    else:
        toggle_button2.set(1)
        en1.config(state=DISABLED)
        choice.config(state=DISABLED)

def toggle_attack3(): # Hide Window or Not
    if toggle_button4.get()==1:
        tmsg.showinfo('Info','Save 0000.txt in the App Directory to Show the App Again')
    if os.path.exists('0000.txt'):
        os.remove('0000.txt')

def toggle_attack4():
    pass

def hide_window():
    global toggle_button4
    if (os.path.exists("0000.txt") == False) and (toggle_button4.get()==1):
        root.withdraw()
    elif (os.path.exists("0000.txt") == True):
        root.deiconify()
        toggle_button4.set(0)

def launch_taskkill():
    global loop,toggle_button3, minutes, target_name, abort
    loop = True
    f=False

    if toggle_button5.get() == 1:
        f=True

    if (toggle_button3.get()==1) and (options[0] == dropdown.get()):
            
            while (loop==True):

                target_time = datetime.now() + timedelta(seconds=minutes.get()*60)
                hide_window()

                while (True):
                    now = datetime.now()

                    if abort:
                        loop+=1
                        break

                    if now >= target_time:
                        for x in target_name:
                            taskkill(x, force=f)
                        break

    else:
        while (loop==True):
            hide_window()

            for x in target_name:
                taskkill(x, force=f)

def disable_everything():
    for items in all_features:
        if items['state'] == DISABLED:
            pass
        else:
            items.config(state=DISABLED)

def enable_everything():
    global toggle_button2
    for items in all_features:
        items.config(state=NORMAL)

    choice.config(state='readonly')

    if toggle_button2.get() == 1: # Both are special cases hence cannot be iterated
        en1.config(state=DISABLED)
        choice.config(state=DISABLED)

def initiate_taskkill():

    global target_name, minutes, abort

    abort=False

    if len(target_name) == 0:
        tmsg.showerror('Error','Failure to Launch Attack! No Target Selected!')
    else:
        btn_main.config(text="Stop Attack", bg="green", command=stop_attack)
        disable_everything()

        if toggle_button3.get()==1:
            if options[1] == dropdown.get():
                target_time = datetime.now() + timedelta(seconds=minutes.get()*60)
                check_time(target_time)
                return

        t1 = threading.Thread(target=launch_taskkill)
        t1.start()

def stop_attack():
    enable_everything()
    global loop, abort
    abort=True
    loop=False
    btn_main.config(text="Activate Taskkill", bg="red", fg="black",command=initiate_taskkill)


# Applying Frames
f1 = Frame(borderwidth=10, bg=global_color)
f2 = Frame(borderwidth=10, bg=global_color)
f3 = Frame(borderwidth=10, bg=global_color)
f4 = Frame(borderwidth=10, bg=global_color)


# Frame 1
btn1 = Button(f1,
    text="Add Target",
    bg='black',
    fg="white", 
    pady=7, 
    padx=7,
    command=choose_target)

btn2 = Button(f1,
    text="Remove Target",
    bg='black',
    fg="white", 
    pady=7, 
    padx=7,
    command=withdraw_target)

ch1 = Checkbutton(f1, 
    text="Toggle Administrator Access", 
    bg=global_color, 
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button1, 
    command=toggle_admin)

spacing(f1)
ch1.pack(side=LEFT)
spacing(f1)
btn1.pack(side=LEFT)
spacing(f1)
btn2.pack(side=LEFT)

# Frame 2
l1 = Listbox(f2, 
    height = 10, 
    width = 35,
    justify="center", 
    bg = "black",
    activestyle = 'dotbox', 
    font = "TimesNewRoman",
    fg = "white",
    highlightthickness=0,
    state=DISABLED)

scrollbar = Scrollbar(f2, 
    orient=VERTICAL, 
    bg="black")



scrollbar.pack(side=RIGHT, fill=Y)
l1.pack(side=LEFT)

# Some Configurations
l1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=l1.yview)

# Frame 3
ch2 = Checkbutton(f3, 
    text="Indefinite Attack", 
    bg=global_color,
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button2, 
    command=toggle_attack1)

ch3 = Checkbutton(f3, 
    text="Timed Attack", 
    bg=global_color,
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button3, 
    command=toggle_attack2)

en1 = Entry(f3,
    width=6,
    fg="black",
    textvariable=minutes,
    font="comicsansms 9 bold",
    state=DISABLED
    )

choice = ttk.Combobox(
    f3, 
    textvariable=dropdown,
    values=options, 
    state="disabled",
    width=12,
)

lbl1 = Label(f3,
    text="minutes",
    bg=global_color,
    font="comicsansms 9 italic",
    )

ch2.pack(side=LEFT)
spacing(f3)
ch3.pack(side=LEFT)
spacing(f3)
choice.pack(side=LEFT)
spacing(f3)
en1.pack(side=LEFT)
lbl1.pack(side=LEFT)


# Frame 4
ch4 = Checkbutton(f4, 
    text="Hide Window When Activated", 
    bg=global_color,
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button4, 
    command=toggle_attack3)

ch5 = Checkbutton(f4, 
    text="Apply Force Kill", 
    bg=global_color,
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button5, 
    command=toggle_attack4)


ch4.pack(side=LEFT)
spacing(f4)
ch5.pack(side=LEFT)


# Packing Frames
f1.pack(anchor=S)
f2.pack(anchor=S)
f3.pack(anchor=S)
f4.pack(anchor=S)


btn_main = Button(text="Activate Taskkill",
    bg='red',
    fg="black", 
    pady=7, 
    padx=7,
    command=initiate_taskkill)

btn_main.pack()

all_features = [btn1, btn2, ch1, ch2, ch3, en1, choice, ch4, ch5]

check_admin()
root.mainloop()
