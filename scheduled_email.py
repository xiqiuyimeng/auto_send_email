# -*- coding: utf-8 -*-
import sys
sys.path.append('../')  # 为了能在命令行启动
from auto_send_email.send_email import Email
from datetime import datetime
import schedule
import requests
import json
_author_ = 'luwt'
_date_ = '2019/8/7 10:40'


ciba_url = 'https://api.ooopn.com/ciba/api.php'
from_address = '847466569@qq.com'
login_pwd = 'ywuppyiilnwsbejb'
to_address = {
    'self': 'JEET847466569@163.com',
}


# 获取金山词霸每日一词，返回中文和英文两句话，图片
def get_ciba_everyday_sentence():
    response = requests.get(ciba_url)
    result = json.loads(response.text)
    return result.get('ciba'), result.get('ciba-en'), result.get('imgurl')


def send(sub, content):
    try:
        email = Email(from_address, login_pwd, to_address.get('self'), sub, content)
        email.send_email()
    except Exception as e:
        raise e
    print("{} 邮件发送成功！".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def morning_job():
    ch, en, img_url = get_ciba_everyday_sentence()
    mail_sub = '{}日常上班打卡提醒！'.format(datetime.now().strftime('%Y-%m-%d'))
    mail_content = '上班时间{}，记得打卡，一个月只有五次补卡机会！<br/>{}<br/>{}<br/><img src="{}">'\
        .format(datetime.now().strftime('%H:%M'), ch, en, img_url)
    send(mail_sub, mail_content)


def nightfall_job():
    ch, en, img_url = get_ciba_everyday_sentence()
    mail_sub = '{}日常下班打卡提醒！'.format(datetime.now().strftime('%Y-%m-%d'))
    mail_content = '下班时间{}，记得打卡，一个月仅仅五次补卡的机会！<br/>{}<br/>{}<br/><img src="{}">'\
        .format(datetime.now().strftime('%H:%M'), ch, en, img_url)
    send(mail_sub, mail_content)


def task_run():
    print('任务开始')
    schedule.every().day.at('08:55').do(morning_job)
    schedule.every().day.at('18:00').do(nightfall_job)
    while True:
        # Monday == 0 ... Sunday == 6
        if datetime.now().weekday() == 6:
            continue
        schedule.run_pending()


if __name__ == '__main__':
    task_run()
