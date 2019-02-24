#-*-coding:utf-8-*-



"""

"""

lastestTitle=""
times = 1

class PhEmailService(object):
    def __init__(self, msgto, body, subject):
        self.msgTo = msgto
        self.body = body
        self.subject = subject
    def sendEmail(self):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        msg = MIMEText(self.body, 'plain', 'utf-8')
        msg['Subject'] = self.subject
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


class LoopClock(object):
    def __init__(self, interval_hours, loop_times, function, args=None):
        self.function = function
        self.interval_hours = interval_hours
        self.loop_times = loop_times
        self.args = args if args is not None else []
        # self.kwargs = kwargs if kwargs is not None else {}
        self.counter = 0
    
    def loop(self):
        from threading import Timer
        while self.counter <= self.loop_times:
            self.function(self.args)
            self.counter += 1
            Timer(self.interval_hours, self.loop).run()
        else:
            print("loop ended...")


def req_pbc_openMarket():
    # 货币政策司 > 货币政策工具 > 公开市场业务 
    import requests
    import re
    from bs4 import BeautifulSoup
    base_url = "http://www.pbc.gov.cn/"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            "Cookie": "wzws_cid=a60fae8b0cba845611f0e14016984a4259f44c6c5d2f6a1c3f26b933811eba378cbff0c9993b9651d7c947c6db6e557c",
        }
    url = base_url + "zhengcehuobisi/125207/125213/125431/index.html"
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "lxml")
    # 返回标题列表
    titleList = soup.find_all(name='a', attrs={"href": re.compile(r"/zhengcehuobisi/125207/125213/125431/125469/\d+/index\.html")})
    firstTitle = titleList[0].get_text()

    return firstTitle



def worker(ph_email_service):
    import time
    import datetime
    global lastestTitle
    global times
    # 设置邮件内容
    ph_email_service.subject = "来自韩博的监控提醒"
    ph_email_service.body = "公开市场业务公告发现更新"
    nowTitle = req_pbc_openMarket()
    if times != 1 and lastestTitle != nowTitle:
        # 发邮件
        ph_email_service.sendEmail()

    lastestTitle = nowTitle
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("现在时刻是：%s , 第 %d 次执行\n\n" % (nowTime, times))
    print('最新的公告为：' + lastestTitle)

    times += 1



def main():
    # 设置邮件收件人
    msgto= "hmhanbo@outlook.com" + ", hanbo_ph@163.com"
    ph_email_service = PhEmailService(msgto,"","")
    # 设置定时器
    loopClock = LoopClock(24, 5, worker, (ph_email_service))
    # 开启定时器
    loopClock.loop()



if __name__=='__main__':
    main()
    # print(req_pbc_openMarket())

