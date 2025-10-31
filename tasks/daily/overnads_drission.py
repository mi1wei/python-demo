from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from base.error import error_browser_seq
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def overnads_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    # extension_url = f"https://app.overnads.xyz/?refCode=FD5C3A3B"
    extension_url ="https://app.overnads.xyz/home"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    # choice_eth_wallet(chromium.new_tab(), metadata, 2)

    try:
        page.get(extension_url)
        if page.ele('text=Twitter ', timeout=10):
            page.ele('text=Twitter ', timeout=10).wait(1).click('js')
            if page.ele('text=授权应用', timeout=20):
                page.ele('text=授权应用').click()
                page.wait(10)
            if page.ele('text= CLAIM ', timeout=5):
                page.ele('text= CLAIM ').click()
            print(f"✅ 浏览器ID: {seq}, 登陆成功")

        page.get('https://app.overnads.xyz/home')
        if page.ele('text=CLAIM', timeout=10):
            page.ele('text=CLAIM').click()
            print(f"✅ 浏览器ID: {seq}, 签到成功")
        else:
            print(f"✅ 浏览器ID: {seq}, 签到过了")

        if page.ele('text= CLAIM ', timeout=5):
            page.ele('text= CLAIM ').click()

        page.wait(5)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
