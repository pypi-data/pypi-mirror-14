# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.constants import block_codes
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.color import Color
from mekk.fics.datatypes.date import FicsDateInfo
from mekk.fics.datatypes.game_clock import GameClock
from mekk.fics.datatypes.game_info import GameReference, ExaminedGame, SetupGame, PlayedGame, GameSpec
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.list_items import ListContents
from mekk.fics.datatypes.notifications import SeekRef, Seek
from mekk.fics.datatypes.player import PlayerName, FingerInfo, ResultStats, PlayerRating
from mekk.fics.datatypes.channel import ChannelRef
from mekk.fics.parsing.reply_parser import parse_fics_reply
from mekk.fics.test_utils import assert_dicts_equal, assert_tables_equal, SkipTest
from mekk.fics.test_utils.internal import (
    load_parse_data_file, load_parse_data_file_patching_continuations)
from mekk.fics import errors
import datetime
from decimal import Decimal


class ParseReplyTestCase(unittest.TestCase):

    def test_handle(self):
        cmd, status, info = parse_fics_reply(
            48,
            """-- Matches: 100 player(s) --
MAd             MADADDS         MADAGASCAROV    madalasriharsha madam           madamdede       Madamspank      madandy         MadArab         madas           madatchess      madaxe          MadBadCat       madbarber       madbishopmelun
mada            madadh          MadagascarX     madalin         MADAMADA        madamebutterfly madamus         madangry        Madaranipuni    madasabadger    MADatlas        madaxeman       MadBadger       madbawl         MadBison
madaboutchess   MadaElshereif   Madahda         madalina        MadaMadaDane    MadameJohn      madamx          Madani          madarasharingan madasafish      madattack       madaxy          MadBadRambo     MadBeans
Madaboutcycling Madafaka        madairman       MadalinaMAnusca madamadamada    MadameSparkle   madamxx         madAnne         madarbozorg     Madasawheel     madatter        madaz           madbalger       MadBiker
MadAboutH       madafakaru      Madak           Madaline        madaman         madami          madan           madantzoy       MadArmenian     madashell       madaus          Madazo          Madball         madbikerpa
madaboutyou     madafakarul     madakram        Madalitso       Madamax         madamimadam     madana          MADAR           Madart          madasigid       MadAussie       MadAzz          madballster     madbiotic
madachab        madagascar      madalasridhar   madalyne        Madamboevarix   madamsm         MADANDAN        Madara          madartink       madasmsm        madawg          madB            madbananas      MadBishop
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "handles")
        self.failUnlessIsInstance(info, ListContents)
        self.failUnlessEqual(len(info.items), 100)
        self.failUnlessEqual(info.items[0], PlayerName('MAd'))
        self.failUnlessEqual(info.items[0].name, 'MAd')
        self.failUnlessEqual(info.items[1], PlayerName('MADADDS'))
        self.failUnlessEqual(info.items[-1], PlayerName('MadBishop'))

    def test_date(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_DATE,
            """Local time     - Tue Jan  3, 02:29 EURCST 2012
Server time    - Tue Jan  3, 00:29 PST 2012
GMT            - Tue Jan  3, 08:29 GMT 2012""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "date")
        self.failUnlessEqual(info, FicsDateInfo(
            local_zone_name="EURCST",
            server_zone_name="PST",
            gmt_zone_name="GMT",
            server=datetime.datetime(2012, 1, 3, 0 ,29, 0),
            local=datetime.datetime(2012, 1, 3, 2, 29, 0),
            gmt=datetime.datetime(2012, 1, 3, 8, 29, 0),
        ))
    def test_observe_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            load_parse_data_file("observe-normal.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessEqual(info.game_no, 92)
        self.failUnlessEqual(info.white_name, PlayerName('Motyl'))
        self.failUnlessEqual(info.white_rating_value, 1857)
        self.failUnlessEqual(info.black_name, PlayerName('Aretus'))
        self.failUnlessEqual(info.black_rating_value, 1907)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock,
                             GameClock(base_in_minutes=15,inc_in_seconds=10))
        self.failUnlessEqual(info.game_spec.is_private, False)
        is12 = info.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (0:00) none 0 0 0")

    def test_observe_private(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            "Sorry, game 125 is a private game")
        self.failIf(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.FicsCommandExecutionException)
        self.failUnlessIsInstance(info, errors.AttemptToAccessPrivateGame)
        # TODO: test exception class and info

    def test_observe_bad_style12(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            """You are now observing game 92.
Game 92: Motyl (1857) Aretus (1907) rated standard 15 10

<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (-:00) none 0 0 0
""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsClientException)
        self.failUnlessIsInstance(info, errors.BadStyle12Format)
        # TODO:
        #self.failUnlessIsInstance(info, errors.FicsCommandException)
        #self.failUnlessIsInstance(info, errors.FicsCommandExecutionException)
        #self.failUnlessIsInstance(info, errors.AttemptToAccessPrivateGame)

    def test_unobserve_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_UNOBSERVE,
            "Removing game 124 from observation list.")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "unobserve")
        self.failUnlessEqual(info, GameReference(game_no=124))

    def test_unobserve_logic_fail(self):
        for line in [
            "You are not observing game 13.",
            "You are not observing any games.",
        ]:
            cmd, status, info = parse_fics_reply(
                block_codes.BLKCMD_UNOBSERVE,
                line)
            self.failIf(status)
            self.failUnlessEqual(cmd, "unobserve")
            self.failUnlessIsInstance(info, errors.AttemptToActOnNotUsedGame)

    def test_unobserve_bad_syntax(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_UNOBSERVE,
            "Blah.")
        self.failIf(status)
        self.failUnlessEqual(cmd, "unobserve")
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_games_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            load_parse_data_file("games.lines")
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "games")
        games = info.games
        examines = info.examines
        setups = info.setups
        self.failUnlessIsInstance(games, list)
        self.failUnlessIsInstance(examines, list)
        self.failUnlessIsInstance(setups, list)
        # TODO: check funny mismatch between actual count in games output
        #       and count reported by FICS in summary (in the sample
        #       we use here there are 260 games, 8 examines and 1 setup,
        #       and FICS summarizes it as 267 games)
        self.failUnlessEqual(len(games), 260, "Games count mismatch")
        self.failUnlessEqual(len(examines), 8)
        self.failUnlessEqual(len(setups), 1)
        for g in games:
            self.failUnlessIsInstance(g, PlayedGame)
            self.failUnlessIsInstance(g.game_no, int)
            self.failUnlessIsInstance(g.white_truncated_name, PlayerName)
            self.failUnlessIsInstance(g.black_truncated_name, PlayerName)
            self.failUnlessIsInstance(g.white_rating_value, int)
            self.failUnlessIsInstance(g.black_rating_value, int)
            self.failUnlessIsInstance(g.game_spec, GameSpec)
            self.failUnlessIsInstance(g.game_spec.is_private, bool)
            self.failUnlessIsInstance(g.game_spec.is_rated, bool)
            self.failUnlessIsInstance(g.game_spec.game_type, GameType)
            self.failUnlessIsInstance(g.game_spec.clock, GameClock)
        for g in examines:
            self.failUnlessIsInstance(g, ExaminedGame)
            self.failUnlessIsInstance(g.game_no, int)
        for g in setups:
            self.failUnlessIsInstance(g, SetupGame)
            self.failUnlessIsInstance(g.game_no, int)
        self.failUnlessEqual(
            examines[0],
            ExaminedGame(game_no=1)
        )
        self.failUnlessEqual(
            examines[3],
            ExaminedGame(game_no=155)
        )
        self.failUnlessEqual(
            setups[0],
            SetupGame(game_no=233)
        )
        # TODO: functions to decode short player name into long one
        self.failUnlessEqual(
            games[0],
            PlayedGame(
                game_no=8,
                white_truncated_name=PlayerName('GuestCNQG'), white_rating_value=0,
                black_truncated_name=PlayerName('GuestBFQS'), black_rating_value=0,
                game_spec=GameSpec(
                    game_type=GameType('s'),
                    is_private=False, is_rated=False,
                    clock=GameClock(10,10))))
        self.failUnlessEqual(
            games[94],
            PlayedGame(
                game_no=239,
                white_truncated_name=PlayerName('Waltherion'), white_rating_value=1133,
                black_truncated_name=PlayerName('LordoftheP'), black_rating_value=1200,
                game_spec=GameSpec(
                    game_type=GameType('b'),
                    is_private=True, is_rated=True,
                    clock=GameClock(5,0))))
        self.failUnlessEqual(
            games[110],
            PlayedGame(
                game_no=146,
                white_truncated_name=PlayerName('Niloz'), white_rating_value=1262,
                black_truncated_name=PlayerName('papier'), black_rating_value=1220,
                game_spec=GameSpec(
                    game_type=GameType('b'),
                    is_private=False, is_rated=True,
                    clock=GameClock(3, 12))))
        self.failUnlessEqual(
            games[75],
            PlayedGame(
                game_no=60,
                white_truncated_name=PlayerName('asturia'), white_rating_value=1840,
                black_truncated_name=PlayerName('GuestNVLL'), black_rating_value=0,
                game_spec=GameSpec(
                    game_type=GameType('s'),
                    is_private=False, is_rated=False,
                    clock=GameClock(15, 0))))
        self.failUnlessEqual(
            games[250],
            PlayedGame(
                game_no=77,
                white_truncated_name=PlayerName('twobi'), white_rating_value=1891,
                black_truncated_name=PlayerName('FiNLiP'), black_rating_value=2074,
                game_spec=GameSpec(
                    game_type=GameType('L'),
                    is_private=False, is_rated=True,
                    clock=GameClock(3, 0))))

    # line-11
    def test_games_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            "")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_games_ugly(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            """
  1 (Exam.    0 Spiro          0 Najdorf   ) [ uu  0   0] W:  3
 34 ++++ xmattbbb    ++++ GuestSGYZ  [ bu  2  12]   2:22 -  2:55 (33-35) W: 10
 some ugly text
 162 1563 sgmza       1611 seva       [ br  5   0]   2:20 -  2:55 (35-21) B: 19

  3 games displayed.""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_games_truncated_no_summary(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            """
 34 ++++ xmattbbb    ++++ GuestSGYZ  [ bu  2  12]   2:22 -  2:55 (33-35) W: 10
 162 1563 sgmza       1611 seva       [ br  5   0]   2:20 -  2:55 (35-21) B: 19""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_finger_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            "")
        self.failIf(status)
        self.failUnlessEqual(cmd, "finger")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_finger_badname(self):
        for error_note, player_name in [
            ("'thebestplayerinthe' is not a valid handle.", "thebestplayerinthe"),
            ("There is no player matching the name guestzzzz.", "guestzzzz"),
        ]:
            cmd, status, info = parse_fics_reply(
                block_codes.BLKCMD_FINGER,
                error_note)
            self.failIf(status)
            self.failUnlessEqual(cmd, "finger")
            self.failUnlessIsInstance(info, Exception)
            self.failUnlessIsInstance(info, errors.FicsCommandException)
            self.failUnlessIsInstance(info, errors.UnknownPlayer)
            self.failUnlessEqual(info.player_name, player_name)

    def test_finger_simple(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file("finger-mek.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="Mek",
            results={
                GameType('Standard'): ResultStats(
                    rating=PlayerRating(1606, rd=Decimal('350.0')),
                    best=None, wins_count=0, losses_count=1, draws_count=0),
            },
            plan=[
            ]))

    def test_finger_complicated(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file_patching_continuations("finger-mekk.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="Mekk",
            results={
                GameType('Atomic'): ResultStats(best=None, wins_count=23, draws_count=1, losses_count=50, rating=PlayerRating(1525, rd=Decimal('159.2'))),
                GameType('Blitz'): ResultStats(best=1522, wins_count=3900, draws_count=410, losses_count=5797, rating=PlayerRating(1342, rd=Decimal('42.4'))),
                GameType('Bughouse'): ResultStats(best=None, wins_count=3, draws_count=0, losses_count=5, rating=PlayerRating(1035, rd=Decimal('350.0'))),
                GameType('Crazyhouse'): ResultStats(best=1495, wins_count=73, draws_count=0, losses_count=235, rating=PlayerRating(1451, rd=Decimal('99.8'))),
                GameType('Lightning'): ResultStats(best=1116, wins_count=15, draws_count=1, losses_count=115, rating=PlayerRating(1495, rd=Decimal('233.0'))),
                GameType('Losers'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=6, rating=PlayerRating(1674, rd=Decimal('350.0'))),
                GameType('Standard'): ResultStats(best=1935, wins_count=730, draws_count=156, losses_count=913, rating=PlayerRating(1759, rd=Decimal('68.8'))),
                GameType('Suicide'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=14, rating=PlayerRating(1384, rd=Decimal('278.1'))),
                GameType('Wild'): ResultStats(best=1875, wins_count=287, draws_count=31, losses_count=457, rating=PlayerRating(1683, rd=Decimal('100.5')))
            },
            plan=[
                'Marcin Kasperski, Warsaw, Poland. http://mekk.waw.pl',
                'wild fr=normal chess with randomized initial position. Great fun! I can play unrated wild fr game and explain the rules, just ask.',
                'Please, say "good game" only if it was good game. Auto-greetings are incredibly irritating.',
                'If I happen to ignore your tells, most likely I am playing from my mobile phone (btw, http://yafi.pl is a great mobile fics client)',
                'Correspondence chess is great if you have little time, but prefer thinking games. My tips:  http://schemingmind.com for web-based play, http://e4ec.org if you want to stay with email. On schemingmind you can also learn atomic, crazyhouse, wild fr and other variants - without time pressure.',
                'I wrote and maintain WatchBot. http://mekk.waw.pl/mk/watchbot',
                'FICS enhancements ideas:  http://mekk.waw.pl/mk/eng/chess/art/ideas_fics',
                'How to write a FICS bot: http://blog.mekk.waw.pl/archives/7-How-to-write-a-FICS-bot-part-I.html',
                'Szachowy slownik polsko-angielski: http://mekk.waw.pl/mk/szachy/art/ang_terminologia',
                'Polski podrecznik FICS: http://mekk.waw.pl/mk/szachy/art/fics_opis',
                ]))

    def test_finger_guest(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file_patching_continuations("finger-guest.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="GuestVNCT",
            results=dict(),
            plan=[
            ]))

    def test_seek_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK,
            "Your seek has been posted with index 95."
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(95))

    def test_seek_seen(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK,
            """Your seek has been posted with index 25."
(3 player(s) saw the seek.)"""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(25))
    def test_seek_updated(self):
        # TODO: check this syntax (not sure whether first line may happen alone)
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK, # ??? TODO: spr czy to ten kod
            """Updating seek ad 35; rating range now 1340-1344.

Your seek has been posted with index 35.
(1 player(s) saw the seek.)"""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(35))
    def test_sought(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SOUGHT,
            """ 90 2663 stayalive(C)        3   0 unrated suicide                0-9999
115 2555 Sordid(C)           3   0 unrated atomic                 0-9999 f
119 ++++ GuestQDXP           5   0 unrated blitz      [white]     0-9999 m
136 ++++ GuestKNGV           2   0 unrated lightning              0-9999 f
146 ++++ GuestYGSC          20  30 unrated standard               0-9999 m
153 ++++ DeepTougtII         3   0 unrated blitz                  0-9999 f
11 ads displayed."""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sought")
        assert_tables_equal(self, info, [
                Seek(seek_no=90,
                     player=PlayerName('stayalive'),
                     player_rating_value=2663,
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('suicide'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=115,
                     player=PlayerName('Sordid'),
                     player_rating_value=2555,
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('atomic'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=119,
                     player=PlayerName('GuestQDXP'),
                     player_rating_value=0,
                     is_manual=True,
                     using_formula=False,
                     color=Color("white"),
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(5, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=136,
                     player=PlayerName('GuestKNGV'),
                     player_rating_value=0,
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('lightning'),
                                        clock=GameClock(2, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=146,
                     player=PlayerName('GuestYGSC'),
                     player_rating_value=0,
                     is_manual=True,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('standard'),
                                        clock=GameClock(20, 30),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=153,
                     player=PlayerName('DeepTougtII'),
                     player_rating_value=0,
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                ])

    def test_sought_sb(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SOUGHT,
            """ 22 1298  Brewwhaha           3   3 rated   blitz                  0-9999 f
 61 1679  Frankkenstein      20   5 rated   standard            1650-9999
 63 1977  antoni              6   0 rated   blitz                  0-9999 m
106 1719  ifufocop            3   0 rated   crazyhouse          1300-1670
114 1776  Embedics            3  12 rated   wild/fr                0-9999
115 1298  SylvainSLA          8  10 rated   blitz                  0-9999
180 1243  taniuzhka           4   0 unrated blitz               1000-1999 mf
8 ads displayed.
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sought")
        assert_tables_equal(self, info, [
                Seek(seek_no=22,
                     player=PlayerName('Brewwhaha'),
                     player_rating_value=1298,
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(3, 3),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=61,
                     player=PlayerName('Frankkenstein'),
                     player_rating_value=1679,
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     # min_rating=1650
                     # max_rating=9999
                     game_spec=GameSpec(game_type=GameType('standard'),
                                        clock=GameClock(20, 5),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=63,
                     player=PlayerName('antoni'),
                     player_rating_value=1977,
                     is_manual=True,
                     using_formula=False,
                     color=None,
                     # TODO
                     # min_rating=1650
                     # max_rating=9999
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(6, 0),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=106,
                     player=PlayerName('ifufocop'),
                     player_rating_value=1719,
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     #min_rating=1300,
                     #max_rating=1670,
                     game_spec=GameSpec(game_type=GameType('crazyhouse'),
                                        clock=GameClock(3, 0),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=114,
                     player=PlayerName('Embedics'),
                     player_rating_value=1776,
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     #min_rating=0,
                     #max_rating=9999,
                     game_spec=GameSpec(game_type=GameType('wild/fr'),
                                        clock=GameClock(3, 12),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=115,
                     player=PlayerName('SylvainSLA'),
                     player_rating_value=1298,
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(8, 10),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=180,
                     player=PlayerName('taniuzhka'),
                     player_rating_value=1243,
                     is_manual=True,
                     using_formula=True,
                     color=None,
                     # TODO
                     # min_rating=1000
                     # max_rating=1999
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(4, 0),
                                        is_rated=False,
                                        is_private=False)),
        ])

    def test_channel_subscribed(self):
        cmd, status, info = parse_fics_reply(
            12, '[1] added to your channel list.')
        self.failUnless(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessEqual(info,
                             ChannelRef(channel=1))

    def test_gnotify_added(self):
        cmd, status, info = parse_fics_reply(
            12, "[Mlasker] added to your gnotify list\n")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessEqual(info, PlayerName('Mlasker'))

    def test_notify_added(self):
        cmd, status, info = parse_fics_reply(
            12, '[ryosHu] added to your notify list.\n')
        self.failUnless(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessEqual(info, PlayerName('ryoshu'))

    def test_gnotify_removed(self):
        cmd, status, info = parse_fics_reply(
            129, '[koza] removed from your gnotify list.\n')
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sublist")
        self.failUnlessEqual(info, PlayerName('koza'))

    def test_notify_removed(self):
        cmd, status, info = parse_fics_reply(
            129, '[koza] removed from your notify list.\n')
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sublist")
        self.failUnlessEqual(info, PlayerName('koza'))

    def test_notify_already(self):
        cmd, status, info = parse_fics_reply(
            12, '[koza] is already on your notify list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.AlreadyOnList)

    def test_gnotify_already(self):
        cmd, status, info = parse_fics_reply(
            12, '[koza] is already on your gnotify list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.AlreadyOnList)

    def test_notify_missing(self):
        cmd, status, info = parse_fics_reply(
            129, '[koza] is not in your notify list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "sublist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.NotOnList)

    def test_gnotify_missing(self):
        cmd, status, info = parse_fics_reply(
            129, '[koza] is not in your gnotify list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "sublist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.NotOnList)


    def test_channel_already(self):
        cmd, status, info = parse_fics_reply(
            12, '[17] is already on your channel list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.AlreadyOnList)

    def test_channel_missing(self):
        cmd, status, info = parse_fics_reply(
            129, '[8] is not in your channel list.\n')
        self.failIf(status)
        self.failUnlessEqual(cmd, "sublist")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.NotOnList)


    # TODO: tests for more commands
