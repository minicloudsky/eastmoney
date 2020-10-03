#!/usr/bin/env python
# coding=utf-8
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import random

# 邮件正文内容
contents = []
# 邮件标题
titles = [
]


def send_email():
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = ''
    """
    pwd为 qq邮箱的授权码
    qq邮箱授权码获取，参考:
    https://baijiahao.baidu.com/s?id=1552315463915496&wfr=spider&for=pc
    """
    pwd = ''
    # 发件人的邮箱
    sender_qq_mail = ''
    # 收件人邮箱
    receiver = ''
    # 邮件的正文内容
    mail_content = random.choice(titles) + random.choice(contents)
    # 邮件标题
    mail_title = random.choice(titles)

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
    print("发送成功")


if __name__ == '__main__':
    send_email()
