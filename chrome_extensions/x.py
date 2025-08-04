from bit_api import *
from base.error import error_browser_seq
from DrissionPage import Chromium, ChromiumOptions

def find_x_authorize_tab(chromium: Chromium, retry: int = 5, interval: float = 1.0):
    """最多重试 retry 次查找 OKX 插件页"""
    for attempt in range(retry):
        for tab in chromium.tabs:
            print(tab.title)
            if 'authorize' in tab.title.lower() or 'authorize' in tab.url.lower():
                return tab
        print(f"🔍 第 {attempt + 1}/{retry} 次未找到 X authorize 页，等待 {interval}s 重试...")
        time.sleep(interval)
    return None

def handle_okx(x_tab, seq, selector='text=OKX Wallet'):
    try:
        if x_tab.ele('text=授权应用', timeout=5):
            x_tab.ele('text=授权应用', timeout=5).wait(1).click()
        return True
    except Exception as e:
        print(f'浏览器ID: {seq}, handle_okx_popup error {e}')
        return False

def x_detect(metadata: dict):
    if len(metadata) < 10:
        return

    browser_id = metadata['browser_id']
    seq = metadata['seq']

    extension_url = f"https://x.com/home"

    co = ChromiumOptions()
    res = openBrowser(browser_id)
    co.set_address(res['data']['http'])
    co.set_pref('profile.default_content_setting_values.notifications', 2)
    chromium = Chromium(co)
    page = chromium.latest_tab

    try:
        page.get(extension_url)
        tweets = page.eles('x://div[@data-testid="tweetText"]', timeout=60)
        # for tweet in tweets:
        #     print(tweet.text)
        if len(tweets) > 0:
            ele = page.ele('x://span[contains(@class, "css-1jxf684") and contains(text(), "@")]')
            if ele:
                print(f"✅ 浏览器ID: {seq}, X 登陆状态正常 {ele.text}, 主页帖子数量: {len(tweets)}")
            else:
                print(f"✅ 浏览器ID: {seq}, X 登陆状态正常, 主页帖子数量: {len(tweets)}")
        else:
            print(f"❌ 浏览器ID: {seq}, X 登陆状态异常")
            error_browser_seq.append(seq)
    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 出现错误: {e}")
        error_browser_seq.append(seq)
    finally:
        page.close()
        closeBrowser(browser_id)