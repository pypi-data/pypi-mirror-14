from fusion_util.enums import Enum, EnumItem, ObjectEnum
# Unfortunately existing external code imports this from this module.
from fusion_util.errors import InvalidEnumItem
from twisted.python.versions import Version
from twisted.python.deprecate import deprecated, deprecatedModuleAttribute

from zope.interface import classImplements
from methanal.imethanal import IEnumeration



@deprecated(Version('Methanal', 0, 2, 1))
def ListEnumeration(theList):
    """
    An L{IEnumeration} adapter for the C{list} type.

    This is deprecated, use L{Enum.from_pairs} instead.
    """
    # If this isn't a grouped input, turn it into one with one unnamed group.
    if (theList and
        len(theList[0]) > 1 and
        not isinstance(theList[0][1], (tuple, list))):
        theList = [(None, theList)]

    items = []
    for groupName, values in theList:
        for value, desc in values:
            items.append(EnumItem(value, desc, group=groupName))

    return Enum('', items)



classImplements(Enum, IEnumeration)
classImplements(ObjectEnum, IEnumeration)



deprecatedModuleAttribute(
    Version('Methanal', 0, 4, 0),
    'Use fusion_util.enums.Enum instead.',
    'methanal.enums',
    'Enum')

deprecatedModuleAttribute(
    Version('Methanal', 0, 4, 0),
    'Use fusion_util.enums.ObjectEnum instead.',
    'methanal.enums',
    'ObjectEnum')

deprecatedModuleAttribute(
    Version('Methanal', 0, 4, 0),
    'Use fusion_util.enums.EnumItem instead.',
    'methanal.enums',
    'EnumItem')

deprecatedModuleAttribute(
    Version('Methanal', 0, 4, 0),
    'Use fusion_util.errors.InvalidEnumItem instead.',
    'methanal.enums',
    'InvalidEnumItem')



__all__ = ['Enum', 'ObjectEnum', 'EnumItem', 'InvalidEnumItem']
