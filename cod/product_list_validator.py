import pydantic


class SizesValidate(pydantic.BaseModel):
    name: str
    origName: str


class ProductValidate(pydantic.BaseModel):
    id: int
    sizes: list[SizesValidate]
    brand: str


class ProductsValidate(pydantic.BaseModel):
    products: list[ProductValidate]


class ProductListValidate(pydantic.BaseModel):
    data: ProductsValidate


def validate(raw_json):
    try:
        json_validate = ProductListValidate.parse_obj(raw_json)
        return json_validate.dict()
    except pydantic.ValidationError as e:
        print(e.json())
        return None


if __name__ == '__main__':
    pass
    # import json
    #
    # with open("../json/product_list.json", "r", encoding="utf-8") as file:
    #     j = json.load(file)
    # print(validate(j).json())
