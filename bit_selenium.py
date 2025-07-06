import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bit_api import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
res = openBrowser("59ccf9a3ab17495d9dbbe453517f4c88")  # 窗口ID从窗口配置界面中复制，或者api创建后返回

print(res)

ip = {

}

driverPath = res['data']['driver']
debuggerAddress = res['data']['http']

# selenium 连接代码
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)

chrome_service = Service(driverPath)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


handles = driver.window_handles
for handle in handles:
    driver.switch_to.window(handle)
    if "C77CD536F8A2978DD967DBED4AF52F0D" in driver.title:
        break

# 3. 等待插件页面加载
wait = WebDriverWait(driver, 20)

# 示例：点击“我已有钱包”
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '导入已有钱包')]"))).click()


def sosovalue():
    driver.get("https://sosovalue.com/zh/exp")
    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)

    task_1 = wait.until(EC.visibility_of_element_located(
        (By.XPATH, ".//h5[text()='分享比特币储备看板']")
    ))

    # 基于任务名元素定位按钮（使用相对XPath，查找后续兄弟按钮）
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[contains(@class, 'MuiButton-contained') and .//span[text()='分享']]")
    ))

    task_2 = wait.until(EC.visibility_of_element_located(
        (By.XPATH, ".//h5[text()='点赞']")
    ))

    # 基于任务名元素定位按钮（使用相对XPath，查找后续兄弟按钮）
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[contains(@class, 'MuiButton-contained') and .//span[text()='分享']]")
    ))

    # 输出定位结果
    print(f"找到任务：{task_1.text}")
    print(f"按钮文本：{button.text}")

    button.click()

    share_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'div.w-6.h-6.flex.justify-center.items-center.bg-background-hover-50-800.rounded.cursor-pointer'
        ))
    )

    # 等待元素完全可交互
    wait.until(
        EC.element_to_be_clickable(share_button)
    )

    # 点击元素
    share_button.click()

    time.sleep(2)

    driver.get("https://sosovalue.com/zh/exp")

    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[contains(@class, 'MuiButton-contained') and .//span[text()='验证']]")
    ))

    button.click()

    # # 等待页面加载，定位任务容器（根据实际结构调整等待条件）
    # task_containers = driver.find_elements(By.CSS_SELECTOR, 'div.rounded-lg.gap-x-4.grid.grid-cols-2.gap-y-4 > div')
    #
    # # 提取任务名称
    # task_names = []
    # for container in task_containers:
    #     # 定位任务名称所在的<span>标签（class="font-medium"）
    #     task_name_element = container.find_element(By.CSS_SELECTOR, 'span.font-medium')
    #     task_names.append(task_name_element.text.strip())
    #
    # # 输出结果
    # print("新手祝福: ")
    # print("未完成的任务: ")
    # for idx, name in enumerate(task_names, 1):
    #     print(f"{idx}. {name}")


# # 以下为PC模式下，打开baidu，输入 BitBrowser，点击搜索的案例
# driver.get('https://www.baidu.com/')
#
# input = driver.find_element(By.CLASS_NAME, 's_ipt')
# input.send_keys('BitBrowser')
#
# print('before click...')
#
# btn = driver.find_element(By.CLASS_NAME, 's_btn')
# btn.click()
#
# print('after click')
