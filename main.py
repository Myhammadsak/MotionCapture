###библиотеки########################################
import asyncio
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyCameraList.camera_device import list_video_devices
import json
####################################################




###базовые переменные##############################
tit = 'STEP CARTOGRAPHER'
##################################################




###Главное окно####################################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #Загрузка окна
        uic.loadUi('ui/menu.ui', self)
        #Название окна
        self.setWindowTitle(tit)

        #Размеры окна
        self.setFixedWidth(820)
        self.setFixedHeight(550)

        #Кнопки
        self.pushButton_3.clicked.connect(self.off)
        self.pushButton.clicked.connect(self.go)
        self.pushButton_4.clicked.connect(self.seti)

    ### открывает класс запуска процесса
    def go(self):
        self.goo = Go()
        self.goo.show()
        Window.close(self)

    ### открывает класс настроек
    def seti(self):
        self.seti = Seti()
        self.seti.show()
        Window.close(self)

    ### завершает программу
    def off(self):
        sys.exit()
##################################################




###Класс настроек#################################
class Seti(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui/Seti.ui', self)
        self.setWindowTitle(tit)

        self.setFixedWidth(900)
        self.setFixedHeight(950)


        #Добавление списка возможных камер камер
        cameras = list_video_devices()
        splitted = list(cameras)
        for i in range(len(splitted)):
            self.listWidget.addItem(f'{splitted[i]}\n')

        #выбор камер
        #читает json файл и устанваливаетв спинбоксы свои параметры
        with open('ui\camera_index.json') as fcc_file:
            self.index_cam = json.load(fcc_file)
        self.spinBox.setValue(self.index_cam["ri"])
        self.spinBox_2.setValue(self.index_cam["le"])
        self.spinBox_3.setValue(self.index_cam["fr"])

        #Кнопки
        self.pushButton_2.clicked.connect(self.boss_window)
        self.pushButton.clicked.connect(self.save_camera)



    #Закрывает это окно и переходит в главное меню
    def boss_window(self):
        self.window = Window()
        self.window.show()
        Seti.close(self)

    def save_camera(self):
        #сохранят в json файл значения которые установил пользователь
        self.index_cam["ri"] = self.spinBox.value()
        self.index_cam["le"] = self.spinBox_2.value()
        self.index_cam["fr"] = self.spinBox_3.value()
        with open("ui\camera_index.json", "wt", encoding="utf-8") as file:
            json.dump(self.index_cam, file, indent=1)

        self.window = Window()
        self.window.show()
        Seti.close(self)
##################################################




###Класс запуска процесса#########################
class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/go1.ui', self)
        self.setWindowTitle(tit)

        self.setFixedWidth(370)
        self.setFixedHeight(490)

        ## Изображение
        self.pixmap = QPixmap('ui/nn.png')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(40, 60)
        self.image.resize(300, 300)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

        self.go.clicked.connect(self.start1)

    #Функция запуска главного процесса с mediapipe
    def start1(self):
        self.name_pap = self.lineEdit.text()
        a = []
        for i in range(len(self.name_pap)):
            if self.name_pap[i] == " ":
                pass
            else:
                a.append(1)
        if len(a) == 0:
            QMessageBox.information(
                self,
                "Error",
                "Название папки некорректно")

        else:
            os.mkdir(fr'C:\{self.name_pap}')

            self.go.hide()
            self.lineEdit.hide()

            try:
                SCRIPTS = [
                    'left_camera.py',
                    'right_camera.py',
                    'the_front_camera.py'
                ]

                async def waiter(sc, p):
                    "Функция которая вернет имя скрипта после ожидания"
                    await p.wait()
                    return sc, p

                async def main():
                    waiters = []

                    # Запуск
                    for sc in SCRIPTS:
                        p = await asyncio.create_subprocess_exec(sys.executable, sc)
                        print('Started', sc)
                        waiters.append(asyncio.create_task(waiter(sc, p)))

                    # Ожидание
                    while waiters:
                        done, waiters = await asyncio.wait(waiters, return_when=asyncio.FIRST_COMPLETED)
                        for w in done:
                            sc, p = await w
                            print('Done', sc)

                if __name__ == "__main__":
                    asyncio.run(main())

            except:
                pass
        self.go_2.clicked.connect(self.ggo)

    #Функция перемещения файлов
    def ggo(self):
        os.rename(fr'C:\the_front_camera.txt', fr'C:\{self.name_pap}\the_front_camera.txt')
        os.rename(fr'C:\left_camera.txt', fr'C:\{self.name_pap}\left_camera.txt')
        os.rename(fr'C:\right_camera.txt', fr'C:\{self.name_pap}\right_camera.txt')
        self.res = Results()
        self.res.show()
        Go.close(self)
##########################################




###конечное меню##########################
class Results(QMainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Results.ui', self)
        self.setWindowTitle(tit)

        self.setFixedWidth(1080)
        self.setFixedHeight(600)

        self.Srav.clicked.connect(self.file_srav)
        # self.Tabl.clicked.connect(self.wid)

    #Выбор файла для сравнения
    def file_srav(self):
        fname_1 = QFileDialog.getOpenFileName(
            self, 'Выбрать значения', '',
            'Первые значения (.txt);Все файлы (*)')[0]
        with open(fname_1, 'r') as file:
            contents_1 = file.read()
            contents_1_save = [].append(contents_1)

    # def wid(self, s):
    #     button = QMessageBox.critical(
    #         self,
    #         "Oh dear!",
    #         "Something went very wrong.",
    #         buttons=QMessageBox.Discard | QMessageBox.NoToAll | QMessageBox.Ignore,
    #         defaultButton=QMessageBox.Discard,
    #     )
#############################################




###запуск программы##########################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
#############################################