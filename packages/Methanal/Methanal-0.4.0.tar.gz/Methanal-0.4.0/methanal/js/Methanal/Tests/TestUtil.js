// import Divmod.UnitTest
// import Methanal.Util
// import Methanal.Tests.Util
// import Methanal.Tests.MockBrowser



Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestUtil').methods(
    /**
     * L{Methanal.Util.addElementClass} and L{Methanal.Util.removeElementClass}
     * add and remove values to an element's C{className} attribute.
     */
    function test_addRemoveElementClass(self) {
        var node = document.createElement('div');
        var addElementClass = Methanal.Util.addElementClass;
        var removeElementClass = Methanal.Util.removeElementClass;

        addElementClass(node, 'foo');
        self.assertIdentical(node.className, 'foo');
        addElementClass(node, 'foo');
        self.assertIdentical(node.className, 'foo');

        addElementClass(node, 'bar');
        self.assertIdentical(node.className, 'foo bar');

        removeElementClass(node, 'foo');
        self.assertIdentical(node.className, 'bar');

        removeElementClass(node, 'bar');
        self.assertIdentical(node.className, '');

        removeElementClass(node, 'bar');
        self.assertIdentical(node.className, '');
    },


    /**
     * Create a DOM node with some children.
     */
    function _makeNodeWithChildren(self) {
        var T = Methanal.Util.DOMBuilder(document);
        var node = T('div', {}, [
            T('span', {}, ['hello ',
                T('strong', {}, 'world')]),
            T('em', {}, ['!'])]);
        self.assertIdentical(node.childNodes.length, 2);
        return node;
    },


    /**
     * L{Methanal.Util.removeNodeContent} removes all of a node's children.
     */
    function test_removeNodeContent(self) {
        var node = self._makeNodeWithChildren();
        Methanal.Util.removeNodeContent(node);
        self.assertIdentical(node.childNodes.length, 0);
    },


    /**
     * L{Methanal.Util.replaceNodeContent} replaces a node's children with
     * some other children.
     */
    function test_replaceNodeContent(self) {
        var T = Methanal.Util.DOMBuilder(document);
        var node = self._makeNodeWithChildren();
        var children = [T('strong', {}, ['yay'])];
        Methanal.Util.replaceNodeContent(node, children);
        self.assertArraysEqual(node.childNodes, children);
    },


    /**
     * L{Methanal.Util.replaceNodeText} replaces a node's content with a text
     * node.
     */
    function test_replaceNodeText(self) {
        var node = self._makeNodeWithChildren();
        Methanal.Util.replaceNodeText(node, 'hey');
        self.assertIdentical(node.childNodes.length, 1);
        self.assertIsInstanceOf(node.firstChild, Divmod.MockBrowser.TextNode);
    },


    /**
     * L{Methanal.Util.formatDecimal} pretty-prints a number with thousand
     * separators.
     */
    function test_formatDecimal(self) {
        var formatDecimal = Methanal.Util.formatDecimal;
        self.assertIdentical(formatDecimal(1), '1');
        self.assertIdentical(formatDecimal(100), '100');
        self.assertIdentical(formatDecimal(1000), '1,000');
        self.assertIdentical(formatDecimal(10000), '10,000');
        self.assertIdentical(formatDecimal(1000000), '1,000,000');

        self.assertIdentical(formatDecimal(1000.25), '1,000.25');
        self.assertIdentical(formatDecimal(1000000.66), '1,000,000.66');
    },


    /**
     * L{Methanal.Util.cycle} produces a callable that iterates through
     * the original arguments indefinitely.
     */
    function test_cycle(self) {
        var cycler = Methanal.Util.cycle(42, 5144, 'a');
        self.assertIdentical(cycler(), 42);
        self.assertIdentical(cycler(), 5144);
        self.assertIdentical(cycler(), 'a');
        self.assertIdentical(cycler(), 42);
    },


    /**
     * L{Methanal.Util.arrayIndexOf} finds the first index of an element in an
     * array, or C{-1} if no such element exists.
     */
    function test_arrayIndexOf(self) {
        var arrayIndexOf = Methanal.Util.arrayIndexOf;
        var a = ['x', 'y', 'z', 'x'];
        self.assertIdentical(arrayIndexOf(a, 'x'), 0);
        self.assertIdentical(arrayIndexOf(a, 'y'), 1);
        self.assertIdentical(arrayIndexOf(a, 'z'), 2);
        self.assertIdentical(arrayIndexOf(a, 'a'), -1);
    },


    /**
     * L{Methanal.Util.nodeInserted} calls a widget's C{nodeInserted} method
     * and the C{nodeInserted} method of each child widget.
     */
    function test_nodeInserted(self) {
        function makeWidget(childWidgets) {
            return {
                'childWidgets': childWidgets,
                'nodeInserted': function () {
                    this.nodeInserted = true;
                }};
        }

        var childWidgets = [];
        for (var i = 0; i < 5; ++i) {
            childWidgets.push(makeWidget([]));
        }
        var widget = makeWidget(childWidgets);

        Methanal.Util.nodeInserted(widget);
        self.assertIdentical(widget.nodeInserted, true);
        for (var i = 0; i < childWidgets.length; ++i) {
            self.assertIdentical(childWidgets[i].nodeInserted, true);
        }
    },


    /**
     * L{Methanal.Util.repr} converts an object to a human-readable string.
     */
    function test_repr(self) {
        var repr = Methanal.Util.repr;
        self.assertIdentical(repr('a'), '"a"');
        self.assertIdentical(repr('a"b"c'), '"a\\"b\\"c"');
        self.assertIdentical(repr(1), '1');
        self.assertIdentical(repr(null), 'null');
        self.assertIdentical(repr(undefined), 'undefined');
        self.assertIdentical(repr(repr), '<function repr>');
        var a = [1, 2, 3, 'a', ['b', '"c"']];
        self.assertIdentical(repr(a), '[1, 2, 3, "a", ["b", "\\"c\\""]]');
        var o = {a: 1};
        self.assertIdentical(repr(o), '{"a": 1}');
        var o2 = {a: 1, b: 2};
        self.assertIdentical(repr(o2), '{"a": 1, "b": 2}');

        var type = Divmod.Class.subclass('Foo');
        var i = type();
        self.assertIdentical(repr(i), i.toString());
    },


    /**
     * Return C{true} iff the given string represents a base-10 numerical value.
     */
    function test_isNumericalString(self) {
        var CASES = [
            ['1234',    true],
            ['1.23',    true],
            ['0',       true],
            ['01',      true],
            [1234,      false],
            [1.23,      false],
            ['0x1',     false],
            ['abc',     false],
            [null,      false],
            [undefined, false]];
        Methanal.Tests.Util.assertCases(
            self, Methanal.Util.isNumericalString, CASES);
    },


    /**
     * L{Methanal.Util.strToInt} converts a base-10 integer value, represented
     * as a C{String}, to an C{Integer}.
     */
    function test_strToInt(self) {
        var CASES = [
            ['1234', 1234],
            ['01234', 1234],
            ['001234', 1234],
            ['019', 19],
            ['123abc', undefined],
            ['abc123', undefined],
            ['0x123', undefined]];
        Methanal.Tests.Util.assertCases(self, Methanal.Util.strToInt, CASES);
    },


    /**
     * L{Methanal.Util.strToFloat} converts a float value, represented
     * as a C{String}, to a floating point C{Number}.
     */
    function test_strToFloat(self) {
        var CASES = [
            ['1234',      1234],
            ['01234.56',  1234.56],
            ['.0',        0],
            ['.5',        0.5],
            ['-1',        -1],
            ['123.45abc', undefined],
            ['abc123.45', undefined],
            ['0x123',     undefined]];
        Methanal.Tests.Util.assertCases(self, Methanal.Util.strToFloat, CASES);
    },


    /**
     * Applies a function of two arguments cumulatively to the elements of a
     * list from left to right, so as to reduce the list to a single value.
     */
    function test_reduce(self) {
        var reduce = Methanal.Util.reduce;

        function add(x, y) {
            return x + y;
        }

        function multiply(x, y) {
            return x * y;
        }

        self.assertIdentical(reduce(add, [1, 2, 3]), 6);
        self.assertIdentical(reduce(multiply, [1, 2, 3], 10), 60);
        self.assertThrows(Error, function () { return reduce(add, []); });
        self.assertIdentical(reduce(add, [], 10), 10);
        self.assertIdentical(reduce(add, [10]), 10);
    },


    /**
     * Test L{Methanal.Util._reprString} correctly escapes various whitespace
     * characters.
     */
    function test_reprString(self) {
        var s = '\r\n\f\b\t';
        var repr = Methanal.Util._reprString(s);
        var expected = "\"\\r\\n\\f\\b\\t\"";
        self.assertIdentical(repr, expected);
    },


    /**
     * Right justifying a string pads it with the first character of the fill
     * character parameter to the specified length.
     */
    function test_rjust(self) {
        var rjust = Methanal.Util.rjust;
        self.assertIdentical(rjust('a', 0), 'a');
        self.assertIdentical(rjust('a', 1), 'a');
        self.assertIdentical(rjust('a', 2), ' a');
        self.assertIdentical(rjust('a', 2, 'b'), 'ba');
        self.assertIdentical(rjust('a', 3, 'b'), 'bba');
        self.assertIdentical(rjust('a', 3, 'b'), 'bba');
        self.assertIdentical(rjust('a', 3, 'xy'), 'xxa');
        var s = 'a';
        self.assertIdentical(rjust(s, 2), ' a');
        self.assertIdentical(s, 'a');
    },


    /**
     * Applying a function over a sequence. Passing a non-function argument
     * throws an error.
     */
    function test_map(self) {
        var seq = [1, 2, 3];
        function square(n) {
            return n * n;
        }
        var result = Methanal.Util.map(square, seq);
        self.assertArraysEqual(result, [1, 4, 9]);

        self.assertThrows(Error,
            function () { Methanal.Util.map(null, seq); });
    },


    /**
     * Find the quotient and remainder of two numbers.
     */
    function test_divmod(self) {
        self.assertArraysEqual(
            Methanal.Util.divmod(12, 12),
            [1, 0]);
        self.assertArraysEqual(
            Methanal.Util.divmod(0, 12),
            [0, 0]);
        self.assertArraysEqual(
            Methanal.Util.divmod(1, 12),
            [0, 1]);
        self.assertArraysEqual(
            Methanal.Util.divmod(23, 12),
            [1, 11]);
    },


    /**
     * L{Methanal.Util.nthItem} applies a function to the nth item in an
     * C{Array}.
     */
    function test_nthItem(self) {
        var seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

        function gatherNth(start, n) {
            var res = [];
            Methanal.Util.nthItem(seq, start, n, function (v) {
                res.push(v);
            });
            return res;
        }

        self.assertArraysEqual(
            gatherNth(-1, 3),
            [3, 2, 1]);

        self.assertArraysEqual(
            gatherNth(1, 0),
            seq);

        self.assertArraysEqual(
            gatherNth(2, 0),
            [2, 4, 6, 8, 10]);

        self.assertArraysEqual(
            gatherNth(2, 1),
            [1, 3, 5, 7, 9]);

        self.assertArraysEqual(
            gatherNth(3, 3),
            [3, 6, 9]);

        self.assertArraysEqual(
            gatherNth(100, 0),
            []);

        self.assertArraysEqual(
            gatherNth(100, 1),
            [1]);
    },


    /**
     * L{Methanal.Util.filter} gathers only those elements from a sequence for
     * which the predicate is true. A predicate of C{null} will filter values
     * whose truth value is false, e.g. C{0}, C{''} etc.  A predicate of
     * C{undefined} will filter values that are C{null} or C{undefined}.
     * Otherwise the predicate must be a function.
     */
    function test_filter(self) {
        var filter = Methanal.Util.filter;
        var seq = [0, undefined, 1, null, 2, '', 3];

        function isOdd(x) {
            return x % 2 !== 0;
        }

        self.assertArraysEqual(
            filter(null, seq),
            [1, 2, 3]);

        self.assertArraysEqual(
            filter(undefined, seq),
            [0, 1, 2, '', 3]);

        self.assertArraysEqual(
            filter(isOdd, filter(null, seq)),
            [1, 3]);

        self.assertThrows(Error,
            function () { filter('hello', seq); });
    },


    /**
     * L{Methanal.Util.trimLeft} trims leading whitespace,
     * L{Methanal.Util.trimRight} trims trailing whitespace and
     * L{Methanal.Util.trim} trims trailing and leading whitespace.
     */
    function test_trim(self) {
        var s = '  foo bar baz ';
        var t = 'foo';

        self.assertIdentical(
            Methanal.Util.trimLeft(s),
            'foo bar baz ');
        self.assertIdentical(
            Methanal.Util.trimLeft(t), t);

        self.assertIdentical(
            Methanal.Util.trimRight(s),
            '  foo bar baz');
        self.assertIdentical(
            Methanal.Util.trimRight(t), t);

        self.assertIdentical(
            Methanal.Util.trim(s),
            'foo bar baz');
        self.assertIdentical(
            Methanal.Util.trim(t), t);
    },


    /**
     * Create a new function with partial application of the given arguments.
     */
    function test_partial(self) {
        function add(a, b) {
            return a + b;
        }
        var p = Methanal.Util.partial(add, 2);
        self.assertIdentical(p(2), 4);
        self.assertIdentical(p(3), 5);
    },


    /**
     * L{Methanal.Util.split} splits a C{String} on a C{String} delimiter,
     * optionally limiting the number of splits that occur and returning the
     * remainder of the string, unsplit, as the final component of an C{Array}.
     */
    function test_split(self) {
        var split = Methanal.Util.split;

        self.assertArraysEqual(
            split('foo bar  baz', ' '),
            ['foo', 'bar', '', 'baz']);

        self.assertArraysEqual(
            split('foo bar  baz', ' '),
            'foo bar  baz'.split(' '));

        self.assertArraysEqual(
            split('foo bar  baz', ' ', 1),
            ['foo', 'bar  baz']);

        self.assertArraysEqual(
            split('foo bar  baz', ' ', 2),
            ['foo', 'bar', ' baz']);

        self.assertArraysEqual(
            split('foo bar  baz', ' ', 3),
            split('foo bar  baz', ' '));
    },


    /**
     * Pipeline the result of one function, to the input of another, beginning
     * with the innermost function.
     */
    function test_compose(self) {
        function addFive(n) {
            return n + 5;
        }

        function timesTen(n) {
            return n * 10;
        }

        var compose = Methanal.Util.compose;
        self.assertIdentical(
            compose(addFive)(3),
            8);

        self.assertIdentical(
            compose(addFive, timesTen)(3),
            35);

        self.assertIdentical(
            compose(timesTen, addFive)(3),
            80);

        self.assertIdentical(
            compose(timesTen, addFive, timesTen)(4),
            450);

        self.assertThrows(Error, compose);
    },


    /**
     * Create a callable that will call the original callable with a sequence
     * from varargs.
     */
    function test_unapply(self) {
        var f = Methanal.Util.partial(
            Methanal.Util.reduce, function (a, b) { return a + b; });
        self.assertIdentical(
            Methanal.Util.unapply(f)(1, 2, 3),
            6);
    },


    /**
     * Pluralise a word.
     */
    function test_plural(self) {
        var plural = Methanal.Util.plural;
        self.assertIdentical(
            plural(1, 'hammer'),
            'hammer');
        self.assertIdentical(
            plural(0, 'hammer'),
            'hammers');
        self.assertIdentical(
            plural(2, 'hammer'),
            'hammers');
        self.assertIdentical(
            plural(-1, 'hammer'),
            'hammers');
        self.assertIdentical(
            plural(2, 'fix', 'fixes'),
            'fixes');
    });



