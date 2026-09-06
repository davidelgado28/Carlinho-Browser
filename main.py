import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit,
    QTabWidget, QProgressBar, QWidget, QVBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView

class NavegadorCarlinho(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador Carlinho v2 (Python Edition)")
        self.setGeometry(100, 100, 1280, 800)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.fechar_aba)
        self.tabs.currentChanged.connect(self.aba_alterada)
        self.setCentralWidget(self.tabs)
        self.barra_navegacao = QToolBar("Navegação")
        self.addToolBar(self.barra_navegacao)
        self.btn_voltar = QAction("◄", self)
        self.btn_voltar.setStatusTip("Voltar página")
        self.btn_voltar.triggered.connect(lambda: self.aba_atual().back())
        self.barra_navegacao.addAction(self.btn_voltar)
        self.btn_avancar = QAction("►", self)
        self.btn_avancar.setStatusTip("Avançar página")
        self.btn_avancar.triggered.connect(lambda: self.aba_atual().forward())
        self.barra_navegacao.addAction(self.btn_avancar)
        self.btn_recarregar = QAction("↻", self)
        self.btn_recarregar.setStatusTip("Recarregar página")
        self.btn_recarregar.triggered.connect(lambda: self.aba_atual().reload())
        self.barra_navegacao.addAction(self.btn_recarregar)
        self.btn_home = QAction("🏠", self)
        self.btn_home.setStatusTip("Ir para Início")
        self.btn_home.triggered.connect(self.ir_para_home)
        self.barra_navegacao.addAction(self.btn_home)
        self.btn_nova_aba = QAction("+", self)
        self.btn_nova_aba.setStatusTip("Nova Aba")
        self.btn_nova_aba.triggered.connect(lambda: self.adicionar_nova_aba())
        self.barra_navegacao.addAction(self.btn_nova_aba)
        self.barra_url = QLineEdit()
        self.barra_url.setPlaceholderText("Digite uma URL ou pesquise no Google...")
        self.barra_url.returnPressed.connect(self.navegar_para_url)
        self.barra_navegacao.addWidget(self.barra_url)
        self.progresso = QProgressBar()
        self.progresso.setMaximumWidth(120)
        self.progresso.setFixedHeight(14)
        self.barra_navegacao.addWidget(self.progresso)
        self.aplicar_estilo_dark()
        self.adicionar_nova_aba(QUrl("https://www.google.com"), "Nova Aba")

    def aplicar_estilo_dark(self):
        estilo = """
            QMainWindow { background-color: #1e1e2e; }
            QToolBar { background-color: #2b2b3b; border: none; padding: 5px; spacing: 8px; }
            QLineEdit { 
                background-color: #181825; color: #cdd6f4; border: 1px solid #45475a; 
                border-radius: 8px; padding: 6px 12px; font-size: 13px; 
            }
            QLineEdit:focus { border: 1px solid #89b4fa; }
            QTabWidget::pane { border: none; }
            QTabBar::tab { 
                background-color: #181825; color: #a6adc8; padding: 8px 16px; 
                border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px;
            }
            QTabBar::tab:selected { background-color: #313244; color: #cdd6f4; font-weight: bold; }
            QProgressBar { border: none; border-radius: 4px; text-align: center; background-color: #313244; }
            QProgressBar::chunk { background-color: #89b4fa; border-radius: 4px; }
        """
        self.setStyleSheet(estilo)

    def aba_atual(self):
        return self.tabs.currentWidget()

    def adicionar_nova_aba(self, qurl=None, label="Nova Aba"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda url, b=browser: self.atualizar_url(url, b))
        browser.loadProgress.connect(lambda p, b=browser: self.atualizar_progresso(p, b))
        browser.titleChanged.connect(lambda title, b=browser: self.atualizar_titulo(title, b))

    def fechar_aba(self, index):
        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(index)

    def aba_alterada(self, index):
        if index != -1:
            browser_atual = self.tabs.widget(index)
            if browser_atual:
                self.barra_url.setText(browser_atual.url().toString())

    def navegar_para_url(self):
        texto = self.barra_url.text().strip()
        if not texto:
            return

        if "." in texto and " " not in texto:
            if not (texto.startswith("http://") or texto.startswith("https://")):
                texto = "https://" + texto
            url = QUrl(texto)
        else:
            url = QUrl(f"https://www.google.com/search?q={texto}")

        self.aba_atual().setUrl(url)

    def ir_para_home(self):
        self.aba_atual().setUrl(QUrl("https://www.google.com"))

    def atualizar_url(self, qurl, browser):
        if browser == self.aba_atual():
            self.barra_url.setText(qurl.toString())

    def atualizar_progresso(self, progresso, browser):
        if browser == self.aba_atual():
            self.progresso.setValue(progresso)

    def atualizar_titulo(self, titulo, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            titulo_curto = (titulo[:15] + "...") if len(titulo) > 15 else titulo
            self.tabs.setTabText(index, titulo_curto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = NavegadorCarlinho()
    janela.show()
    sys.exit(app.exec())
