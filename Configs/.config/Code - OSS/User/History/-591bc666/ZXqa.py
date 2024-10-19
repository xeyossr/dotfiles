import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super(SimpleBrowser, self).__init__()
        
        # Tarayıcı ayarları
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1280, 720)  # Pencere boyutu

        # WebEngineView oluştur
        self.browser = QWebEngineView()
        
        # localhost:5000'ı aç
        self.browser.setUrl("http://localhost:5000")

        # Ana widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())
