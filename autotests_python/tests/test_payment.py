import pytest
from autotests_python.pages.payment_page import PaymentPage
from autotests_python.helpers.utils import save_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Импортируем Keys
from autotests_python.data.test_data import INVALID_CVC_CARD, INVALID_CARD, EMPTY_number_CARD, EXPIRED_CARD, INVALID_M_CARD, VALID_CARD, INVALID_Y_CARD, EMPTY_HOLDER_CARD, EMPTY_CVC_CARD, CARD_WITH_LETTER, MONTH_INVALID_FORMAT, YEAR_INVALID_FORMAT, CVC_WITH_LETTERS, HOLDER_ONLY_DIGITS, MONTH_WITH_SPACES, YEAR_WITH_SPACES, CVC_WITH_SPACE, HOLDER_WITH_SPACE, LONG_NAME_CARD
from autotests_python.tests.payment_steps import PaymentSteps
from autotests_python.helpers.utils import assert_element_text_contains

@pytest.fixture(autouse=True)
def payment_page(browser):
    browser.get("http://localhost:8080/")
    buy_btn = browser.find_element(By.XPATH, "//span[contains(text(), 'Купить')]")
    buy_btn.click()
    return PaymentPage(browser)



def test_payment_with_valid_card(payment_page):
#     """Тест 1: Успешная оплата с валидной картой."""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(VALID_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка 'Неверный формат' не отображается"
    )
    assert "операция одобрена банком" in notification.text.lower()



#
def test_payment_with_invalid_card_declined(payment_page):

 #   Тест 3 : Оплата тура с невалидной картой (статус DECLINED).
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(INVALID_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка 'Неверный формат' не отображается"
    )
    # --- Проверка результата (ОЖИДАЕМАЯ НЕУДАЧА) ---
    # Используем универсальный метод для проверки текста ошибки.
    popup_text = payment_page.get_success_notification_text() # Или другой метод, если ошибка в другом блоке

    print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

    assert "ошибка! банк отказал в проведении операции" in popup_text, \
           f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"



def test_empty_expiry_year(payment_page):
    """Тест 4: Оплата с просроченной картой."""
    # ... (код заполнения формы) ...
    #1. Создаем экземпляр шагов, передавая ему объект страницы
    steps = PaymentSteps(payment_page)

        # 2. Вызываем готовый метод для выполнения действия
    steps.pay_with_card(EXPIRED_CARD)
    # Было:
    # error_text = payment_page.get_error_message_text()
    # assert "Истёк срок" in error_text, f"Ожидалась ошибка по сроку действия, но получила: {error_text}"

    # СТАЛО:
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Истёк срок",
        error_message="Ошибка об истечении срока действия карты не отображается"
    )

def test_invalid_cvc_format(payment_page):
    """Тест 5: Оплата с пустым cvc."""
    # ... (код заполнения формы через steps или напрямую) ...
    #1. Создаем экземпляр шагов, передавая ему объект страницы
    steps = PaymentSteps(payment_page)

        # 2. Вызываем готовый метод для выполнения действия
    steps.pay_with_card(INVALID_CVC_CARD)
    # Было:
    # error_text = payment_page.get_error_message_text()
    # assert "Неверный формат" in error_text, f"Ожидалась ошибка 'Неверный формат', но получила: {error_text}"

    # СТАЛО:
    error_element = payment_page.get_error_message_element()  # Предположим, метод возвращает сам элемент

    # Используем нашу новую функцию-ассерт
    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации CVC не отображается"
    )

#
#
def test_empty_expiry_month(payment_page):
#     # Тест 6: Оплата с пустым месяцем
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(INVALID_M_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации месяца действия карты не отображается"
    )

def test_empty_year(payment_page):
    # Тест 7: Оплата с пустым годом
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(INVALID_Y_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации года действия карты не отображается"
    )



def test_invalid_cardholder_name(payment_page):
    # Тест: №8. Оплата с пустым полем «Владелец»
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(EMPTY_HOLDER_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Поле обязательно для заполнения",
        error_message="Ошибка валидации владельца карты не отображается"
    )

