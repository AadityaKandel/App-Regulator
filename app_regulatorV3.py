from tkinter import *
import subprocess
import tkinter.messagebox as tmsg
import os
import threading
import tkinter.filedialog as filedialog
from tkinter.simpledialog import askstring
from tkinter import ttk
from datetime import datetime, timedelta
import ctypes
import sys
import ast # Converts the file content into a list if possible
from cryptography.fernet import Fernet

root = Tk()
# root.geometry("700x500")
root.minsize(700,500)
root.maxsize(900,530)
root.title("App Regulator/Blocker")
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
dropdown = StringVar() # Option Values
loop = None
admin_info = '''
This feature is only available for an executable version of this app\n
But you can use this feature by manually launching this script as admin from cmd
'''
camouflage_text="Before Attempting Camouflage, choose an Application to use it's name to decieve the admin"
camouflage_app_name = None
abort = False
details = []
already_saved = False
file_path=None
auto_load_file=False
nothing_changed=True
cama_demo=''
camouflage_manual = '''
The Camouflage Technique
It allows the user to make an illusion of running a different app as an administrator but in reality, this app is being ran as admin allowing it higher authorities.

Step1: Click on the "Tools" menu & "Camouflage"\n
Step2: Choose the app to make an illusion\n
Step3: This app will create a fake "Run as administrator" for the app you choose (let's say Notepad)\n
(While this app will secretly launch as administrator, it will disappear immediately & run Notepad)\n
Step4: Just close Notepad and create a document named "0000.txt" in the app directory\n
Step5: The app will suddently open allowing you system level authorities
'''

app_manual='''
Copyright © App Regulator (www.github.com/AadityaKandel)

Manual
This app allows you to block any application within your system by simply choosing it
You can use the "Add Target" button in the UI to add the app you want to block
You can also use the "Remove Target" button in the UI to remove the app you added
Similarly, you can use checkboxes to perform their respective tasks as labelled

*** Functions of Each CheckBoxes ***
Allow Admin = It allows you system level authorities blocking any & every app you add\n
Indefinite Attack = It allows you to launch indefinite block to the app you choose\n
Timed Attack = It allows you to launch attack in the following manners
            Once Every [minute] = It blocks the added app every given minute
            After [minute] = It blocks the app only once after given minute and ends\n
Hide Window When Activated = It hides itself when it blocks the apps you choose\n
Apply Force Kill = It forcibly blocks the app if it cannot be blocked easily\n

*** MENUS ***
It has menus to create a profile to save your daily tasks
Similarly, it also auto-loads your last file so you don't need to worry about loading it again
'''

about_app='''
Made By Aaditya Kandel\n
www.github.com/AadityaKandel
'''

# Enc & Dec Variables
encryption_key = b'X7Z0k2aY5FqznQUMGDfLnFzCzyTqxJbWuJAUBKyoPNs='
enc = Fernet(encryption_key)

# Setting Variables
toggle_button2.set(1)
minutes.set(1)
dropdown.set('Once Every')

# Checking Two Specific Operations
if os.path.exists("0000.txt"):
    os.remove('0000.txt')
if os.path.exists("manual.txt"):
        os.remove("manual.txt")

try:
    def temporary_loop():
        root.withdraw()
        while (True):
            if os.path.exists("0000.txt"):
                root.deiconify()
                break

    f = open('demo.json','r', encoding="utf-8")
    cama_demo = f.read()
    f.close()
    if os.path.exists(cama_demo):
        os.rename(cama_demo,"app_regulator.exe")
        os.remove('demo.json')

    temporary_loop()
except:
    pass


