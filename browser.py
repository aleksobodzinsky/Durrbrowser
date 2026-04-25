# Durrbrowser - A basic browser from scratch.
# Copyright (C) 2026  AleksObodzinsky

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.




import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


class MyWebEngineView(QWebEngineView):
    def createWindow(self, windowType):
        return self


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        
        QWebEngineProfile.defaultProfile().setHttpUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
)

        
        self.browser = MyWebEngineView()

       
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        self.browser.setUrl(QUrl("https://ya.ru"))
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.showMaximized()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://ya.ru"))

    def navigate_to_url(self):
        url_text = self.urlbar.text().strip()
        if not url_text:
            return
        if not (url_text.startswith("http://") or url_text.startswith("https://")):
            if "." in url_text:
                url_text = "https://" + url_text
            else:
                url_text = "https://example.com/search?q=" + url_text
        self.browser.setUrl(QUrl(url_text))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Durrbrowser")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Durrbrowser")
    window = Browser()
    app.exec_()