Divmod.UnitTest.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestStringSet').methods(
    /**
     * Supplying no parameters creates an empty set.
     */
    function test_empty(self) {
        var s = Methanal.Util.StringSet();
        s.each(function () {
            self.assert(false, 'Set is not empty');
        });
    },


    /**
     * L{Methanal.Util.StringSet.each} applies a function over all elements
     * of the set.
     */
    function test_each(self) {
        var called = 0;
        var values = ['a', 'b'];
        var s = Methanal.Util.StringSet(values);
        s.each(function (name) {
            var index = Methanal.Util.arrayIndexOf(values, name);
            self.assert(index !== -1, '"' + name + '" should be in the set!');
            values.splice(index, 1);
            called += 1;
        });
        self.assertIdentical(called, 2);
        self.assertIdentical(values.length, 0);
    },


    /**
     * L{Methanal.Util.StringSet.contains} correctly reports the presence of
     * a value in the set.
     */
    function test_contains(self) {
        var s = Methanal.Util.StringSet(['a', 'b']);
        self.assertIdentical(s.contains('a'), true);
        self.assertIdentical(s.contains('b'), true);
        self.assertIdentical(s.contains('c'), false);
    });



Divmod.UnitTest.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestTimeDelta').methods(
    /**
     * L{Methanal.Util.TimeDelta.offset} correctly specifies a given duration
     * in milliseconds.
     */
    function test_offset(self) {
        var td;
        td = Methanal.Util.TimeDelta({'days': 1});
        self.assertIdentical(td.offset, 1000 * 3600 * 24);

        td = Methanal.Util.TimeDelta({'days': -1});
        self.assertIdentical(td.offset, 1000 * 3600 * -24);

        td = Methanal.Util.TimeDelta({'days': 1,
                                      'hours': 2});
        self.assertIdentical(td.offset, 1000 * 3600 * 26);

        td = Methanal.Util.TimeDelta({'days': 1,
                                      'hours': 2,
                                      'minutes': 3});
        self.assertIdentical(td.offset, 1000 * (3600 * 26 + 60 * 3));

        td = Methanal.Util.TimeDelta({'days': 1,
                                      'hours': 2,
                                      'minutes': 3,
                                      'seconds': 4});
        self.assertIdentical(td.offset, 1000 * (3600 * 26 + 60 * 3 + 4));

        td = Methanal.Util.TimeDelta({'days': 1,
                                      'hours': 2,
                                      'minutes': 3,
                                      'seconds': 4,
                                      'milliseconds': 5});
        self.assertIdentical(td.offset, 1000 * (3600 * 26 + 60 * 3 + 4) + 5);
    },


    /**
     * L{Methanal.Util.TimeDelta.asHumanly} accurately represents delta values
     * in a human readable form.
     */
    function test_asHumanly(self) {
        function asHumanly(deltas) {
            return Methanal.Util.TimeDelta(deltas).asHumanly();
        }

        self.assertIdentical(
            asHumanly({'days': 1}),
            '1 day');

        self.assertIdentical(
            asHumanly({'days': -1}),
            '1 day ago');

        self.assertIdentical(
            asHumanly({'days': 1,
                       'hours': 2}),
            '1 day, 2 hours');

        self.assertIdentical(
            asHumanly({'days': 1,
                       'hours': 2,
                       'minutes': 3}),
            '1 day, 2 hours, 3 minutes');

        self.assertIdentical(
            asHumanly({'days': 1,
                       'hours': 2,
                       'minutes': 3,
                       'seconds': 4}),
            '1 day, 2 hours, 3 minutes, 4 seconds');

        self.assertIdentical(
            asHumanly({'days': 1,
                       'hours': 2,
                       'minutes': 3,
                       'seconds': 4,
                       'milliseconds': 5}),
            '1 day, 2 hours, 3 minutes, 4 seconds, 5 milliseconds');
    });



