from zope.interface import implements

from twisted.python import log
from twisted.python.failure import Failure

from methanal.imethanal import ITextFormatter



class MethodWrapper(object):
    """
    Wrapper around a class method.

    @type unboundMethod: C{callable}
    @ivar unboundMethod: Unbound method

    @type cls: C{type}
    @ivar cls: Type that L{unboundMethod} is a method of

    @type instance: C{instance}
    @ivar instance: Instance to invoke L{unboundMethod} with
    """
    def __init__(self, unboundMethod, cls, instance):
        self.unboundMethod = unboundMethod
        self.cls = cls
        self.instance = instance


    def __call__(self, *a, **kw):
        return self.unboundMethod(self.instance, *a, **kw)



def collectMethods(inst, methodName):
    """
    Traverse an object's MRO, collecting methods.

    Collected methods are wrapped with L{MethodWrapper}.

    @type inst: C{type}
    @param inst: Type instance whose L{methodName} methods should be collected

    @type methodName: C{str}
    @param methodName: Name of the method, along the MRO, to collect

    @rtype: C{iterable} of L{MethodWrapper} instances
    @return: Wrapped methods named L{methodName} along L{inst}'s MRO
    """
    for cls in type(inst).__mro__:
        try:
            method = cls.__dict__[methodName]
        except KeyError:
            pass
        else:
            yield MethodWrapper(method, cls, inst)



def getArgsDict(inst):
    """
    Collect arguments along a class hierarchy.

    Arguments are collected by traversing the MRO in reverse order, looking
    for C{getArgs} methods, which should return a single C{dict} mapping
    C{unicode} keys to values.

    @type inst: C{type}
    @param inst: Type instance whose C{getArgs} results should be collected

    @raise ValueError: If a key is specified more than once
    @raise TypeError: If a key is not a C{unicode} instance

    @rtype: C{dict}
    @return: A dictionary combining the results of all C{getArgs} methods
        in C{inst}'s class hierarchy
    """
    args = {}
    for getter in collectMethods(inst, 'getArgs'):
        for key, value in getter().iteritems():
            if key in args:
                raise ValueError(
                    'Argument %r from %r already specified' % (key, getter.cls))
            if not isinstance(key, unicode):
                raise TypeError(
                    'Argument name %r is not unicode' % (key,))
            args[key] = value
    return args



class Porthole(object):
    """
    Observable event source.

    A porthole is the link between event emitters, and event observers. Any
    event (which are arbitrary objects) emitted will be broadcast to all
    observers registered with the porthole at that point in time.

    @type observers: C{list} of C{callable}
    """
    def __init__(self):
        self.observers = []


    def addObserver(self, observer):
        """
        Add a observer.

        This is a callable that will be invoked when a response is received for
        a finance application submission.

        @type observer: C{callable} taking one parameter
        @param observer: A callable, that participates in event broadcasting,
            taking one argument: C{event}

        @rtype: C{callable} taking no parameters
        @return: A callable that will remove L{observer} from the Porthole's
            observers
        """
        self.observers.append(observer)
        return lambda: self.observers.remove(observer)


    def emitEvent(self, event):
        """
        Emit an event to all attached observers.

        @param event: Object, representing event information, to pass to all
            attached observers
        """
        if isinstance(event, Failure):
            log.err(event)

        # Copy the list so that observers mutating the list won't wreak havoc.
        for observer in list(self.observers):
            observer(event)



def propertyMaker(func):
    """
    Create a property from C{func}'s return values.

    @type func: C{callable} returning an iterable
    @param func: Callable whose return values are passed on as positional
        arguments to C{property}

    @rtype: C{property} instance
    """
    return property(*func())



class DecimalFormatter(object):
    """
    Format values as decimal values.

    @type grouping: C{list} of C{int}
    @ivar grouping: Digit group sizes from right to left. Use C{0} to indicate
        that the previous group size should be used for the rest of the digit
        groups; use C{-1} to indicate that no more grouping should occur.
        Defaults to C{[3, 0]}.

    @type thousandsSeparator: C{unicode}
    @ivar thousandsSeparator: Separator between digit groups. Defaults to
        C{','}.

    @type decimalSeparator: C{unicode}
    @ivar decimalSeparator: Decimal separator. Defaults to C{'.'}.
    """
    implements(ITextFormatter)


    def __init__(self, grouping=[3, 0], thousandsSeparator=u',',
                 decimalSeparator=u'.'):
        self.grouping = grouping
        self.thousandsSeparator = thousandsSeparator
        self.decimalSeparator = decimalSeparator


    def groupings(self):
        """
        Generator of interpreted grouping values.
        """
        lastCount = 0
        for count in self.grouping:
            if count == 0:
                while True:
                    yield lastCount
            elif count == -1:
                return
            else:
                yield count
            lastCount = count


    def format(self, value):
        """
        Format C{value} as a decimal value, grouping digits if required.

        @rtype: C{unicode}
        """
        if not value:
            return u''

        parts = unicode(value).rsplit(self.decimalSeparator, 1)
        value = list(parts[0])
        i = len(value)
        for grouping in self.groupings():
            i -= grouping
            if i < 1:
                break
            value.insert(i, self.thousandsSeparator)

        parts[0] = u''.join(value)
        return self.decimalSeparator.join(parts)



class CurrencyFormatter(DecimalFormatter):
    """
    Format values as currency values.

    @type symbol: C{unicode}
    @ivar symbol: Currency symbol.

    @type symbolSeparator: C{unicode}
    @ivar symbolSeparator: Separator between then currency symbol and decimal
        value, defaults to C{' '}.
    """
    implements(ITextFormatter)


    def __init__(self, symbol, symbolSeparator=u' ', **kw):
        super(CurrencyFormatter, self).__init__(**kw)
        self.symbol = symbol
        self.symbolSeparator = symbolSeparator


    def format(self, value):
        """
        Format C{value} as a currency, prefixing the grouped decimal value with
        the currency symbol and separator.

        @rtype: C{unicode}
        """
        value = super(CurrencyFormatter, self).format(value)
        return self.symbol + self.symbolSeparator + value
