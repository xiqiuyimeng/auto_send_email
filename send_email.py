# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
_author_ = 'luwt'
_date_ = '2019/8/6 17:19'


class Email:

    """
    from_addr: 发件人邮箱地址
    pwd: 发件人授权码，用于第三方邮箱登录
    to_addr: 收件人邮箱地址
    subject: 邮件主题
    content: 邮件内容，目前为字符串文本
    smtp_server: 默认163，如果有其他可以自己设置
    """
    def __init__(self, from_addr, pwd, to_addr, subject, content, smtp_server=None):
        self.from_addr = from_addr
        self.pwd = pwd
        self.to_addr = to_addr
        self.subject = subject
        self.content = content
        self.smtp_server = 'smtp.163.com' if not smtp_server else smtp_server
        self.server = smtplib.SMTP(self.smtp_server, 25, local_hostname='localhost')
        self.login()

    def login(self):
        self.server.login(self.from_addr, self.pwd)

    @staticmethod
    def format_address(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def append_msg(self):
        # 目前仅发送文本，故设置为plain
        msg = MIMEText(self.content, 'plain', 'utf-8')
        msg['From'] = self.format_address('发送人<{}>'.format(self.from_addr))
        msg['To'] = self.format_address('管理员<{}>'.format(self.to_addr))
        msg['Subject'] = Header(self.subject, 'utf-8').encode()
        return msg

    def send_email(self):
        self.server.sendmail(self.from_addr, [self.to_addr], self.append_msg().as_string())
        self.server.quit()
