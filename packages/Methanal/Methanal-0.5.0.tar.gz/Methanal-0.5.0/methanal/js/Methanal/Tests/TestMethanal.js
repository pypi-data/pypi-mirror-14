// import Divmod.UnitTest
// import Methanal.View



Divmod.UnitTest.TestCase.subclass(
    Methanal.Tests.TestMethanal, 'TestMethanal').methods(
    function test_basic(self) {
        var expected = {
            'foo': [true,  [true, false]],
            'bar': [false, [undefined]]};

        function getData(name) {
            return 10;
        }

        function update(name, values) {
            self.assertArraysEqual(values, expected[name][1]);
            self._called = true;
        }

        function isActive(name) {
            return expected[name][0];
        }

        var cache = Methanal.View._HandlerCache(
            getData, update, isActive, undefined);
        cache.addHandler(function (x) { return x == 10; }, ['foo'], ['foo']);
        cache.addHandler(function (x) { return x != 10; }, ['foo'], ['foo']);
        cache.refresh();
        self._called = false;
        cache.changed('foo');
        self.assert(self._called);

        self._called = false;
        cache.addHandler(function (x) { return 42; },      ['bar'], ['bar']);
        cache.changed('bar');
        self.assert(self._called);
    });
