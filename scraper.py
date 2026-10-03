from playwright.async_api import async_playwright

# ============ КАРТА ДЕЙСТВИЙ ============

ACTION_MAP = {
    # === ИПОТЕКА Беларусбанк ===
    "select_ipoteka_24": ("111", None),
    "select_ipoteka_12": ("112", "21"),
    "select_ipoteka_12_gos": ("112", "23"),
    "select_vozvedenie_092": ("092", None),
    "select_vozvedenie_091": ("091", None),
    "select_vozvedenie_093": ("093", None),
    "select_vozvedenie_094": ("094", None),
    "select_vozvedenie_095": ("095", None),
    "select_pokupka_143": ("143", "2"),
    "select_pokupka_144": ("144", "2"),
    "select_pokupka_141": ("141", "2"),
    "select_pokupka_142": ("142", "2"),
    "select_pokupka_145": ("145", "2"),
    "select_pokupka_146": ("146", "2"),
    "select_vremya_stroit_1": (None, "4"),
    "select_refin_1": (None, "4"),
    "select_ekspress_101": ("101", "4"),
    "select_ekspress_102": ("102", "4"),
    "select_ekspress_103": ("103", "4"),
    "select_ekspress_104": ("104", "4"),
    "select_stroysber_vozvedenie_6": (None, "6"),
    "select_stroysber_vozvedenie_8": (None, "8"),
    "select_stroysber_priobretenie_6": (None, "6"),
    "select_stroysber_priobretenie_8": (None, "8"),
    "select_subsidiya_1": (None, None),
    "select_dokredit_2": (None, "2"),
    "select_dokredit_3": (None, "3"),
    "select_stroydom_2": (None, "2"),
    "select_stroydom_3": (None, "3"),
    "select_avto_131": ("131", "2"),
    "select_avto_132": ("132", "2"),
    # === ПОТРЕБИТЕЛЬСКИЕ Беларусбанк ===
    "select_svaye_5": (None, "5"),
    "select_svaye_7": (None, "7"),
    "select_svaye_doma_63": (None, "63"),
    "select_med_5": (None, "5"),
    "select_med_7": (None, "7"),
    "select_tur_63": (None, "63"),
    "select_rodnyya_143": ("143", "35"),
    "select_rodnyya_142": ("142", "35"),
    "select_rodnyya_141": ("141", "35"),
    "select_belgee_21": (None, "21"),
    "select_belgee_24": (None, "24"),
    "select_belgee_27": (None, "27"),
    "select_geely_61": (None, "61"),
    "select_geely_58": (None, "58"),
    "select_geely_47": (None, "47"),
    "select_geely_18": (None, "18"),
    "select_legko_11": (None, "11"),
    "select_legko_8": (None, "8"),
    "select_legko_13": (None, "13"),
    "select_legko_10": (None, "10"),
    "select_legko_svaye_50": (None, "50"),
    "select_legko_svaye_21": (None, "21"),
    "select_legko_svaye_52": (None, "52"),
    "select_auto_161": ("161", "39"),
    "select_auto_162": ("162", "39"),
    "select_barkhat_63": (None, "63"),
    "select_ledi_5": (None, "5"),
    "select_ledi_7": (None, "7"),
    "select_obnovlenie_63": (None, "63"),
}

# ============ ПОЛУЧЕНИЕ СТАВКИ ============

async def get_rate_from_site(url, selector, action=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Accept-Language": "ru-RU,ru;q=0.9"})
        try:
            print(f"[DEBUG] Открываю {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(2000)

            if action:
                print(f"[DEBUG] Выполняю action: {action}")
                value, radio_value = ACTION_MAP.get(action, (None, None))

                if value:
                    await page.evaluate(f"""
                        () => {{
                            const sel = document.querySelector('select#iscredit');
                            if (sel) {{
                                sel.value = '{value}';
                                sel.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}
                    """)
                    await page.wait_for_timeout(2000)

                if radio_value:
                    await page.evaluate(f"""
                        () => {{
                            let radio = document.querySelector('input[name="SPOSOB"][value="{radio_value}"]');
                            if (!radio) {{
                                radio = document.querySelector('input[name="SEND"][value="{radio_value}"]');
                            }}
                            if (radio) {{
                                radio.checked = true;
                                radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}
                    """)
                    await page.wait_for_timeout(2000)

            # === МТБанк ===

            # Грейс + основная (два элемента)
            if selector == "mtbank_na_mary" or selector == "mtbank_greeting_text":
                value = await page.evaluate("""
                    () => {
                        const title = document.querySelector('.hero-banner__feature-title');
                        const text = document.querySelector('.hero-banner__feature-text');
                        const t = title ? title.innerText.trim() : null;
                        const x = text ? text.innerText.trim() : null;
                        if (t && x) return `${t} | ${x}`;
                        return t || x || null;
                    }
                """)
                await browser.close()
                return value if value else None

            # Только текст (льготный период + ставка)
            if selector == "mtbank_text_only":
                value = await page.evaluate("""
                    () => {
                        const text = document.querySelector('.hero-banner__feature-text');
                        return text ? text.innerText.trim() : null;
                    }
                """)
                await browser.close()
                return value if value else None

            # Только одна ставка (title)
            if selector == "mtbank_prosto" or selector == "mtbank_refin" or selector == "mtbank_pensia" or selector == "mtbank_online" or selector == "mtbank_21vek" or selector == "mtbank_gotovoe" or selector == "mtbank_dolevoe":
                value = await page.evaluate("""
                    () => {
                        const title = document.querySelector('.hero-banner__feature-title');
                        return title ? title.innerText.trim() : null;
                    }
                """)
                await browser.close()
                return value if value else None

            # === Беларусбанк ===

            if selector == "input#stavka":
                value = await page.evaluate(f"document.querySelector('{selector}')?.value")
                await browser.close()
                return value if value else None

            if selector == ".detail-banner__prop_title":
                value = await page.evaluate(f"""
                    () => {{
                        const els = document.querySelectorAll('{selector}');
                        return els.length > 1 ? els[1].innerText : null;
                    }}
                """)
                await browser.close()
                return value if value else None

            # === Технобанк ===

            await page.wait_for_selector(selector, timeout=15000)
            elements = await page.query_selector_all(selector)
            values = []
            for el in elements:
                text = await el.inner_text()
                values.append(text.strip())
            await browser.close()
            return ", ".join(values) if values else None

        except Exception as e:
            print(f"[DEBUG] ОШИБКА: {type(e).__name__}: {e}")
            await browser.close()
            return None