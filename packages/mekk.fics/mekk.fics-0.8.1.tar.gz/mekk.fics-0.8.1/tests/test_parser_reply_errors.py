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


#noinspection PyTypeChecker
class ParseReplyCheckErrorsTestCase(unittest.TestCase):
    def _ensure_raw_error(self, got_code, got_text, *expected_classes):
        """
        Woła polecenie, sprawdza czy poleciał wyjątek i czy jest to wyjątek
        jednej z zadanych klas.
        """
        cmd, status, info = parse_fics_reply(got_code, got_text)
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        for expected_class in expected_classes:
            self.failUnlessIsInstance(info, expected_class)
        return info
    def _ensure_error(self, got_code, got_text, *expected_classes):
        """
        Jak _ensure_raw_error ale dorzuca FicsCommandException do sprawdzanych
        wyjątków - tego oczekujemy prawie zawsze
        """
        info = self._ensure_raw_error(got_code, got_text, *expected_classes)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        return info
    def test_bad_handle(self):
        exc = self._ensure_error(48, "'%s' is not a valid handle.", errors.UnknownPlayer)
        self.failUnlessEqual(exc.player_name, "%s")
    def test_bad_handle_normal(self):
        exc = self._ensure_error(48, "There is no player matching the name qzqz.", errors.UnknownPlayer)
        self.failUnlessEqual(exc.player_name, "qzqz")
    def test_bad_command(self):
        self._ensure_error(512, "sk: Command not found.", errors.UnknownFicsCommand)
    def test_bad_seek(self):
        self._ensure_error(155, "No such board: krowa", errors.BadFicsCommandParameters)
    def test_bad_params(self):
        self._ensure_error(513, """Command:  news
Purpose:  list recent news items -OR- display details of a news item
Usage:    news [all|#[-#]]
Examples: news; news all; news 11; news 35-50""", errors.BadFicsCommandParameters)
    def test_ambiguous_command(self):
        self._ensure_error(514, 'Ambiguous command "su". Matches: sublist summon',
                           errors.AmbiguousFicsCommand, errors.UnknownFicsCommand)
    def test_assess_not_playing(self):
        self._ensure_error(15, 'You are not playing a game.', errors.AttemptToActOnNotPlayedGame)
    def test_guest_channel_tell(self):
        self._ensure_error(132, 'Only registered users may send tells to channels other than 4, 7 and 53.',
                           errors.InsufficientPermissions, errors.TrueAccountRequired)
    def test_noblock_marker(self):
        self._ensure_raw_error(519, '', errors.MissingBlockMarkers, errors.FicsProtocolError)
    def test_e2e4(self):
        self._ensure_error(518, 'You are not playing or examining a game.',
                           errors.AttemptToActOnNotPlayedGame)
    def test_wrong_params_addlist(self):
        self._ensure_error(513, """Command:  addlist
Purpose:  add information to a list
Usage:    addlist list information
Alt:      +list information
Examples: addlist noplay Friar; +noplay Friar 
""", errors.BadFicsCommandParameters)
    def test_very_long_message(self):
        # message veeerylongstring resulted in
        # fics% ^U0^V519^V^W
        # ^U100^V97^VLogging you out.
        self._ensure_error(520, "",
                           errors.FicsCommandException, errors.BadFicsCommandSyntax)
    def test_guest_message(self):
        raise SkipTest
        self._ensure_error(74, '''Only registered players can use the messages command.
''',
                           errors.TrueAccountRequired)
