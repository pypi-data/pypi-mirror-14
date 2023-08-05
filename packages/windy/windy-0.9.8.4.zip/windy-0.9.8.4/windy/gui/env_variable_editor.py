# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
import enum

import tkinter as tk
import tkinter.constants as tc
import tkinter.scrolledtext as sc
import tkinter.ttk as ttk
from windy.gui.locale import Locale
import windy.service.environment_variables_service as envvarservice


class EnvironmentVariableEditor(ttk.Frame):

    def __init__(self, root, parent, name="", value="", scope=envvarservice.Scope.user, edit_mode=False):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        self.edit_mode = edit_mode
        
        root.wm_title(Locale.edit.value)
        self.create_gui()
        self.refresh(name, value, edit_mode, scope);
                
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update

    def create_gui(self):
        separatorLabel = ttk.Label(self, text=Locale.env_var_title.value, anchor=tc.NW)
        separatorLabel.grid(column=0, row=0, sticky=tc.EW, columnspan=6)
        
        self.nameLabel = ttk.Label(self, text=Locale.name.value, anchor=tc.NW)
        self.nameLabel.grid(column=0, row=1, sticky=tc.EW)
        
        self.nameModel = tk.StringVar()
        self.nameEntry = ttk.Entry(self, textvariable=self.nameModel)
        self.nameEntry.grid(column=1, row=1, sticky=tc.EW, columnspan=5)
        
        self.valueLabel = ttk.Label(self, text=Locale.value.value, anchor=tc.NW)
        self.valueLabel.grid(column=0, row=2, sticky=tc.NW)
        
        self.txt = sc.ScrolledText(self, undo=True)
        self.txt.grid(column=1, row=2, sticky=tc.NSEW, columnspan=5)
        
        self.scopeModel = tk.IntVar()        
        self.scopeCheckbox = ttk.Checkbutton(self, text=Locale.system.value, variable=self.scopeModel,
                 onvalue=1, offvalue=0)
        self.scopeCheckbox.grid(column=1, row=3, sticky=tc.W)
        
        button = ttk.Button(self, text=Locale.save.value, command=self.save)
        button.grid(column=2, row=4, sticky=tc.EW)

        button = ttk.Button(self, text=Locale.new.value, command=self.new)
        button.grid(column=3, row=4, sticky=tc.EW)

        button = ttk.Button(self, text=Locale.cancel.value, command=self.quit)
        button.grid(column=4, row=4, sticky=tc.EW)

        button = ttk.Button(self, text=Locale.close.value, command=self.quit)
        button.grid(column=5, row=4, sticky=tc.EW)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=7)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
    
    def refresh(self, name, value, edit_mode=False, scope=envvarservice.Scope.user):
        self.nameModel.set(name)
        
        self.txt.configure(state=tc.NORMAL)
        self.txt.delete("0.0", tc.END)
        self.txt.insert("0.0", value)
        
        if scope is envvarservice.Scope.user:
            self.scopeModel.set(0)
        else: 
            self.scopeModel.set(1)
        
        if edit_mode:
            self.nameEntry.configure(state=tc.DISABLED)
            self.scopeCheckbox.configure(state=tc.DISABLED)
        else:
            self.nameEntry.configure(state=tc.NORMAL)
            if  not self.parent.restricted:
                self.scopeCheckbox.configure(state=tc.NORMAL)
            else: 
                self.scopeCheckbox.configure(state=tc.DISABLED)        
            
    def new(self):
        self.refresh("", "")
            
    def save(self):
        name = self.nameModel.get().strip()
        value = self.txt.get(1.0, tc.END).strip()
        valid = (len(name) > 0) and (len(value) > 0)
        if not valid:
            tk.messagebox.showinfo(Locale.empty_entry_not_allowed_title.value, Locale.empty_entry_not_allowed_desc.value)
            return
        
        if(self.scopeModel.get() == 0):
            self.parent.winUserEnvVarService.addEnvVariable(name, value)
            self.refresh(name, value, True, envvarservice.Scope.user)
            self.parent.refresh()
        else:
            try:
                self.parent.winSystemEnvVarService.addEnvVariable(name, value)
                self.refresh(name, value, True, envvarservice.Scope.system)
                self.parent.refresh()
            except WindowsError:
                tk.messagebox.showwarning(Locale.admin_role_title.value, Locale.admin_role_desc.title)

    def quit(self):
        self.root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    EnvironmentVariableEditor(root, None).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
    root.mainloop()
