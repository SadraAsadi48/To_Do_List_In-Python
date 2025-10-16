import tkinter as tk
from tkinter import messagebox
import sqlite3

# -------------------------------------------------------------------------------
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")
conn.commit()

# -------------------------------------------------------------------------------
def add_task():
    task_text = task_entry.get().strip()
    if task_text == "":
        messagebox.showwarning("هشدار", "لطفاً یک کار وارد کنید.")
        return

    cursor.execute("INSERT INTO tasks (text, status) VALUES (?, ?)", (task_text, "در حال انجام"))
    conn.commit()
    task_id = cursor.lastrowid

    create_task_widget(task_id, task_text, "در حال انجام")
    task_entry.delete(0, tk.END)

def update_status(task_id, new_status):
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()

def delete_task(task_id, frame):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    frame.destroy()

def create_task_widget(task_id, text, status):
    frame = tk.Frame(tasks_frame)
    frame.pack(fill="x", pady=2)

    var = tk.StringVar(value=status)

    # Radio Buttons
    tk.Radiobutton(frame, text="در حال انجام", variable=var, value="در حال انجام",
                   command=lambda: update_status(task_id, var.get())).pack(side="left")
    tk.Radiobutton(frame, text="انجام‌شده", variable=var, value="انجام‌شده",
                   command=lambda: update_status(task_id, var.get())).pack(side="left")

    # متن کار
    tk.Label(frame, text=text, anchor="w").pack(side="left", expand=True, fill="x", padx=5)

    # دکمه حذف
    tk.Button(frame, text="حذف", command=lambda: delete_task(task_id, frame)).pack(side="right")

def load_tasks():
    cursor.execute("SELECT id, text, status FROM tasks")
    for task_id, text, status in cursor.fetchall():
        create_task_widget(task_id, text, status)

# -------------------------------------------------------------------------------
root = tk.Tk()
root.title("برنامه‌ی لیست کارها")

task_entry = tk.Entry(root, width=40)
task_entry.grid(row=0, column=0, padx=10, pady=10)

add_button = tk.Button(root, text="افزودن کار", command=add_task)
add_button.grid(row=0, column=1)

tasks_frame = tk.Frame(root)
tasks_frame.grid(row=1, column=0, columnspan=2, pady=10)

load_tasks()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
