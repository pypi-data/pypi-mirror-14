from twisted.python.deprecate import deprecatedModuleAttribute
from twisted.python.versions import Version

from axiom import attributes

from nevow.util import Expose

from methanal import errors
from methanal.util import propertyMaker



constraint = Expose(
    """
    Register one or more functions as constraints for a particular form
    parameter.
    """)



class Value(object):
    """
    A simple value in a model.

    @type name: C{str}
    @ivar name: Name of this parameter

    @ivar value: Initial value of this parameter

    @type doc: C{unicode}
    @ivar doc: A long description of this parameter
    """
    def __init__(self, name, value=None, doc=None, **kw):
        """
        Initialise the parameter.

        @type name: C{str}
        @ivar name: Name of this parameter

        @ivar value: Initial value of this parameter

        @type doc: C{unicode}
        @ivar doc: A long description of this parameter, or C{None} to use the
            parameter's name
        """
        super(Value, self).__init__(**kw)
        self.name = name
        self.value = value
        if doc is None:
            doc = name.decode('ascii')
        self.doc = doc


    def __repr__(self):
        return '<%s name=%r value=%r doc=%r>' % (
            type(self).__name__,
            self.name,
            self.value,
            self.doc)


    @classmethod
    def fromAttr(cls, attr, **kw):
        """
        Construct a parameter from an Axiom attribute.
        """
        kw.setdefault('name', attr.attrname)
        kw.setdefault('value', attr.default)
        kw.setdefault('doc', attr.doc or None)
        return cls(**kw)


    def validate(self, value):
        """
        Validate a value provided for this parameter against all constraints.

        If any constraints were violated a descriptive message is returned,
        otherwise C{None} is returned upon successful validation.
        """
        for constraintName in constraint.exposedMethodNames(self):
            result = constraint.get(self, constraintName)(value)
            if result is not None:
                return result


    def isValid(self, value):
        """
        Determine whether C{value} is valid data for this parameter.
        """
        return self.validate(value) is None


    def getValue(self):
        """
        Retrieve the value for this parameter.

        @raise errors.ConstraintError: If validation for this parameter's value
            failed
        """
        error = self.validate(self.value)
        if error:
            raise errors.ConstraintError(error)
        return self.value



class List(Value):
    """
    A model parameter consisting of multiple values.
    """
    @constraint
    def isIterable(self, value):
        """
        Enforce the iterable constraint.
        """
        try:
            iter(value)
        except TypeError:
            if value is not None:
                return u'Value is not an iterable'



class Enum(Value):
    """
    An enumeration value in a model.

    The value for this parameter must be chosen from a sequence of predefined
    possibilities.

    @ivar values: A sequence of values present in the enumeration
    """
    def __init__(self, values, **kw):
        super(Enum, self).__init__(**kw)
        self.values = values


    @constraint
    def valueInEnumeration(self, value):
        """
        Enforce the enumeration constraint.
        """
        if value not in self.values:
            return u'Value not present in enumeration'



class MultiEnum(Enum):
    """
    A multi-value enumeration model parameter.
    """
    @constraint
    def valueInEnumeration(self, value):
        """
        Enforce the enumeration constraint.
        """
        for v in value:
            if v not in self.values:
                return u'Value not present in enumeration'



class ReferenceParameter(Value):
    """
    XXX: hax :<

    Really, don't use this unless you know what you are doing.
    """
    def __init__(self, model, **kw):
        self.model = model
        super(ReferenceParameter, self).__init__(**kw)


    @classmethod
    def fromAttr(cls, attr, model, **kw):
        return super(ReferenceParameter, cls).fromAttr(attr, model=model)


    @propertyMaker
    def value():
        def get(self):
            return self.model.item
        def set(self, data):
            self.model.item = data
        return get, set


    def getValue(self):
        return self.model.process()



