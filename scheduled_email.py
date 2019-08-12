# -*- coding: utf-8 -*-
import sys
sys.path.append('../')  # 为了能在命令行启动
from auto_send_email.send_email import Email
from auto_send_email import config
from datetime import datetime
import schedule
import requests
import json
_author_ = 'luwt'
_date_ = '2019/8/7 10:40'


ciba_url = config.ciba_url
from_address = config.from_address
login_pwd = config.login_pwd
self_address = config.to_address.get('self')
shaqiang_address = config.to_address.get('shaqiang')


# 获取金山词霸每日一词，返回中文和英文两句话，图片
def get_ciba_everyday_sentence():
    response = requests.get(ciba_url)
    result = json.loads(response.text)
    return result.get('ciba'), result.get('ciba-en'), result.get('imgurl')


def send(sub, content, to_address):
    try:
        email = Email(from_address, login_pwd, to_address, sub, content)
        email.send_email()
    except Exception as e:
        raise e
    print("{} 邮件发送成功！".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def morning_job():
    ch, en, img_url = get_ciba_everyday_sentence()
    mail_sub = '{}日常上班打卡提醒！'.format(datetime.now().strftime('%Y-%m-%d'))
    mail_content = '<h1>上班时间{}，记得打卡，一个月只有五次补卡机会！</h1><br/>{}<br/>{}<br/><img src="{}">'\
        .format(datetime.now().strftime('%H:%M'), ch, en, img_url)
    send(mail_sub, mail_content, self_address)


def morning_job_shaqiang():
    ch, en, img_url = get_ciba_everyday_sentence()
    mail_sub = '{}日常上班打卡提醒！'.format(datetime.now().strftime('%Y-%m-%d'))
    mail_content = '<h1>人生既然不能彩排，那就尽情演义。一天就是一辈子，打卡时间{}又到了，' \
                   '珍惜这美好的一天(天底下第二帅的你)</h1><br/>{}<br/>{}<br/><img src="{}">'\
        .format(datetime.now().strftime('%H:%M'), ch, en, img_url)
    send(mail_sub, mail_content, shaqiang_address)


def nightfall_job():
    ch, en, img_url = get_ciba_everyday_sentence()
    mail_sub = '{}日常下班打卡提醒！'.format(datetime.now().strftime('%Y-%m-%d'))
    mail_content = '<h1>下班时间{}，记得打卡，一个月仅仅五次补卡的机会！</h1><br/>{}<br/>{}<br/><img src="{}">'\
        .format(datetime.now().strftime('%H:%M'), ch, en, img_url)
    send(mail_sub, mail_content, self_address)


def task_run():
    print('任务开始')
    schedule.every().day.at('08:25').do(morning_job_shaqiang)
    schedule.every().day.at('08:55').do(morning_job)
    schedule.every().day.at('18:00').do(nightfall_job)
    while True:
        # Monday == 0 ... Sunday == 6
        if datetime.now().weekday() == 6:
            continue
        schedule.run_pending()


if __name__ == '__main__':
    task_run()
