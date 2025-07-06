import requests
import time
from configuration.primary.xinlan import uid, sign

APIurl = 'https://bsh.bhdata.com:30015/bhmailer'

# 修改为自己需求的目标邮件
title = '是你的'  # 目标邮件的标题
from1 = 'info@x.com'  # 目标邮件的发件人 from不能用作python变量，所以用了任意如from1
fields = '$TITLE-R|\d{6}$'  # 从邮件HTML源代码中截取第一个链接 详见官网接口说明自定义邮件导出规则部分


# 定义函数无需修改
def checkMail(email, password):
    timestamp = round(time.time() * 1000)  # 13位时间戳
    sent = timestamp - 1800000  # 指定邮件发送时间为当前请求时间减去60秒防止时差
    # 发送GET请求
    response = requests.get(
        APIurl + '?uid=' + uid + '&sign=' + sign + '&act=checkMail&email=' + email + '&pass=' + password + '&title=' + title + '&from=' + from1 + '&sent=' + str(
            sent) + '&fields=' + fields + '&t=' + str(timestamp))
    # 获取接口返回的JSON数据
    jsonlist = response.json()
    # 解析返回值
    code = jsonlist["code"]
    msg = jsonlist["msg"]

    while code == 5:
        # print(jsonlist)
        time.sleep(15)
        response = requests.get(
            APIurl + '?uid=' + uid + '&sign=' + sign + '&act=getResult&id=' + msg + '&t=' + str(timestamp))
        # 获取接口返回的JSON数据
        jsonlist = response.json()
        # 解析返回值
        code = jsonlist["code"]
        msg = jsonlist["msg"]
    else:
        return msg


if __name__ == "__main__":
    # 调用函数 密码为空时则邮箱必须提前导入到心蓝助手里，带上密码则自动添加邮箱到心蓝里收信
    print(checkMail('aeksnejx@mailxw.com', ''))
