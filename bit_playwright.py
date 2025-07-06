from bit_api import *
import time
import asyncio
from playwright.async_api import async_playwright, Playwright
from playwright.async_api import TimeoutError


async def wait_until_page_navigated(page, timeout=5000):
    """等待页面从 about:blank 跳转到真实扩展页面"""
    start = time.time()
    while time.time() - start < timeout / 1000:
        if page.url != "about:blank":
            return
        await asyncio.sleep(0.1)
    raise TimeoutError("页面未跳转出 about:blank")


async def on_new_page(page):
    print(f"🆕 新窗口打开：{page.url}")


async def run_okx(playwright: Playwright):
    # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
    browser_id = "f21a50f8ca464a97a78ba4dc9e1db99d"  # 窗口ID从窗口配置界面中复制，或者api创建后返回
    res = openBrowser(browser_id)
    ws = res['data']['ws']
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    # browser.on("context", lambda context: context.on("page", on_new_page))
    # for context in browser.contexts:
    #     context.on("page", on_new_page)

    extension_url = f"chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
    page = await default_context.new_page()
    await page.goto(extension_url)
    print("✅ OKX 插件页面已打开")

    # for idx, page in enumerate(default_context.pages):
    #   print(f"🔍 Page {idx + 1}:")
    #   print(f"   URL      : {page.url}")
    #   print(f"   Title    : {await page.title()}")

    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            await asyncio.sleep(1)

            # 先判断“发送”或“接收”文字是否存在，说明登录态
            send_count = await page.locator("text=发送").count()
            receive_count = await page.locator("text=接收").count()

            if send_count > 0 or receive_count > 0:
                print("🔑 钱包处于登录态")
                return

            try:
                # 等待文本“请输入密码”出现，设置一个短超时避免卡住
                await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
                await page.fill('input[placeholder="请输入密码"]', "12345678")
                print("✅ 输入密码", 12345678)

                await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
                await page.click('[data-testid="okd-button"]')
                print("✅ 已点击『解锁』按钮")
                print("🔑 钱包处于登录态")
                return
            except TimeoutError:
                print("✅ 页面未提示输入密码")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=导入已有钱包", timeout=5000)

            # 点击“导入已有钱包”按钮
            await page.click("text=导入已有钱包")
            print("✅ 已点击『导入已有钱包』按钮")

            await page.click("text=助记词或私钥")
            print("✅ 已点击『助记词或私钥』按钮")

            break

    default_context = browser.contexts[0]
    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=助记词或私钥", timeout=5000)

            if await page.locator("div[data-pane-id='2'][data-e2e-okd-tabs-pane-active='true']").count() == 0:
                await page.locator("div[data-pane-id='2']").click()
                print("✅ 已点击『私钥』按钮")
            else:
                print("✅ 已处于『私钥』tab，无需点击")

            await page.locator("textarea[placeholder='粘贴或输入你的私钥']").fill(
                "t7V6sKeCq8DVrmf7tcBp26HLqCsEsDQjE9cY7onyffX7hzzg8koPiDsHXGwpQnmYHUptE5CLt7Brf4XKs5TLsZj")

            # 点击确认
            await page.locator("text=确认").click()

            await page.locator("text=确认").click()
            print("✅ 选择网络确认")

            await page.locator("text=下一步").click()
            print("✅ 密码验证确认")

            await page.wait_for_selector('input[placeholder="最少输入 8 个字符"]', timeout=5000)
            await page.fill('input[placeholder="最少输入 8 个字符"]', "12345678")

            await page.wait_for_selector('input[placeholder="请再次输入确认"]', timeout=5000)
            await page.fill('input[placeholder="请再次输入确认"]', "12345678")

            await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
            await page.click('[data-testid="okd-button"]')
            print("✅ 已点击『确认』按钮")

            await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
            await page.click('[data-testid="okd-button"]')
            print("✅ 已点击『开启你的 Web3 之旅』按钮")

            break

    await asyncio.sleep(10)
    #
    # print('new page and goto baidu')
    # page = await default_context.new_page()
    # await page.goto('https://baidu.com')
    #
    # time.sleep(2)

    print('clsoe page and browser')
    await page.close()

    time.sleep(2)
    # closeBrowser(browser_id)

