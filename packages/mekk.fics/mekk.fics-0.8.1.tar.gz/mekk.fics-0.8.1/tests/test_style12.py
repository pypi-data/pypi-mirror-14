# -*- coding: utf-8 -*-

"""
Element testów do modułów followbota
"""

#import unittest
from twisted.trial import unittest
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.color import WHITE, BLACK
from mekk.fics.datatypes.player import PlayerName

class SameMoveTestCase(unittest.TestCase):
    def testEqual(self):
        s1 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        s2 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        s3 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1204 1205 1 P/d2-d4 (0:00) d4 0 0 0")
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s2), True)
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s3), True)
    def testDifferent(self):
        s1 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 295 meandeye marcosvzla 0 15 0 39 39 900 900 1 none (0:00) none 0 0 0")
        s2 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 261 GuestZSCN forKed 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s2), False)
    def testDifferentPlayers(self):
        s1 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 261 forKed GuestZSCN 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")
        s2 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 261 GuestZSCN forKed 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")
        s3 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 261 forKed Bejin 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s2), False)
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s3), False)
        self.failUnlessEqual(
            style12.is_the_same_move(s2, s3), False)
    def testDifferentGame(self):
        s1 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        s2 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 177 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s2), False)
    def testDifferentSimilar(self):
        s1 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        s2 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 2 P/d3-d4 (0:00) d4 0 0 0")
        s3 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:02) d4 0 0 0")
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s2), False)
        self.failUnlessEqual(
            style12.is_the_same_move(s1, s3), False)
        self.failUnlessEqual(
            style12.is_the_same_move(s2, s3), False)

