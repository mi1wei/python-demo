from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions


def outlook_email_login(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    username = metadata['outlook_username']
    password = metadata['outlook_password']

    res = openBrowser(browser_id)
    http_addr = res['data']['http']

    # 初始化 DrissionPage 浏览器连接
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    extension_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=9199bf20-a13f-4107-85dc-02114787ef48&scope=https%3A%2F%2Foutlook.office.com%2F.default%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Foutlook.live.com%2Fmail%2F&client-request-id=bc2634cf-790e-19ca-e466-aa43bdfbf92f&response_mode=fragment&client_info=1&prompt=select_account&nonce=019a2f70-dff0-7833-bec3-dcbfa036e208&state=eyJpZCI6IjAxOWEyZjcwLWRmZjAtNzcwNS04YmJiLTlmMTY2ZWFiZWRjNSIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D%7CaHR0cHM6Ly9vdXRsb29rLmxpdmUuY29tL21haWwvMC8_ZGVlcGxpbms9bWFpbCUyRjAlMkYlM0ZubHAlM0Qw&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22CP1%22%5D%7D%7D%7D&x-client-SKU=msal.js.browser&x-client-VER=4.14.0&response_type=code&code_challenge=wT8XkaZaYPHmdzz3S7CDrJ_vTEAMMtpTf75McXyzv4M&code_challenge_method=S256&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&fl=dob,flname,wld&sso_reload=true"
    page.get(extension_url)
    try:
        if page.ele('text=登录', timeout=30):
            page.ele('text=登录').wait(1).click('js')

            if page.ele('x://input[@aria-label="邮箱或电话号码"]', timeout=30):
                page.ele('x://input[@aria-label="邮箱或电话号码"]').wait(1).input(username)

            if page.ele('text=下一步', timeout=30):
                page.ele('text=下一步').wait(1).click()

            if page.ele('x://input[@aria-label="输入您的密码"]', timeout=30):
                page.ele('x://input[@aria-label="输入您的密码"]').wait(1).input(password)

            if page.ele('text=下一步', timeout=10):
                page.ele('text=下一步').wait(1).click()

            if page.ele('x://input[@name="confirm"]', timeout=30):
                page.ele('x://input[@name="confirm"]').wait(1).click('js')

            page.wait(10)

            if 'mail.google.com/mail/' in page.url:
                print(f"✅ 浏览器ID: {seq}, {username} goolge 邮箱登陆成功")

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        error_browser_seq.append(seq)
    finally:
        try:
            page.close()
        except Exception as e:
            print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")
        try:
            closeBrowser(browser_id)
        except Exception as e:
            print(f"⚠️ 执行 closeBrowser({browser_id}) 失败: {e}")


def google_reauthorize(chromium, metadata):
    password = metadata['google_password']
    auth_google_tab = chromium.get_tab(url='accounts.google.com')
    if auth_google_tab:
        auth_google_tab.ele('x://div[@class="r4WGQb"]//ul/li[1]').click()
        auth_google_tab.wait(3)
        if auth_google_tab.ele('x://input[@aria-label="输入您的密码"]', timeout=30):
            auth_google_tab.ele('x://input[@aria-label="输入您的密码"]').wait(1).input(password)
            if auth_google_tab.ele('text=下一步', timeout=10):
                auth_google_tab.ele('text=下一步').wait(1).click()
        if auth_google_tab.ele('text=Continue', timeout=60):
            auth_google_tab.ele('text=Continue').wait(1).click('js')
        # checkboxs = page.eles('x://input[@type="checkbox"]', timeout=60)
        # for box in checkboxs:
        #     box.wait(1).click('js')
        # if page.ele('text=I agree', timeout=10):
        #     page.ele('text=I agree').wait(1).click('js')
