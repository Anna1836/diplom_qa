import pytest
from autotests_python.pages.payment_page import PaymentPage
from autotests_python.helpers.utils import save_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Импортируем Keys

@pytest.fixture(autouse=True)
def payment_page(browser):
    browser.get("http://localhost:8080/")
    buy_btn = browser.find_element(By.XPATH, "//span[contains(text(), 'Купить')]")
    buy_btn.click()
    return PaymentPage(browser)



def test_payment_with_valid_card(payment_page):
    """Тест: Успешная оплата с валидной картой."""
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("123")
    payment_page.fill_date(month="11", year="31")



    payment_page.submit()

    notification = payment_page.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".notification__content.success"))
    )
    assert "операция одобрена банком" in notification.text.lower()


def test_purchase_tour_with_credit_approval(payment_page):
    """
    Тест: Успешное одобрение кредита при покупке тура.
    Проверяет сценарий, где банк одобряет заявку.
    """
    # --- 1. Выбор способа оплаты "В кредит" ---
    # Находим и нажимаем кнопку "Купить в кредит".
    # Локатор изменен с абсолютного XPath на более надежный CSS-селектор по тексту.
    credit_btn = payment_page.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'в кредит')]"))
    )
    payment_page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_btn)
    credit_btn.click()

    # --- 2. Заполнение формы данными карты ---
    payment_page.fill_card_number("4444 4444 4444 4441")  # Валидный номер карты
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("123")
    payment_page.fill_date(month="11", year="35")  # Будущая дата

    # --- 3. Отправка заявки на кредит ---
    # Используем метод submit() из класса страницы.
    payment_page.submit()

    # --- 4. Проверка результата ---
    # Используем метод get_success_notification_text() для получения и проверки текста.
    popup_text = payment_page.get_success_notification_text()

    print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

    assert "операция одобрена банком" in popup_text, \
        f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

    print("✅ ТЕСТ ПРОЙДЕН: Кредит успешно одобрен.")

def test_payment_with_invalid_card_declined(payment_page):
    """
    Тест: Оплата тура с невалидной картой (статус DECLINED).
    Проверяет корректную обработку отказа банка.
    """
    # --- Заполнение данных держателя карты ---
    # Используем методы нашего класса PaymentPage.
    # Номер карты '4444...4442' настроен на отклонение в тестовой среде.
    payment_page.fill_card_number("4444 4444 4444 4442")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("123")
    payment_page.fill_date(month="11", year="26")

    # --- Отправка формы ---
    payment_page.submit()

    # --- Проверка результата (ОЖИДАЕМАЯ НЕУДАЧА) ---
    # Используем универсальный метод для проверки текста ошибки.
    popup_text = payment_page.get_success_notification_text() # Или другой метод, если ошибка в другом блоке

    print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

    assert "ошибка! банк отказал в проведении операции" in popup_text, \
           f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

    print("✅ ТЕСТ ПРОЙДЕН: Успешно обработан отказ банка.")

def test_empty_expiry_year(payment_page):
    #Тест 4: Оплата с просроченной картой
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("123")
    payment_page.fill_date(month="11", year="11") # Срок действия карты истёк

    # Отправка формы
    payment_page.submit()

    # Ожидание появления сообщения об ошибке
    # Локатор ищет элемент <span>, который является следующим соседом (following-sibling)
    # и содержит текст 'Истёк срок действия карты'.
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Истёк срок действия карты')]")
        )
    )

    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Истёк срок действия карты' не отображается"

def test_invalid_cvc_format(payment_page):
    # Тест 5: Оплата с пустым cvc
    # Заполнение полей формы
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc(" ") # Неверный формат CVC (пробел)
    payment_page.fill_date(month="11", year="30")

    # Отправка формы
    payment_page.submit()

    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )

    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

def test_empty_expiry_month(payment_page):
    # Тест 6: Оплата с пустым месяцем
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")  # Неверный формат CVC (пробел)
    payment_page.fill_date(month="", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )

    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"


def test_empty_year(payment_page):
    # Тест 6: Оплата с пустым годом
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )

    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

def test_invalid_cardholder_name(payment_page):
    # Тест: №8. Оплата с пустым полем «Владелец»
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
    )

    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"
def test_empty_cvc_field(payment_page):
#     """Тест 9: Оплата с незаполненным полем CVV"""
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке


    err = payment_page.wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
)

# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_empty_card_number(payment_page):
#     Тест 10: Пустой номер карты
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
# Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
)

# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_card_number_with_letter(payment_page):
#     Тест 11: Номер карты с буквой
    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
# Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
)
# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_month_with_invalid_format(payment_page):
#     """Тест 12: Месяц с неверным форматом, буквы вместо цифр"""

    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="AY", year="30")
    payment_page.submit()
# Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
)
# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_expiry_year_with_non_numeric(payment_page):
#     """№13. Оплата с годом, содержащим неверный формат
    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="AS")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )
    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_cvc_with_non_numeric(payment_page):
#     """Тест 14: Оплата с CVV, содержащим неверный формат (буквы вместо цифр)"""
    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("ABC")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )
    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_cardholder_name_with_numeric(payment_page):
#     """Тест 15: Оплата с именем владельца, содержащим неверный формат (только цифры)"""
    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder("1234567890")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
    )
    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"
def test_month_with_spaces(payment_page):
#     """№16. Оплата с месяцем, содержащим пробелы
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month=" ", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )
    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_expiry_year_with_space(payment_page):
#     """№17. Оплата с годом, содержащим пробелы
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year=" ")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
    )
# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_cvc_field_with_space(payment_page):
#     """Тест №18. Оплата с CVV, содержащим пробелы"""
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov")
    payment_page.fill_cvc(" ")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
)
# Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"
def test_name_with_spaces(payment_page):
#     """Тест 19: Оплата с именем владельца, содержащим пробелы"""
    payment_page.fill_card_number("4444 4444 4444 44A1")
    payment_page.fill_holder(" ")
    payment_page.fill_cvc("999")
    payment_page.fill_date(month="12", year="30")
    payment_page.submit()
    # Ожидание появления сообщения об ошибке
    err = payment_page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
    )
    # Проверка, что элемент с ошибкой отображается на странице
    assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"
def test_payment_long_name(payment_page):
#     """Тест 20: Оплата тура валидной картой с длинным именем владельца """
    payment_page.fill_card_number("4444 4444 4444 4441")
    payment_page.fill_holder("Ivan Ivanov Ivan Ivanov Ivan Ivanov Ivan Ivanov")
    payment_page.fill_cvc("123")
    payment_page.fill_date(month="11", year="31")

    payment_page.submit()

    notification = payment_page.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".notification__content.success"))
    )
    assert "операция одобрена банком" in notification.text.lower()







# --- Вспомогательная функция  ---
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


    # clear_input_by_backspace(card_field)

    # ШАГ 3: Проверяем результат
    # Получаем текущее значение атрибута 'value' из элемента
    field_value = card_field.get_attribute('value')

    # Проверяем, что поле действительно пустое
    assert field_value == "", f"Поле 'Номер карты' не очищено. Текущее значение: '{field_value}'"
