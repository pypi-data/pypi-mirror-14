# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
import tkinter as tk
import tkinter.constants as tc
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import windy.gui.about as guiabout
import windy.gui.env_variable_editor as guieditor
import windy.gui.env_variable_import as guiimport
from windy.gui.locale import Locale
import windy.service.environment_variables_service as envvarservice


class Application(tk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.winUserEnvVarService = envvarservice.EnvironmentVariableService(envvarservice.Scope.user)
        self.winSystemEnvVarService = envvarservice.EnvironmentVariableService(envvarservice.Scope.system)
        self.header = [Locale.scope.value, Locale.name.value, Locale.value.value]
        
        self.menubar = tk.Menu(self)
        
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=Locale.file.value, menu=file_menu)
        file_menu.add_command(label=Locale.exit.value, command=self.quit)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=Locale.help.value, menu=help_menu)
        help_menu.add_command(label=Locale.about.value, command=self.about)

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)
        
        
        self.createGui()
        self.refresh()
        self.restricted = False
        try:
            self.winSystemEnvVarService.getEnvVariable("PATH")
        except WindowsError:
            print("System environment variables can't be loaded because you need to run the application in the admin mode...")
            self.restricted = True
            mb.showwarning(Locale.system_permission_title.value, Locale.system_permission_desc.value)
    
    def createGui(self):
        separatorLabel = ttk.Label(text=Locale.env_variables.value, anchor=tc.NW)
        separatorLabel.pack(fill=tc.X)
        
        container = ttk.Frame()
        container.pack(fill=tc.BOTH, expand=True)
        self.tree = ttk.Treeview(columns=self.header, show="headings")
        vsb = ttk.Scrollbar(orient=tc.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky=tc.NSEW, in_=container)
        vsb.grid(column=1, row=0, sticky=tc.NS, in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        importButton = ttk.Button(text=Locale.importThreeDots.value, command=self.importEnvVars)
        importButton.pack(side=tc.RIGHT)
         
        importButton = ttk.Button(text=Locale.remove.value, command=self.remove)
        importButton.pack(side=tc.RIGHT)
         
        importButton = ttk.Button(text=Locale.edit.value, command=self.edit)
        importButton.pack(side=tc.RIGHT)
         
        addButton = ttk.Button(text=Locale.add_new.value, command=self.addNew)
        addButton.pack(side=tc.RIGHT)
    
    def refresh(self):
        self.envVariables = self.winUserEnvVarService.getAllEnvVariable()
        try:
            systemVars = self.winSystemEnvVarService.getAllEnvVariable()
            self.envVariables.extend(systemVars)
        except WindowsError:
            pass  # user already informed about the lack of the permissions when the application has first started
                
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.envVariables:
            self.tree.insert('', tc.END, values=(item[0].name, item[1], item[2]))
        
    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        # data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))
    
    def addNew(self):
        newWindow = tk.Toplevel(self)
        guieditor.EnvironmentVariableEditor(newWindow, self, scope=envvarservice.Scope.user, edit_mode=False).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
        self.after(1, lambda: newWindow.focus_force())    

    def getSelected(self):
        curItem = self.tree.focus()
        selected = self.tree.item(curItem)
        scope = selected["values"][0]
        name = selected["values"][1]
        value = selected["values"][2]
        return name, value, scope

    def edit(self):
        try:
            name, value, scope = self.getSelected()
        except IndexError:
            tk.messagebox.showinfo(Locale.env_var_selection.value, Locale.env_var_selection_edit.value)   
            return;
        
        newWindow = tk.Toplevel(self)
        guieditor.EnvironmentVariableEditor(newWindow, self, name, value, envvarservice.Scope[scope], True).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
        self.after(1, lambda: newWindow.focus_force())
    
    def remove(self):
        try:
            name, value, scope = self.getSelected()
        except IndexError:
            tk.messagebox.showinfo(Locale.env_var_selection.value, Locale.env_var_selection_remove.value)   
            return;
        
        result = tk.messagebox.askquestion(Locale.env_var_delete_title.value, Locale.env_var_delete_desc.value.format(name=name))
        if result != tk.messagebox.YES:
            return
        if(envvarservice.Scope[scope] == envvarservice.Scope.user):
            self.winUserEnvVarService.removeEnvVariable(name)
        else:
            self.winSystemEnvVarService.removeEnvVariable(name)
        self.refresh()
        
    def importEnvVars(self):
        newWindow = tk.Toplevel(self)
        guiimport.EnvironmentVariableImport(newWindow, self).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
        self.after(1, lambda: newWindow.focus_force())
        
    def about(self):
        newWindow = tk.Toplevel(self)
        guiabout.About(newWindow, self).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
        self.after(1, lambda: newWindow.focus_force())

def main():
    root = tk.Tk()
    root.wm_title(Locale.windy_title.value)
    appSize = (800, 600)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
 
    x = w / 2 - appSize[0] / 2
    y = h / 2 - appSize[1] / 2
    root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
    root.update_idletasks()  # Force geometry update

    Application(root)  # .pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
