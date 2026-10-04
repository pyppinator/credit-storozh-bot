import asyncio
import os

from database import (
    init_db, get_rate_from_db, update_rate_in_db,
    get_subscribers, update_rate_for_all,
    add_pending_change
)
from products_map import PRODUCTS_MAP
from scraper import get_rate_from_site

REFINANCE_URL = "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b"
REFINANCE_SELECTOR = "table tr:nth-child(2) td:nth-child(2)"


async def update_all_rates():
    """Обходит все продукты, обновляет БД и складывает уведомления в pending_changes"""
    init_db()
    print(f"=== Начинаю обход: {len(PRODUCTS_MAP)} продуктов + НБРБ ===")

    updated = 0
    changed = 0

    for (bank, product), (url, selector, action, column_index) in PRODUCTS_MAP.items():
        try:
            print(f"[{updated+1}/{len(PRODUCTS_MAP)}] {bank} — {product}")
            new_rate = await get_rate_from_site(url, selector, action, column_index)

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
                    add_pending_change(user_id, bank, product, old_rate, new_rate)

                changed += 1
                print(f"  📥 Отложено уведомлений: {len(subscribers)}")
            else:
                update_rate_in_db(bank, product, new_rate)

            updated += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"  ✗ Ошибка: {type(e).__name__}: {e}")
            updated += 1
            continue

    # === Ставка рефинансирования ===
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
                    add_pending_change(user_id, "НБРБ", "Ставка рефинансирования", old_rate, new_rate)

                changed += 1
                print(f"  📥 Отложено уведомлений: {len(subscribers)}")
            else:
                update_rate_in_db("НБРБ", "Ставка рефинансирования", new_rate)
        else:
            print(f"  ✗ Не удалось получить")
    except Exception as e:
        print(f"  ✗ Ошибка: {type(e).__name__}: {e}")

    print(f"=== Готово! Обработано: {updated + 1}, изменений: {changed} ===")


if __name__ == "__main__":
    asyncio.run(update_all_rates())