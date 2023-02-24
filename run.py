from contextlib import closing
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets
import socket
import subprocess
import socket
from threading import Thread

django_process = None
browser = None
port = 0

class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, root_url):
        super(WebPage, self).__init__()
        self.root_url = root_url

    def home(self):
        self.load(QtCore.QUrl(self.root_url))

    def acceptNavigationRequest(self, url, kind, is_main_frame):
        """Open external links in browser and internal links in the webview"""
        ready_url = url.toEncoded().data().decode()
        is_clicked = kind == self.NavigationTypeLinkClicked
        if is_clicked and self.root_url not in ready_url:
            QtGui.QDesktopServices.openUrl(url)
            return False
        return super(WebPage, self).acceptNavigationRequest(url, kind, is_main_frame)

class Browser(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)
        self.setStyleSheet("""
            body {
                background-color: black;
            }
            """)

    def contextMenuEvent(self, event):
        return  # Disable the Context Menu

def navigate_back(self):
    browser.page().triggerAction(QtWebEngineWidgets.QWebEnginePage.Back)

def navigate_forward(self):
    browser.page().triggerAction(QtWebEngineWidgets.QWebEnginePage.Forward)

def launch_browser():
    global browser
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.showMaximized()
    window.setWindowTitle('SpiritSoft')
    # window.setWindowIcon(QtGui.QIcon(icon))
    widget = QtWidgets.QWidget()
    window.setCentralWidget(widget)
    layout = QtWidgets.QGridLayout(widget)
    back_btn = QtWidgets.QPushButton("Back")
    back_btn.clicked.connect(navigate_back)
    layout.addWidget(back_btn, 0, 0)
    forward_btn = QtWidgets.QPushButton("Forward")
    forward_btn.clicked.connect(navigate_forward)
    layout.addWidget(forward_btn, 0, 1)
    browser = Browser(window)
    layout.addWidget(browser, 1, 0, 1, 2)
    page = WebPage(f'http://spiritsoft.localhost:{port}/admin/')
    page.home()
    browser.setPage(page)

    window.show()
    app.exec_()

def launch_app():
    global django_process
    django_process = subprocess.Popen(["python", "manage.py", "runserver", str(port)])
    
def main():
    global port
    port = find_free_port()
    app_thread = Thread(target=launch_app)
    app_thread.start()
    launch_browser()
    django_process.terminate()
    
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

if __name__ == '__main__':
    main()
