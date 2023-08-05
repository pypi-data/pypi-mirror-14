# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.constants import block_codes

import re
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.generic import GenericText
from mekk.fics.datatypes.color import Color, BLACK, WHITE
from mekk.fics.datatypes.date import FicsDateInfo
from mekk.fics.datatypes.game_clock import GameClock
from mekk.fics.datatypes.game_info import GameReference, ExaminedGame, SetupGame, PlayedGame, GameSpec, GameInfo, ExaminedGameExt
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.list_items import ListContents
from mekk.fics.datatypes.notifications import SeekRef, GameJoinInfo, Seek
from mekk.fics.datatypes.player import PlayerName, FingerInfo, ResultStats, PlayerRating
from mekk.fics.datatypes.channel import ChannelRef
from mekk.fics.parsing import info_parser
from mekk.fics.parsing.reply.block_mode_filter import BlockModeFilter
from mekk.fics.parsing.reply.finger import parse_finger_reply
from mekk.fics.parsing.reply.games import parse_games_reply_line
from mekk.fics.parsing.reply.who import parse_who_reply
from mekk.fics.parsing.reply.list_operations import parse_showlist_reply
from mekk.fics.parsing.reply.observe import parse_observe_reply, parse_unobserve_reply
from mekk.fics.parsing.reply_parser import parse_fics_reply
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal, SkipTest
from mekk.fics.test_utils.internal import (
    load_parse_data_file, load_parse_data_file_patching_continuations)
from mekk.fics import errors
import datetime
from decimal import Decimal