# Defining Functions
def allow_admin(destination):
    global camouflage_app_name,cama_demo
    try:
        subprocess.run(
            ['powershell', '-Command', f'Start-Process "{destination}" -Verb RunAs'],
            check=True
        )

        if camouflage_app_name !=None:
            os.startfile(camouflage_app_name)
            camouflage_app_name=None

        sys.exit()
    except subprocess.CalledProcessError:
        temporary_loop()
        os.rename(cama_demo, "app_regulator.exe")
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
        toolsmenu.entryconfig(0, state=DISABLED)
        if os.path.exists("0000.txt"):
            os.remove("0000.txt")
        

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
    global target_name, exe_name, nothing_changed
    nothing_changed=False
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
            a = filedialog.askopenfiles(mode='r', title=target_text, filetypes = ['Executable .exe'], initialdir="Desktop")
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
    global target_name, nothing_changed
    nothing_changed=False
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
    global nothing_changed
    nothing_changed=False

    if toggle_button2.get() == 1:
        toggle_button3.set(0)
        en1.config(state=DISABLED)
        choice.config(state=DISABLED)
    else:
        toggle_button3.set(1)
        en1.config(state=NORMAL)
        choice.config(state='readonly')

def toggle_attack2(): # Timed Attack
    global nothing_changed
    nothing_changed=False

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
    global nothing_changed
    nothing_changed=False

    if toggle_button4.get()==1:
        tmsg.showinfo('Info','Save 0000.txt in the App Directory to Show the App Again')
    if os.path.exists('0000.txt'):
        os.remove('0000.txt')

def toggle_attack4():
    global nothing_changed
    nothing_changed=False

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

def gather_details():
    global details
    details = [
    target_name,
    toggle_button2.get(), 
    toggle_button3.get(), 
    dropdown.get(), 
    minutes.get(), 
    toggle_button4.get(), 
    toggle_button5.get()
    ]
    encrypt_everything()

def execute_details():
    global details,exe_name,toggle_button2,toggle_button3,toggle_button4,toggle_button5,dropdown,minutes,target_name

    loaded_targets = details[0]
    target_name = []
    l1.config(state=NORMAL)
    l1.delete(0,END)
    l1.config(state=DISABLED)
    for x in loaded_targets:
        exe_name = x
        target_name.append(exe_name)
        fill_target(len(target_name)-1)

    # Loading Configurations
    toggle_button5.set(details[6])
    dropdown.set(details[3])
    minutes.set(details[4])

    # Loading Special Case Configurations
    toggle_button2.set(details[1]) # Indefinite
    toggle_button3.set(details[2]) # Timed
    toggle_button4.set(details[5])
    root.update()

    if toggle_button3.get() == 1:
        choice.config(state="readonly")
        en1.config(state=NORMAL)
    else:
        choice.config(state=DISABLED)
        en1.config(state=DISABLED)

    if toggle_button4.get()==1:
        toggle_button4.set(0)
        ch4.invoke()
    

def loadfile(exists):
    global details, already_saved, file_path, auto_load_file

    open_path = file_path

    if not exists:
        open_path = filedialog.askopenfilename(defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("Text Files", "*.txt")])

        if open_path == '':
            tmsg.showerror('Error','No File Selected')
            return

        file_path=open_path

    auto_load_file = exists

    f = open(open_path,'rb')
    file_content = f.read()
    # print(file_content)
    file_content = decrypt_everything(file_content)
    if not file_content:
        if os.path.exists("path.json"):
            os.remove("path.json")
        return
    # Now go for decryption
    f.close()

    file_content = file_content.decode('utf-8')
    details = ast.literal_eval(file_content)
    execute_details()
    already_saved=True
    root.title(open_path+'- Loaded')

def savefile():
    global already_saved,file_path,details
    if not already_saved:
        return saveasfile()

    gather_details()
    f = open(file_path,'wb')
    details = details.encode('utf-8') # Convert to bytes
    f.write(details)
    f.close()
    root.title(file_path+' Saved')
    return savepath()


def saveasfile():
    global already_saved,details,file_path

    temp_path = filedialog.asksaveasfilename(defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("Text Files", "*.txt")])

    if temp_path=='':
        tmsg.showerror('Error','Invalid File Path')
        return False

    file_path=temp_path # This is done because if file path is directly used, it can lead to some issues on other functions above
    gather_details()
    details = details.encode('utf-8') # Convert to bytes
    f = open(file_path,'wb')
    f.write(details)
    f.close()

    root.title(file_path+' Saved')
    already_saved=True
    return savepath()

