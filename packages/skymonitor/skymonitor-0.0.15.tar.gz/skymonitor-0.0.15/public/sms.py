# coding: utf-8
import requests
import hashlib
from operator import itemgetter


class SMSSendFailed(Exception):

    def __init__(self, http_status_code, err_code, err_msg):
        self.http_status_code = http_status_code
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):
        return u'http_status_code: %s, err_code: %s, err_msg: %s' % (self.http_status_code, self.err_code,
                                                                     self.err_msg)


class SMSSendVerificationFailed(SMSSendFailed):
    pass


class SMSVerifyFailed(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return u'code: %s, message: %s' % (self.code, self.message)


def _is_valid_phone_number(country_code, phone_number):
    if country_code == '86' and len(phone_number) != 11:
        return False
    elif country_code == '1' and len(phone_number) != 10:
        return False
    return True


class SMS(object):

    def __init__(self, host, public_key, secret_key, timeout=5):
        self.host = host
        self.public_key = public_key
        self.secret_key = secret_key

        self.send_plain_text_url = '%s/api/v1/message/send.json' % self.host
        self.send_verification_code_url = '%s/api/v1/verification/send.json' % self.host
        self.verify_verification_code_url = '%s/api/v1/verification/verify.json' % self.host
        self._session = None
        self.timeout = timeout

    @property
    def session(self):
        if not self._session:
            self._session = requests.session()
        return self._session

    def post(self, *args, **kwargs):
        return self.session.post(*args, timeout=self.timeout, **kwargs)

    def get(self, *args, **kwargs):
        return self.session.get(*args, timeout=self.timeout, **kwargs)

    def sign(self, d):
        md5_str = ''
        for key, value in sorted(d.items(), key=itemgetter(0)):
            if isinstance(value, unicode):
                value = value.encode('utf8')
            if isinstance(value, str):
                md5_str += "%s%s" % (key, value)
        md5_str += str(self.secret_key)
        sign = hashlib.md5(md5_str).hexdigest()
        return sign

    def send_plain_text(self, country_code, phone_number, text):
        if not _is_valid_phone_number(country_code, phone_number):
            raise SMSSendFailed(200, 0, '手机号无效')

        url = self.send_plain_text_url
        data = {'country_code': country_code, 'phone_number': phone_number,
                'text': text, 'public_key': self.public_key}
        data['signature'] = self.sign(data)

        try:
            resp = self.post(url, data=data)
        except IOError:
            raise SMSSendFailed(200, 0, '请求超时请重试')

        if resp.ok:
            return True

        err_code, err_msg = '', ''
        if resp.status_code == requests.codes.bad_request:
            ret = resp.json()
            err_code, err_msg = ret['code'], ret['msg']

        raise SMSSendFailed(resp.status_code, err_code, err_msg)

    def send_verification_code(self, country_code, phone_number):
        if not _is_valid_phone_number(country_code, phone_number):
            raise SMSSendVerificationFailed(200, 0, '手机号无效')

        url = self.send_verification_code_url
        data = {'country_code': country_code, 'phone_number': phone_number,
                'public_key': self.public_key}
        data['signature'] = self.sign(data)

        # try:
        #     resp = self.post(url, data=data)
        # except IOError:
        #     raise SMSSendVerificationFailed(200, 0, '请求超时请重试')

        # 由于缺少监控和报警设施 暂时不处理网络错误 不然难以及时发现问题
        resp = self.post(url, data=data)

        if resp.ok:
            ret = resp.json()
            return ret['content']

        err_code, err_msg = '', ''
        if resp.status_code == requests.codes.bad_request:
            ret = resp.json()
            err_code, err_msg = ret['code'], ret['msg']

        raise SMSSendVerificationFailed(resp.status_code, err_code, err_msg)

    def verify_verification_code(self, country_code, phone_number, code):
        url = self.verify_verification_code_url
        data = {'country_code': country_code, 'phone_number': phone_number,
                'code': code, 'public_key': self.public_key}
        data['signature'] = self.sign(data)

        resp = self.post(url, data=data)

        if resp.ok:
            return True

        ret = resp.json()
        err_code, err_msg = ret['code'], ret['msg']

        raise SMSVerifyFailed(err_code, err_msg)