/**
 * Tests for L{Methanal.Util.Time}.
 *
 * @type _knownTime: L{Methanal.Util.Time}
 * @ivar _knownTime: A known point in time
 */
Divmod.UnitTest.TestCase.subclass(Methanal.Tests.TestUtil, 'TestTime').methods(
    function setUp(self) {
        self._knownTime = Methanal.Util.Time.fromDate(
            new Date(2009, 8, 6, 1, 36, 23, 2));
    },


    /**
     * L{Methanal.Util.Time.guess} creates a L{Methanal.Util.Time} instance
     * when given an input format it can parse.
     */
    function test_guess(self) {
        function assertTimeParsed(data, timestamp) {
            var time = Methanal.Util.Time.guess(data);
            self.assertIdentical(time._oneDay, true);
            // User input is interpreted as local time, but the tests should
            // pass regardless of the runner's local timezone, so we use UTC
            // dates.
            self.assertIdentical(time.asUTCDate().getTime(), timestamp);
        }

        assertTimeParsed('2009/9/1',   1251763200000);
        assertTimeParsed('2009.09.01', 1251763200000);
        assertTimeParsed('2009-09-01', 1251763200000);
        assertTimeParsed('1/9/2009',   1251763200000);
        assertTimeParsed('01.09.2009', 1251763200000);
        assertTimeParsed('01-09-2009', 1251763200000);
        assertTimeParsed('1/9/2009',   1251763200000);
        assertTimeParsed('29/2/2008',  1204243200000);
    },


    /**
     * L{Methanal.Util.Time.guess} throws L{Methanal.Util.TimeParseError} when
     * the input is not in any recognisable format, and reraises the original
     * exception if something other than L{Methanal.Util.TimeParseError} occurs.
     */
    function test_guessFailure(self) {
        function assertTimeParseError(data) {
            self.assertThrows(
                Methanal.Util.TimeParseError,
                function() { return Methanal.Util.Time.guess(data); });
        }

        assertTimeParseError('');
        assertTimeParseError('hello');
        assertTimeParseError('1/2/3');
        assertTimeParseError('2009/01');
        assertTimeParseError('2009/01');
        assertTimeParseError('2009/01/32');
        assertTimeParseError('2009/02/29');

        self.assertThrows(
            TypeError,
            function() { return Methanal.Util.Time.guess(undefined); });
    },


    /**
     * Create a L{Methanal.Util.Time} instance from a C{Date}.
     */
    function test_fromDate(self) {
        var d = new Date(2009, 8, 1, 12, 34, 56, 78);
        var t = Methanal.Util.Time.fromDate(d);
        self.assertIdentical(t.asDate().getTime(), d.getTime());
    },


    /**
     * Create a L{Methanal.Util.Time} instance from a valid relative time
     * reference, while invalid references throw
     * L{Methanal.Util.TimeParseError}.
     */
    function test_fromRelative(self) {
        var today = self._knownTime;

        var t;
        t = Methanal.Util.Time.fromRelative('tomorrow', today);
        self.assertIdentical(t.asHumanly(), 'Mon, 7 Sep 2009');
        t = Methanal.Util.Time.fromRelative('yesterday', today);
        self.assertIdentical(t.asHumanly(), 'Sat, 5 Sep 2009');
        t = Methanal.Util.Time.fromRelative('today', today);
        self.assertIdentical(t.asHumanly(), 'Sun, 6 Sep 2009');

        t = Methanal.Util.Time.fromRelative('sun', today);
        self.assertIdentical(t.asHumanly(), 'Sun, 13 Sep 2009');
        t = Methanal.Util.Time.fromRelative('mon', today);
        self.assertIdentical(t.asHumanly(), 'Mon, 7 Sep 2009');
        t = Methanal.Util.Time.fromRelative('satur', today);
        self.assertIdentical(t.asHumanly(), 'Sat, 12 Sep 2009');

        self.assertThrows(
            Methanal.Util.TimeParseError,
            function() {
                return Methanal.Util.Time.fromRelative('', today);
            });
        self.assertThrows(
            Methanal.Util.TimeParseError,
            function() {
                return Methanal.Util.Time.fromRelative('hello', today);
            });
    },


    /**
     * Create a L{Methanal.Util.Time} instance from a timestamp in milliseconds.
     */
    function test_fromTimestamp(self) {
        var t;
        var timestamp;

        timestamp = 1251766923000;
        t = Methanal.Util.Time.fromTimestamp(timestamp);
        self.assertIdentical(t.asDate().getTime(), timestamp);
        self.assertIdentical(t._timezoneOffset, 0);

        var d = new Date();
        timestamp = d.getTime();
        t = Methanal.Util.Time.fromTimestamp(timestamp, d.getTimezoneOffset());
        self.assertIdentical(t.asDate().getTime(), timestamp);
        self.assertIdentical(
            t._timezoneOffset, d.getTimezoneOffset() * 60 * 1000);

        var now = Methanal.Util.Time();
        self.assertIdentical(
            now.asTimestamp(),
            Methanal.Util.Time.fromTimestamp(now.asTimestamp()).asTimestamp());
    },


    /**
     * L{Methanal.Util.Time.asDate} converts a Time into a C{Date} representing
     * the same I{local} time.
     */
    function test_asDate(self) {
        var t = Methanal.Util.Time();
        var d = t.asDate();
        self.assertIdentical(
            t.asTimestamp(), d.getTime());
    },


    /**
     * L{Methanal.Util.Time.asTimestamp} converts a Time into the number of
     * milliseconds elapsed since the epoch.
     */
    function test_asTimestamp(self) {
        self.assertIdentical(self._knownTime.asTimestamp(), 1252193783002);
    },


    /**
     * L{Methanal.Util.Time.asHumanly} converts a Time into a human-readable
     * string. Times that have been truncated to a date have an appropriately
     * accurate human-readable version.
     */
    function test_asHumanly(self) {
        self.assertIdentical(
            self._knownTime.asHumanly(), 'Sun, 6 Sep 2009 01:36:23 am');
        self.assertIdentical(
            self._knownTime.asHumanly(true), 'Sun, 6 Sep 2009 01:36:23');
        self.assertIdentical(
            self._knownTime.oneDay().asHumanly(), 'Sun, 6 Sep 2009');

        var t;

        t = Methanal.Util.Time.fromDate(new Date(2000, 0, 1, 0, 1, 2));
        self.assertIdentical(
            t.asHumanly(), 'Sat, 1 Jan 2000 12:01:02 am');
        self.assertIdentical(
            t.asHumanly(true), 'Sat, 1 Jan 2000 00:01:02');

        t = Methanal.Util.Time.fromDate(new Date(2000, 0, 1, 12, 13, 14));
        self.assertIdentical(
            t.asHumanly(), 'Sat, 1 Jan 2000 12:13:14 pm');
        self.assertIdentical(
            t.asHumanly(true), 'Sat, 1 Jan 2000 12:13:14');

        t = Methanal.Util.Time.fromDate(new Date(2000, 0, 1, 22, 23, 24));
        self.assertIdentical(
            t.asHumanly(), 'Sat, 1 Jan 2000 10:23:24 pm');
        self.assertIdentical(
            t.asHumanly(true), 'Sat, 1 Jan 2000 22:23:24');
    },


    /**
     * L{Methanal.Util.Time.oneDay} truncates a Time to only a date.
     */
    function test_oneDay(self) {
        var t = Methanal.Util.Time();
        var od = t.oneDay().asDate();
        t = t.asDate();
        self.assertIdentical(od.getFullYear(), t.getFullYear());
        self.assertIdentical(od.getMonth(), t.getMonth());
        self.assertIdentical(od.getDate(), t.getDate());
        self.assertIdentical(od.getHours(), 0);
        self.assertIdentical(od.getMinutes(), 0);
        self.assertIdentical(od.getSeconds(), 0);
        self.assertIdentical(od.getMilliseconds(), 0);
    },


    /**
     * L{Methanal.Util.Time.offset} offsets a Time by the given number of
     * milliseconds.
     */
    function test_offset(self) {
        var t;
        t = self._knownTime.offset(
            Methanal.Util.TimeDelta({'days': -1}));
        self.assertIdentical(t.asTimestamp(), 1252107383002);
        self.assertIdentical(t.oneDay().asHumanly(), 'Sat, 5 Sep 2009');

        t = self._knownTime.offset(
            Methanal.Util.TimeDelta({'days': 1}));
        self.assertIdentical(t.asTimestamp(), 1252280183002);
        self.assertIdentical(t.oneDay().asHumanly(), 'Mon, 7 Sep 2009');
    });



