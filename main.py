import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from privacy_interceptor import CarlinhoPrivacyInterceptor

HTML_TELA_INICIAL = """
<body style="background-color: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
    <div style="width: 200px; height: 200px; border-radius: 50%; background: radial-gradient(circle, #ff0000 0%, #8b0000 100%); display: flex; justify-content: center; align-items: center;">
        <span style="color: white; font-size: 100px; font-family: sans-serif; font-weight: bold;">C</span>
    </div>
</body>
"""

class CarlinhoBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carlinho Browser")
        self.resize(1280, 720)
        self.setStyleSheet("""
            QMainWindow, QTabWidget, QWidget { background-color: #121212; color: #ffffff; }
            QLineEdit { background-color: #1e1e1e; border: 1px solid #333; color: white; padding: 5px; }
            QTabBar::tab { background: #1e1e1e; padding: 8px 20px; border: 1px solid #333; }
            QTabBar::tab:selected { background: #333; border-bottom: 2px solid #ff0000; }
        """)

        self.profile = QWebEngineProfile.defaultProfile()
        self.interceptor = CarlinhoPrivacyInterceptor({'ads': ['doubleclick.net', 'google-analytics.com'], 'trackers': ['facebook.net']})
        self.profile.setUrlRequestInterceptor(self.interceptor)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        
        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.tabs)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setup_shortcuts()
        self.add_new_tab()

    def add_new_tab(self):
        browser = QWebEngineView()
        browser.setHtml(HTML_TELA_INICIAL)
        i = self.tabs.addTab(browser, "Nova Aba")
        self.tabs.setCurrentIndex(i)

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"): url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1: self.tabs.removeTab(index)

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(self.add_new_tab)
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(lambda: self.tabs.currentWidget().reload())
        QShortcut(QKeySequence("F5"), self).activated.connect(lambda: self.tabs.currentWidget().reload())
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(self.url_bar.setFocus)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarlinhoBrowser()
    window.show()
    sys.exit(app.exec())