def test_empty_cvc_field(payment_page):
#     """Тест 9: Оплата с незаполненным полем CVV"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(EMPTY_CVC_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации CVV не отображается"
    )

def test_empty_card_number(payment_page):
#     Тест 10: Пустой номер карты
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(EMPTY_number_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации номера карты карты не отображается"
    )


def test_card_number_with_letter(payment_page):
#     Тест 11: Номер карты с буквой
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(CARD_WITH_LETTER)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации номера карты не отображается"
    )

def test_month_with_invalid_format(payment_page):
#     """Тест 12: Месяц с неверным форматом, буквы вместо цифр"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(MONTH_INVALID_FORMAT)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации месяца действия карты не отображается"
    )


def test_expiry_year_with_non_numeric(payment_page):
#     """№13. Оплата с годом, содержащим неверный формат
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(YEAR_INVALID_FORMAT)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации года действия карты не отображается"
    )

def test_cvc_with_non_numeric(payment_page):
#     """Тест 14: Оплата с CVV, содержащим неверный формат (буквы вместо цифр)"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(CVC_WITH_LETTERS)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации CVV не отображается"
    )

def test_cardholder_name_with_numeric(payment_page):
#     """Тест 15: Оплата с именем владельца, содержащим неверный формат (только цифры)"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(HOLDER_ONLY_DIGITS)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации имени владельца карты не отображается"
    )

def test_month_with_spaces(payment_page):
#     """№16. Оплата с месяцем, содержащим пробелы
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(MONTH_WITH_SPACES)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации месяца действия карты не отображается"
    )

def test_expiry_year_with_space(payment_page):
#     """№17. Оплата с годом, содержащим пробелы
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(YEAR_WITH_SPACES)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации года действия карты не отображается"
    )

def test_cvc_field_with_space(payment_page):
#     """Тест №18. Оплата с CVV, содержащим пробелы"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(CVC_WITH_SPACE)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации CVV не отображается"
    )

def test_name_with_spaces(payment_page):
#     """Тест 19: Оплата с именем владельца, содержащим пробелы"""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(HOLDER_WITH_SPACE)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Неверный формат",
        error_message="Ошибка валидации имени владельца карты не отображается"
    )

def test_payment_long_name(payment_page):
#     """Тест 20: Оплата тура валидной картой с длинным именем владельца """
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(LONG_NAME_CARD)
    error_element = payment_page.get_error_message_element()

    # assert_element_text_contains(
    #     element=error_element,
    #     expected_text="Неверный формат",
    #     error_message="Ошибка валидации месяца действия карты не отображается"
    # )

    assert "операция одобрена банком" in notification.text.lower()





# ... другие импорты (By, EC и т.д.) ...

# --- Вспомогательная функция (если все же нужна) ---
def clear_input_by_backspace(element):
    """Вспомогательная функция для очистки одного input-элемента с помощью BACK_SPACE."""
    element.click()
    current_length = len(element.get_attribute("value"))
    for _ in range(current_length):
        element.send_keys(Keys.BACK_SPACE)



def test_clear_payment_form_fields(payment_page):
    """
    Тест: Проверка работы функции очистки полей формы оплаты.
    Шаг 1: Заполнить поле номера карты.
    Шаг 2: Очистить поле номера карты с помощью стандартного метода .clear().
    Шаг 3: Проверить, что поле стало пустым.
    """

    # ШАГ 1: Заполняем поле номера карты
    payment_page.fill_card_number("4444 4444 4444 4441")

    # ШАГ 2: Находим элемент поля карты и очищаем его
    # Мы используем тот же локатор, что и в методе fill_card_number
    card_field = payment_page.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']"))
    )


    card_field.clear()


    # ШАГ 3: Проверяем результат
    # Получаем текущее значение атрибута 'value' из элемента
    field_value = card_field.get_attribute('value')

    # Проверяем, что поле действительно пустое
    assert field_value == "", f"Поле 'Номер карты' не очищено. Текущее значение: '{field_value}'"
# def test_invalid_cvc_format(payment_page):
