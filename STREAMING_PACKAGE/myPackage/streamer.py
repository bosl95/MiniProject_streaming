import sys, subprocess
import cv2
import threading
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QImage, QPixmap
import time, re
import pyttsx3


class board:
    def __init__(self, name, infoForm):
        self.parentFrom = infoForm
        self.flag = False
        self.send_flag = True
        self.client_socket = infoForm.client_socket
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        print('connecting...')
        self.client_socket.sendall(name.encode())
        self.thread1 = threading.Thread(target=self.readMsg)
        self.thread1.start()

        self.app = QtWidgets.QApplication(sys.argv)  # 프로그램을 실행시켜줌
        self.ui_layout = uic.loadUi("Livechat_streamer.ui")  # ui를 가져온다
        self.ui_layout.show()
        self.ui_layout.stream_screen.setPixmap(QPixmap('pimo.png'))
        self.ui_layout.stream_screen.update()
        self.ui_layout.on_air.clicked.connect(self.start)

        self.ui_layout.close_btn.clicked.connect(self.onExit)
        self.ui_layout.chat_input.returnPressed.connect(self.chat_btn_clicked)
        self.ui_layout.chatbox.ensureCursorVisible()
        self.ui_layout.chat_btn.clicked.connect(self.chat_btn_clicked)
        self.app.exec_()

    def run(self):  # 영상을 출력하는 thread
        self.cap = cv2.VideoCapture("http://192.168.103.72:8091/?action=stream.html")
        if self.cap.isOpened():
            print('carmera is opened')
        else:
            print('camera is not opened')

        while self.flag:
            ret, frame = self.cap.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap(convertFormat)
                p = pixmap.scaled(720, 500, QtCore.Qt.IgnoreAspectRatio)
                self.ui_layout.stream_screen.setPixmap(p)
                self.ui_layout.stream_screen.update()
                time.sleep(0.03)
            else:
                break
        self.ui_layout.stream_screen.setPixmap(QPixmap('pimo.png'))
        self.ui_layout.stream_screen.update()
        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.flag = False
        subprocess.call("kill -9 `pgrep -f mjpg`", shell=True)
        print('stopped')

    def readMsg(self):
        print('read start')

        while self.send_flag:
            print("read")
            data = self.client_socket.recv(1024)
            msg = data.decode()
            tmp = msg.split("/")

            if tmp[0] == "1":
                self.ui_layout.chatbox.append(tmp[1])
            elif tmp[0] == "2":  # 후원
                self.writeDonationMsg(tmp[1])
            elif tmp[0] == "3":
                print(tmp[1])

            if msg == '/stop':
                break

        print('서버 메시지 출력 쓰레드 종료')

    def writeDonationMsg(self, msg):
        # 먕먕먕님 30000원 후원 감사합니당 ^----^\n' + 후원합니다
        print('후원이 들어왓네여~~')
        i1 = msg.index('님')
        i2 = msg.index('원')
        tmp = msg[i1:i2 + 1]

        i = int(re.findall('\d+', tmp)[0])
        print('금액:', i)

        # background-color: rgb(170, 255, 255)
        self.ui_layout.donation_label.setText(msg)

        # 가격별로 달라지는 색깔
        if i < 3000:
            self.ui_layout.donation_label.setStyleSheet("Color: #024249;")
        elif i < 5000:
            self.ui_layout.donation_label.setStyleSheet("Color: #16817a;")
        elif i < 10000:
            self.ui_layout.donation_label.setStyleSheet("Color: #fa744f;")
        else:
            self.ui_layout.donation_label.setStyleSheet("Color: #f79071;")
        saymsg = msg.split("^----^\n")[1]
        self.engine.say(saymsg)
        self.engine.runAndWait()

    def chat_btn_clicked(self):
        str = self.ui_layout.chat_input.text()
        if str == "":
            return
        else:
            str = "1/" + str
            self.client_socket.sendall(str.encode())
            self.ui_layout.chat_input.setText("")

    def start(self):
        self.flag = True
        if self.ui_layout.on_air.text() == "STREAMING OFF":
            self.p1 = subprocess.Popen("./camera_on.py", shell=False)
            time.sleep(2)
            th = threading.Thread(target=self.run)
            th.start()
            time.sleep(1)
            if self.cap.isOpened():
                self.ui_layout.on_air.setText("STREAMING ON")
                print('start....')
        else:
            self.stop()
            self.ui_layout.on_air.setText("STREAMING OFF")

    def onExit(self):
        print('exit')
        self.stop()
        self.send_flag = False
        self.parentFrom.running = False
        self.ui_layout.close()