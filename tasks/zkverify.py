from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def zkverify_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://points.zkverify.io/loyalty?referral_code=MMPQ8G66"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 2)

    try:
        page.get(extension_url)
        if page.ele('text=Connect Wallet', timeout=5):
            button = page.ele('x://button[@data-testid="ConnectButton"]//a[contains(text(), "Connect Wallet")]')
            if button:
                button.click('js')
                page.wait(3)
                js_code = """
                    const el1 = document.querySelector('[data-testid="dynamic-modal-shadow"]').shadowRoot.querySelector('[data-testid="chrome_extensions-list-scroll-container"]').querySelectorAll('button[data-testid="ListTile"]')[1];
                    el1.click();
                """
                page.run_js(js_code)
                page.wait(3)
                okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
                if okx_tab:
                    handle_okx(okx_tab, seq)
        okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
        if okx_tab:
            handle_okx(okx_tab, seq)

        i = 0
        while page.ele('text=Check in',timeout=3):
            page.ele('text=Check in').wait(5).click()
            i = i+1
            if i>5:
                break
            print(f"✅ 浏览器ID: {seq}, Check in")
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
