from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
import random
import string

def generate_coin_name(length=10):
    chars = string.ascii_uppercase + string.digits  # 大写字母 + 数字
    return ''.join(random.choices(chars, k=length))

def wardenprotocol_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://app.wardenprotocol.org/referral?code=93784"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('text=Continue with a chrome_extensions'):
            page.ele('text=Continue with a chrome_extensions').click()
            page.refresh()

        if page.ele('text=Continue with a chrome_extensions'):
            page.ele('text=Continue with a chrome_extensions', ).click()
            if page.ele('text=OKX Wallet'):
                if handle_okx_popup(page, seq) == False:
                    print(f"❌ 浏览器ID: {seq}, Continue with a chrome_extensions 出现错误")
        else:
            print(f"✅ 浏览器ID: {seq}, 已处于登录状态")

        if page.ele('x://input[@placeholder="Enter coin name"]', timeout=5):
            page.ele('x://input[@placeholder="Enter coin name"]').wait(1).input(generate_coin_name())
            if page.ele('text=Save'):
                page.ele('text=Save').click()
            page.wait(10)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
