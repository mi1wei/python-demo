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


async def ethers(playwright: Playwright, metadata: dict, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq = metadata['seq']
        mnemonic = metadata['metamask_ethers_mnemonic']
        res = openBrowser(browser_id)
        # print(res)
        ws = res['data']['ws']
        # print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome"
        page = await default_context.new_page()
        await page.goto(extension_url)
        # print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")

        try:
            # try:
            #     await page.wait_for_selector("text=发送", timeout=3000)
            #     send_count = await page.locator("text=发送").count()
            #     if send_count > 0:
            #         print(f"🔑 浏览器ID: {seq}, 钱包处于登录态")
            #         return
            # except PlaywrightTimeoutError:
            #     pass
            #
            # try:
            #     # 输入密码进行登录
            #     await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
            #     await page.fill('input[placeholder="请输入密码"]', "12345678")
            #     await page.click('[data-testid="okd-button"]')
            #     print(f"✅ 浏览器ID: {seq}, 已点击『解锁』按钮")
            #     return
            # except PlaywrightTimeoutError:
            #     print(f"✅ 浏览器ID: {seq}, 开始导入钱包")

            await page.wait_for_selector("text=我同意MetaMask的使用条款", timeout=6000)
            await page.click("input[type=checkbox]")
            await page.click("text=导入现有钱包")
            print(f"✅ 浏览器ID: {seq}, 已点击『导入现有钱包』按钮")

            await page.click("text=我同意")
            print(f"✅ 浏览器ID: {seq}, 已点击『助记词或私钥』按钮")

            # 等待按钮出现，确保页面渲染完毕
            words = mnemonic.split()
            for i, word in enumerate(words):
                selector = f'input[data-testid="import-srp__srp-word-{i}"]'
                await page.fill(selector, word)

            await page.get_by_test_id("import-srp-confirm").click()
            print(f"✅ 浏览器ID: {seq}, 已点击『确认私钥助记词』按钮")

            await page.get_by_test_id('create-password-new').fill('12345678')
            await page.get_by_test_id('create-password-confirm').fill('12345678')

            await page.wait_for_selector("text=我明白 MetaMask 无法为我恢复此密码", timeout=6000)
            await page.click("input[type=checkbox]")

            await page.click("text=导入我的钱包")
            print(f"✅ 浏览器ID: {seq}, 已点击『导入我的钱包』按钮")

            await page.click("text=完成")
            print(f"✅ 浏览器ID: {seq}, 导入MetaMask钱包成功")
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

async def ethers_sui(playwright: Playwright, row: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = row[1]
        seq = row[0]
        private_key = row[3]

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
            try:
                await page.wait_for_selector("text=发送", timeout=3000)
                send_count = await page.locator("text=发送").count()
                if send_count > 0:
                    print(f"🔑 浏览器ID: {seq}, 钱包处于登录态")
                else:
                    try:
                        # 等待文本“请输入密码”出现，设置一个短超时避免卡住
                        await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=3000)
                        await page.fill('input[placeholder="请输入密码"]', "12345678")
                        await page.click('[data-testid="okd-button"]')
                        print(f"✅ 浏览器ID: {seq}, 已点击『解锁』按钮")
                    except PlaywrightTimeoutError:
                        error_browser_seq.append(seq)
                        print(f"❌ 浏览器ID: {seq}, 导入solana钱包失败, 先导入OKX钱包")
                        return
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
