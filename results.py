import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
from tkinter.ttk import *

class ResultsGUI():
    def __init__(self, root, deaths, kills, killstreaks):
        self.root = root
        self.root.title('AntiAC KnockbackFFA Stats')

        self.deaths = deaths
        self.kills = kills
        self.killstreaks = killstreaks

        self.build_ui()
    
    def build_ui(self):
        self.tab_control = Notebook(self.root)

        self.tab_disclaimer = Frame(self.tab_control)
        self.tab_disclaimer.pack(padx=10, pady=10)

        self.tab_deaths = Frame(self.tab_control)
        self.tab_deaths.pack(padx=10, pady=10)

        self.tab_kills = Frame(self.tab_control)
        self.tab_kills.pack(padx=10, pady=10)

        self.tab_killstreaks = Frame(self.tab_control)
        self.tab_killstreaks.pack(padx=10, pady=10)

        self.tab_about = Frame(self.tab_control)
        self.tab_about.pack(padx=10, pady=10)

        self.tab_control.add(self.tab_disclaimer, text='General')
        self.tab_control.add(self.tab_deaths, text='Deaths')
        self.tab_control.add(self.tab_kills, text='Kills')
        self.tab_control.add(self.tab_killstreaks, text='Killstreaks')
        self.tab_control.add(self.tab_about, text='About')
        self.tab_control.pack(expand=1, fill='both')

        self.build_ui_deaths()
        self.build_ui_kills()
        self.build_ui_killstreaks()
        self.build_ui_about()

    def build_ui_deaths(self):
        self.tab_deaths_control = Notebook(self.tab_deaths)

        self.tab_deaths_players = Frame(self.tab_deaths_control)
        self.tab_deaths_players.pack(padx=10, pady=10)

        self.tab_deaths_days = Frame(self.tab_deaths_control)
        self.tab_deaths_days.pack(padx=10, pady=10)

        self.tab_deaths_control.add(self.tab_deaths_players, text='Players')
        self.tab_deaths_control.add(self.tab_deaths_days, text='Days')
        self.tab_deaths_control.pack(expand=1, fill='both')

        deaths_players_plt = self.pie(self.deaths['players'])
        self.plot(deaths_players_plt, self.tab_deaths_players, (0, 0))

        deaths_days_plt = self.pie(self.deaths['days'])
        self.plot(deaths_days_plt, self.tab_deaths_days, (1, 0))

    def build_ui_kills(self):
        self.tab_kills_control = Notebook(self.tab_kills)

        self.tab_kills_players = Frame(self.tab_kills_control)
        self.tab_kills_players.pack(padx=10, pady=10)

        self.tab_kills_days = Frame(self.tab_kills_control)
        self.tab_kills_days.pack(padx=10, pady=10)

        self.tab_kills_control.add(self.tab_kills_players, text='Players')
        self.tab_kills_control.add(self.tab_kills_days, text='Days')
        self.tab_kills_control.pack(expand=1, fill='both')

        kills_players_plt = self.pie(self.kills['players'])
        self.plot(kills_players_plt, self.tab_kills_players, (0, 0))

        kills_days_plt = self.pie(self.kills['days'])
        self.plot(kills_days_plt, self.tab_kills_days, (1, 0))



    def build_ui_killstreaks(self):
        self.tab_killstreaks_control = Notebook(self.tab_killstreaks)

        self.tab_killstreaks_kills = Frame(self.tab_killstreaks_control)
        self.tab_killstreaks_kills.pack(padx=10, pady=10)

        self.tab_killstreaks_days = Frame(self.tab_killstreaks_control)
        self.tab_killstreaks_days.pack(padx=10, pady=10)

        self.tab_killstreaks_control.add(self.tab_killstreaks_kills, text='Kills')
        self.tab_killstreaks_control.add(self.tab_killstreaks_days, text='Days')
        self.tab_killstreaks_control.pack(expand=1, fill='both')

        killstreaks_kills_plt = self.pie(self.killstreaks['kills'])
        self.plot(killstreaks_kills_plt, self.tab_killstreaks_kills, (0, 0))

        killstreaks_days_plt = self.pie(self.killstreaks['days'])
        self.plot(killstreaks_days_plt, self.tab_killstreaks_days, (1, 0))

    def build_ui_about(self):
        self.about_label = Label(self.tab_about, text="test")
        self.about_label.pack()

    def pie(self, data):
        labels = []
        sizes = []
        i = 0
        fig = plt.figure()
        for x in sorted(data, key=data.get, reverse=True):
            if i <= 50:
                y = data[x]
                labels.append(f'{x} ({y})')
                sizes.append(y)
                i += 1

        plt.pie(sizes, labels=labels, rotatelabels=True, textprops={'size': 8})
        plt.axis('equal')
        plt.tight_layout()
        return fig

    def plot(self, figure, master, pos):
        canvas = FigureCanvasTkAgg(figure, master = master)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, master)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)