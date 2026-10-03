import asyncio
import os
from aiogram import Bot

from database import init_db, get_rate_from_db, update_rate_in_db, get_subscribers, update_rate_for_all
from products_map import PRODUCTS_MAP
from scraper import get_rate_from_site

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=BOT_TOKEN)


async def update_all_rates():
    """Обходит все продукты по одному и обновляет ставки в БД"""
    init_db()
    print(f"=== Начинаю обход: {len(PRODUCTS_MAP)} продуктов ===")

    updated = 0
    changed = 0

    for (bank, product), (url, selector, action) in PRODUCTS_MAP.items():
        try:
            print(f"[{updated+1}/{len(PRODUCTS_MAP)}] {bank} — {product}")
            new_rate = await get_rate_from_site(url, selector, action)

            if not new_rate:
                print(f"  ✗ Не удалось получить")
                updated += 1
                continue

            old_rate = get_rate_from_db(bank, product)
            print(f"  Было: {old_rate}")
            print(f"  Стало: {new_rate}")

            if old_rate != new_rate:
                # Обновляем в БД
                update_rate_in_db(bank, product, new_rate)
                # Обновляем у всех подписчиков
                update_rate_for_all(bank, product, new_rate)
                # Уведомляем подписчиков
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
                        print(f"  Ошибка отправки {user_id}: {e}")
                changed += 1
                print(f"  🔔 Изменение! Уведомлено: {len(subscribers)}")
            else:
                # Даже если не изменилось — обновляем время
                update_rate_in_db(bank, product, new_rate)

            updated += 1
            await asyncio.sleep(1)  # пауза между запросами
        except Exception as e:
            print(f"  ✗ Ошибка: {type(e).__name__}: {e}")
            updated += 1
            continue

    print(f"=== Готово! Обработано: {updated}, изменений: {changed} ===")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(update_all_rates())