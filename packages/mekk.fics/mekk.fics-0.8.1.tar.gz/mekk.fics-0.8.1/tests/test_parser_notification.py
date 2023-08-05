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


class NotificationTestCase(unittest.TestCase):

    def test_arrival(self):
        w, d = info_parser.parse_fics_line(
            'Notification: Mekk has arrived.')
        self.failUnlessEqual(w, 'watched_user_connected')
        self.failUnlessEqual(d, PlayerName('Mekk'))

    def test_departure(self):
        w, d = info_parser.parse_fics_line(
            'Notification: Mekk has departed.')
        self.failUnlessEqual(w, 'watched_user_disconnected')
        self.failUnlessEqual(d, PlayerName('Mekk'))

    def test_arrival_nt(self):
        w, d = info_parser.parse_fics_line(
            'Notification: FiNLiP has arrived and isn\'t on your notify list.')
        self.failUnlessEqual(w, 'watching_user_connected')
        self.failUnlessEqual(d, PlayerName('FiNLiP'))

    def test_departure_nt(self):
        w, d = info_parser.parse_fics_line(
            'Notification: FiNLiP has departed and isn\'t on your notify list.')
        self.failUnlessEqual(w, 'watching_user_disconnected')
        self.failUnlessEqual(d, PlayerName('FiNLiP'))

    def test_auto_logout(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            '''**** Auto-logout because you were idle more than 60 minutes. ****''')

    def test_gnotify_game_notification(self):
        w, d = info_parser.parse_fics_line(
            '''Game notification: Mlasker (1709) vs. emranhamid (1791) rated standard 15 0: Game 262''')
        self.failUnlessEqual(w, 'game_started_ext')
        self.failUnlessEqual(d.white_name, PlayerName('Mlasker'))
        self.failUnlessEqual(d.white_rating, 1709)
        self.failUnlessEqual(d.black_name, PlayerName('emranhamid'))
        self.failUnlessEqual(d.black_rating, 1791)
        self.failUnlessEqual(d.game_no, 262)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))

        w, d = info_parser.parse_fics_line(
            '''Game notification: Cdorf (1861) vs. alextheseaman (1956) rated standard 15 5: Game 257''')
        self.failUnlessEqual(w, 'game_started_ext')
        self.failUnlessEqual(d.white_name, PlayerName('Cdorf'))
        self.failUnlessEqual(d.white_rating, 1861)
        self.failUnlessEqual(d.black_name, PlayerName('alextheseaman'))
        self.failUnlessEqual(d.black_rating, 1956)
        self.failUnlessEqual(d.game_no, 257)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
