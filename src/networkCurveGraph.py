#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPolygon
from PyQt4.QtCore import QString
from time import sleep

"""fun to read NetWork info """
try:
    import psutil

    def getNettate ():
        net_before = psutil.net_io_counters().bytes_recv
        sleep(1)
        net_after = psutil.net_io_counters().bytes_recv
        return net_after - net_before
except ImportError:
    print "no moudle named psutil"
"""fun to read cpu info """
try:
    import psutil

    def currentCPU (time):
        return psutil.cpu_percent(time)
except ImportError:
    print "no moudle named psutil"


class NetWorkCurveGraph(QtGui.QWidget):
    def __init__ (self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.value = 0
        self.maxvalue = 2**20  # 1Mb/s
        self.frontcolor = Qt.red
        self.axiscolor = Qt.black
        self.values = []
        [self.values.append(0) for i in xrange(10)]
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.resize(400, 300)

    def updateValue (self):
        self.bytes_recv = float(getNettate())    
        self.value = self.bytes_recv / self.maxvalue * 100
        print self.bytes_recv, self.value
        for i in xrange(9):
            self.values[i] = self.values[i+1]
        self.values[-1] = float(getNettate()) / self.maxvalue  * 100
            
    def paintEvent (self, QPaintEvent):
        self.updateValue()
        self.painter = QPainter()
        self.painter.begin(self)
        self.side = min(self.width(), self.height())
        self.axesscale = self.side / 10 * 2
        self.histogramscale = self.side - self.axesscale
        self.drawAxes()
        self.drawPoints()

    def drawAxes (self):
        self.painter.save()
        self.painter.setPen(self.axiscolor)

        # draw axes line
        self.painter.drawLine(self.axesscale / 2, self.height() - self.axesscale / 2, self.axesscale / 2, 0)
        self.painter.drawLine(self.axesscale / 2, self.height() - self.axesscale / 2,
                              self.width(), self.height() - self.axesscale / 2)
        #draw y axis num
        self.yheight = self.height() - self.axesscale / 2
        step = self.yheight / 5
        for i in xrange(5):
            lineheight = self.yheight - (i * step)
            self.painter.drawLine(self.axesscale / 2, lineheight, self.axesscale / 2 + 5, lineheight)
            numstr = QString("%1 kb/s").arg(i * 250)
            self.painter.drawText(0, lineheight, numstr)
        self.painter.restore()

    def drawPoints (self):
        self.painter.save()
        self.painter.setPen(self.frontcolor)
        self.painter.setBrush(self.frontcolor)
        width = self.width() - self.axesscale / 2
        step = width / 10

        for i in xrange(0, 9):
            point1height = (100 - self.values[i]) * self.yheight /100
            point2height = (100 - self.values[i+1]) * self.yheight /100
            if(self.values[i]!=0):
                self.painter.drawLine(width - i*step, point1height,
            width - (i+1)*step, point2height)
        self.painter.restore()


def main ():
    app = QtGui.QApplication(sys.argv)
    myapp = NetWorkCurveGraph()
    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()