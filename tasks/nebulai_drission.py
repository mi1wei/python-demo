from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def nebulai_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://nebulai.network/opencompute?invite_by=Xpgd9P"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        page.get(extension_url)

        if page.ele('text=Connect Wallet',timeout=5):
            page.ele('text=Connect Wallet').click('js')

            js_code = """
            const el1 = document.querySelector("w3m-modal")?.shadowRoot.querySelector('w3m-router')?.shadowRoot.querySelector('w3m-connect-view')?.shadowRoot.querySelector('w3m-wallet-login-list')?.shadowRoot.querySelector('w3m-connector-list')?.shadowRoot.querySelector('w3m-connect-announced-widget')?.shadowRoot.querySelector('wui-list-wallet');            
            el1?.click();
            """
            page.run_js(js_code)
            page.wait(5)
            okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
            if okx_tab:
                handle_okx(okx_tab, seq)


            page.ele('x://input[@type="checkbox"]').wait(1).click()
            page.ele('text=Log In / Sign Up').click()
        else:
            print(f"✅ 浏览器ID: {seq}, 已处于登录状态")

        icon_ele = page.ele('x://img[contains(@src, "mining_off.svg")]/..', timeout=10)
        if icon_ele:
            icon_ele.click()
            print(f"浏览器ID: {seq}, Already ON, click one times")
        else:
            icon_ele = page.ele('x://img[contains(@src, "mining-on.svg")]/..', timeout=10)
            icon_ele.click()
            icon_ele.click()
            print(f"浏览器ID: {seq}, Already ON, click two times")

        claims = page.eles('x://div[text()="Go"]')
        print(f"浏览器ID: {seq}, 当前有{len(claims)} 社交任务")

        if len(claims) == 0:
            return
        x_oauth = claims[0]
        x_oauth.wait(1).click()
        if page.ele('text=Link', timeout=5):
            page.ele('text=Link').click()
            page.wait(5)
            if 'oauth2' in page.url:
                if page.ele('text=授权应用', timeout=5):
                    page.ele('text=授权应用').click()
                    page.wait(5)

        claims = page.eles('x://div[text()="Go"]')
        for claim in claims:
            claim.wait(2).click()

        page.wait(10)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
