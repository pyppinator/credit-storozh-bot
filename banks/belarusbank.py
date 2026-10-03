BELARUSBANK = {
    "name": "Беларусбанк",
    "groups": {
        # === ИПОТЕКА И ЖИЛЬЁ ===
        "ipoteka": {
            "name": "🏠 Кредит «Ипотека с нами»",
            "products": {
                "ipoteka_24": {"name": "Грейс 24 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_24"},
                "ipoteka_12": {"name": "Грейс 12 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_12"},
                "ipoteka_12_gos": {"name": "Грейс 12 мес., гос. застройщик", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_12_gos"},
            }
        },
        "vozvedenie": {
            "name": "🏗️ Возведение (реконструкция) жилья",
            "products": {
                "vozvedenie_092": {"name": "Для граждан в населённых пунктах до 20 тыс.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_092"},
                "vozvedenie_091": {"name": "Материалы бел. производства, долевое с гос. заказчиками", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_091"},
                "vozvedenie_093": {"name": "Для граждан с договорами на строительство, облигации", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_093"},
                "vozvedenie_094": {"name": "Одноквартирный дом, реконструкция", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_094"},
                "vozvedenie_095": {"name": "В многоквартирном доме (гос. заказчики)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_095"},
            }
        },
        "pokupka_zhilya": {
            "name": "🏠 Приобретение жилья / незавершённое строение",
            "products": {
                "pokupka_143": {"name": "Для граждан в населённых пунктах до 20 тыс.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_143"},
                "pokupka_144": {"name": "У застройщика", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_144"},
                "pokupka_141": {"name": "У физ. (юр.) лица", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_141"},
                "pokupka_142": {"name": "Незавершённое законсервированное строение", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_142"},
                "pokupka_145": {"name": "Для нуждающихся (у застройщика)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_145"},
                "pokupka_146": {"name": "Для нуждающихся (у физ. (юр.) лица)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_146"},
            }
        },
        "vremya_stroit": {
            "name": "🏗️ Кредит «Время строить»",
            "products": {
                "vremya_stroit_1": {"name": "Время строить (Витебск, Могилёв)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-vremya-stroit-na-vozvedenie-zhilykh-pomeshcheniy-v-mnogokvartirnykh-zhilykh-domakh-zastroyshch/", "selector": "input#stavka", "action": "select_vremya_stroit_1"},
            }
        },
        "refinansirovanie": {
            "name": "🔄 Рефинансирование ипотеки",
            "products": {
                "refin_1": {"name": "Рефинансирование ипотеки", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-refinansirovanie-ipoteki-/", "selector": "input#stavka", "action": "select_refin_1"},
            }
        },
        "ipoteka_ekspress": {
            "name": "⚡ Кредит «Ипотека Экспресс»",
            "products": {
                "ekspress_101": {"name": "У застройщика", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_101"},
                "ekspress_102": {"name": "У застройщика (для нуждающихся)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_102"},
                "ekspress_103": {"name": "У физ. (юр.) лица", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_103"},
                "ekspress_104": {"name": "У физ. (юр.) лица (для нуждающихся)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_104"},
            }
        },
        "stroysberezheniya": {
            "name": "🏦 Стройсбережения",
            "products": {
                "stroysber_vozvedenie_6": {"name": "Возведение (вклад с 01.10.2021)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_vozvedenie_6"},
                "stroysber_vozvedenie_8": {"name": "Возведение (на общих основаниях)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_vozvedenie_8"},
                "stroysber_priobretenie_6": {"name": "Приобретение (вклад с 01.10.2021)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-priobretenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_priobretenie_6"},
                "stroysber_priobretenie_8": {"name": "Приобретение (на общих основаниях)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-priobretenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_priobretenie_8"},
            }
        },
        "subsidiya": {
            "name": "💰 Субсидия на погашение",
            "products": {
                "subsidiya_1": {"name": "Кредит с использованием субсидии", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilykh-pomeshcheniy-s-ispolzovaniem-subsidii-na-ego-pogashenie/", "selector": ".detail-banner__prop_title", "action": None},
            }
        },
        "dokreditovanie": {
            "name": "💰 Кредит «Докредитование»",
            "products": {
                "dokredit_2": {"name": "Расчёт по графику", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dokreditovanie/", "selector": "input#stavka", "action": "select_dokredit_2"},
                "dokredit_3": {"name": "За фактическое время", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dokreditovanie/", "selector": "input#stavka", "action": "select_dokredit_3"},
            }
        },
        "stroydom": {
            "name": "🏗️ Кредит «СТРОЙДОМ»",
            "products": {
                "stroydom_2": {"name": "Расчёт по графику", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-stroydom/", "selector": "input#stavka", "action": "select_stroydom_2"},
                "stroydom_3": {"name": "За фактическое время", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-stroydom/", "selector": "input#stavka", "action": "select_stroydom_3"},
            }
        },
        "dom_dlya_avto": {
            "name": "🚗 Кредит «Дом для Авто»",
            "products": {
                "avto_131": {"name": "Дом для Авто", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dom-dlya-avto/", "selector": "input#stavka", "action": "select_avto_131"},
                "avto_132": {"name": "Дом для Авто (с электрозаправкой)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dom-dlya-avto/", "selector": "input#stavka", "action": "select_avto_132"},
            }
        },
        # === ПОТРЕБИТЕЛЬСКИЕ КРЕДИТЫ ===
        "potrebitelskie": {
            "name": "💳 Потребительские кредиты",
            "products": {
                "svaye_5": {"name": "«На сваё» (в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye/", "selector": "input#stavka", "action": "select_svaye_5"},
                "svaye_7": {"name": "«На сваё» (онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye/", "selector": "input#stavka", "action": "select_svaye_7"},
                "svaye_doma_63": {"name": "«На сваё» (комплекты для домов)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye-dlya-priobreteniya-komplektov-izdeliy-dlya-vozvedeniya-domov-sbornykh-sooruzheniy-i-/", "selector": "input#stavka", "action": "select_svaye_doma_63"},
                "med_5": {"name": "Медицинские услуги (в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-meditsinskoy-pomoshchi-i-uslug-priobretenie-medikamentov-meditsinskoy-tekhniki-/", "selector": "input#stavka", "action": "select_med_5"},
                "med_7": {"name": "Медицинские услуги (онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-meditsinskoy-pomoshchi-i-uslug-priobretenie-medikamentov-meditsinskoy-tekhniki-/", "selector": "input#stavka", "action": "select_med_7"},
                "tur_63": {"name": "Туристические услуги", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-turisticheskikh-uslug-okazyvaemykh-na-territorii-respubliki-belarus/", "selector": "input#stavka", "action": "select_tur_63"},
                "rodnyya_143": {"name": "«На родныя тавары» (1 год)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_143"},
                "rodnyya_142": {"name": "«На родныя тавары» (2 года)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_142"},
                "rodnyya_141": {"name": "«На родныя тавары» (3 года)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_141"},
                "belgee_21": {"name": "BELGEE (грейс 12 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_21"},
                "belgee_24": {"name": "BELGEE (грейс 24 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_24"},
                "belgee_27": {"name": "BELGEE (грейс 36 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_27"},
                "geely_61": {"name": "GEELY (грейс 12 мес., онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_61"},
                "geely_58": {"name": "GEELY (грейс 12 мес., в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_58"},
                "geely_47": {"name": "GEELY (грейс 24 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_47"},
                "geely_18": {"name": "GEELY (грейс 24 мес., бел. сборка)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_18"},
                "legko_11": {"name": "«Лёгка ехаць» (грейс 180 дн.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_11"},
                "legko_8": {"name": "«Лёгка ехаць» (электромобиль)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_8"},
                "legko_13": {"name": "«Лёгка ехаць» (грейс 360 дн.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_13"},
                "legko_10": {"name": "«Лёгка ехаць» (электромобиль, 360 дн.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_10"},
                "legko_svaye_50": {"name": "«Лёгка ехаць. Сваё» (грейс 6 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_50"},
                "legko_svaye_21": {"name": "«Лёгка ехаць. Сваё» (грейс 12 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_21"},
                "legko_svaye_52": {"name": "«Лёгка ехаць. Сваё» (грейс 18 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_52"},
                "auto_161": {"name": "Автомобиль", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-avtomobilya-elektromobilya-/", "selector": "input#stavka", "action": "select_auto_161"},
                "auto_162": {"name": "Электромобиль", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-avtomobilya-elektromobilya-/", "selector": "input#stavka", "action": "select_auto_162"},
                "barkhat_63": {"name": "«Время Жить» (Клуб Бархат)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-vremya-zhit-dlya-uchastnikov-kluba-barkhat/", "selector": "input#stavka", "action": "select_barkhat_63"},
                "ledi_5": {"name": "«Леди» (в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-dlya-uchastnikov-kluba-ledi/", "selector": "input#stavka", "action": "select_ledi_5"},
                "ledi_7": {"name": "«Леди» (онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-dlya-uchastnikov-kluba-ledi/", "selector": "input#stavka", "action": "select_ledi_7"},
                "obnovlenie_63": {"name": "«Удачное обновление»", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-udachnoe-obnovlenie-/", "selector": "input#stavka", "action": "select_obnovlenie_63"},
            }
        },
    }
}