def autoload():
    global file_path
    try:
        f = open('path.json','r')
    except:
        return
    file_path = f.read()
    f.close()

    if os.path.exists(file_path):
        loadfile(True)

def savepath():
    global file_path
    f = open('path.json','w')
    f.write(file_path)
    f.close()
    return True

def camouflage():
    tmsg.showinfo('Info','This Feature Only Works On The Executable Version Of This File')
    # global camouflage_app_name,cama_demo
    # if os.path.exists("0000.txt"):
    #     os.remove("0000.txt")

    # tmsg.showinfo('Info',camouflage_text)
    # try:
    #     camouflage_app = filedialog.askopenfile(mode='r', 
    #         title="Choose A Camouflage App", 
    #         filetypes = ['Executable .exe'], 
    #         initialdir="Desktop"
    #         )
    # except:
    #     return tmsg.showerror('Error',"App Doesn't Exist")
    # if camouflage_app=='':
    #     return tmsg.showerror('Error','Camouflage Error! No App Selected')
    # cama_app = camouflage_app.name
    # camouflage_app_name = cama_app
    # camouflage_name = cama_app.rindex('/')
    # cama_app = cama_app[camouflage_name+1::]
    # cama_app="‎"+cama_app

    # f = open('demo.json','w', encoding="utf-8")
    # f.write(cama_app)
    # cama_demo=cama_app
    # f.close()

    # os.rename('app_regulator.exe',cama_app)
    # current_location = os.getcwd()
    # app_name = f"\\{cama_app}"
    # final_location = os.path.join(current_location+app_name)
    # tmsg.showinfo('Admin Attempt','The App Will Now Attempt to Request For Admin Access....')
    # root.withdraw()
    # allow_admin(final_location)

def how_camouflage():
    tmsg.showinfo('How to use Camouflage?',camouflage_manual)

def manual():
    f = open('manual.txt','w')
    f.write(app_manual)
    f.close()
    os.startfile("manual.txt")

def about():
    tmsg.showinfo("About App",about_app)

def encrypt_everything():
    global details
    details = f'{details}'
    details = details.encode('utf-8')
    encrypted_text = enc.encrypt(details)
    encrypted_text=encrypted_text.decode('utf-8')
    details=encrypted_text

def decrypt_everything(encrypted_text):
    try:
        decrypted_text = enc.decrypt(encrypted_text)
    except:
        if auto_load_file:
            tmsg.showerror('Error','Auto Load Failed! File Contents Corrupted!')
        else:
            tmsg.showerror('Error','Cannot Load File! File Contents Are Corrupted!')
        return False

    return decrypted_text

def autosave():
    global nothing_changed
    if nothing_changed:
        sys.exit()
    qna = tmsg.askquestion('Question','Do you want to save before closing?')
    if qna=="yes":
        if not savefile():
            return
    else:
        pass
    sys.exit()

# Creating Menus
menubar = Menu(root)

# File Menu
filemenu = Menu(menubar, tearoff=0)  
filemenu.add_command(label="Save Profile", command=savefile)
filemenu.add_command(label="Save as...", command=saveasfile)
filemenu.add_command(label="Load Profile", command=lambda:loadfile(False))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=sys.exit)

# Tools Menu
toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Camouflage", command=camouflage)
toolsmenu.add_command(label="How to use Camouflage?",command=how_camouflage)

# Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About",command=about)
helpmenu.add_command(label="Manual", command=manual)


menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Tools", menu=toolsmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

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
    text="Indefinite Block", 
    bg=global_color,
    offvalue=0, 
    onvalue=1, 
    variable=toggle_button2, 
    command=toggle_attack1)

ch3 = Checkbutton(f3, 
    text="Timed Block", 
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
    state=DISABLED,
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
    text="Apply Force Block", 
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


btn_main = Button(text="Block",
    bg='red',
    fg="black", 
    pady=7, 
    padx=7,
    command=initiate_taskkill)

btn_main.pack()

all_features = [btn1, btn2, ch2, ch3, en1, choice, ch4, ch5]

# Smth that cannot be appended above

root.config(menu=menubar)
check_admin()
autoload()
root.protocol("WM_DELETE_WINDOW",autosave)
root.mainloop()
