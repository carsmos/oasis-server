import datetime
import os
from email.mime.text import MIMEText
from typing import Any

from fastapi import APIRouter, Depends, status, HTTPException, Request, Body

from utils.auth import request
import smtplib

router = APIRouter()


@router.post(
    "/send_email_login",
    summary='发送邮件',
    tags=["Email"]
)
def send_email(content: dict = Body(...)):
    return send_mail(content, '')


@router.post(
    "/send_email_logout",
    summary='发送邮件',
    tags=["Email"]
)
def send_email(content: Any = Body(...)):
    return send_mail(content)


def send_mail(content, user_email: str = "",
              to_addrs_list=["service@synkrotron.ai"],
              msg_subject="Oasis Platform 用户反馈", msg_type="html"):
    smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
    if os.environ.get('SUGGEST_EMAIL_EMAIL'):
        username = os.environ.get('SUGGEST_EMAIL_EMAIL')
    else:
        username = "XXX@guardstrike.com"
    if os.environ.get('SUGGEST_EMAIL_EMAIL_PASSWORD'):
        password = os.environ.get('SUGGEST_EMAIL_EMAIL_PASSWORD')
    else:
        password = "XXXXXXXXX"

    from_addr = username
    email_content = content['content']
    email_content = "<h4>用户名: %s </h4>" % user_email + email_content

    msg = MIMEText(email_content, msg_type, "utf-8")
    msg['Subject'] = msg_subject + " " + datetime.datetime.now().strftime('%Y/%m/%d')
    msg['From'] = from_addr
    msg["To"] = ";".join(to_addrs_list)
    try:
        smtp.login(username, password)
        smtp.sendmail(from_addr, to_addrs_list, msg=msg.as_string())
        smtp.quit()
        return "send email successful"
    except Exception as e:
        assert False, 'send email failure by %s' % e