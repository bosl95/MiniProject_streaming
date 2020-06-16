import sys
import socket
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
from STREAMING_SERVICE.streamer import board as streamer_board
from STREAMING_SERVICE.viewer import board as viewer_board
import threading

HOST = '192.168.22.113'
PORT = 9999
form_class1 = uic.loadUiType("login.ui")[0] # login ui 불러오기


class MyWindow(QMainWindow, form_class1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        qPixmapVar = QPixmap()
        qPixmapVar.load("login_image.jpg")
        self.img_label.setPixmap(qPixmapVar)

        self.pushButton.clicked.connect(self.btn_clicked)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        self.running = False

    def run(self):
        while True:
            if not self.running:
                print("sys exit()")
                self.client_socket.sendall('4/'.encode())
                self.client_socket.close()
                sys.exit()

    def btn_clicked(self):
        name = self.lineEdit.text()
        print("name: " + name)
        if self.streamer_btn.isChecked() or self.view_btn.isChecked():
            self.running = True
            print('click')
            if self.streamer_btn.isChecked():
                print("stereamer")
                streamer_board(name, self)  # 스트리머로 접속
                self.close()
                self.thread = threading.Thread(target=self.run)
                self.thread.start()
            elif self.view_btn.isChecked():
                print("viewer")
                viewer_board(name, self)    # 유저로 접속
                self.close()
                self.thread = threading.Thread(target=self.run)
                self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
