import pydantic
import dataclasses


class PodPodPodPodCategoryValidate(pydantic.BaseModel):
    id: int
    name: str
    childs: list = None
    shard: str
    query: str

class PodPodPodCategoryValidate(pydantic.BaseModel):
    id: int
    name: str
    childs: list[PodPodPodPodCategoryValidate] = None
    shard: str
    query: str

class PodPodCategoryValidate(pydantic.BaseModel):
    id: int
    name: str
    childs: list[PodPodPodCategoryValidate] = None
    shard: str
    query: str

class PodCategoryValidate(pydantic.BaseModel):
    id: int
    name: str
    url: str
    shard: str
    query: str
    childs: list[PodPodCategoryValidate] = None

    @pydantic.validator("url")
    def url_validator_1(cls, value: str):
        if " " not in value:
            return value
        raise ValueError

    @pydantic.validator("query")
    def url_validator_2(cls, value: str):
        if " " not in value:
            return value
        raise ValueError


class CategoryValidateAll(pydantic.BaseModel):
    id: int
    name: str
    url: str
    shard: str
    query: str

    @pydantic.validator("url")
    def url_validator_1(cls, value: str):
        if " " not in value:
            return value
        raise ValueError


class CategoryValidateChilds(CategoryValidateAll):
    childs: list[PodCategoryValidate] = None


class CategoryValidateAlcohol(CategoryValidateAll):
    dest: list


def validate(data: str):
    result_category_list = []
    validation_count_errors = 0
    print("Ошибки валидации")
    for category in data:
        try:
            result_category_list.append(CategoryValidateChilds.parse_obj(category))
        except pydantic.ValidationError as e:
            try:
                result_category_list.append(CategoryValidateAlcohol.parse_obj(category))
            except pydantic.ValidationError as e:
                # try:
                #     result_category_list.append(CategoryValidateAll.parse_obj(category))
                # except pydantic.ValidationError as e:
                # print(e.json())
                # pass
                # print(category)
                validation_count_errors += 1
    print("-" * 20)
    print(f"{validation_count_errors}")
    print("-" * 20)
    return result_category_list[:]


if __name__ == '__main__':
    # import json
    #
    # with open("../json/main_menu.json", "r", encoding="utf-8") as file:
    #     json_file = json.load(file)
    # validate(json_file)
    pass
