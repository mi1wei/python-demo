from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx
from base.error import error_browser_seq
import traceback

code = 'HKQLH0U6'


def register(chromium, page, seq, extension_url='https://waitlist.kindredlabs.ai?code=C6886CF'):
    page.get(extension_url)
    if page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        page.wait(10)
        js_code = """
                    const el1 = document.querySelector("w3m-modal")?.shadowRoot.querySelector('w3m-router')?.shadowRoot.querySelector('w3m-connect-view')?.shadowRoot.querySelector('w3m-wallet-login-list')?.shadowRoot.querySelector('w3m-connector-list')?.shadowRoot.querySelector('wui-flex')?.querySelector('w3m-list-wallet[name="OKX Wallet"]');
                    el1?.click();
                    """
        page.run_js(js_code)
        page.wait(3)
        okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
        if okx_tab:
            handle_okx(okx_tab, seq)
            page.wait(10)
    page.wait(2)


def kindred_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://waitlist.kindredlabs.ai?code=C6886CF"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        register(chromium, page, seq)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
