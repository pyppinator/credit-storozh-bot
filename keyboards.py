from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from products import BANKS

def main_menu(is_admin=False):
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

def bank_menu(bank_id):
    bank = BANKS.get(bank_id)
    if not bank:
        return None
    buttons = []
    if "categories" in bank:
        for cat_id, cat_data in bank["categories"].items():
            buttons.append([InlineKeyboardButton(text=cat_data["name"], callback_data=f"c_{bank_id}_{cat_id}")])
    elif "groups" in bank:
        for group_id, group_data in bank["groups"].items():
            buttons.append([InlineKeyboardButton(text=group_data["name"], callback_data=f"g_{bank_id}_{group_id}")])
    elif "products" in bank:
        for prod_id, prod_data in bank["products"].items():
            buttons.append([InlineKeyboardButton(text=prod_data['name'], callback_data=f"p_{bank_id}_{prod_id}")])
    buttons.append([InlineKeyboardButton(text="📝 Нет моего кредита", callback_data="no_product")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="choose_bank")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def category_menu(bank_id, cat_id):
    bank = BANKS.get(bank_id)
    if not bank or "categories" not in bank:
        return None
    category = bank["categories"].get(cat_id)
    if not category:
        return None
    buttons = []
    for group_id, group_data in category["groups"].items():
        buttons.append([InlineKeyboardButton(text=group_data["name"], callback_data=f"g_{bank_id}_{cat_id}_{group_id}")])
    buttons.append([InlineKeyboardButton(text="📝 Нет моего кредита", callback_data="no_product")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"bank_{bank_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def group_menu(bank_id, cat_id, group_id):
    bank = BANKS.get(bank_id)
    if not bank:
        return None
    group = None
    if "categories" in bank:
        category = bank["categories"].get(cat_id)
        if category:
            group = category["groups"].get(group_id)
    elif "groups" in bank:
        group = bank["groups"].get(group_id)
    if not group:
        return None
    buttons = []
    for prod_id, prod_data in group["products"].items():
        buttons.append([InlineKeyboardButton(text=prod_data['name'], callback_data=f"p_{bank_id}_{cat_id}_{group_id}_{prod_id}")])
    buttons.append([InlineKeyboardButton(text="📝 Нет моего кредита", callback_data="no_product")])
    back_callback = f"c_{bank_id}_{cat_id}" if cat_id else f"bank_{bank_id}"
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def subscriptions_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отписаться от...", callback_data="unsubscribe")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])

def unsubscribe_menu(subs_with_id):
    buttons = []
    for sub_id, bank, product, rate in subs_with_id:
        buttons.append([InlineKeyboardButton(text=f"❌ {bank} — «{product}»", callback_data=f"unsub_{sub_id}")])
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
        [InlineKeyboardButton(text="🔄 Запустить обход на GitHub", callback_data="admin_update_rates")],
        [InlineKeyboardButton(text="🔄 Перезапустить бота", callback_data="admin_restart")],
        [InlineKeyboardButton(text="❌ Отписаться от ВСЕХ", callback_data="admin_unsub_all")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])

def top_products_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_main")],
    ])