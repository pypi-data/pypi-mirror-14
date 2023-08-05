
from twisted.trial import unittest

from mekk.fics.constants import block_codes
from mekk.fics.parsing.reply_parser import parse_fics_reply
from mekk.fics.datatypes import ZnotifyInfo, IdleInfo, PlayerName
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal
from mekk.fics.test_utils.internal import load_parse_data_file_patching_continuations

class ZnotifyTestCase(unittest.TestCase):

    def test_znotify_1(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_ZNOTIFY,
            load_parse_data_file_patching_continuations("znotify-1.lines"))
        self.failUnless(status, "znotify parsing failed")
        self.failUnlessEqual(cmd, "znotify")
        assert_dicts_equal(self, info, ZnotifyInfo(
            tracked=[
                IdleInfo(name=PlayerName('BrianJB'), idle=38 * 60),
                IdleInfo(name=PlayerName('herrahuu'), idle=3 * 60),
            ],
            tracking=[],
        ))

    def test_znotify_2(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_ZNOTIFY,
            load_parse_data_file_patching_continuations("znotify-2.lines"))
        self.failUnless(status, "znotify parsing failed")
        self.failUnlessEqual(cmd, "znotify")
        assert_dicts_equal(self, info, ZnotifyInfo(
            tracked=[
                IdleInfo(name=PlayerName('JoshuaR'), idle=26*60),
                IdleInfo(name=PlayerName('MAd'), idle=0),
                IdleInfo(name=PlayerName('NiallAdams'), idle=600),
                IdleInfo(name=PlayerName('TScheduleBot'), idle=180),
                IdleInfo(name=PlayerName('WatchBot'), idle=0),
            ],
            tracking=[
                IdleInfo(name=PlayerName('GuestHHJR'), idle=0),
                IdleInfo(name=PlayerName('GuestQLMB'), idle=0),
                IdleInfo(name=PlayerName('GuestXJLH'), idle=0),
                IdleInfo(name=PlayerName('GuestXLPB'), idle=0),
                IdleInfo(name=PlayerName('GuestYVBQ'), idle=0),
                IdleInfo(name=PlayerName('WatchBot'), idle=0),
               ],
        ))

    def test_znotify_3(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_ZNOTIFY,
            load_parse_data_file_patching_continuations("znotify-3.lines"))
        self.failUnless(status, "znotify parsing failed")
        self.failUnlessEqual(cmd, "znotify")
        assert_dicts_equal(self, info, ZnotifyInfo(
            tracked=[],
            tracking=[],
        ))

    def test_znotify_4(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_ZNOTIFY,
            load_parse_data_file_patching_continuations("znotify-2.lines"))
        self.failUnless(status, "znotify parsing failed")
        self.failUnlessEqual(cmd, "znotify")
        assert_dicts_equal(self, info, ZnotifyInfo(
            tracked=[
                IdleInfo(name=PlayerName('JoshuaR'), idle=26*60),
                IdleInfo(name=PlayerName('MAd'), idle=0),
                IdleInfo(name=PlayerName('NiallAdams'), idle=600),
                IdleInfo(name=PlayerName('TScheduleBot'), idle=180),
                IdleInfo(name=PlayerName('WatchBot'), idle=0),
            ],
            tracking=[
                IdleInfo(name=PlayerName('GuestHHJR'), idle=0),
                IdleInfo(name=PlayerName('GuestQLMB'), idle=0),
                IdleInfo(name=PlayerName('GuestXJLH'), idle=0),
                IdleInfo(name=PlayerName('GuestXLPB'), idle=0),
                IdleInfo(name=PlayerName('GuestYVBQ'), idle=0),
                IdleInfo(name=PlayerName('WatchBot'), idle=0),
               ],
        ))
