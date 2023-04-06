import os
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import *

class SelectGUI():
    def __init__(self, root):
        self.root = root
        self.root.title('AntiAC KnockbackFFA Stats')
        self.root.resizable(False, False)

        self.appdata = os.getenv('APPDATA') # C:\Users\username\AppData\Roaming
        self.user_dir = os.path.expanduser('~') # C:\Users\username
        if self.appdata == None:
            self.appdata = self.user_dir

        self.build_ui()
    
    def build_ui(self):
        self.username_input_frame = Frame(self.root)
        self.username_input_frame.pack(padx=20, pady=10)
        self.username_input_label = Label(self.username_input_frame, text='Minecraft username: ')
        self.username_input_label.pack(side=LEFT)
        self.username_input = Entry(self.username_input_frame)
        self.username_input.pack(side=RIGHT)

        self.mc_instances_frame = Frame(self.root)
        self.mc_instances_frame.pack(padx=20)

        self.label = Label(self.mc_instances_frame, text='Select one or more Minecraft client/launcher')
        self.label.pack()

        self.mc_instances = self.get_instances()
        self.mc_instances_list = Listbox(self.mc_instances_frame, selectmode=MULTIPLE, width=50)
        for instance in self.mc_instances:
            self.mc_instances_list.insert(END, instance[0])
        self.mc_instances_list.pack()

        self.add_instance_button = Button(self.mc_instances_frame, text='Add a client/launcher', command=self.add_instance)
        self.add_instance_button.pack()

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side=BOTTOM, padx=20, pady=10)

        self.confirm_button = Button(self.bottom_frame, text='Confirm', command=self.confirm, width=50)
        self.confirm_button.pack()

    def add_instance(self):
        messagebox.showinfo(message='Please select the "logs" folder in your game files')
        selected_folder = filedialog.askdirectory(initialdir=self.appdata)
        if os.path.exists(selected_folder):
            self.mc_instances.append((selected_folder, selected_folder))
            self.mc_instances_list.insert(END, selected_folder)
        else:
            messagebox.showerror(message='The folder you selected is not valid')

    def confirm(self):
        if len(self.username_input.get()) == 0:
            messagebox.showwarning(message='Please enter an username to continue')
            return

        if len(self.mc_instances_list.curselection()) == 0:
            messagebox.showwarning(message='Please select at least one client/launcher to continue')
            return

        self.selected_mc_instances = []
        for i in self.mc_instances_list.curselection():
            self.selected_mc_instances.append(self.mc_instances[i])
            self.username = self.username_input.get()

        self.root.destroy()

    def get_instances(self): # get a list of minecraft instances (minecraft launcher, lunar client, etc...)
        instances = []
        # minecraft launcher
        if os.path.exists(os.path.join(self.appdata, '.minecraft', 'logs')): # make sure the logs folder exists
            instances.append(('Minecraft Launcher (all versions)', os.path.join(self.appdata, '.minecraft', 'logs'))) # add the game folder and instance name to the list
        
        # lunar client
        if os.path.exists(os.path.join(self.user_dir, '.lunarclient', 'offline')):
            for version in os.listdir(os.path.join(self.user_dir, '.lunarclient', 'offline')): # differents minecraft version are stored in this folder
                if os.path.exists(os.path.join(self.user_dir, '.lunarclient', 'offline', version, 'logs')): # check for each versions if the log folder exists
                    instances.append((f'Lunar Client version {version}', os.path.join(self.user_dir, '.lunarclient', 'offline', version, 'logs'))) # add the game folder and instance name to the list

        # badlion client
        if os.path.exists(os.path.join(self.appdata, '.minecraft', 'logs', 'blclient', 'minecraft')): # BLC logs are located in the .minecraft/logs/blclient/minecraft folder, instead of a separate env like lunar
            instances.append(('Badlion Client (all versions)', os.path.join(self.appdata, '.minecraft', 'logs', 'blclient', 'minecraft'))) # add the game folder and instance name to the list
        
        return instances