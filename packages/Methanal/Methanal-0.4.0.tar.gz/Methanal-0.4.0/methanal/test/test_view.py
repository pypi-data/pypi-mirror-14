from datetime import datetime
from decimal import Decimal
try:
    import xml.etree.ElementTree as etree
    # Appease pyflakes.
    etree
except ImportError:
    import elementtree.ElementTree as etree

from twisted.trial import unittest
from twisted.internet.defer import gatherResults

from epsilon.extime import FixedOffset, Time

from axiom import attributes
from axiom.store import Store
from axiom.item import Item

from nevow import athena, loaders
from nevow.testutil import renderLivePage

from methanal import view, errors
from methanal.imethanal import IEnumeration
from methanal.model import ItemModel, Value, DecimalValue, Model
from methanal.enums import Enum, EnumItem, ObjectEnum



class MockParent(object):
    def __init__(self, param):
        self.store = None
        self.param = param

        self.page = self
        self.liveFragmentChildren = []

        self.model = self


    def getParameter(self, name):
        return self.param


    def addFormChild(self, child):
        pass



def renderWidget(widget, debug=False):
    """
    Flatten and render a widget.

    @rtype: C{Deferred} -> C{ElementTree}
    @return: A deferred that fires with the parsed flattened output.
    """
    def parse(result):
        return etree.ElementTree(
            etree.fromstring('<widget>' + result + '</widget>'))

    def printIt(result):
        print result
        return result

    page = athena.LivePage(docFactory=loaders.stan(widget))
    widget.setFragmentParent(page)
    d = renderLivePage(page)
    if debug:
        d.addCallback(printIt)
    d.addCallback(parse)
    return d



class LiveFormTests(unittest.TestCase):
    """
    Tests for L{methanal.view.LiveForm}.
    """
    def setUp(self):
        self.form = view.LiveForm(store=None, model=Model())


    def test_renderActions(self):
        """
        The actions of a LiveForm are rendered according to the given actions.
        """
        def verifyRendering(tree):
            # Oh where, oh where has my little library gone?
            # Oh where, oh where can it be?
            # With real XPath support and functionality.
            # Oh where, oh where can it be?
            candidates = tree.findall('.//form/div')
            actionsNode = None
            id = 'athenaid:%d-actions' % (self.form._athenaID,)
            for node in candidates:
                if node.get('id') == id:
                    actionsNode = node
                    break

            self.assertNotIdentical(
                actionsNode, None, 'Could not find the form actions node')

            button = actionsNode.find('.//button')
            self.assertEquals(button.get('type'), 'submit')
            self.assertEquals(button.text.strip(), 'Submit')

        return renderWidget(self.form).addCallback(verifyRendering)



class FormInputTests(unittest.TestCase):
    """
    Tests for L{methanal.view.FormInput}.

    Also serves as the base class for other input tests.

    @type controlType: L{methanal.view.FormInput} subclass
    @cvar controlType: Type of control to create with L{createControl}

    @type createArgs: C{list} of C{dict}
    @cvar createArgs: Sequence of arguments that will create controls of
        type L{controlType}

    @type brokenCreateArgs: C{list} of C{(Exception, dict)}
    @cvar brokenCreateArgs: Sequence of C{(exceptionRaised, args)} that will
        fail to create controls of type L{controlType}
    """
    controlType = view.FormInput

    createArgs = []

    brokenCreateArgs = []


    def setUp(self):
        self.name = 'test'


    def createParent(self, args):
        """
        Create a parent control.
        """
        return MockParent(self.createParam(args))


    def createParam(self, args):
        """
        Create a model parameter.
        """
        return Value(self.name)


    def createControl(self, args):
        """
        Create a control of type L{controlType}.
        """
        args.setdefault('name', self.name)
        args.setdefault('parent', self.createParent(args))
        return self.controlType(**args)


    def test_creation(self):
        """
        Creating a control succeeds.

        Try each set of parameters from L{createArgs}.
        """
        for args in self.createArgs:
            control = self.createControl(args)
            self.assertTrue(isinstance(control.name, unicode))
            self.assertIdentical(control.param, control.parent.param)


    def test_creationFails(self):
        """
        Creating a control fails.

        Try each set of parameters from L{brokenCreateArgs}, ensuring that
        the correct exception is raised in each case.
        """
        for errorType, args in self.brokenCreateArgs:
            self.assertRaises(errorType, self.createControl, args)



