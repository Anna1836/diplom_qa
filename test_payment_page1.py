import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time  # Для использования time.sleep()
import os


# --- Фикстуры --- 
@pytest.fixture(scope="function")
def driver():
    """Инициализация браузера."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") # Раскомментируйте для запуска без GUI
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def open_payment_form(driver):
    """Открывает страницу и переходит к форме оплаты."""
    driver.get("http://localhost:8080/")
    wait = WebDriverWait(driver, 20)

    # 1. Жмем кнопку "Купить"
    buy_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Купить")]')))
    buy_button.click()

    # Ждем фактической готовности формы 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form")))

    return wait


# --- Вспомогательные функции ---
def _save_screenshot(driver, name="error"):
    """Сохраняет скриншот при ошибке."""
    os.makedirs("screenshots", exist_ok=True)
    filename = f"screenshots/screenshot_{name}_{int(time.time())}.png"
    driver.save_screenshot(filename)
    print(f"📸 Скриншот сохранен: {filename}")


--- ТЕСТЫ  ---
def test_payment_with_valid_card(open_payment_form):
    """
    Тест 1: Успешная оплата тура банковской картой.
    Проверяет, что при вводе валидных данных появляется сообщение об одобрении операции.
    """
    wait = open_payment_form
    driver = wait._driver  # Получаем экземпляр WebDriver из фикстуры

    try:
        # --- 1. Заполнение данных держателя карты ---
        # Находим поле CVC (по placeholder), затем поднимаемся к родительскому блоку,
        # чтобы найти связанные поля (Имя, Номер карты) в том же контейнере.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # Вводим имя владельца карты
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        # Вводим CVC/CVV код
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        # --- 2. Заполнение даты действия карты ---
        # Месяц и год обычно находятся вне родительского блока CVC, поэтому ищем их отдельно.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08") # Месяц
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26") # Год

        # --- 3. Заполнение номера карты ---
        # Ищем поле с маской ввода номера карты.
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        # Вводим номер карты
        card_field.send_keys("4444 4444 4444 4441")

        # --- 4. Отправка формы ---
        # Находим кнопку оплаты. *Примечание: абсолютный XPath очень хрупок.*
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        # Прокручиваем страницу к кнопке, чтобы она не была скрыта футером или модальным окном.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- 5. Проверка результата ---
        # Ждем появления всплывающего окна с результатом.
        success_popup = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]")
            )
        )

        popup_text = success_popup.text
        print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

        # Проверяем, что текст уведомления содержит ожидаемую фразу об успехе.
        # Используем lower() для игнорирования регистра букв.
        assert "операция одобрена банком" in popup_text.lower(), \
            f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

        print("✅ ТЕСТ ПРОЙДЕН: Операция успешно одобрена.")

    except Exception as e:
        _save_screenshot(driver, name="invalid_card_test") # Сохраняем скриншот для анализа ошибки.
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_purchase_tour_with_credit_approval(open_payment_form):
    """
    Тест 2: Успешное одобрение кредита при покупке тура.
    Проверяет сценарий покупки в кредит, где банк одобряет заявку.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- 1. Выбор способа оплаты "В кредит" ---
        # Находим и нажимаем кнопку "Купить в кредит".
        credit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/button[2]')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_btn)
        credit_btn.click()

        # --- 2. Заполнение формы данными карты ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4441") # Валидный номер карты

        # --- 3. Отправка заявки на кредит ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- 4. Проверка результата ---
        success_popup = wait.until(
             EC.visibility_of_element_located(
                 (By.XPATH, "/html/body/div/div/div[2]/div[3]")
             )
         )
        popup_text = success_popup.text
        print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

        assert "операция одобрена банком" in popup_text.lower(), \
             f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

        print("✅ ТЕСТ ПРОЙДЕН: Кредит успешно одобрен.")

    except Exception as e:
         _save_screenshot(driver, name="credit_approval_test")
         print(f"⚠️ Ошибка в тесте: {e}")
         raise

