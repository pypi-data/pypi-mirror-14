# -*- coding: utf-8 -*-
from twisted.trial import unittest
from twisted.internet import defer
import time
from mekk.fics.support import delaying_executor

# Nieduży czas, w którym na pewno się skończy każda z poniższych metod zakładając brak
# sleepów (tj. wykona się jej kod właściwy)
USUAL_COST=0.02
# Wymuszany interwał, powinien być większy od USUAL_COST bo inaczej test może nie mieć sensu
INTERVAL=0.05

#pycharm goes crazy with isinstance
#noinspection PyTypeChecker
class DelayingExecutorLineTestCase(unittest.TestCase):

    def setUp(self):
        self.call_results = []
    def _command(self, line):
        self.failUnlessIsInstance(line, str)
        self.call_results.append(line)

    @defer.inlineCallbacks
    def test_no_delay(self):
        self.del_exec = delaying_executor.DelayingExecutor(interval = 0, command = self._command, label="aaa")
        t1 = time.time()
        self.del_exec.execute("line 1")
        self.del_exec.execute(line = "line 2")
        for i in range(3, 11):
            self.del_exec.execute("line %d" % i)
        yield self.del_exec.sync()
        t2 = time.time()
        self.failUnless(t2 - t1 < USUAL_COST, "Amazingly slow run on null executor")
        self.failUnlessEqual(self.call_results, [ "line %d" % i for i in range(1,11) ])

    @defer.inlineCallbacks
    def test_with_delay(self):
        self.del_exec = delaying_executor.DelayingExecutor(interval = INTERVAL, command = self._command, label="aaa")
        t1 = time.time()
        self.del_exec.execute("xine 1")
        self.del_exec.execute(line = "xine 2")
        for i in range(3, 11):
            self.del_exec.execute("xine %d" % i)
        yield self.del_exec.sync()
        t2 = time.time()
        self.failUnless(t2 - t1 >= 9 * INTERVAL, "Insufficient delay: %s" % (t2-t1))
        self.failUnless(t2 - t1 < 10 * INTERVAL + USUAL_COST, "Amazingly slow run: %s" % (t2-t1))
        self.failUnlessEqual(self.call_results, [ "xine %d" % i for i in range(1,11) ])

#noinspection PyTypeChecker
class DelayingExecutorComplicatedTestCase(unittest.TestCase):

    def setUp(self):
        self.call_results = []
    def _command(self, a, b, c):
        self.failUnlessIsInstance(a, str)
        self.failUnlessIsInstance(b, int)
        self.failUnlessIsInstance(c, dict)
        self.call_results.append(dict(a=a, b=b, c=c))

    @defer.inlineCallbacks
    def test_no_delay(self):
        self.del_exec = delaying_executor.DelayingExecutor(interval = 0, command = self._command, label="aaa")
        t1 = time.time()
        self.del_exec.execute(a = "line 1", b = 1, c = dict(no=1))
        self.del_exec.execute("line 2", 2, dict(no=2))
        for i in range(3, 11):
            self.del_exec.execute("line %d" % i, i, dict(no=i))
        yield self.del_exec.sync()
        t2 = time.time()
        self.failUnless(t2 - t1 < USUAL_COST, "Amazingly slow run on null executor")
        self.failUnlessEqual(self.call_results, [ dict(a="line %d" % i, b = i, c = dict(no=i)) for i in range(1,11) ])

    @defer.inlineCallbacks
    def test_with_delay(self):
        self.del_exec = delaying_executor.DelayingExecutor(interval = INTERVAL, command = self._command, label="aaa")
        t1 = time.time()
        self.del_exec.execute(a = "line 1", b = 1, c = dict(no=1))
        self.del_exec.execute("line 2", 2, dict(no=2))
        for i in range(3, 11):
            self.del_exec.execute("line %d" % i, i, dict(no=i))
        yield self.del_exec.sync()
        t2 = time.time()
        self.failUnless(t2 - t1 >= 9 * INTERVAL, "Insufficient delay: %s" % (t2-t1))
        self.failUnless(t2 - t1 < 10 * INTERVAL + USUAL_COST, "Amazingly slow run: %s" % (t2-t1))
        self.failUnlessEqual(self.call_results, [ dict(a="line %d" % i, b = i, c = dict(no=i)) for i in range(1,11) ])
