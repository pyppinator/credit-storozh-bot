from playwright.async_api import async_playwright

# ============ КАРТА ДЕЙСТВИЙ ============

ACTION_MAP = {
    # === Беларусбанк — Ипотека ===
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
    # === Беларусбанк — Потребительские ===
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

# ============ БЛОКИРОВКА ЛИШНИХ РЕСУРСОВ ============

async def block_resources(route):
    if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
        await route.abort()
    else:
        await route.continue_()

# ============ ПОЛУЧЕНИЕ СТАВКИ ============

async def get_rate_from_site(url, selector, action=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"Accept-Language": "ru-RU,ru;q=0.9"})
        await page.route("**/*", block_resources)

        try:
            print(f"[DEBUG] Открываю {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(1500)

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
                    await page.wait_for_timeout(1000)

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
                    await page.wait_for_timeout(1000)

            # === Приорбанк: «На белорусские товары» и партнёры ===
            if selector == "priorbank_bel_tovary":
                value = await page.evaluate("""
                    () => {
                        const els = document.querySelectorAll('.icons-text-descr span');
                        const values = [];
                        els.forEach(el => {
                            const t = el.innerText.trim();
                            if (t && t.includes('%')) values.push(t.split(' ')[0]);
                        });
                        return values.length ? values.join(' / ') : null;
                    }
                """)
                print(f"[DEBUG] priorbank_bel_tovary = {value}")
                await browser.close()
                return value if value else None

            # === Приорбанк: «Проще.net» ===
            if selector == "priorbank_prosche_net":
                value = await page.evaluate("""
                    () => {
                        const el = document.querySelector('.banner-content_big-bold');
                        return el ? el.innerText.trim() : null;
                    }
                """)
                print(f"[DEBUG] priorbank_prosche_net = {value}")
                await browser.close()
                return value if value else None

            # === Приорбанк: недвижимость — берём строго 2 ставки: баннер + тултип ===
            if selector == "priorbank_banner_bold":
                value = await page.evaluate("""
                    () => {
                        const parseRate = (s) => {
                            if (!s) return null;
                            const m = s.match(/(\\d{1,2}[.,]\\d{1,2})\\s*%/);
                            if (!m) return null;
                            return m[1].replace(',', '.') + '%';
                        };

                        let first = null;   // ставка из баннера
                        let second = null;  // ставка из тултипа или условий

                        // 1. СТАВКА №1: .banner-content__title .banner-content_big-bold
                        const titleEl = document.querySelector('.banner-content__title .banner-content_big-bold');
                        if (titleEl) first = parseRate(titleEl.innerText);

                        // 2. СТАВКА №2 (приоритет — тултип внутри баннера):
                        //    ищем <u> внутри .banner-content__descr, у которого или родителя есть data-tooltip-text
                        const descrU = document.querySelector('.banner-content__descr u');
                        if (descrU) {
                            // тултип может быть на самом <u> или на его обёртке
                            let tipText = descrU.getAttribute('data-tooltip-text');
                            if (!tipText) {
                                const span = descrU.closest('[data-tooltip-text]');
                                if (span) tipText = span.getAttribute('data-tooltip-text');
                            }
                            if (!tipText) {
                                const parent = descrU.parentElement;
                                if (parent) tipText = parent.getAttribute('data-tooltip-text');
                            }
                            if (tipText) second = parseRate(tipText);
                        }

                        // 3. Если тултип не нашёлся — берём вторую ставку из блока «Условия кредита»
                        if (!second) {
                            const nodes = document.querySelectorAll('p, div, span');
                            const candidates = [];
                            nodes.forEach(el => {
                                if (el.children.length > 0) return;
                                const t = (el.innerText || '').trim();
                                const m = t.match(/^(\\d{1,2}[.,]\\d{1,2})\\s*%\\s*годовых$/i);
                                if (m) {
                                    const num = parseFloat(m[1].replace(',', '.'));
                                    if (num >= 5 && num <= 40) {
                                        candidates.push(m[1].replace(',', '.') + '%');
                                    }
                                }
                            });
                            // второй кандидат — это ставка "далее"
                            if (candidates.length >= 2) second = candidates[1];
                        }

                        // 4. Собираем результат: сначала первая, потом вторая (если есть и не дубликат)
                        const result = [];
                        if (first) result.push(first);
                        if (second && second !== first) result.push(second);

                        return result.length ? result.join(' / ') : null;
                    }
                """)
                print(f"[DEBUG] priorbank_banner_bold = {value}")
                await browser.close()
                return value if value else None

            # === МТБанк ===
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

            if selector == "mtbank_text_only":
                value = await page.evaluate("""
                    () => {
                        const text = document.querySelector('.hero-banner__feature-text');
                        return text ? text.innerText.trim() : null;
                    }
                """)
                await browser.close()
                return value if value else None

            if selector in ["mtbank_prosto", "mtbank_refin", "mtbank_pensia", "mtbank_online", "mtbank_21vek", "mtbank_gotovoe", "mtbank_dolevoe"]:
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