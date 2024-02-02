import os
import json
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from customtkinter import CTk, CTkEntry, CTkLabel, CTkButton

# Открытие json-файла с именами подключений к RDP
base_connection_file = 'base_connection.json'
# Пытаемся открыть файл, если он существует
try:
    with open(base_connection_file) as f:
        base_connection = json.load(f)
except FileNotFoundError:
    # Если файл не найден, создаем новый пустой
    base_connection = {}
    with open(base_connection_file, 'w') as f:
        json.dump(base_connection, f)

# Глобальные переменные для сортировки
sort_column = None
sort_reverse = False

# Определение столбцов
columns = ("Имя подключения", "Адрес подключения", "Комментарий")

def load_connections(tree):
    global base_connection, sort_column, sort_reverse

    # Очистка списка подключений
    tree.delete(*tree.get_children())

    # Загрузка подключений из файла
    with open(base_connection_file, 'r') as f:
        base_connection = json.load(f)

    # Проверяем, что base_connection - это действительно словарь
    if not isinstance(base_connection, dict):
        base_connection = {}

    # Заполнение списка подключений
    data = []
    for name, info in base_connection.items():
        address = info.get("address", "")
        comment = info.get("comment", "")
        data.append((name, address, comment))

    if sort_column:
        data.sort(key=lambda x: x[0], reverse=sort_reverse)

    for name, address, comment in data:
        tree.insert("", "end", values=(name, address, comment))




def sort_tree_column(tree, col):
    global sort_column, sort_reverse
    sort_column = col

    # Получаем все значения столбца в виде отдельного списка
    data = [(tree.set(k, col), k) for k in tree.get_children("")]
    # Сортируем список
    data.sort(reverse=sort_reverse)
    # Переупорядочиваем значения в отсортированном порядке
    for index, (_, k) in enumerate(data):
        tree.move(k, "", index)

    # В следующий раз выполняем сортировку в обратном порядке
    sort_reverse = not sort_reverse
    
def add_connection(tree):
    global base_connection
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
    address_entry = CTkEntry(add_win, placeholder_text="Адрес", width=120)
    comment_label = CTkLabel(add_win, text="Комментарий:")
    comment_entry = CTkEntry(add_win, placeholder_text="Комментарий", width=120)

    # Размещение элементов формы на окне
    name_label.grid(column=0, row=0, pady=3, padx=3)
    name_entry.grid(column=1, row=0, pady=3, padx=3)
    address_label.grid(column=0, row=1, pady=3, padx=3)
    address_entry.grid(column=1, row=1, pady=3, padx=3)
    comment_label.grid(column=0, row=2, pady=3, padx=3)
    comment_entry.grid(column=1, row=2, pady=3, padx=3)

    # Функция для обработки нажатия кнопки "Добавить"
    def add_connection_confirm():
        name = name_entry.get()
        address = address_entry.get()
        comment = comment_entry.get()
        if name and address:
            base_connection[name] = {"address": address, "comment": comment}
            with open(base_connection_file, 'w', encoding='utf-8') as f:
                json.dump(base_connection, f, indent=4, ensure_ascii=False)
            # Добавляем новый элемент в список подключений
            tree.insert("", "end", values=(name, address, comment))
            # Закрываем окно добавления подключения
            add_win.destroy()
            messagebox.showinfo("Сообщение", "Подключение добавлено")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    # Создание кнопки подтверждения
    confirm_button = CTkButton(add_win, text="Добавить", command=add_connection_confirm)
    confirm_button.grid(row=3, column=1, pady=3, padx=3)

    # Ожидание закрытия окна
    add_win.mainloop()

