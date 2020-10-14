#!/usr/bin/env python
# coding=utf-8
import logging
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

logger = logging.getLogger("eastmoneycrawler")


def send_email(title, content, receiver_emails):
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
    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)
    msg = MIMEText(content, "plain", 'utf-8')
    msg["Subject"] = Header(title, 'utf-8')
    msg["From"] = sender_qq_mail
    for receiver_email in receiver_emails:
        msg["To"] = receiver_email
        smtp.sendmail(sender_qq_mail, receiver_email, msg.as_string())
        logger.warning("{} {} send email success".format(datetime.now(), receiver_email))
    smtp.quit()
