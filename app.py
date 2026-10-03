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
from scraper import get_rate_from_site

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
        f"💳 <b>{bank['name']}</b>\n\nВыбери категорию:",
        reply_markup=bank_menu(bank_id),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("cat_"))
async def category_selected(callback: CallbackQuery):
    parts = callback.data.split("_")
    bank_id = parts[1]
    cat_id = "_".join(parts[2:])
    bank = BANKS.get(bank_id)
    if not bank or "categories" not in bank:
        await callback.answer("Категория не найдена")
        return
    category = bank["categories"].get(cat_id)
    if not category:
        await callback.answer("Категория не найдена")
        return
    await callback.message.edit_text(
        f"💳 <b>{category['name']}</b>\n\nВыбери группу:",
        reply_markup=category_menu(bank_id, cat_id),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("group_"))
async def group_selected(callback: CallbackQuery):
    parts = callback.data.split("_")
    bank_id = parts[1]
    rest = "_".join(parts[2:])
    bank = BANKS.get(bank_id)
    if not bank:
        await callback.answer("Банк не найден")
        return

    cat_id = None
    group_id = rest

    if "categories" in bank:
        for cat_key, cat_data in bank["categories"].items():
            if rest.startswith(cat_key + "_"):
                cat_id = cat_key
                group_id = rest[len(cat_key) + 1:]
                break

    group = None
    if cat_id:
        category = bank["categories"].get(cat_id)
        if category:
            group = category["groups"].get(group_id)
    elif "groups" in bank:
        group = bank["groups"].get(group_id)

    if not group:
        await callback.answer("Группа не найдена")
        return

    await callback.message.edit_text(
        f"💳 <b>{group['name']}</b>\n\nВыбери вариант:",
        reply_markup=group_menu(bank_id, cat_id, group_id),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("prod_"))
