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
from xinlan2 import checkMail

# 2,4
# 23,31,42,43,44,81

async def change_email(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq =  metadata['seq']
        secondary_email = metadata['secondary_email']
        x_password = metadata['x_password']
        res = openBrowser(browser_id)
        # print(res)
        ws = res['data']['ws']
        # print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://x.com/settings/your_twitter_data/account"
        page = await default_context.new_page()
        await page.goto(extension_url)
        # print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")

        try:
            await asyncio.sleep(5)
            if await page.locator("text=电子邮件").is_visible() == False:
                await page.wait_for_selector('input[type=password]',timeout=5000)
                await page.fill('input[type=password]',x_password)
                await page.get_by_role("button", name="确认").click()
            await page.locator('[data-testid="pivot"]', has_text="电子邮件").click()
            await page.wait_for_selector('text=更新邮件地址', timeout=30000)
            await page.click('text=更新邮件地址')
            await asyncio.sleep(1)
            await page.fill('input[type=password]',x_password)
            await page.click('text=下一步')
            await asyncio.sleep(1)
            await page.wait_for_selector('input[type=email]', timeout=30000)
            await page.fill('input[type=email]', secondary_email)
            await page.wait_for_selector('text=下一步', timeout=30000)
            await page.click('text=下一步')
            await asyncio.sleep(2)
            verfication_code = checkMail(secondary_email,'')
            if verfication_code == "没有发现匹配的邮件。":
                await asyncio.sleep(2)
                verfication_code = checkMail(secondary_email, '')
            print(verfication_code)
            await page.fill('input[name=verfication_code]', verfication_code)
            await page.wait_for_selector('text=验证', timeout=30000)
            await page.locator("//button//span[text()='验证']").click()
            print('hello')
        except Exception as e:
            print(e)
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
