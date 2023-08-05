# -*- coding: utf-8 -*-

""" Unit test for pyKwalify - extensions """

# python std lib
import os

# pykwalify imports
import pykwalify


class TestExtensions(object):

    def setUp(self):
        pykwalify.partial_schemas = {}

    def f(self, *args):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "files", "extensions", *args)

    def test_(self, tmpdir):
        """
        """
        pass