class TextAreaInputTests(FormInputTests):
    """
    Tests for L{methanal.view.TextAreaInput}.
    """
    controlType = view.TextAreaInput

    createArgs = [
        dict()]



class TextInputTests(FormInputTests):
    """
    Tests for L{methanal.view.TextInput}.
    """
    controlType = view.TextInput

    createArgs = [
        dict(),
        dict(embeddedLabel=True)]



class FilteringTextInputTests(FormInputTests):
    """
    Tests for L{methanal.view.FilteringTextInput}.
    """
    controlType = view.FilteringTextInput

    createArgs = [
        dict(),
        dict(expression=u'[a-zA-Z]')]



class PrePopulatingTextInputTests(FormInputTests):
    """
    Tests for L{methanal.view.PrePopulatingTextInput}.
    """
    controlType = view.PrePopulatingTextInput

    createArgs = [
        dict(targetControlName='bbq')]

    brokenCreateArgs = [
        (TypeError, dict())]



class DateInputTests(FormInputTests):
    """
    Tests for L{methanal.view.DateInput}.
    """
    controlType = view.DateInput

    createArgs = [
        dict(timezone=FixedOffset(0, 0)),
        dict(timezone=FixedOffset(0, 0), twentyFourHours=True)]

    brokenCreateArgs = [
        (TypeError, dict()),
        (TypeError, dict(twentyFourHours=True))]


    def test_getValue(self):
        """
        L{methanal.view.DateInput.getValue} retrieves an empty string in the
        C{None} case and a string representing the C{Time} specified by
        parameter's value, in the case where a value exists.
        """
        control = self.createControl(dict(timezone=FixedOffset(0, 0)))
        param = control.parent.param

        param.value = None
        self.assertEquals(control.getValue(), u'')

        param.value = Time.fromDatetime(datetime(2007, 1, 1))
        self.assertTrue(isinstance(control.getValue(), unicode))
        self.assertEquals(control.getValue(), u'2007-01-01')

        param.value = Time.fromDatetime(datetime(542, 12, 18))
        self.assertEquals(control.getValue(), u'0542-12-18')



class NumericInputTestsMixin(object):
    """
    Tests mixin for numeric inputs.
    """
    def _testMinimumMaximum(self, control, acceptable, tooSmall, tooLarge):
        """
        Assert that C{control} sets its parameter's value to C{None} value or
        C{acceptable}, when invoked with these values. When invoked with
        C{tooSmall} or C{tooLarge} an exception is raised indicating that the
        value is too small or too large.
        """
        param = control.parent.param

        data = {param.name: None}
        control.invoke(data)
        self.assertIdentical(param.value, None)

        data = {param.name: acceptable}
        control.invoke(data)
        self.assertEquals(param.value, acceptable)

        data = {param.name: tooSmall}
        e = self.assertRaises(ValueError, control.invoke, data)
        self.assertIn('is smaller than', str(e))

        data = {param.name: tooLarge}
        e = self.assertRaises(ValueError, control.invoke, data)
        self.assertIn('is larger than', str(e))


    def test_minimumMaximumDefaultValues(self):
        """
        Numeric inputs default to not accepting values smaller than C{-(2 **
        63)} or larger than C{2 ** 63 }.
        """
        control = self.createControl(dict())
        self._testMinimumMaximum(control, 42, -(2 ** 63) - 1, 2 ** 63)


    def test_minimumMaximumOverrideValues(self):
        """
        Numeric inputs can override their minimum and maximum value range.
        """
        control = self.createControl(dict(minimumValue=0, maximumValue=10))
        self._testMinimumMaximum(control, 5, -1, 42)



class IntegerInputTests(FormInputTests, NumericInputTestsMixin):
    """
    Tests for L{methanal.view.IntegerInput}.
    """
    controlType = view.IntegerInput


    def test_getValue(self):
        """
        L{methanal.view.IntegerInput.getValue} retrieves an empty string in the
        C{None} case and an C{int} in the case where a value exists.
        """
        control = self.createControl(dict())
        param = control.parent.param

        param.value = None
        self.assertEquals(control.getValue(), u'')

        param.value = u'5'
        self.assertTrue(isinstance(control.getValue(), int))
        self.assertEquals(control.getValue(), 5)
        param.value = 5
        self.assertTrue(isinstance(control.getValue(), int))
        self.assertEquals(control.getValue(), 5)



