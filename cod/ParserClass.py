import json

import requests as req
import main_menu_validator
import fake_useragent
import product_list_validator
import product_validator


class Parser:
    def __init__(self):
        self.main_page_json = None
        # self.user_agent = fake_useragent.UserAgent()
        self.uesr_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        self.product_list = None
        self.category_list = None

    def my_request(self, url: str):
        '''Делает запрос по указанному url. Возвращает ответ в виде json, если запрос удачен. Иначе возвращает None.'''
        try:
            # response = req.get(url, headers={"user-agent": self.user_agent.chrome})

            response = req.get(url, headers={"user-agent": self.uesr_agent})
            if response.ok:
                return response.json()
            return None
        except:
            print("Ошибка при запросе")
            return None

    def get_categores(self):
        '''Получаем json со всеми категориями и подкатегориями. Если успешно, то возвращат список с категориями,
        иначе None'''
        categores_json = self.my_request("https://static.wbstatic.net/data/main-menu-ru-ru.json")

        with open("../json/main_menu.json", "w", encoding="utf-8") as file:
            json.dump(categores_json, file, ensure_ascii=False, indent=4)

        if categores_json:
            categores_json = main_menu_validator.validate(categores_json)
            return categores_json[:]

    def categore_href_create(self,
                             category_data: main_menu_validator.CategoryValidateChilds | main_menu_validator.CategoryValidateAlcohol,
                             page: int = 1, sort="pricedown"):
        '''Получат на вход обект с данными о категории, возвращает ссылку на страницу со всеми товарами данной под
        категории.
        sort=(pricedown, priceup, popular, rate)'''
        shard = category_data.shard
        query = category_data.query
        if "kind" not in query:
            query = query + "&kind=1"
        href = f"https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort={sort}&spp=0" + "&" + query
        return href

    def get_product_json(self, id: int):
        '''Получает json страницы продукта, при неудаче возвращает None. На вход подаётся id продукта.'''
        for i in range(1, 21):
            if i < 10:
                response = self.my_request(
                    f"https://basket-0{i}.wb.ru/vol{id // 1000 // 100}/part{id // 1000}/{id}/info/ru/card.json")
            else:
                response = self.my_request(
                    f"https://basket-{i}.wb.ru/vol{id // 1000 // 100}/part{id // 1000}/{id}/info/ru/card.json")
            if response:
                return response
        return None

    def product_json_validate(self, product_json: dict):
        ...

    def get_product_list(self, href: str):
        '''Собирает все товары со страницы заданной категории.'''
        response = self.my_request(href)
        # print(response)
        if response:
            valid_json = product_list_validator.validate(response)
            return valid_json
        else:
            print("Не удалось получить все товары из данной категории. Ссылка не верна.")
            return None


if __name__ == '__main__':
    x = Parser()
    j = x.get_categores()
    # print(j[0])
    if j:
        href = x.categore_href_create(j[0].childs[0])
        product_id_json = x.get_product_list(href)
        # print(f"{product_id_json=}")
        if product_id_json:
            # product=x.get_product_json(product_id_json["data"]["product"][0]["id"])
            product_id = product_id_json["data"]["products"][1]["id"]
            product = x.get_product_json(product_id)
            product: dict = product_validator.validate(product)
            print(product)
            # print(list(product.items()).extend(list(product_id_json["data"]["products"][1].items().items())))


    else:
        print("j пусто")
    # j = x.product_json_validate(j)

    #
    # import pickle
    #
    # x = [1, 2, 2, 2, 2]
    # x = pickle.dumps(x)
    # print(x)
    # x = pickle.loads(x)
    # print(x)

# x = Parser()
# import json
#
# with open("../json/main_menu.json", "r", encoding="utf-8") as file:
#     json_file = json.load(file)
# j = main_menu_validate.validate(json_file)
# print(x.category_href_create(j[3].childs[0],page=1))

# shard = "men_clothes1"
# # kind = 1
# subgect = "&kind=1&subject=11;147;216;2287;4575"
# page = 1
# url = f"https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort=pricedown&spp=0" + subgect
# # # url = "https://catalog.wb.ru/catalog/men_clothes1/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&kind=1&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort=pricedown&spp=0&subject=11;147;216;2287;4575"
# response = req.get(url)
# print(response)
# print(response.json())
# print(response.url)

# https://basket-09.wb.ru/vol1244/part124409/124409663/info/ru/card.json

# https://catalog.wb.ru/catalog/men_clothes1/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort=pricedown&spp=0&kind=1&subject=11;147;216;2287;4575
# https://catalog.wb.ru/catalog/men_clothes1/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page=0&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort=pricedown&spp=0&kind=1&subject=11;147;216;2287;4575
# https://catalog.wb.ru/catalog/bl_shirts/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&kind=2&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=0&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&sort=pricedown&spp=0&subject=41;184;1429
