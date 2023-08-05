# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.datatypes.list_items import ListContents
from mekk.fics.parsing.reply.list_operations import parse_showlist_reply
from mekk.fics.test_utils import SkipTest
from mekk.fics.test_utils.internal import load_parse_data_file
from mekk.fics import errors


class ParseShowListTestCase(unittest.TestCase):
    def test_td(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-td.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='td',
                items=['abuse', 'GameBot', 'Oannes', 'srBOT', 'abuseBOT', 'GameLibraryBot',
                       'observatoer', 'statBot', 'abuseII', 'GameSaver', 'ObserveBot',
                       'STCRobot', 'adminBOT', 'javaboardBOT', 'Observer', 'SuperTD',
                       'Analysisbot', 'KothD', 'OCLbot', 'SupportBot', 'BabasChess',
                       'LectureBot', 'Offender', 'SurveyBot', 'Blackteam', 'Lecturer',
                       'OnlineTours', 'tbot', 'CCBOT', 'Linares', 'OpenLib', 'TeamLeague',
                       'ChannelBot', 'linuxchick', 'pebbo', 'testbot', 'chLog', 'littleWild',
                       'PeterParker', 'Thief', 'compabuseBOT', 'logics', 'PokerBot',
                       'ThiefTest', 'ComputerAbuse', 'MadrookBot', 'PoolBot',
                       'TourneyWatcher', 'Computers', 'mailBOT', 'puzzlebot', 'TScheduleBot',
                       'Correspondence', 'mamer', 'Rachel', 'WatchBot', 'CVLbot', 'mamerPR',
                       'Rebecca', 'WatchBotTest', 'dbslave', 'MasterGameBot', 'relay',
                       'WesBot', 'Elvira', 'MateBot', 'RelayInfo', 'Whiteteam', 'endgamebot',
                       'MuelheimNord', 'RelayScheduleBOT', 'wildBot', 'Event',
                       'NorCalLeague', 'ROBOadmin', 'Wildchess', 'FICSChampionships',
                       'notesBot', 'Sibylle', 'Yafi', 'FicsTeamBot', 'NukeBotX',
                       'SparkysDrone',]
                ))
    def test_computer(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-computers.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='computer',
                items=['Abuyen', 'DeepSjeng', 'Koibito', 'SelfKiller', 'AIchess',
                       'DeepThoughts', 'Kromer', 'ShotgunBlues', 'Alfilchess', 'DeepZ',
                       'kurushi', 'SigmaC', 'AliceC', 'DemolitionChess', 'LancePerkins',
                       'SiliconC', 'Almere', 'DeuteriumCCT', 'leaderbeans', 'Sillycon',
                       'AlmondX', 'DeuteriumEngine', 'LilKikr', 'Singularity', 'AlonzoC',
                       'DirtyChess', 'LittleBugger', 'SjengX', 'Angledust', 'djevans',
                       'LittleLurking', 'Skottel', 'Arandora', 'djunior', 'LittleThought',
                       'SlowBox', 'ArasanX', 'donkeyfactory', 'LochChessMonster',
                       'SlowMachine', 'ARChess', 'DorkyX', 'LuigiBot', 'Snelheid', 'ArShah',
                       'DotNetChess', 'Luminance', 'Sordid', 'ascp', 'DSJeng', 'Lurking',
                       'Sorgenkind', 'atomkraft', 'Ecalevol', 'marquisce', 'Species',
                       'AuraBlue', 'EJD', 'MegaBot', 'SpeckEngine', 'AuraBlueA', 'EnginMax',
                       'megielszmergiel', 'Speyside', 'AuraBlueB', 'exeComp', 'meru',
                       'SpyderChess', 'AuraBlueC', 'FeralChess', 'MiloBot', 'Squirrels',
                       'AuraBlueD', 'FireCompi', 'MiniZerdax', 'sregorg', 'AuraBlueE',
                       'FirstCore', 'Moireabh', 'stayalive', 'Azkikr', 'fjjvh',
                       'MortimerBlackwell', 'strelka', 'babylonbot', 'FunComp', 'MrsLurking',
                       'StTeresa', 'BabyLurking', 'Gamin', 'mscp', 'SuperBooker', 'BertaCCT',
                       'Gaviota', 'myceX', 'SuperCanuck', 'BigDaddy', 'GeidiPrime', 'mycomp',
                       'SuperZerdax', 'BigMomma', 'Gigabot', 'MyrddinComp', 'SupremeBeing',
                       'birdcostello', 'GlaurungC', 'nakshatra', 'Symbolic', 'bistromath',
                       'GnuCheese', 'NightmareX', 'Telepath', 'BlackDemon', 'GNUChessSix',
                       'ntwochess', 'tentacle', 'blik', 'GoldBarMM', 'Obnoxious',
                       'TestOfLogics', 'bobbyfischer', 'GreatPumpkin', 'oldman',
                       'TheConfusedComp', 'BotTheBaron', 'GriffyJr', 'Olympus', 'Thiamath',
                       'BremboCE', 'GriffySr', 'Opossum', 'Thinker', 'BugZH',
                       'GuaraniSchulz', 'Osquip', 'Thukydides', 'callipygian', 'Gunwalloe',
                       'owlce', 'TimeaChess', 'CapivaraLK', 'Hephasto', 'parrot',
                       'TinkerFICS', 'CatNail', 'highrating', 'PawnyX', 'TJchess', 'cchess',
                       'hokuspokus', 'Pentiumpatzer', 'TJChessA', 'ChainReaction',
                       'hokuspokusII', 'PhoenixAsh', 'TJchessB', 'ChangeIsComing', 'Horsian',
                       'plink', 'TogaII', 'ChessCentre', 'Hossa', 'plisk', 'TogaRouter',
                       'ChessMindEngine', 'Humpers', 'Plnik', 'Tosco', 'ChessplayingBot',
                       'HussarFICS', 'Polycephaly', 'TrojanKnight', 'ChessPlusPlus',
                       'Hutnik', 'PopperX', 'TurboGM', 'ChessTraining', 'IFDThor', 'Potajex',
                       'TwistedLogicX', 'Chirone', 'IkarusX', 'Prolegomena', 'twoxone',
                       'chirpy', 'inemuri', 'qgchess', 'umko', 'codpiece', 'Ingoc',
                       'Rakanishu', 'Uniblab', 'Compi', 'Inqstr', 'redqueenchess',
                       'VictoriaBot', 'Compucheck', 'InstanceC', 'resistentialism', 'Vogen',
                       'crafty', 'IronSpike', 'RoboSigma', 'Webkikr', 'CrazyBeukiBot',
                       'JabbaChess', 'Rookie', 'wildbird', 'cubebox', 'JadeiteMech', 'Rueno',
                       'XabacUs', 'DarkAngel', 'javachesscomp', 'SaqqaraX', 'ynode',
                       'DayDreamerX', 'JuniorLurking', 'scaramanga', 'Zawaenn', 'DDD',
                       'KayNineDawg', 'Schizophreniac', 'Zchizophrenic', 'DeepJunior', 'Kec',
                       'Scomb', 'zerowin', 'DeepNightmare', 'knightsmasher', 'searcherFICS',
                       'zzzzzztrainer',]))
    def test_channel(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-channel.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='channel',
                items=['4', '53']))
    def test_empty_notify(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-emptynotify.lines"))
        self.failUnlessEqual(info, ListContents(
            name='notify',
            items=[]
        ))
    def test_syntax_error(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_showlist_reply,
            'Zielony krokodyl.')
    def test_logic_error(self):
        self.failUnlessRaises(
            errors.UnknownList,
            parse_showlist_reply,
            '"xx" does not match any list name.')
    def test_logic_error_checkattr(self):
        try:
            parse_showlist_reply(
                '"xx" does not match any list name.')
            self.fail("parse_showlist_reply failed to throw on unknown list name")
        except errors.UnknownList as e:
            self.failUnlessEqual(e.list_name, "xx")
