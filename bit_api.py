import requests
import json
import time
import os

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}


def createBrowser(json_data):  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    res = requests.post(f"{url}/browser/update",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    browserId = res['data']['id']
    time.sleep(2)
    print(browserId)
    return browserId


proxies = [
    "23.27.127.175:7140:hyzb8888:Aa666888",
    "108.165.180.247:6210:hyzb8888:Aa666888",
    "46.203.52.209:5732:hyzb8888:Aa666888",
    "108.165.180.202:6165:hyzb8888:Aa666888",
    "46.203.52.251:5774:hyzb8888:Aa666888",
    "23.26.53.218:6184:hyzb8888:Aa666888",
    "108.165.180.184:6147:hyzb8888:Aa666888",
    "46.203.52.55:5578:hyzb8888:Aa666888",
    "23.26.47.202:6668:hyzb8888:Aa666888"
]


def createBrowsers():  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档

    for proxy in proxies:
        parts = proxy.split(":")
        if len(parts) == 4:
            host, port, proxyUserName, proxyPassword = parts
            print(f"host: {host}, port: {port}, proxyUserName: {proxyUserName}, proxyPassword: {proxyPassword}")
        else:
            print(f"Invalid proxy format: {proxy}")
            return

        json_data = {
            'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
            'proxyType': 'socks5',
            'host': host,  # 代理主机
            'port': port,  # 代理端口
            'proxyUserName': proxyUserName,  # 代理账号
            'proxyPassword': proxyPassword,
            'syncCookies': True,
            'syncIndexedDb': True,
            'syncLocalStorage': True,
            'syncBookmarks': True,
            'syncAuthorization': True,
            'syncHistory': True,
            # 'syncExtensions': True,
            'browserFingerPrint': {
                'isIpCreateLanguage': False,
                'languages': 'zh-CN',
                'displayLanguages': 'zh-CN'
            }
        }
        createBrowser(json_data)


def updateBrowser(
        ids):  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入

    #  ['noproxy', 'http', 'https', 'socks5', 'ssh']
    json_data = {'ids': ids,
                 # 'host': '103.76.117.115',
                 # 'syncCookies': True,
                 # 'syncIndexedDb': True,
                 # 'syncLocalStorage': True,
                 # 'syncBookmarks': True,
                 # 'syncAuthorization': True,
                 # 'syncHistory': True,
                 'proxyType': 'socks5'
                 }
    res = requests.post(f"{url}/browser/update/partial",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    return res


def closeBrowser(id):  # 关闭窗口
    json_data = {'id': f'{id}'}
    requests.post(f"{url}/browser/close",
                  data=json.dumps(json_data), headers=headers).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {'id': f'{id}'}
    print(requests.post(f"{url}/browser/delete",
                        data=json.dumps(json_data), headers=headers).json())


def listBrowsers():  # 列出所有窗口
    json_data = {
        "page": 0,
        "pageSize": 100,
        "sort": "asc"
    }
    browsers = requests.post(f"{url}/browser/list",
                             data=json.dumps(json_data), headers=headers).json()
    # print(browsers)
    return browsers


def getEnvIds():
    browsers = listBrowsers()
    ids = []
    for browser in browsers['data']['list']:
        print(browser['id'])
        ids.append(browser['id'])
    return ids


def export_proxy_to_txt(proxy_list, output_file="proxy_list.txt"):
    """从JSON数据中提取代理信息并导出到txt文件"""

    # 确保列表不为空
    if not proxy_list:
        print("错误：JSON数据中没有找到代理信息")
        return False
    # 用于存储提取的代理信息
    extracted_proxies = []


def export_env_id_proxy_to_txt(proxy_list, output_file="id_proxy_list.txt"):
    """从JSON数据中提取代理信息并导出到txt文件"""

    # 确保列表不为空
    if not proxy_list:
        print("错误：JSON数据中没有找到代理信息")
        return False
    # 用于存储提取的代理信息
    extracted_proxies = []

    # 遍历所有代理条目
    for proxy in proxy_list:
        id = proxy.get('id', '')
        host = proxy.get('host', '')
        port = proxy.get('port', '')
        username = proxy.get('proxyUserName', '')
        password = 'Aa666888'
        # 添加到提取列表
        proxy_line = f"{id},{host},{port},{username},{password}"
        extracted_proxies.append(proxy_line)

        # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(extracted_proxies))

    print(f"成功提取 {len(extracted_proxies)} 个代理信息到 {os.path.abspath(output_file)}")
    return True


if __name__ == '__main__':
    # updateBrowser()
    # browsers = listBrowsers()
    getEnvIds()
    updateBrowser(getEnvIds())

    # export_proxy_to_txt(browsers['data']['list'])
    # export_env_id_proxy_to_txt(browsers['data']['list'])

    # createBrowsers()

    # browser_id = createBrowser()
    # browser_id = '6477f2084fca419b9c583421ce2f84e6'
    # print(openBrowser(browser_id))
    #
    # time.sleep(10)  # 等待10秒自动关闭窗口
    #
    # print(closeBrowser(browser_id))
    #
    # time.sleep(10)  # 等待10秒自动删掉窗口

    # deleteBrowser(browser_id)
