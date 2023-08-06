# -*- encoding: utf-8 -*-

"""REST API

参考: http://docs.yuntongxun.com/index.php/Rest%E4%BB%8B%E7%BB%8D
"""

import json
from io import BytesIO, StringIO
from http import HTTPStatus
import xml.etree.ElementTree as ETree

import aiohttp

from .attrdict import AttrDict
from .auth import build_auth
from .error import raise_if_error, HttpError


async def invoke(base_url, auth_type, account_sid, auth_token, func, func_des, params=None, headers=None, data=None,
                 timeout=15):
    """进行一次 REST 调用

    :param str base_url: 所有被引用的地址都有如下 Base URL：

        * 沙盒地址，用于应用上线前进行业务测试： `https://sandboxapp.cloopen.com:8883/2013-12-26`
        * 生产地址，用于应用上线后进行正式业务： `https://app.cloopen.com:8883/2013-12-26`

        .. attention:: 为了确保数据隐私，云通讯平台的REST API是通过HTTPS方式请求。

    :param str auth_type: 验证级别， **必选** 有：

        * `Accounts` : 主帐号鉴权，云通讯平台会对请求中的主帐号和主帐号Token进行验证
        * `SubAccounts` : 子帐号鉴权，云通讯平台会对请求中的子帐号和子帐号Token进行验证

    :param str account_sid: 主账户或者子账户Id。由32个英文字母和阿拉伯数字组成的主账户唯一标识符 **必选**

    :param str auth_token: 账户 `TOKEN` **必选**

    :param str func: 描述业务功能，**必选** 。对于 `IVR API` 这参数必须是 `ivr`

    :param str func_des: 描述业务功能的具体操作  **必选**

    :param dict params: URL 参数

    :param dict headers: HTTP 请求头域键值对

    :param data: POST 请求数据，它的数据类型可以是：

        * :data:`None`: 将是一个 `GET` 请求
        * :class:`dict`: 采用 `JSON` 格式的调用
        * :class:`xml.etree.ElementTree.ElementTree`: 采用 `XML` 格式的调用

    :param int timeout: HTTP 超时（秒）

    :rtype: AttrDict
    :return: RestAPI 返回结果。XML结果中的标签被转化为了属性名，文本被转化为了属性值
    """

    params = params or {}
    headers = headers or {}
    if auth_type not in ('Accounts', 'SubAccounts'):
        raise ValueError('未知的验证级别 "%s"' % auth_type)
    auth, sig, ts = build_auth(account_sid, auth_token)
    url = '{baseURL}/{authType}/{account}/{func}/{funcdes}'.format(
        baseURL=base_url,
        authType=auth_type,
        account=account_sid,
        func=func,
        funcdes=func_des,
    )
    params['sig'] = sig
    headers['Authorization'] = auth
    if data is None:
        headers['Accept'] = 'application/json'
    elif isinstance(data, ETree.ElementTree):
        headers['Accept'] = 'application/xml'
        headers['Content-Type'] = 'application/xml;charset=utf-8'
        fs = BytesIO()
        try:
            data.write(fs, encoding='utf-8', xml_declaration=True)
            data = fs.getvalue()
        finally:
            fs.close()
    elif isinstance(data, dict):
        headers['Accept'] = 'application/json'
    resp_txt = ''
    with aiohttp.ClientSession() as session:
        with aiohttp.Timeout(timeout):
            method = session.get if data is None else session.post
            async with method(url, headers=headers, params=params, data=data) as resp:
                if not resp.status == HTTPStatus.OK:
                    try:
                        reason = HTTPStatus(resp.status).phrase
                    except ValueError:
                        reason = ''
                    raise HttpError(status=resp.status, reason=reason)
                resp_txt = await resp.text()
    if headers['Accept'] == 'application/json':
        res = json.loads(resp_txt)
        raise_if_error(res)
    elif headers['Accept'] == 'application/xml':
        fs = StringIO(resp_txt)
        try:
            tree = ETree.parse(fs)
        finally:
            fs.close()
        raise_if_error(tree)
        res = recursive_resp_xml_node(tree.getroot())[1]
    else:
        raise RuntimeError('Accept Header error')
    return AttrDict(res)


def recursive_resp_xml_node(node):
    tag = node.tag
    text = node.text.strip()
    if text:
        return tag, text
    else:
        d = {}
        for child in node:
            k, v = recursive_resp_xml_node(child)
            v0 = d.get(child.tag)
            if v0:
                if isinstance(v0, list):
                    v0.append(v)
                else:
                    d[child.tag] = [v0, v]
            else:
                d[k] = v
        return tag, d
