
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

def choice_eth_wallet(page, metadata: dict, index):
    seq = metadata['seq']
    extension_url = "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html"
    page.get(extension_url)
    try:

        if page.ele('x://input[@placeholder="密码"]', timeout=5):
            page.ele('x://input[@placeholder="密码"]').wait(1).input('12345678')
            if page.ele('text=解锁'):
                page.ele('text=解锁').click()
                print(f"✅ 浏览器ID: {seq}, 导入solana钱包成功")


    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        error_browser_seq.append(seq)
    finally:
        try:
            page.close()
        except Exception as e:
            print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")

def safe_click_for_new_tab(ele, timeout=3):
    try:
        return ele.wait(1).click.for_new_tab(timeout=timeout)
    except Exception as e:
        return None

def handle_okx(okx_tab, seq, selector='text=Phantom Wallet'):
    try:
        # if okx_tab.ele('x://input[@placeholder="请输入密码"]', timeout=5):
        #     okx_tab.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
        # if okx_tab.ele('text=解锁', timeout=1):
        #     okx_tab.ele('text=解锁').wait(1).click()
        # if okx_tab.ele('text=切换钱包', timeout=1):
        #     okx_tab.ele('text=切换钱包').wait(1).click()
        #     checkbox = okx_tab.ele('.okui-checkbox-circle')
        #     checkbox.click()
        #     if okx_tab.ele('text=确认', timeout=1):
        #         okx_tab.ele('text=确认').wait(1).click()
        #     if okx_tab.ele('text=连接', timeout=1):
        #         okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()

        if okx_tab.ele('text=连接', timeout=3):
            okx_tab =  okx_tab.ele('x://button[@type="submit"]').wait(1).click.for_new_tab(3)
            # okx_tab = safe_click_for_new_tab(okx_tab.ele('text=连接'), timeout=3)
        max_tries = 20
        count = 0
        while okx_tab is not None and count < max_tries:
            try:
                if okx_tab.ele('text=确认', timeout=1):
                    confirm_btn = okx_tab.ele('text=确认', timeout=10)
                    if not confirm_btn:
                        break
                    confirm_btn.wait(1).click('js')
                    count += 1
                else:
                    break
            except Exception as e:
                error_msg = str(e)
                if '与页面的连接已断开' in error_msg:
                    print(f"⚠️ 浏览器ID: {seq}, 页面已关闭或连接断开，退出循环")
                    break
                else:
                    print(f"❌ 浏览器ID: {seq}, 异常: {error_msg}")
                    return False  # 或者继续处理其他逻辑
        return True
    except Exception as e:
        print(f'浏览器ID: {seq}, handle_okx_popup error {e}')
        return False