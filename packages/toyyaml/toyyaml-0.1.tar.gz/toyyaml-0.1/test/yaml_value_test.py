# coding: utf8

import unittest

from toyyaml.yaml_value import get_enum, get_value


class TestYamlValue(unittest.TestCase):
    def test_get_simple_enum(self):
        enum, string = get_enum("aaa", ",")
        self.assertEquals(enum, "aaa")
        self.assertEquals(string, "")

    def test_get_enum_split_by_comma(self):
        enum, string = get_enum("aaa, aaa", ",")
        self.assertEquals(enum, "aaa")
        self.assertEquals(string, " aaa")

    def test_get_int_value(self):
        enum = get_value("  23 ")
        self.assertEquals(enum, 23)

    def test_get_float_value(self):
        enum = get_value("  23.0 ")
        self.assertEquals(enum, 23.0)