# --- Негативные (ошибочные) сценарии: ---
def test_payment_with_invalid_card_declined(open_payment_form):
    """Тест 3: Оплата тура с невалидной картой (статус DECLINED)
    Проверяет корректную обработку отказа банка при попытке оплаты.
    """
    wait = open_payment_form
    driver = wait._driver  # Получаем драйвер из фикстуры для прямого взаимодействия

    try:
        # --- Заполнение данных держателя карты ---
        # Находим поле CVC по его placeholder. Это стабильный якорь.
        # От этого элемента поднимаемся к родительскому контейнеру,
        # чтобы найти связанные поля (Имя, Номер карты) в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # Вводим имя владельца карты и CVC/CVV код в найденных полях.
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        # --- Заполнение даты действия карты ---
        # Поля месяца и года находятся вне родительского блока CVC, ищем их по placeholder.
        # '08' — месяц (август), '26' — год (2026).
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        # --- Заполнение номера карты ---
        # Ищем поле с маской ввода номера карты по его placeholder.
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        # Вводим тестовый номер карты, который платежная система настроена отклонять (статус DECLINED).
        card_field.send_keys("4444 4444 4444 4442")

        # --- Отправка формы ---
        # Находим кнопку оплаты. *Примечание: абсолютный XPath очень хрупок и может сломаться при любом изменении верстки.*
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        # Прокручиваем страницу к кнопке, чтобы она попала в видимую область браузера.
        # Это гарантирует, что клик сработает корректно.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата (ОЖИДАЕМАЯ НЕУДАЧА) ---
        # Ждем появления всплывающего окна с ошибкой.
        # Использование CSS-селектора ".notification__content" более надежно, чем XPath,
        # так как он ищет по классу элемента, который с меньшей вероятностью изменится.
        error_popup = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".notification__content")
            )
        )

        # Извлекаем текст из элемента ошибки для проверки.
        popup_text = error_popup.text
        print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

        # Проверяем, что текст уведомления содержит ожидаемую фразу об отказе банка.
        # Метод .lower() используется для игнорирования регистра букв в сообщении.
        assert "ошибка! банк отказал в проведении операции" in popup_text.lower(), \
            f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

        print("✅ ТЕСТ ПРОЙДЕН: Успешно обработан отказ банка.")

    except Exception as e:
        # В случае возникновения ошибки сохраняем скриншот страницы.
        # Это поможет визуально проанализировать состояние интерфейса в момент сбоя.
        _save_screenshot(driver, name="invalid_card_declined_test")
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_empty_expiry_year(open_payment_form):
    """Тест 4: Оплата с просроченной картой
    Проверяет валидацию на стороне фронтенда при вводе даты истечения срока действия карты в прошлом.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя карты ---
        # Находим поле CVC по его placeholder. Это стабильный якорь.
        # От этого элемента поднимаемся к родительскому контейнеру,
        # чтобы найти связанные поля (Имя, Номер карты) в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # Вводим данные владельца и CVV в найденных полях.
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("IVAN IVANOV")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Заполнение даты действия карты ---
        # Вводим месяц и год. Год '19' (2019) является просроченным.
        # Тест ожидает, что фронтенд (или валидатор) не даст отправить форму.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("01")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("19")

        # --- Заполнение номера карты ---
        # Ищем поле с маской ввода номера карты по его placeholder.
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        # Вводим валидный тестовый номер карты.
        card_field.send_keys("4444 4444 4444 4441")

        # --- Отправка формы ---
        # Находим кнопку оплаты. *Примечание: абсолютный XPath очень хрупок.*
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        # Прокручиваем страницу к кнопке для корректного срабатывания клика.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата (ОЖИДАЕМАЯ ОШИБКА ВАЛИДАЦИИ) ---
        # Ждем появления сообщения об ошибке.
        # Локатор ищет элемент <span>, который является следующим соседом (following-sibling)
        # и содержит текст 'Неверный формат'.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Истёк срок действия карты')]"))
            )

        # Проверяем, что элемент с ошибкой действительно отображается на странице.
        assert err.is_displayed(), "Ошибка 'Истёк срок действия карты' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот для анализа.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_invalid_cvc_format(open_payment_form):
    """№5. Оплата с неверным CVV-кодом
    Проверяет валидацию поля CVV/CVC. Вводится некорректное значение (например, '000'),
    чтобы убедиться, что система блокирует отправку формы и показывает ошибку.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # 1. Находим якорь для блока CVV и родительский контейнер
        # Используем поле с placeholder '999' как стабильную точку входа.
        # Затем поднимаемся к родительскому div, чтобы найти связанные поля (Имя владельца).
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 2. Заполняем поле владельца карты (находится в том же родительском блоке)
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")

        # 3. Вводим некорректное значение в поле CVV (неверный формат/значение)
        # В данном случае вводится '000'. Для многих платежных систем это недопустимый код.
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("000")

        # 4. Заполняем остальные поля корректными данными, чтобы изолировать проблему
        # Месяц и год действия карты.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        # Номер карты (тестовый валидный номер).
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # 5. Отправляем форму
        # Находим кнопку оплаты. *Примечание: абсолютный XPath очень хрупок.*
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        # Прокручиваем страницу к кнопке, чтобы она попала в видимую область.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # 6. Проверяем, что отображается ошибка о неверном формате
        # Ждем появления сообщения об ошибке.
        # Локатор ищет элемент <span>, который является следующим соседом (following-sibling)
        # и содержит текст 'Неверный формат'.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
            )

        # Проверяем, что элемент с ошибкой виден на странице.
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот страницы для отладки.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise


