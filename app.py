import asyncio
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from playwright.async_api import async_playwright

from keyboards import (
    main_menu, banks_menu, products_menu,
    subscriptions_menu, unsubscribe_menu, refinance_menu
)
from database import (
    init_db, add_subscription, get_user_subscriptions,
    get_user_subscriptions_with_id, delete_subscription_by_id, add_request
)
from products import BANKS

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 232443634

REFINANCE_URL = "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b"
REFINANCE_SELECTOR = "table tr:nth-child(2) td:nth-child(2)"

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running"

@app.route("/health")
def health():
    return "OK"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 <b>Привет! Я — Кредитный Сторож.</b> 🏦\n\n"
        "Я слежу за ставками по кредитам в банках РБ.\n\n"
        "Выбери действие:",
        reply_markup=main_menu(),
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
    await callback.message.edit_text(
        "👋 <b>Привет! Я — Кредитный Сторож.</b> 🏦\n\n"
        "Выбери действие:",
        reply_markup=main_menu(),
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
        await callback.message.edit_text(
            text,
            reply_markup=subscriptions_menu(),
            parse_mode="HTML"
        )

@dp.callback_query(F.data == "unsubscribe")
async def unsubscribe(callback: CallbackQuery):
    subs = get_user_subscriptions_with_id(callback.from_user.id)
    if not subs:
        await callback.message.edit_text(
            "😔 <b>У тебя пока нет подписок.</b>",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
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
    await callback.message.edit_text(
        "✅ <b>Ты отписан!</b>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

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
    await callback.message.edit_text("⏳ Получаю актуальную ставку...")
    rate = await get_rate_from_site(REFINANCE_URL, REFINANCE_SELECTOR) or "не удалось получить"
    add_subscription(
        callback.from_user.id,
        callback.from_user.username,
        "НБРБ",
        "Ставка рефинансирования",
        rate
    )
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
        "📝 <b>Напиши, какой банк ты хочешь добавить.</b>\n\n"
        "Например: <i>Банк Дабрабыт</i>\n\n"
        "Я передам твоё сообщение администратору.",
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "no_product")
async def no_product(callback: CallbackQuery):
    await callback.message.edit_text(
        "📝 <b>Напиши, какой кредит ты хочешь добавить.</b>\n\n"
        "Например: <i>Кредит «На всё про всё» в Технобанке</i>\n\n"
        "Я передам твоё сообщение администратору.",
        parse_mode="HTML"
    )

@dp.message()
async def handle_request(message: Message):
    user = message.from_user
    text = message.text
    add_request(user.id, user.username, text)
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новая заявка!</b>\n\n"
            f"От: @{user.username or 'без username'} (ID: {user.id})\n"
            f"Текст: <i>{text}</i>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    await message.answer(
        "✅ <b>Спасибо! Твоя заявка отправлена.</b>\n\n"
        "Я передал её администратору. Как только добавлю — сообщу.",
        parse_mode="HTML"
    )

def run_bot():
    asyncio.run(dp.start_polling(bot))

bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))