import tkinter as tk
from tkinter import ttk

window=tk.Tk()

def fnc(num:str):
    new_value=strvar_lcd.get()+num
    strvar_lcd.set(new_value)

window.rowconfigure(0, weight=2)
window.rowconfigure([1,2,3,4,5], weight=1)
window.columnconfigure([0,1,2,3],weight=1)

strvar_lcd=tk.StringVar(window)
lbl_lcd=ttk.Label(window, background="black", foreground="white", textvariable=strvar_lcd, anchor="center")
lbl_lcd.grid(row=0, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

btn_0=tk.Button(window, text="0", bg="cyan", command=lambda *args:fnc("0"))
btn_0.grid(row=4, column=1, sticky="nswe", padx=10, pady=10)
btn_1=tk.Button(window, text="1", bg="cyan", command=lambda *args:fnc("1"))
btn_1.grid(row=3, column=0, sticky="nswe", padx=10, pady=10)
btn_2=tk.Button(window, text="2", bg="cyan", command=lambda *args:fnc("2"))
btn_2.grid(row=3, column=1, sticky="nswe", padx=10, pady=10)
btn_3=tk.Button(window, text="3", bg="cyan", command=lambda *args:fnc("3"))
btn_3.grid(row=3, column=2, sticky="nswe", padx=10, pady=10)
btn_4=tk.Button(window, text="4", bg="cyan", command=lambda *args:fnc("4"))
btn_4.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
btn_5=tk.Button(window, text="5", bg="cyan", command=lambda *args:fnc("5"))
btn_5.grid(row=2, column=1, sticky="nswe", padx=10, pady=10)
btn_6=tk.Button(window, text="6", bg="cyan", command=lambda *args:fnc("6"))
btn_6.grid(row=2, column=2, sticky="nswe", padx=10, pady=10)
btn_7=tk.Button(window, text="7", bg="cyan", command=lambda *args:fnc("7"))
btn_7.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
btn_8=tk.Button(window, text="8", bg="cyan", command=lambda *args:fnc("8"))
btn_8.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)
btn_9=tk.Button(window, text="9", bg="cyan", command=lambda *args:fnc("9"))
btn_9.grid(row=1, column=2, sticky="nswe", padx=10, pady=10)

btn_c=tk.Button(window, text="C", bg="red", command=lambda *args:fnc("?"))
btn_c.grid(row=4, column=0, sticky="nswe", padx=10, pady=10)
btn_dot=tk.Button(window, text=".", bg="grey", command=lambda *args:fnc("."))
btn_dot.grid(row=4, column=2, sticky="nswe", padx=10, pady=10)

btn_add=tk.Button(window, text="+", bg="orange", command=lambda *args:fnc("+"))
btn_add.grid(row=1, column=3, sticky="nswe", padx=10, pady=10)
btn_sub=tk.Button(window, text="-", bg="orange", command=lambda *args:fnc("-"))
btn_sub.grid(row=2, column=3, sticky="nswe", padx=10, pady=10)
btn_mul=tk.Button(window, text="*", bg="orange", command=lambda *args:fnc("*"))
btn_mul.grid(row=3, column=3, sticky="nswe", padx=10, pady=10)
btn_div=tk.Button(window, text="/", bg="orange", command=lambda *args:fnc("/"))
btn_div.grid(row=4, column=3, sticky="nswe", padx=10, pady=10)
btn_equal=tk.Button(window, text="=", bg="green", command=lambda *args:fnc("="))
btn_equal.grid(row=5, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

window.mainloop()
