import asyncio
import os
from aiogram import Bot

from database import init_db, get_pending_changes, clear_pending_changes

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=BOT_TOKEN)


async def send_notifications():
    """Рассылает отложенные уведомления"""
    init_db()
    changes = get_pending_changes()

    if not changes:
        print("=== Нет отложенных уведомлений ===")
        await bot.session.close()
        return

    print(f"=== Найдено уведомлений: {len(changes)} ===")

    sent = 0
    for change_id, user_id, bank, product, old_rate, new_rate in changes:
        try:
            await bot.send_message(
                user_id,
                f"🔔 <b>Изменение ставки!</b>\n\n"
                f"Банк: {bank}\n"
                f"Кредит: «{product}»\n\n"
                f"Было: <b>{old_rate}</b>\n"
                f"Стало: <b>{new_rate}</b>",
                parse_mode="HTML"
            )
            sent += 1
            await asyncio.sleep(0.1)  # чтобы не превысить лимит Telegram
        except Exception as e:
            print(f"  ✗ Ошибка отправки {user_id}: {e}")

    clear_pending_changes()
    print(f"=== Отправлено: {sent}, таблица очищена ===")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(send_notifications())