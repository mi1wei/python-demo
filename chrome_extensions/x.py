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
