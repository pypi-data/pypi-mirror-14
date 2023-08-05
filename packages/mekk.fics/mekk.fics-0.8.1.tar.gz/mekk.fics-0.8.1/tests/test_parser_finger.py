from twisted.trial import unittest
from decimal import Decimal
from mekk.fics.datatypes.player import (
    FingerInfo, ResultStats, PlayerRating)
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.test_utils.internal import (
    load_parse_data_file, load_parse_data_file_patching_continuations)
from mekk.fics import errors
from mekk.fics.parsing.reply.finger import parse_finger_reply
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal, SkipTest


class ParseFingerReplyTestCase(unittest.TestCase):

    def _load_file(self, name):
        return load_parse_data_file_patching_continuations(name)

    def test_nonexistant(self):
        self.failUnlessRaises(
            errors.UnknownPlayer,
            parse_finger_reply,
            self._load_file("finger-nonexist.lines")
        )
    def test_empty(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_finger_reply,
            "")
    def test_ugly(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_finger_reply,
            "\nblah")
    def test_gmkramnik(self):
        info = parse_finger_reply(
            self._load_file("finger-gmkramnik.lines"))
        self.failUnlessEqual(
            info,
            FingerInfo(name="GMKramnik",
                 results={
                    GameType("Standard"): ResultStats(
                        wins_count=1, draws_count=0, losses_count=0,
                        rating=PlayerRating(value=2800, rd=Decimal('350.0')), best=None),
                    },
                 plan=['This is the demo account to relay the games of GM Kramnik, Vladimir (RUS) fide id. number = 4101588',
                       'FIDE Elo rating : 2800',
                       'Current World Rank: 4',
                       ]))
    def test_mekk(self):
        info = parse_finger_reply(
            self._load_file("finger-mekk.lines"))
        # TODO: replace assert_dicts_equal with object/namedtuples equiv
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="Mekk",
                results={
                     GameType('Atomic'): ResultStats(best=None, wins_count=23, draws_count=1, losses_count=50, rating=PlayerRating(1525, rd=Decimal('159.2')) ),
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
    def test_mek(self):
        info = parse_finger_reply(
            self._load_file("finger-mek.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(name="Mek",
                 results={
                    GameType('Standard'): ResultStats(rating=PlayerRating(1606, rd=Decimal('350.0')), best=None, wins_count=0, losses_count=1, draws_count=0),
                    },
                 plan=[
                    ]))
    def test_mad(self):
        info = parse_finger_reply(
            self._load_file("finger-mad.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(name="MAd",
                 results={
                     GameType('Blitz'): ResultStats(rating=PlayerRating(1606, rd=Decimal('45.3')), wins_count=10615, losses_count=5217,
                         draws_count=574, best=1722),
                     GameType('Standard'): ResultStats(rating=PlayerRating(1793, rd=Decimal('350.0')), wins_count=35, losses_count=12,
                         draws_count=2, best=None),
                     GameType('Lightning'): ResultStats(rating=PlayerRating(1633, rd=Decimal('350.0')), wins_count=1, losses_count=6,
                         draws_count=0, best=None)},
                 plan=[
                    '''"But I don't want to go among MAd people." Alice remarked "Oh, you can't help that," said the cat: "We are all MAd here, I'm MAd, you're MAd." "How do you know I'm MAd?" said Alice. "You must be." said the cat, "or you wouldn't have come here."''',
                    '''************************************************************************ "Will you tell me something? "Perhaps." "When I dream, sometimes I remember how to fly. You just lift one leg, then you lift the other leg, and you're not standing on anything, and you can fly. And then when I wake up I can't remember how to do it any more." "So?" "So what I want to know is, when I'm asleep, do I really remember how to fly? And forget how when I wake up? Or am I just dreaming I can fly? "When you dream, sometimes you remember. When you wake, you always forget." "But that's not fair..." "No."''',
                    '''************************************************************************* If our game is adjourned I will ask for an abort: since it is a blitz chess game, the possibility that one of the players analyzes the position has to be ruled out. If you insist on playing I'll let you win on time and you'll end up on my noplay. If you refuse to resign when you're lost and I have lot of time I will noplay you too. I don't want to be be bored till I bluder a piece, I'm here to enjoy the game.''',
                    '''************************************************************************* If you know SNOWHITE 7 dwarfs names in your own language please message them to me''',
                    '''************************************************************************* mad@freechess.org MAd was born on Dec 21st 1993''',
                    '''************************************************************************* "Ungluecklich das Land, das Helden noetig hat." (Fortunata la terra che non ha bisogno di eroi)''',
                    '''************************************************************************* MAd is proud to be honourary member of #$%& (Always Right Society of England). MAd is also member of PLO (Punk and Loaded Organization).''',
                    '''************************************************************************* Current BCF: 148''',
                    '''New NMS record 0.000131 - by MAd''',
                    '''************************************************************************** PCA (Pookie Channel Association) president. Message me to join. Members: Seneca, Ovidius, Thanatos, Trixi, Trixi, NOFX, ExGod, knife, MacLoud, Boutros, Westley, TOOTHPICK, jean, RifRaf, Mlausa, Pinocchio, ratemenot, hyjynx, Eeyore (NOW BANNED FROM PCA!), Garion, norpan, Psycho, ARCEE, TheHacker, Jan, Alefith, Tekken, Sheridan, Axel, Chessty, pelicon, seordin, ChessWisdom, AustinPowders, DoctorColossus, PenguinKing, TheGenius, chesswhiz, chessmasterMO, Mackja, munchy''',
                 ]))
    def test_watchbot(self):
        info = parse_finger_reply(
            self._load_file("finger-watchbot.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="WatchBot",
                results=dict(
                ),
                plan=[
                    '''I am a computer bot (automated program). I don't play, I just watch.''',
                    '''My main purpose is to store comments made during the game (whispers/kibitzes) so they can be reviewed by the players after the game. See "http://mekk.waw.pl/mk/watchbot" for details.''',
                    '''.''',
                    '''I handle plenty of commands (in particular you can ask me to send some games via email). Use "tell WatchBot help" or view "http://mekk.waw.pl/mk/watchbot/usage_intro" to learn them.''',
                    '''Or just visit "http://mekk.waw.pl/mk/watchbot" to find, replay, and download the games.''',
                    '''.''',
                    '''This is release c37c7befc1ac, last updated 2011-08-09.''',
                    '''.''',
                    '''I have been written and I am run by Mekk ("finger Mekk").''',
                    '''If I am down or misbehave, my author may be unaware, message Mekk or (preferably) email WatchBotSupport@mekk.waw.pl to report the problem''',
                ]))
    def test_guest(self):
        info = parse_finger_reply(
            self._load_file("finger-guest.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="GuestVNCT",
                results=dict(
                ),
                plan=[
                ]))
    def test_relay(self):
        info = parse_finger_reply(
            self._load_file("finger-relay.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="relay",
                results=dict(
                ),
                plan=[
                    '''use "tell relay help commands" to find more about relay commands''',
                    '''use "tell relay observe" to automatically observe the highest rated relayed game''',
                    '''use "tell relay gtm <game_number> <move>" (eg tell relay gtm 54 Nf3) to guess the next move''',
                    '''I will keep the score and you can check how people are doing with "tell relay gtmrank".''',
                    '''Accepted notation is reduced algebraic, thus e4 works but e2e4 does not. Similarly Nxe5 works but NxN does not. To guess castling use o-o or o-o-o but not e1g1.''',
                    '''Use "tell relay notify" if you want to be told what tournaments are being relayed when you login''',
                    '''http://www.freechess.org/Events/Relay/ and http://www.freechess.org/Events/Relay/2010 to see what tournaments are or will be relayed''',
                ]))

