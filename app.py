import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from playwright.async_api import async_playwright

from keyboards import (
    main_menu, banks_menu, products_menu,
    subscriptions_menu, unsubscribe_menu, refinance_menu,
    admin_menu
)
from database import (
    init_db, add_subscription, get_user_subscriptions,
    get_user_subscriptions_with_id, delete_subscription_by_id, add_request,
    check_subscription_exists, get_unique_products, get_subscribers,
    get_current_rate, update_rate_for_all, get_all_subscriptions, get_stats
)
from products import BANKS
from products_map import PRODUCTS_MAP

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 232443634
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "credit-storozh-secret-2026"

RENDER_URL = "https://credit-storozh-bot.onrender.com"

REFINANCE_URL = "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b"
REFINANCE_SELECTOR = "table tr:nth-child(2) td:nth-child(2)"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ ПОЛУЧЕНИЕ СТАВКИ ============

async def get_rate_from_site(url, selector):
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
            return ", ".join(values) if values else None
        except Exception as e:
            print(f"Ошибка получения ставки: {e}")
            await browser.close()
            return None

# ============ ЕЖЕДНЕВНАЯ ПРОВЕРКА ============

async def daily_check():
    while True:
        try:
            await asyncio.sleep(24 * 3600)
            print("=== Ежедневная проверка ===")
            unique = get_unique_products()
            for bank, product in unique:
                key = (bank, product)
                if key not in PRODUCTS_MAP:
                    continue
                url, selector = PRODUCTS_MAP[key]
                new_rate = await get_rate_from_site(url, selector)
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

# ============ ХЕНДЛЕРЫ ============

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

