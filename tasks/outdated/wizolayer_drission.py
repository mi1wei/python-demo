from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq


def wizolayer_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://wizolayer.app?ref=9155701294"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 2)

    try:
        page.get(extension_url)
        page.wait(5)
        if page.ele('text=Sign Up', timeout=30):
            page.ele('text=Sign Up').wait(1).click('js')
            page.wait(5)
            auth_google_tab = chromium.get_tab(url='accounts.google.com')
            if auth_google_tab:
                auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
                if auth_google_tab.ele('text=Continue', timeout=30):
                    auth_google_tab.ele('text=Continue').wait(1).click('js')
                auth_google_tab.wait(10)

        if page.ele('text=Connect Wallet', timeout=10):
            page.ele('text=Connect Wallet').wait(1).click('js')
            if page.ele('text=OKX Wallet', timeout=10):
                if handle_okx_popup(page, seq) == False:
                    print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")

        if page.ele('text=Start Mining',timeout=10):
            page.ele('text=Start Mining').wait(1).click('js')

        tasks = page.eles('text=Complete Task',timeout=10)
        for task in tasks:
            task.wait(1).click('js')

        page.wait(10)

        verifys = page.eles('text=Verify',timeout=10)
        for verify in verifys:
            verify.wait(1).click('js')

        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
