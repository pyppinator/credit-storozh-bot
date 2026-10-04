from playwright.async_api import async_playwright

# ============ КАРТА ДЕЙСТВИЙ ============

ACTION_MAP = {
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

async def block_resources(route):
    if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
        await route.abort()
    else:
        await route.continue_()

async def get_rate_from_site(url, selector, action=None, column_index=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="ru-RU",
            timezone_id="Europe/Minsk",
        )
        page = await context.new_page()

        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru', 'en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        """)

        await page.set_extra_http_headers({"Accept-Language": "ru-RU,ru;q=0.9"})
        await page.route("**/*", block_resources)

        try:
            print(f"[DEBUG] Открываю {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(3000)

            title = await page.title()
            if "verification" in title.lower() or "проверка" in title.lower():
                await page.wait_for_timeout(5000)
                title2 = await page.title()
                if "verification" in title2.lower() or "проверка" in title2.lower():
                    await browser.close()
                    return None

            if action:
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

            # === Приорбанк ===
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
                await browser.close()
                return value if value else None

            if selector == "priorbank_prosche_net":
                value = await page.evaluate("""
                    () => {
                        const el = document.querySelector('.banner-content_big-bold');
                        return el ? el.innerText.trim() : null;
                    }
                """)
                await browser.close()
                return value if value else None

            if selector == "priorbank_banner_bold":
                value = await page.evaluate("""
                    () => {
                        const parseRate = (s) => {
                            if (!s) return null;
                            const m = s.match(/(\\d{1,2}[.,]\\d{1,2})\\s*%/);
                            if (!m) return null;
                            return m[1].replace(',', '.') + '%';
                        };
                        let first = null, second = null;
                        const bolds = document.querySelectorAll('.banner-content_big-bold');
                        for (const el of bolds) {
                            const t = (el.innerText || '').trim();
                            if (t.includes('%')) { first = parseRate(t); if (first) break; }
                        }
                        const tips = document.querySelectorAll('[data-tooltip-text]');
                        for (const el of tips) {
                            const txt = el.getAttribute('data-tooltip-text') || '';
                            if (/Далее\\s+применяется\\s+ставка/i.test(txt)) { second = parseRate(txt); if (second) break; }
                        }
                        const result = [];
                        if (first) result.push(first);
                        if (second && second !== first) result.push(second);
                        return result.length ? result.join(' / ') : null;
                    }
                """)
                await browser.close()
                return value if value else None

            # === Белгазпромбанк ===
            if selector == "belgazprombank_rates":
                value = await page.evaluate("""
                    () => {
                        const tds = document.querySelectorAll('td');
                        let targetNext = null;
                        for (const td of tds) {
                            const t = (td.innerText || '').replace(/\\u00a0/g, ' ').trim();
                            if (t.length > 150) continue;
                            if (!/размер\\s+процентов/i.test(t)) continue;
                            if (!/порядок/i.test(t)) continue;
                            const next = td.nextElementSibling;
                            if (!next) continue;
                            const nextText = (next.innerText || '').replace(/\\u00a0/g, ' ');
                            if (!/%/.test(nextText)) continue;
                            targetNext = nextText;
                            break;
                        }
                        if (!targetNext) return null;
                        const text = targetNext.replace(/\\s+/g, ' ').trim();
                        const results = [];
                        const firstRe = /первых\\s+(\\d{1,4})\\s+календарных\\s+дней?\\s*[–\\-]\\s*(?:от\\s+)?([\\d.,]+)\\s*%/gi;
                        let m;
                        while ((m = firstRe.exec(text)) !== null) {
                            const days = m[1];
                            const val = m[2].replace(',', '.') + '%';
                            const item = val + ' (' + days + ' дн.)';
                            if (!results.includes(item)) results.push(item);
                        }
                        const secondRe = /с\\s+(\\d{1,4})\\s+календарного\\s+дня\\s*[–\\-]\\s*(?:от\\s+)?([\\d.,]+)\\s*%/gi;
                        while ((m = secondRe.exec(text)) !== null) {
                            const val = m[2].replace(',', '.') + '%';
                            const item = val + ' (далее)';
                            if (!results.includes(item)) results.push(item);
                        }
                        return results.length ? results.join(' / ') : null;
                    }
                """)
                await browser.close()
                return value if value else None

            # === Белагропромбанк: финал ===
            if selector == "belapb_rates":
                value = await page.evaluate("""
                    () => {
                        const parseRate = (s) => {
                            if (!s) return null;
                            const m = s.match(/(\\d{1,2}[.,]\\d{1,2})\\s*%/);
                            if (!m) return null;
                            return m[1].replace(',', '.') + '%';
                        };

                        let mainRate = null;
                        let graceRate = null;

                        // 1. Основная ставка: <td> "Процентная ставка по кредитному договору" → сосед справа
                        const tds = document.querySelectorAll('td');
                        for (const td of tds) {
                            const t = (td.innerText || '').replace(/\\u00a0/g, ' ').trim();
                            if (t.length > 200) continue;
                            if (!/процентная\\s+ставка\\s+по\\s+кредитному\\s+договору/i.test(t)) continue;
                            const next = td.nextElementSibling;
                            if (!next) continue;
                            mainRate = parseRate(next.innerText || '');
                            if (mainRate) break;
                        }

                        // 2. Грейс: <td> ТОЧНО "Грейс-период N дней" (не "Срок действия грейс-периода")
                        for (const td of tds) {
                            const t = (td.innerText || '').replace(/\\u00a0/g, ' ').trim();
                            if (t.length > 200) continue;
                            // именно "Грейс-период" в НАЧАЛЕ строки (а не "Срок действия грейс-периода")
                            if (!/^грейс-период/i.test(t)) continue;
                            const next = td.nextElementSibling;
                            if (!next) continue;
                            graceRate = parseRate(next.innerText || '');
                            if (graceRate) break;
                        }

                        // 3. Формируем результат
                        const results = [];
                        if (graceRate) results.push('Грейс-период ' + graceRate);
                        if (mainRate) results.push(mainRate);

                        if (results.length > 0) {
                            return results.join('; ');
                        }

                        // 4. Fallback: <li class="page-head__list-item"> с "Процентная ставка"
                        const items = document.querySelectorAll('li.page-head__list-item');
                        for (const li of items) {
                            const nameEl = li.querySelector('.page-head__list-name');
                            if (!nameEl) continue;
                            const name = (nameEl.innerText || '').trim().toLowerCase();
                            if (!name.includes('процентная ставка')) continue;
                            const valEl = li.querySelector('.page-head__list-val');
                            if (!valEl) continue;
                            const r = parseRate(valEl.innerText || '');
                            if (r) return r;
                        }

                        return null;
                    }
                """)
                print(f"[DEBUG] belapb_rates = {value}")
                await browser.close()
                return value if value else None

            # === Альфа-Банк: cash ===
            if selector == "alfabank_cash_rate":
                value = await page.evaluate("""
                    () => {
                        const parseRate = (s) => {
                            if (!s) return null;
                            const m = s.match(/(\\d{1,2}[.,]\\d{1,2})\\s*%/);
                            if (!m) return null;
                            return m[1].replace(',', '.') + '%';
                        };
                        const topText = document.querySelector('.page-top-section__text');
                        if (topText) {
                            const r = parseRate(topText.innerText);
                            if (r) return r;
                        }
                        const nodes = document.querySelectorAll('p, div, span, li');
                        for (const el of nodes) {
                            if (el.children.length > 0) return;
                            const t = (el.innerText || '').trim();
                            if (!t) continue;
                            if (/Ставка\\s+\\d/i.test(t)) {
                                const r = parseRate(t);
                                if (r) return r;
                            }
                        }
                        return null;
                    }
                """)
                await browser.close()
                return value if value else None

            # === Альфа-Банк: fixed ===
            if selector == "alfabank_fixed_rate":
                value = await page.evaluate("""
                    () => {
                        const items = document.querySelectorAll('.page-top-section__bottom-item');
                        for (const item of items) {
                            const titleEl = item.querySelector('.item-title');
                            const textEl = item.querySelector('.text');
                            if (!titleEl || !textEl) continue;
                            const title = (titleEl.innerText || '').trim().toLowerCase();
                            if (title.includes('ставка') || title.includes('процент')) {
                                const t = (textEl.innerText || '').trim();
                                const m = t.match(/(\\d{1,2}[.,]\\d{1,2})\\s*%/);
                                if (m) return m[1].replace(',', '.') + '%';
                            }
                        }
                        return null;
                    }
                """)
                await browser.close()
                return value if value else None

            # === Альфа-Банк: auto ===
            if selector == "alfabank_auto_table":
                value = await page.evaluate(f"""
                    () => {{
                        const colIdx = {column_index if column_index is not None else 1};
                        const tables = document.querySelectorAll('.info-section__table-wrapper table');
                        for (const table of tables) {{
                            const rows = table.querySelectorAll('tr');
                            for (const row of rows) {{
                                const cells = row.querySelectorAll('td');
                                if (cells.length < 2) continue;
                                const first = (cells[0].innerText || '').trim().toLowerCase();
                                if (!first.includes('процентная ставка')) continue;
                                if (colIdx >= cells.length) return null;
                                const target = cells[colIdx];
                                const text = (target.innerText || '').replace(/\\u00a0/g, ' ');
                                const lines = text.split(/\\n+/).map(s => s.trim()).filter(Boolean);
                                const results = [];
                                for (const line of lines) {{
                                    const isAfter = /по\\s+истечении/i.test(line);
                                    const re = /(\\d{{1,2}}[.,]\\d{{1,2}})\\s*%?\\s*(?:\\((\\d{{1,3}})\\s*мес[^)]*\\))?/g;
                                    let m;
                                    while ((m = re.exec(line)) !== null) {{
                                        const val = m[1].replace(',', '.') + '%';
                                        const months = m[2];
                                        let label;
                                        if (isAfter) label = ' (далее)';
                                        else if (months) label = ` (${{months}} мес.)`;
                                        else label = '';
                                        const item = val + label;
                                        if (!results.includes(item)) results.push(item);
                                    }}
                                }}
                                return results.length ? results.join(' / ') : null;
                            }}
                        }}
                        return null;
                    }}
                """)
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