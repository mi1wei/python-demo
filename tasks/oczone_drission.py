from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx


def oczone_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']
    x_username = metadata['x_username']
    x_password = metadata['x_password']
    x_token = metadata['x_2fa']

    extension_url = f"https://testnet.gokite.ai?referralCode=YNYDJQI8"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 2)

    try:
        page.get(extension_url)

        if page.ele('text=LOG IN', timeout=60):
            page.ele('text=LOG IN').wait(1).click('js')
        if page.ele('text=OKX Wallet', timeout=30):
            page.ele('text=OKX Wallet').click()
            page.wait(5)
            okx_tab = chromium.get_tab(url='mcohilncbfahbmgdjkbpemcciiolgcge')
            if okx_tab:
                handle_okx(okx_tab, seq)
        if True:
            print(f'签到任务今天已经做过了 浏览器ID: {seq}')
        else:
            page.ele('text=Grab Daily Tokens', timeout=10).click('js')
            print(f"浏览器ID: {seq}, 点击了 Grab Daily Tokens")
            page.wait(10)

        page.wait(1)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
