from fusion_util.errors import InvalidEnumItem
from twisted.python.deprecate import deprecatedModuleAttribute
from twisted.python.versions import Version



class ConstraintError(ValueError):
    """
    One or more constraints specified in the data model were unmet.
    """



class InvalidIdentifier(ValueError):
    """
    An invalid identifier was specified.
    """



deprecatedModuleAttribute(
    Version('Methanal', 0, 4, 0),
    'Use fusion_util.errors.InvalidEnumItem instead.',
    'methanal.errors',
    'InvalidEnumItem')



__all__ = ['InvalidEnumItem', 'ConstraintError', 'InvalidIdentifier']
