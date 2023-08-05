import itertools
from warnings import warn
from zope.interface import implements

from decimal import Decimal

from epsilon.extime import Time

from twisted.python.components import registerAdapter
from twisted.python.versions import Version
from twisted.python.deprecate import deprecated

from axiom.attributes import text, integer, timestamp, boolean, ieee754_double

from nevow.inevow import IAthenaTransportable
from nevow.page import renderer
from nevow.athena import expose

from xmantissa.ixmantissa import IWebTranslator
from xmantissa.webtheme import ThemedElement

from methanal import errors
from methanal.imethanal import IEnumeration
from methanal.model import ItemModel, Model, paramFromAttribute
from methanal.util import getArgsDict, CurrencyFormatter, DecimalFormatter
from methanal.enums import ListEnumeration



class FormAction(ThemedElement):
    """
    L{LiveForm} action.

    @type defaultName: C{unicode}
    @cvar defaultName: Default name for the action.

    @type allowViewOnly: C{bool}
    @cvar allowViewOnly: Allow this action to be enabled in a "view only" form.

    @type name: C{unicode}
    @ivar name: Action name.

    @type id: C{unicode}
    @ivar id: Action identifier.
    """
    defaultName = None
    allowViewOnly = False
    identifier = None


    def __init__(self, name=None, identifier=None, **kw):
        super(FormAction, self).__init__(**kw)
        if not name:
            name = self.defaultName
        if identifier is None:
            identifier = self.identifier
            if identifier is None:
                identifier = unicode(id(self))
        self.name = name
        self.id = identifier


    def getInitialArguments(self):
        return [getArgsDict(self)]


    def getArgs(self):
        return {u'actionID': self.id,
                u'allowViewOnly': self.allowViewOnly,
                u'identifier': self.identifier}



class ActionButton(FormAction):
    """
    L{LiveForm} action represented by a push button.

    @type button: C{str}
    @cvar button: Button type, should correspond with values for the C{button}
        element in HTML forms
    """
    fragmentName = 'methanal-action-button'
    type = 'button'


    @renderer
    def button(self, req, tag):
        return tag(type=self.type)[self.name]



class SubmitAction(ActionButton):
    """
    L{LiveForm} action for submitting a form.
    """
    jsClass = u'Methanal.View.SubmitAction'
    defaultName = u'Submit'
    type = 'submit'
    identifier = u'submit'



class ResetAction(ActionButton):
    """
    L{LiveForm} action for resetting a form's controls.
    """
    jsClass = u'Methanal.View.ResetAction'
    allowViewOnly = True
    defaultName = u'Reset'
    type = 'reset'
    identifier = u'reset'



class ActionContainer(ThemedElement):
    """
    Container for L{FormAction}s.

    @type actions: C{list} of L{FormAction}
    """
    fragmentName = 'methanal-action-container'
    jsClass = u'Methanal.View.ActionContainer'


    def __init__(self, actions, **kw):
        super(ActionContainer, self).__init__(**kw)
        self.actions = []
        for action in actions:
            self.addAction(action)


    def getInitialArguments(self):
        return [getArgsDict(self)]


    def getArgs(self):
        actionIDs = dict.fromkeys(action.id for action in self.actions)
        return {u'actionIDs': actionIDs}


    def addAction(self, action):
        """
        Add an action to the form.

        @type action: L{FormAction}
        """
        self.actions.append(action)


    @renderer
    def formActions(self, req, tag):
        for action in self.actions:
            action.setFragmentParent(self)
            yield action



class SimpleForm(ThemedElement):
    """
    A simple form.

    Simple forms do not contain any submission mechanism.

    @type store: L{axiom.store.Store}
    @ivar store: Backing Axiom store

    @type model: L{Model}
    @ivar model: Model supporting the form inputs
    """
    fragmentName = 'methanal-simple-form'
    jsClass = u'Methanal.View.SimpleForm'


    def __init__(self, store, model, **kw):
        """
        Initialise the form.
        """
        super(SimpleForm, self).__init__(**kw)
        self.store = store
        self.model = model
        self.formChildren = []


    def getInitialArguments(self):
        keys = [c.name for c in self.getAllControls()]
        return [keys]


    def getAllControls(self):
        """
        Get all of the form's child inputs recursively.
        """
        def _getChildren(container, form):
            for child in container.formChildren:
                if hasattr(child, 'formChildren'):
                    if child.model is form.model:
                        for child in _getChildren(child, form):
                            yield child
                else:
                    yield child

        return _getChildren(self, self)


    def addFormChild(self, child):
        """
        Add a new child to the form.

        @param child: Input to add as a child of the form
        """
        self.formChildren.append(child)


    def getParameter(self, name):
        """
        Get a model parameter by name.

        @type name: C{str}
        @param name: Model parameter name

        @rtype: C{methanal.model.Value}
        @return: Named model parameter
        """
        return self.model.params[name]


    @renderer
    def children(self, req, tag):
        """
        Render the child inputs.
        """
        return self.formChildren



