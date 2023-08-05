# -*- coding: utf-8 -*-
import logging
import os

from twisted.internet import defer, reactor
from twisted.trial import unittest
from mekk.fics.twisted_util import delay_succeed, delay_exception, gather_with_cancel

if os.environ.get('DEBUG_REACTOR'):
    import twisted.internet.base
    twisted.internet.base.DelayedCall.debug = True

class SomeExc(Exception):
    pass

class DeferTestCase(unittest.TestCase):
    """
    Tests whether our test mechanique properly sync
    """

    @defer.inlineCallbacks
    def testDelayOks(self):
        x = yield delay_succeed("xyz")
        self.failUnlessEqual(x, "xyz")

    @defer.inlineCallbacks
    def testMultipleOks(self):
        x = yield delay_succeed("xyz")
        self.failUnlessEqual(x, "xyz")
        y = yield delay_succeed("abc")
        self.failUnlessEqual(y, "abc")

    @defer.inlineCallbacks
    def testReorder(self):
        x = delay_succeed("first", delay=0.2)
        y = delay_succeed("second", delay=0.05)
        r = yield defer.gatherResults([x, y])
        self.failUnlessEqual(r, ["first", "second"])

    @defer.inlineCallbacks
    def testDelaySucceedDelays(self):
        t1 = reactor.seconds()
        x = yield delay_succeed("xyz", delay=0.1)
        t2 = reactor.seconds()
        self.failUnlessEqual(x, "xyz")
        self.failUnless(t2 >= t1 + 0.1)

    @defer.inlineCallbacks
    def testExcept(self):
        try:
            y = yield delay_exception(SomeExc())
            self.fail("No exception")
        except SomeExc:
            pass

    @defer.inlineCallbacks
    def testExceptDelays(self):
        t1 = reactor.seconds()
        try:
            y = yield delay_exception(SomeExc(), delay=0.1)
            self.fail("No exception")
        except SomeExc:
            t2 = reactor.seconds()
            self.failUnless(t2 >= t1 + 0.1)

    @defer.inlineCallbacks
    def testOkAndExcept(self):
        try:
            x = yield delay_succeed("a")
            self.failUnlessEqual(x, "a")
            y = yield delay_exception(SomeExc())
            self.fail("No exception")
        except SomeExc:
            pass

    # @defer.inlineCallbacks
    # def testTwoExcept(self):
    #     """
    #     Wrong code which leaves reactor dirty
    #     """
    #     try:
    #         x = delay_exception(SomeExc(), delay=0.2)
    #         y = delay_exception(SomeExc(), delay=0.05)
    #         yield x
    #         yield y
    #         self.fail("No exception")
    #     except SomeExc:
    #         pass
    #     self.failUnless(x.called)
    #     self.failUnless(y.called)
    # testTwoExcept.skip = "This is example of how bad code fails"

    # @defer.inlineCallbacks
    # def testGatherExcept(self):
    #     """
    #     Wrong code which leaves reactor dirty
    #     """
    #     x = delay_succeed("beforee", delay=0.2)
    #     y = delay_exception(SomeExc(),delay=0.05)
    #     try:
    #         r = yield defer.gatherResults([x,y])
    #         self.fail("No exception")
    #     except SomeExc:
    #         pass
    #     self.failUnless(x.called)
    # testGatherExcept.skip = "This is example of bad code"

    # @defer.inlineCallbacks
    # def testGatherTwoExcept(self):
    #     """
    #     Wrong code which leaves reactor dirty
    #     """
    #     x = delay_exception(SomeExc(), delay=0.2)
    #     y = delay_exception(SomeExc(), delay=0.05)
    #     try:
    #         r = yield defer.gatherResults([x,y])
    #         self.fail("No exception")
    #     except SomeExc:
    #         pass
    #     self.failUnless(x.called)
    #     self.failUnless(y.called)
    # testGatherTwoExcept.skip = "This is example of bad code"

    @defer.inlineCallbacks
    def testProperlyGatherWithErr(self):
        x = delay_succeed("x", delay=0.2)
        y = delay_exception(SomeExc(),delay=0.05)
        z = delay_succeed("AAAAA", delay=0.05)
        try:
            #r = yield defer.gatherResults([x,y,z], consumeErrors=True)
            #print r
            reply = yield gather_with_cancel([x,y,z])
            self.fail("No exception, got reply: %s" % reply)
        except SomeExc:
            pass
        self.failUnless(x.called)
        self.failUnless(y.called)
        self.failUnless(z.called)

    @defer.inlineCallbacks
    def testProperlyGatherWithManyErrors(self):
        x = delay_exception(SomeExc(), delay=0.2)
        y = delay_exception(SomeExc(),delay=0.05)
        z = delay_succeed("AAAAA", delay=0.05)
        try:
            #r = yield defer.gatherResults([x,y,z], consumeErrors=True)
            #print r
            reply = yield gather_with_cancel([x,y,z])
            self.fail("No exception, got reply: %s" % reply)
        except SomeExc:
            pass
        self.failUnless(x.called)
        self.failUnless(y.called)
        self.failUnless(z.called)

    @defer.inlineCallbacks
    def testProperlyGatherOK(self):
        x = delay_succeed("XXX", delay=0.2)
        y = delay_succeed("YYY",delay=0.05)
        z = delay_succeed("ZZZ", delay=0.03)
        rx, ry, rz = yield gather_with_cancel([x,y,z])
        self.failUnlessEqual(rx, "XXX")
        self.failUnlessEqual(ry, "YYY")
        self.failUnlessEqual(rz, "ZZZ")

