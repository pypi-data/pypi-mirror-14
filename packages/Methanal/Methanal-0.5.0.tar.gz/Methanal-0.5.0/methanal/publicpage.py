from zope.interface import implements

from twisted.python.filepath import FilePath

from axiom.item import Item
from axiom.attributes import integer

from nevow.tags import h1
from nevow.static import File

from xmantissa.ixmantissa import IPublicPage, ICustomizable, IStaticShellContent
from xmantissa.publicresource import PublicPage

import methanal



class MethanalPublicPage(Item):
    implements(IPublicPage)

    typeName = 'methanal_public_page'
    schemaVersion = 1
    powerupInterfaces = (IPublicPage,)

    dummy = integer()


    def getResource(self):
        return PublicIndexPage(self, IStaticShellContent(self.store, None))



class PublicIndexPage(PublicPage):
    implements(ICustomizable)
    title = 'Methanal'


    def __init__(self, original, staticContent, forUser=None):
        super(PublicIndexPage, self).__init__(
            original, original.store.parent, h1['Methanal'], staticContent,
            forUser)


    def child_static(self, ctx):
        s = FilePath(methanal.__file__).sibling('static')
        return File(s.path)


    def customizeFor(self, forUser):
        return type(self)(self.original, self.staticContent, forUser)
