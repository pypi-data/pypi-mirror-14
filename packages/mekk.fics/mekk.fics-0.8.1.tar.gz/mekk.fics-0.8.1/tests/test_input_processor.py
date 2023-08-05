# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.date import FicsDateInfo
from mekk.fics.datatypes.game_clock import GameClock
from mekk.fics.datatypes.game_info import ExaminedGame, PlayedGame, GameSpec, ObservedGame, GameReference
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.generic import GenericText
from mekk.fics.datatypes.list_items import ListContents
from mekk.fics.datatypes.notifications import ChannelTell, GameNote, AttributedTell
from mekk.fics.datatypes.player import PlayerName, PlayerRating, ResultStats
from mekk.fics.parsing import fics_parser
from mekk.fics.test_utils.helpers import load_tstdata_file, assert_dicts_equal
import logging
import datetime
from decimal import Decimal

logger = logging.getLogger("test")

#pycharm fails to handle self.failUnlessIsInstance
#noinspection PyTypeChecker
class InputProcessorTestCase(unittest.TestCase):

    def setUp(self):
        self.info = []  # list of pairs (what, dict) for fics info
        self.replies = dict()  # command → [ (what, dict) ] for block replies
        self.ip = fics_parser.FicsTextProcessor(
            info_callback=self._info_callback,
            block_callback=self._block_callback,
            label="TEST")
    def _info_callback(self, event_type, event_data):
        self.failUnlessIsInstance(event_type, str)
        self.failUnlessIsInstance(event_data, tuple) # namedtuple
        self.info.append( (event_type, event_data) )
    def _block_callback(self, command_id, command_name, status, command_data):
        self.failUnlessIsInstance(command_id, int)
        self.failUnlessIsInstance(command_name, str)
        self.failUnlessIsInstance(status, bool)
        if status:
            self.failUnlessIsInstance(command_data, tuple) # namedtuple
        else:
            self.failUnlessIsInstance(command_data, Exception)
        if not command_id in self.replies:
            self.replies[command_id] = []
        self.replies[command_id].append( (command_name, status, command_data) )

    def test_input_processor(self):
        file_text = load_tstdata_file('ficsparserdata', 'session-short.transcript')
        file_lines = file_text.split("\n\r")
        for line in file_lines:
            if 'Starting FICS session as' in line:
                break
        for line in file_lines:
            self.ip.consume_input_line(line)
        non_trivial_info = [
            (what, data)
            for what, data in self.info
            if what != 'unknown'
        ]

        # Replies verification (match against session-short.transcript)
        self.failUnlessEqual(
            self.replies.pop(11), [
            ("set", True, GenericText(text="Style 12 set."))
            ])
        self.failUnlessEqual(
            self.replies.pop(12), [
            ("set", True, GenericText(text="You will not see seek ads."))
            ])
        cmd, status, data = self.replies.pop(13)[0]
        self.failUnlessEqual(cmd, "games")
        self.failUnlessEqual(data.examines, [ExaminedGame(game_no=1), ExaminedGame(game_no=150), ExaminedGame(game_no=229)])
        self.failUnlessEqual(data.setups, [])
        self.failUnlessEqual(data.games[0], PlayedGame(
            game_no=2,
            white_truncated_name=PlayerName('hdhdrhgdg'), white_rating_value=0,
            black_truncated_name=PlayerName('GuestFPZK'), black_rating_value=0,
            game_spec=GameSpec(
                    clock=GameClock(8,7),
                    is_private=False,
                    is_rated=False,
                    game_type=GameType('b'))))
        self.failUnlessEqual(data.games[-1],
            PlayedGame(
                game_no=149,
                black_truncated_name=PlayerName('BigDaddy'), black_rating_value=2990,
                white_truncated_name=PlayerName('parrot'), white_rating_value=2300,
                game_spec=GameSpec(
                    clock=GameClock(15,0), is_private=False,
                    is_rated=True, game_type=GameType('s'))))
        self.failUnlessEqual(
            self.replies.pop(15), [
                ("observe", True, ObservedGame(
                            game_no=60,
                            white_name=PlayerName('GYOI'), white_rating_value=2049,
                            black_name=PlayerName('urtooeasy'), black_rating_value=2059,
                            game_spec=GameSpec(
                                clock=GameClock(3, 0), is_private=False,
                                is_rated=True, game_type=GameType('blitz')),
                            initial_style12=style12.Style12(
                                "<12> rnbqkb-r pppppppp -----n-- -------- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 60 GYOI urtooeasy 0 3 0 39 39 178 175 2 P/c2-c4 (0:02) c4 0 1 0"))
                 )
            ])
        self.failUnlessEqual(
            self.replies.pop(16), [
                ("date", True, FicsDateInfo(gmt=datetime.datetime(2012, 1, 2, 8, 46), gmt_zone_name='GMT',
                    local=datetime.datetime(2012, 1, 2, 0, 46), local_zone_name='PST',
                    server=datetime.datetime(2012, 1, 2, 0, 46), server_zone_name='PST'))
            ])
        self.failUnlessEqual(
            self.replies.pop(17), [
                ("observe", True, ObservedGame(
                    game_no=182,
                    white_name=PlayerName('milecker'), white_rating_value=1933,
                    black_name=PlayerName('jamofr'), black_rating_value=1908,
                    game_spec=GameSpec(
                        is_rated=True, is_private=False, game_type=GameType('blitz'), clock=GameClock(3, 0)),
                    initial_style12=style12.Style12(
                        "<12> r-q-kbnr ppp--p-p ---p--p- ---Pp--- --P----- -QNBPP-- PP----PP R----RK- B -1 0 0 1 1 1 182 milecker jamofr 0 3 0 33 33 118 148 11 o-o (0:04) O-O 0 1 0")))
            ])
        self.failUnlessEqual(
            self.replies.pop(18), [
                ("unobserve", True, GameReference(game_no=60))
            ])
        self.failUnlessEqual(
            self.replies.pop(19), [
                ("showlist", True, ListContents(name='td', items=[
                    'abuse', 'GameBot', 'Oannes', 'srBOT', 'abuseBOT', 'GameLibraryBot', 'observatoer', 'statBot',
                    'abuseII', 'GameSaver', 'ObserveBot', 'STCRobot', 'adminBOT', 'javaboardBOT', 'Observer', 'SuperTD',
                    'Analysisbot', 'KothD', 'OCLbot', 'SupportBot', 'BabasChess', 'LectureBot', 'Offender', 'SurveyBot',
                    'Blackteam', 'Lecturer', 'OnlineTours', 'tbot', 'CCBOT', 'Linares', 'OpenLib', 'TeamLeague',
                    'ChannelBot', 'linuxchick', 'pebbo', 'testbot', 'chLog', 'littleWild', 'PeterParker', 'Thief',
                    'compabuseBOT', 'logics', 'PokerBot', 'ThiefTest', 'ComputerAbuse', 'MadrookBot', 'PoolBot',
                    'TourneyWatcher', 'Computers', 'mailBOT', 'puzzlebot', 'TScheduleBot', 'Correspondence', 'mamer',
                    'Rachel', 'WatchBot', 'CVLbot', 'mamerPR', 'Rebecca', 'WatchBotTest', 'dbslave', 'MasterGameBot',
                    'relay', 'WesBot', 'Elvira', 'MateBot', 'RelayInfo', 'Whiteteam', 'endgamebot', 'MuelheimNord',
                    'RelayScheduleBOT', 'wildBot', 'Event', 'NorCalLeague', 'ROBOadmin', 'Wildchess',
                    'FICSChampionships',
                    'notesBot', 'Sibylle', 'Yafi', 'FicsTeamBot', 'NukeBotX', 'SparkysDrone']))])
        r14 = self.replies.pop(14)
        self.failUnlessEqual(len(r14), 1)
        r14_cmd, r14_sts, r14_info = r14[0]
        self.failUnlessEqual(r14_cmd, "finger")
        self.failUnlessEqual(r14_sts, True)
        self.failUnlessEqual(r14_info.name, 'Mekk')
        assert_dicts_equal(self, r14_info.results, {
            GameType('Atomic'): ResultStats(best=None, wins_count=23, draws_count=1, losses_count=50, rating=PlayerRating(1525, rd=Decimal('158.9'))),
            GameType('Blitz'): ResultStats(best=1522, wins_count=3900, draws_count=410, losses_count=5797, rating=PlayerRating(1342, rd=Decimal('41.5'))),
            GameType('Bughouse'): ResultStats(best=None, wins_count=3, draws_count=0, losses_count=5, rating=PlayerRating(1035, rd=Decimal('350.0'))),
            GameType('Crazyhouse'): ResultStats(best=1495, wins_count=73, draws_count=0, losses_count=235, rating=PlayerRating(1451, rd=Decimal('99.4'))),
            GameType('Lightning'): ResultStats(best=1116, wins_count=15, draws_count=1, losses_count=115, rating=PlayerRating(1495, rd=Decimal('232.8'))),
            GameType('Losers'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=6, rating=PlayerRating(1674, rd=Decimal('350.0'))),
            GameType('Standard'): ResultStats(best=1935, wins_count=730, draws_count=156, losses_count=913, rating=PlayerRating(1759, rd=Decimal('68.2'))),
            GameType('Suicide'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=14, rating=PlayerRating(1384, rd=Decimal('277.9'))),
            GameType('Wild'): ResultStats(best=1875, wins_count=287, draws_count=31, losses_count=457, rating=PlayerRating(1683, rd=Decimal('100.1')))
            })
        assert_dicts_equal(
            self,
            r14_info.plan,[
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
                ])
        self.failUnlessEqual(
            self.replies.pop(20), [
                ("quit", True, GenericText(text='Logging you out.'))
            ])
        self.failUnlessEqual(self.replies, {})

        # Async notes verification (match against session-short.transcript)
        self.failUnlessEqual(
            non_trivial_info.pop(0),
            # TODO: handle continuations - and require this text to be longer
            ("tell", AttributedTell(player=PlayerName('ROBOadmin'), text='Welcome to FICS - the Free Internet Chess Server. '))
        )
        self.failUnlessEqual(
            non_trivial_info.pop(0),
            ("channel_tell", ChannelTell(player=PlayerName('GuestXMRT'), text="you don't win by resigning or disconnecting", channel=53))
        )
        self.failUnlessEqual(
            non_trivial_info.pop(0),
            ("game_note", GameNote(game_no=60, note="GYOI requests to abort the game."))
        )

        what, data = non_trivial_info.pop(0)
        self.failUnlessEqual(what, "game_move")
        self.failUnlessIsInstance(data.style12, style12.Style12)
        self.failUnlessEqual(str(data.style12), "<12> r-q-k-nr ppp--pbp ---p--p- ---Pp--- --P----- -QNBPP-- PP----PP R----RK- W -1 0 0 1 1 2 182 milecker jamofr 0 3 0 33 33 118 146 12 B/f8-g7 (0:02) Bg7 0 1 185")

        what, data = non_trivial_info.pop(0)
        self.failUnlessEqual(what, "game_move")
        self.failUnlessIsInstance(data.style12, style12.Style12)
        self.failUnlessEqual(str(data.style12), "<12> r-q-k-nr ppp--pbp ---p--p- --PPp--- -------- -QNBPP-- PP----PP R----RK- B -1 0 0 1 1 0 182 milecker jamofr 0 3 0 33 33 106 146 12 P/c4-c5 (0:12) c5 0 1 53")

        what, data = non_trivial_info.pop(0)
        self.failUnlessEqual(what, "game_move")
        self.failUnlessIsInstance(data.style12, style12.Style12)
        self.failUnlessEqual(str(data.style12), "<12> r-q-k--r ppp-npbp ---p--p- --PPp--- -------- -QNBPP-- PP----PP R----RK- W -1 0 0 1 1 1 182 milecker jamofr 0 3 0 33 33 106 141 13 N/g8-e7 (0:05) Ne7 0 1 946")

        what, data = non_trivial_info.pop(0)
        self.failUnlessEqual(what, "game_move")
        self.failUnlessIsInstance(data.style12, style12.Style12)
        self.failUnlessEqual(str(data.style12), "<12> r-q-k--r ppp-npbp ---p--p- -BPPp--- -------- -QN-PP-- PP----PP R----RK- B -1 0 0 1 1 2 182 milecker jamofr 0 3 0 33 33 102 141 13 B/d3-b5 (0:04) Bb5+ 0 1 52")

        #what, data = non_trivial_info.pop(0)
        #self.failUnlessEqual(what, "game_move")
        #self.failUnlessIsInstance(data.style12, style12.Style12)
        #self.failUnlessEqual(str(data.style12), "<12> r-q-kbnr ppp--p-p ---p--p- ---Pp--- --P----- -QNBPP-- PP----PP R----RK- B -1 0 0 1 1 1 182 milecker jamofr 0 3 0 33 33 118 148 11 o-o (0:04) O-O 0 1 0")

        #what, data = non_trivial_info.pop(0)
        #self.failUnlessEqual(what, "game_move")
        #self.failUnlessIsInstance(data.style12, style12.Style12)
        #self.failUnlessEqual(str(data.style12), "<12> r-q-k-nr ppp--pbp ---p--p- --PPp--- -------- -QNBPP-- PP----PP R----RK- B -1 0 0 1 1 0 182 milecker jamofr 0 3 0 33 33 106 146 12 P/c4-c5 (0:12) c5 0 1 53")

        #what, data = non_trivial_info.pop(0)
        #self.failUnlessEqual(what, "game_move")
        #self.failUnlessIsInstance(data.style12, style12.Style12)
        #self.failUnlessEqual(str(data.style12), "<12> r-q-k--r ppp-npbp ---p--p- --PPp--- -------- -QNBPP-- PP----PP R----RK- W -1 0 0 1 1 1 182 milecker jamofr 0 3 0 33 33 106 141 13 N/g8-e7 (0:05) Ne7 0 1 946")

        # Without block wrapper as it happens after logout
        what,data = non_trivial_info.pop(0)
        self.failUnlessEqual(what, "observing_finished")
        self.failUnlessEqual(data, GameReference(game_no=182))

        self.failUnlessEqual(non_trivial_info, [])

