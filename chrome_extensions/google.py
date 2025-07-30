from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions


def google_email_login(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    username = metadata['google_username']
    password = metadata['google_password']

    res = openBrowser(browser_id)
    http_addr = res['data']['http']

    # 初始化 DrissionPage 浏览器连接
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    extension_url = "https://workspace.google.com/intl/zh-CN/gmail/"
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