class Style12TestCase(unittest.TestCase):
    def setUp(self):
        self.texts = (
            "<12> rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback -3 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0",
            "<12> rnbqkbnr ppp-pppp -------- ---p---- ---P---- -------- PPP-PPPP RNBQKBNR W 3 1 1 1 1 0 175 yacc dontrookback -2 20 20 39 39 1200 1200 2 P/d7-d5 (0:00) d5 0 1 0",
            "rnbqkbnr ppp-pppp -------- ---p---- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 175 yacc dontrookback 2 20 20 39 39 1220 1200 2 P/c2-c4 (0:00) c4 0 1 0",
            "r-----k- ------B- p--pN--- P----N-p ----n--- -------- -P---P-P n-----K- W 7 0 0 0 0 0 41 SuperEarth dreserto -1 15 0 13 14 249 354 29 P/h7-h5 (1:08) h5 0 1 210",
            "r--q-rk- pp--ppbp ---p-np- n--b---- --P-P--- P--Q-N-P -P--BPP- R-B-K--R W -1 1 1 0 0 0 458 getupan Aizenmyoo 1 15 0 35 38 849 771 12 B/e6-d5 (0:26) Bxd5 0 1 649",
            "r----rk- pp-q-pp- --nbpn-p ---p---- ---N--b- -QP--NP- PP--PPBP R-B-R-K- W -1 0 0 0 0 4 352 StiliDimitrov hobochess 0 15 0 38 38 777 652 12 o-o (0:11) O-O 0 1 425",
            "<12> q------r ---nkppp p---b--- -p--p--- ----n--- -N------ PPP-QPPP --KR-B-R B -1 0 0 0 0 1 283 ADTI titancrasher 0 25 0 31 29 1053 1355 16 o-o-o (3:47) O-O-O 0 1 176",
            "-----R-Q ----k--- -------- -------- -------- ---p---- ---K---- ---b---- B -1 0 0 0 0 0 92 ArrogantFrenchman Pappyglue 0 15 0 14 4 14 15 83 P/h7-h8=Q (0:01) h8=Q 0 1 20",
            "-R------ k------- -Q------ -------- -------- ---p---- --bK---- -------- B -1 0 0 0 0 10 92 ArrogantFrenchman Pappyglue 0 15 0 14 4 12 0 88 Q/d6-b6 (0:00) Qb6# 0 1 62",
            "rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 385 mackofelso Teuton 0 5 20 39 39 300 300 1 none (0:00) none 0 0 0",
            )
        self.s12 = tuple(style12.Style12(x) for x in self.texts)

    def test_game_no(self):
        for s12obj, expval in zip(
            self.s12,
            [ 175, 175, 175, 41, 458, 352,283, 92, 92, 385 ]):
            self.failUnlessEqual(s12obj.game_no, expval)

    def test_game_no_str(self):
        for s12obj, expval in zip(
            self.s12,
            [ "175", "175", "175", "41", "458",
              "352", "283", "92", "92", "385" ]):
            self.failUnlessEqual(str(s12obj.game_no), expval)

    def test_white(self):
        for s12obj, expval in zip(
            self.s12,
            ["yacc", "yacc", "yacc", "SuperEarth", "getupan",
             "StiliDimitrov", "ADTI", "ArrogantFrenchman", "ArrogantFrenchman", "mackofelso" ]):
            self.failUnlessEqual(s12obj.white, PlayerName(expval))
    def test_black(self):
        for s12obj, expval in zip(
            self.s12,
            ["dontrookback", "dontrookback", "dontrookback", "dreserto", "Aizenmyoo",
             "hobochess", "titancrasher", "Pappyglue", "Pappyglue", "Teuton" ]):
            self.failUnlessEqual(s12obj.black, PlayerName(expval))
    def test_clock_base_min(self):
        for s12obj, expval in zip(
            self.s12,
            [ 20, 20, 20, 15,15,
              15, 25, 15, 15, 5 ]):
            self.failUnlessEqual(s12obj.clock.base_min, expval)
    def test_clock_base_sec(self):
        for s12obj, expval in zip(
            self.s12,
            [ 20*60, 20*60, 20*60, 15*60,15*60,
              15*60, 25*60, 15*60, 15*60, 5*60 ]):
            self.failUnlessEqual(s12obj.clock.base_sec, expval)
    def test_clock_inc (self):
        for s12obj, expval in zip(
            self.s12,
            [ 20, 20, 20, 0, 0,
              0, 0, 0, 0, 20 ]):
            self.failUnlessEqual(s12obj.clock.inc_sec, expval)
    def test_clock_text(self):
        for s12obj, expval in zip(
            self.s12,
            [ "20+20", "20+20", "20+20", "15+0", "15+0", 
              "15+0", "25+0", "15+0", "15+0", "5+20" ]):
            self.failUnlessEqual(s12obj.clock.text, expval)
    def test_side_to_move(self):
        for s12obj, expval in zip(
            self.s12,
            [ "B", "W", "B", "W", "W",
              "W", "B", "B", "B", "W" ]):
            self.failUnlessEqual(s12obj.side_to_move, expval)
    def test_to_move(self):
        for s12obj, expval in zip(
            self.s12,
            [ BLACK, WHITE, BLACK, WHITE, WHITE,
              WHITE, BLACK, BLACK, BLACK, WHITE ]):
            self.failUnlessEqual(s12obj.to_move, expval)
    # def test_is_white_to_move(self):
    #     for s12obj, expval in zip(
    #         self.s12,
    #         [ False, True, False, True, True,
    #           True, False, False, False, True ]):
    #         self.failUnlessEqual(s12obj.is_white_to_move, expval)
    # def test_is_black_to_move(self):
    #     for s12obj, expval in zip(
    #         self.s12,
    #         [ True, False, True, False, False,
    #           False, True, True, True, False ]):
    #         self.failUnlessEqual(s12obj.is_black_to_move, expval)
    # def test_is_last_white_move(self):
    #     for s12obj, expval in zip(
    #         self.s12,
    #         [ True, False, True, False, False,
    #           False, True, True, True, False ]):
    #         self.failUnlessEqual(s12obj.is_last_white_move, expval)
    # def test_is_last_black_move(self):
    #     for s12obj, expval in zip(
    #         self.s12,
    #         [ False, True, False, True, True,
    #           True, False, False, False, True ]):
    #        self.failUnlessEqual(s12obj.is_last_black_move, expval)
    def test_after_double_push(self):
        for s12obj, expval in zip(
            self.s12,
            [ "d", "d", "c", "h", None,
              None, None, None, None, None ]):
            self.failUnlessEqual(s12obj.after_double_push, expval)
    def test_can_white_castle_short(self):
        for s12obj, expval in zip(
            self.s12,
            [ True, True, True, False, True,
              False, False, False, False, True ]):
            self.failUnlessEqual(s12obj.can_white_castle_short, expval)
    def test_can_white_castle_long(self):
        for s12obj, expval in zip(
            self.s12,
            [ True, True, True, False, True,
              False, False, False, False, True ]):
            self.failUnlessEqual(s12obj.can_white_castle_long, expval)
    def test_can_black_castle_short(self):
        for s12obj, expval in zip(
            self.s12,
            [ True, True, True, False, False,
              False, False, False, False, True ]):
            self.failUnlessEqual(s12obj.can_black_castle_short, expval)
    def test_can_black_castle_long(self):
        for s12obj, expval in zip(
            self.s12,
            [ True, True, True, False, False,
              False, False, False, False, True ]):
            self.failUnlessEqual(s12obj.can_black_castle_long, expval)
    def test_is_standard_initial_position(self):
        for idx, s12obj, expval in zip(
            list(range(0, len(self.s12))),
            self.s12,
            [ False, False, False, False, False,
              False, False, False, False, True ]):
            self.failUnlessEqual(s12obj.is_standard_initial_position, expval,
                                 "Pos %d, game %s" % (idx, s12obj))
    def test_reversible_plies_count(self):
        for pos, s12obj, expval in zip(
            list(range(0, len(self.s12))),
            self.s12,
            [ 0, 0, 0, 0, 0, 
              4, 1, 0, 10, 0]):
            self.failUnlessEqual(
                s12obj.reversible_plies_count, expval,
                "Pos %d, game %d" %(pos, s12obj.game_no))
    def test_is_clock_ticking(self):
        for s12obj, expval in zip(
            self.s12,
            [ False, True, True, True, True,
              True, True, True, True, False ]):
            self.failUnlessEqual(s12obj.is_clock_ticking, expval,
                                 "Game %d" % s12obj.game_no)
    def test_white_material(self):
        for s12obj, expval in zip(
            self.s12,
            [ 39, 39, 39, 13, 35,
              38, 31, 14, 14, 39 ]):
            self.failUnlessEqual(s12obj.white_material, expval)
    def test_black_material(self):
        for idx, s12obj, expval in zip(
            list(range(0, len(self.s12))),
            self.s12,
            [ 39, 39, 39, 14, 38,
              38, 29, 4, 4, 39 ]):
            self.failUnlessEqual(s12obj.black_material, expval,
                                 "Game %s (pos %d)" % (str(s12obj), idx))
    def test_white_remaining_time(self):
        for s12obj, expval in zip(
            self.s12,
            [ 1200, 1200, 1220, 249, 849,
              777, 1053, 14, 12, 300]):
            self.failUnlessEqual(s12obj.white_remaining_time, expval)
    def test_black_remaining_time(self):
        for s12obj, expval in zip(
            self.s12,
            [ 1200, 1200, 1200, 354, 771,
              652, 1355, 15, 0, 300]):
            self.failUnlessEqual(s12obj.black_remaining_time, expval)
    def test_next_move_no(self):
        for idx, s12obj, expval in zip(
            list(range(0,len(self.s12))),
            self.s12,
            [ 1, 2, 2, 29, 12,
              12, 16, 83, 88, 1 ]):
            self.failUnlessEqual(s12obj.next_move_no, expval)
    def test_last_move_no(self):
        for idx, s12obj, expval in zip(
            list(range(0,len(self.s12))),
            self.s12,
            [ 1, 1, 2, 28, 11,
              11, 16, 83, 88, 0 ]):
            self.failUnlessEqual(s12obj.last_move_no, expval, 
                                 "Game %s (pos %d)" % (s12obj, idx))
    def test_last_ply_no(self):
        for idx, s12obj, expval in zip(
            list(range(0,len(self.s12))),
            self.s12,
            [ 1, 2, 3, 56, 22,
              22, 31, 165, 175, 0 ]):
            self.failUnlessEqual(s12obj.last_ply_no, expval,
                                 "Game %s (pos %d)" % (s12obj, idx))
    def test_is_move(self):
        for s12obj, expval in zip(
            self.s12,
            [ True, True, True, True, True,
              True, True, True, True, False ]):
            self.failUnlessEqual(s12obj.is_move, expval)
    def test_last_move_text(self):
        for s12obj, expval in zip(
            self.s12,
            [ "d4", "d5", "c4", "h5", "Bxd5",
              "O-O", "O-O-O", "h8=Q", "Qb6#", None ]):
            self.failUnlessEqual(s12obj.last_move_text, expval)
    def test_last_move_coord_text(self):
        for s12obj, expval in zip(
            self.s12,
            [ "P/d2-d4", "P/d7-d5", "P/c2-c4", "P/h7-h5", "B/e6-d5",
              "o-o", "o-o-o", "P/h7-h8=Q", "Q/d6-b6", None ]):
            self.failUnlessEqual(s12obj.last_move_coord_text, expval)
    def test_last_move_time_spent(self):
        for s12obj, expval in zip(
            self.s12,
            [ 0, 0, 0, 68, 26,
              11, 227, 1, 0, 0 ]):
            self.failUnlessEqual(s12obj.last_move_time_spent, expval)
    def test_last_move_time_spent_text(self):
        for s12obj, expval in zip(
            self.s12,
            [ "(0:00)", "(0:00)", "(0:00)", "(1:08)", "(0:26)",
              "(0:11)", "(3:47)", "(0:01)", "(0:00)", "(0:00)" ]):
            self.failUnlessEqual(s12obj.last_move_time_spent_text, expval)
    def test_last_move_lag(self):
        for s12obj, expval in zip(
            self.s12,
            [ 0, 0, 0, 210, 649,
              425, 176, 20, 62, 0 ]):
            self.failUnlessEqual(s12obj.last_move_lag, expval)
    def test_fen(self):
        for s12obj, expval in zip(
            self.s12,
            [ "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1",
              "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2",
              "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2",
              "r5k1/6B1/p2pN3/P4N1p/4n3/8/1P3P1P/n5K1 w - h6 0 29",
              "r2q1rk1/pp2ppbp/3p1np1/n2b4/2P1P3/P2Q1N1P/1P2BPP1/R1B1K2R w KQ - 0 12",
              "r4rk1/pp1q1pp1/2nbpn1p/3p4/3N2b1/1QP2NP1/PP2PPBP/R1B1R1K1 w - - 4 12",
              "q6r/3nkppp/p3b3/1p2p3/4n3/1N6/PPP1QPPP/2KR1B1R b - - 1 16",
              "5R1Q/4k3/8/8/8/3p4/3K4/3b4 b - - 0 83",
              "1R6/k7/1Q6/8/8/3p4/2bK4/8 b - - 10 88",
              "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
              ]):
            self.failUnlessEqual(s12obj.fen, expval, str(s12obj))
    def test_observer_role(self):
        for s12obj, expval in zip(
            self.s12,
            [ style12.OBSERVER_WATCHING_ISOLATED_POSITION,
              style12.OBSERVER_WATCHING_EXAMINE, 
              style12.OBSERVER_EXAMINING, 
              style12.OBSERVER_PLAYING_WITH_OPP_TO_MOVE,
              style12.OBSERVER_PLAYING_AND_TO_MOVE,
              style12.OBSERVER_WATCHING_GAME,
              style12.OBSERVER_WATCHING_GAME, 
              style12.OBSERVER_WATCHING_GAME,
              style12.OBSERVER_WATCHING_GAME, 
              style12.OBSERVER_WATCHING_GAME,
              ]):
            self.failUnlessEqual(s12obj.observer_role, expval)
    def test_board_flipped(self):
        for s12obj, expval in zip(
            self.s12,
            [ False, False, False, False, False,
              False, False, False, False, False, ]):
            self.failUnlessEqual(s12obj.board_flipped, expval)
    def test_str(self):
        for s, t in zip(self.s12, self.texts):
            self.failUnlessEqual(
                str(s),
                t.startswith("<12>") and t or ("<12> " + t))

