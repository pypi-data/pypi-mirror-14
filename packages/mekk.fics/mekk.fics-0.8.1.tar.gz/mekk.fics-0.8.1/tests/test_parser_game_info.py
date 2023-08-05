# -*- coding: utf-8 -*-

import datetime
from twisted.trial import unittest
from mekk.fics.constants import block_codes
from mekk.fics.parsing.reply_parser import parse_fics_reply
from mekk.fics import errors
from mekk.fics.datatypes.game_info import GameReference, ExaminedGame, SetupGame, PlayedGame, GameSpec, GameInfo, ExaminedGameExt
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal, SkipTest
from mekk.fics.datatypes.player import PlayerName, FingerInfo, ResultStats, PlayerRating
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.game_clock import GameClock


class GameInfoTestCase(unittest.TestCase):

    def test_simple(self):
        text = """Game 295: Game information.
  anandkvs (2063) vs donnadistruttiva (1960) rated Standard game.
  Time controls: 5400 30
  Time of starting: Sat Sep 15, 23:34 PDT 2012
  White time 1:25:27    Black time 1:23:58
  The clock is not paused
  16 halfmoves have been made.
  Fifty move count started at halfmove 13 (97 halfmoves until a draw).
  White may castle both kingside and queenside.
  Black may castle both kingside and queenside.
  Double pawn push didn't occur.
"""
        cmd, status, info = parse_fics_reply(
            46, text)
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, GameInfo)
        self.failUnlessIsInstance(info.game_no, int)
        self.failUnlessIsInstance(info.white_name, PlayerName)
        self.failUnlessIsInstance(info.black_name, PlayerName)
        self.failUnlessIsInstance(info.white_rating_value, int)
        self.failUnlessIsInstance(info.black_rating_value, int)
        self.failUnlessIsInstance(info.game_spec, GameSpec)
        self.failUnlessIsInstance(info.game_spec.is_private, bool)
        self.failUnlessIsInstance(info.game_spec.is_rated, bool)
        self.failUnlessIsInstance(info.game_spec.game_type, GameType)
        self.failUnlessIsInstance(info.game_spec.clock, GameClock)
        self.failUnlessEqual(info.game_no, 295)
        self.failUnlessEqual(info.white_name, 'anandkvs')
        self.failUnlessEqual(info.black_name, 'donnadistruttiva')
        self.failUnlessEqual(info.white_rating_value, 2063)
        self.failUnlessEqual(info.black_rating_value, 1960)
        self.failUnlessEqual(info.game_spec.is_private, False)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock, GameClock(90,30))
        self.failUnlessEqual(info.start_time, datetime.datetime(2012, 9, 15, 23, 34, 0))

    def test_simple_eurcst(self):
        text = """Game 295: Game information.
  anandkvs (2063) vs donnadistruttiva (1960) rated Standard game.
  Time controls: 5400 30
  Time of starting: Sat Sep 15, 23:34 EURCST 2012
  White time 1:25:27    Black time 1:23:58
  The clock is not paused
  16 halfmoves have been made.
  Fifty move count started at halfmove 13 (97 halfmoves until a draw).
  White may castle both kingside and queenside.
  Black may castle both kingside and queenside.
  Double pawn push didn't occur.
"""
        cmd, status, info = parse_fics_reply(
            46, text)
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, GameInfo)
        self.failUnlessIsInstance(info.game_no, int)
        self.failUnlessIsInstance(info.white_name, PlayerName)
        self.failUnlessIsInstance(info.black_name, PlayerName)
        self.failUnlessIsInstance(info.white_rating_value, int)
        self.failUnlessIsInstance(info.black_rating_value, int)
        self.failUnlessIsInstance(info.game_spec, GameSpec)
        self.failUnlessIsInstance(info.game_spec.is_private, bool)
        self.failUnlessIsInstance(info.game_spec.is_rated, bool)
        self.failUnlessIsInstance(info.game_spec.game_type, GameType)
        self.failUnlessIsInstance(info.game_spec.clock, GameClock)
        self.failUnlessEqual(info.game_no, 295)
        self.failUnlessEqual(info.white_name, 'anandkvs')
        self.failUnlessEqual(info.black_name, 'donnadistruttiva')
        self.failUnlessEqual(info.white_rating_value, 2063)
        self.failUnlessEqual(info.black_rating_value, 1960)
        self.failUnlessEqual(info.game_spec.is_private, False)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock, GameClock(90,30))
        self.failUnlessEqual(info.start_time, datetime.datetime(2012,9,15,23,34,0))


    def test_examine(self):
        cmd, status, info = parse_fics_reply(
            46, """Game 95: Game information.

  MAd is examining MAd vs pgv.
  59 halfmoves have been made.
  Fifty move count started at halfmove 59 (100 moves until a draw).
  White may castle both kingside and queenside.
  Black may not castle.
  Double pawn push didn't occur.
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, ExaminedGameExt)
        self.failUnlessEqual(info.examiner,"MAd")
        self.failUnlessEqual(info.white,"MAd")
        self.failUnlessEqual(info.black,"pgv")
        self.failUnlessEqual(info.game_no,95)

    def test_wrong(self):
        cmd, status, info = parse_fics_reply(
            46, "The current range of game numbers is 1 to 780.\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.NoSuchGame)

    def test_wrong_player(self):
        cmd, status, info = parse_fics_reply(
            46, "brianjb is not logged in.\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.BadPlayerState)
        cmd, status, info = parse_fics_reply(
            46, "BrianJB is not playing, examining or setting up a game\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.BadPlayerState)

    def test_wrong_observe(self):
        cmd, status, info = parse_fics_reply(
            80, "There is no such game.\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.NoSuchGame)

    def test_who_1(self):
        raise SkipTest
        info = parse_who_reply(
            load_parse_data_file("who.lines"))
        raise NotImplementedError() # Testy co ma wyjść

    def test_who_2(self):
        raise SkipTest
        cmd, status, info = parse_fics_reply(
            146, load_parse_data_file("who.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "who")
        raise NotImplementedError() # Testy co ma wyjść

