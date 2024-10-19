import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super(SimpleBrowser, self).__init__()
        
        # Tarayıcı penceresi oluştur
        self.browser = QWebEngineView()
        
        # Tarayıcıyı localhost:5000'de aç
        self.browser.setUrl(QUrl("http://localhost:5000"))
        
        # Tarayıcı penceresini ayarla
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutunu ayarla
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    sys.exit(app.exec_())
