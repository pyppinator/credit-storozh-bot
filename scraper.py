from playwright.async_api import async_playwright

# ============ КАРТА ДЕЙСТВИЙ ДЛЯ БЕЛАРУСБАНКА ============

ACTION_MAP = {
    # Ипотека с нами
    "select_ipoteka_24": ("111", None),
    "select_ipoteka_12": ("112", "21"),
    "select_ipoteka_12_gos": ("112", "23"),
    # Возведение жилья
    "select_vozvedenie_092": ("092", None),
    "select_vozvedenie_091": ("091", None),
    "select_vozvedenie_093": ("093", None),
    "select_vozvedenie_094": ("094", None),
    "select_vozvedenie_095": ("095", None),
    # Приобретение жилья / незавершённое строение
    "select_pokupka_143": ("143", "2"),
    "select_pokupka_144": ("144", "2"),
    "select_pokupka_141": ("141", "2"),
    "select_pokupka_142": ("142", "2"),
    "select_pokupka_145": ("145", "2"),
    "select_pokupka_146": ("146", "2"),
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
                value, sposob = ACTION_MAP.get(action, (None, None))

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
                    print(f"[DEBUG] Установил iscredit = {value}")
                    await page.wait_for_timeout(2000)

                if sposob:
                    await page.evaluate(f"""
                        () => {{
                            const radio = document.querySelector('input[name="SPOSOB"][value="{sposob}"]');
                            if (radio) {{
                                radio.checked = true;
                                radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}
                    """)
                    print(f"[DEBUG] Установил SPOSOB = {sposob}")
                    await page.wait_for_timeout(2000)

                print(f"[DEBUG] Action выполнен")

            if selector.startswith("input#"):
                value = await page.evaluate(f"document.querySelector('{selector}')?.value")
                print(f"[DEBUG] input.value = {value}")
                await browser.close()
                return value if value else None

            await page.wait_for_selector(selector, timeout=15000)
            elements = await page.query_selector_all(selector)
            values = []
            for el in elements:
                text = await el.inner_text()
                values.append(text.strip())
            print(f"[DEBUG] Найдено элементов: {len(values)}")
            await browser.close()
            return ", ".join(values) if values else None

        except Exception as e:
            print(f"[DEBUG] ОШИБКА: {type(e).__name__}: {e}")
            await browser.close()
            return None