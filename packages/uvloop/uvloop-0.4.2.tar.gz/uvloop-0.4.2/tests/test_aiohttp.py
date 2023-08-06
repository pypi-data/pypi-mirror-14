import asyncio
import socket
import uvloop
import unittest

from uvloop import _testbase as tb

try:
    import aiohttp
except ImportError:
    raise unittest.SkipTest('no aiohttp')

class _TestHttp:
    def test_create_server_1(self):
        print(1)


class Test_UV_HTTP(_TestHttp, tb.UVTestCase):
    pass


class Test_AIO_HTTP(_TestHttp, tb.AIOTestCase):
    pass
