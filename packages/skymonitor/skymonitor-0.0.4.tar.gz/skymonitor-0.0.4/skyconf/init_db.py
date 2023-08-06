# coding: utf-8


# 发邮件
from public.mail_server import SendCloud
from skyconf import (SEND_CLOUD_CONFIG, SYS_EMAIL_SENDER, SYS_EMAIL_SENDER_NAME,
    INTERNAL_EMAIL_SENDER, INTERNAL_SEND_CLOUD_CONFIG)

mail_server = SendCloud(
    default_from_name=SYS_EMAIL_SENDER_NAME,
    default_from_mail=SYS_EMAIL_SENDER,
    **SEND_CLOUD_CONFIG
)

internal_mail_server = SendCloud(
    default_from_name=SYS_EMAIL_SENDER_NAME,
    default_from_mail=INTERNAL_EMAIL_SENDER,
    **INTERNAL_SEND_CLOUD_CONFIG
)

# 短信
from public.sms import SMS
from skyconf import (SMSCENTER_HOST, SMSCENTER_PUBLIC_KEY, SMSCENTER_SECRET_KEY)
sms = SMS(SMSCENTER_HOST, SMSCENTER_PUBLIC_KEY, SMSCENTER_SECRET_KEY)
