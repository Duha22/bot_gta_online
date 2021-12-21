import os, pyautogui, easyocr, PyQt5.QtWidgets, torch, sys, smtplib, traceback, datetime
from keyboard import add_hotkey, wait
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyQt5.QtCore import QThread, pyqtSignal
from ahk import AHK
from design import Ui_MainWindow

class Main_GUI(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.main)
        self.show()
        self.flag = 0

    def main(self):
        self.function = ""
        if self.ui.radioButton.isChecked():
            self.function = "inside_track"
            self.key = ''
        elif self.ui.radioButton_2.isChecked():
            self.function = "anti_afk"
            self.key = self.ui.comboBox.currentText()

        if self.flag == 0:
            self.ui.pushButton.setText('STOP')
            self.main = Main(function=self.function, key=self.key)
            self.thread = Tread(self.main)
            self.thread.stop_main_tread.connect(self.stop_main_thread)
            self.thread.start()
            self.main.start()
            self.flag = 1
        elif self.flag == 1:
            self.ui.pushButton.setText('START')
            self.main.terminate()
            self.flag = 0

    def stop_main_thread(self):
        self.ui.pushButton.setText('START')
        self.flag = 0

class Tread(QThread):
    stop_main_tread = pyqtSignal(bool)
    def __init__(self, thread):
        QThread.__init__(self)
        self.thread = thread

    def run(self):
        add_hotkey("Ctrl + S", self.test)

    def test(self):
        if self.thread.isRunning():
            self.thread.terminate()
            self.stop_main_tread.emit(0)

class Main(QThread):
    X, Y = pyautogui.size()
    ex_email = pyqtSignal(str)
    MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, function, key=''):
        QThread.__init__(self)
        self.function = function
        self.key = key
        self.stop = "__init__"
        torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.ahk = AHK()

    def run(self):
        # x = round(self.X / 8)
        # y = round(self.Y / 5)
        QThread.msleep(10000)
        # self.ahk.mouse_move(x, y)
        # if self.ahk.pixel_get_color(x, y) == "0x000000":
        #     print(1)
        # exit(0)
        if self.function == "inside_track":
            self.inside_track()
        elif self.function == "anti_afk":
            self.anti_afk()

    def anti_afk(self):
        active_window = pyautogui.getActiveWindowTitle()
        while active_window != "Grand Theft Auto V":
            QThread.msleep(1000)
            active_window = pyautogui.getActiveWindowTitle()
            continue
        self.ahk.key_press(self.key, release=False)

    def inside_track(self):
        path = os.getcwd()
        if path.split("\\")[-1] != "png":
            os.chdir('png')
        while pyautogui.getActiveWindowTitle() != "Grand Theft Auto V":
            QThread.msleep(1000)
            continue
        while True:
            try:
                if self.stop == "stop":
                    break
                flag_11 = 0
                click_check = self.ahk.pixel_get_color(10, 30)
                mb_x, mb_y = pyautogui.locateCenterOnScreen("main_bet.png")
                self.ahk.click(mb_x, mb_y)
                while self.ahk.pixel_get_color(10,30) == click_check:
                    QThread.msleep(300)
                    self.ahk.click()
                QThread.msleep(1000)
                list_of_coefficients = {}
                y_coefficient = 340
                reader = easyocr.Reader(['en'])
                for val_coef in range(0, 6):
                    pyautogui.screenshot(imageFilename=f"{val_coef}_hourse.png",
                                         region=(173, y_coefficient, 70, 50))
                    hourse_coefficient = int(reader.readtext(f"{val_coef}_hourse.png",
                                                             detail=0)[0].replace('/', ''))
                    if hourse_coefficient in list_of_coefficients.values() and hourse_coefficient== 11:
                        flag_11 = 1
                    list_of_coefficients[f'{val_coef}_hourse.png'] = hourse_coefficient
                    y_coefficient += 121
                tuple_coef = sorted(list_of_coefficients.items(), key=lambda x: x[1])
                list_of_coefficients = dict(tuple_coef)
                first_hourse = list(list_of_coefficients.keys())[0]
                click_check = self.ahk.pixel_get_color(1160, 280)
                fh_x, fh_y = pyautogui.locateCenterOnScreen(first_hourse)
                self.ahk.click(fh_x, fh_y)
                while self.ahk.pixel_get_color(1160, 280) == click_check:
                    self.ahk.click()
                    QThread.msleep(300)
                QThread.msleep(500)
                if flag_11 != 1:
                    self.ahk.key_press('tab')
                    QThread.msleep(300)
                bbr_x, bbr_y =pyautogui.locateCenterOnScreen('place_bet_befor_run.png')
                self.ahk.click(bbr_x, bbr_y)
                click_check = self.ahk.pixel_get_color(1160, 280)
                while self.ahk.pixel_get_color(1160, 280) == click_check:
                    self.ahk.click()
                    QThread.msleep(300)
                while pyautogui.locateCenterOnScreen('put_it_again.png') == None:
                    QThread.msleep(1000)
                else:
                    click_check = self.ahk.pixel_get_color(10, 30)
                    pa_x, pa_y = pyautogui.locateCenterOnScreen('put_it_again.png')
                    self.ahk.click(pa_x, pa_y)
                    QThread.msleep(500)
                    while self.ahk.pixel_get_color(10, 30) == click_check:
                        self.ahk.click()
                        QThread.msleep(300)
            except Exception as _ex:
                x = round(self.X/8)
                y = round(self.Y/5)
                if self.ahk.pixel_get_color(x, y) == "0x000000":
                    self.ahk.key_press('enter')
                    if pyautogui.locateCenterOnScreen("error_check.png", confidence=0.1):
                        self.ahk.click(self.X/2, self.Y/2)
                    continue
                QThread.msleep(2000)
                if pyautogui.getActiveWindowTitle() == "Grand Theft Auto V":
                    sender = "bitprog.official@gmail.com"
                    password = "ixr-hMm-Xtg-mb8"
                    message_text = str(traceback.format_exc())
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    pyautogui.screenshot(imageFilename="error.png")
                    try:
                        server.login(sender, password)
                        part = MIMEApplication(open("error.png", 'rb').read())
                        msg = MIMEMultipart()
                        part.add_header('Content-Disposition', 'attachment', filename='error.png')
                        msg.attach(part)
                        msg.attach(MIMEText(message_text))
                        server.sendmail(sender, "danilovandrey22@gmail.com", msg.as_string())
                    except Exception as _ex_email:
                        exit(0)
                    break
                else:
                    break

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])
    application = Main_GUI()
    application.show()
    sys.exit(app.exec())