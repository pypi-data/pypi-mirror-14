from twisted.trial.unittest import TestCase
from twisted.python.versions import Version
from twisted.python.deprecate import _getDeprecationWarningString
from twisted.python.deprecate import DEPRECATION_WARNING_FORMAT


from axiom.store import Store
from axiom.item import Item
from axiom.attributes import integer, text, textlist, reference
from axiom.dependency import installOn

from xmantissa.website import WebSite

from methanal import errors, model as mmodel
from methanal.model import (Model, ItemModel, constraint, Value, Enum, List,
    loadFromItem)
from methanal.view import (LiveForm, FormGroup, ItemView, GroupInput,
    IntegerInput)



_marker = object()



class MethanalTests(TestCase):
    def test_constraints(self):
        def _constraint(value):
            if value != 5:
                return u'Value must be 5'

        param = Value(name='param')
        param._constraint = constraint(_constraint)
        self.assertFalse(param.isValid(4))
        self.assertTrue(param.isValid(5))

        model = Model([param])
        param.value = 3
        self.assertRaises(errors.ConstraintError, model.process)


    def test_enumeration(self):
        param = Enum(name='param', values=range(5))
        self.assertTrue(param.isValid(3))
        self.assertFalse(param.isValid(10))


    def test_processing(self):
        model = Model(
            params=[
                Value(name='foo', value=4),
                Value(name='bar', value=u'quux')])
        result = model.process()
        self.assertEquals(result, dict(foo=4, bar=u'quux'))


    def test_repr(self):
        """
        L{methanal.model.Value} has a useful human-readable representation.
        """
        self.assertEquals(
            repr(Value(name='foo', value=u'bar')),
            "<Value name='foo' value=u'bar' doc=u'foo'>")
        self.assertEquals(
            repr(Value(name='foo', value=u'bar', doc=u'Hello')),
            "<Value name='foo' value=u'bar' doc=u'Hello'>")



class ParameterTests(TestCase):
    def test_enumerationValidation(self):
        param = List(name='foo')
        self.assertTrue(param.isValid([]))
        self.assertTrue(param.isValid(None))
        self.assertFalse(param.isValid(5))



class _DummyItem(Item):
    i = integer(default=5)
    t = text(doc=u'param t')
    tl = textlist(doc=u'param tl')



class _DummyChildItem(Item):
    i = integer(default=5)



class _DummyParentItem(Item):
    r = reference(reftype=_DummyChildItem, doc=u'dummy reference')



class _BrokenReference(Item):
    r = reference()



class AttributeTests(TestCase):
    def test_valueParamNoDoc(self):
        param = Value.fromAttr(_DummyItem.i)
        self.assertIdentical(type(param), Value)
        self.assertEqual(param.name, 'i')
        self.assertEqual(param.value, 5)
        self.assertEqual(param.doc, 'i')


    def test_valueParam(self):
        param = Value.fromAttr(_DummyItem.t)
        self.assertIdentical(type(param), Value)
        self.assertEqual(param.name, 't')
        self.assertEqual(param.value, None)
        self.assertEqual(param.doc, 'param t')


    def test_listParam(self):
        param = List.fromAttr(_DummyItem.tl)
        self.assertIdentical(type(param), List)
        self.assertEqual(param.name, 'tl')
        self.assertEqual(param.value, None)
        self.assertEqual(param.doc, 'param tl')



class ItemUtilityTests(TestCase):
    def test_loadFromItem(self):
        item = _DummyItem(i=55, t=u'lulz')
        model = Model(params=[Value.fromAttr(_DummyItem.i),
                              Value.fromAttr(_DummyItem.t)])
        loadFromItem(model, item)
        self.assertEqual(model.params['i'].value, item.i)
        self.assertEqual(model.params['t'].value, item.t)



class AutoSchemaTests(TestCase):
    expectedParams = {
        'i': (Value(name='i', doc=u'i'), 5, 5),
        't': (Value(name='t', doc=u'param t'), None, u'text'),
        'tl': (List(name='tl', doc=u'param tl'), None, [u'text1', u'text2']),
        }


    def setUp(self):
        self.store = Store()


    def test_schemaAnalysis(self):
        """
        Test that parameters are correctly synthesized from an Item schema.
        """
        store = Store()
        model = ItemModel(itemClass=_DummyItem, store=store)
        params = model.params

        self.assertEquals(params.keys(), self.expectedParams.keys())
        for k in params:
            p1 = params[k]
            p2, classDefault, itemDefault = self.expectedParams[k]
            self.assertIdentical(type(p1), type(p2))
            self.assertEquals(p1.name, p2.name)
            self.assertEquals(p1.value, classDefault)
            self.assertEquals(p1.doc, p2.doc)


    def test_schemaIgnore(self):
        """
        Test that ignoredAttributes is respected.
        """
        store = Store()
        model = ItemModel(
            itemClass=_DummyItem, store=store, ignoredAttributes=set(['tl']))
        params = model.params
        self.assertNotIn('tl', params)


    def test_itemAnalysis(self):
        dummyItem = _DummyItem(
            store=self.store, i=5, t=u'text', tl=[u'text1', u'text2'])
        model = ItemModel(item=dummyItem)
        params = model.params
        for k in params:
            p1 = params[k]
            p2, classDefault, itemDefault = self.expectedParams[k]
            self.assertEquals(p1.value, itemDefault)


    def test_itemCreation(self):
        model = ItemModel(itemClass=_DummyItem, store=self.store)
        model.params['i'].value = 7
        model.params['t'].value = u'foo'

        self.assertIdentical(model.item, None)

        model.process()

        self.assertEquals(model.item.i, 7)
        self.assertEquals(model.item.t, u'foo')


    def test_itemEditing(self):
        model = ItemModel(item=_DummyItem(store=self.store))
        model.params['i'].value = 7
        model.params['t'].value = u'foo'

        model.process()

        self.assertEquals(model.item.i, 7)
        self.assertEquals(model.item.t, u'foo')


    def test_referenceAttributeCreating(self):
        dummyParent = _DummyParentItem(store=self.store, r=None)
        model = ItemModel(dummyParent)
        self.assertIdentical(dummyParent.r, None)

        model.process()
        self.assertEquals(dummyParent.r.i, 5)


    def test_referenceAttributeEditing(self):
        dummyChild = _DummyChildItem(store=self.store, i=5)
        dummyParent = _DummyParentItem(store=self.store, r=dummyChild)
        model = ItemModel(dummyParent)
        self.assertIdentical(dummyParent.r, dummyChild)

        model.params['r'].model.params['i'].value = 6
        model.process()
        self.assertIdentical(dummyParent.r, dummyChild)
        self.assertEquals(dummyChild.i, 6)


    def test_noRefType(self):
        """
        Attempting to automatically synthesise a model for an Item with a
        C{reference} attribute with no C{'reftype'} raises C{ValueError}.
        """
        brokenParent = _BrokenReference(store=self.store)
        self.assertRaises(ValueError, ItemModel, brokenParent)



