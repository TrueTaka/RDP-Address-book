import os
import json
import subprocess
import tkinter as tk
from tkinter import messagebox
#import customtkinter
from customtkinter import CTk, CTkEntry, CTkLabel, CTkButton
# Открытие json-файла с именами подключений к RDP
base_connection_file = 'base_connection.json'
if os.path.exists(base_connection_file):
    with open(base_connection_file) as f:
        base_connection = json.load(f)
else:
    base_connection = {}
    
def load_connections():
    # Создание файла base_connection.json, если его нет
    if not os.path.isfile(base_connection_file):
        with open(base_connection_file, 'w') as f:
            json.dump({}, f)

    # Очистка списка подключений
    connection_listbox.delete(0, tk.END)

    # Загрузка подключений из файла
    with open(base_connection_file, 'r') as f:
        base_connection = json.load(f)

    # Заполнение списка подключений
    for name, address in base_connection.items():
        connection_listbox.insert(tk.END, f"{name} - {address}")

# Функция добавления подключения
def add_connection():
    # Создание окна для ввода параметров подключения
    add_win = CTk()
    add_win.title("Добавить подключение")
    add_win.geometry("320x300x400x400")  # Ширина, высота, x - позиционирование ,  y - позиционирование
    add_win.resizable(0, 0)
    add_win.grid_columnconfigure(0, weight=1)

    # Создание элементов формы
    name_label = CTkLabel(add_win, text="Название подключения:")
    name_entry = CTkEntry(add_win, placeholder_text="Имя", width=120)
    address_label = CTkLabel(add_win, text="Адрес подключения:")
    address_entry = CTkEntry(add_win, placeholder_text="адрес", width=120)

    # Размещение элементов формы на окне
    name_label.grid(column=0, row=0, pady=3, padx=3)
    name_entry.grid(column=1, row=0, pady=3, padx=3)
    address_label.grid(column=0, row=1, pady=3, padx=3)
    address_entry.grid(column=1, row=1, pady=3, padx=3)

    # Функция для обработки нажатия кнопки "Добавить"
    def add_connection_confirm():
        name = name_entry.get()
        address = address_entry.get()
        if name and address:
            base_connection[name] = address
            with open(base_connection_file, 'w', encoding='utf-8') as f:
                json.dump(base_connection, f, indent=4, ensure_ascii=False)
            # Добавляем новый элемент в список подключений
            connection_listbox.insert(tk.END, f"{name} - {address}")
            # Закрываем окно добавления подключения
            add_win.destroy()
            messagebox.showinfo("Сообщение", "Подключение добавлено")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    # Создание кнопки подтверждения
    confirm_button = CTkButton(add_win, text="Добавить", command=add_connection_confirm)
    confirm_button.grid(row=2, column=1, pady=3, padx=3)

    # Ожидание закрытия окна
    add_win.mainloop()

#Функция изменения подключения    
def edit_connection():
    # Получение выделенного элемента из списка подключений
    try:
        selected_item = connection_listbox.get(connection_listbox.curselection())
        selected_name, address = selected_item.split(' - ', 1)
    except tk.TclError:
        messagebox.showerror("Ошибка", "Выберите подключение для изменения данных")
        return
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат строки подключения")
        return

    # Создание окна для редактирования параметров подключения
    edit_win = CTk()
    edit_win.title("Изменить подключение")
    edit_win.geometry("320x300x400x400")  # Ширина, высота, x - позиционирование ,  y - позиционирование
    edit_win.resizable(0, 0)
    edit_win.grid_columnconfigure(0, weight=1)

    # Создание элементов формы
    name_label = CTkLabel(edit_win, text="Название подключения:")
    name_entry = CTkEntry(edit_win, width=120)
    name_entry.insert(0, selected_name)
    address_label = CTkLabel(edit_win, text="Адрес подключения:")
    address_entry = CTkEntry(edit_win, width=120)
    address_entry.insert(0, address)

    # Размещение элементов формы на окне
    name_label.grid(column=0, row=0, pady=3, padx=3)
    name_entry.grid(column=1, row=0, pady=3, padx=3)
    address_label.grid(column=0, row=1, pady=3, padx=3)
    address_entry.grid(column=1, row=1, pady=3, padx=3)

    # Функция сохранения изменений
    def edit_connection_confirm():
        name = name_entry.get()
        new_address = address_entry.get()
        if name and new_address:
            # Удаление старого подключения
            del base_connection[selected_name]
            # Добавление нового подключения
            base_connection[name] = new_address
            with open(base_connection_file, 'w') as f:
                json.dump(base_connection, f, indent=4)
            # Изменение названия в списке подключений
            if connection_listbox.curselection():
                connection_listbox.delete(connection_listbox.curselection())
            connection_listbox.insert(tk.END, f"{name} - {new_address}")
            # Обновление списка подключений
            load_connections()
            # Закрытие окна редактирования подключения
            edit_win.destroy()
            messagebox.showinfo("Сообщение", "Подключение изменено")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    # Создание кнопки сохранения
    confirm_button = CTkButton(edit_win, text="Сохранить", command=edit_connection_confirm)
    confirm_button.grid(row=2, column=1, pady=3, padx=3)

    edit_win.mainloop()

        
