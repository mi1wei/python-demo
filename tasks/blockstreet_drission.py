from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq
import traceback


def register(chromium, page, seq, extension_url='https://blockstreet.money/dashboard?invite_code=brzEJR'):
    page.get(extension_url)
    if page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        if handle_okx_popup(page, seq) == False:
            print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")
    page.wait(2)

def blockstreet_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://blockstreet.money/dashboard?invite_code=brzEJR"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        register(chromium, page, seq, extension_url)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
