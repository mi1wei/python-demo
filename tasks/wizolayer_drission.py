from DrissionPage import Chromium, ChromiumOptions
from bit_api import *
from chrome_extensions.okx import add_eth_wallet, choice_eth_wallet, handle_okx_popup


def wizolayer_drission(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']
    email = metadata['email']

    extension_url = f"https://wizolayer.xyz?ref=9155701294"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        if page.ele('text=Connect your ', timeout=5):
            page.ele('text=Connect your ').click()
            if page.ele('text=授权应用', timeout=30):
                page.ele('text=授权应用').click()
            # page.get('https://www.goblin.meme/box/685b97de8a7e7ec8bdfd2335')
            # if page.ele('text=START MINING'):
            #     page.ele('text=START MINING').click()

        BOXES = [
            {"index": 1, "id": "685b97de8a7e7ec8bdfd2335", "name": "The Mich Khan"},
            {"index": 2, "id": "685b907a2cf1a69830bbdb67", "name": "The Hiisver Khan"},
            {"index": 3, "id": "6856701d223b22873ed1d730", "name": "The Goblin Khan"},
            {"index": 4, "id": "685b8ec85d0d1a68533c21c2", "name": "The Hiilink Khan"},
        ]

        task_dict = {
            3: 1, 2: 1, 1: 1, 4: 1, 5: 1, 7: 3, 6: 4, 8: 4, 11: 1, 10: 2, 9: 3, 14: 1, 12: 3,
            13: 3, 16: 1, 15: 3, 17: 3, 20: 1, 19: 2, 18: 4, 21: 2, 23: 1, 24: 3, 22: 4, 36: 4,
            25: 3, 26: 2, 27: 3, 28: 3, 29: 3, 30: 3, 31: 3, 32: 4, 33: 3, 35: 1, 34: 4,
            39: 3, 37: 1, 38: 4, 41: 3, 40: 4, 43: 1, 42: 4, 44: 1, 47: 1, 45: 3, 46: 3, 48: 2,
            50: 1, 52: 1, 51: 3, 49: 4, 53: 3, 55: 2, 54: 4, 56: 3, 58: 3, 59: 3, 60: 3,57:3,
            61: 3, 62: 3, 63: 3, 64: 3, 65: 3, 68: 1, 69: 1, 66: 3, 67: 3, 70: 3, 72: 3,
            71: 4, 75: 1, 73: 3, 74: 3, 76: 3, 78: 3, 77: 3, 79: 3, 80: 4, 83: 1, 82: 3,
            84: 3, 85: 3, 87: 3, 86: 4, 90: 1, 89: 3, 88: 4, 93: 1, 91: 3, 94: 1, 92: 3,
            96: 1, 95: 2, 99: 3, 98: 4, 97: 4, 100: 3
        }

        if seq in task_dict:
            box = BOXES[task_dict[seq] - 1]
            page.get(f'https://www.goblin.meme/box/{box["id"]}')
            if page.ele('tag:p@class:text-3xl font-mono text-lime-400', timeout=3):
                print(
                    f"✅ 浏览器ID: {seq}, [{box['index']}] {box['name']}: Mining in progress… {page.ele('tag:p@class:text-3xl font-mono text-lime-400').text}")
                return
            else:
                if page.ele('text=Go to Mission 1', timeout=3):
                    while page.ele('text=Go to Mission 1', timeout=5):
                        page.ele('text=Go to Mission 1').wait(2).click()
                if page.ele('text=Go to Mission 2', timeout=3):
                    while page.ele('text=Go to Mission 2', timeout=5):
                        page.ele('text=Go to Mission 2').wait(2).click()
                page.get(f'https://www.goblin.meme/box/{box["id"]}')
                if page.ele('text=OPEN BOX', timeout=5):
                    page.ele('text=OPEN BOX').click()
                    if page.ele('text=AWESOME!'):
                        page.ele('text=AWESOME!').click()
                while page.ele('text=START MINING'):
                    page.ele('text=START MINING').wait(1).click()
                    print(f"✅ 浏览器ID: {seq}, [{box['index']}] {box['name']}: START MINING")
                page.wait(5)
            return

        for box in BOXES:
            page.get(f'https://www.goblin.meme/box/{box["id"]}')
            if page.ele('tag:p@class:text-3xl font-mono text-lime-400'):
                print(
                    f"✅ 浏览器ID: {seq}, [{box['index']}] {box['name']}: Mining in progress… {page.ele('tag:p@class:text-3xl font-mono text-lime-400').text}")
                return
            else:
                if page.ele('text=Go to Mission 1', timeout=5):
                    while page.ele('text=Go to Mission 1', timeout=5):
                        page.ele('text=Go to Mission 1').wait(2).click()
                if page.ele('text=Go to Mission 2', timeout=5):
                    while page.ele('text=Go to Mission 2', timeout=5):
                        page.ele('text=Go to Mission 2').wait(2).click()
                if page.ele('text=OPEN BOX', timeout=5):
                    page.ele('text=OPEN BOX').click()
                    if page.ele('text=AWESOME!'):
                        page.ele('text=AWESOME!').click()
                    while page.ele('text=START MINING'):
                        page.ele('text=START MINING').wait(1).click()
                    print(f"✅ 浏览器ID: {seq}, [{box['index']}] {box['name']}: START MINING")
                page.wait(5)
        page.wait(1)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
    finally:
        page.close()
        closeBrowser(browser_id)
