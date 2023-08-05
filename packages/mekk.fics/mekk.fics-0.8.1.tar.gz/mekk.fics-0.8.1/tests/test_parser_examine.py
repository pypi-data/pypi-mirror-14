# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.parsing import info_parser
from mekk.fics.constants import block_codes
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal, SkipTest


class ExamineTestCase(unittest.TestCase):

    def test_mex(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'puzzlebot is now an examiner of game 212.')

    def test_stop(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'puzzlebot stopped examining game 212.')

    def test_noex(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 419 (which you were observing) has no examiners.')

    def test_move(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 212: chudzida moves: Qg5')

    def test_move2(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 212: chudzida moves: e6')
