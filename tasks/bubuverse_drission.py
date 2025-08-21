from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx
from base.error import error_browser_seq

def bubuverse_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://bubuverse.fun?ref=GQtGNoGVKxaoBWwqtyDwPKywETFhkGSkehkG4EF7oFZ4"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 1)

    try:
        page.get(extension_url)
        if page.ele('text=Connect Wallet', timeout=10):
            page.ele('text=Connect Wallet').wait(1).click('js')
            if page.ele('text=OKX Wallet', timeout=10):
                if handle_okx_popup(page, seq) == False:
                    print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")

        page.get('https://bubuverse.fun/tasks')
        if page.ele('text=Check in Now',timeout=30):
            page.ele('text=Check in Now').wait(1).click('js')

        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
