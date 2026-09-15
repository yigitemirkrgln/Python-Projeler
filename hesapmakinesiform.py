import tkinter as tk
from tkinter import ttk, messagebox
import math, json, os, requests
import sympy as sp
import matplotlib.pyplot as plt

# ================= FILES =================
CONFIG_FILE = "config.json"
AI_FILE = "ai_memory.json"

def load(file, default):
    if os.path.exists(file):
        with open(file,"r",encoding="utf-8") as f:
            return json.load(f)
    return default

config = load(CONFIG_FILE, {"theme":"LIGHT"})
ai = load(AI_FILE, {"usage":{}})

# ================= AI =================
def remember(key):
    ai["usage"][key] = ai["usage"].get(key,0)+1
    with open(AI_FILE,"w") as f:
        json.dump(ai,f,indent=2)

def ai_suggest():
    if not ai["usage"]:
        return "—"
    return max(ai["usage"], key=ai["usage"].get)

# ================= CORE =================
def calculate():
    try:
        expr = entry.get()
        x = sp.symbols("x")
        result = sp.sympify(expr)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        history.insert(tk.END, f"{expr} = {result}")
        remember("calculate")
        update_ai_label()
    except:
        messagebox.showerror("Error", "Invalid Expression")

def press(val):
    entry.insert(tk.END, val)

def clear():
    entry.delete(0, tk.END)

# ================= SCIENTIFIC =================
def sci(func):
    try:
        x = float(entry.get())
        funcs = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "fact": lambda n: math.factorial(int(n))
        }
        res = funcs[func](x)
        entry.delete(0, tk.END)
        entry.insert(0, str(res))
        remember(func)
        update_ai_label()
    except:
        messagebox.showerror("Math Error", "Invalid Input")

# ================= PROGRAMMER =================
def convert(base):
    try:
        n = int(entry.get())
        if base == "bin":
            entry.delete(0, tk.END)
            entry.insert(0, bin(n))
        elif base == "hex":
            entry.delete(0, tk.END)
            entry.insert(0, hex(n))
        elif base == "dec":
            entry.delete(0, tk.END)
            entry.insert(0, int(n, 0))
        remember(base)
        update_ai_label()
    except:
        messagebox.showerror("Error", "Conversion Error")

# ================= GRAPH =================
def plot_graph():
    try:
        expr = entry.get()
        x = sp.symbols("x")
        f = sp.lambdify(x, sp.sympify(expr), "math")
        xs = [i/10 for i in range(-100,100)]
        ys = [f(i) for i in xs]
        plt.plot(xs, ys)
        plt.grid()
        plt.title(expr)
        plt.show()
        remember("plot")
        update_ai_label()
    except:
        messagebox.showerror("Plot Error", "Invalid Function")

# ================= FINANCE =================
def usd_try():
    try:
        r = requests.get("https://api.exchangerate.host/latest?base=USD").json()
        rate = r["rates"]["TRY"]
        messagebox.showinfo("USD → TRY", f"1 USD = {rate:.2f} TRY")
        remember("finance")
        update_ai_label()
    except:
        messagebox.showerror("API Error", "Internet Error")

# ================= THEME =================
def toggle_theme():
    global theme
    theme = "DARK" if theme == "LIGHT" else "LIGHT"
    bg = "#1e1e1e" if theme=="DARK" else "#f0f0f0"
    fg = "white" if theme=="DARK" else "black"
    root.configure(bg=bg)
    for w in root.winfo_children():
        try:
            w.configure(bg=bg, fg=fg)
        except:
            pass
    config["theme"] = theme
    with open(CONFIG_FILE,"w") as f:
        json.dump(config,f,indent=2)

# ================= GUI =================
theme = config["theme"]
root = tk.Tk()
root.title("ULTIMATE AI CALCULATOR 👑")
root.geometry("620x720")

entry = tk.Entry(root, font=("Consolas", 22), justify="right")
entry.pack(fill="x", padx=10, pady=10)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# -------- TAB: Calculator --------
tab_calc = tk.Frame(notebook)
notebook.add(tab_calc, text="Calculator")

buttons = [
    "7","8","9","/","sin",
    "4","5","6","*","cos",
    "1","2","3","-","tan",
    "0",".","=","+","√"
]

def handle(b):
    if b == "=":
        calculate()
    elif b == "√":
        press("sqrt(")
    elif b in ["sin","cos","tan"]:
        press(f"{b}(")
    else:
        press(b)

r=c=0
for b in buttons:
    tk.Button(tab_calc, text=b, width=6, height=2,
              command=lambda x=b: handle(x))\
        .grid(row=r, column=c, padx=2, pady=2)
    c+=1
    if c>4:
        c=0; r+=1

# -------- TAB: Scientific --------
tab_sci = tk.Frame(notebook)
notebook.add(tab_sci, text="Scientific")

for i,f in enumerate(["sqrt","log","ln","fact","abs"]):
    tk.Button(tab_sci, text=f, command=lambda x=f: sci(x))\
        .grid(row=0, column=i, padx=5, pady=10)

# -------- TAB: Programmer --------
tab_prog = tk.Frame(notebook)
notebook.add(tab_prog, text="Programmer")

tk.Button(tab_prog, text="BIN", command=lambda:convert("bin")).pack(pady=5)
tk.Button(tab_prog, text="HEX", command=lambda:convert("hex")).pack(pady=5)
tk.Button(tab_prog, text="DEC", command=lambda:convert("dec")).pack(pady=5)

# -------- TAB: Graph --------
tab_graph = tk.Frame(notebook)
notebook.add(tab_graph, text="Graph")
tk.Button(tab_graph, text="Plot f(x)", command=plot_graph).pack(pady=30)

# -------- TAB: Finance --------
tab_fin = tk.Frame(notebook)
notebook.add(tab_fin, text="Finance")
tk.Button(tab_fin, text="USD → TRY", command=usd_try).pack(pady=30)

# -------- HISTORY --------
history = tk.Listbox(root, height=6)
history.pack(fill="x", padx=10, pady=5)

# -------- BOTTOM --------
bottom = tk.Frame(root)
bottom.pack(fill="x", pady=5)

def update_ai_label():
    ai_label.config(text=f"AI Suggestion: {ai_suggest()}")

tk.Button(bottom, text="Tema", command=toggle_theme).pack(side="left", padx=5)
tk.Button(bottom, text="Temizle", command=clear).pack(side="left", padx=5)

ai_label = tk.Label(bottom, text="AI Suggestion: —")
ai_label.pack(side="left", padx=10)

tk.Label(bottom, text="Made by Sonul Paşa").pack(side="right", padx=10)

toggle_theme()
root.mainloop()
