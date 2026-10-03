import asyncio

from database import (
    get_unique_products, get_subscribers,
    get_current_rate, update_rate_for_all
)
from products_map import PRODUCTS_MAP
from scraper import get_rate_from_site


async def daily_check(bot):
    """Раз в день проверяет все ставки и рассылает уведомления"""
    while True:
        try:
            await asyncio.sleep(24 * 3600)
            print("=== Ежедневная проверка ===")
            unique = get_unique_products()
            for bank, product in unique:
                key = (bank, product)
                if key not in PRODUCTS_MAP:
                    continue
                url, selector, action = PRODUCTS_MAP[key]
                new_rate = await get_rate_from_site(url, selector, action)
                if not new_rate:
                    continue
                old_rate = get_current_rate(bank, product)
                if old_rate != new_rate:
                    subscribers = get_subscribers(bank, product)
                    for user_id in subscribers:
                        try:
                            await bot.send_message(
                                user_id,
                                f"🔔 <b>Изменение!</b>\n\n"
                                f"Банк: {bank}\n"
                                f"Кредит: «{product}»\n\n"
                                f"Было: <b>{old_rate}</b>\n"
                                f"Стало: <b>{new_rate}</b>",
                                parse_mode="HTML"
                            )
                        except Exception as e:
                            print(f"Ошибка отправки {user_id}: {e}")
                    update_rate_for_all(bank, product, new_rate)
        except Exception as e:
            print(f"Ошибка в daily_check: {e}")
            await asyncio.sleep(3600)