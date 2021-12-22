import os, pyautogui, easyocr, PyQt5.QtWidgets, sys, smtplib, traceback, datetime
from keyboard import add_hotkey
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
        self.ahk = AHK()

    def run(self):
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

    def black_win(self):
        QThread.msleep(2000)
        if pyautogui.locateCenterOnScreen("internet_error.png", confidence=0.4) != None:
            while pyautogui.locateCenterOnScreen("internet_error.png", confidence=0.4) != None:
                self.ahk.key_press('enter')
            QThread.msleep(200)
            self.email_send("ConnectError")
            if pyautogui.locateCenterOnScreen("error_check.png", confidence=0.4) != None:
                while pyautogui.locateCenterOnScreen("error_check.png", confidence=0.4) != None:
                    self.ahk.click(self.X / 2, self.Y / 2)
                    QThread.msleep(1000)
                return True
            elif pyautogui.locateCenterOnScreen("put_it_again.png") != None:
                x, y = pyautogui.locateCenterOnScreen("put_it_again.png")
                self.ahk.click(x, y)
                color_check1 = self.ahk.pixel_get_color(round(self.X / 8), round(self.Y / 6))
                color_chech2 = self.ahk.pixel_get_color(self.X - round(self.X / 8), self.Y - round(self.Y / 6))
                while self.ahk.pixel_get_color(round(self.X / 8), round(self.Y / 6)) == color_check1 and \
                        self.ahk.pixel_get_color(self.X - round(self.X / 8),
                                                 self.Y - round(self.Y / 6)) == color_chech2:
                    self.ahk.click(x, y)
                    QThread.msleep(1000)
                return True
        elif pyautogui.getActiveWindowTitle() == "Grand Theft Auto V" and pyautogui.locateCenterOnScreen("internet_error.png", confidence=0.4) == None:
            self.email_send(error_valuem='OtherERROR')
            return False
        else:
            return False

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
                    QThread.msleep(200)
                bbr_x, bbr_y =pyautogui.locateCenterOnScreen('place_bet_befor_run.png')
                click_check_1 = self.ahk.pixel_get_color(1160, 280)
                self.ahk.click(bbr_x, bbr_y)
                while self.ahk.pixel_get_color(1160, 280) == click_check_1:
                    self.ahk.click()
                    QThread.msleep(300)
                if pyautogui.locateCenterOnScreen('put_it_again.png') == None:
                    black_1 = self.ahk.pixel_get_color(round(self.X / 8), round(self.Y / 6))
                    black_2 = self.ahk.pixel_get_color(self.X - round(self.X / 8), self.Y - round(self.Y / 6))
                    if black_1 == "0x000000" and black_2 == "0x000000":
                        con = self.black_win()
                        if con == True:
                            continue
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
                QThread.msleep(1000)
                con = self.black_win()
                if con == True: continue
                elif con == False: break
                # if pyautogui.locateCenterOnScreen("internet_error.png", confidence=0.4) != None:
                #     while pyautogui.locateCenterOnScreen("internet_error.png", confidence=0.4) != None:
                #         self.ahk.key_press('enter')
                #     QThread.msleep(200)
                #     self.email_send("ConnectError")
                #     if pyautogui.locateCenterOnScreen("error_check.png", confidence=0.4) != None:
                #         while pyautogui.locateCenterOnScreen("error_check.png", confidence=0.4) != None:
                #             self.ahk.click(self.X/2, self.Y/2)
                #             QThread.msleep(1000)
                #         continue
                #     elif pyautogui.locateCenterOnScreen("put_it_again.png") != None:
                #         x, y = pyautogui.locateCenterOnScreen("put_it_again.png")
                #         self.ahk.click(x, y)
                #         color_check1 = self.ahk.pixel_get_color(round(self.X / 8), round(self.Y / 6))
                #         color_chech2 = self.ahk.pixel_get_color(self.X - round(self.X / 8), self.Y - round(self.Y / 6))
                #         while self.ahk.pixel_get_color(round(self.X / 8), round(self.Y / 6)) == color_check1 and \
                #                 self.ahk.pixel_get_color(self.X - round(self.X / 8), self.Y - round(self.Y / 6)) == color_chech2:
                #             self.ahk.click(x, y)
                #             QThread.msleep(1000)
                #         continue
                # if pyautogui.getActiveWindowTitle() == "Grand Theft Auto V":
                #     self.email_send(error_valuem='OtherERROR')
                #     break
                # else:
                #     break

    def email_send(self, error_valuem):
        try:
            error_valuem = error_valuem
            sender = "bitprog.official@gmail.com"
            password = "ixr-hMm-Xtg-mb8"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            pyautogui.screenshot(imageFilename="error.png")
            server.login(sender, password)
            msg = MIMEMultipart()
            part = MIMEApplication(open("error.png", 'rb').read())
            # if error_valuem == "ConnectError":
            #     self.message_text = "The RockStarGames error has been overcome"
            #     part.add_header('Content-Disposition', 'attachment', filename='cheak_screnshot.png')
            #     msg.attach(part)
            # elif error_valuem == 'OtherERROR':
            self.message_text =  str(traceback.format_exc())
            part.add_header('Content-Disposition', 'attachment', filename='error.png')
            msg.attach(part)
            msg.attach(MIMEText(self.message_text))
            server.sendmail(sender, "danilovandrey22@gmail.com", msg.as_string())
            server.quit()
        except Exception as _ex_email:
            os.chdir('..')
            os.chdir('crashreport')
            now = datetime.datetime.now()
            file_name = f"{datetime.date.today()}_{now.strftime('%H:%M:%S')}".replace(':', '-')
            text = str(traceback.format_exc())
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(text)



if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])
    application = Main_GUI()
    application.show()
    sys.exit(app.exec())