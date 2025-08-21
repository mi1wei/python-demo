from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx
from base.error import error_browser_seq

# BILLIONS500K
# SENTIENTXBILLIONS
# BILLIONS400POINTS
def unich_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://unich.com/en/airdrop/sign-up?ref=GeWM8Ozf3G"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('text=Continue with Google', timeout=10):
            page.ele('text=Continue with Google').wait(1).click('js')
            page.wait(5)
            auth_google_tab = chromium.get_tab(url='accounts.google.com')
            if auth_google_tab:
                auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
                auth_google_tab.wait(3)
                if auth_google_tab.ele('text=Continue', timeout=60):
                    auth_google_tab.ele('text=Continue').wait(1).click('js')
                checkboxs = page.eles('x://input[@type="checkbox"]', timeout=60)
                for box in checkboxs:
                    box.wait(1).click('js')
                if page.ele('text=I agree', timeout=10):
                    page.ele('text=I agree').wait(1).click('js')
        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