class UglyTestCase(unittest.TestCase):
    def test1(self):
        txt = '<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 40 moetown rikosuara 0 15 0 39 39 900 900 1 none (0:00) none 0 0 0'
        s12obj = style12.Style12(txt)
        self.failUnlessEqual(s12obj.white, 'moetown')
        self.failUnlessEqual(s12obj.black, 'rikosuara')
    def test2(self):
        txt = '<12> -------- -QppK-B- -------- -n------ -Nk-N--- -------- -RB----- r--r---- W -1 0 0 0 0 0 419 GuestQQSZ puzzlebot -2 0 0 0 0 0 0 1 none (0:00) none 0 0 0'
        s12obj = style12.Style12(txt)
        self.failUnlessEqual(s12obj.white, 'GuestQQSZ')
        self.failUnlessEqual(s12obj.black, 'puzzlebot')        


class Style12LegacyTestCase(unittest.TestCase):
    def test1(self):
        s12 = style12.Style12("rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        self.failUnlessEqual(s12.game_no, 175)
        self.failUnlessEqual(s12.white_remaining_time, 1200)
        self.failUnlessEqual(s12.black_remaining_time, 1200)
        self.failUnlessEqual(s12.next_move_no, 1)
        self.failUnlessEqual(s12.last_move_time_spent_text, '(0:00)')
        self.failUnlessEqual(s12.last_move_text, 'd4')
        self.failIfEqual(s12.to_move, WHITE)
        self.failUnlessEqual(s12.to_move, BLACK)
        self.failUnless(s12.is_move)
        self.failUnlessEqual(s12.last_move_no, 1)
        self.failUnlessEqual(s12.last_ply_no, 1)
    def test2(self):
        s12 = style12.Style12("rnbqkbnr ppp-pppp -------- ---p---- ---P---- -------- PPP-PPPP RNBQKBNR W 3 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 2 P/d7-d5 (0:00) d5 0 1 0")
        self.failUnlessEqual(s12.game_no, 175)
        self.failUnlessEqual(s12.white_remaining_time, 1200)
        self.failUnlessEqual(s12.black_remaining_time, 1200)
        self.failUnlessEqual(s12.next_move_no, 2)
        self.failUnlessEqual(s12.last_move_time_spent_text, '(0:00)')
        self.failUnlessEqual(s12.last_move_text, 'd5')
        self.failIfEqual(s12.to_move, BLACK)
        self.failUnlessEqual(s12.to_move, WHITE)
        self.failUnless(s12.is_move)
        self.failUnlessEqual(s12.last_move_no, 1)
        self.failUnlessEqual(s12.last_ply_no, 2)
    def test3(self):
        s12 = style12.Style12("rnbqkbnr ppp-pppp -------- ---p---- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1220 1200 2 P/c2-c4 (0:00) c4 0 1 0")
        self.failUnlessEqual(s12.game_no, 175)
        self.failUnlessEqual(s12.white_remaining_time, 1220)
        self.failUnlessEqual(s12.black_remaining_time, 1200)
        self.failUnlessEqual(s12.next_move_no, 2)
        self.failUnlessEqual(s12.last_move_time_spent_text, '(0:00)')
        self.failUnlessEqual(s12.last_move_text, 'c4')
        self.failIfEqual(s12.to_move, WHITE)
        self.failUnlessEqual(s12.to_move, BLACK)
        self.failUnless(s12.is_move)
        self.failUnlessEqual(s12.last_move_no, 2)
        self.failUnlessEqual(s12.last_ply_no, 3)
    def testFEN(self):
        s12 = style12.Style12("rnbqkbnr pppppppp -------- -------- ----P--- -------- PPPP-PPP RNBQKBNR B 4 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/e2-e4 (0:00) e4 0 0 0")
        fen = s12.fen
        self.failUnlessEqual(fen, 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
    def testFENStd(self):
        s12 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (0:00) d4 0 0 0")
        fen = s12.fen
        self.failUnlessEqual(fen, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def testVeryLongTime(self):
        s12 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (1:06:12) d4 0 0 0")
        self.failUnlessEqual(s12.last_move_time_spent_text, '(1:06:12)')
        self.failUnlessEqual(s12.last_move_time_spent, 3972)

    def testVeryLongTime(self):
        s12 = style12.Style12("rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1200 1200 1 P/d2-d4 (1:00:00) d4 0 0 0")
        self.failUnlessEqual(s12.last_move_time_spent_text, '(1:00:00)')
        self.failUnlessEqual(s12.last_move_time_spent, 3600)

    def testVeryLongTime2(self):
        s12 = style12.Style12("rnbqkbnr ppp-pppp -------- ---p---- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 175 yacc dontrookback 0 20 20 39 39 1220 1200 2 P/c2-c4 (1:02:28) c4 0 1 0")
        self.failUnlessEqual(s12.game_no, 175)
        self.failUnlessEqual(s12.white_remaining_time, 1220)
        self.failUnlessEqual(s12.black_remaining_time, 1200)
        self.failUnlessEqual(s12.next_move_no, 2)
        self.failUnlessEqual(s12.last_move_time_spent_text, '(1:02:28)')
        self.failUnlessEqual(s12.last_move_text, 'c4')
        self.failIfEqual(s12.to_move, WHITE)
        self.failUnlessEqual(s12.to_move, BLACK)
        self.failUnless(s12.is_move)
        self.failUnlessEqual(s12.last_move_no, 2)
        self.failUnlessEqual(s12.last_ply_no, 3)
        self.failUnlessEqual(s12.last_move_time_spent, 3748)

