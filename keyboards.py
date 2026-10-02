from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from products import BANKS

def main_menu(is_admin=False):
    """Главное меню. Если is_admin=True — добавляет админ-кнопку."""
    buttons = [
        [InlineKeyboardButton(text="📋 Выбрать банк", callback_data="choose_bank")],
        [InlineKeyboardButton(text="📌 Мои подписки", callback_data="my_subs")],
        [InlineKeyboardButton(text="🔥 Популярные кредиты", callback_data="top_products")],
        [InlineKeyboardButton(text="📊 Ставка рефинансирования", callback_data="refinance")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")],
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="🔐 Админ-панель", callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def banks_menu():
    buttons = []
    for bank_id, bank_data in BANKS.items():
        buttons.append([InlineKeyboardButton(text=f"🏦 {bank_data['name']}", callback_data=f"bank_{bank_id}")])
    buttons.append([InlineKeyboardButton(text="📝 Нет моего банка", callback_data="no_bank")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def products_menu(bank_id):
    bank = BANKS.get(bank_id)
    if not bank:
        return None
    buttons = []
    for prod_id, prod_data in bank["products"].items():
        buttons.append([InlineKeyboardButton(text=f"💳 {prod_data['name']}", callback_data=f"prod_{bank_id}_{prod_id}")])
    buttons.append([InlineKeyboardButton(text="📝 Нет моего кредита", callback_data="no_product")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="choose_bank")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def subscriptions_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отписаться от...", callback_data="unsubscribe")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])

def unsubscribe_menu(subs_with_id):
    buttons = []
    for sub_id, bank, product, rate in subs_with_id:
        buttons.append([InlineKeyboardButton(
            text=f"❌ {bank} — «{product}»",
            callback_data=f"unsub_{sub_id}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="my_subs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def refinance_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Следить за изменениями", callback_data="refinance_subscribe")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика и подписки", callback_data="admin_subs")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])

def top_products_menu():
    """Меню для раздела «Популярные кредиты»"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])