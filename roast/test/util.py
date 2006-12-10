from twisted.trial import unittest

import sys, os

from twisted.internet import utils

class TestFormattingMixin(object):
    def path(self, *segments):
        module = sys.modules[self.__class__.__module__]
        path = os.path.dirname(module.__file__)
        path = os.path.join(path, *segments)
        return path

    def open(self, *segments):
        path = self.path(*segments)
        return file(path)

    def slurp(self, *segments):
        f = self.open(*segments)
        data = f.read()
        f.close()
        return data

    def verify(self, got, *segments):
        path = self.mktemp()
        os.mkdir(path)
        path = os.path.join(path, 'got.html')
        f = file(path, 'w')
        f.write(got)
        f.close()

        d = utils.getProcessOutputAndValue(
            'xmldiff',
            args=[self.path(*segments), os.path.abspath(path)])

        def cb((out, err, code)):
            if out or err or code!=0:
                l = ["Files are not equal according to xmldiff."]
                for line in out.splitlines():
                    l.append("%s" % line)
                for line in err.splitlines():
                    l.append("xmldiff error: %s" % line)
                if code!=1:
                    l.append("xmldiff exited with status %d" % code)
                raise unittest.FailTest('\n'.join(l))

        d.addCallback(cb)
        return d