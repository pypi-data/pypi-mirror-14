# -*- coding: utf-8 -*-

from twisted.trial import unittest
from mekk.fics.constants import block_codes
from mekk.fics.parsing.reply.block_mode_filter import BlockModeFilter


#noinspection PyTypeChecker
class BlockModeFilterTestCase(unittest.TestCase):
    def _callback(self, id, code, text):
        self.failUnlessIsInstance(id, int)
        self.failUnlessIsInstance(code, int)
        self.failUnlessIsInstance(text, str)
        return dict(id = id, code=code, text=text)
    def test_plainline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("abcdefgh"),
            ("abcdefgh", []))
        self.failIf(flt.prompt_seen())
    def test_promptline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("fics% abcdefgh"),
            ("abcdefgh", []))
        self.failUnless(flt.prompt_seen())
    def test_emptyline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(""),
            ("", []))
    def test_emptypromptline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("fics% "),
            ("", []))
    def test_fullblock(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam") ] ))
    def test_fullblock_and_text(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "ala"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END
                + "ma kota"),
            ("alama kota", [ dict(id=33, code=99, text="param pam pam") ] ))
    def test_two_full_blocks(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "ala"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END
                + "-"
                + block_codes.BLOCK_START + "44"
                + block_codes.BLOCK_SEPARATOR + "2"
                + block_codes.BLOCK_SEPARATOR + "taram pam wam"
                + block_codes.BLOCK_END
                + "ma kota"),
            ("ala-ma kota", [
                dict(id=33, code=99, text="param pam pam"),
                dict(id=44, code=2, text="taram pam wam"),
                ]))
    def test_normal_twoline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam\naj ja ja jaj") ]))
    def test_normal_multiline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj") ]))
    def test_mixed_multiline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "pre rre"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("pre rre", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END
                + "postttt"),
            ("postttt", [ dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj") ]))
    def test_multiline_and_normal(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "pre rre"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("pre rre", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END
                + "-"
                + block_codes.BLOCK_START + "44"
                + block_codes.BLOCK_SEPARATOR + "2"
                + block_codes.BLOCK_SEPARATOR + "taram pam wam"
                + block_codes.BLOCK_END
                + "postttt"),
            ("-postttt", [
                dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj"),
                dict(id=44, code=2, text="taram pam wam"),
                ]))
    def test_multiline_with_continuation(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                r'\     aj ja ja jaj '),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                r'\ho ho'
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam aj ja ja jaj ho ho") ]))
    def test_multiline_with_continuation_fingerlike(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "38"
                + block_codes.BLOCK_SEPARATOR + "98"
                + block_codes.BLOCK_SEPARATOR + " 1: Marcin, Warsaw, Poland. http://mekk.waw.pl"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "2: wild fr=normal chess with randomized initial position. Great fun! I can "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "\\   play unrated wild fr game and explain the rules, just ask."),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "3: Please, say \"good game\" only if it was good game. Auto-greetings are "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "\\   incredibly irritating."),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_END),
            ("", [ dict(id=38, code=98, text=""" 1: Marcin, Warsaw, Poland. http://mekk.waw.pl
2: wild fr=normal chess with randomized initial position. Great fun! I can play unrated wild fr game and explain the rules, just ask.
3: Please, say "good game" only if it was good game. Auto-greetings are incredibly irritating.
""") ]))
