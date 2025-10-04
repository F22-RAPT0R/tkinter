import tkinter as tk
from tkinter import ttk
from pathlib import Path
from csv import writer
from datetime import datetime

class App(tk.Tk):
    def __init__(self, path="ABQ.csv", *args, **kwargs):
        self.path=path
        super().__init__(*args, **kwargs)
        self.widgets={}
        # self.debug()
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight()-31)     # 31 is title bar height
        self.layout()
        self.create_save_file()
        self.mainloop()

    def layout(self):
        self.rowconfigure([0], weight=1, uniform="a")
        self.rowconfigure([1,2,3,4], weight=3, uniform="a")
        self.rowconfigure([5], weight=1, uniform="a")
        self.columnconfigure([0], weight=1)

        frame_heading=tk.Frame(self)
        label_heading=tk.Label(frame_heading, text="ABQ DATA ENTRY APPLICATION", bg="green")
        self.widgets["record_information"]=Record_information(self, "Recored Information", ["Date", "Time", "Technician", "Lab", "Plot", "Seed Sample"])
        self.widgets["environmental_data"]=Enviromental_data(self, "Enviromental Data", ["Humidity", "light", "Temperature", ""])
        self.widgets["plant_data"]=Plant_data(self, "Plant Data", ["Plants", "Blossoms", "Fruit", "Min Height", "Max Height", "Median Height"])       
        self.widgets["notes"]=Notes(self, "Notes")
        self.widgets["buttons_and_status_text"]=Buttons_and_status_text(self)

        frame_heading.grid(row=0, column=0, sticky="nswe", padx=10, pady=0)
        label_heading.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
        self.widgets["record_information"].grid(row=1, column=0, sticky="nswe", padx=10, pady=5)
        self.widgets["environmental_data"].grid(row=2, column=0, sticky="nswe", padx=10, pady=5)
        self.widgets["plant_data"].grid(row=3, column=0, sticky="nswe", padx=10, pady=5)
        self.widgets["notes"].grid(row=4, column=0, sticky="nswe", padx=10, pady=5)
        self.widgets["buttons_and_status_text"].grid(row=5, column=0, sticky="nswe", padx=0, pady=0)

    def save(self):
        save_time=datetime.now()
        save_data=[save_time]
        for widget_name, widget in self.widgets.items():
            if hasattr(widget, "variables"):
                print(widget_name)
                for key, value in widget.variables.items():
                    print(f"\t{key}: {value.get()}")
                    save_data.append(value.get())            

        print("notes:")
        print(self.widgets["notes"].text_notes.get("1.0", "end - 1 chars"))
        save_data.append(self.widgets["notes"].text_notes.get("1.0", "end - 1 chars"))

        with open(self.path, "a", newline="") as file:
            csv_writer=writer(file)
            csv_writer.writerow(save_data)

    def reset(self):
        for widget_name, widget in self.widgets.items():
            if hasattr(widget, "variables"):
                print(widget_name)
                for key, value in widget.variables.items():
                    if isinstance(value, tk.StringVar):
                        value.set("")
                    elif isinstance(value, tk.IntVar): 
                        value.set(0)
                    elif isinstance(value, tk.DoubleVar): 
                        value.set(0.0)
                    elif isinstance(value, tk.BooleanVar): 
                        value.set(False)                                            
                    
        self.widgets["notes"].text_notes.delete("1.0", "end")

    def create_save_file(self):
        file=Path(self.path)
        if not Path.exists(file):
            header=["save_time"]
            for name, widget in self.widgets.items():
                if hasattr(widget, "variables"):
                    for key, value in widget.variables.items():
                        header.append(key)      

            header.append("notes")

            with open(self.path, "w", newline="") as file:
                csv_writer=writer(file)
                csv_writer.writerow(header)

    def debug(self):
        # print(self.winfo_screenwidth(), self.winfo_screenheight())
        print(self.winfo_rooty(), self.winfo_y())

class Labelframe_me(tk.LabelFrame):
    def __init__(self, master, text, texts):
        super().__init__(master, text=text)
        self.rowconfigure([0,1], weight=1, uniform="a")
        self.columnconfigure([0,1,2], weight=1, uniform="b")

        self.widgets=[]
        for i in range(2):
            for j in range(3):
                index=3*i+j
                if index<=len(texts)-1:
                    label_text=texts[index]
                    widget=tk.LabelFrame(self, text=label_text, bd=0)
                    widget.grid(row=i, column=j, sticky="nswe", padx=5, pady=3)
                    self.widgets.append(widget)

