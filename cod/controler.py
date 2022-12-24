import datetime
import json
import multiprocessing
import threading
import tkinter as tk
import ParserClass
import product_validator
import cProfile
import line_profiler
import memory_profiler


def get_categories():
    "получает категории и подкатегории товаров с сайта."
    pars = ParserClass.Parser()
    product_list = pars.get_categores()
    if product_list:
        return product_list
    else:
        return None


def pars(category):
    multiprocessing.Process(target=pars_thread, args=(category,), daemon=True).start()


def pars_thread(category):
    print(category)
    result_data_list = []
    if category:
        pars = ParserClass.Parser()
        href = pars.categore_href_create(category)
        print(href)
        data = pars.get_product_list(href)
        print(data)
        if data:
            print("@" * 20)
            for i, value in enumerate(data["data"]["products"]):
                print(i, value)
                product_data = pars.get_product_json(value["id"])
                print(product_data)
                result_data_list.append(product_data)
            if result_data_list:
                with open(f"../data/{datetime.datetime.now().strftime('%d.%m.%y_%H_%M_%S')}.json", "w",
                          encoding="utf-8") as file:
                    json.dump(result_data_list, file, indent=4, ensure_ascii=False)
                print("всё")
                return True
            else:
                print("всё  ")
                return None
    else:
        print("всё")
        return None