def edit_connection(tree):
    global base_connection
    # Получение выделенного элемента из списка подключений
    try:
        selected_item = tree.selection()[0]
        selected_name, address, comment = tree.item(selected_item, 'values')
    except IndexError:
        messagebox.showerror("Ошибка", "Выберите подключение для изменения данных")
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
    comment_label = CTkLabel(edit_win, text="Комментарий:")
    comment_entry = CTkEntry(edit_win, width=120)
    comment_entry.insert(0, comment)

    # Размещение элементов формы на окне
    name_label.grid(column=0, row=0, pady=3, padx=3)
    name_entry.grid(column=1, row=0, pady=3, padx=3)
    address_label.grid(column=0, row=1, pady=3, padx=3)
    address_entry.grid(column=1, row=1, pady=3, padx=3)
    comment_label.grid(column=0, row=2, pady=3, padx=3)
    comment_entry.grid(column=1, row=2, pady=3, padx=3)

    # Функция сохранения изменений
    def edit_connection_confirm():
        name = name_entry.get()
        new_address = address_entry.get()
        new_comment = comment_entry.get()
        if name and new_address:
            # Удаление старого подключения
            del base_connection[selected_name]
            # Добавление нового подключения
            base_connection[name] = {"address": new_address, "comment": new_comment}
            with open(base_connection_file, 'w') as f:
                json.dump(base_connection, f, indent=4)
            # Изменение названия в списке подключений
            tree.item(selected_item, values=(name, new_address, new_comment))
            # Обновление списка подключений
            load_connections(tree)
            # Закрытие окна редактирования подключения
            edit_win.destroy()
            messagebox.showinfo("Сообщение", "Подключение изменено")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    # Создание кнопки сохранения
    confirm_button = CTkButton(edit_win, text="Сохранить", command=edit_connection_confirm)
    confirm_button.grid(row=3, column=0, pady=3, padx=6)

    edit_win.mainloop()

def delete_connection(tree):
    global base_connection
    # Получение выделенного элемента из списка подключений
    try:
        selected_item = tree.selection()[0]
        selected_name, _, _ = tree.item(selected_item, 'values')
    except IndexError:
        messagebox.showerror("Ошибка", "Выберите подключение для удаления")
        return

    # Подтверждение удаления
    confirm = messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить подключение '{selected_name}'?")
    if confirm:
        # Удаление подключения из словаря
        del base_connection[selected_name]

        # Запись обновленных данных в файл
        with open(base_connection_file, 'w') as f:
            json.dump(base_connection, f, indent=4)

        # Удаление элемента из Treeview
        tree.delete(selected_item)

def connect(tree):
    # Получение выделенного элемента из списка подключений
    try:
        selected_item = tree.selection()[0]
        _, address, _ = tree.item(selected_item, 'values')
    except IndexError:
        messagebox.showerror("Ошибка", "Выберите подключение для соединения")
        return

    # Запуск RDP
    subprocess.run(['mstsc', '/v:' + address])

# Создание главного окна приложения
root = CTk()
root.title("RDP Address book")
root.geometry("610x380x400x400")
root.resizable(0, 0)

# Создание Treeview для отображения подключений
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")

tree.column("Имя подключения", anchor="center", width=200)
tree.column("Адрес подключения", anchor="center", width=200)
tree.column("Комментарий", anchor="center", width=200)

tree.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# Настройка заголовков столбцов
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: sort_tree_column(tree, c))

# Загрузка подключений из файла
load_connections(tree)

# Создание кнопок для добавления, удаления и соединения с подключением
button_frame = tk.Frame(root, padx=5, pady=5)
button_frame.grid(row=1, column=0, columnspan=3)

add_button = CTkButton(button_frame, text="Добавить", command=lambda: add_connection(tree))
add_button.grid(row=0, column=0, padx=5, pady=5)

delete_button = CTkButton(button_frame, text="Удалить", command=lambda: delete_connection(tree))
delete_button.grid(row=0, column=1, padx=5, pady=5)

connect_button = CTkButton(button_frame, text="Соединение", command=lambda: connect(tree))
connect_button.grid(row=1, column=1, padx=5, pady=5)

edit_button = CTkButton(button_frame, text="Изменить", command=lambda: edit_connection(tree))
edit_button.grid(row=1, column=0, padx=5, pady=5)

# Добавлены кнопки для комментариев
#add_comment_button = CTkButton(button_frame, text="Добавить комментарий", command=lambda: add_comment(tree))
#add_comment_button.grid(row=1, column=1, padx=5, pady=5)

#edit_comment_button = CTkButton(button_frame, text="Изменить комментарий", command=lambda: edit_comment(tree))
#edit_comment_button.grid(row=1, column=2, padx=5, pady=5)

# Запуск главного цикла обработки событий
root.mainloop()