async def run_okx_solana(playwright: Playwright):
    # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
    browser_id = "f21a50f8ca464a97a78ba4dc9e1db99d"  # 窗口ID从窗口配置界面中复制，或者api创建后返回
    res = openBrowser(browser_id)
    ws = res['data']['ws']
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    # browser.on("context", lambda context: context.on("page", on_new_page))
    # for context in browser.contexts:
    #     context.on("page", on_new_page)

    extension_url = f"chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
    page = await default_context.new_page()
    await page.goto(extension_url)
    print("✅ OKX 插件页面已打开")

    # for idx, page in enumerate(default_context.pages):
    #   print(f"🔍 Page {idx + 1}:")
    #   print(f"   URL      : {page.url}")
    #   print(f"   Title    : {await page.title()}")

    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            await asyncio.sleep(1)

            # 先判断“发送”或“接收”文字是否存在，说明登录态
            send_count = await page.locator("text=发送").count()
            receive_count = await page.locator("text=接收").count()

            if send_count > 0 or receive_count > 0:
                print("🔑 钱包处于登录态")

            else:
                try:
                    # 等待文本“请输入密码”出现，设置一个短超时避免卡住
                    await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
                    await page.fill('input[placeholder="请输入密码"]', "12345678")
                    print("✅ 输入密码", 12345678)

                    await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
                    await page.click('[data-testid="okd-button"]')
                    print("✅ 已点击『解锁』按钮")
                    print("🔑 钱包处于登录态")
                except TimeoutError:
                    print("✅ 页面未提示输入密码")

            # 等待按钮出现，确保页面渲染完毕
            await page.click('img[alt="chrome_extensions-avatar"]');

            await page.wait_for_selector('[data-testid="chrome_extensions-management-page-add-chrome_extensions-button"]', timeout=5000)
            await page.click('[data-testid="chrome_extensions-management-page-add-chrome_extensions-button"]')
            print("✅ 已点击『确认』按钮")

            await page.wait_for_selector("text=导入已有钱包", timeout=5000)
            await page.click("text=导入已有钱包")
            print("✅ 已点击『导入已有钱包』按钮")

            break

    default_context = browser.contexts[0]
    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=助记词或私钥", timeout=5000)

            if await page.locator("div[data-pane-id='2'][data-e2e-okd-tabs-pane-active='true']").count() == 0:
                await page.locator("div[data-pane-id='2']").click()
                print("✅ 已点击『私钥』按钮")
            else:
                print("✅ 已处于『私钥』tab，无需点击")

            await page.locator("textarea[placeholder='粘贴或输入你的私钥']").fill(
                "3mGCmYbdDn5aRpZJU7MHPZQmfiyf46NDmMn79zpNsZRFuqevbjARvhJWsPeJH48fnymMCWu4L7p8axD5GVckpx8X")

            # 点击确认
            await page.locator("text=确认").click()

            await page.locator("text=确认").click()
            print("✅ 选择网络确认")

            # 打印okx所有钱包
            # send_count = await page.locator("text=发送").count()
            # receive_count = await page.locator("text=接收").count()
            #
            # if send_count > 0 or receive_count > 0:
            #     await page.click('img[alt="chrome_extensions-avatar"]')


    await asyncio.sleep(10)
    #
    # print('new page and goto baidu')
    # page = await default_context.new_page()
    # await page.goto('https://baidu.com')
    #
    # time.sleep(2)

    print('clsoe page and browser')
    await page.close()

    time.sleep(2)
    # closeBrowser(browser_id)

