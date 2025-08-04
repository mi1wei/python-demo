from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from base.error import error_browser_seq
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


# 2,9,21,23,42,48,59,66,70,68,61,64,75,86,89
def rialo_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://www.rialo.io/"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('Join waitlist', timeout=10):
            page.ele('Join waitlist', timeout=10).wait(1).click('js')
            # if page.ele("text=Your spot on the waitlist is confirmed. We'll keep you posted with next steps and early access updates soon.",timeout=10):
            #     print(f"✅ 浏览器ID: {seq}, Join waitlist success")
            #     return

            if page.ele('x://input[@placeholder="Enter your full name"]', timeout=10):
                page.ele('x://input[@placeholder="Enter your full name"]').input(email.split('@')[0])
            if page.ele('x://input[@placeholder="Enter your email"]', timeout=10):
                page.ele('x://input[@placeholder="Enter your email"]').input(email)
            if page.ele('x://input[@value=" join waitlist"]', timeout=10):
                page.ele('x://input[@value=" join waitlist"]', timeout=10).wait(1).click('js')
            if page.ele("text=Your spot on the waitlist is confirmed. We'll keep you posted with next steps and early access updates soon.",timeout=10):
                print(f"✅ 浏览器ID: {seq}, Join waitlist success")
            else:
                print(f"❌ 浏览器ID: {seq}, Join waitlist failed")
                error_browser_seq.append(seq)
        page.wait(5)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