class FloatInputTests(FormInputTests, NumericInputTestsMixin):
    """
    Tests for L{methanal.view.FloatInput}.
    """
    controlType = view.FloatInput


    def test_getValue(self):
        """
        L{methanal.view.FloatInput.getValue} retrieves an empty string in the
        C{None} case and a C{float} in the case where a value exists.
        """
        control = self.createControl(dict())
        param = control.parent.param

        param.value = None
        self.assertEquals(control.getValue(), u'')

        param.value = u'5'
        self.assertTrue(isinstance(control.getValue(), float))
        self.assertEquals(control.getValue(), 5.0)
        param.value = 5.0
        self.assertTrue(isinstance(control.getValue(), float))
        self.assertEquals(control.getValue(), 5.0)


    def test_minimumMaximumDefaultValues(self):
        """
        The limits for SQL and Python float types are the same value, so no
        minimum or maximum checking is required in Methanal for the default
        ranges.
        """
        pass



class DecimalInputTests(FormInputTests, NumericInputTestsMixin):
    """
    Tests for L{methanal.view.DecimalInput}.
    """
    controlType = view.DecimalInput

    decimalPlaces = 3

    createArgs = [
        dict(),
        dict(decimalPlaces=1)]


    def createParam(self, args):
        decimalPlaces = args.get('decimalPlaces', self.decimalPlaces)
        return DecimalValue(name=self.name, decimalPlaces=decimalPlaces)


    def test_getValue(self):
        """
        L{methanal.view.DecimalInput.getValue} retrieves an empty string in the
        C{None} case and a C{float} in the case where a value exists.
        """
        control = self.createControl(dict(decimalPlaces=2))
        param = control.parent.param

        param.value = None
        self.assertEquals(control.getValue(), u'')

        param.value = u'12.34'
        self.assertTrue(isinstance(control.getValue(), float))
        self.assertEquals(control.getValue(), 12.34)


    def test_invoke(self):
        """
        L{methanal.view.DecimalInput.invoke} sets the parameter value to C{None}
        in the C{None} case and a C{Decimal} in the case where a value exists.
        """
        control = self.createControl(dict(decimalPlaces=2))
        param = control.parent.param

        data = {param.name: None}
        control.invoke(data)
        self.assertIdentical(param.value, None)

        data = {param.name: u'12.34'}
        control.invoke(data)
        self.assertEquals(param.value, Decimal('12.34'))



class VerifiedPasswordInputTests(FormInputTests):
    """
    Tests for L{methanal.view.VerifiedPasswordInput}.
    """
    controlType = view.VerifiedPasswordInput

    createArgs = [
        dict(),
        dict(minPasswordLength=3),
        dict(strengthCriteria=['ALPHA'])]



class ChoiceInputTestsMixin(object):
    """
    Mixin for L{methanal.view.ChoiceInput} based controls.
    """
    def createControl(self, args):
        """
        Create a L{methanal.view.ChoiceInput} from C{values} and assert that
        L{methanal.view.ChoiceInput.values} provides L{IEnumeration}.
        """
        control = super(ChoiceInputTestsMixin, self).createControl(args)
        self.assertTrue(IEnumeration.providedBy(control.values))
        return control



