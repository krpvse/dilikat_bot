from pydantic import BaseModel, field_validator


class CustomerInfoSchema(BaseModel):
    __DIGITS: str = '0123456789'
    __LETTERS: str = 'abcdefghijklmnopqrstuvwxyz'
    __LETTERS_RU: str = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
    __ALL_LETTERS: str = __LETTERS + __LETTERS_RU + __LETTERS.upper() + __LETTERS_RU.upper()

    first_name: str = None
    last_name: str = None
    phone_number: str = None
    delivery_address: str = None

    @classmethod
    def __get_letter_qty(cls, v: str):
        all_letters = str(cls.__ALL_LETTERS)
        letters = list(filter(lambda x: x in all_letters, v))
        return len(letters)

    @classmethod
    def __get_digit_qty(cls, v: str):
        all_digits = str(cls.__DIGITS)
        digits = list(filter(lambda x: x in all_digits, v))
        return len(digits)

    @field_validator('first_name', 'last_name')
    @classmethod
    def must_be_2_letters_and_more(cls, v: str):
        letter_qty = cls.__get_letter_qty(v)
        if letter_qty < 2:
            raise ValueError('Name should have at least 2 letters')
        return v

    @field_validator('delivery_address')
    @classmethod
    def must_be_5_letters_and_more(cls, v: str):
        letter_qty = cls.__get_letter_qty(v)
        if letter_qty < 5:
            raise ValueError('Address should have at least 5 letters')
        return v

    @field_validator('phone_number')
    @classmethod
    def must_be_5_digits_and_more(cls, v: str):
        digit_qty = cls.__get_digit_qty(v)
        if digit_qty < 5:
            raise ValueError('Phone number should have at least 5 digits')
        return v
