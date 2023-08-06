"""
Public interfaces used in Methanal.
"""
from zope.interface import Interface, Attribute



class IColumn(Interface):
    """
    Represents a column that can be viewed via a query list, and provides hints
    and metadata about the column.
    """
    attributeID = Attribute(
        """
        An ASCII-encoded C{str} uniquely describing this column.
        """)


    title = Attribute(
        """
        C{unicode} text for a human-readable column title.
        """)


    def extractValue(model, item):
        """
        Extract a value for the column from an Item.

        @type model: L{methanal.widgets.Table}

        @type  item: L{axiom.item.Item}
        @param item: Item from which to extract a value

        @return: Underlying value for this column
        """


    def extractLink(model, item):
        """
        Extract a URI for the column from an Item.

        @type model: L{methanal.widgets.Table}

        @type  item: L{axiom.item.Item}
        @param item: Item from which to extract a URI

        @rtype: C{unicode}
        @return: A URI somehow relevant for this column, or C{None}
        """


    def getType():
        """
        Get a name identifying the type of data this column contains.

        @rtype: C{str}
        """



class IEnumeration(Interface):
    """
    An enumeration.
    """
    doc = Attribute("""
    A brief description of the enumeration's intent.
    """)

    def asPairs():
        """
        Represent the enumeration as a sequence of pairs.

        @rtype: C{list} of 2-C{tuple}s
        @return: A sequence of C{(value, description)}
        """


    def get(value):
        """
        Get an enumeration item for a given enumeration value.

        @raise L{methanal.errors.InvalidEnumItem}: If C{value} does not match
            any known enumeration value.

        @rtype: L{EnumItem}
        """


    def getDesc(value):
        """
        Get the description for a given enumeration value.
        """


    def getExtra(value, extraName, default=None):
        """
        Get the extra value for C{extraName} or use C{default}.
        """


    def find(**names):
        """
        Find the first L{EnumItem} with matching extra values.

        @param **names: Extra values to match

        @rtype:  L{EnumItem}
        @return: The first matching L{EnumItem} or C{None} if there are no
            matches
        """


    def findAll(**names):
        """
        Find all L{EnumItem}s with matching extra values.

        @param **names: Extra values to match

        @rtype:  C{iterable} of L{EnumItem}
        """



class ITextFormatter(Interface):
    """
    Format values as text in a human-readable way.
    """
    def format(value):
        """
        Provide a legible well-formatted representation of I{value}.

        For example: L{DecimalFormatter} performs digit grouping,
        L{CurrencyFormatter} applies a currency symbol and digit grouping.

        @rtype: C{unicode}
        """
