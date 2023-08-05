# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.constants import block_codes

#noinspection PySetFunctionToLiteral
class BlockCodesTestCase(unittest.TestCase):
    """
    Just make sure those constants exist
    """
    def testBlock(self):
        s = set([block_codes.BLOCK_START, block_codes.BLOCK_SEPARATOR,
                 block_codes.BLOCK_END, block_codes.BLOCK_POSE_START,
                 block_codes.BLOCK_POSE_END])
        self.failUnlessEqual(len(s), 5)
    def testCommand(self):
        s = set([block_codes.BLKCMD_NULL,
                 block_codes.BLKCMD_GAME_MOVE,
                 block_codes.BLKCMD_ABORT,
                 block_codes.BLKCMD_ACCEPT,
                 block_codes.BLKCMD_BACKWARD,
                 block_codes.BLKCMD_PLAY,
                 block_codes.BLKCMD_ERROR_BADCOMMAND,
                 block_codes.BLKCMD_ERROR_BADPARAMS])
        self.failUnlessEqual(len(s), 8)