async def run_metamask(playwright: Playwright):
    # /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
    browser_id = "f21a50f8ca464a97a78ba4dc9e1db99d"  # 窗口ID从窗口配置界面中复制，或者api创建后返回
    res = openBrowser(browser_id)
    ws = res['data']['ws']
    print("ws address ==>>> ", ws)

    chromium = playwright.chromium
    browser = await chromium.connect_over_cdp(ws)
    default_context = browser.contexts[0]

    # browser.on("context", lambda context: context.on("page", on_new_page))
    # for context in browser.contexts:
    #     context.on("page", on_new_page)

    extension_url = f"chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
    page = await default_context.new_page()
    await page.goto(extension_url)
    print("✅ OKX 插件页面已打开")

    # for idx, page in enumerate(default_context.pages):
    #   print(f"🔍 Page {idx + 1}:")
    #   print(f"   URL      : {page.url}")
    #   print(f"   Title    : {await page.title()}")

    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            await asyncio.sleep(1)

            # 先判断“发送”或“接收”文字是否存在，说明登录态
            send_count = await page.locator("text=发送").count()
            receive_count = await page.locator("text=接收").count()

            if send_count > 0 or receive_count > 0:
                print("🔑 钱包处于登录态")
                return

            try:
                # 等待文本“请输入密码”出现，设置一个短超时避免卡住
                await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
                await page.fill('input[placeholder="请输入密码"]', "12345678")
                print("✅ 输入密码", 12345678)

                await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
                await page.click('[data-testid="okd-button"]')
                print("✅ 已点击『解锁』按钮")
                print("🔑 钱包处于登录态")
                return
            except TimeoutError:
                print("✅ 页面未提示输入密码")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=导入已有钱包", timeout=5000)

            # 点击“导入已有钱包”按钮
            await page.click("text=导入已有钱包")
            print("✅ 已点击『导入已有钱包』按钮")

            await page.click("text=助记词或私钥")
            print("✅ 已点击『助记词或私钥』按钮")

            break

    default_context = browser.contexts[0]
    for page in default_context.pages:
        if "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html" in page.url:
            print("🎯 找到 OKX 插件页面")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=助记词或私钥", timeout=5000)

            if await page.locator("div[data-pane-id='2'][data-e2e-okd-tabs-pane-active='true']").count() == 0:
                await page.locator("div[data-pane-id='2']").click()
                print("✅ 已点击『私钥』按钮")
            else:
                print("✅ 已处于『私钥』tab，无需点击")

            await page.locator("textarea[placeholder='粘贴或输入你的私钥']").fill(
                "t7V6sKeCq8DVrmf7tcBp26HLqCsEsDQjE9cY7onyffX7hzzg8koPiDsHXGwpQnmYHUptE5CLt7Brf4XKs5TLsZj")

            # 点击确认
            await page.locator("text=确认").click()

            await page.locator("text=确认").click()
            print("✅ 选择网络确认")

            await page.locator("text=下一步").click()
            print("✅ 密码验证确认")

            await page.wait_for_selector('input[placeholder="最少输入 8 个字符"]', timeout=5000)
            await page.fill('input[placeholder="最少输入 8 个字符"]', "12345678")

            await page.wait_for_selector('input[placeholder="请再次输入确认"]', timeout=5000)
            await page.fill('input[placeholder="请再次输入确认"]', "12345678")

            await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
            await page.click('[data-testid="okd-button"]')
            print("✅ 已点击『确认』按钮")

            await page.wait_for_selector('[data-testid="okd-button"]', timeout=5000)
            await page.click('[data-testid="okd-button"]')
            print("✅ 已点击『开启你的 Web3 之旅』按钮")

            break

    await asyncio.sleep(10)
    #
    # print('new page and goto baidu')
    # page = await default_context.new_page()
    # await page.goto('https://baidu.com')
    #
    # time.sleep(2)

    print('clsoe page and browser')
    await page.close()

    time.sleep(2)
    # closeBrowser(browser_id)


async def main():
    async with async_playwright() as playwright:
        await run_okx(playwright)


asyncio.run(main())