@dp.callback_query(F.data == "choose_bank")
async def choose_bank(callback: CallbackQuery):
    await callback.message.edit_text(
        "👇 <b>Выбери банк:</b>",
        reply_markup=banks_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    is_admin = (callback.from_user.id == ADMIN_ID)
    await callback.message.edit_text(
        "👋 <b>Привет! Я — Кредитный Сторож.</b> 🏦\n\n"
        "Выбери действие:",
        reply_markup=main_menu(is_admin=is_admin),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "my_subs")
async def my_subs(callback: CallbackQuery):
    subs = get_user_subscriptions(callback.from_user.id)
    if not subs:
        await callback.message.edit_text(
            "😔 <b>У тебя пока нет подписок.</b>\n\n"
            "Выбери банк, чтобы подписаться:",
            reply_markup=banks_menu(),
            parse_mode="HTML"
        )
    else:
        text = "📌 <b>Твои подписки:</b> 😊\n\n"
        for i, (bank, product, rate) in enumerate(subs, 1):
            text += f"{i}. {bank} — «{product}» ({rate})\n"
        await callback.message.edit_text(text, reply_markup=subscriptions_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "unsubscribe")
async def unsubscribe(callback: CallbackQuery):
    subs = get_user_subscriptions_with_id(callback.from_user.id)
    if not subs:
        await callback.message.edit_text("😔 <b>У тебя пока нет подписок.</b>", reply_markup=main_menu(), parse_mode="HTML")
        return
    await callback.message.edit_text(
        "❌ <b>Выбери, от чего отписаться:</b>",
        reply_markup=unsubscribe_menu(subs),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("unsub_"))
async def do_unsubscribe(callback: CallbackQuery):
    sub_id = int(callback.data.replace("unsub_", ""))
    delete_subscription_by_id(sub_id, callback.from_user.id)
    await callback.message.edit_text("✅ <b>Ты отписан!</b>", reply_markup=main_menu(), parse_mode="HTML")

@dp.callback_query(F.data.startswith("bank_"))
async def bank_selected(callback: CallbackQuery):
    bank_id = callback.data.replace("bank_", "")
    bank = BANKS.get(bank_id)
    if not bank:
        await callback.answer("Банк не найден")
        return
    await callback.message.edit_text(
        f"💳 <b>Кредиты {bank['name']}:</b>",
        reply_markup=products_menu(bank_id),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("prod_"))
async def product_selected(callback: CallbackQuery):
    parts = callback.data.split("_")
    bank_id = parts[1]
    prod_id = "_".join(parts[2:])
    bank = BANKS.get(bank_id)
    product = bank["products"].get(prod_id) if bank else None
    if not product:
        await callback.answer("Кредит не найден")
        return

    if check_subscription_exists(callback.from_user.id, bank["name"], product["name"]):
        await callback.answer("⚠️ Ты уже подписан на этот кредит!", show_alert=True)
        return

    await callback.message.edit_text("⏳ Получаю актуальную ставку...")
    rate = await get_rate_from_site(product["url"], product["selector"]) or "не удалось получить"

    add_subscription(
        callback.from_user.id,
        callback.from_user.username,
        bank["name"],
        product["name"],
        rate
    )
    await callback.message.edit_text(
        f"✅ <b>Ты подписан!</b>\n\n"
        f"Банк: {bank['name']}\n"
        f"Кредит: «{product['name']}»\n"
        f"Текущая ставка: <b>{rate}</b>\n\n"
        f"Я буду следить за изменениями и сообщу, если что-то поменяется.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ <b>Помощь</b>\n\n"
        "Я — <b>Кредитный Сторож</b>. Слежу за ставками по кредитам в банках РБ.\n\n"
        "<b>Что я умею:</b>\n"
        "• 📋 Выбрать банк — подписаться на кредит\n"
        "• 📌 Мои подписки — посмотреть и отписаться\n"
        "• 📊 Ставка рефинансирования — следить за НБРБ\n"
        "• 📝 Нет моего банка/кредита — отправить заявку админу\n\n"
        "<b>Как это работает:</b>\n"
        "Ты выбираешь кредит. Я каждый день в <b>12:00 по Минску</b> проверяю ставку на сайте банка. "
        "Если она изменится — пришлю уведомление.\n\n"
        "<i>🔒 Все данные берутся только из открытых источников — "
        "публичных страниц банков, которые они сами показывают своим клиентам. "
        "Я не нарушаю авторские права и не собираю персональные данные.</i>\n\n"
        "<i>По вопросам: @pyppinator</i>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "refinance")
async def refinance_handler(callback: CallbackQuery):
    await callback.message.edit_text("⏳ Получаю актуальную ставку рефинансирования...")
    rate = await get_rate_from_site(REFINANCE_URL, REFINANCE_SELECTOR) or "не удалось получить"
    await callback.message.edit_text(
        f"📊 <b>Ставка рефинансирования НБРБ</b>\n\n"
        f"Текущее значение: <b>{rate}%</b>\n\n"
        f"Этот показатель важен для многих кредитов — если он изменится, я сообщу.",
        reply_markup=refinance_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "refinance_subscribe")
async def refinance_subscribe(callback: CallbackQuery):
    if check_subscription_exists(callback.from_user.id, "НБРБ", "Ставка рефинансирования"):
        await callback.answer("⚠️ Ты уже подписан на ставку рефинансирования!", show_alert=True)
        return
    await callback.message.edit_text("⏳ Получаю актуальную ставку...")
    rate = await get_rate_from_site(REFINANCE_URL, REFINANCE_SELECTOR) or "не удалось получить"
    add_subscription(callback.from_user.id, callback.from_user.username, "НБРБ", "Ставка рефинансирования", rate)
    await callback.message.edit_text(
        f"✅ <b>Ты подписан на уведомления об изменении ставки рефинансирования НБРБ.</b>\n\n"
        f"Текущая ставка: <b>{rate}%</b>\n\n"
        f"Если ставка изменится, я сообщу.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "no_bank")
async def no_bank(callback: CallbackQuery):
    await callback.message.edit_text(
        "📝 <b>Напиши, какой банк ты хочешь добавить.</b>\n\nНапример: <i>Банк Дабрабыт</i>\n\nЯ передам твоё сообщение администратору.",
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "no_product")
async def no_product(callback: CallbackQuery):
    await callback.message.edit_text(
        "📝 <b>Напиши, какой кредит ты хочешь добавить.</b>\n\nНапример: <i>Кредит «На всё про всё» в Технобанке</i>\n\nЯ передам твоё сообщение администратору.",
        parse_mode="HTML"
    )

# ============ АДМИН-ПАНЕЛЬ ============

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        "🔐 <b>Админ-панель</b>\n\n"
        "Здесь ты можешь посмотреть статистику и всех подписчиков.",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "admin_subs")
async def admin_subs_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    stats = get_stats()
    text = "📊 <b>Статистика Кредитного Сторожа</b>\n\n"
    text += f"👥 Уникальных пользователей: <b>{stats['total_users']}</b>\n"
    text += f"📌 Всего подписок: <b>{stats['total_subs']}</b>\n"
    text += f"🕐 Последняя подписка: <b>{stats['last_sub'][:16].replace('T', ' ') if stats['last_sub'] else '—'}</b>\n\n"

    if stats['top_products']:
        text += "🔥 <b>Топ-5 популярных кредитов:</b>\n"
        for i, (bank, product, cnt) in enumerate(stats['top_products'], 1):
            text += f"{i}. {bank} — «{product}» — <b>{cnt}</b> подп.\n"
        text += "\n"

    if stats['bank_stats']:
        text += "🏦 <b>Подписки по банкам:</b>\n"
        for bank, cnt in stats['bank_stats']:
            text += f"• {bank}: <b>{cnt}</b>\n"
        text += "\n"

    subs = get_all_subscriptions()
    if subs:
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += f"📋 <b>Все подписки ({len(subs)}):</b>\n\n"
        for i, (user_id, username, bank, product, rate, created_at) in enumerate(subs, 1):
            date = created_at[:16].replace("T", " ") if created_at else "—"
            user = f"@{username}" if username else f"id{user_id}"
            text += (
                f"<b>{i}. {user}</b>\n"
                f"   🆔 <code>{user_id}</code>\n"
                f"   🏦 {bank}\n"
                f"   💳 «{product}»\n"
                f"   📈 Ставка: <b>{rate}</b>\n"
                f"   📅 {date}\n\n"
            )

    if len(text) > 4000:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            await callback.message.answer(part, parse_mode="HTML")
    else:
        await callback.message.edit_text(text, reply_markup=main_menu(is_admin=True), parse_mode="HTML")

# ============ ЗАЯВКИ ============

@dp.message()
async def handle_request(message: Message):
    user = message.from_user
    text = message.text
    add_request(user.id, user.username, text)
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новая заявка!</b>\n\nОт: @{user.username or 'без username'} (ID: {user.id})\nТекст: <i>{text}</i>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    await message.answer("✅ <b>Спасибо! Твоя заявка отправлена.</b>\n\nЯ передал её администратору. Как только добавлю — сообщу.", parse_mode="HTML")

# ============ WEBHOOK ============

async def on_startup(app):
    webhook_url = f"{RENDER_URL}{WEBHOOK_PATH}"
    print(f"Устанавливаю webhook: {webhook_url}")
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET, drop_pending_updates=True)
    print("Webhook установлен!")
    asyncio.create_task(daily_check())
    print("Ежедневная проверка запущена!")

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
    webhook_url = f"{RENDER_URL}{WEBHOOK_PATH}"
    asyncio.run(bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET, drop_pending_updates=True))
    print(f"Webhook установлен: {webhook_url}")
    
    app = create_webhook_app()
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))