class LiveForm(SimpleForm):
    """
    A form view implemented as an Athena widget.

    @type viewOnly: C{bool}
    @ivar viewOnly: Flag indicating whether model values are written back when
        invoked.

    @type hideModificationIndicator: C{bool}
    @ivar hideModificationIndicator: Hide the modification indicator for this
        form? Defaults to C{False}.

    @type hideValidationErrorIndicator: C{bool}
    @ivar hideValidationErrorIndicator: Hide the validation error indicator for
        this form? Defaults to C{False}.

    @type actions: L{ActionContainer}

    @type doc: C{unicode}
    @ivar doc: Form title, or C{None} for no title.
    """
    fragmentName = 'methanal-liveform'
    jsClass = u'Methanal.View.LiveForm'


    def __init__(self, store, model, viewOnly=False, actions=None, doc=None,
                 **kw):
        super(LiveForm, self).__init__(store=store, model=model, **kw)
        if self.model.doc is None:
            viewOnly = True
        self.viewOnly = viewOnly

        if actions is None:
            actions = ActionContainer(
                actions=[SubmitAction(name=self.model.doc)])
        self.actions = actions
        self.doc = doc

        self.hideModificationIndicator = False
        self.hideValidationErrorIndicator = False


    def getInitialArguments(self):
        args = super(LiveForm, self).getInitialArguments()
        return [getArgsDict(self)] + args


    def getArgs(self):
        return {
            u'viewOnly': self.viewOnly,
            u'hideModificationIndicator': self.hideModificationIndicator,
            u'hideValidationErrorIndicator': self.hideValidationErrorIndicator}


    @renderer
    def formCaption(self, req, tag):
        if self.doc:
            return tag[self.doc]
        return []


    @renderer
    def formActions(self, req, tag):
        self.actions.setFragmentParent(self)
        return tag[self.actions]


    @expose
    def invoke(self, data):
        """
        Process form data for each child input.

        The callback for L{self.model} is invoked once all the child inputs
        have been invoked.

        @type data: C{dict}
        @param data: Form data.

        @raise RuntimeError: If L{self.viewOnly} is C{True}.

        @return: The result of the model's callback function.
        """
        if self.viewOnly:
            raise RuntimeError('Attempted to submit view-only form')

        for child in self.formChildren:
            child.invoke(data)
        return self.model.process()



class InputContainer(ThemedElement):
    """
    Generic container for form inputs.
    """
    jsClass = u'Methanal.View.InputContainer'


    def __init__(self, parent, doc=u'', **kw):
        """
        Initialise the container.

        @param parent: Parent input

        @type doc: C{unicode}
        @param doc: Input caption
        """
        super(InputContainer, self).__init__(**kw)
        parent.addFormChild(self)
        self.setFragmentParent(parent)
        self.parent = parent
        self.doc = doc
        self.model = self.parent.model
        self.store = self.parent.store
        self.formChildren = []


    def addFormChild(self, child):
        """
        Add a new child to the form.
        """
        self.formChildren.append(child)


    def getParameter(self, name):
        """
        Get a model parameter, from the container parent, by name.

        @type name: C{str}
        @param name: Model parameter name

        @rtype: C{methanal.model.Value}
        @return: Named model parameter
        """
        return self.parent.getParameter(name)


    @renderer
    def caption(self, req, tag):
        """
        Render the input's caption.
        """
        return tag[self.doc]


    @renderer
    def children(self, req, tag):
        """
        Render the input's child inputs.
        """
        return self.formChildren


    def invoke(self, data):
        """
        Process form data for each child input.

        @type data: C{dict}
        @param data: Form data
        """
        for child in self.formChildren:
            child.invoke(data)



class FormGroup(InputContainer):
    """
    Container for visually grouping inputs.

    A C{FormGroup} will be set inactive (and thus hidden) if all of its
    child controls are inactive too.
    """
    fragmentName = 'methanal-group'



class FormRow(InputContainer):
    """
    Container for visually organising inputs into rows.
    """
    fragmentName = 'methanal-form-row'
    jsClass = u'Methanal.View.FormRow'



