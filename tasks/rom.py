from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from base.error import error_browser_seq
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup, handle_okx


def rom_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['google_username']
    password = metadata['google_password']

    extension_url = f"https://event.wemixplay.com/rom-wp?inviteCode=C0A0F376"
    url2 = f'https://romgoldenage.com/event02'
    url3 = f'https://romgoldenage.com/event03'
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        # 注册任务
        # page.get(extension_url)
        # if page.ele('x://input[@type="checkbox"]', timeout=60):
        #     page.ele('x://input[@type="checkbox"]').wait(1).click('js')
        #
        #     if page.ele('text=PRE-REGISTER NOW', timeout=60):
        #         page.ele('text=PRE-REGISTER NOW').wait(1).click('js')
        #
        #     if page.ele("text=Continue with Google"):
        #         page.ele("text=Continue with Google").wait(1).click('js')
        #         page.wait(5)
        #         auth_google_tab = chromium.get_tab(url='accounts.google.com')
        #         if auth_google_tab:
        #             auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
        #             auth_google_tab.wait(3)
        #             if auth_google_tab.ele('text=Continue',timeout=60):
        #                 auth_google_tab.ele('text=Continue').wait(1).click('js')
        #
        #         if page.ele('text=Sign Up',timeout=60):
        #             page.ele('text=Sign Up').wait(1).click('js')
        #
        #             checkboxs =  page.eles('x://input[@type="checkbox"]', timeout=60)
        #             for box in checkboxs:
        #                 box.wait(1).click('js')
        #
        #             if page.ele('text=Next', timeout=60):
        #                 page.ele('text=Next').wait(1).click('js')
        #
        #         if page.ele('x://input[@name="nickname"]', timeout=60):
        #             page.ele('x://input[@name="nickname"]').input(email.lower().split('@')[0][:12])

        # 预注册任务
        # page.get('https://romgoldenage.com/pre-registration')
        # if page.ele('x://input[@type="checkbox"]', timeout=60):
        #     page.ele('x://input[@type="checkbox"]').wait(1).click('js')
        #     if page.ele("text=Apply Pre-Registration"):
        #         page.ele("text=Apply Pre-Registration").wait(1).click('js')
        #         if page.ele("text=Sign in with Google"):
        #             page.ele("text=Sign in with Google").wait(1).click('js')
        #             page.wait(5)
        #             auth_google_tab = chromium.get_tab(url='accounts.google.com')
        #             if auth_google_tab:
        #                 auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
        #                 auth_google_tab.wait(3)
        #                 if auth_google_tab.ele('text=Continue', timeout=60):
        #                     auth_google_tab.ele('text=Continue').wait(1).click('js')

        # 签到任务
        page.get(url2)
        if page.ele("text=Check My Mission Progress"):
            page.ele("text=Check My Mission Progress").wait(1).click('js')
            if page.ele("text=Sign in with Google", timeout=30):
                page.ele("text=Sign in with Google").wait(1).click('js')
                page.wait(5)
                auth_google_tab = chromium.get_tab(url='accounts.google.com')
                if auth_google_tab:
                    auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
                    auth_google_tab.wait(10)
                page.get(url3)
                if page.ele("text=Check In Now"):
                    page.ele("text=Check In Now").wait(1).click('js')

            # if page.ele("text=使用 Google 账号登录", timeout=30):
            #     page.ele("text=使用 Google 账号登录").wait(1).click('js')
            #     page.wait(5)
            #     auth_google_tab = chromium.get_tab(url='accounts.google.com')
            #     if auth_google_tab:
            #         auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
            #         if auth_google_tab.ele('x://input[@aria-label="输入您的密码"]', timeout=30):
            #             auth_google_tab.ele('x://input[@aria-label="输入您的密码"]').wait(1).input(password)
            #             if auth_google_tab.ele('text=下一步', timeout=10):
            #                 auth_google_tab.ele('text=下一步').wait(1).click()

        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
