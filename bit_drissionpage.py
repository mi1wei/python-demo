import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from DrissionPage._pages.chromium_page import ChromiumPage
from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from xinlan import checkMail
from time import sleep
from bit_playwright_threads import get_browser_metadata
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from tasks.ruffie_drission import ruffie_drission
from tasks.goblin_meme_drission import goblin_meme_drission
from tasks.monadscore_drission import monadscore_drission
from tasks.shelby_drission import shelby_drission
from tasks.pharosnetwork_drission import pharosnetwork_drission
from tasks.wardenprotocol_drission import  wardenprotocol_drission
from tasks.onefootball_drission import onefootball_drission
from tasks.zkverify import zkverify_drission
from chrome_extensions.yescaptcha import yescaptcha_drission
from tasks.sosovalue_drission import sosovalue_drission


def x_detect(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']

    extension_url = f"https://x.com/home"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        tweets = page.eles('x://div[@data-testid="tweetText"]', timeout=60)
        # for tweet in tweets:
        #     print(tweet.text)
        if len(tweets) > 0:
            ele = page.ele('x://span[contains(@class, "css-1jxf684") and contains(text(), "@")]')
            if ele:
                print(f"✅ 浏览器ID: {seq}, X 登陆状态正常 {ele.text}, 主页帖子数量: {len(tweets)}")
            else:
                print(f"✅ 浏览器ID: {seq}, X 登陆状态正常, 主页帖子数量: {len(tweets)}")

        else:
            print(f"❌ 浏览器ID: {seq}, X 登陆状态异常")
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)


def discord_detect(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']

    extension_url = f"https://discord.com/channels/@me"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.eles('text=在线', timeout=60):
            ele = page.ele('x://div[contains(@class, "hovered__")]')
            if ele:
                print(f"✅ 浏览器ID: {seq} , Discord {ele.text} 登陆状态正常")
            else:
                print(f"✅ 浏览器ID: {seq}, Discord 登陆状态正常")

        else:
            print(f"❌ 浏览器ID: {seq}, Discord 登陆状态异常")
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)


def nebulai_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://nebulai.network/opencompute?invite_by=Xpgd9P"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)

        if page.ele('text=Sign Up/Log In'):
            page.ele('text=Sign Up/Log In').click()
            page.ele('x://input[@name="email"]').input(email)
            page.ele('text=Send').click()

            print(f"✅ 浏览器ID: {seq}, 已发送验证码")
            sleep(6)

            code = checkMail(email, '')
            if code == '没有发现匹配的邮件。':
                sleep(6)
                code = checkMail(email, '')
            print(f"✅ 浏览器ID: {seq}, {code}")
            page.ele('x://input[@name="auth_code"]').input(code)
            page.ele('x://input[@type="checkbox"]').wait(1).click()
            page.ele('text=Log In / Sign Up').click()

        else:
            print(f"✅ 浏览器ID: {seq}, 已处于登录状态")

        icon_ele = page.ele('x://img[contains(@src, "mining_off.svg")]/..', timeout=10)
        if icon_ele:
            icon_ele.click()
            sleep(3)
            print(f"浏览器ID: {seq}, Already ON, click one times")
        else:
            icon_ele = page.ele('x://img[contains(@src, "mining_on.svg")]/..', timeout=10)
            icon_ele.click()
            icon_ele.click()
            print(f"浏览器ID: {seq}, Already ON, click two times")
            sleep(3)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)


# def wardenprotocol_drission(configuration: dict):
#     if len(configuration) < 10:
#         return
#
#     browser_id = configuration['browser_id']
#     seq = configuration['seq']
#     email = configuration['email']
#
#     extension_url = f"https://app.wardenprotocol.org/referral?code=93784"
#
#     co = ChromiumOptions()
#     res = openBrowser(browser_id)
#     co.set_address(res['data']['http'])
#     co.set_pref('profile.default_content_setting_values.notifications', 2)
#     chromium = Chromium(co)
#     page = chromium.latest_tab
#
#     try:
#         page.get(extension_url)
#         if page.ele('text=Continue with a chrome_extensions'):
#             page.ele('text=Continue with a chrome_extensions').click()
#             page.refresh()
#
#         if page.ele('text=Continue with a chrome_extensions'):
#             page.ele('text=Continue with a chrome_extensions', ).click()
#             if page.ele('text=OKX Wallet'):
#                 try:
#                     max_tries = 10  # 防止死循环，最多点击10次
#                     count = 0
#                     okx_tab = page.ele('text=OKX Wallet', timeout=2).click.for_new_tab()
#                     if okx_tab:
#                         if okx_tab.ele('x://input[@placeholder="请输入密码"]', timeout=5):
#                             okx_tab.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
#                         if okx_tab.ele('text=解锁', timeout=1):
#                             okx_tab.ele('text=解锁').wait(1).click()
#                         if okx_tab.ele('text=切换钱包', timeout=1):
#                             okx_tab.ele('text=切换钱包').wait(1).click()
#                             checkbox = okx_tab.ele('.okui-checkbox-circle')
#                             checkbox.click()
#                             if okx_tab.ele('text=确认', timeout=1):
#                                 okx_tab.ele('text=确认').wait(1).click()
#                             if okx_tab.ele('text=连接', timeout=1):
#                                 okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()
#                         if okx_tab.ele('text=连接', timeout=1):
#                             okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()
#
#                         while count < max_tries:
#                             confirm_btn = okx_tab.ele('text=确认', timeout=1)
#                             if not confirm_btn:
#                                 break
#                             confirm_btn.wait(1).click('js')
#                             count += 1
#                 except Exception as e:
#                     print(f'浏览器ID: {seq}, {e}')
#
#             page.wait(10)
#         else:
#             print(f"✅ 浏览器ID: {seq}, 已处于登录状态")
#     except Exception as e:
#         print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
#     finally:
#         page.close()
#         closeBrowser(browser_id)


