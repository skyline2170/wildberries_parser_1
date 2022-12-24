import os.path
import profile
import threading
import time
import tkinter as tk
import ParserClass
import controler
import tkinter.messagebox as mbox
import line_profiler
import tkinter.ttk as ttk

root = tk.Tk()
root.geometry("300x300+100+100")

parse = None

data = None
last_list = []
# category_check = None
# child_list = None
path_list = []


def check_directory():
    if not os.path.exists("../data"):
        os.mkdir("../data")


def get_cat_product_button():

    global data
    # global category_check
    # global child_list
    global path_list

    listbox.delete(0, tk.END)

    data = controler.get_categories()
    print(data)
    if data:
        for i, d in enumerate(data):
            listbox.insert(i, d.name)
        # category_check = None
        # child_list = None
        path_list.clear()
        # b1["command"] = pars_button
        # b1["text"] = "Получить данные"
    else:
        mbox.showerror("Ошибка", "Не удалось получить данные.")


def listbox_click(event):
    print("gg")
    global data
    global last_list
    global path_list
    # global category_check
    active_category = listbox.curselection()

    print(active_category)
    if listbox.get(active_category) == "Назад" and last_list != None:
        listbox.delete(0, tk.END)
        for i, value in enumerate(last_list[-1]):
            listbox.insert(i, value)
        last_list.pop()
        # if len(path_list) > 0:
        #     path_list.pop()
        return True
    elif data:
        find_childs(data[:], listbox.get(active_category))


def find_childs(data: list, name):
    ii = 0
    try:
        name_list = []
        for ii in data:
            name_list.append(ii.name)
    except Exception as e:
        print(f"{ii=}")
    if name in name_list:
        index = name_list.index(name)
        if data[index].childs:
            last_list.append(listbox.get(0, tk.END))
            listbox.delete(0, tk.END)
            listbox.insert(0, "Назад")
            for i, value in enumerate(data[index].childs):
                listbox.insert(i + 1, value.name)
        else:
            # print("!" * 10)
            # print(l[index])
            # print("запрос на получение данных")
            return controler.pars(data[index])

    else:
        for i in data:
            if i.childs:
                if find_childs(i.childs, name):
                    break
            else:
                continue





def pars():
    pass





frame = tk.Frame(root)

listbox = tk.Listbox(frame, selectmode="SINGLE", width=40)
scroll_bar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
listbox["yscrollcommand"] = scroll_bar.set
listbox.pack(side=tk.LEFT)

listbox.bind("<Double-Button-1>", listbox_click)
scroll_bar.pack(side=tk.LEFT, fill=tk.Y)
frame.pack(side=tk.TOP)

b1 = tk.Button(root, text="Получить категории товаров", command=lambda:threading.Thread(target=get_cat_product_button,daemon=True).start(), bg="orange")
b1.pack(side=tk.TOP, fill=tk.X)

# button_clear = tk.Button(root, text="Очистить", command=None)
# button_clear.pack(side=tk.TOP, fill=tk.X)

if __name__ == '__main__':
    check_directory()
    root.mainloop()
