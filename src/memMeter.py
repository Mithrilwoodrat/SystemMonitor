#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  sys
from Meter import  Meter
from PyQt4 import  QtGui, QtCore


"""fun to read Memory info """
try:
    import psutil
    def getMemorystate():
        phymem = psutil.phymem_usage()
        #used = phymem.total - (phymem.free + psutil.phymem_buffers() + psutil.cached_phymem())
        return phymem.percent
except ImportError:
    print "no moudle named psutil"
class MEMMeter(Meter):
    def __init__(self,parent=None):
        super(MEMMeter,self).__init__()
        self.logo = "Mem"
    def updateValue(self):
        self.value = getMemorystate()
def main():
    app = QtGui.QApplication(sys.argv)
    myapp = MEMMeter()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