class ObjectChoiceTestsMixin(ChoiceInputTestsMixin):
    """
    Mixin for L{methanal.view.ChoiceInput}s that support arbitrary Python
    objects.
    """
    values = [
        (object(), u'Foo'),
        (object(), u'Bar'),
        (None,     u'Baz')]

    createArgs = [
        dict(values=values)]

    def test_choiceValues(self):
        """
        L{ChoiceInput}s that support arbitrary Python objects maintain a
        mapping of object identities (stored as text) to objects, and use the
        object identites for enumeration values.
        """
        control = self.createControl(dict(values=self.values))
        expectedValues = [(id(obj), desc) for obj, desc in self.values]
        self.assertEquals(control.values.as_pairs(), expectedValues)


    def test_encodeDecodeValue(self):
        """
        L{_ObjectChoiceMixinBase.encodeValue} and
        L{_ObjectChoiceMixinBase.decodeValue} are symmetric.
        """
        control = self.createControl(dict(values=self.values))
        for obj, desc in self.values:
            self.assertIdentical(
                control.decodeValue(control.encodeValue(obj)), obj)


    def test_getValue(self):
        """
        Object-enabled L{ChoiceInput}s return an encoded object identity from
        their C{getValue} method.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        for obj, desc in self.values:
            param.value = obj
            self.assertEquals(
                control.getValue(),
                control.encodeValue(obj))


    def test_invoke(self):
        """
        Object-enabled L{ChoiceInput}s set their parameter value to the
        corresponding real object when invoked with an encoded object identity.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        pairs = [(obj, value)
                 for (obj, desc), (value, desc)
                 in zip(self.values, control.values.as_pairs())]
        for obj, value in pairs:
            data = {param.name: value}
            control.invoke(data)
            self.assertIdentical(param.value, obj)


    def test_render(self):
        """
        Rendering the control raises no exceptions.
        """
        control = self.createControl(dict(values=self.values))
        ds = []

        def _render(value):
            control.parent.param.value = value
            ds.append(renderWidget(control))

        _render(None)
        for obj, desc in self.values:
            _render(obj)
        return gatherResults(ds)



