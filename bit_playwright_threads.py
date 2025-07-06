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
from base.okx import run_okx, run_okx_solana, yescaptcha
from base.metamask import ethers
from base.x import change_email
from tasks.sowing_taker_playwright import taker
from base.browser import get_browser_metadata


def get_value(row, index, default=""):
    """安全地从列表中获取值，超出范围时返回默认值"""
    return row[index] if len(row) > index else default


async def find_extension_page(context, extension_url: str):
    for page in context.pages:
        if extension_url in page.url:
            return page
    return None


def send_curl_request(code):
    url = f'https://2fa.fb.rip/api/otp/{code}'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('ok'):
            return data['data']['otp']
        print('请求成功，但数据格式不符合预期')
        return None
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


async def x_login(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq = metadata['seq']
        if len(metadata) < 7:
            return
        x_username = metadata['x_username']
        x_password = metadata['x_password']
        x_2fa_code = metadata['x_2fa']
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://x.com/"
        page = await default_context.new_page()
        await page.goto(extension_url, wait_until="load")
        try:
            await asyncio.sleep(2)
            count = await page.locator('text=登录').count()
            if count == 0:
                print(f"✅ X 已登录, 浏览器ID: {seq}")
                return
            await page.click('text=登录')
            await page.locator('input[name="text"]').fill(x_username)
            await page.click('text=下一步')
            await page.locator('input[name="password"]').fill(x_password)
            await page.click('text=登录')
            code = send_curl_request(x_2fa_code)
            if code is not None:
                await page.wait_for_selector('input[name="text"]', timeout=3000)
                await page.locator('input[name="text"]').fill(code)
                await page.click('text=下一步')
                await asyncio.sleep(5)
                print(f"✅ X 登录成功, 浏览器ID: {seq}")
            else:
                print(f"❌ 2fa code exchange token failed, 浏览器ID: {seq}")

        except Exception as e:
            print(f"❌ 操作过程中发生错误: {e}, 浏览器ID: {seq}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"⚠️ 关闭页面失败: {e}, 浏览器ID: {seq}")

            try:
                await browser.close()
            except Exception as e:
                print(f"⚠️ 关闭浏览器失败: {e}, 浏览器ID: {seq}")

            try:
                closeBrowser(browser_id)
            except Exception as e:
                print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")


async def discord_login(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq = metadata['seq']
        if len(metadata) < 10:
            return
        x_token = metadata['discord_2fa']
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://discord.com/login"
        page = await default_context.new_page()
        await page.goto(extension_url, wait_until="load")
        try:
            await asyncio.sleep(2)
            count = await page.locator('text=登录').count()
            if count == 0:
                print(f"✅ DC 已登录, 浏览器ID: {seq}")
                return

            # 方式1 邮箱, 密码, 2fa
            # await page.locator('input[name="email"]').fill(x_username)
            # await page.locator('input[name="password"]').fill(x_username)
            # await page.click('text=登录')

            # 方式2 token
            extension_url = f"chrome-extension://kfjglmgfjedhhcddpfgfogkahmenikan/popup/index.html"
            page = await default_context.new_page()
            await page.goto(extension_url)
            print(f"✅ OKX 插件页面已打开, 浏览器ID: {seq}")
            await page.get_by_placeholder('Paste your Discord token here').fill(x_token)
            await page.click('text=Login to Discord')
            await asyncio.sleep(5)



        except Exception as e:
            print(f"❌ 操作过程中发生错误: {e}, 浏览器ID: {seq}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"⚠️ 关闭页面失败: {e}, 浏览器ID: {seq}")

            try:
                await browser.close()
            except Exception as e:
                print(f"⚠️ 关闭浏览器失败: {e}, 浏览器ID: {seq}")

            try:
                closeBrowser(browser_id)
            except Exception as e:
                print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")


async def export_discord_token(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata[1]
        seq = metadata[0]
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://discord.com/login"
        page = await default_context.new_page()
        await page.goto(extension_url, wait_until="networkidle")
        try:
            await asyncio.sleep(2)
            count = await page.locator('text=登录').count()
            if count == 0:
                print(f"✅ DC 已登录, 浏览器ID: {seq}")
                local_storage = page.evaluate('''() => {
                                try {
                                    const storage = {};
                                    // 遍历所有 iframe
                                    const iframes = document.querySelectorAll('iframe');
                                    const allStorages = [localStorage];

                                    // 收集所有 iframe 的 Local Storage（如果允许访问）
                                    for (const iframe of iframes) {
                                        try {
                                            allStorages.push(iframe.contentWindow.localStorage);
                                        } catch (e) {
                                            console.warn('无法访问 iframe Local Storage:', e.message);
                                        }
                                    }

                                    // 合并所有 Local Storage
                                    for (const ls of allStorages) {
                                        for (let i = 0; i < ls.length; i++) {
                                            const key = ls.key(i);
                                            if (!storage[key]) {
                                                storage[key] = ls.getItem(key);
                                            }
                                        }
                                    }

                                    return storage;
                                } catch (e) {
                                    console.error('获取 Local Storage 失败:', e);
                                    return null;
                                }
                            }''')
                for key, value in local_storage.items():
                    print(f"{key}: {value}")
                print(local_storage)
                return
            else:
                print(f"❌ DC 未登录, 浏览器ID: {seq}")


        except Exception as e:
            print(f"❌ 操作过程中发生错误: {e}, 浏览器ID: {seq}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"⚠️ 关闭页面失败: {e}, 浏览器ID: {seq}")

            try:
                await browser.close()
            except Exception as e:
                print(f"⚠️ 关闭浏览器失败: {e}, 浏览器ID: {seq}")

            # try:
            #     closeBrowser(browser_id)
            # except Exception as e:
            #     print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")


async def run_cess(playwright: Playwright, row: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = row[1]
        seq = row[0]
        private_key = row[2]
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://cess.network/deshareairdrop/"
        page = await default_context.new_page()
        await page.goto(extension_url, wait_until="networkidle")
        print(f"✅ CESS 插件页面已打开, 浏览器ID: {seq}")

        cards = page.locator('div.px-6.bg-boxblue')
        count = await cards.count()
        print(count)
        results = []
        for i in range(count):
            card = cards.nth(i)
            task_locator = card.locator('p.text-\\[16px\\]')
            if await task_locator.count() > 0:
                task_name = (await task_locator.nth(0).inner_text()).strip()
            else:
                task_name = "Unknown task name"

            btn_locator = card.locator('button')
            btn_count = await btn_locator.count()
            if btn_count > 0:
                btn_text = (await btn_locator.nth(0).inner_text()).strip()
                results.append({"task": task_name, "status": btn_text, "button": btn_locator})
            else:
                # 没按钮则检查是否有成功图标
                success_count = await card.locator('img[alt="icon_success"]').count()
                btn_text = "✅ Completed" if success_count > 0 else "No action"
                results.append({"task": task_name, "status": btn_text, "button": None})

        for result in results:
            # if result['button'] is not None and result["task"] == "Quiz challenge: What is CESS?":
            #     await result["button"].nth(0).click()
            #     answers = [
            #         "2019",  # 1. In which year was CESS team formed?
            #         "Storage",  # 2. CESS Network has 4 types of nodes...
            #         "gateway",  # 3. DeOSS is the ___ to the CESS Network.
            #         "Proof of Data Reduplication and Recovery (PoDR)",  # 4. Mechanism to prevent data loss
            #         "2021",  # 5. In which year was CESS Testnet v0.1 launched
            #         "Trusted Execution Environment (TEE)",  # 6. PoDR executed within ___
            #         "Retrieval",  # 7. Distributed content delivery includes ___ Node
            #         "11",  # 8. How many validators in Random Rotational Selection?
            #         "circulation",  # 9. Proxy Re-encryption secures the ___ of data
            #         "3"  # 10. How many SDKs does CESS support?
            #     ]
            #     await page.wait_for_selector("textarea")
            #     # 找到所有 textarea 元素
            #     textareas = await page.query_selector_all("textarea")
            #
            #     # 输入答案
            #     for i, textarea in enumerate(textareas):
            #         if i < len(answers):
            #             await textarea.fill(answers[i])
            #             await asyncio.sleep(0.3)
            #     submit_button = await page.query_selector("button:text('Submit')")
            #     if submit_button:
            #         await submit_button.click()
            #     else:
            #         print("❌ Submit button not found.")
            #     print('1')
            if result["task"] == "Join Discord":
                await result["button"].nth(0).click()
                await asyncio.sleep(60)

        print(results)


async def assisterr(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata[1]
        seq = metadata[0]
        if len(metadata) < 10:
            return
        x_username = metadata[7]
        x_password = metadata[8]
        x_token = metadata[9]
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://build.assisterr.ai/dashboard"
        page = await default_context.new_page()
        try:
            await page.goto(extension_url, wait_until="load")
            try:
                come_back = await page.wait_for_selector('text=Come back in', timeout=30000)
                if come_back:
                    print(f'签到任务今天已经做过了 浏览器ID: {seq}')
                else:
                    await page.wait_for_selector('text=Grab Daily Tokens', timeout=5000, state='attached')
                    button = page.locator('text=Grab Daily Tokens')
                    if await button.is_visible():
                        await button.click()
                    else:
                        print(f"按钮是 disabled，不执行点击操作 浏览器ID: {seq}")

                buttons = page.locator('button', has_text="$ASRR")
                count = await buttons.count()
                #
                # task_elements = page.locator('div.text-secondary-700.font-semibold')
                #
                # # 获取任务数量
                # task_count = await task_elements.count()
                #
                # # 提取所有任务名
                # task_names = []
                # for i in range(task_count):
                #     task_name = await task_elements.nth(i).text_content()
                #     if task_name:
                #         task_names.append(task_name.strip())
                #
                # print("任务名列表：", task_names)

                if count == 2:
                    for i in range(count - 1):
                        await buttons.nth(i).click()
                        await page.wait_for_selector('text=授权应用', timeout=60000)
                        await page.click('text=授权应用')
                        await page.wait_for_selector('text=Discord Auth', timeout=60000)
                        await page.click('text=Discord Auth')
                        await page.wait_for_selector('text=Assister Incentive', timeout=60000)
                        await page.evaluate('''() => {
                                           setTimeout(() => {
                                               const div = document.querySelector('.content__49fc1');
                                               if (div) {
                                                   div.scrollTop = div.scrollHeight;
                                                   console.log('已滚动到底部');
                                               }
                                           }, 100);
                                       }''')
                        await page.wait_for_selector('text=授权', timeout=30000)
                        await page.locator('button', has_text="授权").click()
                        await page.wait_for_selector('text=Start building', timeout=30000)
                        await page.click('text=Start building')
                else:
                    for i in range(count):
                        if i == 0:
                            try:
                                await buttons.nth(i).click()
                                await page.wait_for_selector('text=授权应用', timeout=60000)
                                await page.click('text=授权应用')
                                await page.goto(extension_url)
                            except Exception as e:
                                continue
                        else:
                            await buttons.nth(i).click()
            except Exception as e:
                print(f"❌ 操作过程中发生错误: {e}, 浏览器ID: {seq}")
                error_browser_seq.append(seq)
            finally:
                try:
                    if not page.is_closed():
                        await page.close()
                except Exception as e:
                    print(f"⚠️ 关闭页面失败: {e}, 浏览器ID: {seq}")
                try:
                    await browser.close()
                except Exception as e:
                    print(f"⚠️ 关闭浏览器失败: {e}, 浏览器ID: {seq}")
                try:
                    closeBrowser(browser_id)
                except Exception as e:
                    print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")

        except Exception as e:
            print(f'目标网页打开失败: {e} 浏览器ID: {seq}')


async def prdt(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq = metadata['seq']
        if len(metadata) < 10:
            return
        email = metadata['email']
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://mining.prdt.finance?referralCode=L6GKIM5WU"
        page = await default_context.new_page()
        await page.goto(extension_url, wait_until="load")
        try:
            await page.click('text=Connect')
            await page.click('text=OKX Wallet')
            await page.fill('input[placeholder="Your Email Address"]', email)
            await page.click('text=Send Verification Link')
            await asyncio.sleep(3)
        except Exception as e:
            print(f"❌ 操作过程中发生错误: {e}, 浏览器ID: {seq}")
            error_browser_seq.append(seq)
        finally:
            try:
                if not page.is_closed():
                    await page.close()
            except Exception as e:
                print(f"⚠️ 关闭页面失败: {e}, 浏览器ID: {seq}")

            try:
                await browser.close()
            except Exception as e:
                print(f"⚠️ 关闭浏览器失败: {e}, 浏览器ID: {seq}")

            try:
                closeBrowser(browser_id)
            except Exception as e:
                print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")


async def nebulai(playwright: Playwright, metadata: list, semaphore: asyncio.Semaphore):
    async with semaphore:
        browser_id = metadata['browser_id']
        seq = metadata['seq']
        if len(metadata) < 10:
            return
        email = metadata['email']
        res = openBrowser(browser_id)
        ws = res['data']['ws']
        print(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]

        extension_url = f"https://nebulai.network/opencompute?invite_by=Xpgd9P"
        page = await default_context.new_page()
        # await stealth_async(page)
        # with open('stealth.min.js', 'r') as f:
        #     js = f.read()
        # await page.add_init_script(js)
        try:
            await page.goto(extension_url, wait_until="load")

            try:
                if await page.locator("text=Sign Up/Log In").is_visible():
                    await page.click('text=Sign Up/Log In')
                    await page.wait_for_selector('text=Verification log in', timeout=60000)
                    await page.fill('input[placeholder="Email Address"]', email)
                    await page.click('text=Send')
                    # await page.wait_for_load_state("networkidle")
                    # await page.wait_for_timeout(3000)
                    #
                    # await page.locator('input[type="checkbox"]').click()
                    # print({seq}, checkMail(email,''))
                    await browser.close()
                    await asyncio.sleep(10)
                    print(f"  ✅ 浏览器ID: {seq}, {checkMail(metadata['email'], '')}")
                    return
                else:
                    print(f"  ✅ 浏览器ID: {seq}, nebulai 处于登录中")

                icon_locator = page.locator("img[src='/openCompute/mining_off.svg']")
                if await icon_locator.count() > 0:
                    # 点击它的包裹容器
                    await icon_locator.locator("xpath=ancestor::div[contains(@class, 'cursor-pointer')]").click()
                    print("Clicked to turn ON")
                else:
                    print("Already ON, no click needed.")
                # await locator.locator("xpath=ancestor::div[1]").click()

            except Exception as e:
                print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
                error_browser_seq.append(seq)
            finally:
                pass
                # try:
                #     if not page.is_closed():
                #         await page.close()
                # except Exception as e:
                #     print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")
                # try:
                #     await browser.close()
                # except Exception as e:
                #     print(f"⚠️ 浏览器ID: {seq}, 关闭浏览器失败: {e}")
                # try:
                #     closeBrowser(browser_id)
                # except Exception as e:
                #     print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")

        except Exception as e:
            print(f'浏览器ID: {seq}, 目标网页打开失败: {e}')

    print(checkMail(metadata['email'], ''))


async def run(playwright: Playwright, metadatas: list, max_concurrent_tasks: int):
    # 假设我们有多个浏览器窗口ID要处理
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    tasks = []

    error_seq_id = [7,11]
    if error_seq_id:
        metadatas = [metadata for metadata in metadatas if metadata['seq'] in error_seq_id]

    for metadata in metadatas:
        task = discord_login(playwright, metadata, semaphore)

        tasks.append(task)

    await asyncio.gather(*tasks)
    if len(error_browser_seq) > 0:
        print("❌ 操作失败的浏览器ID列表:", error_browser_seq)


async def main():
    file_path = 'configuration/primary'  # 替换成实际的文件路径
    metadatas = get_browser_metadata(file_path)

    # 设置最大并发任务数
    max_concurrent_tasks = 3  # 你可以根据需要调整并发数量

    async with async_playwright() as playwright:
        await run(playwright, metadatas, max_concurrent_tasks)


if __name__ == "__main__":
    asyncio.run(main())
