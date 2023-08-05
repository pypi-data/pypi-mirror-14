# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
import tkinter as tk
import tkinter.constants as tc
import tkinter.scrolledtext as sc
import tkinter.ttk as ttk
from windy.gui.locale import Locale


class About(ttk.Frame):

    def __init__(self, root, parent):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        
        self.create_gui()
        root.wm_title(Locale.about.value)
                
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update

    def create_gui(self):
        self.txt = sc.ScrolledText(self, undo=True)
        self.txt.grid(column=0, row=0, sticky=tc.NSEW, columnspan=2)
        self.txt.delete("0.0", tc.END)
        self.txt.insert("0.0", Locale.about_desc.value)
        self.txt.configure(state=tc.DISABLED)

        button = ttk.Button(self, text=Locale.close.value, command=self.quit)
        button.grid(column=1, row=1, sticky=tc.EW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def quit(self):
        self.root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    About(root, None).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
    root.mainloop()