class _DummyControl(object):
    invoked = 0


    def __init__(self, parent):
        parent.addFormChild(self)


    def invoke(self, data):
        self.invoked += 1



class LiveFormTests(TestCase):
    def setUp(self):
        s = self.store = Store()
        installOn(WebSite(store=s), s)

        self.model = Model(
            params=[
                Value(name='foo', value=4),
                Value(name='bar', value=u'quux')])


    def test_process(self):
        view = LiveForm(self.store, self.model)
        control = _DummyControl(view)
        view.invoke({})
        self.assertEquals(control.invoked, 1)


    def test_groups(self):
        view = LiveForm(self.store, self.model)
        group = FormGroup(view)
        control = _DummyControl(group)
        view.invoke({})
        self.assertEquals(control.invoked, 1)



class _DummyParameter(object):
    name = u'DUMMY_PARAMETER'
    value = u'DUMMY_PARAMETER_VALUE'
    doc = ''



class _DummyLiveForm(object):
    page = None
    liveFragmentChildren = []
    model = Model(params=[])


    def addFormChild(self, *args):
        pass


    def getParameter(self, name):
        return _DummyParameter()



class _GroupTestView(ItemView):
    def __init__(self, *args, **kw):
        super(_GroupTestView, self).__init__(*args, **kw)
        group = GroupInput(parent=self, name='r')
        IntegerInput(parent=group, name='i')



class GroupInputTests(TestCase):
    def setUp(self):
        self.store = Store()
        installOn(WebSite(store=self.store), self.store)


    def test_editing(self):
        dummyChild = _DummyChildItem(store=self.store)
        dummyParent = _DummyParentItem(store=self.store, r=dummyChild)
        view = _GroupTestView(item=dummyParent)
        self.assertIdentical(dummyParent.r, dummyChild)

        view.invoke({u'r': {u'i': 6}})

        self.assertIdentical(dummyParent.r, dummyChild)
        self.assertEquals(dummyChild.i, 6)


    def test_creation(self):
        dummyParent = _DummyParentItem(store=self.store, r=None)
        view = _GroupTestView(item=dummyParent, switchInPlace=True)
        self.assertIdentical(dummyParent.r, None)

        view.invoke({u'r': {u'i': 6}})

        self.assertEquals(dummyParent.r.i, 6)



class ModelTests(TestCase):
    def test_attach(self):
        model = Model()
        p = Value(name='foo')
        model.attach(p)
        self.assertIdentical(model.params['foo'], p)


    def test_attachMany(self):
        model = Model()
        p1 = Value(name='foo')
        p2 = Value(name='bar')

        model.attach(p1, p2)
        self.assertIdentical(model.params['foo'], p1)
        self.assertIdentical(model.params['bar'], p2)



class DeprecatedAttributesTests(TestCase):
    """
    Tests for deprecated attributes in L{methanal.model}.
    """
    version020 = Version('methanal', 0, 2, 0)


    def _getWarningString(self, obj, name, version):
        """
        Create the warning string used by deprecated attributes.
        """
        return _getDeprecationWarningString(
            obj.__name__ + '.' + name,
            version,
            DEPRECATION_WARNING_FORMAT + ': ')


    def assertDeprecated(self, obj, name, version):
        """
        Assert that the attribute C{name} on C{obj} was deprecated in
        C{version}, by testing whether a deprecation warning was issued.
        """
        getattr(obj, name)
        warningsShown = self.flushWarnings([
            self.assertDeprecated])
        self.assertEquals(len(warningsShown), 1)
        self.assertIdentical(warningsShown[0]['category'], DeprecationWarning)
        self.assertIn(self._getWarningString(obj, name, version),
                      warningsShown[0]['message'])


    def test_valueParameter(self):
        """
        L{methanal.model.ValueParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'ValueParameter', self.version020)


    def test_listParameter(self):
        """
        L{methanal.model.ListParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'ListParameter', self.version020)


    def test_enumerationParameter(self):
        """
        L{methanal.model.EnumerationParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'EnumerationParameter', self.version020)


    def test_decimalParameter(self):
        """
        L{methanal.model.DecimalParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'DecimalParameter', self.version020)


    def test_storeIDParameter(self):
        """
        L{methanal.model.StoreIDParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'StoreIDParameter', self.version020)


    def test_multiEnumerationParameter(self):
        """
        L{methanal.model.MultiEnumerationParameter} is deprecated.
        """
        self.assertDeprecated(mmodel, 'MultiEnumerationParameter', self.version020)
