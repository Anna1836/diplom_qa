# --- URL ---
BASE_URL = "http://localhost:8080/"

# --- Данные для оплаты ---
VALID_CARD = {
    "number": "4444 4444 4444 4442", # Пример валидной карты
    "holder": "Ivan Ivanov",
    "cvc": "123",
    "month": "12",
    "year": "30" # Будущий год
}

INVALID_CARD = {
    "number": "4444 4444 4444 4442", # Пример валидной карты
    "holder": "Ivan Ivanov",
    "cvc": "123",
    "month": "12",
    "year": "30" # Будущий год
}

EXPIRED_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "123",
    "month": "11",
    "year": "20" # Прошедший год
}

INVALID_CVC_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": " ", # Неверный формат
    "month": "11",
    "year": "30"
}

INVALID_M_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": " ", # Неверный формат
    "year": "30"
}
# autotests_python/data/test_data.py

"""
Модуль содержит константы с тестовыми данными для сценариев оплаты.
Данные извлечены из существующих тестов для централизации и переиспользования.
"""

# --- Позитивный сценарий ---


# Тест 7: Оплата с пустым годом
INVALID_Y_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": "12",
    "year": ""   # Пустой год
}

# Тест 8: Оплата с пустым полем «Владелец»
EMPTY_HOLDER_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "", # Пустое поле
    "cvc": "999",
    "month": "12",
    "year": "30"
}

# Тест 9: Оплата с незаполненным полем CVV
EMPTY_CVC_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "",   # Пустой CVC
    "month": "12",
    "year": "30"
}
# Тест 10: Пустой номер карты
EMPTY_number_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "",
    "month": "12",
    "year": "30"
}
# Тест 11: Номер карты с буквой
CARD_WITH_LETTER = {
    "number": "4444 4444 4444 44A1", # Буква 'A' вместо цифры
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": "12",
    "year": "30"
}

# Тест 12: Месяц с неверным форматом (буквы)
MONTH_INVALID_FORMAT = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": "AY", # Недопустимые символы
    "year": "30"
}

# Тест 13: Год с неверным форматом (буквы)
YEAR_INVALID_FORMAT = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": "12",
    "year": "AS"  # Недопустимые символы
}

# Тест 14: CVV с буквами
CVC_WITH_LETTERS = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "ABC", # Только буквы
    "month": "12",
    "year": "30"
}

# Тест 15: Имя владельца - только цифры
HOLDER_ONLY_DIGITS = {
    "number": "4444 4444 4444 4441",
    "holder": "1234567890", # Только цифры
    "cvc": "999",
    "month": "12",
    "year": "30"
}

# Тест 16: Месяц - пробелы
MONTH_WITH_SPACES = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": " ",  # Пробел
    "year": "30"
}

# Тест 17: Год - пробелы
YEAR_WITH_SPACES = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": "999",
    "month": "12",
    "year": " "   # Пробел
}

# Тест 18: CVV - пробел
CVC_WITH_SPACE = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov",
    "cvc": " ",   # Пробел
    "month": "12",
    "year": "30"
}

# Тест 19: Имя владельца - пробел
HOLDER_WITH_SPACE = {
    "number": "4444 4444 4444 4441",
    "holder": " ",  # Пробел
    "cvc": "999",
    "month": "12",
    "year": "30"
}

# Тест 20: Длинное имя владельца
LONG_NAME_CARD = {
    "number": "4444 4444 4444 4441",
    "holder": "Ivan Ivanov Ivan Ivanov Ivan Ivanov Ivan Ivanov",
    "cvc": "123",
    "month": "11",
    "year": "31"
}