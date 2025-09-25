from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions


def discord_detect(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']

    extension_url = f"https://discord.com/channels/@me"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.eles('text=在线', timeout=60) or page.eles('text=Online', timeout=60):
            ele = page.ele('x://div[contains(@class, "hovered__")]')
            if ele:
                print(f"✅ 浏览器ID: {seq} , Discord {ele.text} 登陆状态正常")
            else:
                print(f"✅ 浏览器ID: {seq}, Discord 登陆状态正常")
        else:
            print(f"❌ 浏览器ID: {seq}, Discord 登陆状态异常")
            error_browser_seq.append(seq)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
