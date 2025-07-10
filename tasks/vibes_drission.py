from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def vibes_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']
    x_username = metadata['x_username']
    x_password = metadata['x_password']
    x_token = metadata['x_2fa']

    extension_url = f"https://www.vibes.fun/?ref=mi_wei74404"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    # choice_eth_wallet(chromium.new_tab(), metadata, 1)

    try:
        page.get(extension_url)

        while page.ele('text=connect x', timeout=10):
            page.ele('text=connect x').wait(1).click()
            page.wait(5)
            if 'oauth2' in page.url:
                if page.ele('text=授权应用', timeout=5):
                    page.ele('text=授权应用').click()
                    page.wait(10)
            page.get(extension_url)
            page.wait(5)


        if page.ele('x://button[text()="claim now"]',timeout=10):
            buttons = page.eles('x://button[text()="claim now"]')
            buttons[0].click()
            page.wait(2)
            buttons = page.eles('x://button[text()="claim now"]')
            buttons[2].click()
            page.wait(2)
            page.get(extension_url)

        page.wait(10)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
