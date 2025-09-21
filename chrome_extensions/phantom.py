
from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions

def add_solana_wallet(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    private_key = metadata['okx_solana_private_key']

    res = openBrowser(browser_id)
    http_addr = res['data']['http']
    # 初始化 DrissionPage 浏览器连接
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    extension_url = "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html"
    page.get(extension_url)
    try:

        if page.ele('text=解锁'):
            print(f"✅ 浏览器ID: {seq}, solana钱包已导入")
            return

        page.ele('text=我已经有一个钱包', timeout=5).click()
        print(f"✅ 浏览器ID: {seq}, 已点击『导入已有钱包』按钮")

        page.ele('text=导入私钥', timeout=5).click()

        page.ele('x://input[@name="name"]').input('solana')
        page.ele('x://textarea[@placeholder="私钥"]').input(private_key)

        page.ele('text=导入').click()

        page.ele('x://input[@placeholder="密码"]').input('12345678')
        page.ele('x://input[@placeholder="确认密码"]').input('12345678')

        if page.ele('x://input[@aria-checked="false"]',timeout=3):
            page.ele('x://input[@type="checkbox"]').click()
        page.ele('text=继续', timeout=5).click()
        page.wait(10)

        while page.ele('text=继续', timeout=5):
            page.ele('text=继续', timeout=5).click()
            page.wait(2)

        page.wait(5)
        print(f"✅ 浏览器ID: {seq}, 导入solana钱包成功")

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