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


class ParseUnobserveReplyTestCase(unittest.TestCase):
    def test_unobserve_correct(self):
        info = parse_unobserve_reply(
            "Removing game 124 from observation list.")
        self.failUnlessEqual(info, GameReference(game_no=124))
    def test_unobserve_logic_fail(self):
        for text in [
            "You are not observing game 13.",
            "You are not observing any games.",
            ]:
            self.failUnlessRaises(errors.AttemptToActOnNotUsedGame,
                parse_unobserve_reply, text)
    def test_unobserve_bad_syntax(self):
        for text in [
            "",
            "blah blah",
            "Removing game KROKODYL from observation list.",
            ]:
            self.failUnlessRaises(errors.ReplyParsingException,
                parse_unobserve_reply, text)


class ParseObserveReplyTestCase(unittest.TestCase):
    def test_private(self):
        self.failUnlessRaises(
            errors.AttemptToAccessPrivateGame,
            parse_observe_reply,
            "Sorry, game 125 is a private game")
    def test_already_observed(self):
        self.failUnlessRaises(
            errors.GameAlreadyObserved,
            parse_observe_reply,
            "You are already observing game 77."
        )
    def test_limit(self):
        self.failUnlessRaises(
            errors.LimitExceeded,
            parse_observe_reply,
            "You are already observing the maximum number of games")
    def test_rubbish(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_observe_reply,
            "Blah blah")
    def testNormal(self):
        d = parse_observe_reply( load_tstdata_file( 'ficsparserdata', 'observe-normal.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 92)
        self.failUnlessEqual(d.white_name, PlayerName('Motyl'))
        self.failUnlessEqual(d.white_rating_value, 1857)
        self.failUnlessEqual(d.black_name, PlayerName('Aretus'))
        self.failUnlessEqual(d.black_rating_value, 1907)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15,10))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (0:00) none 0 0 0")
    def testProblematic(self):
        d = parse_observe_reply( load_tstdata_file( 'ficsparserdata', 'observe-spec-norating.lines')  )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 161)
        self.failUnlessEqual(d.white_name, PlayerName('ilmagicoalverman'))
        self.failUnlessEqual(d.white_rating_value, 1582)
        self.failUnlessEqual(d.black_name, PlayerName('bibibibi'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15, 0))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 161 ilmagicoalverman bibibibi 0 15 0 39 39 900 900 1 none (0:00) none 0 0 0")

    def testProblematic2(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-spec-shortrating.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 222)
        self.failUnlessEqual(d.white_name, PlayerName('Johnnyp'))
        self.failUnlessEqual(d.white_rating_value, 923)
        self.failUnlessEqual(d.black_name, PlayerName('schakeric'))
        self.failUnlessEqual(d.black_rating_value, 1321)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20,0))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 222 Johnnyp schakeric 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")

    def testProblematic3(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-spec-shortrating-white.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 221)
        self.failUnlessEqual(d.white_name, PlayerName('GuestMGVG'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_name, PlayerName('Mekk'))
        self.failUnlessEqual(d.black_rating_value, 1371)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,5))

    def testWild4(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-wild4.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 226)
        self.failUnlessEqual(d.white_name, PlayerName('Raph'))
        self.failUnlessEqual(d.white_rating_value, 1827)
        self.failUnlessEqual(d.black_name, PlayerName('andycappablanca'))
        self.failUnlessEqual(d.black_rating_value, 1878)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/4'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3,0))
