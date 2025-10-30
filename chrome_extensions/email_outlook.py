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

    extension_url = "https://outlook.live.com/mail/0/junkemail"
    page.get(extension_url)
    try:
        if page.ele('text=登录', timeout=30):
            page.ele('text=登录').wait(1).click('js')

            if page.ele('x://input[@aria-describedby="loginHeader usernameError"]', timeout=30):
                page.ele('x://input[@aria-describedby="loginHeader usernameError"]').wait(1).input(username)

            if page.ele('x://input[@value="下一步"]', timeout=30):
                page.ele('x://input[@value="下一步"]').wait(1).click('js')

            if page.ele('text=使用密码', timeout=30):
                page.ele('text=使用密码').wait(1).click()

            if page.ele('x://input[@name="passwd"]', timeout=30):
                page.ele('x://input[@name="passwd"]').wait(1).input(password)

            if page.ele('text=下一步', timeout=30):
                page.ele('text=下一步').wait(1).click()

            if page.ele('text=下一步', timeout=30):
                page.ele('text=下一步').wait(1).click()

            if page.ele('text=暂时跳过', timeout=30):
                page.ele('text=暂时跳过').wait(1).click()

            if page.ele('text=是', timeout=30):
                page.ele('text=是').wait(1).click()

            page.wait(10)
            if 'mail/0' in page.url:
                print(f"✅ 浏览器ID: {seq}, {username} outlook 邮箱登陆成功")
            else:
                error_browser_seq.append(seq)

        elif 'mail/0' in page.url:
            print(f"✅ 浏览器ID: {seq}, {username} outlook 邮箱处于登录态")
        page.wait(5)

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
