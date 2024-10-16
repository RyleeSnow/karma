# -- coding: utf-8 --

import smtplib
import urllib.parse
import urllib.request
from email.mime.text import MIMEText


def wechat_notification(message_title, message='', key='[SENDKEY]'):
    '''
    Send message to wechat (using https://sct.ftqq.com/)

    Args:
        message_title: str, title of the message
        message: str, content of the message
        key: str, sendkey of the wechat
    Returns:
        result: str, result of the message
    '''

    postdata = urllib.parse.urlencode({'text': message_title, 'desp': message}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result


def email_notification(message_title, message, mail_host, mail_user, mail_pass, sender, receivers):
    '''
    Send message to email (using smtp)

    Args:
        message_title: str, title of the message
        message: str, content of the message
        mail_host: str, host of the email
        mail_user: str, user of the email
        mail_pass: str, password of the email
        sender: str, sender of the email
        receivers: list, receivers of the email
    Returns:
        result: str, result of the message
    '''

    the_email = MIMEText(message, 'plain', 'utf-8')
    the_email['Subject'] = message_title
    the_email['From'] = sender
    the_email['To'] = receivers[0]

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, the_email.as_string())
    smtpObj.quit()
