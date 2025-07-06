from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def sosovalue_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://sosovalue.com/zh/exp"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        # 检查语言是否是中文
        if page.ele('x://div[contains(text(), "EN")]',timeout=10):
            print(page.ele('x://div[contains(text(), "EN")]').html)
            print(f"❌ 浏览器ID: {seq}, 切换语言到中文")
            return

        # 加入SoDEX测试网白名单
        join_btn = page.ele('x://div[@id="JOIN_SODEX_TESTNET_WHITELIST"]')
        if join_btn:
            if join_btn.html.__contains__('完成'):
                print(f'✅ 浏览器ID: {seq}, 成功 -> 加入SoDEX测试网白名单')
            else:
                if join_btn.ele('text=加入', timeout=5):
                    join_btn.ele('text=加入').click()
                    print(f'✅ 浏览器ID: {seq}, 加入 -> 加入SoDEX测试网白名单')

        page.refresh()
        join_btn = page.ele('x://div[@id="JOIN_SODEX_TESTNET_WHITELIST"]')
        if join_btn:
            if join_btn.ele('text=验证', timeout=60):
                join_btn.ele('text=验证').click()
                print(f'✅ 浏览器ID: {seq}, 验证 -> 加入SoDEX测试网白名单')
        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
