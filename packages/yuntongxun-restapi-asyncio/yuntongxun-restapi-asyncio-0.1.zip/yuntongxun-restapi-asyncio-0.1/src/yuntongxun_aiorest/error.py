# -*- encoding: utf-8 -*-

import xml.etree.ElementTree as ETree


class HttpError(Exception):
    """HTTP 错误"""

    def __init__(self, status, reason=''):
        super().__init__('HTTP Error [{}]: {}'.format(status, reason))
        self._status = int(status)
        self._reason = str(reason)

    @property
    def status(self):
        return self._status

    @property
    def reason(self):
        return self._reason


class RestApiError(Exception):
    """REST API 错误返回"""

    def __init__(self, code, message=''):
        super().__init__('Restful API Error [{}]: {}'.format(code, message))
        self._code = int(code)
        self._message = str(message)

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message


def raise_if_error(obj):
    """检查 REST API 返回的 XML 结果，如果有错，则抛出异常，否则不返回任何内容。

    :param xml.etree.ElementTree obj: XML 返回值
    :raise RestApiError: 如果 XML 结果表明调用中发生错误，抛出的这个类型的异常
    """
    if isinstance(obj, ETree.ElementTree):
        root = obj.getroot()
        code = int(root.find('./statusCode').text)
        ele_msg = root.find('./statusMsg')
        message = '' if ele_msg is None else ele_msg.text
    elif isinstance(obj, dict):
        code = int(obj['statusCode'])
        message = str(obj.get('statusMsg', ''))
    else:
        raise TypeError('Unknown object type')
    raise RestApiError(code, message)
