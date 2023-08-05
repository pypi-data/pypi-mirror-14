# -*- coding: utf-8 -*-
from twisted.trial import unittest
from twisted.python import failure
from mekk.fics.support import block_deferreds
from mekk.fics.errors import FicsCommandExecutionException

#noinspection PyTypeChecker
class BlockDeferredsTestCase(unittest.TestCase):
    def setUp(self):
        self.rd = block_deferreds.BlockDeferreds("xyz")
    def test_single(self):
        id, df = self.rd.allocate()
        self.failUnlessEqual(id, 1)
        fired = []
        def setIt(val):
            fired.append(val)
        df.addCallback(setIt)
        self.rd.fire(id, "baaa")
        self.failUnlessEqual(fired, ["baaa"])
    def test_many(self):
        id1, df1 = self.rd.allocate()
        self.failUnlessEqual(id1, 1)
        id2, df2 = self.rd.allocate()
        self.failUnlessEqual(id2, 2)
        id3, df3 = self.rd.allocate()
        self.failUnlessEqual(id3, 3)
        fired = []
        def setIt(val):
            fired.append(val)
        df1.addCallback(setIt)
        df2.addCallback(setIt)
        df3.addCallback(setIt)
        self.rd.fire(id3, "c")
        self.rd.fire(id2, "b")
        self.rd.fire(id1, "a")
        self.failUnlessEqual(fired, ["c", "b", "a"])

    def test_many_jump(self):
        id1, df1 = self.rd.allocate()
        self.failUnlessEqual(id1, 1)
        id2, df2 = self.rd.allocate()
        self.failUnlessEqual(id2, 2)
        id3, df3 = self.rd.allocate()
        self.failUnlessEqual(id3, 3)
        fired = []
        def setIt(val):
            fired.append(val)
        df1.addCallback(setIt)
        df2.addCallback(setIt)
        df3.addCallback(setIt)

        self.rd.fire(id2, "b")
        self.failUnlessEqual(fired, ["b"])

        id4, df4 = self.rd.allocate()
        self.failUnlessEqual(id4, 2)
        id5, df5 = self.rd.allocate()
        self.failUnlessEqual(id5, 4)
        df4.addCallback(setIt)
        df5.addCallback(setIt)

        self.rd.fire(id3, "c")
        self.rd.fire(id4, "d")
        self.rd.fire(id5, "e")
        self.rd.fire(id1, "a")
        self.failUnlessEqual(fired, ["b", "c", "d", "e", "a"])

    def test_reset(self):
        id1, df1 = self.rd.allocate()
        self.failUnlessEqual(id1, 1)
        id2, df2 = self.rd.allocate()
        self.failUnlessEqual(id2, 2)
        id3, df3 = self.rd.allocate()
        self.failUnlessEqual(id3, 3)
        self.rd.reset()
        id4, df4 = self.rd.allocate()
        self.failUnlessEqual(id4, 1)

    def test_error(self):
        id, df = self.rd.allocate()
        self.failUnlessEqual(id, 1)
        fired = []
        failed = []
        def setIt(val):
            fired.append(val)
        def errIt(val):
            failed.append(val)
        df.addCallback(setIt)
        df.addErrback(errIt)
        self.rd.fire_error(id, FicsCommandExecutionException("baaam"))
        self.failUnlessEqual(fired, [])
        self.failUnlessEqual(len(failed), 1)
        fail_obj = failed[0]
        self.assertIsInstance(fail_obj, failure.Failure)
        self.assertIsInstance(fail_obj.value, FicsCommandExecutionException)
        self.assertEqual(fail_obj.getErrorMessage(), "Command failed: baaam")


if __name__ == '__main__':
    unittest.main()
