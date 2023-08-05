# -*- coding: utf-8 -*-
from unittest import TestCase
from mekk.fics.datatypes.game_type import GameType

#noinspection PySetFunctionToLiteral
class TestGameType(TestCase):

    def test_standard(self):
        for spec in ['standard', 'Standard', 's']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, 'standard')
    def test_crazyhouse(self):
        for spec in ['crazyhouse', 'Crazyhouse', 'z']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, 'crazyhouse')
    def test_bughouse(self):
        for spec in ['bughouse', 'Bughouse', 'B']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, 'bughouse')
    def test_wild(self):
        for spec in ['Wild', 'w']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, 'wild')
        for spec in ['wild/fr', 'wild/3']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, spec)

    def test_wild_comparisons(self):
        wild_generic = GameType("wild")
        wild_fr = GameType("wild/fr")
        wild_3 = GameType("wild/3")
        self.failIfEqual(wild_generic, wild_3)
        self.failIfEqual(wild_generic, wild_fr)
        self.failIfEqual(wild_fr, wild_3)
        self.failUnless(wild_generic.matches(wild_3))
        self.failUnless(wild_generic.matches(wild_fr))
        self.failUnless(wild_generic.matches(wild_generic))
        self.failUnless(wild_fr.matches(wild_generic))
        self.failUnless(wild_3.matches(wild_generic))
        self.failUnless(wild_fr.matches(wild_fr))
        self.failUnless(wild_3.matches(wild_3))
        self.failIf(wild_fr.matches(wild_3))
        self.failIf(wild_3.matches(wild_fr))

    def test_equalable(self):
        g1 = GameType('standard')
        g2 = GameType('s')
        g3 = GameType('atomic')
        self.failUnlessEqual(g1, g1)
        self.failUnlessEqual(g1, g2)
        self.failIfEqual(g1, g3)
        self.failIfEqual(g2, g3)

    def test_sortable(self):
        g1 = GameType('standard')
        g2 = GameType('s')
        g3 = GameType('atomic')
        g4 = GameType('bughouse')
        self.failUnless(g3 < g1)
        self.failUnless(g2 > g3)
        self.failIf(g1 == g3)
        tab = [g4,g1,g3]
        tab.sort()
        self.failUnlessEqual(tab, [g3, g4, g1])

    def test_stringifiable(self):
        for spec in ['standard', 'blitz', 'B', 'z', 'x']:
            gt = GameType(spec)
            self.failUnlessEqual(gt.name, str(gt))

    def test_setable(self):
        g1 = GameType('standard')
        g2 = GameType('s')
        g3 = GameType('atomic')
        st = set([g1, g2, g3])
        self.failUnlessEqual(st, set([g1, g3]))

    def test_hashable(self):
        g1 = GameType('standard')
        g2 = GameType('s')
        g3 = GameType('atomic')
        dct = dict()
        dct[g1] = 1
        dct[g2] = 2
        dct[g3] = 3
        self.failUnlessEqual(dct, {g1: 2, g3: 3})