# XXX: Do we still need this revolting hack?
class GroupInput(FormGroup):
    """
    Container for grouping controls belonging to a ReferenceParameter submodel.

    XXX: This API should be considered extremely unstable.
    """
    jsClass = u'Methanal.View.GroupInput'


    def __init__(self, parent, name):
        self.param = parent.getParameter(name)
        super(GroupInput, self).__init__(parent=parent, doc=self.param.doc)
        self.model = self.param.model
        self.name = name


    def getInitialArguments(self):
        keys = (unicode(n, 'ascii') for n in self.model.params)
        return [self.param.name.decode('ascii'),
                dict.fromkeys(keys, 1)]


    def getParameter(self, name):
        """
        Get a model parameter by name.

        @type name: C{str}
        @param name: Model parameter name

        @rtype: C{methanal.model.Value}
        @return: Named model parameter
        """
        return self.model.params[name]


    def invoke(self, data):
        ourData = data[self.name]
        for child in self.formChildren:
            child.invoke(ourData)



class FormInput(ThemedElement):
    """
    Abstract input widget class.
    """
    def __init__(self, parent, name, label=None, **kw):
        """
        Initialise the input.

        @param parent: Parent input

        @type name: C{str}
        @param name: Name of the model parameter this input represents

        @type label: C{unicode}
        @param label: Input's label or caption, or C{None} to use the
            model parameter's C{doc} attribute
        """
        super(FormInput, self).__init__(**kw)
        self.parent = parent
        self.name = unicode(name, 'ascii')
        self.param = parent.getParameter(name)

        self.store = parent.store

        if label is None:
            label = self.param.doc
        self.label = label

        if not isinstance(parent, FormRow):
            container = FormRow(parent=parent, doc=self.param.doc)
            container.addFormChild(self)
            self.setFragmentParent(container)
        else:
            parent.addFormChild(self)
            self.setFragmentParent(parent)


    def getInitialArguments(self):
        return [getArgsDict(self)]


    def getArgs(self):
        """
        Get input-specific arguments.
        """
        return {u'name':  self.name,
                u'value': self.getValue(),
                u'label': self.label}


    @renderer
    def value(self, req, tag):
        """
        Render the input's value.
        """
        value = self.getValue()
        if value is None:
            value = u''
        return tag[value]


    @renderer
    def renderName(self, req, tag):
        """
        Render the input's name.
        """
        return tag[self.name]


    def invoke(self, data):
        """
        Set the model parameter's value from form data.
        """
        self.param.value = data[self.param.name]


    def getValue(self):
        """
        Get the model parameter's value.
        """
        return self.param.value



class TextAreaInput(FormInput):
    """
    Multi-line text input.
    """
    fragmentName = 'methanal-text-area-input'
    jsClass = u'Methanal.View.TextAreaInput'



class TextInput(FormInput):
    """
    Text input.

    @type embeddedLabel: C{bool}
    @ivar embeddedLabel: Place a label in the text input control when the
        input is empty?

    @type stripWhitespace: C{bool}
    @ivar stripWhitespace: Strip trailing and leading whitespace from user
        input?

    @type formatter: C{ITextFormatter} adaptable to C{IAthenaTransportable}
    @ivar formatter: Text formatter, transported to the client side, to
        provide the friendly representation of the input; or C{None} for the
        default formatter.
    """
    fragmentName = 'methanal-text-input'
    jsClass = u'Methanal.View.TextInput'


    def __init__(self, embeddedLabel=False, stripWhitespace=True,
                 formatter=None, **kw):
        super(TextInput, self).__init__(**kw)
        self.embeddedLabel = embeddedLabel
        self.stripWhitespace = stripWhitespace
        self.formatter = formatter


    def getArgs(self):
        return {u'embeddedLabel':   self.embeddedLabel,
                u'stripWhitespace': self.stripWhitespace,
                u'formatter':       self.formatter}



class FilteringTextInput(TextInput):
    """
    A L{TextInput} that allows real time filtering on the input and provides
    customizable default validation.

    See the JavaScript docstrings for more detail.

    @type expression: C{unicode}
    @ivar expression: A regular expression that specifies what characters
        are allowed to be part of the value of the input field, or C{None}
        for no validation

        For example::

            - Allow alphanumerics: [a-zA-z0-9]
            - Allow either the string "cat" or "dog": cat|dog
    """
    jsClass = u'Methanal.View.FilteringTextInput'


    def __init__(self, expression=None, **kw):
        super(FilteringTextInput, self).__init__(**kw)
        self.expression = expression


    def getArgs(self):
        return {u'expression': self.expression}



class PrePopulatingTextInput(TextInput):
    """
    Text input that updates another input's value with its own in real time.

    @type targetControlName: C{str}
    @ivar targetControlName: The name of the input to pre-populate
    """
    jsClass = u'Methanal.View.PrePopulatingTextInput'


    def __init__(self, targetControlName, **kw):
        super(PrePopulatingTextInput, self).__init__(**kw)
        self.targetControlName = unicode(targetControlName, 'ascii')


    def getArgs(self):
        return {u'targetControlName': self.targetControlName}



