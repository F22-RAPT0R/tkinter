# clear all button

# DONE# EntryRadioCheck._on_clear()
# DONE  # EntryRadioCheck is added on demand, like excel argument dialogue box 
# DONE  # convert to .exe

import tkinter as tk
from tkinter import ttk

class EntryRadioCheck(tk.Frame):
    def __init__(self, master, textvariable, num, id, *args):
        self.master=master
        self.num=num
        self.textvariable=textvariable
        self.id=id
        self._seperator=","

        super().__init__(master)
        
        self._layout()

    def _layout(self):
        self.rowconfigure([0], weight=1)
        self.columnconfigure([0,1,2], weight=1)

        self.entry_textvariable=tk.StringVar(self)
        self.entry_textvariable.trace_add("write", self._set_textvariable)

        self.radiocheck_textvariable=tk.StringVar(self)
        self.radiocheck_textvariable.trace_add("write", self._set_textvariable)

        tk.Button(self, text="clear", command=self._on_clear, bg="red").grid(row=0, column=0, sticky="", padx=2)

        entry=tk.Entry(self, textvariable=self.entry_textvariable)
        entry.grid(row=0, column=1, sticky="we", padx=2)
        entry.bind("<FocusIn>", lambda event:self.master.on_entry_focus(self.id))

        RadioCheck(self, self.radiocheck_textvariable, self.num, self._seperator).grid(row=0, column=2, sticky="nswe", padx=2)              

    def _set_textvariable(self, *args):
        if self.entry_textvariable.get()=="":
            self.textvariable.set("")
        else:    
            deck_str=f"deck::VOCAB::{self.entry_textvariable.get()}"
            flags_str=""
            for flag in self.radiocheck_textvariable.get().split(self._seperator):
                if flag!="":
                    flags_str+=f" flag:{int(flag)+1}"

            self.textvariable.set(f"({deck_str}{flags_str})")

    def _on_clear(self):
        self.entry_textvariable.set("")
        self.radiocheck_textvariable.set("")

class RadioCheck(tk.Frame):
    def __init__(self, master, textvariable, num, seperator, *args, **kwargs):
        # num: number of tk.ChckButtons
        
        self.num=num  
        self.variables=[]
        self.last_selected=0  # to be used with shift + click
        self.textvariable=textvariable  # textvariable:tk.StringVar(), self._seperator seperated string of checked tk.CheckButton indexes, zero based, e.g. (self._seperator is space) "0 5 6" 
        self._seperator=seperator
       
        super().__init__(master, *args, **kwargs)

        self.textvariable.trace_add("write", self._on_textvariable_change)
        self._layout() 
        self._on_textvariable_change()  # to handle initial value of self.textvariable
    
    def _layout(self):
        for _ in range(self.num):
            boolvar=tk.BooleanVar(self, value=False)
            self.variables.append(boolvar)

            checkbutton=ttk.Checkbutton(self, text=_+1, onvalue=True, offvalue=False, variable=boolvar)
            checkbutton.bind("<Button-1>", lambda event, id=_:self._on_click(id))
            checkbutton.bind("<Shift-Button-1>", lambda event, id=_:self._on_shift(id))
            checkbutton.bind("<Control-Button-1>", lambda event, id=_:self._on_ctrl(id))
            checkbutton.pack(expand=True, side="left", fill="both")

    def _on_click(self, id):
        self._set_selection([id])
        self.last_selected=id
        return "break"

    def _on_shift(self, id):
        minimum=min(self.last_selected, id)
        maximum=max(self.last_selected, id)
        self._set_selection([_ for _ in range(minimum, maximum+1)])
        self.last_selected=id
        return "break"

    def _on_ctrl(self, id):
        selection=self._get_selection()
        if id in selection:
            selection.remove(id)
        else:
            selection.append(id)    

        self._set_selection(selection)
        self.last_selected=id
        return "break"      
    
    def _on_textvariable_change(self, *args):
        selection=self._get_selection()

        for index,variable in enumerate(self.variables, start=0):
            if index in selection:
                variable.set(True)
            else:
                variable.set(False)    

    def _set_selection(self, selection):
        selection_str=""
        for id in sorted(selection):
            selection_str+=f"{id}"
        selection_str=self._seperator.join(selection_str)    
        self.textvariable.set(selection_str)

    def _get_selection(self):
        if self.textvariable.get()=="":
            selection=[]
        else:
            selection=[int(alfa) for alfa in self.textvariable.get().split(self._seperator)]

        return selection
        
class App(tk.Tk):
    def __init__(self, num, title="ANKI", *args, **kwargs):
        # num: initial EntryRadioCheck's number
        # title: window title

        self._last_row=0
        self.entryradiocheck_variables=[]   # to be used with _add_EntryRadioCheck

        super().__init__(*args, **kwargs)
        self.num=num
        self.title(title)
        # self.resizable(False, False)
        self._layout()
        self.mainloop()    

    def _layout(self):
        self.rowconfigure([0], weight=1, uniform="1")
        self.columnconfigure([0], weight=1)

        button_frame=tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=5)
        tk.Button(button_frame, text="filter", command=self._on_filter, bg="green").place(relx=0.5, rely=0.5, relwidth=0.5, relheight=1, anchor="center")  

        for row in range(1, self.num+1):
            self._add_EntryRadioCheck()

    def _on_filter(self):
        alfa=[]
        for entryradiocheck_variable in self.entryradiocheck_variables:
            if entryradiocheck_variable.get()!="":
                alfa.append(entryradiocheck_variable.get())

        filter_str=" OR ".join(alfa)
        self.clipboard_append(filter_str)
        print(filter_str)

    def _add_EntryRadioCheck(self):
            self._last_row+=1
            entryradiocheck_variable=tk.StringVar(self)
            self.entryradiocheck_variables.append(entryradiocheck_variable)
            self.rowconfigure(self._last_row, weight=1, uniform="1")            
            EntryRadioCheck(master=self, textvariable=entryradiocheck_variable, num=9, id=self._last_row).grid(row=self._last_row, column=0, sticky="nswe", padx=10, pady=5)

    def on_entry_focus(self, entry_id):
        if entry_id==self._last_row:
            self._add_EntryRadioCheck()

    def _debug1(self, message=""):
        print(message, [variable.get() for variable in self.variables])

App(1)
