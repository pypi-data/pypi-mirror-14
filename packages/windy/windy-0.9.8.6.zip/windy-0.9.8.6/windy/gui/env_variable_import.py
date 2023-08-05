# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''
import tkinter as tk
import tkinter.constants as tc
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from windy.gui.locale import Locale


class EnvironmentVariableImport(ttk.Frame):
    def __init__(self, root, parent):
        ttk.Frame.__init__(self, root)
        self.root = root
        self.parent = parent
        
        root.wm_title(Locale.importThreeDots.value)
        self.createGui()
        self.refresh()
        
        appSize = (600, 400)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        x = w / 2 - appSize[0] / 2
        y = h / 2 - appSize[1] / 2
        self.root.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
        self.root.update_idletasks()  # Force geometry update


    def createGui(self):
        separatorLabel = ttk.Label(self.root, text=Locale.content_import.value, anchor=tc.W)
        separatorLabel.grid(column=0, row=0, sticky=tc.W, columnspan=6)
        separatorLabel.pack(fill=tc.X)
        
        self.txt = tk.scrolledtext.ScrolledText(self, undo=True)
        self.txt.grid(column=0, row=1, sticky=tc.NSEW, columnspan=6)
        
        self.scopeModel = tk.IntVar(0)
        self.scopeCheckbox = ttk.Checkbutton(self, text=Locale.system.value, variable=self.scopeModel,
                 onvalue=1, offvalue=0)
        self.scopeCheckbox.grid(column=0, row=2, sticky=tc.W)

        button = ttk.Button(self, text=Locale.from_file.value, command=self.openFile)
        button.grid(column=2, row=3, sticky=tc.E)

        button = ttk.Button(self, text=Locale.clear_content.value, command=self.clearContent)
        button.grid(column=3, row=3, sticky=tc.E)

        button = ttk.Button(self, text=Locale.save.value, command=self.save)
        button.grid(column=4, row=3, sticky=tc.E)

        button = ttk.Button(self, text=Locale.close.value, command=self.quit)
        button.grid(column=5, row=3, sticky=tc.E)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(2, weight=1)
    
    def refresh(self, content=""):
        self.txt.delete("0.0", tc.END)
        self.txt.insert("0.0", content)
        
        if self.parent.restricted:
            self.scopeCheckbox.configure(state=tc.DISABLED)

    def clearContent(self):
        # self.txt.delete("0.0", "end")
        self.refresh()

    def openFile(self):
        filename = fd.askopenfilename(parent=self)
        if filename:
            with open(filename, "r") as f:
                content = f.read()
            self.refresh(content);    
    
    def save(self):
        content = self.txt.get(1.0, tc.END).strip()
        
        valid = len(content) > 0
        if not valid:
            tk.messagebox.showinfo(Locale.empty_content_title.value, Locale.empty_content_desc.value)
            return
        
        lines = [s.strip() for s in content.splitlines()]
        for line in lines:
            try :
                name, value = line.split("=")
            except ValueError:
                tk.messagebox.showinfo(Locale.bad_format_title.value, Locale.bad_format_desc.value.format(line=line))
                continue
            
            name = name.strip()
            value = value.strip()
            if name and value:
                if self.scopeModel.get() == 0:
                    self.parent.winUserEnvVarService.addEnvVariable(name, value)
                else:
                    try:
                        self.parent.winSystemUserEnvVarService.addEnvVariable(name, value)
                    except WindowsError:
                        tk.messagebox.showwarning(Locale.import_file_title.value, Locale.import_file_desc.value)
                        break
            else:
                tk.messagebox.showinfo(Locale.bad_format_title.value, Locale.bad_format_desc.value.format(line=line))   
        self.parent.refresh()
                
    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    EnvironmentVariableImport(root, None).pack(side=tc.TOP, fill=tc.BOTH, expand=True)
    root.mainloop()
