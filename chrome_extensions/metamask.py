from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions
import traceback


def metamask_add_wallet(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    mnemonic = metadata['my_metamask_eth_wallet_mnemonic']

    res = openBrowser(browser_id)
    http_addr = res['data']['http']
    # 初始化 DrissionPage 浏览器连接
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    onboarding_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome"
    index_url = "chrome-extension://ejjladinnckdgjemekebdpeokbikhfci/index.html"
    page.get(onboarding_url)
    try:

        if page.ele('text=登录', timeout=20):
            print(f"✅ 浏览器ID: {seq}, 钱包已导入")
            page.wait(10)
            return

        if page.ele('x://input[@data-testid="onboarding-terms-checkbox"]', timeout=10):
            page.ele('x://input[@data-testid="onboarding-terms-checkbox"]', timeout=10).click('js')

        if page.ele('text=导入现有钱包', timeout=10):
            page.ele('text=导入现有钱包', timeout=10).click('js')
            print(f"✅ 浏览器ID: {seq}, 已点击『导入现有红包』按钮")

        page.ele('text=我同意', timeout=5).click('js')

        words = mnemonic.split()
        for i, word in enumerate(words):
            selector = f'x://input[@data-testid="import-srp__srp-word-{i}"]'
            page.ele(selector).input(word)

        page.ele('x://button[@data-testid="import-srp-confirm"]').click('js')
        print(f"✅ 浏览器ID: {seq}, 已点击『确认私钥助记词』按钮")

        page.ele('x://input[@data-testid="create-password-new"]').input('12345678')
        page.ele('x://input[@data-testid="create-password-confirm"]').input('12345678')
        page.ele('x://input[@data-testid="create-password-terms"]').click('js')

        page.ele('x://button[@data-testid="create-password-import"]').click('js')

        page.ele('text=完成', timeout=5).click('js')
        if page.ele('text=下一步', timeout=5):
            page.ele('text=下一步', timeout=5).click('js')
        page.ele('text=完成', timeout=5).click('js')
        if page.ele('text=明白了', timeout=5):
            page.ele('text=明白了', timeout=5).click('js')
        page.wait(10)
        print(f"✅ 浏览器ID: {seq}, 导入钱包成功")

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        traceback.print_exc()
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


def unlock_wallet(page, metadata: dict):
    seq = metadata['seq']
    index_url = "chrome-extension://ejjladinnckdgjemekebdpeokbikhfci/index.html"
    page.get(index_url)
    try:
        if page.ele('x://input[@placeholder="Password"]', timeout=5):
            page.ele('x://input[@placeholder="Password"]').wait(1).input('A@qwe1994720')
            if page.ele('text=Unlock'):
                page.ele('text=Unlock').click()
                # print(f"✅ 浏览器ID: {seq}, 导入solana钱包成功")
        page.wait(2)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        try:
            page.close()
        except Exception as e:
            print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")


def add_eth_wallet(metadata: dict):
    browser_id = metadata['browser_id']
    seq = metadata['seq']
    private_key = metadata['my_okx_solana_wallet_private_key']

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
        if page.ele('x://input[@placeholder="密码"]', timeout=5):
            page.ele('x://input[@placeholder="密码"]').wait(1).input('12345678')
            if page.ele('text=解锁'):
                page.ele('text=解锁').click()
                # print(f"✅ 浏览器ID: {seq}, 导入solana钱包成功")

        page.ele('x://button[@data-testid="settings-menu-open-button"]').wait(5).click()
        page.wait(1)
        accounts_div = page.ele('#accounts')
        buttons = accounts_div.eles('t:button')
        wallet_names = [btn.eles('t:div')[-1].text for btn in buttons]
        # print(f"✅ 浏览器ID: {seq}, {wallet_names}")
        if len(wallet_names) >= 2:
            account = page.ele('x://div[@data-testid="home-header-account-name"]').text
            if account == "solana":
                buttons[1].click()
                account = page.ele('x://div[@data-testid="home-header-account-name"]').text
            print(f"✅ 浏览器ID: {seq}, 当前账户 {account}")
            return
        page.ele('x://button[@data-testid="sidebar_menu-button-add_account"]').click()
        page.wait(1)
        page.ele('text=导入私钥').click()
        page.ele('x://input[@name="name"]').input('solana2')
        page.ele('x://textarea[@placeholder="私钥"]').input(private_key)
        page.ele('text=导入').click()
        print(f"✅ 浏览器ID: {seq}, 添加新钱包成功")
        page.wait(1)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        try:
            page.close()
        except Exception as e:
            print(f"⚠️ 浏览器ID: {seq}, 关闭页面失败: {e}")


def open_devnet(page, metadata: dict):
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
        openTestNetwork = False
        if page.ele('text=您目前处于测试网模式', timeout=2):
            openTestNetwork = True
            print(f"✅ 浏览器ID: {seq}, devnet 模式已打开")
        if openTestNetwork == False:
            page.ele('x://button[@data-testid="settings-menu-open-button"]').click()
            page.ele('x://button[@data-testid="sidebar_menu-button-settings"]').click()
            page.ele('x://button[@id="settings-item-developer-settings"]').click()
            page.ele('x://button[@id="toggleTestNetwork"]').click()
            print(f"✅ 浏览器ID: {seq}, 打开devnet")
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()


def safe_click_for_new_tab(ele, timeout=3):
    try:
        return ele.wait(1).click.for_new_tab(timeout=timeout)
    except Exception as e:
        return None


def handle_okx(okx_tab, seq, selector='text=Phantom Wallet'):
    try:
        if okx_tab.ele('text=Sign In', timeout=3):
            okx_tab.ele('text=Sign In').wait(1).click('js')
        return True
    except Exception as e:
        print(f'浏览器ID: {seq}, handle_okx_popup error {e}')
        return False
