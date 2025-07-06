from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions


def add_eth_wallet(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    private_key = metadata['my_okx_eth_wallet_private_key']

    res = openBrowser(browser_id)
    http_addr = res['data']['http']

    # 初始化 DrissionPage 浏览器连接
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    extension_url = "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
    page.get(extension_url)
    try:
        login = False

        if page.ele('text=发送', timeout=3):
            print(f"🔑 浏览器ID: {seq}, 钱包处于登录态")
            login = True

        if not login:
            if page.ele('x://input[@placeholder="请输入密码"]', timeout=5):
                page.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
                if page.ele('text=解锁', timeout=1):
                    page.ele('text=解锁').wait(1).click()
                    print(f"✅ 浏览器ID: {seq}, 已点击『解锁』按钮")
            else:
                print(f"❌ 浏览器ID: {seq}, 导入solana钱包失败, 先导入OKX钱包")
                error_browser_seq.append(seq)
                return

        # 查看是否已经导入
        page.ele('text=私钥').click()
        page.wait(1)

        keys = page.eles('css:._detail_1ke1k_5')
        if len(keys) == 3:
            print(f"✅ 浏览器ID: {seq}, solana钱包已导入")
            return
        # elif len(keys) == 3:
        #     print(f"⚠️ 浏览器ID: {seq}, 存在多余的钱包, 请确认")
        #     return

        page.ele('@data-testid=chrome_extensions-management-page-add-chrome_extensions-button').click()
        print(f"✅ 浏览器ID: {seq}, 已点击『添加钱包』按钮")

        page.ele('text=导入已有钱包', timeout=5).click()
        print(f"✅ 浏览器ID: {seq}, 已点击『导入已有钱包』按钮")

        page.ele('text=助记词或私钥', timeout=5)

        if not page.ele('css:div[data-pane-id="2"][data-e2e-okd-tabs-pane-active="true"]'):
            page.ele('css:div[data-pane-id="2"]').click()
            print(f"✅ 浏览器ID: {seq}, 已点击『私钥』按钮")
        else:
            print(f"✅ 浏览器ID: {seq}, 已处于『私钥』tab，无需点击")

        page.ele('x://textarea[@placeholder="粘贴或输入你的私钥"]').input(private_key)

        while page.ele('text=确认', timeout=5):
            page.ele('text=确认').click()
            print(f"✅ 浏览器ID: {seq}, 已点击『确认』按钮")
            page.wait(2)
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
    extension_url = "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"
    page.get(extension_url)
    try:
        login = False

        if page.ele('text=发送', timeout=3):
            print(f"🔑 浏览器ID: {seq}, 钱包处于登录态")
            login = True

        # while page.ele('text=确认', timeout=2):
        #     page.ele('text=确认').wait(1).click()

        if not login:
            if page.ele('x://input[@placeholder="请输入密码"]', timeout=5):
                page.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
                if page.ele('text=解锁', timeout=1):
                    page.ele('text=解锁').wait(1).click()
                    print(f"✅ 浏览器ID: {seq}, 已点击『解锁』按钮")
            else:
                print(f"❌ 浏览器ID: {seq}, 导入solana钱包失败, 先导入OKX钱包")
                error_browser_seq.append(seq)
                return

        # while page.ele('text=确认',timeout=2):
        #     page.ele('text=确认').wait(1).click()

        # 查看是否已经导入
        page.ele('text=私钥').click()
        page.wait(1)

        checkboxes = page.eles('._selector_1b6e8_22')
        if len(checkboxes) >= 3:
            checkboxes[index].click()  # 第三个索引是 2
            print(f"✅ 浏览器ID: {seq}, 成功选中自己的 ETH 钱包")
        else:
            print(f"⚠️ 浏览器ID: {seq}, 找不到第 3 个 钱包（共 {len(checkboxes)} 个）")


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


def handle_okx_popup(page, seq, selector='text=OKX Wallet'):
    try:
        okx_tab = safe_click_for_new_tab(page.ele(selector, timeout=2))
        if okx_tab:
            if okx_tab.ele('x://input[@placeholder="请输入密码"]', timeout=5):
                okx_tab.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
            if okx_tab.ele('text=解锁', timeout=1):
                okx_tab.ele('text=解锁').wait(1).click()
            # if okx_tab.ele('text=切换钱包', timeout=1):
            #     okx_tab.ele('text=切换钱包').wait(1).click()
            #     checkbox = okx_tab.ele('.okui-checkbox-circle')
            #     checkbox.click()
            #     if okx_tab.ele('text=确认', timeout=1):
            #         okx_tab.ele('text=确认').wait(1).click()
            #     if okx_tab.ele('text=连接', timeout=1):
            #         okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()

            if okx_tab.ele('text=连接', timeout=3):
                okx_tab = safe_click_for_new_tab(okx_tab.ele('text=连接'), timeout=3)
            max_tries = 10
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
        return False
    except Exception as e:
        print(f'浏览器ID: {seq}, handle_okx_popup error {e}')
        return False

def handle_okx(okx_tab, seq, selector='text=OKX Wallet'):
    try:
        if okx_tab.ele('x://input[@placeholder="请输入密码"]', timeout=5):
            okx_tab.ele('x://input[@placeholder="请输入密码"]').wait(1).input('12345678')
        if okx_tab.ele('text=解锁', timeout=1):
            okx_tab.ele('text=解锁').wait(1).click()
        # if okx_tab.ele('text=切换钱包', timeout=1):
        #     okx_tab.ele('text=切换钱包').wait(1).click()
        #     checkbox = okx_tab.ele('.okui-checkbox-circle')
        #     checkbox.click()
        #     if okx_tab.ele('text=确认', timeout=1):
        #         okx_tab.ele('text=确认').wait(1).click()
        #     if okx_tab.ele('text=连接', timeout=1):
        #         okx_tab = okx_tab.ele('text=连接').wait(1).click.for_new_tab()

        if okx_tab.ele('text=连接', timeout=3):
            okx_tab = safe_click_for_new_tab(okx_tab.ele('text=连接'), timeout=3)
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