class DateInput(TextInput):
    """
    Textual date input.

    A variety of date formats is supported, in order make entering an
    absolute date value as natural as possible. See the Javascript
    docstrings for more detail.

    @type timezone: C{datetime.tzinfo}
    @ivar timezone: A C{tzinfo} implementation, representing the timezone
        this date input is relative to

    @type twentyFourHours: C{bool}
    @ivar twentyFourHours: Display human readable time in 24-hour
        format?
    """
    jsClass = u'Methanal.View.DateInput'


    def __init__(self, timezone, twentyFourHours=False, **kw):
        super(DateInput, self).__init__(**kw)
        self.timezone = timezone
        self.twentyFourHours = twentyFourHours


    def getArgs(self):
        return {u'twentyFourHours': self.twentyFourHours}


    def getValue(self):
        value = self.param.value
        if value is None:
            return u''

        dt = value.asDatetime(self.timezone)
        return u'%04d-%02d-%02d' % (dt.year, dt.month, dt.day)


    def invoke(self, data):
        value = data[self.param.name]
        if value is not None:
            value = Time.fromPOSIXTimestamp(value / 1000)
        self.param.value = value



class NumericInput(TextInput):
    """
    Base class for numeric inputs.

    @ivar minimumValue: Minimum allowed value, defaults to the smallest integer
        value allowed in SQLite.

    @ivar maximumValue: Maximum allowed value, defaults to the largest integer
        value allowed in SQLite.
    """
    MINIMUM = -9223372036854775808
    MAXIMUM =  9223372036854775807

    NO_BOUNDS = object()


    def __init__(self, minimumValue=None, maximumValue=None, **kw):
        super(NumericInput, self).__init__(**kw)
        if minimumValue is None:
            minimumValue = self.MINIMUM
        self.minimumValue = minimumValue

        if maximumValue is None:
            maximumValue = self.MAXIMUM
        self.maximumValue = maximumValue


    def getArgs(self):
        args = {}
        if self.minimumValue is not self.NO_BOUNDS:
            args[u'lowerBound'] = self.minimumValue - 1
        if self.maximumValue is not self.NO_BOUNDS:
            args[u'upperBound'] = self.maximumValue + 1
        return args


    def checkValue(self, value):
        """
        Check that C{value} is within the minimum and maximum ranges. Raise
        C{ValueError} if C{value} is outside of the allowed range.
        """
        if value is None:
            return
        maximumValue, minimumValue = self.maximumValue, self.minimumValue
        if maximumValue is not self.NO_BOUNDS and value > maximumValue:
            raise ValueError('%s is larger than %s' % (
                value, maximumValue))
        elif minimumValue is not self.NO_BOUNDS and value < minimumValue:
            raise ValueError('%s is smaller than %s' % (
                value, minimumValue))


    def convertValue(self, value):
        return value


    def invoke(self, data):
        value = self.convertValue(data[self.param.name])
        self.checkValue(value)
        self.param.value = value



class IntegerInput(NumericInput):
    """
    Integer input.
    """
    jsClass = u'Methanal.View.IntegerInput'


    def getValue(self):
        value = self.param.value
        if value is None:
            return u''
        return int(value)



class FloatInput(NumericInput):
    """
    Float input.
    """
    jsClass = u'Methanal.View.FloatInput'


    def __init__(self, minimumValue=NumericInput.NO_BOUNDS,
                 maximumValue=NumericInput.NO_BOUNDS, **kw):
        super(FloatInput, self).__init__(
            minimumValue=minimumValue, maximumValue=maximumValue, **kw)


    def convertValue(self, value):
        if value is not None:
            value = float(value)
        return value


    def getValue(self):
        value = self.param.value
        if value is None:
            return u''
        return float(value)



class DecimalInput(NumericInput):
    """
    Decimal input.

    @type decimalPlaces: C{int}
    @ivar decimalPlaces: The number of decimal places to allow, or C{None} to
        use the model parameter's value.
    """
    jsClass = u'Methanal.View.DecimalInput'


    def __init__(self, decimalPlaces=None, **kw):
        super(DecimalInput, self).__init__(**kw)
        if decimalPlaces is None:
            decimalPlaces = self.param.decimalPlaces
        self.decimalPlaces = decimalPlaces


    def convertValue(self, value):
        if value is not None:
            value = Decimal(str(value))
        return value


    def getArgs(self):
        return {u'decimalPlaces': self.decimalPlaces}


    def getValue(self):
        value = self.param.value
        if value is None:
            return u''

        return float(value)



class PercentInput(DecimalInput):
    """
    Decimal input, with values interpreted as percentages.
    """
    jsClass = u'Methanal.View.PercentInput'



