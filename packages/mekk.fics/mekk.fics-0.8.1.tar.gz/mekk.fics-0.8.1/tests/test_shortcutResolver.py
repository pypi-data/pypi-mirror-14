# -*- coding: utf-8 -*-
from unittest import TestCase
from mekk.fics.tell_commands.shortcut_resolver import ShortcutResolver
from mekk.fics.tell_commands.tell_errors import ShortcutAliasToUnknownKeyword, ShortcutKeywordConflict, ShortcutAmbiguousKeyword, ShortcutUnknownKeyword
import six


class TestKeywordOnlyShortcutResolver(TestCase):
    def setUp(self):
        self.kwlist = [
            "listplayers", "listgames", "finger", "register", "play"]
        self.sr = ShortcutResolver(keywords=self.kwlist)
    def test_keywords(self):
        for kw in self.kwlist:
            self.failUnlessEqual(
                self.sr.resolve(kw), kw)
            self.failUnlessEqual(
                self.sr.resolve(kw.upper()), kw)
        self.failUnlessEqual(
            self.sr.resolve("PLaY"), "play")
    def test_good_prefixes(self):
        self.failUnlessEqual(
            self.sr.resolve("fin"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("f"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("listp"), "listplayers")
        self.failUnlessEqual(
            self.sr.resolve("P"), "play")
        self.failUnlessEqual(
            self.sr.resolve("reg"), "register")
    def test_ambiguous_prefixes(self):
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "list")
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "l")
    def test_unknown(self):
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "z")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "fingerme")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "listbadguys")

class TestKeywordOnlyShortcutResolverCreatedManually(TestCase):
    def setUp(self):
        self.kwlist = [
            "listplayers", "listgames", "finger", "register", "play"]
        self.sr = ShortcutResolver()
        for kw in self.kwlist:
            self.sr.add_keyword(kw)
    def test_keywords(self):
        for kw in self.kwlist:
            self.failUnlessEqual(
                self.sr.resolve(kw), kw)
            self.failUnlessEqual(
                self.sr.resolve(kw.upper()), kw)
        self.failUnlessEqual(
            self.sr.resolve("PLaY"), "play")
    def test_good_prefixes(self):
        self.failUnlessEqual(
            self.sr.resolve("fin"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("f"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("listp"), "listplayers")
        self.failUnlessEqual(
            self.sr.resolve("P"), "play")
        self.failUnlessEqual(
            self.sr.resolve("reg"), "register")
    def test_ambiguous_prefixes(self):
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "list")
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "l")
    def test_unknown(self):
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "z")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "fingerme")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "listbadguys")

class TestShortcutResolverWithAliases(TestCase):
    def setUp(self):
        self.kwlist = [
            "listplayers", "listgames", "finger", "register", "play"]
        self.aliases = {
            "list": "listgames",
            "enter": "register",
            "go": "play",
            "join": "register",
            "enjoy": "register",
        }
        self.sr = ShortcutResolver(keywords=self.kwlist, aliases=self.aliases)
    def test_keywords(self):
        for kw in self.kwlist:
            self.failUnlessEqual(
                self.sr.resolve(kw), kw)
            self.failUnlessEqual(
                self.sr.resolve(kw.upper()), kw)
        self.failUnlessEqual(
            self.sr.resolve("PLaY"), "play")
    def test_exact_aliases(self):
        for name, value in six.iteritems(self.aliases):
            self.failUnlessEqual(
                self.sr.resolve(name), value)
            self.failUnlessEqual(
                self.sr.resolve(name.upper()), value)
    def test_good_prefixes(self):
        self.failUnlessEqual(
            self.sr.resolve("fin"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("f"), "finger")
        self.failUnlessEqual(
            self.sr.resolve("listp"), "listplayers")
        self.failUnlessEqual(
            self.sr.resolve("P"), "play")
        self.failUnlessEqual(
            self.sr.resolve("reg"), "register")
    def test_alias_prefixes(self):
        self.failUnlessEqual(
            self.sr.resolve("j"), "register")
        self.failUnlessEqual(
            self.sr.resolve("g"), "play")
    def test_alias_prefix_duplicate_but_known(self):
        self.failUnlessEqual(
            self.sr.resolve("e"), "register")
    def test_ambiguous_prefixes(self):
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "lis")
        self.failUnlessRaises(
            ShortcutAmbiguousKeyword,
            self.sr.resolve, "l")
    def test_unknown(self):
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "z")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "fingerme")
        self.failUnlessRaises(
            ShortcutUnknownKeyword,
            self.sr.resolve, "listbadguys")
    def test_list_keywords(self):
        self.failUnlessEqual(sorted(self.sr.list_keywords(skip_aliases=True)),
                            sorted(self.kwlist))
    def test_list_all(self):
        self.failUnlessEqual(sorted(self.sr.list_keywords()),
                             sorted(self.kwlist + list(self.aliases.keys())))


class TestShortcutResolverWithAliasesCreatedIncrementally(TestCase):
    def setUp(self):
        self.kwlist = [
            "listplayers", "listgames", "finger", "register", "play"]
        self.aliases = {
            "list": "listgames",
            "enter": "register",
            "go": "play",
            "join": "register",
            "enjoy": "register",
            }
        self.sr = ShortcutResolver()
        for kw in self.kwlist:
            self.sr.add_keyword(kw)
        for alias, kw in six.iteritems(self.aliases):
            self.sr.add_alias(alias, kw)
    # Tests inherited

class TestShortcutResolverMisconfig(TestCase):
    def setUp(self):
        self.sr = ShortcutResolver(keywords=["list", "go"], aliases={"play":"go"})
    def test_add_alias_conflict_with_keyword(self):
        self.failUnlessRaises(
            ShortcutKeywordConflict,
            self.sr.add_alias, "go", "list")
    def test_add_keyword_conflict_with_alias(self):
        self.failUnlessRaises(
            ShortcutKeywordConflict,
            self.sr.add_keyword, "play")
    def test_alias_to_unknown_keyword(self):
        self.failUnlessRaises(
            ShortcutAliasToUnknownKeyword,
            self.sr.add_alias, "sleep", "wait")