class DecimalValue(Value):
    """
    A decimal number model parameter.
    """
    def __init__(self, decimalPlaces, **kw):
        super(DecimalValue, self).__init__(**kw)
        self.decimalPlaces = decimalPlaces


    @classmethod
    def fromAttr(cls, attr, **kw):
        kw.setdefault('decimalPlaces', attr.decimalPlaces)
        return super(DecimalValue, cls).fromAttr(attr, **kw)



class ForeignRef(Value):
    """
    XXX: Describe me.
    """
    def __init__(self, itemType, store, **kw):
        super(ForeignRef, self).__init__(**kw)
        self.itemType = itemType
        self.store = store

    @classmethod
    def fromAttr(cls, attr, store, **kw):
        return super(ForeignRef, cls).fromAttr(
            attr, itemType=attr.reftype, store=store, **kw)



def mandatory(value):
    """
    An external constraint that prohibits a value of C{None}.
    """
    if value is None:
        return u'Value is mandatory'



class Model(object):
    """
    A Methanal form model.
    """
    def __init__(self, params=[], callback=lambda **d: d, doc=u''):
        """
        Initialise the model.

        @type params: C{iterable} of parameter instances
        @param params: Model parameters

        @type callback: C{callable} taking parameters named the same as the
            model parameters

        @type doc: C{unicode}
        @param doc: A description for the model's action
        """
        self.params = {}
        self.attach(*params)

        self.callback = callback
        self.doc = doc


    def attach(self, *params):
        """
        Attach parameters to this model.

        @param *params: The parameters to attach.
        """
        for param in params:
            self.params[param.name] = param


    def process(self):
        """
        Invoke L{self.callback} with all the model parameter data.
        """
        data = self.getData()
        return self.callback(**data)


    def getData(self):
        """
        Get all of the model parameters' values.

        @rtype: C{dict} mapping C{str} to values
        """
        data = {}
        for param in self.params.itervalues():
            data[param.name] = param.getValue()
        return data



_paramTypes = {
    attributes.integer:        Value,
    attributes.ieee754_double: Value,
    attributes.text:           Value,
    attributes.boolean:        Value,
    attributes.textlist:       List,
    attributes.timestamp:      Value}

def paramFromAttribute(store, attr, value, name=None):
    doc = attr.doc or None

    if name is None:
        name = attr.attrname

    if isinstance(attr, attributes.reference):
        if attr.reftype is None:
            raise ValueError('%r has no reference type' % (attr,))
        model = ItemModel(item=value, itemClass=attr.reftype, store=store)
        return ReferenceParameter(name=name,
                                  value=value,
                                  doc=doc,
                                  model=model)
    elif isinstance(attr, attributes.AbstractFixedPointDecimal):
        return DecimalValue(name=name,
                            value=value,
                            doc=doc,
                            decimalPlaces=attr.decimalPlaces)
    else:
        factory = _paramTypes.get(type(attr))
        if factory:
            return factory(name=name,
                           value=value,
                           doc=doc)



def paramsFromSchema(store, itemClass, item=None, ignoredAttributes=set()):
    """
    Construct model parameters from an Axiom item schema.

    @type store: L{axiom.store.Store}
    @param store: Store used for reference attributes in the item schema

    @type itemClass: C{type}
    @param itemClass: Item type whose schema model parameters are based on

    @type item: L{axiom.item.Item}
    @param item: Item instance used for retrieving attribute values, or
        C{None} to use the attribute's default

    @type ignoredAttributes: C{set} of C{str}
    @param ignoredAttributes: Names of attributes to skip creating parameters
        for

    @rtype: C{iterable} of model parameters
    """
    for name, attr in itemClass.getSchema():
        if name in ignoredAttributes:
            continue

        if item is not None:
            value = getattr(item, name)
        else:
            value = attr.default

        yield paramFromAttribute(store, attr, value, name)



