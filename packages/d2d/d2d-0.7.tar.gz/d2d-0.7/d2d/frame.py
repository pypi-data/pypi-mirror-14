from PySide.QtWebKit import QWebView
from PySide import QtGui, QtCore
import sys

from urllib.request import urlopen
import time
import threading
from .runserver import runserver


########################################################################
class PySideQWebView(QWebView):

    #----------------------------------------------------------------------
    def __init__(self, parent=None, settings={}):
        """"""
        super(PySideQWebView, self).__init__(parent)

        self.settings = settings
        self.wait_deploy()

        #Host
        self.load(self.settings.get("HOST"))

        #Title
        self.setWindowTitle(self.settings.get("WINDOW_TITLE"))

        #Maximized
        if self.settings.get("MAXIMIZED", False):
            self.showMaximized()

        #Size
        if "SIZE" in self.settings:
            if type(self.settings.get("SIZE")) == type(""):
                percent = float(self.settings.get("SIZE").replace("%", "")) / 100.0
                self.resize(QtGui.QDesktopWidget().screenGeometry().size()*percent)
            else:
                self.resize(*self.settings.get("SIZE"))
        else:
            self.resize(QtGui.QDesktopWidget().screenGeometry().size()/1.5)

        #Position
        if "POSITION" in self.settings:
            if self.settings.get("POSITION") == "CENTER":
                screen = QtGui.QDesktopWidget().screenGeometry()
                size =  self.geometry()
                self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
            else:
                self.move(*self.settings.get("POSITION"))


        #Icon
        self.setWindowIcon(QtGui.QIcon(self.settings.get("ICON")))


    #----------------------------------------------------------------------
    def wait_deploy(self):
        """"""
        start = time.time()
        while True or (time.time() - start) > self.settings.get("TIMEOUT"):
            try:
                urlopen(self.settings.get("HOST"))
                break
            except:
                time.sleep(1)


#----------------------------------------------------------------------
def deploy(settings):
    """"""

    threading.Thread(target=runserver, args=(settings, )).start()
    app = QtGui.QApplication(sys.argv)
    frame = PySideQWebView(settings=settings)
    frame.show()
    app.exec_()
