from contextlib import closing
import ctypes
import psutil
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets, QtPrintSupport
import socket
import subprocess
import socket
from threading import Thread

django_process = None
browser = None
port = 0
icon = "favicon.png"

class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, root_url):
        super(WebPage, self).__init__()
        self.root_url = root_url

    def goto(self, url):
        self.load(QtCore.QUrl(url))

    def acceptNavigationRequest(self, url, mode, is_main_frame):
        """Open external links in browser and internal links in the webview"""
        new_url = url.toEncoded().data().decode()
        is_clicked = mode == self.NavigationTypeLinkClicked
        if is_clicked and (not new_url.startswith(self.root_url) or new_url.endswith("?ext")):
            QtGui.QDesktopServices.openUrl(url)
            return False
        return super(WebPage, self).acceptNavigationRequest(url, mode, is_main_frame)


class Browser(QtWebEngineWidgets.QWebEngineView):
    _windows = set()

    # https://stackoverflow.com/questions/71319768/how-to-use-qtwebengine-createwindow-in-pyqt5
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)
        self.page().windowCloseRequested.connect(self.handleWindowCloseRequested)
        self.page().printRequested.connect(self.handlePrint)

    def contextMenuEvent(self, event):
        return  # Disable the Context Menu

    def handleWindowCloseRequested(self):
        self._removeWindow(self)

    def handlePrint(self):
        print("bruh")
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.page().document().print_(dialog.printer())

    @classmethod
    def _removeWindow(cls, window):
        cls._windows.discard(window)

    @classmethod
    def new_window(cls):
        window = cls()
        cls._windows.add(window)
        return window

    def createWindow(self, mode):
        window = self.new_window()
        window.resize(600, 500)
        window.setWindowTitle('SpiritSoft')
        window.setWindowIcon(QtGui.QIcon(icon))
        window.show()
        return window


def launch_browser():
    global browser
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.showMaximized()
    window.setWindowTitle('SpiritSoft')
    window.setWindowIcon(QtGui.QIcon(icon))
    widget = QtWidgets.QWidget()
    browser = Browser(window)
    window.setCentralWidget(browser)
    page = WebPage(f'http://spiritsoft.localhost:{port}')
    page.goto(f'http://spiritsoft.localhost:{port}/iframe/')
    browser.setPage(page)

    window.show()
    app.exec_()


def launch_app():
    global django_process
    django_process = subprocess.Popen(f"python manage.py runserver {port} --noreload >NUL 2>NUL", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def main():
    # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('spiritsoft.desktop.entry')
    global port
    port = find_free_port()
    app_thread = Thread(target=launch_app)
    app_thread.start()
    launch_browser()
    # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    for p in psutil.Process(django_process.pid).children(recursive=True): 
       p.kill()
    psutil.Process(django_process.pid).kill()


if __name__ == '__main__':
    main()
