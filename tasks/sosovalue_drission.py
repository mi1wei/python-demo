from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
import traceback


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
        max_attempts = 3
        for attempt in range(max_attempts):
            page.wait(10)
            if not page.ele('text=注册', timeout=5):
                break
            if page.ele('text=注册', timeout=30):
                page.ele('text=注册').wait(1).click('js')
                page.ele('text=成功！', timeout=60)
                if page.ele('text=Twitter'):
                    page.ele('text=Twitter').wait(1).click()
                    page.wait(30)
                page.get(extension_url)
                page.wait(30)

        # if page.ele('x://div[@id="go_exp"]', timeout=60) == None:
        #     print(f"❌ 浏览器ID: {seq}, 未登陆")
        #     return

        # 检查语言是否是中文
        # if page.ele('x://div[contains(text(), "EN")]',timeout=10):
        #     print(page.ele('x://div[contains(text(), "EN")]').html)
        #     print(f"❌ 浏览器ID: {seq}, 切换语言到中文")
        #     return

        if page.ele('x://span[contains(text(), "Exp")]', timeout=5):
            exp = page.ele('x://span[contains(text(), "Exp")]').text

        listen = page.ele('x://button[.//span[text()="立即收听"]]', timeout=5)
        # if page.ele('text=点赞',timeout=5):
        if listen:
            listen.wait(1).click('js')
            page.get(extension_url)
            page.wait(10)

        like = page.ele('x://button[.//span[text()="点赞"]]', timeout=5)
        # if page.ele('text=点赞',timeout=5):
        if like:
            like.wait(1).click('js')

        share = page.ele('x://button[.//span[text()="分享"]]', timeout=5)
        if share:
            share.wait(1).click('js')

        # yinyong = page.ele('x://button[.//span[text()="引用"]]', timeout=5)
        # if yinyong:
        #     yinyong.wait(1).click('js')
        #
        # huifu = page.ele('x://button[.//span[text()="回复"]]', timeout=5)
        # if huifu:
        #     huifu.wait(1).click('js')

        if like or listen or share:
            pass
        else:
            print(f'✅ 浏览器ID: {seq}, 今日任务已经做完, {exp}')
            return

        if page.ele('text=关注'):
            page.ele('text=关注').click()
            print(f'✅ 浏览器ID: {seq}, 关注博客成功, {exp}')


        for i in range(10):
            page.refresh()
            page.wait(10)
            validations = page.eles('x://button[.//span[text()="验证"]]', timeout=5)
            if validations:
                print(f'✅ 浏览器ID: {seq}, {len(validations)}个验证错误')
                for validation in validations:
                    validation.click('js')
            else:
                print(f'✅ 浏览器ID: {seq}, 今日任务已经做完, 无需要验证的任务 3, {exp}')
                return
        page.wait(10)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
    finally:
        page.close()
        closeBrowser(browser_id)