async def product_selected(callback: CallbackQuery):
    parts = callback.data.split("_")
    bank_id = parts[1]
    bank = BANKS.get(bank_id)
    if not bank:
        await callback.answer("Ошибка")
        return

    product = None

    if "categories" in bank:
        for cat_id, cat_data in bank["categories"].items():
            for group_id, group_data in cat_data["groups"].items():
                prefix = f"prod_{bank_id}_{cat_id}_{group_id}_"
                if callback.data.startswith(prefix):
                    prod_id = callback.data[len(prefix):]
                    product = group_data["products"].get(prod_id)
                    if product:
                        break
            if product:
                break

    if not product and "groups" in bank:
        for group_id, group_data in bank["groups"].items():
            prefix = f"prod_{bank_id}_{group_id}_"
            if callback.data.startswith(prefix):
                prod_id = callback.data[len(prefix):]
                product = group_data["products"].get(prod_id)
                if product:
                    break

    if not product and "products" in bank:
        prefix = f"prod_{bank_id}_"
        if callback.data.startswith(prefix):
            prod_id = callback.data[len(prefix):]
            product = bank["products"].get(prod_id)

    if not product:
        await callback.answer("Кредит не найден")
        return

    if check_subscription_exists(callback.from_user.id, bank["name"], product["name"]):
        await callback.answer("⚠️ Ты уже подписан на этот кредит!", show_alert=True)
        return

    rate = get_rate_from_db(bank["name"], product["name"]) or "загружается..."

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
        f"Кредит: <a href=\"{product['url']}\">{product['name']}</a>\n"
        f"Текущая ставка: <b>{rate}</b>\n\n"
        f"Я буду следить за изменениями и сообщу, если что-то поменяется.",
        reply_markup=main_menu(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@dp.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ <b>Помощь</b>\n\n"
        "Я — <b>Кредитный Сторож</b>. Слежу за ставками по кредитам в банках РБ.\n\n"
        "<b>Что я умею:</b>\n"
        "• 📋 Выбрать банк — подписаться на кредит\n"
        "• 📌 Мои подписки — посмотреть и отписаться\n"
        "• 🔥 Популярные кредиты — что выбирают другие\n"
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
    rate = get_rate_from_db("НБРБ", "Ставка рефинансирования") or "загружается..."
    await callback.message.edit_text(
        f"📊 <b>Ставка рефинансирования НБРБ</b>\n\n"
        f"Текущее значение: <b>{rate}</b>\n\n"
        f"Этот показатель важен для многих кредитов — если он изменится, я сообщу.",
        reply_markup=refinance_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "refinance_subscribe")
async def refinance_subscribe(callback: CallbackQuery):
    if check_subscription_exists(callback.from_user.id, "НБРБ", "Ставка рефинансирования"):
        await callback.answer("⚠️ Ты уже подписан на ставку рефинансирования!", show_alert=True)
        return
    rate = get_rate_from_db("НБРБ", "Ставка рефинансирования") or "загружается..."
    add_subscription(callback.from_user.id, callback.from_user.username, "НБРБ", "Ставка рефинансирования", rate)
    await callback.message.edit_text(
        f"✅ <b>Ты подписан на уведомления об изменении ставки рефинансирования НБРБ.</b>\n\n"
        f"Текущая ставка: <b>{rate}</b>\n\n"
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

# ============ ПОПУЛЯРНЫЕ КРЕДИТЫ ============

@dp.callback_query(F.data == "top_products")
async def top_products_handler(callback: CallbackQuery):
    stats = get_stats()
    if not stats['top_products']:
        await callback.message.edit_text(
            "📊 Пока никто не подписался ни на один кредит.\n\n"
            "Будь первым! Выбери банк в главном меню.",
            reply_markup=top_products_menu(),
            parse_mode="HTML"
        )
        return

    text = "🔥 <b>Топ-5 популярных кредитов</b>\n\n"
    for i, (bank, product, cnt) in enumerate(stats['top_products'], 1):
        text += f"<b>{i}.</b> {bank} — «{product}»\n"
        text += f"    👥 Следят: <b>{cnt}</b> чел.\n\n"
    text += f"📌 Всего подписок: <b>{stats['total_subs']}</b>\n"
    text += f"👥 Пользователей: <b>{stats['total_users']}</b>"

    await callback.message.edit_text(text, reply_markup=top_products_menu(), parse_mode="HTML")

# ============ АДМИН-ПАНЕЛЬ ============

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    last_update = get_last_update_time() or "никогда"
    await callback.message.edit_text(
        f"🔐 <b>Админ-панель</b>\n\n"
        f"🕐 Последнее обновление ставок: <b>{last_update[:16].replace('T', ' ') if last_update != 'никогда' else 'никогда'}</b>\n\n"
        f"Обход ставок запускается <b>автоматически</b> на GitHub Actions каждый день в 3:00.\n"
        f"Чтобы запустить вручную — нажми «🔄 Запустить обход на GitHub».",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "admin_update_rates")
async def admin_update_rates(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f"🔄 <b>Запуск обхода ставок</b>\n\n"
        f"Обход запускается на <b>GitHub Actions</b> (не на Render).\n\n"
        f"1. Перейди по ссылке: <a href=\"{GITHUB_ACTIONS_URL}\">GitHub Actions</a>\n"
        f"2. Нажми <b>«Run workflow»</b>.\n"
        f"3. Дождись завершения (2–3 минуты).\n\n"
        f"После этого ставки обновятся.",
        reply_markup=admin_menu(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@dp.callback_query(F.data == "admin_restart")
async def admin_restart(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        "🔄 <b>Перезапускаю бота...</b>\n\n"
        "Через 10–20 секунд я снова буду в сети.",
        parse_mode="HTML"
    )
    os.execv(sys.executable, [sys.executable] + sys.argv)

@dp.callback_query(F.data == "admin_unsub_all")
async def admin_unsub_all(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return
    count = delete_all_user_subscriptions(callback.from_user.id)
    await callback.message.edit_text(
        f"✅ <b>Ты отписан от всех подписок!</b>\n\n"
        f"Удалено: <b>{count}</b> шт.",
        reply_markup=main_menu(is_admin=True),
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

    grouped = get_grouped_subscriptions()
    if grouped:
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += f"📋 <b>Подписчики ({len(grouped)} чел.):</b>\n\n"
        for user_data in grouped:
            user = f"@{user_data['username']}" if user_data['username'] else f"id{user_data['user_id']}"
            text += f"👤 <b>{user}</b>\n"
            text += f"   🆔 <code>{user_data['user_id']}</code>\n"
            for sub in user_data['subscriptions']:
                text += f"   • {sub['bank']} — «{sub['product']}»\n"
                text += f"     📈 {sub['rate']}\n"
            text += "\n"

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

    is_admin = (message.from_user.id == ADMIN_ID)
    await message.answer(
        "✅ <b>Спасибо! Твоя заявка отправлена.</b>\n\n"
        "Я передал её администратору. Как только добавлю — сообщу.",
        reply_markup=main_menu(is_admin=is_admin),
        parse_mode="HTML"
    )

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
    app = create_webhook_app()
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))