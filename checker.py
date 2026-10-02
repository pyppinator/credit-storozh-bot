import asyncio
import logging
from playwright.async_api import async_playwright
from aiogram import Bot

from database import (
    init_db, get_unique_products, get_subscribers,
    get_current_rate, update_rate_for_all
)
from products_map import PRODUCTS_MAP

BOT_TOKEN = "8948549772:AAGz7CmPl4pdsvnX3DObmWKAFpq8ey5n6hc"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)

async def get_rate_from_site(url, selector):
    """Заходит на сайт и возвращает текст всех элементов с селектором"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Accept-Language": "ru-RU,ru;q=0.9"})
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_selector(selector, timeout=15000)
            elements = await page.query_selector_all(selector)
            values = []
            for el in elements:
                text = await el.inner_text()
                values.append(text.strip())
            await browser.close()
            if values:
                return ", ".join(values)
            return None
        except Exception as e:
            print(f"Ошибка получения ставки: {e}")
            await browser.close()
            return None

async def send_notification(user_id, message):
    """Отправляет сообщение пользователю"""
    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        print(f"  → Уведомление отправлено {user_id}")
    except Exception as e:
        print(f"  ✗ Ошибка отправки {user_id}: {e}")

async def check_all():
    """Главная функция: проверяет все уникальные продукты"""
    init_db()
    unique_products = get_unique_products()

    if not unique_products:
        print("Нет подписок для проверки.")
        return

    print(f"Найдено уникальных продуктов: {len(unique_products)}")

    for bank, product in unique_products:
        print(f"\n🔍 Проверяю: {bank} — «{product}»")

        key = (bank, product)
        if key not in PRODUCTS_MAP:
            print(f"  ⚠ Нет URL для этой пары. Пропускаю.")
            continue

        url, selector = PRODUCTS_MAP[key]

        # Получаем актуальную ставку
        new_rate = await get_rate_from_site(url, selector)
        if not new_rate:
            print(f"  ✗ Не удалось получить ставку.")
            continue

        print(f"  Текущая с сайта: {new_rate}")

        # Получаем предыдущую
        old_rate = get_current_rate(bank, product)
        print(f"  Предыдущая: {old_rate}")

        # Сравниваем
        if old_rate != new_rate:
            print(f"  🔔 ИЗМЕНЕНИЕ! Рассылаю уведомления...")

            subscribers = get_subscribers(bank, product)
            print(f"  Подписчиков: {len(subscribers)}")

            for user_id in subscribers:
                message = (
                    f"🔔 <b>Изменение!</b>\n\n"
                    f"Банк: {bank}\n"
                    f"Кредит: «{product}»\n\n"
                    f"Было: <b>{old_rate}</b>\n"
                    f"Стало: <b>{new_rate}</b>"
                )
                await send_notification(user_id, message)

            # Обновляем в базе для всех
            update_rate_for_all(bank, product, new_rate)
            print(f"  ✅ База обновлена.")
        else:
            print(f"  ✓ Без изменений.")

    print("\n=== Проверка завершена ===")

async def main():
    await check_all()
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())