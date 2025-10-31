'''
[] draw UML
[T] create class for settings
[T] create class for QRcode
[T] create class for input frame
'''

import tkinter as tk
# from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
import qrcode
import json
from pathlib import Path

class Application(tk.Tk):
    def __init__(self, geometry="400x500"):
        super().__init__()
        self.setup(geometry)
        database_file=Path(__file__).parent/"lib"/"settings.json"   
        self.database=DataBase(database_file)
        database_defaults_file=Path(__file__).parent/"lib"/"settings_defaults.json"
        self.database_defaults=DataBase(database_defaults_file)
        self.layout()

    def setup(self, geometry):
        self.title("QRcode")
        self.geometry(geometry)

        icon_path=Path(__file__).parent/"lib"/"root_icon.png"
        self.iconphoto(True, tk.PhotoImage(file=icon_path))

        # self.resizable(width=False, height=False)

    def layout(self):
        self.rowconfigure([0], weight=0)
        self.rowconfigure([1], weight=4, uniform="a")
        self.rowconfigure([2], weight=1, uniform="a")
        self.columnconfigure([0], weight=1)

        # self.settings.create_frame().grid(row=0, column=0, sticky="ns", padx=10, pady=5)    # delete
        SettingsFrame(master=self, on_settings_callback=self.on_settings).grid(row=0, column=0, sticky="ns", padx=10, pady=5)
        
        self.qrcode=QRcode(master=self)
        self.qrcode.grid(row=1, column=0, sticky="nswe", padx=10, pady=5)

        self.input_widget=InputWidget(master=self, save_callback=self.on_save, create_qrcode_callback=self.qrcode.create_qrcode)
        self.input_widget.grid(row=2, column=0, sticky="nswe", padx=10, pady=5)

        self.qrcode.set_GetSettings(self.database.get)
        # self.settings.set_entry_change_callback(self.input_widget.on_text_entry_change)   # delete

    def on_save(self):
        filepath=filedialog.asksaveasfilename(initialfile=self.text_entry_strvar.get(), defaultextension=".png")
        if filepath:
            self.qrcode.qrcode_image.save(filepath)
            self.input_widget.save_button.configure(state="disabled")
        else:
            # user cancelled save operation
            pass    
    
    def on_settings(self):
        SettingsForm(self, self.database, self.database_defaults, self.input_widget.on_text_entry_change)

    def __dubug(self, *_):
        pass

class SettingsForm(tk.Toplevel):
    def __init__(self, master, database, database_defaults, on_text_entry_change_callback):
        self.database=database
        self.database_defaults=database_defaults
        self.on_text_entry_change=on_text_entry_change_callback
        super().__init__(master)
        config=self.database.read()
        self.configswidget=ConfigsWidget(self, config)
        self.configswidget.pack()
        tk.Button(self, text="save", command=self.on_save).pack()
        tk.Button(self, text="default", command=self.on_default).pack()
        tk.Button(self, text="cancel", command=self.on_cancel).pack()

    def on_save(self):
        config=self.configswidget.get_fields()
        self.database.write(config)
        self.on_text_entry_change()
        self.die()
    
    def on_default(self):
        config=self.database_defaults.read()
        self.configswidget.set_fields(config)

    def on_cancel(self):
        self.die()

    def die(self):
        self.destroy()

class SettingsFrame(tk.Frame):
    def __init__(self, master, on_settings_callback):
        self.master=master
        super().__init__(self.master)
        tk.Button(self, text="settings", command=on_settings_callback).pack(expand=True)

