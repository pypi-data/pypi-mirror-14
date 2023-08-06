from twisted.python import filepath
from nevow import athena

import methanal

js = filepath.FilePath(methanal.__file__).parent().child('js')
package = athena.AutoJSPackage(js.path)
