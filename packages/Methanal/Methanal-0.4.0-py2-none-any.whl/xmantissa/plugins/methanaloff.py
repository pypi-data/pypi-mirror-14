from twisted.python.filepath import FilePath

from xmantissa.offering import Offering

import methanal
from methanal.theme import Theme
from methanal.publicpage import MethanalPublicPage

plugin = Offering(
    name=u'Methanal',
    description=u'A forms library for Mantissa',
    siteRequirements=[],
    appPowerups=[MethanalPublicPage],
    installablePowerups=[],
    loginInterfaces=[],
    themes=[Theme('methanal-base', 0)],
    staticContentPath=FilePath(methanal.__file__).sibling('static'))
