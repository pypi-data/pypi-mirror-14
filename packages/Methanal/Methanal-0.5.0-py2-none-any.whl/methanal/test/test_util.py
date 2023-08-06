from decimal import Decimal

from twisted.trial.unittest import TestCase

from methanal.util import (
    collectMethods, getArgsDict, Porthole, CurrencyFormatter, DecimalFormatter)



class MethodCollectorTests(TestCase):
    def test_simpleUsage(self):
        class A(object):
            def foo(self):
                return 'A'

        class B(A):
            def foo(self):
                return 'B'

        results = [m() for m in collectMethods(B(), 'foo')]
        self.assertEquals(results, ['B', 'A'])


    def test_missingMethod(self):
        class A(object):
            def foo(self):
                return 'A'

        class B(A):
            pass

        class C(B):
            def foo(self):
                return 'C'

        results = [m() for m in collectMethods(C(), 'foo')]
        self.assertEquals(results, ['C', 'A'])


    def test_noneAttribute(self):
        """
        Test that None attributes named the same as the method we are
        collecting are not silently ignored.
        """
        class A(object):
            foo = None

        class B(A):
            pass

        results1 = list(collectMethods(A(), 'foo'))
        self.assertEquals(len(results1), 1)

        results2 = list(collectMethods(B(), 'foo'))
        self.assertEquals(len(results2), 1)

        self.assertRaises(TypeError, results2[0])


    def test_argumentCollection(self):
        class A(object):
            """
            Test class with correct getArgs implementation.
            """
            def getArgs(self):
                return {u'foo': 1}

        class B(A):
            """
            Another test getArgs implementor.
            """
            def getArgs(self):
                return {u'bar': 2}

        self.assertEquals(getArgsDict(A()), {u'foo': 1})
        self.assertEquals(getArgsDict(B()), {u'foo': 1, u'bar': 2})


    def test_argumentCollision(self):
        class A(object):
            """
            Test class with correct getArgs implementation.
            """
            def getArgs(self):
                return {u'foo': 1}

        class B(A):
            """
            A getArgs implementor with a colliding argument name.
            """
            def getArgs(self):
                return {u'foo': 2}

        self.assertRaises(ValueError, getArgsDict, B())


    def test_argumentNameType(self):
        class A(object):
            """
            A getArgs implementor with an argument name of the wrong type.
            """
            def getArgs(self):
                return {'foo': 1}

        self.assertRaises(TypeError, getArgsDict, A())



class PortholeTests(TestCase):
    """
    Tests for L{Porthole}.
    """
    def setUp(self):
        """
        Set up a basic test porthole.
        """
        self.emitter = Porthole()


    def test_noObservers(self):
        """
        Emitting an event when there are no observers does nothing.
        """
        self.emitter.emitEvent(u'anEvent')
        self.assertEqual(self.emitter.observers, [])


    def test_addObserver(self):
        """
        Invoking C{addObserver} adds an observer to the list, and returns a
        callable that can be used to remove the observer again.
        """
        r = self.emitter.addObserver(None)
        self.assertEqual(self.emitter.observers, [None])
        r()
        self.assertEqual(self.emitter.observers, [])


    def test_twoObservers(self):
        """
        Emitting an event when there are two observers causes two callbacks to
        occur.
        """
        self.observed = 0
        def _obs(event):
            self.observed += 1

        self.emitter.addObserver(_obs)
        self.emitter.addObserver(_obs)
        self.emitter.emitEvent(u'anEvent')
        self.assertEqual(self.observed, 2)
        self.assertEqual(len(self.emitter.observers), 2)


    def test_reentrancy(self):
        """
        Adding or removing observers from within an observer callback have no
        effect on the event currently being emitted.
        """
        def _obs(event):
            self.observed += 1

        def _obsWithRemove(event):
            self.observed += 1
            r()
            r2()

        def _obsWithAdd(event):
            self.observed += 1
            self.emitter.addObserver(_obsWithAdd)

        r = self.emitter.addObserver(_obsWithRemove)
        r2 = self.emitter.addObserver(_obs)

        self.observed = 0
        self.emitter.emitEvent(u'anEvent')
        self.assertEqual(self.observed, 2)
        self.assertEqual(len(self.emitter.observers), 0)

        self.emitter.addObserver(_obsWithAdd)
        self.observed = 0
        self.emitter.emitEvent(u'anEvent')
        self.assertEqual(self.observed, 1)
        self.assertEqual(len(self.emitter.observers), 2)

        self.observed = 0
        self.emitter.emitEvent(u'anEvent')
        self.assertEqual(self.observed, 2)
        self.assertEqual(len(self.emitter.observers), 4)



