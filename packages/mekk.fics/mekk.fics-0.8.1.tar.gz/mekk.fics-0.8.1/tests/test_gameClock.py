# -*- coding: utf-8 -*-
from unittest import TestCase
from mekk.fics.datatypes.game_clock import GameClock

#noinspection PyCompatibility
class TestGameClock(TestCase):

    def setUp(self):
        self.t0500 = GameClock(5, 0)
        self.t0212 = GameClock(2, 12)
        self.t9030 = GameClock(90, 30)

    def test_base_min(self):
        self.failUnlessEqual(self.t0500.base_min, 5)
        self.failUnlessEqual(self.t0212.base_min, 2)
        self.failUnlessEqual(self.t9030.base_min, 90)

    def test_base_sec(self):
        self.failUnlessEqual(self.t0500.base_sec, 5 * 60)
        self.failUnlessEqual(self.t0212.base_sec, 2 * 60)
        self.failUnlessEqual(self.t9030.base_sec, 90 * 60)

    def test_inc_sec(self):
        self.failUnlessEqual(self.t0500.inc_sec, 0)
        self.failUnlessEqual(self.t0212.inc_sec, 12)
        self.failUnlessEqual(self.t9030.inc_sec, 30)

    def test_time_for_moves_sec(self):
        for moves_count in [0, 10, 250]:
            self.failUnlessEqual(self.t0500.time_for_moves_sec(moves_count), 5 * 60)
            self.failUnlessEqual(self.t0212.time_for_moves_sec(moves_count), 2 * 60 + moves_count * 12)
            self.failUnlessEqual(self.t9030.time_for_moves_sec(moves_count), 90 * 60 + moves_count * 30)

    def test_time_for_40_moves_sec(self):
        self.failUnlessEqual(self.t0500.time_for_40_moves_sec, 5 * 60)
        self.failUnlessEqual(self.t0212.time_for_40_moves_sec, 2 * 60 + 40 * 12)
        self.failUnlessEqual(self.t9030.time_for_40_moves_sec, 90 * 60 + 40 * 30)

    def test_str_fics(self):
        self.failUnlessEqual(self.t0500.text_fics, "5 0")
        self.failUnlessEqual(self.t0212.text_fics, "2 12")
        self.failUnlessEqual(self.t9030.text_fics, "90 30")

    def test_str(self):
        self.failUnlessEqual(str(self.t0500), "5+0")
        self.failUnlessEqual(str(self.t0212), "2+12")
        self.failUnlessEqual(str(self.t9030), "90+30")

    def test_equalable(self):
        g1 = GameClock(2,12)
        g2 = GameClock(2,2)
        g3 = GameClock(5,12)
        g4 = GameClock(2,12)
        self.failUnlessEqual(g1, g1)
        self.failUnlessEqual(g1, g4)
        self.failIfEqual(g1, g2)
        self.failIfEqual(g1, g3)
        self.failIfEqual(g2, g3)

    def test_sortable(self):
        g1 = GameClock(2,12)
        g2 = GameClock(2,2)
        g3 = GameClock(5,12)
        g4 = GameClock(3,0)
        self.failUnless(g1 < g3)
        self.failUnless(g4 > g2)
        self.failIf(g1 == g3)
        tab = [g1, g2, g3, g4]
        tab.sort()
        self.failUnlessEqual(tab, [g2,g1,g4,g3])

    def test_setable(self):
        g1 = GameClock(2,12)
        g2 = GameClock(2,2)
        g3 = GameClock(5,12)
        g4 = GameClock(3,0)
        st = set([g1, g2, g3, g4, GameClock(2, 2), GameClock(5, 12)])
        self.failUnlessEqual(st, set([g1, g2, g3, g4]))

    def test_hashable(self):
        g1 = GameClock(2,12)
        g2 = GameClock(2,2)
        g3 = GameClock(5,12)
        g4 = GameClock(2,12)
        dct = dict()
        dct[g1] = 1
        dct[g2] = 2
        dct[g3] = 3
        dct[g4] = 4
        self.failUnlessEqual(dct, {g1: 4, g2: 2, g3: 3})
