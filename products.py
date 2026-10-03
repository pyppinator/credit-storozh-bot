BANKS = {
    "tb": {
        "name": "Технобанк",
        "products": {
            "online_2_0": {
                "name": "Обыкновенный кредит «ONLINE» 2.0",
                "url": "https://tb.by/individuals/crediting/top/obyknovennyy-kredit--online--2-0/",
                "selector": ".deposit-banner__feature-title"
            },
            "na_polgoda": {
                "name": "Обыкновенный кредит «На полгода»",
                "url": "https://tb.by/individuals/crediting/na-potrebitelskie-nuzhdy/obyknovennyy-kredit--na-polgoda-/",
                "selector": ".deposit-banner__feature-title"
            },
            "na_refinansirovanie": {
                "name": "Кредитный продукт «На рефинансирование»",
                "url": "https://tb.by/individuals/crediting/na-refinansirovanie/kreditnyy-produkt--na-refinansirovanie--2/",
                "selector": ".deposit-banner__feature-title"
            },
            "poekhali": {
                "name": "Кредитный продукт «Поехали»",
                "url": "https://tb.by/individuals/crediting/na-avto/kreditnyy-produkt--poekhali-/",
                "selector": ".deposit-banner__feature-title"
            },
            "milyy_dom": {
                "name": "Кредитный продукт «Милый дом»",
                "url": "https://tb.by/individuals/crediting/top/kreditnyy-produkt--milyy-dom-/",
                "selector": ".deposit-banner__feature-title"
            },
            "ya_postroyu_milyy_dom": {
                "name": "Кредитный продукт «Я построю Милый дом»",
                "url": "https://tb.by/individuals/crediting/na-nedvizhimost/kreditnyy-produkt--ya-postroyu-milyy-dom-/",
                "selector": ".deposit-banner__feature-title"
            },
            "kuplyay_by": {
                "name": "Кредитный продукт «КУПЛЯЙ!BY»",
                "url": "https://tb.by/individuals/crediting/na-otechestvennye-tovary/kreditnyy-produkt--kuplyay-by-/",
                "selector": ".deposit-banner__feature-title"
            },
            "kuplyay_by_plus": {
                "name": "Кредитный продукт «КУПЛЯЙ!BY ПЛЮС»",
                "url": "https://tb.by/individuals/crediting/na-otechestvennye-tovary/kreditnyy-produkt--kuplyay-by-plyus-/",
                "selector": ".deposit-banner__feature-title"
            },
        }
    },
    "belarusbank": {
        "name": "Беларусбанк",
        "groups": {
            "ipoteka": {
                "name": "🏠 Кредит «Ипотека с нами»",
                "products": {
                    "ipoteka_24": {
                        "name": "Грейс 24 мес.",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/",
                        "selector": "input#stavka",
                        "action": "select_ipoteka_24"
                    },
                    "ipoteka_12": {
                        "name": "Грейс 12 мес.",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/",
                        "selector": "input#stavka",
                        "action": "select_ipoteka_12"
                    },
                    "ipoteka_12_gos": {
                        "name": "Грейс 12 мес., гос. застройщик",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/",
                        "selector": "input#stavka",
                        "action": "select_ipoteka_12_gos"
                    },
                }
            },
            "vozvedenie": {
                "name": "🏗️ Возведение (реконструкция) жилья",
                "products": {
                    "vozvedenie_092": {
                        "name": "Для граждан в населённых пунктах до 20 тыс.",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/",
                        "selector": "input#stavka",
                        "action": "select_vozvedenie_092"
                    },
                    "vozvedenie_091": {
                        "name": "Материалы бел. производства, долевое с гос. заказчиками",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/",
                        "selector": "input#stavka",
                        "action": "select_vozvedenie_091"
                    },
                    "vozvedenie_093": {
                        "name": "Для граждан с договорами на строительство, облигации",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/",
                        "selector": "input#stavka",
                        "action": "select_vozvedenie_093"
                    },
                    "vozvedenie_094": {
                        "name": "Одноквартирный дом, реконструкция",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/",
                        "selector": "input#stavka",
                        "action": "select_vozvedenie_094"
                    },
                    "vozvedenie_095": {
                        "name": "В многоквартирном доме (гос. заказчики)",
                        "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/",
                        "selector": "input#stavka",
                        "action": "select_vozvedenie_095"
                    },
                }
            },
        }
    },
}