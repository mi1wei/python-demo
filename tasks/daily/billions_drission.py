from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx
from base.error import error_browser_seq
from chrome_extensions.google import google_reauthorize


# BILLIONS500K
# SENTIENTXBILLIONS
# BILLIONS400POINTS
def billions_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['google_username']

    extension_url = f"https://signup.billions.network?rc=EUKZZZF4"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('text=Google', timeout=10):
            page.ele('text=Google').wait(1).click('js')
            page.wait(5)
            google_reauthorize(chromium, metadata)
            page.wait(10)

        if page.ele('x:(//div[@class="ant-flex css-orst1n ant-flex-justify-center"]//button)[3]', timeout=3):
            page.ele('x:(//div[@class="ant-flex css-orst1n ant-flex-justify-center"]//button)[3]').click('js')
            page.wait(10)

        # 签到
        if page.ele('text=Click & Earn ', timeout=10):
            page.ele('text=Click & Earn ').wait(1).click('js')
            print(f'✅ 浏览器ID: {seq}, Dally Reward')

        # if page.ele('x://input[@placeholder="Enter code"]', timeout=60):
        #     codes = [
        #         "BILLIONS500K",
        #         "SENTIENTXBILLIONS",
        #         "BILLIONS400POINTS"
        #     ]
        #     for code in codes:
        #         code_input = page.ele('x://input[@placeholder="Enter code"]').clear()
        #         code_input.input(code)
        #         page.ele('text=Apply').wait(1).click('js')
        #         page.wait(5)

        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
