import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from gui import MainWindow
import subprocess
import os

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
