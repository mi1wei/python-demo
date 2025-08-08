from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


# BILLIONS500K
# SENTIENTXBILLIONS
# BILLIONS400POINTS
def billions_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://signup.billions.network?rc=EUKZZZF4"

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
        if page.ele("text=Login with Twitter", timeout=30):
            page.ele("text=Login with Twitter").wait(1).click('js')
            if page.ele('x://input[@value="授权应用程序"]', timeout=60):
                page.ele('x://input[@value="授权应用程序"]').wait(1).click('js')
            if page.ele('text=GO TO DASHBOARD', timeout=60):
                page.ele('text=GO TO DASHBOARD').wait(1).click('js')
                print(f"✅ 浏览器ID: {seq}, GO TO DASHBOARD")
        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
