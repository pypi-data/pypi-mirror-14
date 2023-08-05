# -*- coding: utf-8 -*-

# TODO → test komend robionych klasą

#import unittest
from twisted.internet import defer
from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest

from mekk.fics import tell_commands, datatypes
from mekk.fics.tell_commands import tell_errors
from mekk.fics.tell_commands.odict import OrderedDict
from six.moves import map
from six.moves import zip

class CommandParserResolverTestCase(unittest.TestCase):
    def setUp(self):
        self.resolver = tell_commands.ShortcutResolver(
            ['listplayers','getGames','getStatus','getGamesHistory','showUsers','read','help'],
            { 'lp': 'listplayers', 'su': 'showUsers' })
        self.resolver.add_keyword('view')
        self.resolver.add_alias('see', 'view')
    def testFull(self):
        self.failUnlessEqual(self.resolver.resolve('listplayers'), 'listplayers')
        self.failUnlessEqual(self.resolver.resolve('showusers'), 'showusers')
        self.failUnlessEqual(self.resolver.resolve('view'), 'view')
    def testFullUpp(self):
        self.failUnlessEqual(self.resolver.resolve('ListPlayers'), 'listplayers')
        self.failUnlessEqual(self.resolver.resolve('SHOWUSERS'), 'showusers')
        self.failUnlessEqual(self.resolver.resolve('vIEw'), 'view')
    def testBeingPfx(self):
        self.failUnlessEqual(self.resolver.resolve('getgames'), 'getgames')
    def testPfx(self):
        self.failUnlessEqual(self.resolver.resolve('r'), 'read')
        self.failUnlessEqual(self.resolver.resolve('show'), 'showusers')
        self.failUnlessEqual(self.resolver.resolve('v'), 'view')
    def testPfxToSelfAndAlias(self):
        self.failUnlessEqual(self.resolver.resolve('l'), 'listplayers')
    def testAlias(self):
        self.failUnlessEqual(self.resolver.resolve('lp'), 'listplayers')
        self.failUnlessEqual(self.resolver.resolve('see'), 'view')
    def testPfxToAlias(self):
        self.failUnlessEqual(self.resolver.resolve('se'), 'view')
    def testDupe(self):
        self.failUnlessRaises(tell_errors.ShortcutAmbiguousKeyword, self.resolver.resolve,'g')
    def testDupeWithPfx(self):
        self.failUnlessRaises(tell_errors.ShortcutAmbiguousKeyword, self.resolver.resolve,'s')
    def testUnknown(self):
        self.failUnlessRaises(tell_errors.ShortcutUnknownKeyword, self.resolver.resolve,'ab')
    def testTooLong(self):
        self.failUnlessRaises(tell_errors.ShortcutUnknownKeyword, self.resolver.resolve,'helpme')

class TellCommandsWrapper(tell_commands.TellCommandsMixin):
    """
    Uzupełnienie klasy mixina o minimum metod wymaganych do jego używania.
    Dodatkowo rejestruje wszystkie ewentualne tell-e i pozwala je testować
    """
    def is_TD(self, player):
        return False
    def is_computer(self, player):
        d = defer.Deferred()
        #defer.returnValue(False)
        d.callback(False)
        return d
    def tell_to(self, player, text):
        if not hasattr(self, '_got_tells'):
            self._got_tells = []
        self._got_tells.append( (player, text) )

    def verify_tell(self, testcase, player, text):
        """
        Sprawdza że otrzymano taki tell i zarazem zdejmuje go z kolejki.
        """
        if not hasattr(self, '_got_tells'):
            self._got_tells = []
        if self._got_tells:
            testcase.failUnlessEqual(self._got_tells.pop(0), (player, text))
        else:
            testcase.fail("Missing tell: %s: %s" % (player, text))

    def __del__(self):
        if hasattr(self, '_got_tells'):
            if self._got_tells:
                raise Exception("Unexpected tell(s): " % self._got_tells)

class CommandParserTestCase(unittest.TestCase):
    def setUp(self):
        #self.parser = command_parser.CommandParser()
        self.parser = TellCommandsWrapper()
        self.parser.register_command(tell_commands.make_tell_command(
            self._helpCalled, name='help', name_aliases=['doc'], max_positional_parameter_count=5))
        self.parser.register_command(tell_commands.make_tell_command(
            self._printCalled, 'print', ['write'], max_positional_parameter_count=6))
        self.parser.register_command(tell_commands.make_tell_command(self._addCalled, 'add', max_positional_parameter_count=10))
        self.parser.register_command(tell_commands.make_tell_command(self._multCalled, 'mult', max_positional_parameter_count=13))
        self.helpCalled = None
        self.printCalled = None
        self.addCalled = None
        self.multCalled = None
    def _helpCalled(self, client, player, args, named_args):
        self.helpCalled = 1
    def _printCalled(self, client, player, args, named_args):
        self.printCalled = ",".join(args)
    def _addCalled(self, client, player, args, named_args):
        self.addCalled = sum( map(int, args) )
    def _multCalled(self, client, player, args, named_args):
        named_args_dict = OrderedDict(named_args)
        mult = int(named_args_dict['mult'])
        self.multCalled = sum( map( lambda x: mult * x, map(int, args) ))

    @inlineCallbacks
    def testHelp(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerXXX", "help"))
        self.failUnless(self.helpCalled)
        self.helpCalled = None
    @inlineCallbacks
    def testHelp2(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playeryyy", "d "))
        self.failUnless(self.helpCalled)
        self.helpCalled = None
    @inlineCallbacks
    def testHelp3(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "doc groc koc"))
        self.failUnless(self.helpCalled)
        self.helpCalled = None
    @inlineCallbacks
    def testPrint(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "print Ala Ma Kota"))
        self.failUnlessEqual(self.printCalled, "Ala,Ma,Kota")
    @inlineCallbacks
    def testPrint2(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "print Ala Ma Kota I Psa "))
        self.failUnlessEqual(self.printCalled, "Ala,Ma,Kota,I,Psa")
    @inlineCallbacks
    def testPrint3(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "print "))
        self.failUnlessEqual(self.printCalled, "")
    @inlineCallbacks
    def testSum(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "add 1 2 3 4"))
        self.failUnlessEqual(self.addCalled, 10)
    @inlineCallbacks
    def testMult(self):
        yield self.parser.on_tell(datatypes.AttributedTell("playerz", "mult 1 2 3 4 mult=7"))
        self.failUnlessEqual(self.multCalled, 70)
    #def testUnknown(self):
    #    d = self.parser.on_tell(
    #        datatypes.AttributedTell('zoo', 'krokodyl'))
    #    return self.failUnlessFailure(d, tell_errors.UnknownCommand)
    @inlineCallbacks
    def testUnknown(self):
        yield self.parser.on_tell(
            datatypes.AttributedTell('zoo', 'krokodyl'))
        self.parser.verify_tell(self, 'zoo', "Unknown command: krokodyl (expected one of: add, doc, help, mult, print, write)")
