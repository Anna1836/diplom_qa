from autotests_python.data.test_data import INVALID_CVC_CARD, EXPIRED_CARD, \
    INVALID_M_CARD, INVALID_Y_CARD, INVALID_CVC_CARD, INVALID_CARD, EMPTY_number_CARD, EXPIRED_CARD, INVALID_M_CARD, VALID_CARD, INVALID_Y_CARD, EMPTY_HOLDER_CARD, EMPTY_CVC_CARD, CARD_WITH_LETTER, MONTH_INVALID_FORMAT, YEAR_INVALID_FORMAT, CVC_WITH_LETTERS, HOLDER_ONLY_DIGITS, MONTH_WITH_SPACES, YEAR_WITH_SPACES, CVC_WITH_SPACE, HOLDER_WITH_SPACE, LONG_NAME_CARD
from autotests_python.steps.payment_steps import PaymentSteps
from autotests_python.helpers.utils import assert_element_text_contains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_payment_with_valid_card(payment_page):
    #     """Тест 1: Успешная оплата с валидной картой."""
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(VALID_CARD)

    assert "операция одобрена банком" in notification.text.lower()


#
def test_payment_with_invalid_card_declined(payment_page):
    #   Тест 3 : Оплата тура с невалидной картой (статус DECLINED).
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(INVALID_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Ошибка! Банк отказал в проведении операции",
        error_message="Ошибка 'Ошибка! Банк отказал в проведении операции' не отображается"
    )



def test_empty_expiry_year(payment_page):
    """Тест 4: Оплата с просроченной картой."""

    steps = PaymentSteps(payment_page)
    steps.pay_with_card(EXPIRED_CARD)
    error_element = payment_page.get_error_message_element()

    assert_element_text_contains(
        element=error_element,
        expected_text="Истёк срок",
        error_message="Ошибка об истечении срока действия карты не отображается"
    )


def test_invalid_cvc_format(payment_page):
    """Тест 5: Оплата с пустым cvc."""

    steps = PaymentSteps(payment_page)
    steps.pay_with_card(INVALID_CVC_CARD)

    error_element = payment_page.get_error_message_element()
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
        expected_text="Поле обязательно для заполнения",
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
        expected_text="Поле обязательно для заполнения",
        error_message="Ошибка валидации имени владельца карты не отображается"
    )


def test_payment_long_name(payment_page):
    #     """Тест 20: Оплата тура валидной картой с длинным именем владельца """
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(LONG_NAME_CARD)
    error_element = payment_page.get_error_message_element()

    assert "операция одобрена банком" in notification.text.lower()


def test_clear_payment_form_fields(payment_page):
    #     """Тест 21: Проверка очистки полей формы """
    steps = PaymentSteps(payment_page)
    steps.fill_card_number("4444 4444 4444 4441")
    steps.fill_card_number("")

    field_value = payment_page.driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"
    ).get_attribute("value")

    assert field_value == ""
