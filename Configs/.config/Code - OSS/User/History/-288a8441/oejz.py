# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
from datetime import datetime
import os
import subprocess

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"wf-recorder GUI")
        MainWindow.resize(798, 377)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(110, 10, 251, 31))

        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        self.lineEdit.setPalette(palette)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(651, 10, 121, 31))
        self.spinBox.setMinimum(500)
        self.spinBox.setMaximum(30000)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(600, 15, 51, 21))

        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(100, 109, 61, 20))
        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(170, 109, 61, 20))
        self.radioButton_3 = QRadioButton(self.centralwidget)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(240, 109, 71, 20))
        self.radioButton_4 = QRadioButton(self.centralwidget)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(320, 109, 71, 20))

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 17, 91, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 110, 51, 16))

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(110, 44, 251, 31))

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(370, 44, 111, 31))
        self.pushButton_3.setText("Browse")
        self.pushButton_3.clicked.connect(self.browse_folder)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 51, 101, 16))

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 320, 111, 31))

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(150, 320, 111, 31))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.lineEdit_2.setText(folder)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"wf-recorder GUI", None))
        current_time = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
        home = os.path.expanduser("~")
        self.lineEdit.setText(current_time)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Bitrate:", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"MKV", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"MP4", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"WEBM", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"MOV", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Output Name:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", home, None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Output location:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

class App(MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.pushButton.clicked.connect(self.start_recording)
        self.pushButton_2.clicked.connect(self.stop_recording)
        self.recording_process = None  # Process reference

    def start_recording(self):
        output_name = self.lineEdit.text().strip()
        output_location = self.lineEdit_2.text().strip()
        bitrate = f"{self.spinBox.value()}k"

        selected_format = "MKV" if self.radioButton.isChecked() else \
                          "MP4" if self.radioButton_2.isChecked() else \
                          "WEBM" if self.radioButton_3.isChecked() else \
                          "MOV" if self.radioButton_4.isChecked() else None

        # Hata Kontrolü
        if not output_name or not output_location or selected_format is None:
            QMessageBox.warning(self, "Warning", "Please fill all fields.")
            return

        # Aynı isimde bir dosya varsa uyarı göster
        output_file = f"{output_location}/{output_name}.{selected_format.lower()}"
        if os.path.exists(output_file):
            reply = QMessageBox.question(self, 'File Exists',
                                         f"The file '{output_file}' already exists. Do you want to overwrite it?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                return
            else:
                try:
                    os.remove(output_file)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete the existing file: {str(e)}")
                    return

        process_data(output_name, output_location, selected_format, bitrate)

        # Bildirim
        QMessageBox.information(self, "Recording", "Recording has started.")

        command = f"wf-recorder -f {output_location}/{output_name}.{selected_format.lower()} -t {selected_format} --bitrate {bitrate}"
        self.recording_process = subprocess.Popen(command, shell=True)

    def stop_recording(self):
        if self.recording_process:
            self.recording_process.terminate()
            self.recording_process = None
            QMessageBox.information(self, "Recording", "Recording has stopped.")

def process_data(output_name, output_location, selected_format, bitrate):
    print(f"Output Name: {output_name}")
    print(f"Output Location: {output_location}")
    print(f"Selected Format: {selected_format}")
    print(f"Bitrate: {bitrate}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
