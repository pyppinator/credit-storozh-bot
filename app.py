import asyncio
import os
import sys
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from keyboards import (
    main_menu, banks_menu, bank_menu, category_menu, group_menu,
    subscriptions_menu, unsubscribe_menu, refinance_menu,
    admin_menu, top_products_menu
)
from database import (
    init_db, add_subscription, get_user_subscriptions,
    get_user_subscriptions_with_id, delete_subscription_by_id, add_request,
    check_subscription_exists, get_rate_from_db, get_all_subscriptions, get_stats,
    get_grouped_subscriptions, delete_all_user_subscriptions, get_last_update_time
)
from products import BANKS
from products_map import PRODUCTS_MAP

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 232443634
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "credit-storozh-secret-2026"

RENDER_URL = "https://credit-storozh-bot.onrender.com"
GITHUB_ACTIONS_URL = "https://github.com/pyppinator/credit-storozh-bot/actions/workflows/updater.yml"

REFINANCE_URL = "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b"
REFINANCE_SELECTOR = "table tr:nth-child(2) td:nth-child(2)"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ ХЕНДЛЕРЫ ============
# (все обработчики остаются без изменений — вставь их из предыдущего кода)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    is_admin = (message.from_user.id == ADMIN_ID)
    await message.answer(
        "👋 <b>Привет! Я — Кредитный Сторож.</b> 🏦\n\n"
        "Я слежу за ставками по кредитам в банках РБ.\n\n"
        "Выбери действие:",
        reply_markup=main_menu(is_admin=is_admin),
        parse_mode="HTML"
    )

# ... остальные обработчики ...

# ============ WEBHOOK ============

async def on_startup(app):
    webhook_url = f"{RENDER_URL}{WEBHOOK_PATH}"
    print(f"Устанавливаю webhook: {webhook_url}")
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET, drop_pending_updates=True)
    print("Webhook установлен!")

async def on_shutdown(app):
    await bot.delete_webhook()

async def health_check(request):
    return web.Response(text="OK")

def create_webhook_app():
    app = web.Application()
    app.router.add_get("/health", health_check)
    app.router.add_get("/", health_check)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    init_db()
    
    # УСТАНАВЛИВАЕМ WEBHOOK ДО ЗАПУСКА ПРИЛОЖЕНИЯ
    webhook_url = f"{RENDER_URL}{WEBHOOK_PATH}"
    asyncio.run(bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET, drop_pending_updates=True))
    print(f"Webhook установлен: {webhook_url}")
    
    app = create_webhook_app()
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))