class DecimalFormatterTransportable(object):
    """
    L{IAthenaTransportable} adapter for L{methanal.util.DecimalFormatter}.
    """
    implements(IAthenaTransportable)
    jsClass = u'Methanal.Util.DecimalFormatter'


    def __init__(self, formatter):
        self.formatter = formatter


    def getInitialArguments(self):
        f = self.formatter
        return [f.grouping, f.thousandsSeparator, f.decimalSeparator]

registerAdapter(DecimalFormatterTransportable, DecimalFormatter,
                IAthenaTransportable)



class CurrencyFormatterTransportable(object):
    """
    L{IAthenaTransportable} adapter for L{methanal.util.CurrencyFormatter}.
    """
    implements(IAthenaTransportable)
    jsClass = u'Methanal.Util.CurrencyFormatter'


    def __init__(self, formatter):
        self.formatter = formatter


    def getInitialArguments(self):
        f = self.formatter
        return [f.symbol, f.symbolSeparator, f.grouping, f.thousandsSeparator,
                f.decimalSeparator]

registerAdapter(CurrencyFormatterTransportable, CurrencyFormatter,
                IAthenaTransportable)



class VerifiedPasswordInput(TextInput):
    """
    Password input with verification and strength checking.

    @type minPasswordLength: C{int}
    @ivar minPasswordLength: Minimum acceptable password length, or C{None}
        to use the default client-side value

    @type strengthCriteria: C{list} of C{unicode}
    @ivar strengthCriteria: A list of criteria names for password strength
        testing, or C{None} for no additional strength criteria. See
        L{Methanal.View.VerifiedPasswordInput.STRENGTH_CRITERIA} in the
        Javascript source for possible values
    """
    fragmentName = 'methanal-verified-password-input'
    jsClass = u'Methanal.View.VerifiedPasswordInput'


    def __init__(self, minPasswordLength=None, strengthCriteria=None, **kw):
        kw.setdefault('stripWhitespace', False)
        super(VerifiedPasswordInput, self).__init__(**kw)
        self.minPasswordLength = minPasswordLength
        if strengthCriteria is None:
            strengthCriteria = []
        self.strengthCriteria = strengthCriteria


    def getArgs(self):
        return {u'minPasswordLength': self.minPasswordLength,
                u'strengthCriteria':  self.strengthCriteria}



class ChoiceInput(FormInput):
    """
    Abstract input with multiple options.

    @type values: L{IEnumeration}
    @ivar values: An enumeration to be used for choice options. C{ChoiceInput}
        will group enumeration values by their C{'group'} extra value, if one
        exists.
    """
    def __init__(self, values, **kw):
        super(ChoiceInput, self).__init__(**kw)
        _values = IEnumeration(values, None)
        if _values is None:
            _values = IEnumeration(list(values))
            warn('ChoiceInput: "values" should be adaptable to IEnumeration',
                 DeprecationWarning, 2)
        self.values = _values


    def _makeOptions(self, pattern, enums):
        """
        Create "option" elements, based on C{pattern}, from C{enums}.
        """
        for enum in enums:
            o = pattern()
            o.fillSlots('value', enum.get('id', enum.value))
            o.fillSlots('description', enum.desc)
            yield o


    @renderer
    def options(self, req, tag):
        """
        Render all available options.
        """
        optionPattern = tag.patternGenerator('option')
        groupPattern = tag.patternGenerator('optgroup')

        groups = itertools.groupby(self.values, lambda e: e.get('group'))
        for group, enums in groups:
            options = self._makeOptions(optionPattern, enums)
            if group is not None:
                g = groupPattern()
                g.fillSlots('label', group)
                yield g[options]
            else:
                yield options


    def _invokeOne(self, value):
        if value:
            item = self.values.find(id=value)
            if item is None:
                item = self.values.get(value)
                # We got tricked into fetching an enumeration item by value
                # instead of id.
                if item.get('id') is not None:
                    raise errors.InvalidEnumItem(value)
            value = item.value
        return value


    def invoke(self, data):
        """
        Set the model parameter's value from form data.
        """
        value = data[self.param.name]
        self.param.value = self._invokeOne(value)


    def _getOneValue(self, value):
        """
        Get up the enumeration item for a value or C{None} if no enumeration
        item could be found.
        """
        if value is None:
            return None
        try:
            item = self.values.get(value)
        except errors.InvalidEnumItem:
            return None
        else:
            return item.get('id', item.value)


    def getValue(self):
        """
        Get the model parameter's value.
        """
        return self._getOneValue(self.param.value)


registerAdapter(ListEnumeration, list, IEnumeration)



