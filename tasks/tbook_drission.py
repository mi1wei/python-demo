from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup,okx_reauthorize
from base.error import error_browser_seq
import traceback


# https://x.com/ulaganathanj6/status/1983084204322893845
# https://t.me/weimi07201

def register(chromium, page, metadata, extension_url):
    page.get(extension_url)
    if page.ele('text=Log In'):
        page.ele('text=Log In').click('js')
        if page.ele('text=Sui Wallet'):
            page.ele('text=Sui Wallet').click('js')
            if page.ele('text=OKX'):
                page.ele('text=OKX').click('js')
                page.wait(3)
                okx_reauthorize(chromium, page, metadata)
    page.wait(2)


def tbook_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://engage.tbook.com/wise?referCode=VORLJE"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        register(chromium, page, metadata, extension_url)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
