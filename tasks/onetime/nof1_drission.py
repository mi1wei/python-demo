from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq
import traceback
from chrome_extensions.email_outlook import outlook_get_name_email_password, generate_us_phone_number

# 28, 55...
def waitlist(chromium, page, metadata, extension_url):
    name, email, _ = outlook_get_name_email_password(metadata)
    page.get(extension_url)
    if page.ele('x://input[@placeholder="NAME"]', timeout=5):
        page.ele('x://input[@placeholder="NAME"]').wait(1).input(name)
    if page.ele('x://input[@placeholder="EMAIL"]', timeout=5):
        page.ele('x://input[@placeholder="EMAIL"]').wait(1).input(email)
    if page.ele('x://input[@placeholder="PHONE"]', timeout=5):
        page.ele('x://input[@placeholder="PHONE"]').wait(1).input(generate_us_phone_number())
    if page.ele('x://button[@type="submit"]', timeout=5):
        page.ele('x://button[@type="submit"]').wait(1).click('js')
    page.wait(15)


def nof1_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://nof1.ai/waitlist"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        waitlist(chromium, page, metadata, extension_url)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
