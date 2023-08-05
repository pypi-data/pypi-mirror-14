from http.cookies import SimpleCookie
import base64
import os
import logging
import time
from saml2 import time_util
from saml2.httputil import NotFound

__author__ = 'roland'

logger = logging.getLogger(__name__)


def not_found(environ, start_response):
    """Called if no URL matches."""
    resp = NotFound()
    return resp(environ, start_response)


def staticfile(environ, start_response, args):
    try:
        path = args.path
        if path is None or len(path) == 0:
            path = os.path.dirname(os.path.abspath(__file__))
        if path[-1] != "/":
            path += "/"
        _path = environ.get('PATH_INFO', '').lstrip('/')
        while True:
            if _path.startswith("./"):
                _path = path[2:]
            elif _path.startswith("../"):
                _path = _path[3:]
            else:
                break

        path += _path
        start_response('200 OK', [('Content-Type', "text/xml")])
        return open(path, 'r').read()
    except Exception as ex:
        logger.error("An error occured while creating metadata:" + ex.message)
        return not_found(environ, start_response)


def expiration(timeout, tformat="%a, %d-%b-%Y %H:%M:%S GMT"):
    """

    :param timeout:
    :param tformat:
    :return:
    """
    if timeout == "now":
        return time_util.instant(tformat)
    elif timeout == "dawn":
        return time.strftime(tformat, time.gmtime(0))
    else:
        # validity time should match lifetime of assertions
        return time_util.in_a_while(minutes=timeout, format=tformat)


# ----------------------------------------------------------------------------
# Cookie handling
# ----------------------------------------------------------------------------


def delete_cookie(environ, name):
    kaka = environ.get("HTTP_COOKIE", '')
    logger.debug("delete KAKA: %s" % kaka)
    if kaka:
        cookie_obj = SimpleCookie(kaka)
        morsel = cookie_obj.get(name, None)
        cookie = SimpleCookie()
        cookie[name] = ""
        cookie[name]['path'] = "/"
        logger.debug("Expire: %s" % morsel)
        cookie[name]["expires"] = expiration("dawn")
        return tuple(cookie.output().split(": ", 1))
    return None


def set_cookie(name, _, *args):
    cookie = SimpleCookie()
    cookie[name] = base64.b64encode(":".join(args))
    cookie[name]['path'] = "/"
    cookie[name]["expires"] = expiration(5)  # 5 minutes from now
    logger.debug("Cookie expires: %s" % cookie[name]["expires"])
    return tuple(cookie.output().split(": ", 1))

