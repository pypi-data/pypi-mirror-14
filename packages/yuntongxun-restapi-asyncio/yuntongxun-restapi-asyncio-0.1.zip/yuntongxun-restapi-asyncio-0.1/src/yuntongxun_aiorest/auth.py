# -*- encoding: utf-8 -*-

from hashlib import md5
from base64 import b64encode
from datetime import datetime


def build_auth(sid, token):
    """帐号鉴权

    * `URL` 后必须带有 `sig` 参数，例如： ``sig=AAABBBCCCDDDEEEFFFGGG`` 。
    * 使用 MD5 加密（主帐号Id + 主帐号授权令牌 +时间戳）。其中主帐号Id和主帐号授权令牌分别对应管理控制台中的 `ACCOUNT` `SID` 和 `AUTH TOKEN` 。
    * 时间戳是当前系统时间，格式 `yyyyMMddHHmmss` 。时间戳有效时间为24小时，如： `20140416142030`
    * `SigParameter` 参数需要大写

    :param str sid: 账户的 SID
    :param str token: 账户的 Token
    :rtype: Tuple[str, str, str]
    :return: 帐号鉴权字符串，签名字符串，时间戳字符串
    """
    ts = '{:%Y%m%d%H%M%S}'.format(datetime.now())
    sig = md5(
        '{}{}{}'.format(sid, token, ts).encode()
    ).hexdigest().upper()
    auth = b64encode('{}:{}'.format(sid, ts).encode()).decode()
    return auth, sig, ts