class QRcode(tk.Label):
    def __init__(self, master):
        self.master=master
        super().__init__(master, text="QRcode", anchor="center")
        self.bind("<Configure>", self.on_label_resize) # resize qrcode image when its label is resized, otherwise qrcode image doesnt change with qrcode label resize
    
    def set_GetSettings(self, get_settings_callback):
        self.get_settings=get_settings_callback

    def on_label_resize(self, *_):
        self.display_image()

    def display_image(self):
        if hasattr(self, "qrcode_image")==False or self.qrcode_image==None:
            self.configure(image="")
        else:
            self.resized_qrcode_image=self.qrcode_image.resize(self.get_image_size())
            photo=ImageTk.PhotoImage(self.resized_qrcode_image)
            self.configure(image=photo)
            self.photo=photo   # keep a refrence to image, otherwise no image is shown after image is garbaged(out of scope)

    def get_image_size(self, *_):
        # image is always square
        width=int(self.winfo_width())
        height=int(self.winfo_height())
        size=min(width, height)
        return (size, size)

    def generate_image(self, text):
        qr=qrcode.QRCode(version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(text)
        qr.make(fit=True)
        self.qrcode_image=qr.make_image(fill_color=self.get_settings("fill_color"), back_color=self.get_settings("back_color"))  

    def create_qrcode(self, text):
        if text=="":
            self.qrcode_image=None
            self.display_image()
        else:
            self.generate_image(text)
            self.display_image()

class InputWidget(tk.Frame):
    def __init__(self, master, save_callback, create_qrcode_callback):
        self.on_save=save_callback
        self.create_qrcode=create_qrcode_callback
        super().__init__(master)

        self.text_entry_strvar=tk.StringVar()
        self.text_entry_strvar.trace_add("write", self.on_text_entry_change)
        text_entry=tk.Entry(self, textvariable=self.text_entry_strvar, justify="center")
        text_entry.place(anchor="center", relx=0.5, rely=0.5, relwidth=0.5, relheight=0.4)
        text_entry.focus()

        self.save_button=tk.Button(self, text="SAVE", state="disabled", command=self.on_save)
        self.save_button.place(anchor="s", relx=0.5, rely=1, relwidth=0.25, relheight=0.2)

    def on_text_entry_change(self, *args):
        text=self.text_entry_strvar.get()
        if text=="":
            self.save_button.configure(state="disabled")
        else:
            self.save_button.configure(state="normal")
        
        self.create_qrcode(text)

class DataBase():
    def __init__(self, path):
        self.path=path

    def read(self):
        with open(self.path, "r") as file:
            config=json.load(file)
            return config

    def write(self, config):
        with open(self.path, "w") as file:
            json.dump(config, file)        
    
    def get(self, key):
        config=self.read()
        return config[key]

class ConfigWidget(tk.Frame):
    def __init__(self, master, label_text):
        super().__init__(master)

        self.rowconfigure([0], weight=1)
        self.columnconfigure([0], weight=1, uniform="a")
        self.columnconfigure([1], weight=1, uniform="a")

        tk.Label(self, text=label_text).grid(row=0, column=0, sticky="e")
        self.textvariable=tk.StringVar()
        tk.Entry(self, textvariable=self.textvariable).grid(row=0, column=1, sticky="w")

    def set(self, value):
        self.textvariable.set(value)

    def get(self):
        return self.textvariable.get()

class ConfigsWidget(tk.Frame):
    def __init__(self, master, config):
        self.configwidgets={}
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.add_fields(config.keys())
        self.set_fields(config)

    def add_fields(self, fields):
	    # it gets iterator of strings that are used as lablel_text for ConfigWidget 
        indices=list(range(1, len(fields)+1))
        self.rowconfigure(indices, weight=1, uniform="a")       
        for index, field in enumerate(fields):
            self.configwidgets[field]=ConfigWidget(self, field)
            self.configwidgets[field].grid(row=index, column=0, sticky="nswe")

    def get_fields(self):
        config={}
        for key, value in self.configwidgets.items():
            config[key]=value.get()
        return config

    def set_fields(self, config):
        for key in config:
            self.configwidgets[key].set(config[key])

if __name__=="__main__":
    app=Application()
    app.mainloop()