def nebulai2_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://nebulai.network/opencompute?invite_by=Xpgd9P"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        page.wait(5)
        page.get(extension_url)

        page.ele('x://input[@name="email"]').wait(2).input(email)
        page.ele('text=Send').click()

        print(f"✅ 浏览器ID: {seq}, 已发送验证码")
        page.wait(10)

        code = checkMail(email, '')
        if code == '没有发现匹配的邮件。':
            page.wait(10)
            code = checkMail(email, '')
        print(f"✅ 浏览器ID: {seq}, {code}")
        page.ele('x://input[@name="verificationCode"]').input(code)
        page.ele('text=Link').wait(1).click()
        page.wait(5)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)


def cess_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://cess.network/deshareairdrop/"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        page.wait(5)
        page.get(extension_url)
        page.wait(5)
        page.get(extension_url)

        if page.ele('xpath://button[contains(@class, "bg-primary") and text()="Get"]', timeout=5):
            page.ele('xpath://button[contains(@class, "bg-primary") and text()="Get"]').click()
            if page.ele('text=OKX Wallet', timeout=5):
                page.ele('text=OKX Wallet').click()
                if page.ele('text=Accept', timeout=5):
                    try:
                        max_tries = 10  # 防止死循环，最多点击10次
                        count = 0
                        okx_tab = page.ele('text=Accept', timeout=2).click.for_new_tab()
                        if okx_tab:
                            if okx_tab.ele('x://input[@placeholder="请输入密码"]', timeout=5):
                                okx_tab.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
                            if okx_tab.ele('text=解锁', timeout=1):
                                okx_tab.ele('text=解锁').wait(1).click()
                            if okx_tab.ele('text=切换钱包', timeout=1):
                                okx_tab.ele('text=切换钱包').wait(1).click()
                                checkbox = okx_tab.ele('.okui-checkbox-circle')
                                checkbox.click()
                                if okx_tab.ele('text=确认', timeout=1):
                                    okx_tab.ele('text=确认').wait(1).click()
                                if okx_tab.ele('text=连接', timeout=1):
                                    okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()

                            while count < max_tries:
                                confirm_btn = okx_tab.ele('text=确认', timeout=1)
                                if not confirm_btn:
                                    break
                                confirm_btn.wait(1).click('js')
                                count += 1
                            page.wait(10)
                    except Exception as e:
                        print(f'浏览器ID: {seq}, {e}')
        else:
            print(f"✅ 浏览器ID: {seq}, Eligibility for Bitget Airdrop Done")

        page.wait(5)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)

def find_okx_tab(chromium: Chromium, retry: int = 5, interval: float = 1.0):
    """最多重试 retry 次查找 OKX 插件页"""
    for attempt in range(retry):
        for tab in chromium.tabs:
            if 'okx' in tab.title.lower() or 'okx' in tab.url.lower():
                return tab
        print(f"🔍 第 {attempt + 1}/{retry} 次未找到 OKX 插件页，等待 {interval}s 重试...")
        time.sleep(interval)
    return None


def taker_drission(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    private_key = metadata['okx_ethers_private_key']

    try:
        # 设置浏览器连接配置
        co = ChromiumOptions()
        res = openBrowser(browser_id)
        co.set_address(res['data']['http'])
        co.set_pref('profile.default_content_setting_values.notifications', 2)
        chromium = Chromium(co)
        page = chromium.latest_tab
        page.get("https://sowing.taker.xyz/")

        # 点击连接钱包
        if page.ele('text=Connect Wallet'):
            page.ele('text=Connect Wallet').click()
            page.ele('text=OKX Wallet').click()

        # 查找 OKX 插件页（重试5次）
        okx_tab = find_okx_tab(chromium, retry=5, interval=1.5)

        if not okx_tab:
            print(f"❌ 浏览器ID: {seq}, 重试5次后仍未找到 OKX 插件页面")
            return

        # 登录钱包
        if okx_tab.ele('input@placeholder=请输入密码'):
            okx_tab.ele('input@placeholder=请输入密码').input("12345678")
            okx_tab.ele('data-testid=okd-button').click()

        # 点击确认按钮
        while okx_tab.ele('text=确认'):
            okx_tab.ele('text=确认').click()
            time.sleep(0.3)

        print(f"✅ 浏览器ID: {seq}, 已完成钱包连接流程")

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
    finally:
        try:
            page.close()
            chromium.quit()
        except Exception as e:
            print(f"⚠️ 浏览器ID: {seq}, 清理失败: {e}")




def main():
    file_path = 'configuration/primary'  # 替换成实际路径
    # [20]
    metadatas = get_browser_metadata(file_path)[8:]

    # 设置并发线程数，比如最多同时运行 5 个任务
    max_workers = 1

    error_seq_id = []
    if error_seq_id:
        metadatas = [metadata for metadata in metadatas if metadata['seq'] in error_seq_id]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_metadata = {
            executor.submit(sosovalue_drission, metadata): metadata for metadata in metadatas
        }

        for future in as_completed(future_to_metadata):
            metadata = future_to_metadata[future]
            try:
                future.result()
            except Exception as exc:
                print(f"❌ 浏览器ID: {metadata['seq']}, 执行出错: {exc}")


if __name__ == "__main__":
    main()
