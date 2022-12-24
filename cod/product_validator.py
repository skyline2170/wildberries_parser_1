import datetime

import pydantic


class OptionsValidate(pydantic.BaseModel):
    name: str = None
    value: str = None


class CompositionsValidate(pydantic.BaseModel):
    name: str = None


class ProductValidate(pydantic.BaseModel):
    name: str = pydantic.Field(None, alias="imt_name")
    id: int = pydantic.Field(None, alias="nm_id")
    description: str = None
    options: list[OptionsValidate] = None
    compositions: list[CompositionsValidate] = None


def validate(raw_json):
    try:
        valid_json = ProductValidate.parse_obj(raw_json)
        return valid_json.dict()
    except pydantic.ValidationError as e:
        print(e)
        print("Ошибка валидации товара")
        return None


if __name__ == '__main__':
    pass
