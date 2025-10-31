from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, okx_reauthorize, okx_reauthorize_2
from base.error import error_browser_seq
import traceback

code = 'HKQLH0U6'


def register(chromium, page, metadata, extension_url='https://community.nitrograph.com/app/missions'):
    page.get(extension_url)
    seq = metadata['seq']
    if page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        page.wait(10)
        js_code = """
                    const el1 = document.querySelector("w3m-modal")?.shadowRoot.querySelector('w3m-router')?.shadowRoot.querySelector('w3m-connect-view')?.shadowRoot.querySelector('w3m-wallet-login-list')?.shadowRoot.querySelector('w3m-connector-list')?.shadowRoot.querySelector('wui-flex')?.querySelector('w3m-list-wallet[name="OKX Wallet"]');
                    el1?.click();
                    """
        page.run_js(js_code)
        page.wait(3)
        okx_reauthorize_2(chromium, page, metadata)

    if page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        page.wait(10)
        js_code = """
                    const el1 = document.querySelector("w3m-modal")?.shadowRoot.querySelector('w3m-router')?.shadowRoot.querySelector('w3m-connect-view')?.shadowRoot.querySelector('w3m-wallet-login-list')?.shadowRoot.querySelector('w3m-connector-list')?.shadowRoot.querySelector('wui-flex')?.querySelector('w3m-list-wallet[name="OKX Wallet"]');
                    el1?.click();
                    """
        page.run_js(js_code)
        page.wait(3)
        okx_reauthorize(chromium, page, metadata)
        page.wait(10)
        page.refresh()
        page.wait(10)

    page.get(extension_url)
    # View Your Agent
    if page.ele('text=Mint Your Agent ', timeout=5):
        page.ele('text=Mint Your Agent ').click('js')
        print(f"✅ 浏览器ID: {seq}, Mint Your Agent")

    page.wait(2)


def daily(chromium, page, metadata, extension_url='https://community.nitrograph.com/app/missions'):
    # page.get(extension_url)
    seq = metadata['seq']
    if page.ele('text=CLAIM', timeout=5):
        page.ele('text=CLAIM').click('js')
        print(f"✅ 浏览器ID: {seq}, Claim your daily $NITRO")
    if page.ele('text=Claim', timeout=5):
        page.ele('text=Claim').click('js')
        print(f"✅ 浏览器ID: {seq}, Daily claim")
    page.wait(10)


def nitrograph_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://community.nitrograph.com/app/missions"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        register(chromium, page, metadata)
        daily(chromium, page, metadata)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
