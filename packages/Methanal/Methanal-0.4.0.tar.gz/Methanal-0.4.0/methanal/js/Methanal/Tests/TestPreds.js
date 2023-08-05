// import Divmod.UnitTest
// import Methanal.Preds
// import Methanal.Util
// import Methanal.Tests.Util



/**
 * Return C{true}.
 */
Methanal.Tests.TestPreds.T = function T() {
    return true;
};



/**
 * Return C{false}.
 */
Methanal.Tests.TestPreds.F = function F() {
    return false;
};



Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestPreds, 'PredsTestCase').methods(
    /**
     * Assert that C{value} predicates C{pred}.
     */
    function assertTrue(self, pred /*...*/) {
        var args = Array.prototype.slice.call(arguments, 2);
        self.assertIdentical(pred.apply(null, args), true,
            'Predicate is false for ' + Methanal.Util.repr(pred));
    },


    /**
     * Assert that C{value} does not predicate C{pred}.
     */
    function assertFalse(self, pred /*...*/) {
        var args = Array.prototype.slice.call(arguments, 2);
        self.assertIdentical(pred.apply(null, args), false,
            'Predicate is true for ' + Methanal.Util.repr(pred));
    });



Methanal.Tests.TestPreds.PredsTestCase.subclass(
    Methanal.Tests.TestPreds, 'TestPreds').methods(
    /**
     * Predicate is inverted.
     */
    function test_invert(self) {
        var x = Methanal.Preds.invert(
            Methanal.Util.partial(Methanal.Preds.lengthOf(3)));
        self.assertTrue(x, 'a');
        self.assertTrue(x, 'ab');
        self.assertFalse(x, 'abc');
        self.assertTrue(x, 'abcd');
    },


    /**
     * Gather the results of functions and combine them.
     */
    function test_combine(self) {
        function nonzero(value) { return value !== 0; }
        function even(value) { return value % 2 === 0; }
        function odd(value) { return value % 2 !== 0; }

        var isEven = Methanal.Preds.combine(
            Methanal.Preds.AND, [Methanal.Preds.notNull, nonzero, even]);
        var isOdd = Methanal.Preds.combine(
            Methanal.Preds.AND, [Methanal.Preds.notNull, nonzero, odd]);
        self.assertTrue(isEven, 2);
        self.assertTrue(isEven, 24);
        self.assertTrue(isOdd, 3);
        self.assertTrue(isOdd, 33);
        self.assertFalse(isEven, 0);
        self.assertFalse(isOdd, 0);
        self.assertFalse(isEven, null);
        self.assertFalse(isOdd, null);
    },


    /**
     * Logically AND values together.
     */
    function test_AND(self) {
        var AND = Methanal.Preds.AND;
        self.assertTrue(AND, [true]);
        self.assertTrue(AND, [true, true]);
        self.assertFalse(AND, [false]);
        self.assertFalse(AND, [false, false]);
        self.assertFalse(AND, [false, true]);
    },


    /**
     * Logical intersection of combined predicate results.
     */
    function test_intersection(self) {
        var intersection = Methanal.Preds.intersection;
        var T = Methanal.Tests.TestPreds.T, F = Methanal.Tests.TestPreds.F;
        self.assertTrue(intersection([T]));
        self.assertTrue(intersection([T, T]));
        self.assertFalse(intersection([F]));
        self.assertFalse(intersection([F, F]));
        self.assertFalse(intersection([F, T]));
    },


    /**
     * Logically OR values together.
     */
    function test_OR(self) {
        var OR = Methanal.Preds.OR;
        self.assertTrue(OR, [true]);
        self.assertTrue(OR, [true, true]);
        self.assertFalse(OR, [false]);
        self.assertFalse(OR, [false, false]);
        self.assertTrue(OR, [false, true]);
    },


    /**
     * Logical union of combined predicate results.
     */
    function test_union(self) {
        var union = Methanal.Preds.union;
        var T = Methanal.Tests.TestPreds.T, F = Methanal.Tests.TestPreds.F;
        self.assertTrue(union([T]));
        self.assertTrue(union([T, T]));
        self.assertFalse(union([F]));
        self.assertFalse(union([F, F]));
        self.assertTrue(union([F, T]));
    },


    /**
     * Logically XOR values together.
     *
     * @type  values: C{Array} of C{Boolean}.
     */
    function test_XOR(self) {
        var XOR = Methanal.Preds.XOR;
        self.assertTrue(XOR, [true]);
        self.assertFalse(XOR, [true, true]);
        self.assertFalse(XOR, [false]);
        self.assertFalse(XOR, [false, false]);
        self.assertTrue(XOR, [false, true]);
    },


    /**
     * Logical symmetric difference of combined predicate results.
     */
    function test_symmetricDifference(self) {
        var symmetricDifference = Methanal.Preds.symmetricDifference;
        var T = Methanal.Tests.TestPreds.T, F = Methanal.Tests.TestPreds.F;
        self.assertTrue(symmetricDifference([T]));
        self.assertFalse(symmetricDifference([T, T]));
        self.assertFalse(symmetricDifference([F]));
        self.assertFalse(symmetricDifference([F, F]));
        self.assertTrue(symmetricDifference([F, T]));
    },


    /**
     * Value is C{true} when evaluated as a boolean.
     */
    function test_isTrue(self) {
        var isTrue = Methanal.Preds.isTrue;
        self.assertTrue(isTrue, 'hello');
        self.assertTrue(isTrue, 42);
        self.assertTrue(isTrue, []);
        self.assertTrue(isTrue, [1]);
        self.assertFalse(isTrue, null);
        self.assertFalse(isTrue, '');
        self.assertFalse(isTrue, 0);
    },


    /**
     * Value is C{false} when evaluated as a boolean.
     */
    function test_isFalse(self) {
        var isFalse = Methanal.Preds.isFalse;
        self.assertFalse(isFalse, 'hello');
        self.assertFalse(isFalse, 42);
        self.assertFalse(isFalse, []);
        self.assertFalse(isFalse, [1]);
        self.assertTrue(isFalse, null);
        self.assertTrue(isFalse, '');
        self.assertTrue(isFalse, 0);
    },


    /**
     * Value is identical to C{is}.
     */
    function test_valueIs(self) {
        var valueIs = Methanal.Preds.valueIs;
        var a = [];
        self.assertTrue(valueIs(5), 5);
        self.assertTrue(valueIs('hello'), 'hello');
        self.assertTrue(valueIs(''), '');
        self.assertTrue(valueIs(a), a);
        self.assertFalse(valueIs(4), 2);
        self.assertFalse(valueIs('foo'), 'bar');
        self.assertFalse(valueIs(''), null);
        self.assertFalse(valueIs([]), []);
        self.assertFalse(valueIs([1]), [1]);
        self.assertFalse(valueIs(undefined), null);
    },


    /**
     * Value is defined and has non-zero, positive length.
     */
    function test_hasLength(self) {
        var hasLength = Methanal.Preds.hasLength;
        self.assertTrue(hasLength, 'hi');
        self.assertTrue(hasLength, [1]);
        self.assertFalse(hasLength, '');
        self.assertFalse(hasLength, []);
        self.assertFalse(hasLength, null);
        self.assertFalse(hasLength, undefined);
    },


    /**
     * Value is not defined or has zero length.
     */
    function test_empty(self) {
        var empty = Methanal.Preds.empty;
        self.assertFalse(empty, 'hi');
        self.assertFalse(empty, [1]);
        self.assertTrue(empty, '');
        self.assertTrue(empty, []);
        self.assertTrue(empty, null);
        self.assertTrue(empty, undefined);
    },


    /**
     * Value has a length of exactly C{n}.
     */
    function test_lengthOf(self) {
        var lengthOf = Methanal.Preds.lengthOf;
        self.assertTrue(lengthOf(0), '');
        self.assertTrue(lengthOf(3), 'foo');
        self.assertFalse(lengthOf(3), '');
        self.assertFalse(lengthOf(3), null);
        self.assertFalse(lengthOf(3), undefined);
    },


    /**
     * Value has a length of at least C{n}.
     */
    function test_lengthAtLeast(self) {
        var lengthAtLeast = Methanal.Preds.lengthAtLeast;
        self.assertTrue(lengthAtLeast(2), 'quux');
        self.assertTrue(lengthAtLeast(2), 'foo');
        self.assertTrue(lengthAtLeast(2), 'hi');
        self.assertFalse(lengthAtLeast(2), 'a');
        self.assertFalse(lengthAtLeast(2), '');
        self.assertFalse(lengthAtLeast(2), null);
        self.assertFalse(lengthAtLeast(2), undefined);
    },


    /**
     * Value has a length of at most C{n}.
     */
    function test_lengthAtMost(self) {
        var lengthAtMost = Methanal.Preds.lengthAtMost;
        self.assertFalse(lengthAtMost(2), 'quux');
        self.assertFalse(lengthAtMost(2), 'foo');
        self.assertTrue(lengthAtMost(2), 'hi');
        self.assertTrue(lengthAtMost(2), 'a');
        self.assertTrue(lengthAtMost(2), '');
        self.assertFalse(lengthAtMost(2), null);
        self.assertFalse(lengthAtMost(2), undefined);
    },


    /**
     * Value is not null.
     */
    function test_notNull(self) {
        var notNull = Methanal.Preds.notNull;
        self.assertTrue(notNull, 2);
        self.assertTrue(notNull, '');
        self.assertTrue(notNull, []);
        self.assertFalse(notNull, null);
    },


    /**
     * Value is within a given range.
     */
    function test_between(self) {
        var between = Methanal.Preds.between;
        self.assertTrue(between(0, 3), 1);
        self.assertTrue(between(0, 3), 3);
        self.assertTrue(between(-3, 3), 0);
        self.assertFalse(between(-3, 3), 4);
        self.assertFalse(between(-3, 3), -4);
    },


    /**
     * Value is less than C{n}.
     */
    function test_lessThan(self) {
        var lessThan = Methanal.Preds.lessThan;
        self.assertTrue(lessThan(3), 2);
        self.assertTrue(lessThan(0), -1);
        self.assertTrue(lessThan(-1), -2);
        self.assertFalse(lessThan(3), 3);
        self.assertFalse(lessThan(0), 3);
    },


    /**
     * Value is at most (or, not greater than; or less than or equal to) C{n}.
     */
    function test_atMost(self) {
        var atMost = Methanal.Preds.atMost;
        self.assertTrue(atMost(3), 2);
        self.assertTrue(atMost(0), -1);
        self.assertTrue(atMost(-1), -2);
        self.assertTrue(atMost(3), 3);
        self.assertFalse(atMost(0), 3);
    },


    /**
     * Value is greater than C{n}.
     */
    function test_greaterThan(self) {
        var greaterThan = Methanal.Preds.greaterThan;
        self.assertTrue(greaterThan(2), 3);
        self.assertTrue(greaterThan(-1), 0);
        self.assertTrue(greaterThan(-2), -1);
        self.assertFalse(greaterThan(3), 3);
        self.assertFalse(greaterThan(0), -1);
        self.assertFalse(greaterThan(3), 1);
    },


    /**
     * Value is at least (or, not less than; or greater than or equal to) C{n}.
     */
    function test_atLeast(self) {
        var atLeast = Methanal.Preds.atLeast;
        self.assertTrue(atLeast(2), 3);
        self.assertTrue(atLeast(-1), 0);
        self.assertTrue(atLeast(-2), -1);
        self.assertTrue(atLeast(3), 3);
        self.assertFalse(atLeast(0), -1);
        self.assertFalse(atLeast(3), 1);
    },


    /**
     * Value is a multiple of C{n}.
     */
    function test_multipleOf(self) {
        var multipleOf = Methanal.Preds.multipleOf;
        self.assertTrue(multipleOf(3), 3);
        self.assertTrue(multipleOf(3), 6);
        self.assertTrue(multipleOf(2), -8);
        self.assertFalse(multipleOf(2), 1);
        self.assertFalse(multipleOf(2), 0);
    },


    /**
     * Value is one of a given set.
     */
    function test_oneOf(self) {
        var oneOf = Methanal.Preds.oneOf;
        self.assertTrue(oneOf(['foo', 'bar']), 'foo');
        self.assertFalse(oneOf(['foo', 'bar']), 'baz');
        self.assertFalse(oneOf(['foo', 'bar']), '');
        self.assertFalse(oneOf([]), 'foo');
        self.assertFalse(oneOf([]), '');
    },


    /**
     * Value contains a subset (in no particular order) of an C{Array}.
     */
    function test_arraySubset(self) {
        var arraySubset = Methanal.Preds.arraySubset;
        var x = ['a', 'b'];
        self.assertTrue(arraySubset([]), x);
        self.assertTrue(arraySubset(['a']), x);
        self.assertTrue(arraySubset(['b']), x);
        self.assertTrue(arraySubset(['a', 'b']), x);
        self.assertFalse(arraySubset(['c']), x);
        self.assertFalse(arraySubset(['a', 'c']), x);
    },


    /**
     * Value contains only characters matching a regular expression character
     * class.
     */
    function test_isChars(self) {
        var isChars = Methanal.Preds.isChars;
        self.assertTrue(isChars('[0-9]'), '0123456789');
        self.assertTrue(isChars('[A-Z]'), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
        self.assertTrue(isChars('[a-z]'), 'abcdefghijklmnopqrstuvwxyz');
        self.assertTrue(isChars("[a-z_']"), "hello_world's");
        self.assertFalse(isChars('[0-9]'), 'hello');
    },


    /**
     * Value matches a regular expression.
     */
    function test_regex(self) {
        var regex = Methanal.Preds.regex;
        self.assertTrue(regex(/^\d+$/), '123');
        self.assertTrue(regex(/^foo\d{2}$/), 'foo12');
        self.assertFalse(regex(/^\d+$/), 'hello');
        self.assertFalse(regex(/^foo\d{2}$/), 'bar12');
    },


    /**
     * Value is within a timedelta and a start date.
     */
    function test_dateSince(self) {
        var now = Methanal.Util.Time().oneDay();
        var tomorrow = now.offset(
            Methanal.Util.TimeDelta({'days': 1}));
        var nextDay = now.offset(
            Methanal.Util.TimeDelta({'days': 2}));

        var dateSince = Methanal.Preds.dateSince;
        self.assertTrue(
            dateSince(Methanal.Util.TimeDelta({'days': 2}), tomorrow),
            nextDay.asDate());
        self.assertTrue(
            dateSince(Methanal.Util.TimeDelta({'days': 2}), tomorrow),
            nextDay.asTimestamp());
        self.assertFalse(
            dateSince(Methanal.Util.TimeDelta({'hours': 1}), tomorrow),
            nextDay.asDate());
        self.assertFalse(
            dateSince(Methanal.Util.TimeDelta({'days': 1}), tomorrow),
            nextDay.asTimestamp());
    },


    /**
     * Value is within a timedelta and the current time.
     */
    function test_dateWithin(self) {
        var now = Methanal.Util.Time();
        var tomorrow = now.offset(
            Methanal.Util.TimeDelta({'days': 1, 'minutes': 10}));

        var dateWithin = Methanal.Preds.dateWithin;
        self.assertTrue(
            dateWithin(Methanal.Util.TimeDelta({'hours': 1})),
            now.offset(Methanal.Util.TimeDelta({'minutes': 30})).asDate());
        self.assertTrue(
            dateWithin(Methanal.Util.TimeDelta({'days': 1,
                                                 'minutes': 30})),
            tomorrow.asTimestamp());
        self.assertFalse(
            dateWithin(Methanal.Util.TimeDelta({'days': 1})),
            tomorrow.asDate());

        var yesterday = now.offset(
            Methanal.Util.TimeDelta({'days': -1, 'minutes': -10}));
        self.assertTrue(
            dateWithin(Methanal.Util.TimeDelta({'hours': -1})),
            now.offset(Methanal.Util.TimeDelta({'minutes': -30})).asDate());
        self.assertTrue(
            dateWithin(Methanal.Util.TimeDelta({'days': -1,
                                                 'minutes': -30})),
            yesterday.asDate());
        // XXX: Fudge it slightly since dateWithin uses the current time and
        // sometimes things take some time.
        self.assertFalse(
            dateWithin(Methanal.Util.TimeDelta({'days': -1})),
            yesterday.asDate());
        self.assertFalse(
            dateWithin(Methanal.Util.TimeDelta({'days': -1})),
            yesterday.asTimestamp());
    },


    /**
     * Value is a future date.
     */
    function test_futureDate(self) {
        var now = Methanal.Util.Time();
        var yesterday = now.offset(
            Methanal.Util.TimeDelta({'days': -1})).asDate();
        var tomorrow = now.offset(
            Methanal.Util.TimeDelta({'days': 1})).asDate();
        var futureDate = Methanal.Preds.futureDate;
        self.assertTrue(futureDate, tomorrow);
        self.assertFalse(futureDate, yesterday);
    },


    /**
     * Value is a past date.
     */
    function test_pastDate(self) {
        var now = Methanal.Util.Time();
        var yesterday = now.offset(
            Methanal.Util.TimeDelta({'days': -1})).asDate();
        var tomorrow = now.offset(
            Methanal.Util.TimeDelta({'days': 1})).asDate();
        var pastDate = Methanal.Preds.pastDate;
        self.assertFalse(pastDate, tomorrow);
        self.assertTrue(pastDate, yesterday);
    });
