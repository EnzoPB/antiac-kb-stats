import gzip
import os
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *

class ProcessGUI():
    def __init__(self, root, selected_mc_instances, username):
        self.root = root
        self.root.title('AntiAC KnockbackFFA Stats')
        self.root.resizable(False, False)

        self.selected_mc_instances = selected_mc_instances
        self.username = username

        self.build_ui()
    
    def build_ui(self):
        self.main_frame = Frame(self.root)
        self.main_frame.pack(padx=20, pady=10)

        self.loading_label = Label(self.main_frame, text='Loading...')
        self.loading_label.pack()

        self.progress_bar = Progressbar(self.main_frame, mode='indeterminate', length=60)
        self.progress_bar.pack(ipadx=100)
        self.progress_bar.start()
        
        self.status_label = Label(self.main_frame, text='')
        self.status_label.pack()

        self.status_bis_label = Label(self.main_frame, text='')
        self.status_bis_label.pack()

        self.process()
        

    def process(self): # process the logs files
        self.deaths = {
            'players': {},
            'days': {},
            'count': 0
        }
        self.kills = {
            'players': {},
            'days': {},
            'count': 0
        }
        self.killstreaks = {
            'kills': {},
            'days': {},
            'count': 0
        }
        for instance, path in self.selected_mc_instances:
            files_list = os.listdir(path) # get every file in the instance's logs directory
            for i in range(len(files_list)):
                file_name = files_list[i]
                self.status_label['text'] = f'Processing "{instance}" logs ({i}/{len(files_list)})'

                if file_name.endswith('.log.gz') and file_name.startswith('20') or file_name == 'latest.log': # only take gzip files starting with "20-" OR the uncompressed latest.log file, so we are sure that these are mc logs
                    file_path = os.path.join(path, file_name)
                    date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y') # format the file's modified date into a dd/mm/yyyy format
                    if file_name == 'latest.log':
                        file = open(file_path, 'r') # read the file
                    else: # if the file needs decompression
                        file = gzip.open(file_path, 'rt') # decompress the file and read it as text

                    lines = file.readlines()
                    for i in range(len(lines)):
                        # fun fact: the whole process could be almost instantaneous if we remove the next 3 lines,
                        # but that's not fun and i want a cool loading window :)
                        if i % 50 == 0: # only update 1/50 times
                            self.status_bis_label['text'] = f'File {file_name}, line {i}/{len(lines)}'
                            self.root.update() # tick the window to avoid a freeze

                        line = lines[i]

                        if '[CHAT] [Knockback]' in line: # the only we are interested in begins with [CHAT] [Knockback]
                            # "[CHAT] [Knockback] {username} has a Killstreak! {killstreak} Kills"
                            if f'{self.username} has a Killstreak' in line:
                                killstreak = line.split(' ')[9] # number of kills in the killstreak
                                self.killstreaks['count'] += 1
                                self.killstreaks['kills'] = self.dict_add_count(self.killstreaks['kills'], killstreak, 1)
                                self.killstreaks['days'] = self.dict_add_count(self.killstreaks['days'], date, 1)

                            # "[CHAT] [Knockback] You killed {killed_username}! +X Trophies"
                            elif 'You killed' in line:
                                killed_username = line.split(' ')[7][:-1] # killed player's username
                                self.kills['count'] += 1
                                self.kills['players'] = self.dict_add_count(self.kills['players'], killed_username, 1)
                                self.kills['days'] = self.dict_add_count(self.kills['days'], date, 1)

                            # "[CHAT] [Knockback] You were killed by {killer_username}!"
                            # "[CHAT] [Knockback] You died!"
                            elif 'You were killed' in line or 'You died' in line:
                                self.deaths['count'] += 1
                                self.deaths['days'] = self.dict_add_count(self.deaths['days'], date, 1)
                                if 'You were killed' in line: # killed by a player
                                    killer_username = line.split(' ')[9][:-1] # killer's username
                                    self.deaths['players'] = self.dict_add_count(self.deaths['players'], killer_username, 1)
                                else: # killed by no one, most likely just fell into the void
                                    self.deaths['players'] = self.dict_add_count(self.deaths['players'], 'NONE', 1)
                    file.close()
        print('Done')
        print('Kills', self.kills['count'])
        print('Killstreaks', self.killstreaks['count'])
        print('Deaths', self.deaths['count'])

        self.root.destroy() # close the window


    def dict_add_count(self, _dict, key, amount): # increase or create a count in a dictionnary
        try:
            _dict[key] += amount
        except KeyError:
            _dict[key] = amount
        return _dict
                        