from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup,handle_okx


def find_okx_tab(chromium: Chromium, retry: int = 5, interval: float = 1.0):
    """最多重试 retry 次查找 OKX 插件页"""
    for attempt in range(retry):
        for tab in chromium.tabs:
            print(tab.title)
            if 'okx' in tab.title.lower() or 'okx' in tab.url.lower():
                return tab
        print(f"🔍 第 {attempt + 1}/{retry} 次未找到 OKX 插件页，等待 {interval}s 重试...")
        time.sleep(interval)
    return None


def pharosnetwork_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']



    extension_url = f"https://testnet.pharosnetwork.xyz/experience?inviteCode=pvNxkApfCe8avXao"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 2)

    try:
        page.get(extension_url)

        if page.ele('text=Connect Wallet',timeout=10):
            page.ele('text=Connect Wallet').wait(2).click()
            page.wait(5)

            js_code = """
            const el1 = document.querySelector("w3m-modal")?.shadowRoot.querySelector('w3m-router')?.shadowRoot.querySelector('w3m-connect-view')?.shadowRoot.querySelector('w3m-chrome_extensions-login-list')?.shadowRoot.querySelector('w3m-connector-list')?.shadowRoot.querySelector('w3m-connect-announced-widget')?.shadowRoot.querySelector('wui-list-chrome_extensions');
            el1.click();
            """
            page.run_js(js_code)
            page.wait(5)
            if page.ele('text=Continue', timeout=5):
                page.ele('text=Continue').click()
                page.wait(5)
                okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
                if okx_tab:
                    handle_okx(okx_tab, seq)
            okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
            if okx_tab:
                handle_okx(okx_tab,seq)

        if page.ele('text=Switch >',timeout=10):
            page.ele('text=Switch >').click()

        if page.ele('text=Continue', timeout=5):
            page.ele('text=Continue').click()
            page.wait(2)
            okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
            if okx_tab:
                handle_okx(okx_tab, seq)

        page.wait(2)
        while page.ele('text=Check in',timeout=5):
            page.ele('text=Check in').wait(2).click()
            print(f"✅ 浏览器ID: {seq}, Check in")

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
