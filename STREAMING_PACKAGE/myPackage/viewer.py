import sys, subprocess
import cv2
import threading
import pyttsx3
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QImage, QPixmap
import time, re
from PyQt5.QtWidgets import QButtonGroup
import winsound
class board:
    def __init__(self, name, infoForm):
        self.done_app = QtWidgets.QApplication(sys.argv)
        self.done_layout = uic.loadUi("donation.ui")
        self.done_layout.done_btn.clicked.connect(self.done_btn_clicked)
        # donation layout
        print("viewer board")
        self.parentFrom = infoForm
        self.flag = True
        self.send_flag = True
        self.client_socket = infoForm.client_socket
        print('connecting...')
        self.client_socket.sendall(name.encode())
        # socket
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        # ttx
        self.thread1 = threading.Thread(target=self.readMsg)
        self.thread1.start()
        # chatting
        self.app = QtWidgets.QApplication(sys.argv)  # 프로그램을 실행시켜줌
        self.ui_layout = uic.loadUi("Livechat_viewer.ui")  # ui를 가져온다
        self.ui_layout.show()
        # default ui
        self.ui_layout.stream_screen.setPixmap(QPixmap('pimo.png'))
        self.ui_layout.stream_screen.update()
        # streaming off image
        self.stream_thread = threading.Thread(target=self.run)
        self.stream_thread.start()
        # streaming
        self.ui_layout.close_btn.clicked.connect(self.onExit)
        self.ui_layout.chat_input.returnPressed.connect(self.chat_btn_clicked)
        self.ui_layout.chatbox.ensureCursorVisible()
        self.ui_layout.chat_btn.clicked.connect(self.chat_btn_clicked)
        self.ui_layout.donation_btn.clicked.connect(self.donation_bnt_clicked)
        self.app.exec_()
        # default ui
    def run(self):  # 영상을 출력하는 thread
        while self.flag:
            self.cap = cv2.VideoCapture("http://192.168.103.72:8091/?action=stream.html")
            if not self.cap.isOpened():
                self.ui_layout.stream_screen.setPixmap(QPixmap('pimo.png'))
                self.ui_layout.stream_screen.update()
            else:
                ret, frame = self.cap.read()
                if ret:
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    convertFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                    pixmap = QPixmap(convertFormat)
                    p = pixmap.scaled(720, 500, QtCore.Qt.IgnoreAspectRatio)
                    self.ui_layout.stream_screen.setPixmap(p)
                    self.ui_layout.stream_screen.update()
                    time.sleep(0.03)
        self.cap.release()
        cv2.destroyAllWindows()
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
        if i < 3000:
            self.ui_layout.donation_label.setStyleSheet("Color: #024249;")
        elif i < 5000:
            self.ui_layout.donation_label.setStyleSheet("Color: #16817a;")
        elif i < 10000:
            self.ui_layout.donation_label.setStyleSheet("Color: #fa744f;")
        else:
            self.ui_layout.donation_label.setStyleSheet("Color: #f79071;")
        winsound.PlaySound('coin.wav', winsound.SND_FILENAME)
        saymsg = msg.split("^----^\n")[1]
        self.engine.say(saymsg)
        self.engine.runAndWait()
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
                print("donation")
            elif tmp[0] == "3":
                print(tmp[1])
            if msg == '/stop':
                break
        print('서버 메시지 출력 쓰레드 종료')
    def chat_btn_clicked(self):
        str = self.ui_layout.chat_input.text()
        if str == "":
            return
        else:
            str = "1/" + str
            self.client_socket.sendall(str.encode())
            self.ui_layout.chat_input.setText("")
    def donation_bnt_clicked(self): # 후원 버튼을 누르면 후원 창을 생성
        self.done_layout.show()
        self.done_price_group = QButtonGroup()
        self.done_price_group.addButton(self.done_layout.done_1000)
        self.done_price_group.addButton(self.done_layout.done_3000)
        self.done_price_group.addButton(self.done_layout.done_5000)
        self.done_price_group.addButton(self.done_layout.done_10000)
        self.done_price_group.addButton(self.done_layout.done_user_input)
        self.done_price_group.buttonPressed.connect(self.price_radio_btn_clicked)
        self.done_app.exec_()
    def price_radio_btn_clicked(self, btn):
        if btn is self.done_layout.done_1000:
            self.done_layout.done_price.setText("1000")
            print("1000")
        elif btn is self.done_layout.done_3000:
            self.done_layout.done_price.setText("3000")
            print("3000")
        elif btn is self.done_layout.done_5000:
            self.done_layout.done_price.setText("5000")
            print("5000")
        elif btn is self.done_layout.done_10000:
            self.done_layout.done_price.setText("10000")
            print("10000")
        elif btn is self.done_layout.done_user_input:
            self.done_layout.done_price.setText("")
            self.done_layout.done_price.setReadOnly(False)
        else:
            print("에러")
            return
    def done_btn_clicked(self):    # 후원 창에서 금액을 입력하여 후원하기
        done = "2/"+self.done_layout.done_price.text()+"@"+self.done_layout.done_msg.text()
        self.client_socket.sendall(done.encode())
        self.done_layout.close()
    def stop(self):
        self.flag = False

    def onExit(self):
        print('exit')
        self.stop()
        self.send_flag = False
        self.parentFrom.running = False
        self.ui_layout.close()