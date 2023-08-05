# coding: utf8

import unittest

from toyyaml.toyyaml import pair_data, loads, multi_string_data


class TestYaml(unittest.TestCase):
    def test_get_pair_with_simple_dict(self):
        pair, string = pair_data("aaa: bbb")
        self.assertEquals(pair, ("aaa", "bbb"))
        self.assertEquals(string, "")

    def test_success_split_key_and_value_when_key_and_value_has_quote(self):
        pair, string = pair_data("aa:a: bb:b")
        self.assertEquals(pair, ("aa:a", "bb:b"))
        self.assertEquals(string, "")

    def test_get_pair_and_popup_string(self):
        pair, string = pair_data("aaa: bbb\nasdasd")
        self.assertEquals(pair, ("aaa", "bbb"))
        self.assertEquals(string, "asdasd")

    def test_get_multi_line_string_pair_value(self):
        pair, string = pair_data("""aaa: |
        asdasd
        bbbbb
        """)
        self.assertEquals(pair, ("aaa", "asdasd\nbbbbb"))
        self.assertEquals(string, "")

    def test_get_pair_with_value_is_list(self):
        pair, string = pair_data("aaa: [bb, cc, dd]")

        self.assertEquals(pair, ("aaa", ["bb", "cc", "dd"]))
        self.assertEquals(string, "")

    def test_get_pair_with_value_is_dict(self):
        pair, string = pair_data("""aaa:
            bb: cc
            dd: ee
        """)

        self.assertEquals(pair, ("aaa", dict(bb="cc", dd="ee")))
        self.assertEquals(string, "        ")

    def test_get_pair_with_value_is_yaml_list(self):
        pair, string = pair_data("""aaa:
            - bbcc
            - ddee
        """)

        self.assertEquals(pair, ("aaa", ["bbcc", "ddee"]))
        self.assertEquals(string, "        ")

    def test_load_list_datas(self):
        result = loads("""
        - aaa

        - bbb
        """)
        self.assertEquals(len(result), 2)
        self.assertEquals(result, ["aaa", "bbb"])

    def test_success_get_multi_line_string_value_when_with_empty_line(self):
        result, tail = multi_string_data("""
            asd
            aaa

            bbb
        - t
        """)
        self.assertEquals(result, "\nasd\naaa\n\nbbb")
        self.assertEquals(tail, "        - t\n        ")

    def test_load_read_data(self):
        result = loads("""
        project_name: mothership-admin

        tasks:
          asd-supasdponv:
            runner: buiasld_image
            workspace: troasds//webaasd/
            dockerfile: xxx/vvv.asd
            sasduasdffix: aasd

          asd-asd-asd:
            runner: asd
            workspace: tros/src/main/webapp/
            asdbb: asdasd/asdasdaf/asdasd.afasdasd
            asd: asdas

          123:
            asd: 12324
            aaa: asd/asd.asd
            ppp: asd

          unittest:
            - aaa
            - bb

          asdasd:
            asd: asd
            dockerfile: 22/33.release
            asdga: 111
            tag: dev
        """)
        self.assertEquals(len(result), 2)
        self.assertEquals(len(result["tasks"]), 5)
