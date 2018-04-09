#-*-coding:utf-8-*-

import time
from threading import Timer
import smtplib
import datetime
import requests
import re
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
total = 0
lastesttitle =""
oneDaySeconds = 60 * 60 * 24

subject = "来自韩博的每日监控提醒"

class EmailSend(object):
    def __init__(self, msgto, data, subject):
        self.msgTo = msgto
        self.data2 = data
        self.Subject = subject

    def sendEmail(self):
        msg = MIMEText(self.data2, 'plain', 'utf-8')
        msg['Subject'] = self.Subject
        msg['From'] = 'hanbo_ph@163.com' #'hmhanbo@outlook.com'
        msg['To'] = self.msgTo
        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.163.com', 25)
            smtp.login(msg['From'], 'zgsxhm111')  #'Hb4289197'
            smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
            print('邮件发送成功')
        except Exception as e:
            print('--------邮件发送失败错误：--------', e)


def pbc_req(url):
    import requests
    import re

    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.pbc.gov.cn",
        "Referer": "diagnostics://4/",
        "Cookie": "_gscu_1042262807=749843495iifnl11; wzwsconfirm=acce31e19f7527b3d684c5f77608d920; wzwsvtime=1523283333; wzwstemplate=Mg==; wzwschallenge=-1; ccpassport=f646f9a1ec11821ae517049d2ab81611",
    }

    req = requests.get(url, headers=headers)
    #req = requests.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "lxml")
    return soup.find_all(name='a', attrs={"href": re.compile(r"/zhengcehuobisi/125207/125213/125431/125469/\d+/index\.html")})


def worker(sendTo, url):
    global total
    global lastesttitle
    total += 1
    if total < 5:
        fd = pbc_req(url)
        if lastesttitle == fd[0].get_text():
            bodypart2 = "跟前一次一样"
        else:
            bodypart2 = "发现更新，请注意！！！"

        lastesttitle = fd[0].get_text()
        bodypart1 = "现在时刻是：%s , 第 %d 次执行\n\n" % (nowTime, total)
        bodypart3 = '\n\n最新的公告为：' + lastesttitle
        body = bodypart1 + bodypart2 + bodypart3

        print(body)
        sendtask = EmailSend(sendTo, body, subject)
        # sendtask.sendEmail()
        Timer(oneDaySeconds, worker).start()

pbc_url = 'http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/index.html'
receivers = "hmhanbo@outlook.com" + ", hanbo@phfund.com.cn"
worker(receivers, pbc_url)
