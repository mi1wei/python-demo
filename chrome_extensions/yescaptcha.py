from DrissionPage import Chromium, ChromiumOptions
from bit_api import openBrowser, closeBrowser
from time import sleep
from base.error import error_browser_seq


def is_checkbox_selected_by_svg(page, label_text):
    label = page.ele(f'x://label[.//span[contains(text(),"{label_text}")]]',timeout=1)
    if label.html.__contains__('CheckBoxIcon'):
        return True
    return False


def yescaptcha_drission(row: dict):
    browser_id = row['browser_id']
    seq = row['seq']

    try:
        res = openBrowser(browser_id)
        http_addr = res['data']['http']

        # 初始化 DrissionPage 浏览器连接
        co = ChromiumOptions()
        co.set_address(http_addr)
        chromium = Chromium(co)
        page = chromium.new_tab()

        extension_url = "chrome-extension://jiofmdifioeejeilfkpegipdjiopiekl/popup/index.html"
        page.get(extension_url)

        try:
            # page.ele('x://input[@type="text"]', timeout=5).input('eb11154eadd3f19b47591b2d226bae3ec57c88cf68722')
            # if page.ele('text=保存', timeout=3):
            #     page.ele('text=保存').click()
            #     page.wait(3)

            if page.ele('text=余额', timeout=5):
                print(f"  ✅ 浏览器ID: {seq}, YesCaptcha 人机助手导入成功")
            else:
                print(f"  ❌ 浏览器ID: {seq}, YesCaptcha 人机助手导入失败")
                return

            auto_div = page.ele('xpath=//div[contains(@class, "data-input") and .//span[text()="自动开启"]]', timeout=3)
            # # 打开 YesCaptcha 自动开启
            # if auto_div.html.__contains__('CheckBoxOutlineBlankIcon'):
            #     checkbox = auto_div.ele('x:.//input[@type="checkbox"]')
            #     checkbox.click()
            #     print(f"  ✅ 浏览器ID: {seq},  YesCaptcha 打开 自动开启")

            # 关闭 YesCaptcha 自动开启
            if auto_div.html.__contains__('CheckBoxIcon'):
                checkbox = auto_div.ele('x:.//input[@type="checkbox"]')
                checkbox.click()
                print(f"  ✅ 浏览器ID: {seq},  YesCaptcha 关闭 自动开启")

            # #  打开 文字验证码
            # if not is_checkbox_selected_by_svg(page, '文字验证码'):
            #     # 如果没选中，就点击 checkbox
            #     page.ele(f'x://label[.//span[contains(text(),"文字验证码")]]//input[@type="checkbox"]').click()
            #     print(f"  ✅ 浏览器ID: {seq},  YesCaptcha 打开 文字验证码")
            #
            # page.wait(2)
            #
            # #  打开 Cloudflare
            # if not is_checkbox_selected_by_svg(page, 'Cloudflare'):
            #     # 如果没选中，就点击 checkbox
            #     page.ele(f'x://label[.//span[contains(text(),"Cloudflare")]]//input[@type="checkbox"]').click()
            #     print(f"  ✅ 浏览器ID: {seq},  YesCaptcha 打开 Cloudflare")

            page.wait(10)

        except Exception as e:
            print(f"❌ 浏览器ID: {seq}, 操作过程中发生错误: {e}")
            error_browser_seq.append(seq)

    except Exception as e:
        print(f"❌ 浏览器ID: {seq}, 打开浏览器失败: {e}")
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