class MultiChoiceInputMixin(object):
    """
    A mixin for supporting multiple values in a L{ChoiceInput}.
    """
    def invoke(self, data):
        value = data[self.param.name]
        if value is None:
            value = []
        self.param.value = map(self._invokeOne, value)


    def getValue(self):
        if self.param.value is None:
            return []
        return filter(None, map(self._getOneValue, self.param.value))



# XXX: All his friends are deprecated, remove this too.
class _ObjectChoiceMixinBase(object):
    """
    Common base class for L{ObjectChoiceMixin} and L{ObjectMultiChoiceMixin}.

    @type _objects: C{dict} mapping C{int} to C{object}
    @ivar _objects: Mapping of object identities to objects.
    """
    def __init__(self, values, **kw):
        """
        Initialise the choice input.

        @type values: C{iterable} of C{(obj, unicode)}
        @param values: An iterable of C{(object, description)} pairs
        """
        self._objects = objects = {}
        objectIDs = []
        for obj, desc in values:
            value = id(obj)
            objects[value] = obj
            objectIDs.append((value, desc))
        super(_ObjectChoiceMixinBase, self).__init__(values=objectIDs, **kw)


    def invoke(self, data):
        """
        Set the model parameter's value from form data.
        """
        self.param.value = data[self.param.name]


    def getValue(self):
        """
        Get the model parameter's value.
        """
        return self.param.value


    def encodeValue(self, value):
        """
        Encode a Python object's identifier as text.

        @rtype: C{unicode}
        @return: Text representation of C{value}'s identifier, or the empty
            string if C{value} is C{None}.
        """
        if value is None:
            return u''
        return unicode(id(value))


    def decodeValue(self, encodedValue):
        """
        Decode a text identifier into a Python object.

        @return: Object represented by C{encodedValue}, or C{None} if
            C{encodeValue} is not a valid identifier.
        """
        try:
            objID = int(encodedValue)
        except (ValueError, TypeError):
            value = None
        else:
            value = self._objects.get(objID)
        return value



# XXX: All his friends are deprecated, remove this too.
class ObjectChoiceMixin(_ObjectChoiceMixinBase):
    """
    A mixin for supporting arbitrary Python objects in a L{ChoiceInput}.
    """
    def getValue(self):
        value = super(ObjectChoiceMixin, self).getValue()
        return self.encodeValue(value)


    def invoke(self, data):
        self.param.value = self.decodeValue(data[self.param.name])



# XXX: All his friends are deprecated, remove this too.
class ObjectMultiChoiceMixin(_ObjectChoiceMixinBase):
    """
    A mixin for supporting many arbitrary Python objects in a L{ChoiceInput}.
    """
    def getValue(self):
        values = super(ObjectMultiChoiceMixin, self).getValue() or []
        return map(self.encodeValue, values)


    def invoke(self, data):
        values = data[self.param.name] or []
        self.param.value = map(self.decodeValue, values)



class RadioGroupInput(ChoiceInput):
    """
    Group of radio button inputs.
    """
    fragmentName = 'methanal-radio-input'
    jsClass = u'Methanal.View.RadioGroupInput'

    def _makeOptions(self, pattern, enums):
        options = super(RadioGroupInput, self)._makeOptions(pattern, enums)
        for o in options:
            o.fillSlots('name', self.name)
            yield o



class ObjectRadioGroupInput(ObjectChoiceMixin, RadioGroupInput):
    """
    Variant of L{RadioGroupInput} for arbitrary Python objects.

    Deprecated. Use L{RadioGroupInput} with L{methanal.enums.ObjectEnum}.
    """
ObjectRadioGroupInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    ObjectRadioGroupInput.__init__)



class MultiCheckboxInput(MultiChoiceInputMixin, ChoiceInput):
    """
    Multiple-checkboxes input.
    """
    fragmentName = 'methanal-multicheck-input'
    jsClass = u'Methanal.View.MultiCheckboxInput'



class ObjectMultiCheckboxInput(ObjectMultiChoiceMixin, MultiCheckboxInput):
    """
    Variant of L{MultiCheckboxInput} for arbitrary Python objects.

    Deprecated. Use L{MultiCheckboxInput} with L{methanal.enums.ObjectEnum}.
    """
ObjectMultiCheckboxInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    ObjectMultiCheckboxInput.__init__)



class SelectInput(ChoiceInput):
    """
    Dropdown input.
    """
    fragmentName = 'methanal-select-input'
    jsClass = u'Methanal.View.SelectInput'



class ObjectSelectInput(ObjectChoiceMixin, SelectInput):
    """
    Variant of L{SelectInput} for arbitrary Python objects.

    Deprecated. Use L{SelectInput} with L{methanal.enums.ObjectEnum}.
    """
ObjectSelectInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    ObjectSelectInput.__init__)



class IntegerSelectInput(ObjectSelectInput):
    """
    Deprecated. Use L{ObjectSelectInput}.
    """
IntegerSelectInput.__init__ = deprecated(Version('methanal', 0, 2, 0))(
    IntegerSelectInput.__init__)



class MultiSelectInput(MultiChoiceInputMixin, ChoiceInput):
    """
    Multiple-selection list box input.
    """
    fragmentName = 'methanal-multiselect-input'
    jsClass = u'Methanal.View.MultiSelectInput'



class ObjectMultiSelectInput(ObjectMultiChoiceMixin, MultiSelectInput):
    """
    Variant of L{MultiSelectInput} for arbitrary Python objects.

    Deprecated. Use L{MultiSelectInput} with L{methanal.enums.ObjectEnum}.
    """
ObjectMultiSelectInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    ObjectMultiSelectInput.__init__)



class GroupedSelectInput(SelectInput):
    """
    Dropdown input with grouped values.

    Values should be structured as follows::

        (u'Group name', [(u'value', u'Description'),
                         ...]),
         ...)

    Deprecated. Use L{methanal.view.SelectInput} with L{methanal.enums.Enum}
    values with a C{'group'} extra value instead.
    """
GroupedSelectInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    GroupedSelectInput.__init__)



class ObjectGroupedSelectInput(ObjectChoiceMixin, SelectInput):
    """
    Variant of L{GroupedSelectInput} for arbitrary Python objects.

    Deprecated. Use L{SelectInput} with L{methanal.enums.ObjectEnum}.
    """
ObjectGroupedSelectInput.__init__ = deprecated(Version('methanal', 0, 2, 1))(
    ObjectGroupedSelectInput.__init__)



class CheckboxInput(FormInput):
    """
    Checkbox input.
    """
    fragmentName = 'methanal-check-input'
    jsClass = u'Methanal.View.CheckboxInput'


    def __init__(self, inlineLabel=None, **kw):
        """
        Initialise the input.

        @type inlineLabel: C{unicode}
        @param inlineLabel: Inline caption to use, or C{True} to use the model
            parameter's C{doc} attribute, or C{None} for no inline label
        """
        super(CheckboxInput, self).__init__(**kw)
        self.inlineLabel = inlineLabel


    @renderer
    def checkLabel(self, req, tag):
        """
        Render the inline caption.
        """
        if not self.inlineLabel:
            return tag

        doc = self.inlineLabel
        if doc is True:
            doc = self.param.doc
        return tag[doc]


    @renderer
    def value(self, req, tag):
        if self.param.value:
            tag(checked="checked")
        return tag



class ItemViewBase(LiveForm):
    """
    Base class for common item view behaviour.

    @type modelFactory: C{callable} with the signature
        C{item, itemClass, store, ignoredAttributes}
    @cvar modelFactory: Callable to invoke when synthensizing a L{Model}
    """
    modelFactory = ItemModel


    def __init__(self, item=None, itemClass=None, store=None,
                 ignoredAttributes=None, **kw):
        """
        Initialise the item view.

        Either L{item} or L{itemClass} must be given.

        @type item: L{Item}
        @param item: An item to synthesize a model for, and commit changes
            back to, or C{None} if there is no specific item

        @type itemClass: L{Item} type
        @param itemClass: An item type to synthesize a model for, and create
            for the first time when the view is invoked, or C{None} if a new
            item is not to be synthesized

        @type store: L{axiom.store.Store}
        @param store: The store the synthesized L{Model} is backed by; if
            C{None}, the store of L{item} is used, if given

        @type ignoredAttributes: C{set} of C{str}
        @param ignoredAttributes: A set of parameter names to ignore when
            synthesizing a model, or C{None}; useful for omitting parameters
            that are not intended for editing, such as timestamps

        @raise ValueError: If neither L{item} nor L{itemClass} is given
        """
        self.item = item

        if item is not None:
            self.itemClass = itemClass or type(item)
            self.store = store or item.store
            self.original = item
        elif itemClass is not None:
            self.itemClass = itemClass
            if store is None:
                raise ValueError('You must pass "store" with "itemClass"')
            self.store = store
            self.original = itemClass
        else:
            raise ValueError('You must pass either "item" or "itemClass"')

        self.model = self.modelFactory(item=self.item,
                                       itemClass=self.itemClass,
                                       store=self.store,
                                       ignoredAttributes=ignoredAttributes)

        super(ItemViewBase, self).__init__(store=self.store,
                                           model=self.model,
                                           **kw)



