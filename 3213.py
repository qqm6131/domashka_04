import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import sqlite3

def create_db():
    connection = sqlite3.connect('app_data.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS records
                   (record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   content TEXT,
                   level INTEGER)
    ''')
    connection.commit()
    connection.close()

def set_status(msg, color="black"):
    status_label.config(text=msg, fg=color)

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_content.delete(0, tk.END)
    entry_level.current(0)

def add_record():
    new_content = entry_content.get().strip()
    selected_level = entry_level.get()
    new_level = selected_level.split(" ")[0]
    
    if new_content and new_level.isdigit() and 0 <= int(new_level) <= 3:
        connection = sqlite3.connect('app_data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO records (content, level) VALUES (?, ?)", (new_content, int(new_level)))
        connection.commit()
        connection.close()
        clear_entries()
        view_records()
    else:
        set_status("Ошибка: Введите текст и выберите уровень приоритета.") 

def edit_record():
    edit_id = entry_id.get().strip()
    updated_content = entry_content.get().strip()
    selected_level = entry_level.get()
    updated_level = selected_level.split(" ")[0]
    
    if edit_id.isdigit() and updated_content and updated_level.isdigit() and 0 <= int(updated_level) <= 3: 
        connection = sqlite3.connect('app_data.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE records SET content = ?, level = ? WHERE record_id = ?", 
                   (updated_content, int(updated_level), int(edit_id)))
        if cursor.rowcount == 0:
            set_status(f"Ошибка: Запись с ID {edit_id} не найдена.")
        else:
            set_status("Запись обновлена.")
            clear_entries()
            view_records()
        connection.commit()
        connection.close()
    else:
        set_status("Ошибка: Введите ID, текст и выберите уровень приоритета.", "red")

def delete_record():
    delete_id = entry_id.get().strip()
    
    if delete_id.isdigit():
        connection = sqlite3.connect('app_data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM records WHERE record_id = ?", (int(delete_id),))
        if cursor.rowcount == 0:
            set_status(f"Ошибка: Запись с ID {delete_id} не найдена.")
        else:
            set_status("Запись удалена.")
            clear_entries()
            view_records()
        connection.commit()
        connection.close()
    else:
        set_status("Ошибка: Введите ID записи.")

def view_records():
    connection = sqlite3.connect('app_data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM records ORDER BY level DESC")
    records = cursor.fetchall()
    connection.close()
    
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    if records:
        for record in records:
            line = f"ID: {record[0]} | Текст: {record[1]} | Уровень: {record[2]}\n"
            text_area.insert(tk.END, line)
    else:
        text_area.insert(tk.END, "Записей нет.")
    text_area.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Записи")
root.geometry("500x400")
root.resizable(False, False)

padx, pady = 10, 5

tk.Label(root, text="ID записи (для редактирования/удаления):").grid(row=0, column=0, sticky="w", padx=padx, pady=pady)
entry_id = tk.Entry(root, width=40)
entry_id.grid(row=0, column=1, padx=padx, pady=pady)

tk.Label(root, text="Текст записи:").grid(row=1, column=0, sticky="w", padx=padx, pady=pady)
entry_content = tk.Entry(root, width=40)
entry_content.grid(row=1, column=1, padx=padx, pady=pady)

tk.Label(root, text="Уровень приоритета:").grid(row=2, column=0, sticky="w", padx=padx, pady=pady)

priority_values = [
    "0 - без приоритета",
    "1 - низкий",
    "2 - средний",
    "3 - высокий"
]

entry_level = ttk.Combobox(root, values=priority_values, state="readonly", width=37)
entry_level.grid(row=2, column=1, padx=padx, pady=pady)
entry_level.current(0)

btn_frame = tk.Frame(root)
btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 10))

btn_add = tk.Button(btn_frame, text="Добавить запись", width=15, command=add_record)
btn_add.grid(row=0, column=0, padx=5)

btn_edit = tk.Button(btn_frame, text="Изменить запись", width=15, command=edit_record)
btn_edit.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(btn_frame, text="Удалить запись", width=15, command=delete_record)
btn_delete.grid(row=0, column=2, padx=5)

btn_view = tk.Button(btn_frame, text="Обновить список", width=15, command=view_records)
btn_view.grid(row=0, column=3, padx=5)

btn_exit = tk.Button(btn_frame, text="Выход", width=15, command=root.quit)
btn_exit.grid(row=0, column=4, padx=5)

text_area = scrolledtext.ScrolledText(root, width=60, height=12, state=tk.DISABLED)
text_area.grid(row=4, column=0, columnspan=2, padx=padx, pady=(0,10))

status_label = tk.Label(root, text="", anchor="w", fg="green")
status_label.grid(row=5, column=0, columnspan=2, sticky="we", padx=padx, pady=(0,10))

create_db()
view_records()

root.mainloop()
