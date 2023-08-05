# -*- coding: utf-8 -*-
from unittest import TestCase
import sys
if sys.argv[0].endswith("trial"):
    from twisted.trial.unittest import SkipTest as TrialSkipTest
    SkipTest = TrialSkipTest
else:
    from nose import SkipTest as NoseSkipTest
    SkipTest = NoseSkipTest
from mekk.fics.datatypes.player import PlayerName

class TestPlayerName(TestCase):
    def test_equal_are_equal(self):
        p1 = PlayerName("Mekk")
        p2 = PlayerName("Mekk")
        self.failUnlessEqual(p1, p2)
    def test_case_different_are_equal(self):
        p1 = PlayerName("MekK")
        p2 = PlayerName("meKk")
        self.failUnlessEqual(p1, p2)
    def test_different_are_different(self):
        p1 = PlayerName("Mekk")
        p2 = PlayerName("ryoshu")
        self.failIfEqual(p1, p2)
    def test_different_are_different_even_if_pfx(self):
        p1 = PlayerName("Mekk")
        p2 = PlayerName("Mek")
        self.failIfEqual(p1, p2)
    def test_substring_is_equal(self):
        p1 = PlayerName("Malabelajestluba")
        p2 = PlayerName("Malabelaj", can_be_truncated=True)
        self.failUnlessEqual(p1, p2)
    def test_full_substring_is_not_equal(self):
        p1 = PlayerName("Malabelajestluba")
        p2 = PlayerName("Malabelaj", can_be_truncated=False)
        self.failIfEqual(p1, p2)
    def test_short_substring_is_not_equal(self):
        p1 = PlayerName("Malabelajestluba")
        p2 = PlayerName("Mala", can_be_truncated=True)
        self.failIfEqual(p1, p2)
    def test_hashable(self):
        d = { PlayerName("ala"): 1, PlayerName("bela"): 2 }
        self.failUnlessEqual( d[PlayerName("bela")], 2 )
        d[ PlayerName("ala") ] = 3
        self.failUnlessEqual( d[PlayerName("ala")], 3 )
    def test_hashable_short(self):
        d = { PlayerName("alamalaka"): 1, PlayerName("belamalaka"): 2 }
        self.failUnlessEqual( d[PlayerName("belamalaka")], 2 )
        d[ PlayerName("alamalaka", True) ] = 3
        self.failUnlessEqual( d[PlayerName("alamalaka")], 3 )
        d[ PlayerName("belamalak", True) ] = 5
        self.failUnlessEqual( d[PlayerName("belamalaka")], 5 )
        self.failIf( PlayerName("belamalak") in d )
        self.failUnlessEqual( d[PlayerName("belamalak", True)], 5 )
        d[ PlayerName("bela", True) ] = 6
        d[ PlayerName("belaj", True) ] = 7
        self.failUnlessEqual( d[PlayerName("belamalaka")], 5 )
        self.failUnlessEqual( d[PlayerName("bela")], 6 )
        self.failUnlessEqual( d[PlayerName("belaj")], 7 )
    def test_comparable_with_string(self):
        self.failUnlessEqual(PlayerName("Mekk"), "mekk")
        self.failIfEqual(PlayerName("Mekk"), "mek")
