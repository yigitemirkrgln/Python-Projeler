import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ===================== DATABASE =====================

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            completed INTEGER,
            created_at TEXT
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            count INTEGER
        )
        """)
        self.conn.commit()

    # ---------- TASKS ----------
    def add_task(self, title):
        self.cur.execute(
            "INSERT INTO tasks VALUES (NULL, ?, 0, ?)",
            (title, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        self.conn.commit()

    def get_tasks(self):
        self.cur.execute("SELECT * FROM tasks")
        return self.cur.fetchall()

    def toggle_task(self, task_id, state):
        self.cur.execute(
            "UPDATE tasks SET completed=? WHERE id=?",
            (state, task_id)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        self.cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    # ---------- HABITS ----------
    def add_habit(self, name):
        self.cur.execute(
            "INSERT INTO habits VALUES (NULL, ?, 0)", (name,)
        )
        self.conn.commit()

    def increment_habit(self, habit_id):
        self.cur.execute(
            "UPDATE habits SET count = count + 1 WHERE id=?",
            (habit_id,)
        )
        self.conn.commit()

    def get_habits(self):
        self.cur.execute("SELECT * FROM habits")
        return self.cur.fetchall()

# ===================== THEME =====================

class Theme:
    LIGHT = {
        "bg": "#ffffff",
        "fg": "#000000"
    }
    DARK = {
        "bg": "#2b2b2b",
        "fg": "#ffffff"
    }

# ===================== MAIN APP =====================

class TaskManagerApp:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("Advanced Task Manager")
        self.root.geometry("900x600")

        self.theme = Theme.LIGHT
        self.build_ui()

    def build_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.task_tab = tk.Frame(self.notebook)
        self.habit_tab = tk.Frame(self.notebook)
        self.stats_tab = tk.Frame(self.notebook)
        self.settings_tab = tk.Frame(self.notebook)

        self.notebook.add(self.task_tab, text="Görevler")
        self.notebook.add(self.habit_tab, text="Alışkanlıklar")
        self.notebook.add(self.stats_tab, text="İstatistik")
        self.notebook.add(self.settings_tab, text="Ayarlar")

        self.build_tasks()
        self.build_habits()
        self.build_stats()
        self.build_settings()

    # ================= TASKS =================

    def build_tasks(self):
        tk.Label(self.task_tab, text="Yeni Görev").pack(pady=5)

        self.task_entry = tk.Entry(self.task_tab, width=40)
        self.task_entry.pack()

        tk.Button(
            self.task_tab, text="Ekle", command=self.add_task
        ).pack(pady=5)

        self.task_list = tk.Listbox(self.task_tab, width=80)
        self.task_list.pack(pady=10)

        tk.Button(
            self.task_tab, text="Tamamlandı / Geri Al",
            command=self.toggle_task
        ).pack(pady=2)

        tk.Button(
            self.task_tab, text="Sil", command=self.delete_task
        ).pack(pady=2)

        self.load_tasks()

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        self.tasks_cache = self.db.get_tasks()

        for task in self.tasks_cache:
            status = "✔" if task[2] else "✗"
            self.task_list.insert(
                tk.END, f"[{status}] {task[1]} ({task[3]})"
            )

    def add_task(self):
        title = self.task_entry.get()
        if not title:
            messagebox.showwarning("Hata", "Boş görev olmaz")
            return
        self.db.add_task(title)
        self.task_entry.delete(0, tk.END)
        self.load_tasks()

    def toggle_task(self):
        index = self.task_list.curselection()
        if not index:
            return
        task = self.tasks_cache[index[0]]
        self.db.toggle_task(task[0], 0 if task[2] else 1)
        self.load_tasks()

    def delete_task(self):
        index = self.task_list.curselection()
        if not index:
            return
        task = self.tasks_cache[index[0]]
        self.db.delete_task(task[0])
        self.load_tasks()

    # ================= HABITS =================

    def build_habits(self):
        self.habit_entry = tk.Entry(self.habit_tab, width=30)
        self.habit_entry.pack(pady=5)

        tk.Button(
            self.habit_tab, text="Alışkanlık Ekle",
            command=self.add_habit
        ).pack()

        self.habit_list = tk.Listbox(self.habit_tab, width=60)
        self.habit_list.pack(pady=10)

        tk.Button(
            self.habit_tab, text="+1",
            command=self.increment_habit
        ).pack()

        self.load_habits()

    def load_habits(self):
        self.habit_list.delete(0, tk.END)
        self.habits_cache = self.db.get_habits()
        for h in self.habits_cache:
            self.habit_list.insert(
                tk.END, f"{h[1]} → {h[2]} gün"
            )

    def add_habit(self):
        name = self.habit_entry.get()
        if not name:
            return
        self.db.add_habit(name)
        self.habit_entry.delete(0, tk.END)
        self.load_habits()

    def increment_habit(self):
        index = self.habit_list.curselection()
        if not index:
            return
        habit = self.habits_cache[index[0]]
        self.db.increment_habit(habit[0])
        self.load_habits()

    # ================= STATS =================

    def build_stats(self):
        self.stats_label = tk.Label(
            self.stats_tab, text="", font=("Arial", 14)
        )
        self.stats_label.pack(pady=20)
        self.update_stats()

    def update_stats(self):
        tasks = self.db.get_tasks()
        completed = len([t for t in tasks if t[2]])
        total = len(tasks)
        self.stats_label.config(
            text=f"Toplam Görev: {total}\nTamamlanan: {completed}"
        )

    # ================= SETTINGS =================

    def build_settings(self):
        tk.Button(
            self.settings_tab, text="Dark Mode",
            command=self.set_dark
        ).pack(pady=10)

        tk.Button(
            self.settings_tab, text="Light Mode",
            command=self.set_light
        ).pack(pady=10)

    def set_dark(self):
        self.theme = Theme.DARK
        self.apply_theme()

    def set_light(self):
        self.theme = Theme.LIGHT
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])

    def run(self):
        self.root.mainloop()

# ===================== RUN =====================

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
