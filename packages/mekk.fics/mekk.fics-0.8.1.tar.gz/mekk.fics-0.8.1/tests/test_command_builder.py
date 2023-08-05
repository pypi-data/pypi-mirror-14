# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.command_building import ivar_login
from mekk.fics import errors

class CommandBuilderIvarsTestCase(unittest.TestCase):
    def testIvarsEmpty(self):
        l = ivar_login.ivar_login_line()
        self.failUnlessEqual(l, '%b')
    def testIvarsSimple(self):
        l = ivar_login.ivar_login_line('DEFPROMPT', 'BLOCK', 'LOCK')
        self.failUnlessEqual(l, '%b0001101')
    def testIvarsAll(self):
        l = ivar_login.ivar_login_line(
            'COMPRESSMOVE', 'AUDIOCHAT', 'SEEKREMOVE', 'DEFPROMPT',
            'LOCK', 'STARTPOS', 'BLOCK', 'GAMEINFO', 'XDR',
            'PENDINFO', 'GRAPH', 'SEEKINFO', 'EXTASCII',
            'NOHIGHLIGHT', 'VT_HIGHLIGHT', 'SHOWSERVER', 'PIN',
            'MS', 'PINGINFO', 'BOARDINFO', 'EXTUSERINFO',
            'SEEKCA', 'SHOWOWNSEEK', 'PREMOVE', 'SMARTMOVE',
            'MOVECASE', 'SUICIDE', 'CRAZYHOUSE', 'LOSERS',
            'WILDCASTLE', 'FR', 'NOWRAP', 'ALLRESULTS', 'OBSPING',
            'SINGLEBOARD')
        self.failUnlessEqual(l, '%b11111111111111111111111111111111111')
    def testIvarsBadParam(self):
        self.failUnlessRaises(
            errors.UnknownIVar, ivar_login.ivar_login_line, 'KURA')
    def testIvarsMixedParam(self):
        self.failUnlessRaises(
            errors.UnknownIVar, ivar_login.ivar_login_line, 'OBSPING', 'KURA')