def test_empty_expiry_month(open_payment_form):
    """Тест 6: Оплата с пустым месяцем
    Проверяет валидацию поля 'Месяц истечения срока действия карты'.
    Тест имитирует ситуацию, когда пользователь оставляет это поле пустым.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        # Находим поле CVC по его placeholder и поднимаемся к родительскому контейнеру,
        # чтобы заполнить имя владельца в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Ввод данных срока действия ---
        # 1. Оставляем поле месяца пустым (send_keys("")).
        # 2. Заполняем поле года корректным значением.
        # Это позволяет проверить, что валидация срабатывает именно на пустое значение месяца.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        # --- Заполнение номера карты ---
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ждем появления сообщения об ошибке валидации.
        # Локатор ищет элемент <span>, который является следующим соседом (following-sibling)
        # и содержит текст 'Неверный формат'.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )

        # Проверяем, что сообщение об ошибке действительно отображается на странице.
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот для анализа состояния страницы.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise


def test_empty_year(open_payment_form):
    """Тест 7: Оплата с пустым годом
    Проверяет валидацию поля 'Год истечения срока действия карты'.
    Тест имитирует ситуацию, когда пользователь оставляет это поле пустым.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        # Находим поле CVC по его placeholder и поднимаемся к родительскому контейнеру,
        # чтобы заполнить имя владельца в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # Вводим данные владельца и CVV в найденных полях.
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("IVAN IVANOV")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Ввод данных срока действия ---
        # 1. Заполняем поле месяца корректным значением.
        # 2. Оставляем поле года пустым (send_keys("")).
        # Это позволяет изолировать проверку на обязательное заполнение поля 'Год'.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("01")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("")

        # --- Заполнение номера карты ---
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4441")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        # Прокручиваем страницу к кнопке, чтобы она попала в видимую область браузера.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ждем появления сообщения об ошибке валидации.
        # Локатор ищет элемент <span>, который является следующим соседом (following-sibling)
        # и содержит текст 'Неверный формат'.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )

        # Проверяем, что сообщение об ошибке действительно отображается на странице.
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот для анализа состояния страницы в момент сбоя.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise


