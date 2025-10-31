from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq
import traceback

# https://x.com/xiaoayi1997/status/1980837000606597301
# 签署: app.sandchain.com/manifesto
# 社交任务平台: app.sandchain.com
# 领水: https://sandchain-hub.caldera.xyz
# omnihub 铸造nft: https://omnihub.xyz/collection/sandchain-testnet/sandchain-omnihub
# SANDchain Builder https://build.sandchain.com/landing

def register(chromium, page, seq, extension_url):
    page.get(extension_url)
    page.wait(2)

def example_drission(metadata: dict):
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

    try:
        register(chromium, page, seq, extension_url)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
