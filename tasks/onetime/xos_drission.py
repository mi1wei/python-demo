from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from base.error import error_browser_seq
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def xos_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://x.ink/airdrop"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('text=Apply Now', timeout=60):
            page.ele('text=Apply Now', timeout=10).wait(1).click('js')
            if page.ele('text=OKX Wallet', timeout=10):
                page.ele('text=OKX Wallet', timeout=10).wait(1).click('js')
                page.wait(5)
                okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
                if okx_tab:
                    handle_okx(okx_tab, seq)

            if page.ele('text=Accept', timeout=30):
                page.ele('text=Accept', timeout=10).wait(1).click('js')

            if page.ele('text=Next', timeout=30):
                page.ele('text=Next', timeout=10).wait(1).click('js')

        buttons = page.eles('text=Let\'s go', timeout=30)
        for button in buttons:
            button.wait(2).click('js')

        verifys = page.eles('text=Verify', timeout=30)
        for button in verifys:
            button.wait(2).click('js')
            # count = len(buttons)
            # if page.ele("text=Let's go", timeout=30):
            #     page.ele("text=Let's go").wait(1).click('js')
        page.wait(5)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
