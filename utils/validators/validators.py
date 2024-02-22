

letters = 'abcdefghijklmnopqrstuvwxyz'
letters_ru = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
all_letters = letters + letters_ru + letters.upper() + letters_ru.upper()


async def validate_name(name: str):
    """Validate name - not required name without letters, letters quantity > 1"""

    letters_in_name = [sign for sign in name if sign in all_letters]
    if len(letters_in_name) > 1:
        print(f'[Validation] Name "{name}" is GOOD')
        result = name.capitalize()
    else:
        print(f'[Validation] Name "{name}" is WRONG')
        result = None

    return result


async def validate_phone_number(phone: str):
    """Validate phone number - digits in message from user >= 5 """

    digit_qty = 0
    for sign in phone:
        try:
            int(sign)
            digit_qty += 1
        except ValueError:
            pass

    if digit_qty >= 5:
        print(f'[Validation] Phone "{phone}" is GOOD')
        result = phone
    else:
        print(f'[Validation] Phone "{phone}" is WRONG')
        result = None

    return result


async def validate_delivery_address(address: str):
    """Validate delivery address - not required address without letters, letters quantity > 5"""

    letters_in_name = [sign for sign in address if sign in all_letters]
    if len(letters_in_name) > 5:
        print(f'[Validation] Address "{address}" is GOOD')
        result = address
    else:
        print(f'[Validation] Address "{address}" is WRONG')
        result = None

    return result
