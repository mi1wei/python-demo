from bit_api import *
import time
import asyncio
import logging
from playwright.async_api import async_playwright, Playwright
from playwright.async_api import Playwright, TimeoutError as PlaywrightTimeoutError
from concurrent.futures import ThreadPoolExecutor
import csv
from xinlan import checkMail
from base.error import error_browser_seq

async def find_extension_page(context, extension_url: str):
    for page in context.pages:
        if extension_url in page.url:
            return page
    return None



async def taker(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq =  metadata['seq']
        private_key = metadata['okx_ethers_private_key']
        res = openBrowser(browser_id)
        # print(res)
        ws = res['data']['ws']
        # print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://sowing.taker.xyz/"
        page = await default_context.new_page()
        await page.goto(extension_url)
        # print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")

        try:
            await page.get_by_role('button',name='Connect Wallet').click()
            await page.click('text=OKX Wallet')
            okx = await find_extension_page(default_context,'mcohilncbfahbmgdjkbpemcciiolgcge')
            if okx is None:
                await asyncio.sleep(1)
                okx = await find_extension_page(default_context, 'mcohilncbfahbmgdjkbpemcciiolgcge')
            await okx.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
            await okx.fill('input[placeholder="请输入密码"]', "12345678")
            await okx.click('[data-testid="okd-button"]')
            await okx.get_by_role("button", name="连接").click()
            while True:
                locator = okx.get_by_role("button", name="确认")
                if await locator.is_visible():
                    await locator.click()
                    await okx.wait_for_timeout(300)
                else:
                    break
            await okx.get_by_role("button", name="确认").click()
        except Exception as e:
            print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")

            try:
                await browser.close()
            except Exception as e:
                print(f"⚠️ 浏览器ID: {seq}, 关闭浏览器失败: {e}")

            # try:
            #     closeBrowser(browser_id)
            # except Exception as e:
            #     print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")

async def run_okx_solana(playwright: Playwright, row: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = row['browser_id']
        seq = row['seq']
        private_key = row['okx_solana_private_key']

        res = openBrowser(browser_id)
        ws = res['data']['ws']

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
        page = await default_context.new_page()
        await page.goto(extension_url)
        # print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")

        try:
            login = False
            try:
                await page.wait_for_selector("text=发送", timeout=3000)
                send_count = await page.locator("text=发送").count()
                if send_count > 0:
                    print(f"🔑 浏览器ID: {seq}, 钱包处于登录态")
                    login = True
            except PlaywrightTimeoutError:
                pass

            if login == False:
                try:
                    # 等待文本“请输入密码”出现，设置一个短超时避免卡住
                    await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=5000)
                    await page.fill('input[placeholder="请输入密码"]', "12345678")
                    await page.click('[data-testid="okd-button"]')
                    print(f"✅ 浏览器ID: {seq}, 已点击『解锁』按钮")
                except PlaywrightTimeoutError:
                    error_browser_seq.append(seq)
                    print(f"❌ 浏览器ID: {seq}, 导入solana钱包失败, 先导入OKX钱包")
                    return

            # 等待按钮出现，确保页面渲染完毕
            await page.click('text=私钥')
            await page.wait_for_selector('._detail_1ke1k_5', timeout=3000)
            keys = await page.query_selector_all('._detail_1ke1k_5')
            if len(keys) == 2:
                print(f"✅ 浏览器ID: {seq}, solana钱包已导入")
                return

            if len(keys) == 3:
                print(f"⚠️ 浏览器ID: {seq}, 存在多余的钱包, 请确认")
                return

            await page.wait_for_selector('[data-testid="chrome_extensions-management-page-add-chrome_extensions-button"]', timeout=5000)
            await page.click('[data-testid="chrome_extensions-management-page-add-chrome_extensions-button"]')
            print(f"  ✅ 浏览器ID: {seq}, 已点击『确认』按钮")

            await page.wait_for_selector("text=导入已有钱包", timeout=5000)
            await page.click("text=导入已有钱包")
            print(f"  ✅ 浏览器ID: {seq}, 已点击『导入已有钱包』按钮")

            # 等待按钮出现，确保页面渲染完毕
            await page.wait_for_selector("text=助记词或私钥", timeout=5000)

            if await page.locator("div[data-pane-id='2'][data-e2e-okd-tabs-pane-active='true']").count() == 0:
                await page.locator("div[data-pane-id='2']").click()
                print(f"  ✅ 浏览器ID: {seq}, 已点击『私钥』按钮")
            else:
                print(f"  ✅ 浏览器ID: {seq}, 已处于『私钥』tab，无需点击")

            await page.locator("textarea[placeholder='粘贴或输入你的私钥']").fill(private_key)

            # 点击确认
            await page.locator("text=确认").click()

            await page.locator("text=确认").click()
            print(f"  ✅ 浏览器ID: {seq}, 导入solana钱包成功")
        except Exception as e:
            print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"  ⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")

            try:
                await browser.close()
            except Exception as e:
                print(f"  ⚠️ 浏览器ID: {seq}, 关闭浏览器失败: {e}")

            # try:
            #     closeBrowser(browser_id)
            # except Exception as e:
            #     print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")

async def yescaptcha(playwright: Playwright, row: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = row['browser_id']
        seq = row['seq']
        private_key = row['okx_solana_private_key']

        res = openBrowser(browser_id)
        ws = res['data']['ws']

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"chrome-extension://jiofmdifioeejeilfkpegipdjiopiekl/popup/index.html"
        page = await default_context.new_page()
        await page.goto(extension_url)
        # print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")

        try:
            await page.fill('input[type=text]','eb11154eadd3f19b47591b2d226bae3ec57c88cf68722')
            try:
                await page.wait_for_selector('text=保存', timeout=3000)
                await page.click('text=保存')
                await asyncio.sleep(3)
            except Exception as e:
                pass
            await page.get_by_role("checkbox", name="Cloudflare").click()
            await page.get_by_role("checkbox", name="文字验证码").click()
            if await page.locator("text=余额").is_visible():
                print(f"  ✅ 浏览器ID: {seq}, YesCaptcha人机助手导入成功")
            else:
                print(f"  ❌ 浏览器ID: {seq}, YesCaptcha人机助手导入失败")
        except Exception as e:
            print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"  ⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")

            try:
                await browser.close()
            except Exception as e:
                print(f"  ⚠️ 浏览器ID: {seq}, 关闭浏览器失败: {e}")

            try:
                closeBrowser(browser_id)
            except Exception as e:
                print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")
