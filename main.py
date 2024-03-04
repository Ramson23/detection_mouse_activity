import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, Qt, QProcess, pyqtSignal
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QByteArray

import logging
import io


logging.basicConfig(filename='qw.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('urbanGUI')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./widgets/main.ui', self)

        self.startButton.clicked.connect(self.clicked_startButton)
        self.stopButton.clicked.connect(self.clicked_stopButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showCheckWindow)

        self.checkWindow = CheckWindow()
        self.checkWindow.modelOutChanged.connect(self.set_model_out)
        self.checkWindow.conditionChanged.connect(self.set_condition)

    def clicked_startButton(self):
        self.startButton.setEnabled(False)
        self.statusLabel.setText('Происходит предсказание...')

        self.checkWindow.show()
        self.timer.start(300000)

    def clicked_stopButton(self):
        self.checkWindow.p.write('stop'.encode("windows-1252"))

        self.timer.stop()
        self.startButton.setEnabled(True)
        self.statusLabel.setText('Ожидание запуска...')

    def showCheckWindow(self):
        self.checkWindow.show()

    def set_model_out(self, model_out):
        logger.info(f'con in main window: {model_out}')
        self.dynamicModelLabel.setText(model_out)

    def set_condition(self, condition):
        self.dynamicSelfLabel.setText(condition)


class CheckWindow(QtWidgets.QWidget):
    modelOutChanged = pyqtSignal(str)
    conditionChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./widgets/check.ui', self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.move_to_right_bottom()

        self.okButton.clicked.connect(self.clicked_okButton)

        self.p = None

    def clicked_okButton(self):
        self.hide()
        self.conditionChanged.emit(self.comboBox.currentText())

        if self.p is None:
            self.p = QProcess()
            self.p.finished.connect(self.process_finished)
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.start("./venv/Scripts/python", ['worker.py', str(self.comboBox.currentIndex()), '10'])
        else:
            self.p.write(str(f'con{self.comboBox.currentIndex()}').encode("windows-1252"))

    def process_finished(self, exitCode, exitStatus):
        print(f"Process finished. {exitCode}, {exitStatus}")

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        model_out = bytes(data).decode("utf8")
        self.modelOutChanged.emit(model_out)

    def move_to_right_bottom(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
