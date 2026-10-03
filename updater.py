import asyncio
import os
from aiogram import Bot

from database import init_db, get_rate_from_db, update_rate_in_db, get_subscribers, update_rate_for_all
from products_map import PRODUCTS_MAP
from scraper import get_rate_from_site

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

REFINANCE_URL = "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b"
REFINANCE_SELECTOR = "table tr:nth-child(2) td:nth-child(2)"

bot = Bot(token=BOT_TOKEN)


async def update_all_rates():
    """Обходит все продукты по одному и обновляет ставки в БД"""
    init_db()
    print(f"=== Начинаю обход: {len(PRODUCTS_MAP)} продуктов + НБРБ ===")

    updated = 0
    changed = 0

    # === 1. Обход кредитов ===
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
                update_rate_in_db(bank, product, new_rate)
                update_rate_for_all(bank, product, new_rate)
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
                update_rate_in_db(bank, product, new_rate)

            updated += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"  ✗ Ошибка: {type(e).__name__}: {e}")
            updated += 1
            continue

    # === 2. Обход ставки рефинансирования ===
    print(f"[НБРБ] Ставка рефинансирования")
    try:
        new_rate = await get_rate_from_site(REFINANCE_URL, REFINANCE_SELECTOR)
        if new_rate:
            old_rate = get_rate_from_db("НБРБ", "Ставка рефинансирования")
            print(f"  Было: {old_rate}")
            print(f"  Стало: {new_rate}")

            if old_rate != new_rate:
                update_rate_in_db("НБРБ", "Ставка рефинансирования", new_rate)
                update_rate_for_all("НБРБ", "Ставка рефинансирования", new_rate)
                subscribers = get_subscribers("НБРБ", "Ставка рефинансирования")
                for user_id in subscribers:
                    try:
                        await bot.send_message(
                            user_id,
                            f"🔔 <b>Изменение!</b>\n\n"
                            f"НБРБ — Ставка рефинансирования\n\n"
                            f"Было: <b>{old_rate}</b>\n"
                            f"Стало: <b>{new_rate}</b>",
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        print(f"  Ошибка отправки {user_id}: {e}")
                changed += 1
                print(f"  🔔 Изменение! Уведомлено: {len(subscribers)}")
            else:
                update_rate_in_db("НБРБ", "Ставка рефинансирования", new_rate)
        else:
            print(f"  ✗ Не удалось получить")
    except Exception as e:
        print(f"  ✗ Ошибка: {type(e).__name__}: {e}")

    print(f"=== Готово! Обработано: {updated + 1}, изменений: {changed} ===")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(update_all_rates())