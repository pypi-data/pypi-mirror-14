# -*- coding: utf-8 -*-

from twisted.trial import unittest

import datetime

from mekk.fics.parsing import info_parser
from mekk.fics.constants import block_codes
from mekk.fics.datatypes.player import PlayerName, FingerInfo, ResultStats, PlayerRating
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.game_clock import GameClock
from mekk.fics.datatypes.game_info import GameReference, ExaminedGame, SetupGame, PlayedGame, GameSpec, GameInfo, ExaminedGameExt
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.generic import GenericText
from mekk.fics.datatypes.color import Color, BLACK, WHITE
from mekk.fics.datatypes.notifications import SeekRef, GameJoinInfo, Seek
from mekk.fics.test_utils import (
    load_tstdata_file, assert_dicts_equal, assert_tables_equal, SkipTest)
from mekk.fics.test_utils.internal import load_parse_data_file


class ParseFicsLineTestCase(unittest.TestCase):

    def testTell(self):
        (w,d) = info_parser.parse_fics_line("Johny tells you: blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')

    def testTellTD(self):
        (w,d) = info_parser.parse_fics_line("Mamer(TD) tells you: bleh bleh")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Mamer'))
        self.failUnlessEqual(d.text, 'bleh bleh')

    def testTellSRTM(self):
        (w,d) = info_parser.parse_fics_line("Johny(SR)(TM) tells you: blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')

    def testDoubleTell(self):
        # see #2
        (w,d) = info_parser.parse_fics_line("Johny tells you: tell WatchBot blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')

    def testChannelTell(self):
        (w,d) = info_parser.parse_fics_line("playerbis(106): ble ble ble")
        self.failUnlessEqual(w, 'channel_tell')
        self.failUnlessEqual(d.player, PlayerName('playerbis'))
        self.failUnlessEqual(d.channel, 106)
        self.failUnlessEqual(d.text, 'ble ble ble')

    def testChannelTellGuest(self):
        (w,d) = info_parser.parse_fics_line("GuestKKLX(U)(4): your extremely lucky i just slipped my piece there")
        self.failUnlessEqual(w, 'channel_tell')
        self.failUnlessEqual(d.player, PlayerName('GuestKKLX'))
        self.failUnlessEqual(d.channel, 4)
        self.failUnlessEqual(d.text, 'your extremely lucky i just slipped my piece there')

    def testItShout(self):
        (w,d) = info_parser.parse_fics_line("--> MAd> (ics-auto-salutes 'Mekk)")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('Mad'))
        self.failUnlessEqual(d.text, "MAd> (ics-auto-salutes 'Mekk)")

    def testItShout2(self):
        (w,d) = info_parser.parse_fics_line(
            "--> botchvinik Announcement!!!!  /\/\/\/\/\/\  RJJ /\/\/\/\/\/\ has arrived! !BCS->(gong)")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('botchvinik'))
        self.failUnlessEqual(d.text, "botchvinik Announcement!!!!  /\/\/\/\/\/\  RJJ /\/\/\/\/\/\ has arrived! !BCS->(gong)")

    def testItShout3(self):
        (w,d) = info_parser.parse_fics_line("--> Mekk manually salutes MAd.")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('Mekk'))
        self.failUnlessEqual(d.text, "Mekk manually salutes MAd.")

    def testCShout(self):
        (w,d) = info_parser.parse_fics_line("TScheduleBot(TD) c-shouts: Thursday's Scheduled 15 0 SS scheduled tournament. See 'finger TScheduleBot' for more information about this and other scheduled events on FICS.")
        self.failUnlessEqual(w, 'cshout')
        self.failUnlessEqual(d.player, PlayerName('TScheduleBot'))
        self.failUnlessEqual(d.text, "Thursday's Scheduled 15 0 SS scheduled tournament. See 'finger TScheduleBot' for more information about this and other scheduled events on FICS.")

    def testShout(self):
        (w,d) = info_parser.parse_fics_line("Georg(SR)(TM) shouts: To be or not to be")
        self.failUnlessEqual(w, 'shout')
        self.failUnlessEqual(d.player, PlayerName('Georg'))
        self.failUnlessEqual(d.text, "To be or not to be")

    def testStyle12(self):
        (w,d) = info_parser.parse_fics_line("<12> -----r-- --r-p-kp ----Qnp- ----p--- -------- -----PP- P-q---BP ---R-R-K B -1 0 0 0 0 0 164 CamyC android 0 3 0 26 26 112 107 24 Q/a6-e6 (0:01) Qxe6 0 1 215")
        self.failUnlessEqual(w, 'game_move')
        s12 = d.style12
        self.failUnless( isinstance(s12, style12.Style12) )
        #self.failUnlessEqual( s12.FEN(),

    def testQtellTShout1(self):
        (w, d) = info_parser.parse_fics_line(':AGree(TM) t-shouts: Come on! 1 more player for 3 0 tourney and we start: "mam j 24"')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, 'AGree(TM) t-shouts: Come on! 1 more player for 3 0 tourney and we start: "mam j 24"')
        # TODO: think about recognizing this type of qtells

    def testQtellTShout2(self):
        (w, d) = info_parser.parse_fics_line(':mamer(TD) t-shouts: 1 0 r DRR tourney: "tell mamer JoinTourney 19" to join.')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, 'mamer(TD) t-shouts: 1 0 r DRR tourney: "tell mamer JoinTourney 19" to join.')

    def testQtellNormal(self):
        (w, d) = info_parser.parse_fics_line(':Blah blah blah')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, "Blah blah blah")

    def testCompressedMove(self):
        # TODO: more examples of http://www.freechess.org/Help/HelpFiles/iv_compressmove.html
        (w,d) = info_parser.parse_fics_line("<d1> 2 64 Rxc2 e2c2p 1200 203800")
        self.failUnlessEqual(w, 'compressed_move')
        self.failUnlessEqual(d.game_no, 2)
        self.failUnlessEqual(d.half_moves_count, 64)
        self.failUnlessEqual(d.algebraic, 'Rxc2')
        self.failUnlessEqual(d.time_taken, datetime.timedelta(microseconds=1200*1000))
        self.failUnlessEqual(d.time_left, datetime.timedelta(microseconds=203800*1000))
        # TODO: rozpakowac smith move (to jest czteroliterowe skąd-dokąd a potem
        # - opcjonalna dodatkowa literka: pnbrqkEcC (pnbrqk - zbito podaną bierkę,
        #    E - zbito en-passant, c - krótka roszada, C - długa roszada)
        # - opcjonalna literka "promoted to" ( NBRQ)
        # patrz https://www.chessclub.com/chessviewer/smith.html
        self.failUnlessEqual(d.smith, 'e2c2p')
        #self.failUnlessEqual(d.src_square, 'e2')
        #self.failUnlessEqual(d.dst_square, 'c2')
        #self.failUnlessEqual(d.captured, Piece(color=Color('white'), name='pawn'))
        #self.failUnlessEqual(d.en_passant, False)
        #self.failUnlessEqual(d.castling, None)
        # TODO: testy z różnymi smithami

    def testGameStartedIvGameInfo(self):
        (w,d) = info_parser.parse_fics_line('<g1> 1 p=0 t=blitz r=1 u=1,1 it=5,6 i=8,9 pt=0 rt=1586E,2100  ts=1,0')
        # TODO: name (it shows up when game starts or is observed)
        self.failUnlessEqual(w, 'game_joined') # TODO: or maybe game_started_iv ???
        self.failUnlessIsInstance(d, GameJoinInfo)
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        # TODO
        #self.failUnlessEqual(d.white_registered, True)
        #self.failUnlessEqual(d.black_registered, True)
        # TODO
        #self.failUnlessEqual(d.white_clock, GameClock(5,8))
        #self.failUnlessEqual(d.black_clock, GameClock(6,9))
        # TODO
        #self.failUnlessEqual(d.partner_game_no, None)
        self.failUnlessEqual(d.white_rating, 1586)
        self.failUnlessEqual(d.black_rating, 2100)
        # TODO
        #self.failUnlessEqual(d.white_timeseal, True)
        #self.failUnlessEqual(d.black_timeseal, False)

    def testWhisper(self):
        (w,d) = info_parser.parse_fics_line("John(1740)[90] whispers: I like white")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 90)
        self.failUnlessEqual(d.player, PlayerName('John'))
        self.failUnlessEqual(d.rating_value, 1740)
        self.failUnlessEqual(d.text, 'I like white')
        self.failUnlessEqual(d.method, 'whispers')
    def testKibitz(self):
        (w,d) = info_parser.parse_fics_line("John(1740)[90] kibitzes: I like white")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 90)
        self.failUnlessEqual(d.player, PlayerName('John'))
        self.failUnlessEqual(d.rating_value, 1740)
        self.failUnlessEqual(d.text, 'I like white')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testKibitzShortRating(self):
        # Z watchbotowych przeżyć
        (w,d) = info_parser.parse_fics_line("MiloBot(C)( 958)[235] whispers: Hello from Crafty v22.7 !")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 235)
        self.failUnlessEqual(d.player, PlayerName('MiloBot'))
        self.failUnlessEqual(d.rating_value, 958)
        self.failUnlessEqual(d.text, 'Hello from Crafty v22.7 !')
        self.failUnlessEqual(d.method, 'whispers')
        (w,d) = info_parser.parse_fics_line("MiloBot(C)( 958)[235] kibitzes: mated in 1 moves.")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 235)
        self.failUnlessEqual(d.player, PlayerName('MiloBot'))
        self.failUnlessEqual(d.rating_value, 958)
        self.failUnlessEqual(d.text, 'mated in 1 moves.')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testWhisper2(self):
        (w,d) = info_parser.parse_fics_line("Goober(C)(2399)[185] kibitzes: Hello from Crafty v19.19! (2 cpus)")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 185)
        self.failUnlessEqual(d.player, PlayerName('Goober'))
        self.failUnlessEqual(d.rating_value, 2399)
        self.failUnlessEqual(d.text, 'Hello from Crafty v19.19! (2 cpus)')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testKibitz2(self):
        (w,d) = info_parser.parse_fics_line("Mainflame(C)(2322)[185] whispers: d10 +0.27 c3 Be7 dxe5 Nxe4 Nbd2 Nxd2 Bxd2 O-O Bd3 Nc6 O-O d5 egtb: 0 time: 18.70 nps: 132397")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 185)
        self.failUnlessEqual(d.player, PlayerName('Mainflame'))
        self.failUnlessEqual(d.rating_value, 2322)
        self.failUnlessEqual(d.text, 'd10 +0.27 c3 Be7 dxe5 Nxe4 Nbd2 Nxd2 Bxd2 O-O Bd3 Nc6 O-O d5 egtb: 0 time: 18.70 nps: 132397')
        self.failUnlessEqual(d.method, 'whispers')

    def test_announcement(self):
        (w,d) = info_parser.parse_fics_line('    **ANNOUNCEMENT** from relay: FICS is relaying the XLI Rilton Cup - Last Round. To find more about Relay type "tell relay help"')
        self.failUnlessEqual(w, 'announcement')
        self.failUnlessEqual(d.player, PlayerName('relay'))
        self.failUnlessEqual(d.text, 'FICS is relaying the XLI Rilton Cup - Last Round. To find more about Relay type "tell relay help"')

    def testUserConnected(self):
        (w,d) = info_parser.parse_fics_line('[playerbis has connected.]')
        self.failUnlessEqual(w, 'user_connected')
        self.failUnlessEqual(d, PlayerName('playerbis'))

    def testUserDisconnected(self):
        (w,d) = info_parser.parse_fics_line('[playerbis has disconnected.]')
        self.failUnlessEqual(w, 'user_disconnected')
        self.failUnlessEqual(d, PlayerName('playerbis'))

    def testGameStarted(self):
        (w,d) = info_parser.parse_fics_line('{Game 1 (playerbis vs. root) Creating rated standard match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('playerbis'))
        self.failUnlessEqual(d.black_name, PlayerName('root'))
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))

    def testGameStartedUnrated(self):
        (w,d) = info_parser.parse_fics_line('{Game 142 (GuestFQJN vs. GuestCFVZ) Creating unrated blitz match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('GuestFQJN'))
        self.failUnlessEqual(d.black_name, PlayerName('GuestCFVZ'))
        self.failUnlessEqual(d.game_no, 142)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
    def testGameStartedBug(self):
        (w,d) = info_parser.parse_fics_line('{Game 155 (spgs vs. Miklo) Creating rated bughouse match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('spgs'))
        self.failUnlessEqual(d.black_name, PlayerName('Miklo'))
        self.failUnlessEqual(d.game_no, 155)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('bughouse'))
    def testGameStartedSuicide(self):
        (w,d) = info_parser.parse_fics_line('{Game 32 (Chussi vs. SquibCakes) Creating rated suicide match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('Chussi'))
        self.failUnlessEqual(d.black_name, PlayerName('SquibCakes'))
        self.failUnlessEqual(d.game_no, 32)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
    def testGameStartedWild4(self):
        (w,d) = info_parser.parse_fics_line('{Game 165 (ThawCY vs. ChessCracker) Creating rated wild/4 match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('ThawCY'))
        self.failUnlessEqual(d.black_name, PlayerName('ChessCracker'))
        self.failUnlessEqual(d.game_no, 165)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/4'))
    def testGameStartedCont(self):
        (w,d) = info_parser.parse_fics_line('{Game 166 (xufei vs. chessactuary) Continuing rated blitz match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('xufei'))
        self.failUnlessEqual(d.black_name, PlayerName('chessactuary'))
        self.failUnlessEqual(d.game_no, 166)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
    def testGameFinishedDraw(self):
        (w,d) = info_parser.parse_fics_line('{Game 164 (CamyC vs. android) Neither player has mating material} 1/2-1/2')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 164)
        self.failUnlessEqual(d.white_name, PlayerName('CamyC'))
        self.failUnlessEqual(d.black_name, PlayerName('android'))
        self.failUnlessEqual(d.result, '1/2-1/2')
        self.failUnlessEqual(d.result_desc, 'Neither player has mating material')
        self.failIf(d.early_abort)
    def testGameFinishedForfeit(self):
        (w,d) = info_parser.parse_fics_line('{Game 173 (android vs. CamyC) CamyC forfeits on time} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 173)
        self.failUnlessEqual(d.white_name, PlayerName('android'))
        self.failUnlessEqual(d.black_name, PlayerName('CamyC'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'CamyC forfeits on time')
        self.failIf(d.early_abort)
    def testGameFinishedMate(self):
        (w,d) = info_parser.parse_fics_line('{Game 62 (Rasquinho vs. farwest) Rasquinho checkmated} 0-1')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 62)
        self.failUnlessEqual(d.white_name, PlayerName('Rasquinho'))
        self.failUnlessEqual(d.black_name, PlayerName('farwest'))
        self.failUnlessEqual(d.result, '0-1')
        self.failUnlessEqual(d.result_desc, 'Rasquinho checkmated')
        self.failIf(d.early_abort)
    def testGameFinishedResign(self):
        (w,d) = info_parser.parse_fics_line('{Game 126 (SquibCakes vs. Chussi) Chussi resigns} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 126)
        self.failUnlessEqual(d.white_name, PlayerName('SquibCakes'))
        self.failUnlessEqual(d.black_name, PlayerName('Chussi'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'Chussi resigns')
        self.failIf(d.early_abort)
    def testGameFinishedAdjourn(self):
        (w,d) = info_parser.parse_fics_line('{Game 74 (Christen vs. Rajan) Christen lost connection; game adjourned} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 74)
        self.failUnlessEqual(d.white_name, PlayerName('Christen'))
        self.failUnlessEqual(d.black_name, PlayerName('Rajan'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Christen lost connection; game adjourned')
        self.failIf(d.early_abort)
    def testGameFinishedAbort1(self):
        (w,d) = info_parser.parse_fics_line('{Game 39 (Sillopsism vs. sparpas) Game aborted on move 1} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.white_name, PlayerName('Sillopsism'))
        self.failUnlessEqual(d.black_name, PlayerName('sparpas'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game aborted on move 1')
        self.failUnless(d.early_abort)
    def testGameFinishedCourtesy(self):
        (w,d) = info_parser.parse_fics_line('{Game 78 (msparrow vs. Belofte) Game courtesyadjourned by msparrow} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 78)
        self.failUnlessEqual(d.white_name, PlayerName('msparrow'))
        self.failUnlessEqual(d.black_name, PlayerName('Belofte'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game courtesyadjourned by msparrow')
        self.failIf(d.early_abort)
    def testGameFinishedForfTime2(self):
        (w,d) = info_parser.parse_fics_line('{Game 143 (samthefam vs. NemSiMing) samthefam forfeits on time} 0-1')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 143)
        self.failUnlessEqual(d.white_name, PlayerName('samthefam'))
        self.failUnlessEqual(d.black_name, PlayerName('NemSiMing'))
        self.failUnlessEqual(d.result, '0-1')
        self.failUnlessEqual(d.result_desc, 'samthefam forfeits on time')
        self.failIf(d.early_abort)
    def testGameFinishedAbort1_1(self):
        (w,d) = info_parser.parse_fics_line('{Game 52 (bububfo vs. Friscopat) Game aborted on move 1} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_name, PlayerName('bububfo'))
        self.failUnlessEqual(d.black_name, PlayerName('Friscopat'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game aborted on move 1')
        self.failUnless(d.early_abort)
    def testGameFinishedStalemate(self):
        (w,d) = info_parser.parse_fics_line('{Game 192 (electricrook vs. dalf) Game drawn by stalemate} 1/2-1/2')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 192)
        self.failUnlessEqual(d.white_name, PlayerName('electricrook'))
        self.failUnlessEqual(d.black_name, PlayerName('dalf'))
        self.failUnlessEqual(d.result_desc, 'Game drawn by stalemate')
        self.failUnlessEqual(d.result, '1/2-1/2')
        self.failIf(d.early_abort)
    def testGameFinishedAbortTooFew(self):
        (w,d) = info_parser.parse_fics_line('{Game 52 (bububfo vs. Hono) Hono lost connection and too few moves; game aborted} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_name, PlayerName('bububfo'))
        self.failUnlessEqual(d.black_name, PlayerName('Hono'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Hono lost connection and too few moves; game aborted')
        self.failUnless(d.early_abort)
    def testGameFinishedAdjudicated(self):
        (w,d) = info_parser.parse_fics_line('{Game 47 (MAd vs. pgv) MAd wins by adjudication} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 47)
        self.failUnlessEqual(d.white_name, PlayerName('MAd'))
        self.failUnlessEqual(d.black_name, PlayerName('pgv'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'MAd wins by adjudication')
        self.failIf(d.early_abort)
        # TODO: flag for adjudication?

    def testObservingFinished(self):
        (w,d) = info_parser.parse_fics_line('Removing game 138 from observation list.')
        self.failUnlessEqual(w, 'observing_finished')
        self.failUnlessEqual(d.game_no, 138)
    def testGameNoteDrawOffer(self):
        (w,d) = info_parser.parse_fics_line('Game 39: Berke offers a draw.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.note, 'Berke offers a draw.')
    def testGameNoteDrawDecline(self):
        (w,d) = info_parser.parse_fics_line('Game 39: radioegg declines the draw request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.note, 'radioegg declines the draw request.')
    def testGameNotePauseReq(self):
        (w,d) = info_parser.parse_fics_line('Game 4: wivawo requests to pause the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'wivawo requests to pause the game.')
    def testGameNotePauseAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Kobac accepts the pause request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Kobac accepts the pause request.')
    def testGameNoteClockPaus(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Game clock paused.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Game clock paused.')
    def testGameNoteUnpauseReq(self):
        (w,d) = info_parser.parse_fics_line('Game 4: wivawo requests to unpause the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'wivawo requests to unpause the game.')
    def testGameNoteUnpauseAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Kobac accepts the unpause request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Kobac accepts the unpause request.')
    def testGameNoteClockResum(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Game clock resumed.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Game clock resumed.')
    def testGameNoteTakebackReq(self):
        (w,d) = info_parser.parse_fics_line('Game 97: rahulchess requests to take back 1 half move(s).')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 97)
        self.failUnlessEqual(d.note, 'rahulchess requests to take back 1 half move(s).')
    def testGameNoteTakebackAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 97: Memler accepts the takeback request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 97)
        self.failUnlessEqual(d.note, 'Memler accepts the takeback request.')
    def testGameNoteTakebackDecl(self):
        (w,d) = info_parser.parse_fics_line('Game 290: Divljak declines the takeback request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 290)
        self.failUnlessEqual(d.note, 'Divljak declines the takeback request.')
    def testGameNoteAbortReq(self):
        (w,d) = info_parser.parse_fics_line('Game 51: daneg requests to abort the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.note, 'daneg requests to abort the game.')
    def testGameNoteAbortDecl(self):
        (w,d) = info_parser.parse_fics_line('Game 51: kmhaswad declines the abort request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.note, 'kmhaswad declines the abort request.')
    def testGameNoteDrawAccept(self):
        (w,d) = info_parser.parse_fics_line('Game 128: dcwarren accepts the draw request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 128)
        self.failUnlessEqual(d.note, 'dcwarren accepts the draw request.')
    def testAnnouncement(self):
        (w,d) = info_parser.parse_fics_line('    **ANNOUNCEMENT** from relay: FICS is relaying the Swedish Championship. To find out which games are being relayed type "tell relay listgames", to observe the top n games type "tell relay observe n". Read news 1153 for the instructions on the "guess the move" no prize competition.')
        self.failUnlessEqual(w, 'announcement')
        self.failUnlessEqual(d.player, PlayerName('relay'))
        self.failUnlessEqual(d.text, 'FICS is relaying the Swedish Championship. To find out which games are being relayed type "tell relay listgames", to observe the top n games type "tell relay observe n". Read news 1153 for the instructions on the "guess the move" no prize competition.')
    def testSeekLineWildFr(self):
        (w,d) = info_parser.parse_fics_line('GuestBCYW (++++) seeking 5 0 unrated wild/fr ("play 36" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.seek_no, 36)
        self.failUnlessEqual(d.player, PlayerName('GuestBCYW'))
        self.failUnlessEqual(d.player_rating_value, 0)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/fr'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,0))
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, False)
    def testSeekLineGuestColor(self):
        (w,d) = info_parser.parse_fics_line('xxxccc (++++) seeking 5 0 unrated blitz [white] ("play 131" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.seek_no, 131)
        self.failUnlessEqual(d.player, PlayerName('xxxccc'))
        self.failUnlessEqual(d.player_rating_value, 0)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,0))
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.color, Color('white'))
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, False)
    def testSeekLineRegisteredManualNoColor(self):
        (w,d) = info_parser.parse_fics_line('Pieraleco (1531) seeking 2 30 rated blitz m ("play 42" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.player, PlayerName('Pieraleco'))
        self.failUnlessEqual(d.player_rating_value, 1531)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2,30))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        # TODO: private?
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.seek_no, 42)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, True)
    def test_seek_line_admin_manual_formula(self):
        (w,d) = info_parser.parse_fics_line('Farad(SR)(TD) (1231E) seeking 1 2 rated suicide m ("play 42" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.player, PlayerName('Farad'))
        self.failUnlessEqual(d.player_rating_value, 1231)
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(1,2))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.seek_no, 42)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, True)
    # TODO: manual, formula, ranking, nawiaski w imieniu
    def testManySeeks(self):
        seek_lines = load_parse_data_file("seeks.lines").split("\n")
        private_count = 0
        manual_count = 0
        color_count = { WHITE: 0, BLACK: 0 }
        rated_count = { True: 0, False: 0 }
        for line in seek_lines:
            if not line.strip():
                continue
            (w,d) = info_parser.parse_fics_line(line)
            self.failUnlessEqual(w, "seek", "Failed to parse seek: " + line)
            self.failUnlessIsInstance(d.seek_no, int)
            self.failUnlessIsInstance(d.player, PlayerName)
            self.failUnlessIsInstance(d.player_rating_value, int)
            self.failUnlessIsInstance(d.is_manual, bool)
            self.failUnlessIsInstance(d.using_formula, bool)
            if d.color is not None:
                self.failUnlessIsInstance(d.color, Color)
            self.failUnlessIsInstance(d.game_spec, GameSpec)
            self.failUnlessIsInstance(d.game_spec.game_type, GameType)
            self.failUnlessIsInstance(d.game_spec.is_rated, bool)
            self.failUnlessIsInstance(d.game_spec.is_private, bool)
            self.failUnlessIsInstance(d.game_spec.clock, GameClock)
            if d.game_spec.is_private:
                private_count += 1
            if d.is_manual:
                manual_count += 1
            if d.color is not None:
                color_count[d.color] += 1
            rated_count[d.game_spec.is_rated] += 1
        self.failIfEqual(manual_count, 0, "No manual seek spotted")
        self.failIfEqual(color_count[WHITE], 0, "No white seek spotted")
        self.failIfEqual(color_count[BLACK], 0, "No black seek spotted")
        self.failIfEqual(rated_count[True], 0, "No rated seek spotted")
        self.failIfEqual(rated_count[False], 0, "No unrated seek spotted")
        self.failUnlessEqual(private_count, 0, "Some private seek spotted, should not happen")

        # TODO: check some of those lines
    def testRemovedSeeksOne(self):
        (w,d) = info_parser.parse_fics_line('Ads removed: 37')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=37) ] )
    def testRemovedSeeksMore(self):
        (w,d) = info_parser.parse_fics_line('Ads removed: 22 1 119')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=x) for x in [22, 1, 119] ] )
    def testSeekIvSeekInfo1(self):
        (w,d) = info_parser.parse_fics_line('<s> 8 w=visar ti=02 rt=2194  t=4 i=0 r=r tp=suicide c=? rr=0-9999 a=t f=t')
        self.failUnlessEqual(w, "seek")
        self.failUnlessEqual(d.seek_no, 8)
        self.failUnlessEqual(d.player, PlayerName('visar'))
        # TODO: ti (titles). This is hex number with or-ed 0x1 - unregistered 0x2 - computer 0x4 - GM 0x8 - IM
        # 0x10 - FM 0x20 - WGM 0x40 - WIM 0x80 - WFM
        self.failUnlessEqual(d.player_rating_value, 2194)
        self.failUnlessEqual(d.game_spec.clock, GameClock(4,0))
        self.failUnlessEqual(d.game_spec.is_rated, True) # r=r rated, r=u unrated
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.color, None)   # ?, W, B
        # TODO self.failUnlessEqual(d.rating_min, 0)
        # TODO self.failUnlessEqual(d.rating_max, 9999)
        self.failUnlessEqual(d.is_manual, False) # a=t automatic, a=f manual
        self.failUnlessEqual(d.using_formula, True)
    def testSeekIvSeekInfo2(self):
        (w,d) = info_parser.parse_fics_line('<s> 12 w=saeph ti=00 rt=1407  t=1 i=0 r=r tp=lightning c=? rr=0-9999 a=t f=f  ')
        self.failUnlessEqual(w, "seek")
        # TODO: add fields
    def testSeekIvSeekInfo3(self):
        (w,d) = info_parser.parse_fics_line('<sn> 82 w=Mekk ti=00 rt=1341  t=5 i=2 r=r tp=blitz c=? rr=1401-1403 a=t f=f')
        self.failUnlessEqual(w, "seek")  # TODO: maybe seek own? what is <sn>?
        # TODO: add fields
    def testSeeksClearedIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sc>')
        self.failUnlessEqual(w, 'seeks_cleared')
        self.failUnlessEqual(d, GenericText('<sc>'))
    def testRemovedSeeksOneIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sr> 37')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=37) ])
    def testRemovedSeeksMoreIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sr> 22 1 119')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(no) for no in [22, 1, 119] ] )
    def testOffersIvPendinfoOfferReceived(self):
        # http://www.freechess.org/Help/HelpFiles/iv_pendinfo.html
        # <pf> index w=name_from t=offer_type p=params
        # TODO: grab sample data and make test
        raise SkipTest
    def testOffersIvPendinfoOfferSent(self):
        # http://www.freechess.org/Help/HelpFiles/iv_pendinfo.html
        #(w,d) = parser.parse_fics_line('<pt> index w=name_to t=offer_type p=params')
        # TODO: grab sample data and make test
        raise SkipTest
    def testOffersIvPendinfoOfferDeclined(self):
        # <pr> index
        # what's that? - offer accepted/declined/withdrawn/removed
        # TODO: grab sample data and make test
        raise SkipTest
    def testAutoLogout(self):
        (w,d) = info_parser.parse_fics_line(
            '**** Auto-logout because you were idle more than 60 minutes. ****')
        #print w
        #print d
        self.failUnlessEqual(w, 'auto_logout')
        self.failUnlessEqual(d, GenericText("Auto-logout because you were idle more than 60 minutes."))

    def testIgnores(self):
        # TODO: move those to reply parsing and treat as they should be treated
        not_used_lines = [
          'Style 12 set.',
          'You are no longer receiving match requests.',
          'Highlight is off.',
          'You will not hear shouts.',
          'You will not hear cshouts.',
          'You will now hear kibitzes.',
          'You will now hear tells from unregistered users.',
          'You will now hear game results.',
          'You will now hear logins/logouts.',
          'Plan variable 1 changed to \'I am a bot\'',
          'Width set to 1024.',
          'startpos set.',
          'graph set.',
          'You will not auto unobserve.',
          'You will not see seek ads',
          ]
        lines = [
            'block set.',
            '  ',
            "\r   \n",
        ]
        for x in lines:
            t = info_parser.parse_fics_line(x)
            self.failUnless(t, "Should ignore: %s" %x)
            self.failUnlessEqual(t[0], 'ignore', "Should ignore: %s" % x)
