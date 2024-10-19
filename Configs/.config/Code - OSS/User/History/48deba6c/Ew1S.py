import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import subprocess
import os

def process_data(output_name, output_location, selected_format, bitrate):
    print(f"Output Name: {output_name}")
    print(f"Output Location: {output_location}")
    print(f"Selected Format: {selected_format}")
    print(f"Bitrate: {bitrate}")

class App(MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.pushButton.clicked.connect(self.start_recording)

    def start_recording(self):
        output_name = self.lineEdit.text()
        output_location = self.lineEdit_2.text()
        bitrate = f"{self.spinBox.value()}k"
        
        selected_format = "MKV" if self.radioButton.isChecked() else \
                          "MP4" if self.radioButton_2.isChecked() else \
                          "WEBM" if self.radioButton_3.isChecked() else \
                          "MOV" if self.radioButton_4.isChecked() else None
        
        process_data(output_name, output_location, selected_format, bitrate)

        command = f"wf-recorder -f {output_location}{output_name}.{selected_format.lower()} -t {selected_format} --bitrate {bitrate}"
        os.system(command)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
