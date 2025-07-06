from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def onefootball_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://ofc.onefootball.com/s2/mission/f34d3b68-fe15-4cd5-8be8-df93e78c8fe7/"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele("text=View details", timeout=5):
            page.ele("text=View details").click()
            if page.ele("text=Let's go", timeout=5):
                allowlist_tab = page.ele("text=Let's go").click.for_new_tab()
                allowlist_tab.ele('x://input[@type="checkbox"]').wait(1).click()
                allowlist_tab.ele('text=Continue').click()
                if allowlist_tab.ele('text=Connect Wallet'):
                    allowlist_tab.ele('text=Connect Wallet').click()
                    if handle_okx_popup(allowlist_tab, seq) == False:
                        print(f"❌ 浏览器ID: {seq}, handle_okx_popup1 出现错误")
                    if allowlist_tab.ele('text=Sign to verify'):
                        if handle_okx_popup(allowlist_tab, seq,'text=Sign to verify') == False:
                            print(f"❌ 浏览器ID: {seq}, handle_okx_popup2 出现错误")
                    if allowlist_tab.ele('text= Connect X'):
                        allowlist_tab.ele('text= Connect X').click()
                        if allowlist_tab.ele('text=授权应用'):
                            allowlist_tab.ele('text=授权应用').click()

                    if allowlist_tab.ele('text=Must follow @ofc_the_club'):
                        allowlist_tab.ele('text=Must follow @ofc_the_club').wait(1).click()

                    if allowlist_tab.ele('x://input[@placeholder="yourname@example.com"]', timeout=5):
                        allowlist_tab.ele('x://input[@placeholder="yourname@example.com"]').wait(1).input(email)

                    if allowlist_tab.ele('x://input[@data-testid="multipleChoice-question-6-radio-2-input"]', timeout=5):
                        allowlist_tab.ele('x://input[@data-testid="multipleChoice-question-6-radio-2-input"]').click()

                    # allowlist_tab.ele('x://span[@role="checkbox"]').wait(1).click()

        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
