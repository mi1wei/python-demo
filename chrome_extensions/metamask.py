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


def metamask_unlock_wallet(page, metadata: dict):
    seq = metadata['seq']
    index_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html"
    page.get(index_url)
    try:
        if page.ele('x://input[@data-testid="unlock-password"]', timeout=5):
            page.ele('x://input[@data-testid="unlock-password"]').wait(1).input('12345678')
            if page.ele('text=登录'):
                page.ele('text=登录').click()
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


def safe_click_for_new_tab(ele, timeout=3):
    try:
        return ele.wait(1).click.for_new_tab(timeout=timeout)
    except Exception as e:
        return None


def metamask_reauthorize(chromium, page, metadata):
    seq = metadata['seq']
    okx_tab = chromium.get_tab(url='nkbihfbeogaeaoehlefnkodbefgpgknn')
    if okx_tab:
        handle_okx(okx_tab, seq)
        page.wait(5)


def handle_okx(okx_tab, seq, selector='text=Phantom Wallet'):
    try:
        if okx_tab.ele('text=连接', timeout=3):
            okx_tab.ele('text=连接').click('js')
        if okx_tab.ele('text=确认', timeout=3):
            okx_tab.ele('text=确认').wait(1).click('js')
        if okx_tab.ele('text=批准', timeout=3):
            okx_tab.ele('text=批准').wait(1).click('js')
        return True
    except Exception as e:
        print(f'浏览器ID: {seq}, handle_okx_popup error {e}')
        return False
