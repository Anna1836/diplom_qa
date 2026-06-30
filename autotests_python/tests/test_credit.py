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
# Импортируем наш новый класс шагов

#
#
def test_purchase_tour_with_credit_approval(payment_page):
    """
    Покупка тура в кредит → Банк одобрил заявку.
    Проверяет, что отображается правильное уведомление.
    """
    steps = PaymentSteps(payment_page)
    steps.pay_with_card(VALID_CARD)

    # Ждем появления уведомления
    notification = steps.wait_for_popup(timeout=10)
    message = notification.text.strip()

    assert message == "Операция одобрена банком.", (
        f"Появилось другое сообщение: `{message}`"
    )
