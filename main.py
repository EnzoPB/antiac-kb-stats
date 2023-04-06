import tkinter as tk
from tkinter import ttk

from _select import SelectGUI
from process import ProcessGUI
from results import ResultsGUI

root = None

def show_select():
    global root
    # create the first window (select window)
    root = tk.Tk()
    root.style = ttk.Style()
    #root.style.theme_use('vista') # modern windows style

    select_gui = SelectGUI(root)
    root.mainloop()
    
    load_logs(select_gui.selected_mc_instances, select_gui.username)

def load_logs(selected_mc_instances, username):
    global root
    # create the second window (loading window)
    root = tk.Tk()
    root.style = ttk.Style()
    #root.style.theme_use('vista') # modern windows style

    process_gui = ProcessGUI(root, selected_mc_instances, username)
    root.mainloop()

    show_results(process_gui.deaths, process_gui.kills, process_gui.killstreaks)

def show_results(deaths, kills, killstreaks):
    global root
    # create the last window (results window)
    root = tk.Tk()
    root.style = ttk.Style()
    #root.style.theme_use('vista') # modern windows style

    results_gui = ResultsGUI(root, deaths, kills, killstreaks)
    root.mainloop()

if __name__ == '__main__':
    show_select()
