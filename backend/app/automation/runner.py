from playwright.async_api import async_playwright


async def execute_browser(job_id, url, manager):
    browser = None

    try:
        playwright = await async_playwright().start()

        browser = await playwright.chromium.launch(headless=True)

        await manager.send_log(job_id, {
            "event": "browser.launched",
            "message": "Chromium launched"
        })

        page = await browser.new_page()

        await manager.send_log(job_id, {
            "event": "page.navigating",
            "message": f"Navigating to {url}"
        })

        await page.goto(url)

        await manager.send_log(job_id, {
            "event": "page.loaded",
            "message": "Page loaded successfully"
        })

        products = await page.locator("article.product_pod").all()

        data = []
        for product in products:
            title = await product.locator("h3 a").get_attribute("title")
            price = await product.locator(".price_color").inner_text()

            data.append({
                "title": title,
                "price": price
            })

        await manager.send_log(job_id, {
            "event": "data.extracted",
            "message": f"Extracted {len(data)} products"
        })

        screenshot_path = f"screenshots/{job_id}.png"

        await page.screenshot(path=screenshot_path)

        await manager.send_log(job_id, {
            "event": "screenshot.captured",
            "message": "Screenshot captured"
        })

        return {
            "products": data,
            "screenshot": screenshot_path
        }

    finally:
        if browser:
            await browser.close()