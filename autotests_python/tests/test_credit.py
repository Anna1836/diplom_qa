import pytest
from autotests_python.pages.payment_page import PaymentPage
from autotests_python.helpers.utils import save_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Импортируем Keys

import pytest
from autotests_python.data.test_data import INVALID_CVC_CARD, INVALID_CARD, EMPTY_number_CARD, EXPIRED_CARD, \
    INVALID_M_CARD, VALID_CARD, INVALID_Y_CARD, EMPTY_HOLDER_CARD, EMPTY_CVC_CARD, CARD_WITH_LETTER, \
    MONTH_INVALID_FORMAT, YEAR_INVALID_FORMAT, CVC_WITH_LETTERS, HOLDER_ONLY_DIGITS, MONTH_WITH_SPACES, \
    YEAR_WITH_SPACES, CVC_WITH_SPACE, HOLDER_WITH_SPACE, LONG_NAME_CARD

from autotests_python.tests.payment_steps import PaymentSteps
from autotests_python.helpers.utils import assert_element_text_contains
import logging

# Импорты из Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger(__name__)


def test_purchase_tour_with_credit_approval(credit_payment_page):
    """
    Проверяет успешный сценарий покупки тура в кредит.
    Ожидаемый результат: банк одобряет заявку на кредит.
    """
    # Инициализируем шаги. Фикстура credit_payment_page уже перевела нас на нужный путь.
    steps = PaymentSteps(credit_payment_page)

    # --- 2. Заполнение формы данными карты ---
    # Данные для кредитной карты могут отличаться от обычной.
    # Если у вас есть отдельный набор данных VALID_CREDIT_CARD, используйте его.
    # Здесь для примера используем ручное заполнение.

    # ВАЖНО: Убедитесь, что номер карты, который вы используете, предназначен для теста кредита.
    # Часто для разных типов платежей используются разные "тестовые" карты.
    steps.pay_with_card(VALID_CARD)
    # --- 3. Отправка заявки на кредит ---
    steps.submit()

    # --- 4. Проверка результата ---
    popup_text = credit_payment_page.get_success_notification_text()

    logger.info(f"\n📝 Текст всплывающего окна: '{popup_text}'")

    assert "операция одобрена банком" in popup_text.lower(), \
        f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

    logger.info("✅ ТЕСТ ПРОЙДЕН: Кредит успешно одобрен.")