/**
 * Tests for L{Methanal.Util.Throbber}.
 */
Divmod.UnitTest.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestThrobber').methods(
    function _createThrobber(self) {
        var widget = Nevow.Athena.Widget(
            Nevow.Test.WidgetUtil.makeWidgetNode());
        var throbberNode = Methanal.Tests.Util.makeWidgetChildNode(
            widget, 'img', 'throbber');
        document.body.appendChild(widget.node);
        return Methanal.Util.Throbber(widget);
    },


    /**
     * Creating a throbber finds a DOM node with the ID "throbber".
     */
    function test_create(self) {
        var throbber = self._createThrobber();
        self.assertIdentical(throbber.node.tagName, 'IMG');
    },


    /**
     * Starting and stopping the throbber, under normal conditions, adjusts the
     * throbber node's visibility style.
     */
    function test_startStop(self) {
        var throbber = self._createThrobber();
        throbber.start();
        self.assertIdentical(
            Methanal.Util.containsElementClass(throbber.node, 'hidden'),
            false);
        throbber.stop();
        self.assertIdentical(
            Methanal.Util.containsElementClass(throbber.node, 'hidden'),
            true);
    });



/**
 * Tests for L{Methanal.Util.DOMBuilder}.
 */
Divmod.UnitTest.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestDOMBuilder').methods(
    /**
     * Helper function for building a node using C{DOMBuilder}.
     */
    function _build(self/*, ...*/) {
        var T = Methanal.Util.DOMBuilder(document);
        var args = [];
        for (var i = 1; i < arguments.length; ++i) {
            args.push(arguments[i]);
        }
        return T.apply(null, args);
    },


    /**
     * Building an element with a tag name.
     */
    function test_element(self) {
        var node = self._build('foo');
        self.assertIdentical(node.tagName, 'FOO');
    },


    /**
     * Building an element with children that are strings results in text nodes.
     */
    function test_textChild(self) {
        var node = self._build('foo', {}, ['hello']);
        self.assertIdentical(node.childNodes.length, 1);
        self.assertIdentical(node.childNodes[0].nodeType, node.TEXT_NODE);
        self.assertIdentical(node.childNodes[0].nodeValue, 'hello');
    },


    /**
     * Passing an attribute mapping results in an element with the specified
     * attributes.
     */
    function test_attributes(self) {
        var node = self._build('foo',
            {'id':    'an_id',
             'class': 'a_class',
             'foo':   'bar'},
            ['hello']);

        self.assertIdentical(node.getAttribute('id'), 'an_id');
        self.assertIdentical(node.getAttribute('class'), 'a_class');
        self.assertIdentical(node.getAttribute('foo'), 'bar');
    },


    /**
     * Copy properties from one object to another.
     */
    function test_copyProperties(self) {
        var src = {'a': 5};
        var dst = {'b': 6};
        Methanal.Util.copyProperties(src, dst);
        self.assertIdentical(dst.b, 6);
        self.assertIdentical(dst.a, 5);
    });



