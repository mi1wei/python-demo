from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def _monadscore_drission(choice_eth_wallet_page,page,seq,metadata):
    choice_eth_wallet(choice_eth_wallet_page, metadata, 0)
    try:
        try:
            if page.ele('text=Sign Wallet & Continue ', timeout=5):
                if handle_okx_popup(page, seq, selector='text=Sign Wallet & Continue ') == False:
                    print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")
                    return
        except Exception as e:
            print(f'❌ 浏览器ID: {seq}, {e}, Sign Wallet & Continue Failed')

        try:
            if page.ele('text=Run Node ', timeout=5):
                if handle_okx_popup(page, seq, selector='text=Run Node ') == False:
                    print(f"❌ 浏览器ID: {seq}, Run Node 出现错误")
        except Exception as e:
            pass

        page.wait(2)
        page.get('https://dashboard.monadscore.xyz/tasks')
        tasks = page.eles('text=Do Task')
        for task in tasks:
            task.wait(1).click()

        claims = page.eles('text=Claim')
        print(f"浏览器ID: {seq}, 当前有{len(claims)} 社交任务")
        for claim in claims:
            claim.wait(1).click()

        if page.ele('text=Check In', timeout=2):
            print(f"浏览器ID: {seq}， 点击 Chech In")
            page.ele('text=Check In').wait(1).click()

        page.wait(5)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()



def monadscore_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://dashboard.monadscore.xyz/signup/r/rFWqZ2hQ"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    choice_eth_wallet(chromium.new_tab(), metadata, 0)

    page.get(extension_url)

    if page.ele('text=Connect Wallet', timeout=5):
        page.ele('text=Connect Wallet').click()
        if handle_okx_popup(page, seq) == False:
            print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")
            return
        page.wait(10)

    try:
        try:
            if page.ele('text=Sign Wallet & Continue ', timeout=5):
                if handle_okx_popup(page, seq,selector='text=Sign Wallet & Continue ') == False:
                    print(f"❌ 浏览器ID: {seq}, handle_okx_popup 出现错误")
        except Exception as e:
            print(f'❌ 浏览器ID: {seq}, {e}, Sign Wallet & Continue Failed')

        try:
            if page.ele('text=Run Node ', timeout=5):
                if handle_okx_popup(page, seq,selector='text=Run Node ') == False:
                    # print(f"❌ 浏览器ID: {seq}, Run Node 出现错误")
                    if handle_okx_popup(page, seq, selector='text=Run Node ') == False:
                        print(f"❌ 浏览器ID: {seq}, Run Node 出现错误")
        except Exception as e:
            pass

        page.wait(2)
        print(f"""✅ 浏览器ID: {seq}, Today's Earning: {page.ele('x://h1[@style="font-weight: bold;"]').text}""")
        page.get('https://dashboard.monadscore.xyz/tasks')
        # tasks = page.eles('text=Do Task')
        # for task in tasks:
        #     task.wait(1).click()
        #
        # claims = page.eles('text=Claim')
        # print(f"浏览器ID: {seq}, 当前有{len(claims)} 社交任务")
        # for claim in claims:
        #     claim.wait(1).click()

        if page.ele('text=Check In', timeout=2):
            print(f"浏览器ID: {seq}， 点击 Chech In")
            page.ele('text=Check In').wait(1).click()

        page.wait(5)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