# Функция удаления подключения
def delete_connection():
    # Получение выделенного элемента из списка подключений
    try:
        selected_name = connection_listbox.get(connection_listbox.curselection())
    except tk.TclError:
        messagebox.showerror("Ошибка", "Выберите подключение для удаления")
        return
    # Подтверждение удаления
    confirm = messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить подключение '{selected_name}'?")
    if confirm:
        # Create a copy of the keys before iterating and deleting
        keys_to_delete = [key for key in base_connection.keys() if key == selected_name]

        # Iterate over the copied keys and delete from the original dictionary
        for key in keys_to_delete:
            del base_connection[key]

        with open(base_connection_file, 'w') as f:
            json.dump(base_connection, f, indent=4)
        connection_listbox.delete(connection_listbox.curselection())

# Функция соединения с выбранным подключением
def connect():
    # Получение выделенного элемента из списка подключений
    try:
        selected_item = connection_listbox.get(connection_listbox.curselection())
        selected_name, address = selected_item.split(' - ', 1)
    except tk.TclError:
        messagebox.showerror("Ошибка", "Выберите подключение для соединения")
        return
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат строки подключения")
        return

    # Запуск RDP
    subprocess.run(['mstsc', '/v:' + address])

# Создание главного окна приложения
root = CTk()
root.title("RDP Соединения")
root.geometry("480x400x400x400")
root.resizable(0, 0)

# Создание рамки для списка подключений
connection_frame = tk.LabelFrame(root, text="Список подключений", padx=5, pady=5)
connection_frame.pack(fill="both", expand="yes")

# Надпись "Имя подключения"
name_label = tk.Label(connection_frame, text="Имя подключения")
name_label.grid(row=0, column=0, padx=5, pady=5)
# Надпись "Адрес подключения"
address_label = tk.Label(connection_frame, text="Адрес подключения")
address_label.grid(row=0, column=1, padx=5, pady=5)
# Создание Listbox для отображения подключений
connection_listbox = tk.Listbox(connection_frame, selectmode="SINGLE", activestyle="dotbox")
connection_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
# Загрузка подключений из файла
load_connections()

# Создание кнопок для добавления, удаления и соединения с подключением
button_frame = tk.Frame(root, padx=5, pady=5)
button_frame.pack()
add_button = CTkButton(button_frame, text="Добавить", command=add_connection)
add_button.grid(row=0, column=0, padx=5, pady=5)
delete_button = CTkButton(button_frame, text="Удалить", command=delete_connection)
delete_button.grid(row=0, column=1, padx=5, pady=5)
connect_button = CTkButton(button_frame, text="Соединение", command=connect)
connect_button.grid(row=1, column=1, padx=5, pady=5)
edit_button = CTkButton(button_frame, text=" Изменить ", command=edit_connection)
edit_button.grid(row=1, column=0, padx=5, pady=5)

# Запуск главного цикла обработки событий
root.mainloop()