/**
 * Tests for L{Methanal.Util.DateFormatter}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestDateFormatter').methods(
    /**
     * Formatting a C{Date} produces a human readable version of the date.
     */
    function test_formatDefaults(self) {
        var f = Methanal.Util.DateFormatter();

        self.assertIdentical(
            f.format(null),
            '');

        self.assertIdentical(
            f.format(new Date(2009, 0, 1)),
            'Thu, 1 Jan 2009');
    });



/**
 * Tests for L{Methanal.Util.DecimalFormatter}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestDecimalFormatter').methods(
    /**
     * Formatting a value with the default settings produces a decimal number
     * grouped 3 digits at a time.
     */
    function test_formatDefaults(self) {
        var f = Methanal.Util.DecimalFormatter();

        self.assertIdentical(
            f.format(''),
            '');
        self.assertIdentical(
            f.format('1'),
            '1');
        self.assertIdentical(
            f.format('123'),
            '123');
        self.assertIdentical(
            f.format('1234'),
            '1,234');
        self.assertIdentical(
            f.format('1234.56'),
            '1,234.56');
        self.assertIdentical(
            f.format('123456'),
            '123,456');
        self.assertIdentical(
            f.format('12345678'),
            '12,345,678');
        self.assertIdentical(
            f.format('1234567.89'),
            '1,234,567.89');
    },


    /**
     * Formatting a value obeys the decimal grouping and separator
     * specifications.
     */
    function test_formatCustom(self) {
        var f = Methanal.Util.DecimalFormatter([3, 2, -1]);

        self.assertIdentical(
            f.format(''),
            '');
        self.assertIdentical(
            f.format('1'),
            '1');
        self.assertIdentical(
            f.format('123'),
            '123');
        self.assertIdentical(
            f.format('1234'),
            '1,234');
        self.assertIdentical(
            f.format('123456'),
            '1,23,456');
        self.assertIdentical(
            f.format('123456789'),
            '1234,56,789');

        f = Methanal.Util.DecimalFormatter(
            [3, 2, -1], '.', ',');
        self.assertIdentical(
            f.format('123456'),
            '1.23.456');
        self.assertIdentical(
            f.format('123456789'),
            '1234.56.789');
        self.assertIdentical(
            f.format('1234567,89'),
            '12.34.567,89');
    });



