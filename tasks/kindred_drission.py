from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx
from base.error import error_browser_seq
import traceback
from chrome_extensions.metamask import metamask_unlock_wallet, metamask_reauthorize

code = 'HKQLH0U6'


def register(chromium, page, metadata, extension_url='https://waitlist.kindredlabs.ai?code=C6886CF'):
    page.get(extension_url)

    if page.ele('text=in', timeout=10):
        page.ele('x:(//div[@class="mt-5 flex items-center justify-center gap-x-4"]//button)[3]').click()
        page.wait(5)
        metamask_reauthorize(chromium, page, metadata)

    if page.ele('text=dashboard', timeout=10):
        page.ele('text=dashboard').click('js')
        page.wait(10)

    if page.ele('text=Claim Reward', timeout=10):
        page.ele('text=Claim Reward').click('js')

    social_tasks = page.eles('x://button[.//b[contains(text(), "Now")]]')
    for index, social_task in enumerate(social_tasks):
        social_task.wait(1).click('js')

        # page.refresh()
        page.wait(5)
        metamask_reauthorize(chromium, page, metadata)

        while page.ele('text=Loading ...'):
            print(f"✅ 浏览器ID: {metadata['seq']}, Social Task Loading ...")
            page.wait(10)

        if page.ele('text=Claim reward'):
            page.ele('text=Claim reward').click('js')
            print(f"✅ 浏览器ID: {metadata['seq']}, social task")
            page.wait(5)

    daily_tasks = page.eles('x://button[.//b[contains(text(), "Visit X")]]')
    for index, daily_task in enumerate(daily_tasks):
        print(daily_task.html)
        daily_task.wait(1).click('js')

        page.wait(5)
        metamask_reauthorize(chromium, page, metadata)

        while page.ele('text=Loading ...'):
            print(f"✅ 浏览器ID: {metadata['seq']}, Daily Task Loading ...")
            page.wait(10)

        if page.ele('text=Claim reward'):
            page.ele('text=Claim reward').click('js')
            print(f"✅ 浏览器ID: {metadata['seq']}, daily task")
            page.wait(5)

    page.wait(2)


def kindred_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://waitlist.kindredlabs.ai?code=C6886CF"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    metamask_unlock_wallet(chromium.new_tab(), metadata)
    # choice_eth_wallet(chromium.new_tab(), metadata, 0)

    try:
        register(chromium, page, metadata)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        traceback.print_exc()
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)
