# Связка: (банк, продукт) -> (url, selector)

PRODUCTS_MAP = {
    # Технобанк
    ("Технобанк", "Обыкновенный кредит «ONLINE» 2.0"): (
        "https://tb.by/individuals/crediting/top/obyknovennyy-kredit--online--2-0/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Обыкновенный кредит «На полгода»"): (
        "https://tb.by/individuals/crediting/na-potrebitelskie-nuzhdy/obyknovennyy-kredit--na-polgoda-/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «На рефинансирование»"): (
        "https://tb.by/individuals/crediting/na-refinansirovanie/kreditnyy-produkt--na-refinansirovanie--2/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «Поехали»"): (
        "https://tb.by/individuals/crediting/na-avto/kreditnyy-produkt--poekhali-/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «Милый дом»"): (
        "https://tb.by/individuals/crediting/top/kreditnyy-produkt--milyy-dom-/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «Я построю Милый дом»"): (
        "https://tb.by/individuals/crediting/na-nedvizhimost/kreditnyy-produkt--ya-postroyu-milyy-dom-/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «КУПЛЯЙ!BY»"): (
        "https://tb.by/individuals/crediting/na-otechestvennye-tovary/kreditnyy-produkt--kuplyay-by-/",
        ".deposit-banner__feature-title"
    ),
    ("Технобанк", "Кредитный продукт «КУПЛЯЙ!BY ПЛЮС»"): (
        "https://tb.by/individuals/crediting/na-otechestvennye-tovary/kreditnyy-produkt--kuplyay-by-plyus-/",
        ".deposit-banner__feature-title"
    ),
    # НБРБ
    ("НБРБ", "Ставка рефинансирования"): (
        "https://www.gb.by/spravochniki/stavka-refinansirovaniya-natsionalnogo-b",
        "table tr:nth-child(2) td:nth-child(2)"
    ),
}