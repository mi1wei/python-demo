from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def dream_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://dreamerquests.partofdream.io/login?referralCodeForPOD=a3f6dfda"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('x://div[contains(@class, "border-[#5700FF]")]', timeout=10):
            points = page.ele('x://div[contains(@class, "border-[#5700FF]")]').text.replace('\n', ': ')
            print(f"✅ 浏览器ID: {seq}, {points}")
            return
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
