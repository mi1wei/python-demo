from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def assisterr_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']
    x_username = metadata['x_username']
    x_password = metadata['x_password']
    x_token = metadata['x_2fa']

    extension_url = f"https://build.assisterr.ai/dashboard"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 1)

    try:
        page.get(extension_url)
        page.refresh()
        page.wait(10)

        come_back = page.ele('text=Come back in ', timeout=10)
        if come_back:
            print(f'签到任务今天已经做过了 浏览器ID: {seq}')
        else:
            page.ele('text=Grab Daily Tokens', timeout=10).click('js')
            print(f"浏览器ID: {seq}, 点击了 Grab Daily Tokens")
            page.wait(10)

        page.wait(1)



        # buttons = page.eles('x://button[.//p[text()="$ASRR"]]')
        # count = len(buttons)
        #
        # for button in buttons:
        #     button.click()

        # if count == 2:
        #     for i in range(count - 1):
        #         buttons[i].click()
        #         page.ele('text=授权应用', timeout=60000).click()
        #         page.ele('text=Discord Auth', timeout=60000).click()
        #         page.ele('text=Assister Incentive', timeout=60000).click()
        #
        #         # 等待滚动并执行自定义脚本
        #         page.run_js('''() => {
        #                            const div = document.querySelector('.content__49fc1');
        #                            if (div) {
        #                                div.scrollTop = div.scrollHeight;
        #                                console.log('已滚动到底部');
        #                            }
        #                        }''')
        #
        #         page.ele('text=授权', timeout=30000).click()
        #         page.ele('text=Start building', timeout=30000).click()
        #
        # else:
        #     pass
        #     # for i in range(count):
        #     #     if i == 0:
        #     #         try:
        #     #             buttons[i].click()
        #     #             page.ele('text=授权应用', timeout=60000).click()
        #     #             page.get("https://build.assisterr.ai/dashboard")  # Reload
        #     #         except Exception as e:
        #     #            pass
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