class ItemModelBase(Model):
    """
    A model backed by an item or item class.
    """
    def __init__(self, item=None, itemClass=None, store=None, doc=u'Save',
                 **kw):
        """
        Initialise model.

        Either C{item} or C{itemClass} must be specified, specifying only
        an item class will result in an item of that type being created
        when the model's callback is triggered.  This can be useful for
        providing a model for an item type that you wish to create but
        have no instance of yet.

        @type item: C{axiom.item.Item}
        @param item: An Axiom item to synthesize a model for, or C{None}
            to create an item of L{itemClass} when the callback is triggered

        @type itemClass: C{type}
        @param itemClass: Item type to synthesize a model and create an
            instance for, or C{None} to use the type of L{item}

        @type store: C{axiom.store.Store}
        """
        super(ItemModelBase, self).__init__(
            callback=self.storeData, doc=doc, **kw)

        if item is None:
            if itemClass is None:
                raise ValueError('You must pass in either item or itemClass')

            self.item = None
            self.itemClass = itemClass
        else:
            self.item = item

        self.itemClass = itemClass or type(item)
        self.store = store or item.store


    def _storeData(self, data):
        """
        Store model data.
        """
        if self.item is None:
            self.item = self.itemClass(store=self.store, **data)
            self.createItem(self.item)
        else:
            for name, value in data.iteritems():
                setattr(self.item, name, value)
        return self.stored(self.item)


    def storeData(self, **data):
        """
        Model callback.

        Write model parameter values back to our item, creating a new one if
        no item instance was given.

        @rtype: C{axiom.item.Item}
        @return: The newly modified or created item
        """

        if self.store is not None:
            return self.store.transact(self._storeData, data)
        else:
            return self._storeData(data)


    def createItem(self, item):
        """
        Callback for item creation.

        @param item: The newly-created item.
        """


    def stored(self, item):
        """
        Callback for saved item.

        @param item: The modified or newly-created item.
        """



class ItemModel(ItemModelBase):
    """
    A model automatically synthesized from an Item class or instance.
    """
    def __init__(self, item=None, itemClass=None, store=None,
                 ignoredAttributes=None, **kw):
        """
        @type ignoredAttibutes: C{container}
        @param ignoredAttributes: Attribute names to ignore when synthesizing
            the model
        """
        super(ItemModel, self).__init__(
            item=item, itemClass=itemClass, store=store, params=[], **kw)

        if ignoredAttributes is None:
            ignoredAttributes = set()
        self.ignoredAttributes = ignoredAttributes

        params = paramsFromSchema(
            self.store, self.itemClass, self.item, self.ignoredAttributes)
        self.attach(*params)


    def stored(self, item):
        return item



def modelFromItem(item, ignoredAttributes=None):
    """
    Automatically synthesize a model from an Item instance.
    """
    return ItemModel(item=item, ignoredAttributes=ignoredAttributes)



def modelFromItemClass(itemClass, store=None, ignoredAttributes=None):
    """
    Automatically synthesize a model from an Item class.
    """
    return ItemModel(itemClass=itemClass,
                     store=store,
                     ignoredAttributes=ignoredAttributes)



def loadFromItem(model, item):
    """
    Initialise model parameters from an Axiom item instance.

    @type model: L{Model}

    @type item: L{axiom.item.Item}
    """
    for name, param in model.params.iteritems():
        param.value = getattr(item, name)



ValueParameter = Value
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.Value instead', __name__, 'ValueParameter')

ListParameter = List
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.List instead', __name__, 'ListParameter')

EnumerationParameter = Enum
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.Enum instead', __name__, 'EnumerationParameter')

DecimalParameter = DecimalValue
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.DecimalValue instead', __name__, 'DecimalParameter')

StoreIDParameter = ForeignRef
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.ForeignRefinstead', __name__, 'StoreIDParameter')

MultiEnumerationParameter = MultiEnum
deprecatedModuleAttribute(
    Version('methanal', 0, 2, 0),
    'use methanal.model.MultiEnum', __name__, 'MultiEnumerationParameter')