class ItemView(ItemViewBase):
    """
    A view for an L{Item} that automatically synthesizes a model.

    In the case of a specific L{Item} instance, for editing it, and in the case
    of an L{Item} subclass, for creating a new instance.
    """
    def __init__(self, switchInPlace=False, **kw):
        """
        Initialise the item view.

        @type switchInPlace: C{bool}
        @param switchInPlace: Switch to item editing mode upon creating
            a new instance
        """
        super(ItemView, self).__init__(**kw)
        self.switchInPlace = switchInPlace


    @expose
    def invoke(self, *a, **kw):
        item = super(ItemView, self).invoke(*a, **kw)
        if self.item is None and item is not None:
            self.createItem(item)
            if self.switchInPlace:
                self.item = item
            else:
                link = IWebTranslator(item.store).linkTo(item.storeID)
                return link.decode('ascii')


    def createItem(self, item):
        """
        A callback that is invoked when an item is created.
        """



class ReferenceItemView(ItemView):
    """
    An L{ItemView} associated with an attribute reference on another item.

    When the referenced item is created the view will be switched, in-place,
    to editing mode.
    """
    def __init__(self, parentItem, refAttr, itemClass=None, **kw):
        if not isinstance(refAttr, str):
            warn('refAttr should be an attribute name, not an attribute',
                 DeprecationWarning, 2)
            refAttr = refAttr.attrname

        if itemClass is None:
            itemClass = getattr(type(parentItem), refAttr).reftype

        value = getattr(parentItem, refAttr)
        super(ReferenceItemView, self).__init__(
            item=value,
            itemClass=itemClass,
            store=parentItem.store,
            switchInPlace=True,
            **kw)

        self.parentItem = parentItem
        self.refAttr = refAttr


    def createItem(self, item):
        super(ReferenceItemView, self).createItem(item)
        setattr(self.parentItem, self.refAttr, item)



class AutoItemView(ItemView):
    """
    An L{ItemView} that automatically synthesizes a form.
    """
    def __init__(self, env=None, **kw):
        """
        Initialise the view.

        Any additional keyword arguments are passed on to L{ItemView}.

        @type env: C{dict}
        @param env: Additional parameters to pass when creating inputs
        """
        super(AutoItemView, self).__init__(**kw)

        if env is None:
            env = {}

        for name, attr in self.itemClass.getSchema():
            inputTypeFromAttribute(attr, **env)(parent=self, name=name)



_inputTypes = {
    boolean:        lambda env: CheckboxInput,
    text:           lambda env: TextInput,
    integer:        lambda env: IntegerInput,
    ieee754_double: lambda env: FloatInput,
    timestamp:      lambda env:
        lambda **kw: DateInput(timezone=env['timezone'], **kw)}

def inputTypeFromAttribute(attr, **env):
    """
    Create a form input from an Axiom attribute.
    """
    return _inputTypes[type(attr)](env)



def containerFromAttributes(containerFactory, store, attributes, callback, doc,
                            **env):
    """
    Generate a model and view, with inputs, from Axiom attributes.

    Any additional keyword arguments are passed to L{inputTypeFromAttribute},
    when creating the inputs.

    @type containerFactory: C{callable} taking a L{Model} parameter
    @param containerFactory: Callable to create an input container

    @type store: L{axiom.store.Store}
    @param store: Store backing the synthesized L{Model}

    @type attributes: C{iterable} of Axiom attributes
    @param attributes: Attributes to synthesize a model and view for

    @type callback: C{callable} taking keyword arguments with names matching
        those of L{attributes}
    @param callback: Model callback

    @type doc: C{unicode}
    @param doc: Model caption

    @return: View container with child inputs for L{attributes}
    """
    attributes = tuple(attributes)

    model = Model(callback=callback,
                  params=[paramFromAttribute(store, attr, None)
                          for attr in attributes],
                  doc=doc)

    container = containerFactory(model)

    for attr in attributes:
        inputType = inputTypeFromAttribute(attr, **env)
        inputType(parent=container, name=attr.attrname)

    return container



def liveFormFromAttributes(store, attributes, callback, doc, **env):
    """
    Generate a L{LiveForm} from attributes.

    Any additional keyword arguments are passed to L{inputTypeFromAttribute},
    when creating the inputs.

    @type store: L{axiom.store.Store}
    @param store: Store backing the synthesized L{Model}

    @type attributes: C{iterable} of Axiom attributes
    @param attributes: Attributes to synthesize a model and view for

    @type callback: C{callable} taking keyword arguments with names matching
        those of L{attributes}
    @param callback: Model callback

    @type doc: C{unicode}
    @param doc: Model caption

    @return: L{LiveForm} with child inputs for L{attributes}
    """
    fact = lambda model: LiveForm(store, model)
    return containerFromAttributes(
        fact, store, attributes, callback, doc, **env)
