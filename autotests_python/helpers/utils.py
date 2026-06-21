

import os
import datetime
import logging
from typing import Any, List

# --- НАСТРОЙКА ЛОГГЕРА ---
# Создаем логгер с осмысленным именем
logger = logging.getLogger('test_automation')
logger.setLevel(logging.DEBUG)  # Логгер будет ловить все сообщения уровня DEBUG и выше

# 1. Обработчик для записи в файл (полная история)
log_filename = f"test_run_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)  # В файл пишем всё: от DEBUG до CRITICAL

# 2. Обработчик для вывода в консоль (только важное)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # В консоль выводим только INFO и ошибки (ERROR, CRITICAL)

# Создаем форматтер и добавляем его к обоим обработчикам
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру, если их еще нет
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# --- УТИЛИТЫ ДЛЯ РАБОТЫ С ФАЙЛАМИ И СКРИНШОТАМИ ---

def save_screenshot(driver, name="error"):
    """
    Сохраняет скриншот в папку 'screenshots' и логирует действие.
    """
    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)
        logger.debug(f"Создана папка для скриншотов: {folder}")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{name}_{timestamp}.png"
    path = os.path.join(folder, filename)

    try:
        driver.save_screenshot(path)
        logger.info(f"Скриншот сохранен: {path}")
        return path
    except Exception as e:
        logger.error(f"Не удалось сохранить скриншот. Ошибка: {e}")
        return None


# --- МОДУЛЬ ДЛЯ АССЕРТОВ (assert) ---

def assert_that(condition: bool, message: str = "") -> None:
    """
    Базовая функция для проверки условия.
    Логирует результат (успех или провал) и вызывает стандартный assert.
    """
    if condition:
        logger.info(f"[УСПЕХ] {message}")
    else:
        logger.error(f"[ОШИБКА] {message}")
    assert condition, message


def assert_element_text_contains(element: Any, expected_text: str, error_message: str = "") -> None:
    """
    Проверяет, что текст элемента содержит ожидаемый текст.
    """
    actual_text = element.text
    condition = expected_text in actual_text

    # Формируем информативное сообщение для лога и assert-а
    # Используем параметр error_message, который передается из теста
    full_error_message = (
        f"{error_message}. "
        f"Ожидалось, что текст содержит: '{expected_text}'. "
        f"Фактический текст элемента: '{actual_text}'"
    )

    assert_that(condition, full_error_message)

def print(*args, sep=' ', end='\n'):
    """
    Временная функция для перехвата вызовов print() и их перенаправления в логгер.
    """
    message = sep.join(map(str, args)) + end
    logger.info(message.strip())
