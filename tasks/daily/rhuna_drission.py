from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup
from base.error import error_browser_seq
from chrome_extensions.petra_aptos import unlock_wallet, handle_okx


def register(chromium, page, seq, extension_url):
    page.get(extension_url)
    if page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        page.wait(3)
        try:
            okx_tab = chromium.get_tab(url='ejjladinnckdgjemekebdpeokbikhfci')
            if okx_tab:
                handle_okx(okx_tab, seq)
        except Exception as e:
            pass
    page.wait(2)
    if page.ele('text=Apply Code', timeout=3):
        page.ele('text=Apply Code', timeout=3).wait(1).click('js')
        page.wait(2)

def daily_check_in(chromium, page, seq, extension_url="https://portal.rhuna.io/quests"):
    page.get(extension_url)
    while page.ele('text=Connect Wallet', timeout=10):
        page.ele('text=Connect Wallet').wait(1).click('js')
        page.wait(3)
        try:
            okx_tab = chromium.get_tab(url='ejjladinnckdgjemekebdpeokbikhfci')
            if okx_tab:
                handle_okx(okx_tab, seq)
        except Exception as e:
            pass
    page.wait(5)

    if page.ele('text=Daily Check-in'):
        page.ele('text=Daily Check-in').wait(1).click('js')
        if page.ele('text=Claim', timeout=2):
            page.ele('text=Claim').wait(1).click('js')
            print(f'✅ 浏览器ID: {seq}, Daily Check-in')
        elif page.ele('text=Quest completed successfully!', timeout=2):
            print(f'✅ 浏览器ID: {seq}, Daily Check-in Completed')
        else:
            print(f"❌ 浏览器ID: {seq}, Daily Check-in error")
            error_browser_seq.append(seq)

#  A@qwe1994720
def rhuna_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://portal.rhuna.io/?referralCode=wise-hurricane-9745&address=0x85515a73aae43c35b196a4b70c8398105ac0a0817c6c7707b08120031ce6dfa1"
    url_1 = "https://portal.rhuna.io/?referralCode=cheerful-hurricane-5031&address=0xdf89e814fed90e6a574b07fd33204eab9e8b9f5f2f5e9d4fb00ae01f47b1a6ec"
    url_2 = "https://portal.rhuna.io/?referralCode=energetic-summoner-1440&address=0xe2fb0aa6f2b3e1c8fca9a7c6fa72cefcd84e4dc8d55cb71d76c4252931e24cfb"
    url_3 = "https://portal.rhuna.io/?referralCode=furious-plasma-3017&address=0x41d4399176e4a0c1a60ee2304e1b5b181a7e32759ad3e8cbf1d836f272d076c7"
    url_4 = "https://portal.rhuna.io/?referralCode=breezy-lizard-8359&address=0x108a210a2bfea056b5036df955a792904e3aff07259d0689712ba5e7b6a1f783"
    url_5 = "https://portal.rhuna.io/?referralCode=stormy-bear-3266&address=0x5562efb2c24804692cec062c6938cf85edaf8356de0dbd3a990075ffc82fb05e"
    url_6 = "https://portal.rhuna.io/?referralCode=friendly-gladiator-3498&address=0xa8484ba1bfd6e3d6df2c4d67d7c0505662b84f415a98c9cb447b48b76fbdc61b"
    url_7 = "https://portal.rhuna.io/?referralCode=cheerful-samurai-4134&address=0xac2e9eb3fa4916d885fce628c96c662e1e410ab2d8e19c675b275cc529d89c13"
    url_8 = "https://portal.rhuna.io/?referralCode=vigorous-thunder-1078&address=0xd2cf4b64998634d9b517c36520355419680036fda148d1d44295c842e0c7e180"
    url_9 = "https://portal.rhuna.io/?referralCode=skillful-gazelle-2554&address=0x1851fc2292fb981f066d07dc4563a6c0c7861b4e451ca7ca3976fabb376cd760"
    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    unlock_wallet(chromium.new_tab(), metadata)

    try:
        # register(chromium, page, seq, extension_url)
        daily_check_in(chromium, page, seq)
        page.wait(15)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
