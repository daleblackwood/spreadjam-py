import tkinter as tk
from tkinter import filedialog
from jamstats import get_stats, get_totals, format_length

class SpreadJamUI():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("SpreadJam")
        self.win.minsize(200, 600)
        self.lbl_time = tk.StringVar()
        self.lbl_time.set("...")
        lab=tk.Label(self.win, textvariable=self.lbl_time, bg='#40E0D0', fg='#FF0000')
        lab.place(x=20, y=30)
        self.select_folder()
        self.update()
        self.win.mainloop()

    def select_folder(self):
        self.vid_stats = None
        self.vid_folder = filedialog.askdirectory(title="Select a folder to Jam from...")
        print("Selected folder %s" % self.vid_folder)

    def update(self):
        self.vid_stats = get_stats(self.vid_folder, self.vid_stats)
        count, size, length = get_totals(self.vid_stats)
        self.lbl_time.set("%i vids, %s length" % (count, format_length(length)))
        self.win.after(1000, self.update)

app=SpreadJamUI()
