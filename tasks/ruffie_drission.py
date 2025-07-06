from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def ruffie_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://task.ruffie.ai/referrals/beke40"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        page.get(extension_url)
        # if page.ele('text=Join Waitlist', timeout=5):
        #     page.ele('text=Join Waitlist').click()
        #     if page.ele('x://input[@placeholder="Enter your email"]', timeout=30):
        #         page.ele('x://input[@placeholder="Enter your email"]').wait(1).input(email)
        #         print(f"✅ 浏览器ID: {seq}, Join Waitlist")
        #         if page.ele('text=Join Waitlist', timeout=30):
        #             page.ele('text=Join Waitlist').click()
        #             page.wait(5)
        #             page.get(extension_url)
        if page.ele('text=Connect Wallet', timeout=5):
            page.ele('text=Connect Wallet').click()
            if handle_okx_popup(page, seq) == False:
                print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")
                return

        page.get('https://task.ruffie.ai/tasks')
        if page.ele('text=Daily Check-In', timeout=5):
            page.ele('text=Daily Check-In', timeout=2).click()
            print(f"✅ 浏览器ID: {seq}, Daily Check-In")

        page.wait(20)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
