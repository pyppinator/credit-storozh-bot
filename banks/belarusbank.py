BELARUSBANK = {
    "name": "Беларусбанк",
    "categories": {
        "nedv": {
            "name": "🏠 Кредиты на недвижимость",
            "groups": {
                "ipot": {
                    "name": "🏠 Кредит «Ипотека с нами»",
                    "products": {
                        "ipot_24": {"name": "🏠 Ипотека с нами (грейс 24 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_24"},
                        "ipot_12": {"name": "🏠 Ипотека с нами (грейс 12 мес.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_12"},
                        "ipot_12gos": {"name": "🏛️ Ипотека с нами (грейс 12 мес., гос. застройщик)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-s-nami-v-ramkakh-partnerskikh-programm/", "selector": "input#stavka", "action": "select_ipoteka_12_gos"},
                    }
                },
                "vozv": {
                    "name": "🏗️ Возведение (реконструкция) жилья",
                    "products": {
                        "vozv_092": {"name": "🌾 Возведение жилья (в населённых пунктах до 20 тыс.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_092"},
                        "vozv_091": {"name": "🧱 Возведение жилья (материалы бел. пр-ва, долевое с гос.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_091"},
                        "vozv_093": {"name": "📜 Возведение жилья (договоры на строительство, облигации)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_093"},
                        "vozv_094": {"name": "🏡 Возведение жилья (одноквартирный дом, реконструкция)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_094"},
                        "vozv_095": {"name": "🏢 Возведение жилья (многоквартирный дом, гос. заказчики)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilya/", "selector": "input#stavka", "action": "select_vozvedenie_095"},
                    }
                },
                "pokup": {
                    "name": "🏠 Приобретение жилья / незавершённое строение",
                    "products": {
                        "pokup_143": {"name": "🌾 Приобретение жилья (в населённых пунктах до 20 тыс.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_143"},
                        "pokup_144": {"name": "🏗️ Приобретение жилья (у застройщика)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_144"},
                        "pokup_141": {"name": "👤 Приобретение жилья (у физ. (юр.) лица)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_141"},
                        "pokup_142": {"name": "🏚️ Приобретение незавершённого строения", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_142"},
                        "pokup_145": {"name": "🏗️ Приобретение жилья (для нуждающихся, у застройщика)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_145"},
                        "pokup_146": {"name": "👤 Приобретение жилья (для нуждающихся, у физ. (юр.) лица)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredity-na-priobretenie-zhilya-nezavershennogo-zakonservirovannogo-kapitalnogo-stroeniya-na-zemelnom/", "selector": "input#stavka", "action": "select_pokupka_146"},
                    }
                },
                "vremya": {
                    "name": "🏗️ Кредит «Время строить»",
                    "products": {
                        "vremya_1": {"name": "🏗️ Время строить (Витебск, Могилёв)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-vremya-stroit-na-vozvedenie-zhilykh-pomeshcheniy-v-mnogokvartirnykh-zhilykh-domakh-zastroyshch/", "selector": "input#stavka", "action": "select_vremya_stroit_1"},
                    }
                },
                "refin": {
                    "name": "🔄 Рефинансирование ипотеки",
                    "products": {
                        "refin_1": {"name": "🔄 Рефинансирование ипотеки", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-refinansirovanie-ipoteki-/", "selector": "input#stavka", "action": "select_refin_1"},
                    }
                },
                "ekspr": {
                    "name": "⚡ Кредит «Ипотека Экспресс»",
                    "products": {
                        "ekspr_101": {"name": "🏗️ Ипотека Экспресс (у застройщика)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_101"},
                        "ekspr_102": {"name": "🏗️ Ипотека Экспресс (у застройщика, для нуждающихся)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_102"},
                        "ekspr_103": {"name": "👤 Ипотека Экспресс (у физ. (юр.) лица)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_103"},
                        "ekspr_104": {"name": "👤 Ипотека Экспресс (у физ. (юр.) лица, для нуждающихся)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-ipoteka-ekspress-na-priobretenie-zhilogo-pomeshcheniya/", "selector": "input#stavka", "action": "select_ekspress_104"},
                    }
                },
                "stroysb": {
                    "name": "🏦 Стройсбережения",
                    "products": {
                        "stroysb_v6": {"name": "🏦 Стройсбережения: возведение (вклад с 01.10.2021)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_vozvedenie_6"},
                        "stroysb_v8": {"name": "🏦 Стройсбережения: возведение (общие основания)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_vozvedenie_8"},
                        "stroysb_p6": {"name": "🏦 Стройсбережения: приобретение (вклад с 01.10.2021)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-priobretenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_priobretenie_6"},
                        "stroysb_p8": {"name": "🏦 Стройсбережения: приобретение (общие основания)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-priobretenie-zhilya-po-sisteme-stroysberezheniy/", "selector": "input#stavka", "action": "select_stroysber_priobretenie_8"},
                    }
                },
                "subsid": {
                    "name": "💰 Субсидия на погашение",
                    "products": {
                        "subsid_1": {"name": "💰 Субсидия на погашение", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-na-vozvedenie-rekonstruktsiyu-zhilykh-pomeshcheniy-s-ispolzovaniem-subsidii-na-ego-pogashenie/", "selector": ".detail-banner__prop_title", "action": None},
                    }
                },
                "dokred": {
                    "name": "💰 Кредит «Докредитование»",
                    "products": {
                        "dokred_2": {"name": "💰 Докредитование (расчёт по графику)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dokreditovanie/", "selector": "input#stavka", "action": "select_dokredit_2"},
                        "dokred_3": {"name": "💰 Докредитование (за фактическое время)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dokreditovanie/", "selector": "input#stavka", "action": "select_dokredit_3"},
                    }
                },
                "strdom": {
                    "name": "🏗️ Кредит «СТРОЙДОМ»",
                    "products": {
                        "strdom_2": {"name": "🏗️ СТРОЙДОМ (расчёт по графику)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-stroydom/", "selector": "input#stavka", "action": "select_stroydom_2"},
                        "strdom_3": {"name": "🏗️ СТРОЙДОМ (за фактическое время)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-stroydom/", "selector": "input#stavka", "action": "select_stroydom_3"},
                    }
                },
                "avto": {
                    "name": "🚗 Кредит «Дом для Авто»",
                    "products": {
                        "avto_131": {"name": "🚗 Дом для Авто (машино-место, гараж)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dom-dlya-avto/", "selector": "input#stavka", "action": "select_avto_131"},
                        "avto_132": {"name": "⚡ Дом для Авто (с электрозаправкой)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/financing/kredit-dom-dlya-avto/", "selector": "input#stavka", "action": "select_avto_132"},
                    }
                },
            }
        },
        "potr": {
            "name": "💳 Потребительские кредиты",
            "groups": {
                "potr_all": {
                    "name": "💳 Все потребительские кредиты",
                    "products": {
                        "svaye_5": {"name": "🛍️ «На сваё» (товары бел. пр-ва, в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye/", "selector": "input#stavka", "action": "select_svaye_5"},
                        "svaye_7": {"name": "🛍️ «На сваё» (товары бел. пр-ва, онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye/", "selector": "input#stavka", "action": "select_svaye_7"},
                        "svaye_doma_63": {"name": "🏠 «На сваё» (комплекты для домов)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-svaye-dlya-priobreteniya-komplektov-izdeliy-dlya-vozvedeniya-domov-sbornykh-sooruzheniy-i-/", "selector": "input#stavka", "action": "select_svaye_doma_63"},
                        "med_5": {"name": "🏥 Медицинские услуги (в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-meditsinskoy-pomoshchi-i-uslug-priobretenie-medikamentov-meditsinskoy-tekhniki-/", "selector": "input#stavka", "action": "select_med_5"},
                        "med_7": {"name": "🏥 Медицинские услуги (онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-meditsinskoy-pomoshchi-i-uslug-priobretenie-medikamentov-meditsinskoy-tekhniki-/", "selector": "input#stavka", "action": "select_med_7"},
                        "tur_63": {"name": "✈️ Туристические услуги", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-oplatu-turisticheskikh-uslug-okazyvaemykh-na-territorii-respubliki-belarus/", "selector": "input#stavka", "action": "select_tur_63"},
                        "rodnyya_143": {"name": "🛒 «На родныя тавары» (1 год)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_143"},
                        "rodnyya_142": {"name": "🛒 «На родныя тавары» (2 года)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_142"},
                        "rodnyya_141": {"name": "🛒 «На родныя тавары» (3 года)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-rodnyya-tavary/", "selector": "input#stavka", "action": "select_rodnyya_141"},
                        "belgee_21": {"name": "🚗 BELGEE (S50, X50, X70, X80) — грейс 12 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_21"},
                        "belgee_24": {"name": "🚗 BELGEE (S50, X50, X70, X80) — грейс 24 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_24"},
                        "belgee_27": {"name": "🚗 BELGEE (S50, X50, X70, X80) — грейс 36 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-avtomobiley-marki-belgee-modeli-s50-x50-x70-x80/", "selector": "input#stavka", "action": "select_belgee_27"},
                        "geely_61": {"name": "🚙 GEELY (Cityray, Okavango, Monjaro, EX5) — онлайн", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_61"},
                        "geely_58": {"name": "🚙 GEELY (Cityray, Okavango, Monjaro, EX5) — в отделении", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_58"},
                        "geely_47": {"name": "🚙 GEELY (Cityray, Okavango, Monjaro) — грейс 24 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_47"},
                        "geely_18": {"name": "🚙 GEELY (EX2, бел. сборка) — грейс 24 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-u-dilerov-szao-beldzhi-elektromobiley-marki-geely-modeli-ex5/", "selector": "input#stavka", "action": "select_geely_18"},
                        "legko_11": {"name": "🚗 «Лёгка ехаць» — грейс 180 дн.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_11"},
                        "legko_8": {"name": "⚡ «Лёгка ехаць» (электромобиль)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_8"},
                        "legko_13": {"name": "🚗 «Лёгка ехаць» — грейс 360 дн.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_13"},
                        "legko_10": {"name": "⚡ «Лёгка ехаць» (электромобиль, 360 дн.)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-na-priobretenie-avtomobilya-elektromobilya-v-ramkakh-zaklyuchennykh-dogovorov-s/", "selector": "input#stavka", "action": "select_legko_10"},
                        "legko_svaye_50": {"name": "🚗 «Лёгка ехаць. Сваё» — грейс 6 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_50"},
                        "legko_svaye_21": {"name": "🚗 «Лёгка ехаць. Сваё» — грейс 12 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_21"},
                        "legko_svaye_52": {"name": "🚗 «Лёгка ехаць. Сваё» — грейс 18 мес.", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-lyegka-ekhats-svaye-na-priobretenie-avtomobiley-proizvodstva-respubliki-belarus-v-ramkakh-zak/", "selector": "input#stavka", "action": "select_legko_svaye_52"},
                        "auto_161": {"name": "🚗 Автомобиль", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-avtomobilya-elektromobilya-/", "selector": "input#stavka", "action": "select_auto_161"},
                        "auto_162": {"name": "⚡ Электромобиль", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-na-priobretenie-avtomobilya-elektromobilya-/", "selector": "input#stavka", "action": "select_auto_162"},
                        "barkhat_63": {"name": "👑 «Время Жить» (Клуб Бархат)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-vremya-zhit-dlya-uchastnikov-kluba-barkhat/", "selector": "input#stavka", "action": "select_barkhat_63"},
                        "ledi_5": {"name": "💃 «Леди» (в отделении)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-dlya-uchastnikov-kluba-ledi/", "selector": "input#stavka", "action": "select_ledi_5"},
                        "ledi_7": {"name": "💃 «Леди» (онлайн)", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-dlya-uchastnikov-kluba-ledi/", "selector": "input#stavka", "action": "select_ledi_7"},
                        "obnovlenie_63": {"name": "🔄 «Удачное обновление»", "url": "https://belarusbank.by/fizicheskim_licam/kredit/consumer/kredit-udachnoe-obnovlenie-/", "selector": "input#stavka", "action": "select_obnovlenie_63"},
                    }
                },
            }
        },
    }
}