class ObjectMultiChoiceTestsMixin(ObjectChoiceTestsMixin):
    """
    Mixin for L{methanal.view.ChoiceInput}s that support many arbitrary Python
    objects.
    """
    def test_getValueNoValues(self):
        """
        Multiple-object-enabled L{ChoiceInput}s return an empty list from
        C{getValue} when the parameter is C{None}, or empty.
        """
        control = self.createControl(dict(values=self.values))

        control.parent.param.value = None
        self.assertEquals(control.getValue(), [])

        control.parent.param.value = []
        self.assertEquals(control.getValue(), [])


    def test_getValue(self):
        """
        Multiple-object-enabled L{ChoiceInput}s return many encoded object
        identities from C{getValue}.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        for obj, desc in self.values:
            param.value = [obj]
            self.assertEquals(
                control.getValue(),
                [control.encodeValue(obj)])

        obj1, obj2 = [self.values[0][0], self.values[1][0]]
        param.value = [obj1, obj2]
        self.assertEquals(
            control.getValue(),
            [control.encodeValue(obj1), control.encodeValue(obj2)])


    def test_invokeNoValues(self):
        """
        Multiple-object-enabled L{ChoiceInput}s set their parameter value to an
        empty list when invoked with C{None}, or empty.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param
        control.invoke({param.name: None})
        self.assertEquals(param.value, [])

        control = self.createControl(dict(values=self.values))
        param = control.parent.param
        control.invoke({param.name: []})
        self.assertEquals(param.value, [])


    def test_invoke(self):
        """
        Multiple-object-enabled L{ChoiceInput}s set their parameter value to
        many corresponding real objects when invoked with encoded object
        identities.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        pairs = [(obj, value)
                 for (obj, desc), (value, desc)
                 in zip(self.values, control.values.as_pairs())]
        for obj, value in pairs:
            data = {param.name: [value]}
            control.invoke(data)
            self.assertEquals(param.value, [obj])

        obj1, obj2 = [pairs[0][0], pairs[1][0]]
        value1, value2 = [pairs[0][1], pairs[1][1]]
        data = {param.name: [value1, value2]}
        control.invoke(data)
        self.assertEquals(param.value, [obj1, obj2])


    def test_render(self):
        """
        Rendering the control raises no exceptions.
        """
        control = self.createControl(dict(values=self.values))
        ds = []

        def _render(value):
            control.parent.param.value = value
            ds.append(renderWidget(control))

        _render(None)
        for obj, desc in self.values:
            _render([obj])
        return gatherResults(ds)



class ChoiceInputTests(ChoiceInputTestsMixin, FormInputTests):
    """
    Tests for L{methanal.view.ChoiceInput}.
    """
    controlType = view.ChoiceInput

    createArgs = [
        dict(values=[
            (u'foo', u'Foo'),
            (u'bar', u'Bar')])]

    brokenCreateArgs = [
        (TypeError, dict())]


    def createControl(self, args, checkExpectedValues=True):
        """
        Create a L{methanal.view.ChoiceInput} from C{values}, assert that
        L{methanal.view.ChoiceInput.value} provides L{IEnumeration} and
        calling C{as_pairs} results in the same values as C{values}.
        """
        control = super(ChoiceInputTests, self).createControl(args)
        if checkExpectedValues:
            self.assertEquals(control.values.as_pairs(),
                              list(args.get('values')))
        return control


    def test_createDeprecated(self):
        """
        Passing values that are not adaptable to IEnumeration are converted
        to a C{list}, adapted to L{IEnumeration} and a warning is emitted.
        """
        # Not a list.
        values = tuple([
            (u'foo', u'Foo'),
            (u'bar', u'Bar')])
        self.createControl(dict(values=values))
        self.assertEquals(len(self.flushWarnings()), 2)


    def test_invalidEnumValues(self):
        """
        Specifying invalid enumeration item values returns C{None} instead of
        raising L{InvalidEnumItem}.
        """
        values = [
            (u'foo', u'Foo'),
            (u'bar', u'Bar')]
        control = self.createControl(dict(values=values))
        control.param.value = u'nopenotinhere'
        self.assertEqual(
            control.getValue(),
            None)



class SelectInputTests(ChoiceInputTests):
    """
    Tests for L{methanal.view.SelectInput}.
    """
    controlType = view.SelectInput

    def test_renderGroupsOptions(self):
        """
        The options of a C{SelectInput} are rendered as groups if the enumeration
        values specify a C{'group'} extra value.
        """
        values = Enum(
            '',
            [EnumItem(u'foo', u'Foo', group=u'Group'),
             EnumItem(u'bar', u'Bar', group=u'Group')])

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        def verifyRendering(tree):
            groupNodes = tree.findall('.//select/optgroup')
            groups = set(item.group for item in values)
            self.assertEquals(len(groupNodes), len(groups))
            for groupNode, item in zip(groupNodes, values):
                self.assertEquals(groupNode.get('label'), item.group)

                optionNodes = groupNode.findall('option')
                self.assertEquals(len(optionNodes), len(list(values)))
                for optionNode, innerItem in zip(optionNodes, values):
                    self.assertEquals(optionNode.get('value'), innerItem.value)
                    self.assertEquals(optionNode.text.strip(), innerItem.desc)

        return renderWidget(control).addCallback(verifyRendering)


    def test_renderObjectOptions(self):
        """
        If a C{SelectInput}'s values are an C{ObjectEnum} then the rendered
        option values match the C{'id'} extra of the object enumeration.
        """
        object1 = object()
        object2 = object()
        values = ObjectEnum(
            '',
            [EnumItem(object1, u'Foo'),
             EnumItem(object2, u'Bar', id=u'chuck')])

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        def verifyRendering(tree):
            optionNodes = tree.findall('.//option')
            self.assertEquals(len(optionNodes), len(list(values)))
            for optionNode, item in zip(optionNodes, values):
                self.assertEquals(optionNode.get('value'), item.id)
                self.assertEquals(optionNode.text.strip(), item.desc)

        return renderWidget(control).addCallback(verifyRendering)


    def test_getValueObjectEnum(self):
        """
        L{SelectInput.getValue} returns the C{'id'} extra value when backed by
        an C{ObjectEnum}.
        """
        object1 = object()
        object2 = object()
        values = ObjectEnum(
            '',
            [EnumItem(object1, u'Foo'),
             EnumItem(object2, u'Bar', id=u'chuck')])

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        param = control.parent.param

        param.value = None
        self.assertIdentical(control.getValue(), None)

        for value in values:
            param.value = value.value
            self.assertEquals(control.getValue(), value.id)


    def test_invokeObjectEnum(self):
        """
        When backed by an C{ObjectEnum}, L{SelectInput.invoke} sets the
        parameter value to the Python object of L{EnumItem} with C{'id'} extra
        matching the invocation data value and C{None} in the C{None} case.
        """
        object1 = object()
        object2 = object()
        values = ObjectEnum(
            '',
            [EnumItem(object1, u'Foo'),
             EnumItem(object2, u'Bar', id=u'chuck')])

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        param = control.parent.param
        data = {param.name: None}
        control.invoke(data)
        self.assertIdentical(param.value, None)

        for value in values:
            data = {param.name: value.id}
            control.invoke(data)
            self.assertIdentical(param.value, value.value)


    def test_invokeObjectEnumTrickery(self):
        """
        L{SelectInput.invoke} falls back to locating enumeration items by value
        when no C{'id'} extra value matches. However, this can lead to leaking
        information about the enumeration values in the case of objects such as
        strings and integers. In case we fallback to an item with a C{'id'}
        extra, even if it doesn't match, C{InvalidEnumItem} is raised.
        """
        object1 = object()
        values = ObjectEnum(
            '',
            [EnumItem(object1,     u'Foo'),
             EnumItem(u'password', u'Bar', id=u'chuck')])

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        param = control.parent.param

        data = {param.name: u'password'}
        self.assertRaises(errors.InvalidEnumItem,
            control.invoke, data)



class MultiValueChoiceInputTestsMixin(object):
    """
    Tests mixin for L{methanal.view.ChoiceInput}s that support multiple values.
    """
    values = [
        (u'foo', u'Foo'),
        (u'bar', u'Bar'),
        (u'baz', u'Baz')]

    def test_getValueNoValues(self):
        """
        Multi-value L{ChoiceInput}s return an empty list from C{getValue} when
        the parameter is C{None}, or empty.
        """
        control = self.createControl(dict(values=self.values))

        control.parent.param.value = None
        self.assertEquals(control.getValue(), [])

        control.parent.param.value = []
        self.assertEquals(control.getValue(), [])


    def test_getValue(self):
        """
        Multi-value L{ChoiceInput}s return a C{list} of the selected values
        from C{getValue}.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        for value, desc in self.values:
            param.value = [value]
            self.assertEquals(
                control.getValue(),
                [value])

        v1, v2 = [self.values[0][0], self.values[1][0]]
        param.value = [v1, v2]
        self.assertEquals(
            control.getValue(),
            [v1, v2])


    def test_invokeNoValues(self):
        """
        Multi-value L{ChoiceInput}s set their parameter value to an empty list
        when invoked with C{None}, or empty.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param
        control.invoke({param.name: None})
        self.assertEquals(param.value, [])

        control = self.createControl(dict(values=self.values))
        param = control.parent.param
        control.invoke({param.name: []})
        self.assertEquals(param.value, [])


    def test_invoke(self):
        """
        Multi-value L{ChoiceInput}s set their parameter value to a C{list}
        containing the values of the invoked data.
        """
        control = self.createControl(dict(values=self.values))
        param = control.parent.param

        data = {param.name: None}
        control.invoke(data)
        self.assertEquals(param.value, [])

        data = {param.name: [None]}
        control.invoke(data)
        self.assertEquals(param.value, [None])

        for value, desc in self.values:
            data = {param.name: [value]}
            control.invoke(data)
            self.assertEquals(param.value, [value])

        v1, v2 = self.values[0][0], self.values[1][0]
        data = {param.name: [v1, v2]}
        control.invoke(data)
        self.assertEquals(param.value, [v1, v2])


    def test_invokeObjectEnum(self):
        """
        Invoking a multi-value L{ChoiceInput}s backed by an L{ObjectEnum} sets
        their parameter value to a C{list} of objects referenced by ID in the
        invocation data.
        """
        object1 = object()
        values = ObjectEnum(
            '',
            [EnumItem(object1, u'Foo'),
             EnumItem(u'buzz', u'Buzz', id=u'quux')])
        control = self.createControl(
            dict(values=values), checkExpectedValues=False)
        param = control.parent.param

        for value in values:
            data = {param.name: [value.id]}
            control.invoke(data)
            self.assertEquals(param.value, [value.value])

        vs = [v.value for v in values]
        vIDs = [v.id for v in values]
        data = {param.name: vIDs}
        control.invoke(data)
        self.assertEquals(param.value, vs)

        data = {param.name: [u'buzz']}
        self.assertRaises(errors.InvalidEnumItem, control.invoke, data)


    def test_render(self):
        """
        Rendering the control raises no exceptions.
        """
        control = self.createControl(dict(values=self.values))
        ds = []

        def _render(value):
            control.parent.param.value = value
            ds.append(renderWidget(control))

        _render(None)
        for obj, desc in self.values:
            _render([obj])
        return gatherResults(ds)


    def test_invalidEnumValues(self):
        """
        Invalid enumeration item values are stripped instead of raising
        L{InvalidEnumItem}.
        """
        values = [
            (u'foo', u'Foo'),
            (u'bar', u'Bar')]
        control = self.createControl(dict(values=values))
        control.param.value = [u'nopenotinhere']
        self.assertEqual(
            control.getValue(),
            [])

        control.param.value = [u'nopenotinhere', u'foo']
        self.assertEqual(
            control.getValue(),
            [u'foo'])



class MultiSelectInputTests(MultiValueChoiceInputTestsMixin, ChoiceInputTests):
    controlType = view.MultiSelectInput



class GroupedSelectInputTests(ChoiceInputTests):
    """
    Tests for L{methanal.view.GroupedSelectInput}.
    """
    controlType = view.GroupedSelectInput

    def test_createDeprecated(self):
        """
        Passing values that are not adaptable to IEnumeration are converted
        to a C{list}, adapted to L{IEnumeration} and a warning is emitted.
        """
        # Not a list.
        values = tuple([
            (u'foo', u'Foo'),
            (u'bar', u'Bar')])
        self.createControl(dict(values=values))
        self.assertEquals(len(self.flushWarnings()), 3)


    def test_renderOptions(self):
        """
        The options of a GroupedSelectInput are rendered according to the given
        values.
        """
        values = [(u'Group', [(u'foo', u'Foo'),
                              (u'bar', u'Bar')])]

        control = self.createControl(
            dict(values=values), checkExpectedValues=False)

        def verifyRendering(tree):
            groupNodes = tree.findall('.//select/optgroup')
            self.assertEquals(len(groupNodes), len(values))
            for groupNode, (group, subvalues) in zip(groupNodes, values):
                self.assertEquals(groupNode.get('label'), group)

                optionNodes = groupNode.findall('option')
                self.assertEquals(len(optionNodes), len(subvalues))
                for optionNode, (value, desc) in zip(optionNodes, subvalues):
                    self.assertEquals(optionNode.get('value'), value)
                    self.assertEquals(optionNode.text.strip(), desc)

        return renderWidget(control).addCallback(verifyRendering)



class ObjectGroupedSelectInputTests(ObjectChoiceTestsMixin, FormInputTests):
    """
    Tests for L{methanal.view.ObjectGroupedSelectInput}.
    """
    controlType = view.ObjectGroupedSelectInput



class ObjectSelectInputTests(ObjectChoiceTestsMixin, FormInputTests):
    """
    Tests for L{methanal.view.ObjectSelectInput}.
    """
    controlType = view.ObjectSelectInput



class IntegerSelectInputTests(ObjectSelectInputTests):
    """
    Tests for L{methanal.view.IntegerSelectInput}.
    """
    controlType = view.IntegerSelectInput

    values = [
        (1, u'Foo'),
        (2, u'Bar')]



class ObjectMultiSelectInputTests(ObjectMultiChoiceTestsMixin, FormInputTests):
    """
    Tests for L{methanal.view.ObjectMultiSelectInput}.
    """
    controlType = view.ObjectMultiSelectInput



class RadioGroupInputTests(ChoiceInputTests):
    """
    Tests for L{methanal.view.RadioGroupInput}.
    """
    controlType = view.RadioGroupInput


    def test_renderOptions(self):
        """
        The options of a GroupedSelectInput are rendered according to the given
        values.
        """
        values = [(u'foo', u'Foo'),
                  (u'bar', u'Bar')]

        control = self.createControl(dict(values=values))

        def verifyRendering(tree):
            inputs = tree.findall('.//input')
            self.assertEquals(len(values), len(inputs))
            for input, (value, desc) in zip(inputs, values):
                self.assertEquals(input.get('name'), self.name)
                self.assertEquals(input.get('value'), value)
                self.assertEquals(input.tail.strip(), desc)

        return renderWidget(control).addCallback(verifyRendering)



class ObjectRadioGroupInputTests(ObjectChoiceTestsMixin, FormInputTests):
    """
    Tests for L{methanal.view.ObjectRadioGroupInput}.
    """
    controlType = view.ObjectRadioGroupInput



class CheckboxInputTests(FormInputTests):
    """
    Tests for L{methanal.view.CheckboxInput}.
    """
    controlType = view.CheckboxInput


    def test_renderNotChecked(self):
        """
        An unchecked CheckboxInput renders no C{checked} attribute.
        """
        control = self.createControl(dict())
        control.parent.param.value = False

        def verifyRendering(tree):
            input = tree.find('.//input')
            self.assertIdentical(input.get('checked'), None)

        return renderWidget(control).addCallback(verifyRendering)


    def test_renderChecked(self):
        """
        An checked CheckboxInput renders a C{checked} attribute.
        """
        control = self.createControl(dict())
        control.parent.param.value = True

        def verifyRendering(tree):
            input = tree.find('.//input')
            self.assertEquals(input.get('checked'), 'checked')

        return renderWidget(control).addCallback(verifyRendering)


    def test_renderInlineLabel(self):
        """
        Specifying an C{inlineLabel} value results in that label being used
        when renderering the CheckboxInput.
        """
        control = self.createControl(dict(inlineLabel=u'HELLO WORLD'))
        control.parent.param.value = True

        def verifyRendering(tree):
            input = tree.find('.//input')
            self.assertEquals(input.tail.strip(), 'HELLO WORLD')

        return renderWidget(control).addCallback(verifyRendering)



class MultiCheckboxInputTests(MultiValueChoiceInputTestsMixin,
                              ChoiceInputTests):
    controlType = view.MultiCheckboxInput



class TestItem(Item):
    """
    A test Item with some attributes.
    """
    foo = attributes.text(doc=u'Foo')
    bar = attributes.boolean(doc=u'Bar?')



class ItemViewBaseTests(unittest.TestCase):
    """
    Tests for L{methanal.view.ItemViewBase}.
    """
    viewType = view.ItemViewBase

    def setUp(self):
        self.store = Store()
        self.item = TestItem(store=self.store)


    def test_createWithItem(self):
        """
        Create an item view with an axiom Item instance.
        """
        iv = self.viewType(item=self.item)
        self.assertIdentical(iv.store, self.store)
        self.assertIdentical(iv.itemClass, type(self.item))
        self.assertIdentical(iv.original, self.item)


    def test_createWithItemClass(self):
        """
        Create an item view with an axiom Item type and store, an exception
        is raised if the C{store} parameter is not given.
        """
        iv = self.viewType(itemClass=type(self.item), store=self.store)
        self.assertIdentical(iv.store, self.store)
        self.assertIdentical(iv.itemClass, type(self.item))
        self.assertIdentical(iv.original, type(self.item))

        self.assertRaises(ValueError, self.viewType, itemClass=type(self.item))


    def test_customModelFactory(self):
        """
        Creating an item view subclass with a custom model factory.
        """
        class TestModel(ItemModel):
            pass

        class CustomItemView(self.viewType):
            modelFactory = TestModel

        iv = CustomItemView(item=self.item)
        self.assertTrue(isinstance(iv.model, TestModel))



class ItemViewTests(ItemViewBaseTests):
    """
    Tests for L{methanal.view.ItemView}.
    """
    viewType = view.ItemView

    def test_invoke(self):
        """
        Invoking an item view will set the attributes on the underlying item to
        the invoked values for the available inputs.
        """
        iv = self.viewType(item=self.item)
        # Without inputs, invoking the item view won't do anything.
        view.TextInput(parent=iv, name='foo')
        view.CheckboxInput(parent=iv, name='bar')
        iv.invoke({'foo': u'hello',
                   'bar': False})

        item = iv.item
        self.assertIdentical(item, self.item)
        self.assertEquals(item.foo, u'hello')
        self.assertEquals(item.bar, False)


    def test_invokeWithItemClass(self):
        """
        Invoking an item view, without a concrete underlying item, will create
        the item, with the invoked values, when invoked.
        """
        iv = self.viewType(
            store=self.store, itemClass=type(self.item), switchInPlace=True)
        self.assertIdentical(iv.item, None)
        # Without inputs, invoking the item view won't do anything.
        view.TextInput(parent=iv, name='foo')
        view.CheckboxInput(parent=iv, name='bar')
        iv.invoke({'foo': u'hello',
                   'bar': False})

        item = iv.item
        self.assertNotIdentical(item, None)
        self.assertEquals(item.foo, u'hello')
        self.assertEquals(item.bar, False)



class AutoItemViewTests(ItemViewTests):
    """
    Tests for L{methanal.view.AutoItemView}.
    """
    viewType = view.AutoItemView
