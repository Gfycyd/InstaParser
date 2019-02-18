from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
validator_fn = [
    ##RegexValidator(r'[#]s+', "Hashtag #.....(любой символ)"),
    RegexValidator(r'@[w.]*','Login @...(0-9,a-z,_)')

]
validator_fn2 = [
    RegexValidator(r'[#]s+', "Hashtag #.....(любой символ)"),

]
def valid(value):
    err = None
    if (value[0] == "@"):
        for validator in validator_fn:
            try:
                validator(value)
            # Valid value, return it
                return value
            except ValidationError:
                return "Введенные данные: " + value + ". Неправильный формат для логина, логин: @....( вместо точек любая буква английского алфавита, цифра или нижнее подчеркивание)"

    if (value[0] == "#"):
        for validator in validator_fn:
            try:
                validator(value)
            # Valid value, return it
                return value
            except ValidationError:
                return "Введенные данные: " + value + ". Неправильный формат для хештега, хештег: #....( вместо точек любой символ кроме пробела)"
    else:
        return