def test_invalid_cardholder_name(open_payment_form):
    """Тест: №8. Оплата с пустым полем «Владелец»
    Проверяет валидацию обязательного поля 'Имя владельца карты'.
    Тест имитирует ситуацию, когда пользователь оставляет это поле пустым.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- НАХОДИМ ЭЛЕМЕНТЫ В СТРУКТУРЕ SHADOW DOM ---
        # 1. Ищем "якорь" по известному полю (CVC), чтобы получить стабильную точку входа.
        #    Это поле находится в том же компоненте, что и поле имени.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))

        # 2. Находим родительский контейнер, который инкапсулирует поля (Shadow DOM).
        #    Это позволяет нам работать с внутренними элементами компонента.
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 3. Ищем поле имени внутри этого блока.
        #    Используем селектор по классу для поиска конкретного input'а.
        name_field = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")

        # --- ЗАПОЛНЕНИЕ ФОРМЫ ---
        # Оставляем поле имени владельца пустым (основное действие теста).
        name_field.send_keys("")

        # Заполняем остальные поля корректными данными, чтобы изолировать ошибку.
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")  # CVV

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")  # Месяц
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")  # Год

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")  # Номер карты

        # --- ОТПРАВКА ФОРМЫ ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- ПРОВЕРКА ОШИБКИ ---
        # Ошибка валидации должна появиться рядом с полем имени.
        # Ищем её в том же родительском блоке, где находится пустое поле.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
        )

        assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_empty_cvc_field(open_payment_form):
    """Тест 9: Оплата с незаполненным полем CVV"""
    wait = open_payment_form
    driver = wait._driver

    try:
        # Находим якорь и родительский блок для CVV
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 1. Заполняем поле владельца (в том же блоке)
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")

        # 2. НЕ ВВОДИМ НИЧЕГО в поле CVВ (пропускаем этот шаг)

        # 3. Заполняем остальные поля (срок действия и номер карты)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # Отправляем форму
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # Проверяем ошибку рядом с полем CVV
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_empty_card_number(open_payment_form):
    """Тест 10: Пустой номер карты
    Проверяет валидацию обязательного поля 'Номер карты'.
    Тест имитирует попытку отправки формы с незаполненным полем номера.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя, CVV и срока действия ---
        # Находим якорный элемент (CVC) и его родительский контейнер,
        # чтобы заполнить имя и CVV в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        # Заполняем поля срока действия карты корректными данными.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("12")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("35")

        # --- Оставляем поле номера карты пустым ---
        # Находим поле для ввода номера карты.
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        # Вводим пустую строку. Это основное действие теста.
        card_field.send_keys("")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ожидаем появление сообщения об ошибке валидации.
        # Локатор ищет элемент <span>, который является соседом и содержит текст ошибки.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
            )

        # Проверяем, что сообщение об ошибке действительно отображается на странице.
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот для отладки.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_card_number_with_letter(open_payment_form):
    """Тест 11: Номер карты с буквой
    Проверяет валидацию поля 'Номер карты' на ввод некорректных символов.
    Тест имитирует ввод буквенного символа в поле, предназначенное только для цифр.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        # Находим поле CVC по его placeholder и поднимаемся к родительскому контейнеру,
        # чтобы заполнить имя владельца в том же блоке формы.
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        # --- Заполнение срока действия карты ---
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='12']"))).send_keys("12") # Месяц
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='35']"))).send_keys("35") # Год

        # --- Ввод некорректного номера карты ---
        # Находим поле для ввода номера карты.
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        # Вводим номер карты, содержащий букву 'A'.
        # Это некорректный формат, который должен быть заблокирован валидацией.
        card_field.send_keys("4444 4444 4444 44A1")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ожидаем появление сообщения об ошибке валидации.
        # Локатор ищет элемент <span>, который является соседом и содержит текст ошибки.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
            )

        # Проверяем, что сообщение об ошибке действительно отображается на странице.
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        # В случае ошибки сохраняем скриншот для анализа состояния страницы.
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_month_with_invalid_format(open_payment_form):
    """Тест 12: Месяц с неверным форматом, буквы вместо цифр"""
    wait = open_payment_form
    driver = wait._driver

    try:
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # Вводим буквы в поле месяца (например, 'AB')
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("AB")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_expiry_year_with_non_numeric(open_payment_form):
    """№13. Оплата с годом, содержащим неверный формат
    Проверяет валидацию поля 'Год истечения срока действия карты'.
    Тест имитирует ввод нецифровых символов ('XY') вместо ожидаемых цифр.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("IVAN IVANOV")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Ввод данных срока действия ---
        # 1. Месяц заполняем корректным значением.
        # 2. Год заполняем некорректным значением ('XY'), чтобы проверить валидацию на стороне фронтенда.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("01")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("XY")

        # --- Заполнение номера карты ---
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4441")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ожидаем появление сообщения об ошибке валидации из-за неверного формата года.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
            )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_cvc_with_non_numeric(open_payment_form):
    """Тест 14: Оплата с CVV, содержащим неверный формат (буквы вместо цифр)"""
    wait = open_payment_form
    driver = wait._driver

    try:
        # 1. Находим якорь для блока CVV и родительский контейнер (Shadow DOM)
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 2. Заполняем поле владельца (находится в том же блоке)
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")

        # 3. Вводим буквы в поле CVV (неверный формат)
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("ABC")

        # 4. Заполняем остальные поля корректными данными
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # 5. Отправляем форму
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # 6. Проверяем, что отображается ошибка о неверном формате
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_cardholder_name_with_numeric(open_payment_form):
    """Тест 15: Оплата с именем владельца, содержащим неверный формат (только цифры)"""
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- НАХОДИМ ЭЛЕМЕНТ SHADOW DOM ---
        # 1. Ищем "якорь" по известному полю (например, CVC)
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))

        # 2. Находим родительский блок, который содержит Shadow DOM
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 3. Ищем поле имени внутри этого блока (оно имеет класс input__control)
        #    Используем JS, чтобы пробраться внутрь Shadow DOM
        name_field = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")

        # --- ЗАПОЛНЕНИЕ ФОРМЫ ---
        name_field.send_keys("1234567890")  # Вводим цифры в имя владельца

        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # --- ОТПРАВКА ФОРМЫ ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- ПРОВЕРКА ОШИБКИ ---
        # Ошибка может появиться рядом с полем имени. Ищем её в том же родительском блоке.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
        )

        assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_month_with_spaces(open_payment_form):
    """№16. Оплата с месяцем, содержащим пробелы
    Проверяет валидацию поля 'Месяц истечения срока действия карты'.
    Тест имитирует ввод некорректного значения — одиночного пробела.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Ввод данных срока действия ---
        # 1. В поле месяца вводим некорректное значение — пробел (" ").
        # 2. Год заполняем корректным значением, чтобы изолировать проверку на поле месяца.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys(" ")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        # --- Заполнение номера карты ---
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ожидаем появление сообщения об ошибке валидации из-за неверного формата месяца.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
            )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_expiry_year_with_space(open_payment_form):
    """№17. Оплата с годом, содержащим пробелы
    Проверяет валидацию поля 'Год истечения срока действия карты'.
    Тест имитирует ввод некорректного значения — одиночного пробела.
    """
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- Заполнение данных держателя и CVV ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("IVAN IVANOV")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("999")

        # --- Ввод данных срока действия ---
        # 1. Месяц заполняем корректным значением ('01').
        # 2. Год заполняем некорректным значением (пробел), чтобы проверить валидацию на стороне фронтенда.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("01")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys(" ")

        # --- Заполнение номера карты ---
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4441")

        # --- Отправка формы ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- Проверка результата ---
        # Ожидаем появление сообщения об ошибке валидации из-за неверного формата года.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
def test_cvc_field_with_space(open_payment_form):
    """Тест №18. Оплата с CVV, содержащим пробелы"""
    wait = open_payment_form
    driver = wait._driver

    try:
        # Находим якорь и родительский блок для CVV
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 1. Заполняем поле владельца (в том же блоке)
        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("Ivan Ivanov")

        # 2. Вводим ПРОБЕЛ в поле CVV
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys(" ")

        # 3. Заполняем остальные поля (срок действия и номер карты)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # Отправляем форму
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # Проверяем ошибку рядом с полем CVV
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Неверный формат')]"))
        )
        assert err.is_displayed(), "Ошибка 'Неверный формат' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_name_with_spaces(open_payment_form):
    """Тест 19: Оплата с именем владельца, содержащим пробелы"""
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- НАХОДИМ ЭЛЕМЕНТ SHADOW DOM ---
        # 1. Ищем "якорь" по известному полю (например, CVC)
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))

        # 2. Находим родительский блок, который содержит Shadow DOM
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        # 3. Ищем поле имени внутри этого блока (оно имеет класс input__control)
        #    Используем JS, чтобы пробраться внутрь Shadow DOM
        name_field = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")

        # --- ЗАПОЛНЕНИЕ ФОРМЫ ---
        name_field.send_keys("  ")  # Вводим цифры в имя владельца

        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4444")

        # --- ОТПРАВКА ФОРМЫ ---
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # --- ПРОВЕРКА ОШИБКИ ---
        # Ошибка может появиться рядом с полем имени. Ищем её в том же родительском блоке.
        err = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//following-sibling::span[contains(text(), 'Поле обязательно для заполнения')]"))
        )

        assert err.is_displayed(), "Ошибка 'Поле обязательно для заполнения' не отображается"

    except Exception as e:
        _save_screenshot(driver)
        print(f"⚠️ Ошибка в тесте: {e}")
        raise

def test_payment_long_name(open_payment_form):
    """Тест 20: Оплата тура валидной картой с длинным именем владельца """
    wait = open_payment_form
    driver = wait._driver  # Получаем драйвер из фикстуры (внутренний доступ)

    try:
        # --- Ваш код для заполнения формы ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        parent_block.find_element(By.CSS_SELECTOR, "input.input__control").send_keys("IVAN IVANOV IVAN IVANOV IVAN IVANOV")
        parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']").send_keys("123")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']"))).send_keys("08")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']"))).send_keys("26")

        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))
        card_field.send_keys("4444 4444 4444 4441")  # Слишком короткий номер

        btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/fieldset/div[4]/button')))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()
        # --- 4. Проверка ОЖИДАЕМОГО РЕЗУЛЬТАТА ---

        # Ждем появления всплывающего окна по абсолютному XPath
        success_popup = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div[3]")
            )
        )

        # Получаем текст из элемента
        popup_text = success_popup.text
        print(f"\n📝 Текст всплывающего окна: '{popup_text}'")

        # Проверяем, что текст содержит ожидаемую фразу
        assert "операция одобрена банком" in popup_text.lower(), \
            f"Тест провален! Окно появилось, но текст не совпадает. Фактический текст: '{popup_text}'"

        print("✅ ТЕСТ ПРОЙДЕН: Операция успешно одобрена.")
    except Exception as e:
        _save_screenshot(driver, name="invalid_card_test")
        print(f"⚠️ Ошибка в тесте: {e}")
        raise



def test_clear_payment_form_fields(open_payment_form):
    """№21. Проверка работы функции очистки полей формы оплаты

    Тестовые данные: Произвольные некорректные данные для заполнения формы.
    Шаг 1: Заполнить все поля формы оплаты некорректными данными.
    Шаг 2: Очистить КАЖДОЕ поле формы с помощью многократного нажатия Backspace.
    Шаг 3: Проверить состояние всех полей после очистки.
    Ожидаемый результат: Все поля формы оказываются пустыми.
    """
    from selenium.webdriver.common.keys import Keys
    wait = open_payment_form
    driver = wait._driver

    try:
        # --- НАХОДИМ ЭЛЕМЕНТЫ ФОРМЫ ---
        cvc_anchor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='999']")))
        parent_block = cvc_anchor.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]")

        name_field = parent_block.find_element(By.CSS_SELECTOR, "input.input__control")
        cvv_field = parent_block.find_element(By.CSS_SELECTOR, "input[placeholder='999']")
        month_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='08']")))
        year_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='22']")))
        card_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.input__control[placeholder='0000 0000 0000 0000']")))

        # --- ШАГ 1: ЗАПОЛНЕНИЕ ПОЛЕЙ НЕВАЛИДНЫМИ ДАННЫМИ ---
        name_field.send_keys("%$#@")  # Имя владельца
        cvv_field.send_keys("000")  # CVV
        month_field.send_keys("13")  # Месяц
        year_field.send_keys("20")  # Год
        card_field.send_keys("1234 5678 9012 3456")  # Номер карты

        # Небольшая пауза, чтобы убедиться во вводе данных
        time.sleep(1)

        # --- ШАГ 2: ИСПОЛЬЗОВАНИЕ ФУНКЦИИ ОЧИСТКИ (СИМУЛЯЦИЯ BACKSPACE) ДЛЯ КАЖДОГО ПОЛЯ ---

        def clear_input_by_backspace(element):
            """Вспомогательная функция для очистки одного input-элемента."""
            element.click()
            # Получаем текущую длину значения с помощью JS, это надежно
            current_length = driver.execute_script("return arguments[0].value.length;", element)
            for _ in range(current_length):
                element.send_keys(Keys.BACK_SPACE)

        # Применяем функцию очистки ко всем полям
        clear_input_by_backspace(name_field)
        clear_input_by_backspace(cvv_field)
        clear_input_by_backspace(month_field)
        clear_input_by_backspace(year_field)
        clear_input_by_backspace(card_field)

        # Небольшая пауза после очистки
        time.sleep(1)

        # --- ШАГ 3: ПРОВЕРКА РЕЗУЛЬТАТА ---
        assert name_field.get_attribute('value') == "", f"Поле 'Имя владельца' не очищено."
        assert cvv_field.get_attribute('value') == "", f"Поле 'CVV' не очищено."
        assert month_field.get_attribute('value') == "", f"Поле 'Месяц' не очищено."
        assert year_field.get_attribute('value') == "", f"Поле 'Год' не очищено."
        assert card_field.get_attribute('value') == "", f"Поле 'Номер карты' не очищено."

        print("✅ ТЕСТ ПРОЙДЕН: Функция очистки полей работает корректно. Все поля пусты.")

    except Exception as e:
        _save_screenshot(driver, name="clear_form_test")
        print(f"⚠️ Ошибка в тесте: {e}")
        raise
