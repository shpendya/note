import customtkinter as ctk
from tkinter import simpledialog, filedialog 
import json
import os

# тема
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ctk.ThemeManager.theme["CTkButton"]["corner_radius"] = 12
ctk.ThemeManager.theme["CTkButton"]["fg_color"] = "#FF5722" 
ctk.ThemeManager.theme["CTkButton"]["hover_color"] = "#E64A19"
ctk.ThemeManager.theme["CTkEntry"]["corner_radius"] = 10

# Путь к файлу
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

tasks_data = [] 
task_widgets = [] 

# сохранение
def save_tasks():
    # автосохранение скрытое
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)

def load_tasks():
    global tasks_data
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)

# экспорт
def export_tasks():
    # Открываем окно "Сохранить как"
    file_path = filedialog.asksaveasfilename(
        title="Сохранить задачи как...",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
        initialfile="my_tasks.json"
    )
    
    
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)
        print(f"Сохранено в {file_path}") # проверка

context_menu = ctk.CTkToplevel()
context_menu.withdraw()
context_menu.overrideredirect(True)
context_menu.attributes("-topmost", True)
context_menu.configure(fg_color=("#e0e0e0", "#2b2b2b"))

def update_task_list():
    for widget in task_widgets:
        widget.destroy()
    task_widgets.clear()

    for index, task in enumerate(tasks_data):
        frame = ctk.CTkFrame(task_frame, fg_color="transparent", corner_radius=10)
        frame.pack(fill="x", pady=4, padx=10) 
        
        prefix = "📌 " if task["pinned"] else "• "
        text_color = "yellow" if task["pinned"] else "white"
        
        label = ctk.CTkLabel(frame, text=f"{prefix}{task['text']}", font=("Segoe UI", 14), text_color=text_color, anchor="w")
        label.pack(side="left", fill="x", expand=True, padx=10, pady=8)

        def on_enter(e, f=frame):
            f.configure(fg_color=("gray80", "gray25")) 
            
        def on_leave(e, f=frame):
            f.configure(fg_color="transparent") 

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Button-3>", lambda event, i=index: show_context_menu(event, i))
        
        task_widgets.append(frame)

def show_context_menu(event, index):
    for widget in context_menu.winfo_children():
        widget.destroy()

    btn_edit = ctk.CTkButton(context_menu, text="✏️ Изменить", command=lambda: [edit_task(index), context_menu.withdraw()], 
                             fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), anchor="w", width=120)
    btn_edit.pack(fill="x", padx=4, pady=2)

    btn_pin = ctk.CTkButton(context_menu, text="📌 Закрепить", command=lambda: [pin_task(index), context_menu.withdraw()], 
                            fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), anchor="w", width=120)
    btn_pin.pack(fill="x", padx=4, pady=2)

    btn_delete = ctk.CTkButton(context_menu, text="❌ Удалить", command=lambda: [delete_task(index), context_menu.withdraw()], 
                               fg_color="transparent", text_color=("red", "red"), hover_color=("gray70", "gray30"), anchor="w", width=120)
    btn_delete.pack(fill="x", padx=4, pady=2)

    context_menu.geometry(f"+{event.x_root}+{event.y_root}")
    context_menu.deiconify()

def add_task():
    task_text = entry.get()
    if task_text != "":
        tasks_data.append({"text": task_text, "pinned": False})
        entry.delete(0, "end")
        save_tasks()
        update_task_list()

def delete_task(index):
    del tasks_data[index]
    save_tasks()
    update_task_list()

def edit_task(index):
    old_text = tasks_data[index]["text"]
    new_text = simpledialog.askstring("Редактирование", "Изменить задачу:", initialvalue=old_text)
    if new_text:
        tasks_data[index]["text"] = new_text
        save_tasks()
        update_task_list()

def pin_task(index):
    tasks_data[index]["pinned"] = not tasks_data[index]["pinned"]
    tasks_data.sort(key=lambda x: x["pinned"], reverse=True)
    save_tasks()
    update_task_list()

def hide_menu(event):
    context_menu.withdraw()

app = ctk.CTk()
app.title("To-Do")
app.geometry("420x600") # Чуть увеличили высоту, чтобы влезла новая кнопка
app.resizable(False, False) 
app.bind("<Button-1>", hide_menu)

title = ctk.CTkLabel(app, text="Мои задачи", font=("Segoe UI", 24, "bold"))
title.pack(pady=(20, 10))

entry = ctk.CTkEntry(app, placeholder_text="Что надо сделать?", width=340, height=40, font=("Segoe UI", 14))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: add_task()) 

btn = ctk.CTkButton(app, text="Добавить", command=add_task, width=340, height=40, font=("Segoe UI", 14, "bold"))
btn.pack(pady=(0, 10))

# кнопка экспорта
btn_export = ctk.CTkButton(app, text="💾 Сохранить как...", command=export_tasks, width=340, height=35, font=("Segoe UI", 13), fg_color="gray30", hover_color="gray40")
btn_export.pack(pady=(0, 20))

task_frame = ctk.CTkScrollableFrame(app, width=360, height=320, fg_color="transparent", scrollbar_button_color="gray30")
task_frame.pack(pady=0, padx=20, fill="both", expand=True)

load_tasks()
update_task_list()

app.mainloop()