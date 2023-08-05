# -*- coding: utf-8 -*-
from twisted.trial import unittest
from mekk.fics.support import tell_status

class LoopPreventionTestCase(unittest.TestCase):
    def setUp(self):
        self.loop_prevention = tell_status.TellLoopPrevention(3)
    def test_StopAfter3(self):
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
    def test_StopAfter3For2(self):
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("bejoho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("bejoho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("bejoho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("bejoho") )
    def test_GoodResets(self):
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.loop_prevention.good_tell("joho")
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failUnless( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )
        self.failIf( self.loop_prevention.bad_tell("joho") )