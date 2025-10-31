from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq
import traceback

# [1-27]

def register(chromium, page, metadata, extension_url):
    page.get(extension_url)
    chromium.new_tab().get('https://outlook.live.com/mail/0/junkemail')
    chromium.activate_tab(page)
    print(metadata['outlook_username'])
    js_code = f"""
                      const el1 = document.querySelector('[placeholder="Your Email"]');
                      el1.value = "{metadata['outlook_username']}"
                  """
    page.run_js(js_code)
    page.ele('x://button[@type="submit"]').wait(1).click('js')
    page.wait(2)


def stable_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://app.stable.xyz/"

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
