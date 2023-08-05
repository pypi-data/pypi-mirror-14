
"""this module is defined to detect the requests module
"""

import logging
from tingyun.armoury.ammunition.external_tracker import wrap_external_trace, process_cross_trace

console = logging.getLogger(__name__)


def detect_requests_request(module):
    """
    :param module:
    :return:
    """
    def request_url(method, url, *args, **kwargs):
        """
        """
        return url

    wrap_external_trace(module, 'request', 'requests', request_url)


def detect_requests_sessions(module):
    """
    :param module:
    :return:
    """
    def request_url(instance, method, url, *args, **kwargs):
        """
        """
        return url

    def parse_params(method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                     timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                     json=None):
        _args = (method, url)
        _kwargs = {"params": params, "data": data, "headers": process_cross_trace(headers), "cookies": cookies,
                   "files": files, "auth": auth, "timeout": timeout, "allow_redirects": allow_redirects,
                   "proxies": proxies, "hooks": hooks, "stream": stream, "verify": verify, "cert": cert, "json": json}

        return _args, _kwargs

    wrap_external_trace(module, 'Session.request', 'requests', request_url, params=parse_params)