/**
 * Tests for L{Methanal.Util.PercentageFormatter}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestPercentageFormatter').methods(
    /**
     * Formatting a value with the default settings produces a digit-grouped
     * decimal followed by a percentage symbol C{'%'}.
     */
    function test_formatDefaults(self) {
        var f = Methanal.Util.PercentageFormatter();

        self.assertIdentical(
            f.format(0.01),
            '1%');
        self.assertIdentical(
            f.format(12.34),
            '1,234%');
        self.assertIdentical(
            f.format(12.3456),
            '1,234.56%');
    },


    /**
     * Formatting a value obeys the decimal grouping and separator
     * specifications.
     */
    function test_formatCustom(self) {
        var f = Methanal.Util.PercentageFormatter([2, -1]);

        self.assertIdentical(
            f.format(0.01),
            '1%');
        self.assertIdentical(
            f.format(12.34),
            '12,34%');
        self.assertIdentical(
            f.format(123.4567),
            '123,45.67%');
    });



/**
 * Tests for L{Methanal.Util.CurrencyFormatter}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestUtil, 'TestCurrencyFormatter').methods(
    /**
     * Formatting a value with the default settings produces the currency
     * symbol followed by one space and the decimal number grouped 3 digits at
     * a time.
     */
    function test_formatDefaults(self) {
        var f = Methanal.Util.CurrencyFormatter('X');

        self.assertIdentical(
            f.format('1'),
            'X 1');
        self.assertIdentical(
            f.format('1234'),
            'X 1,234');
        self.assertIdentical(
            f.format('1234.56'),
            'X 1,234.56');
        self.assertIdentical(
            f.format('1234567'),
            'X 1,234,567');
    },


    /**
     * Formatting a value obeys the decimal grouping, separator and currency
     * symbol separator specifications.
     */
    function test_formatCustom(self) {
        var f = Methanal.Util.CurrencyFormatter('X', '', [3, 2, -1]);

        self.assertIdentical(
            f.format('1'),
            'X1');
        self.assertIdentical(
            f.format('1234'),
            'X1,234');
        self.assertIdentical(
            f.format('1234.56'),
            'X1,234.56');
        self.assertIdentical(
            f.format('1234567'),
            'X12,34,567');
        self.assertIdentical(
            f.format('1234567890'),
            'X12345,67,890');
    });
