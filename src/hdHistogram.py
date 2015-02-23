#!/usr/bin/python
# -*- coding: utf-8 -*-

import  sys
from PyQt4 import  QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPolygon
from PyQt4.QtCore import QString

"""fun to read harddrive info """
try:
    import psutil
    def getHdstate():
        return psutil.disk_usage("/").percent
except ImportError:
    print "no moudle named psutil"


class HdHistogram(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.value = 0
        self.frontcolor = Qt.blue
        self.axiscolor = Qt.black
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.values = []
        [self.values.append(getHdstate()) for i in xrange(10)]
        self.resize(400,300)
        
    def updateValue(self):
        self.value = getHdstate()
        for i in xrange(9):
            self.values[i] = self.values[i+1]
        self.values[-1] = getHdstate()
        for i in xrange(10):
            print(self.values[i])
            
    def paintEvent(self, QPaintEvent):
        self.updateValue()
        self.painter = QPainter()
        self.painter.begin(self)
        self.side = min(self.width(), self.height())
        self.axesscale = self.side/10 *2
        self.histogramscale = self.side -self.axesscale
        self.drawAxes()
        self.drawRect()

    def drawAxes(self):
        self.painter.save()
        self.painter.setPen(self.axiscolor)

        #draw axes line
        self.painter.drawLine(self.axesscale/2, self.height() - self.axesscale/2, self.axesscale/2, 0)
        self.painter.drawLine(self.axesscale/2, self.height() - self.axesscale/2,
                              self.width(), self.height() - self.axesscale/2)
        #draw y axis num
        self.yheight = self.height()-self.axesscale/2
        step = self.yheight / 11
        for i in xrange(11):
            lineheight = self.yheight - (i * step)
            self.painter.drawLine(self.axesscale/2 , lineheight, self.axesscale/2 + 5, lineheight)
            numstr = QString( "%1%" ).arg(i*10)
            self.painter.drawText(0, lineheight, numstr)
        self.painter.restore()
    def drawRect(self):
        self.painter.save()
        self.painter.setPen(self.frontcolor)
        self.painter.setBrush(self.frontcolor)
        width = self.width() - self.axesscale/2
        step = width / 10

        for i in xrange(0,10):
            rectheight = (self.values[i] / 100)*self.yheight
            self.painter.drawRect(width- step * i, self.yheight-rectheight,
                              step, rectheight)
        self.painter.restore()


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = HdHistogram()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