# record information
class Record_information(Labelframe_me):
    def __init__(self, master, text, texts):
        super().__init__(master, text, texts)
        self.variables={"date":tk.StringVar(), "time":tk.StringVar(), "technician":tk.StringVar(), "lab":tk.StringVar(), "plot":tk.StringVar(), "seed_sample":tk.StringVar()}

        entry_date=tk.Entry(self.widgets[0], textvariable=self.variables["date"])
        entry_technician=tk.Entry(self.widgets[2], textvariable=self.variables["technician"])
        entry_seed_sample=tk.Entry(self.widgets[5], textvariable=self.variables["seed_sample"])

        radiobutton_lab1=tk.Radiobutton(self.widgets[3], text="A", variable=self.variables["lab"], value="A")
        radiobutton_lab2=tk.Radiobutton(self.widgets[3], text="B", variable=self.variables["lab"], value="B")
        radiobutton_lab3=tk.Radiobutton(self.widgets[3], text="C", variable=self.variables["lab"], value="C")

        combobox_time=ttk.Combobox(self.widgets[1], textvariable=self.variables["time"])
        combobox_plot=ttk.Combobox(self.widgets[4], textvariable=self.variables["plot"])

        entry_date.pack(expand=True, fill="both")
        entry_technician.pack(expand=True, fill="both")
        entry_seed_sample.pack(expand=True, fill="both")

        radiobutton_lab1.pack(side="left", expand=True)
        radiobutton_lab2.pack(side="left", expand=True)
        radiobutton_lab3.pack(side="left", expand=True)

        combobox_time.pack(expand=True, fill="both")
        combobox_plot.pack(expand=True, fill="both")

# environmental data
class Enviromental_data(Labelframe_me):
    def __init__(self, master, text, texts):
        super().__init__(master, text, texts)
        self.variables={"humidity":tk.StringVar(), "light":tk.StringVar(), "temperature":tk.StringVar(), "equipment_fault":tk.BooleanVar()}
        
        spinbox_humidity=tk.Spinbox(self.widgets[0], textvariable=self.variables["humidity"])
        spinbox_light=tk.Spinbox(self.widgets[1], textvariable=self.variables["light"])
        spinbox_temperature=tk.Spinbox(self.widgets[2], textvariable=self.variables["temperature"])

        checkbutton1=tk.Checkbutton(self.widgets[3], text="Equipment Fault", variable=self.variables["equipment_fault"])

        spinbox_humidity.pack(expand=True, fill="both")
        spinbox_light.pack(expand=True, fill="both")
        spinbox_temperature.pack(expand=True, fill="both")
        checkbutton1.pack(expand=True, fill="both", anchor="w")
        # checkbutton1.place(x=0, y=0, relwidth=1, relheight=1)

# plant data
class Plant_data(Labelframe_me):
    def __init__(self, master, text, texts):
        super().__init__(master, text, texts)
        self.variables={"plants":tk.StringVar(), "blossoms":tk.StringVar(), "fruit":tk.StringVar(), "min_height":tk.DoubleVar(), "max_height":tk.DoubleVar(), "median_height":tk.DoubleVar()}

        spinbox_plants=tk.Spinbox(self.widgets[0], textvariable=self.variables["plants"])
        spinbox_blossoms=tk.Spinbox(self.widgets[1], textvariable=self.variables["blossoms"])
        spinbox_fruit=tk.Spinbox(self.widgets[2], textvariable=self.variables["fruit"])
        spinbox_min_height=tk.Spinbox(self.widgets[3], textvariable=self.variables["min_height"])
        spinbox_max_height=tk.Spinbox(self.widgets[4], textvariable=self.variables["max_height"])
        spinbox_median_height=tk.Spinbox(self.widgets[5], textvariable=self.variables["median_height"])

        spinbox_plants.pack(expand=True, fill="both")
        spinbox_blossoms.pack(expand=True, fill="both")
        spinbox_fruit.pack(expand=True, fill="both")        
        spinbox_min_height.pack(expand=True, fill="both")        
        spinbox_max_height.pack(expand=True, fill="both")        
        spinbox_median_height.pack(expand=True, fill="both")  

# notes
class Notes(tk.LabelFrame):
    def __init__(self, master, text):
        super().__init__(master, text=text,bd=0)

        self.text_notes=tk.Text(self)
        self.text_notes.pack(expand=True, fill="both")

# buttons and status
class Buttons_and_status_text(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master=master
        self.rowconfigure([0,1], weight=1, uniform="c")
        self.columnconfigure([0,1,2], weight=1, uniform="d")

        button_reset=tk.Button(self, text="Reset", command=self.reset)
        button_save=tk.Button(self, text="Save", command=self.save)
        label1=tk.Label(self, text="Status Text", anchor="w")

        button_reset.grid(row=0, column=1, sticky="nswe", padx=0, pady=1)
        button_save.grid(row=0, column=2, sticky="nswe", padx=10, pady=1)
        label1.grid(row=1, column=0, sticky="nswe", columnspan=3, padx=0, pady=0)

    def save(self):
        self.master.save()

    def reset(self):
        self.master.reset()

App()