class DecimalFormatterTests(TestCase):
    """
    Tests for L{methanal.util.DecimalFormatter}.
    """
    def test_formatDefaults(self):
        """
        Formatting a value with the default settings produces a decimal number
        grouped 3 digits at a time.
        """
        f = DecimalFormatter()

        self.assertEquals(
            f.format(u''),
            u'')
        self.assertEquals(
            f.format(u'1'),
            u'1')
        self.assertEquals(
            f.format(u'123'),
            u'123')
        self.assertEquals(
            f.format(u'1234'),
            u'1,234')
        self.assertEquals(
            f.format(u'1234.56'),
            u'1,234.56')
        self.assertEquals(
            f.format(u'123456'),
            u'123,456')
        self.assertEquals(
            f.format(u'12345678'),
            u'12,345,678')
        self.assertEquals(
            f.format(u'1234567.89'),
            u'1,234,567.89')


    def test_formatCustom(self):
        """
        Formatting a value obeys the decimal grouping and separator
        specifications.
        """
        f = DecimalFormatter(grouping=[3, 2, -1])

        self.assertEquals(
            f.format(u''),
            u'')
        self.assertEquals(
            f.format(u'1'),
            u'1')
        self.assertEquals(
            f.format(u'123'),
            u'123')
        self.assertEquals(
            f.format(u'1234'),
            u'1,234')
        self.assertEquals(
            f.format(u'123456'),
            u'1,23,456')
        self.assertEquals(
            f.format(u'123456789'),
            u'1234,56,789')
        self.assertEquals(
            f.format(u'1234567.89'),
            u'12,34,567.89')

        f = DecimalFormatter(
            grouping=[3, 2, -1], thousandsSeparator=u'.',
            decimalSeparator=u',')
        self.assertEquals(
            f.format(u'123456'),
            u'1.23.456')
        self.assertEquals(
            f.format(u'123456789'),
            u'1234.56.789')
        self.assertEquals(
            f.format(u'1234567,89'),
            u'12.34.567,89')


    def test_formatNonString(self):
        """
        L{methanal.util.DecimalFormatter.format} can handle some non-string
        values, such as C{None}, C{int} and C{Decimal}.
        """
        f = DecimalFormatter(grouping=[3, 2, -1])
        self.assertEquals(
            f.format(None),
            u'')
        self.assertEquals(
            f.format(1),
            u'1')
        self.assertEquals(
            f.format(Decimal(123)),
            u'123')
        self.assertEquals(
            f.format(Decimal('1234')),
            u'1,234')

        f = DecimalFormatter(
            grouping=[3, 2, -1], thousandsSeparator=u'.',
            decimalSeparator=u',')
        self.assertEquals(
            f.format(123456),
            u'1.23.456')
        self.assertEquals(
            f.format(123456789),
            u'1234.56.789')



class CurrencyFormatterTests(TestCase):
    """
    Tests for L{methanal.util.CurrencyFormatter}.
    """
    def test_formatDefaults(self):
        """
        Formatting a value with the default settings produces the currency
        symbol followed by one space and the decimal number grouped 3 digits at
        a time.
        """
        f = CurrencyFormatter(u'X')

        self.assertEquals(
            f.format(u'1'),
            u'X 1')
        self.assertEquals(
            f.format(u'1234'),
            u'X 1,234')
        self.assertEquals(
            f.format(u'1234.56'),
            u'X 1,234.56')
        self.assertEquals(
            f.format(u'1234567'),
            u'X 1,234,567')


    def test_formatCustom(self):
        """
        Formatting a value obeys the decimal grouping, separator and currency
        symbol separator specifications.
        """
        f = CurrencyFormatter(
            symbol=u'X', symbolSeparator=u'', grouping=[3, 2, -1])

        self.assertEquals(
            f.format(u'1'),
            u'X1')
        self.assertEquals(
            f.format(u'1234'),
            u'X1,234')
        self.assertEquals(
            f.format(u'1234.56'),
            u'X1,234.56')
        self.assertEquals(
            f.format(u'1234567'),
            u'X12,34,567')
        self.assertEquals(
            f.format(u'1234567890'),
            u'X12345,67,890')