class ParseGamesLineTestCase(unittest.TestCase):

    def testEx1(self):
        (w,d) = parse_games_reply_line('2 (Exam.    0 LectureBot     0 LectureBot) [ uu  0   0] W:  1')
        self.failUnlessEqual(w, 'Examine')
        self.failUnlessEqual(d.game_no, 2)

    def testEx2(self):
        (w,d) = parse_games_reply_line('8 (Exam. 1830 Myopic      1890 BULLA     ) [ br  3   0] W:  1')
        self.failUnlessEqual(w, 'Examine')
        self.failUnlessEqual(d.game_no, 8)

    def testG1(self):
        (w,d) = parse_games_reply_line('4 ++++ yetis       ++++ GuestWWJX  [ bu  5  12]   1:09 -  3:39 (28-26) W: 19')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('yetis'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestWWJX'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,12))

    def testG2(self):
        (w,d) = parse_games_reply_line('14 ++++ DeathValzer ++++ GuestMLSG  [ uu  0   0]   0:00 -  0:00 (34-11) B: 26')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 14)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('DeathValzer'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestMLSG'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('u'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('untimed'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(0,0))

    def testG3(self):
        (w,d) = parse_games_reply_line('51 ++++ SupraPhonic ++++ GuestTWMQ  [ Su  3   0]   2:59 -  2:52 (14-15) B:  4')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('SupraPhonic'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestTWMQ'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('S'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3, 0))

    def testG4(self):
        (w,d) = parse_games_reply_line('52 ++++ bozziofan   ++++ GuestBFRV  [ su 20   0]  13:33 - 15:41 ( 3-19) W: 39')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('bozziofan'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestBFRV'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20, 0))

    def testG5(self):
        (w,d) = parse_games_reply_line('53 ++++ Wampum      1172 nurp       [ bu  5   0]   4:02 -  3:39 (37-34) B: 15')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 53)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('Wampum'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('nurp'))
        self.failUnlessEqual(d.black_rating_value, 1172)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5, 0))

    def testG6(self):
        (w,d) = parse_games_reply_line('36 1447 zzzzzztrain ++++ GuestBVXT  [ bu  2  12]   1:36 -  2:25 (35-36) W: 10')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 36)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('zzzzzztrain'))
        self.failUnlessEqual(d.white_rating_value, 1447)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestBVXT'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2, 12))

    def testG7(self):
        (w,d) = parse_games_reply_line('71  832 paratoner    912 stshot     [ br 10   0]   5:47 -  7:28 (14-22) W: 20')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 71)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('paratoner'))
        self.failUnlessEqual(d.white_rating_value,  832)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('stshot'))
        self.failUnlessEqual(d.black_rating_value, 912)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(10, 0))

    def testG8(self):
        (w,d) = parse_games_reply_line('83 1013 origamikid   841 drmksingh  [ br  3   5]   0:23 -  0:44 (27-33) W: 25')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 83)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('origamikid'))
        self.failUnlessEqual(d.white_rating_value, 1013)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('drmksingh'))
        self.failUnlessEqual(d.black_rating_value, 841)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3, 5))

    def testG9(self):
        (w,d) = parse_games_reply_line('44  913 Veeber      1013 LorenzoDV  [pbr 12   0]   5:13 -  3:01 (17-25) W: 31')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 44)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('Veeber'))
        self.failUnlessEqual(d.white_rating_value,  913)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('LorenzoDV'))
        self.failUnlessEqual(d.black_rating_value, 1013)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(12, 0))

    def testG10(self):
        (w,d) = parse_games_reply_line('34 1118 JaronGroffe  868 sklenar    [ br 10   0]   4:41 -  6:41 (14-11) W: 29')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 34)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('JaronGroffe'))
        self.failUnlessEqual(d.white_rating_value, 1118)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('sklenar'))
        self.failUnlessEqual(d.black_rating_value, 868)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(10, 0))

    def testG11(self):
        (w,d) = parse_games_reply_line('85 1254 rugs         823 MjollnirPa [ br  5   3]   1:37 -  0:35 (29-20) W: 30')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 85)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('rugs'))
        self.failUnlessEqual(d.white_rating_value, 1254)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('MjollnirPa'))
        self.failUnlessEqual(d.black_rating_value, 823)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5, 3))

    def testG12(self):
        (w,d) = parse_games_reply_line('1 1700 yacc        1542 dontrookba [psr 20  20]  28:42 - 23:38 (17-19) B: 32')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('yacc'))
        self.failUnlessEqual(d.white_rating_value, 1700)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('dontrookba'))
        self.failUnlessEqual(d.black_rating_value, 1542)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20, 20))

    def testG13(self):
        (w,d) = parse_games_reply_line('42 1608 monteleo    2545 Topolino   [ sr 15   2]  14:34 - 13:48 (38-35) B:  8')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 42)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('monteleo'))
        self.failUnlessEqual(d.white_rating_value, 1608)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('Topolino'))
        self.failUnlessEqual(d.black_rating_value, 2545)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15, 2))

    def testG14(self):
        (w,d) = parse_games_reply_line('67 1095 PlatinumKni 1735 LiquidEmpt [pbr  2  12]   3:34 -  2:07 (21-24) W: 34')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 67)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('PlatinumKni'))
        self.failUnlessEqual(d.white_rating_value, 1095)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('LiquidEmpt'))
        self.failUnlessEqual(d.black_rating_value, 1735)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2, 12))

    def testG15(self):
        (w,d) = parse_games_reply_line('204 1534 NoSpeedChes 1513 EvilSchmoo [ sr165   0] 2:14:11 -2:37:11 (33-31) B: 21')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 204)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('NoSpeedChes'))
        self.failUnlessEqual(d.white_rating_value, 1534)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('EvilSchmoo'))
        self.failUnlessEqual(d.black_rating_value, 1513)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(165, 0))

    def testGSetup(self):
        (w,d) = parse_games_reply_line('112 (Setup 1129 Yunoguthi   1129 Yunoguthi ) [ uu  0   0] W:  1')
        self.failUnlessEqual(w, 'Setup')

    def testGSetup2(self):
        (w,d) = parse_games_reply_line('   2 (Setup    0 LectureBot     0 LectureBot) [ uu  0   0] B:  1')
        self.failUnlessEqual(w, 'Setup')
