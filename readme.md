
## Real-time streaming Program
> ### 1. Server
- 채팅 관리 : ``sendMsg()``
- 도네이션(후원) 기능 : ```sendDonation()```
	- 접속자 중 후원을 보내면 후원 금액과 메세지를 모든 접속자에게 전달
- 회원 입장/퇴장 관리 및 서버 기능 구별  : ``recvOp()``
	- 채팅 메세지 / 후원 메세지 / 퇴장 등을 구분
	- 입/퇴장 표시
		
> ### 2. Streamer
- UI design : PyQt5 를 이용
- chat / real-time streaming ⇒ **Thread 모듈** 이용
- ``start()`` : 방송 버튼을 눌렀을 경우 실행되는 함수. camera_on.py 파일을 통해서 mjpg streamer를 실행하는 파일.

	  # camera_on.py
      #!/usr/bin/python  
	  import os, subprocess  
	  os.system("cd ~")  
	  subprocess.call("sh ~/mjpg.sh", shell=True)		# mjpg.sh 실행.
	  
- ``run()`` : 방송 영상을 mjpg stream으로부터 가져오는 thread 함수.
	다른 서비스와 함께 계속 실행되면서 **flag가 False가 되는 경우(방송이 종료된 경우)** 영상 송출을 멈춘다.
- ``writeDonationMsg()`` : 후원 메세지를 서버로부터 받아와 후원명과 금액을 송출. 이때 금액에 따라 컬러를 구별

	  # 후원 금액에 따른 색 변경  
	  if i < 3000:  
		   self.ui_layout.donation_label.setStyleSheet("Color: #024249;")  
	  elif i < 5000:  
	 	   self.ui_layout.donation_label.setStyleSheet("Color: #16817a;")  
	  elif i < 10000:  
		   self.ui_layout.donation_label.setStyleSheet("Color: #fa744f;")  
	  else:  
		   self.ui_layout.donation_label.setStyleSheet("Color: #f79071;")
    
	- pyttsx3 : 후원 메세지를 읽어주는 모듈
	
		  saymsg = msg.split("^----^\n")[1]  
		  self.engine.say(saymsg)  
		  self.engine.runAndWait()
	
	- winsound : 후원 사운드를 실행시켜주는 모듈

		  winsound.PlaySound('coin.wav', winsound.SND_FILENAME)
	
- ``chat_btn_clicked()`` : 채팅창의 입력 버튼 클릭시 활성화 함수. 엔터를 눌러도 함수가 실행됨.

	  self.ui_layout.chat_input.returnPressed.connect(self.chat_btn_clicked) 	# 엔터키도 활성화 

- UI 구성

	![enter image description here](https://user-images.githubusercontent.com/34594339/88698605-39bd2d00-d141-11ea-9f1c-b5a51a3a6a18.png)
	 - STREAMING OFF Button
		- STREAMING OFF : 방송 미송출 상태
		- STREAMING ON : 버튼을 누르면 화면 송출 레이아웃 (왼쪽 상단) 에 라즈베리 파이의 화면이 출력되면서 button 값이 STREAMING ON으로 바뀜.
	- Donation Layout(우측 상단) : 후원명 / 후원 메세지 / 후원 금액을 모든 접속자에게 송출하는 부분
	- Chatting Layout(우측 하단)
	- Exit Button : 프로그램 종료

> ### 03. Viewer
- 기본적인 영상 송출 / 채팅 / 후원 출력 등의 기능은 streamer와 같음.
- 후원 버튼 클릭 시  ==> done_layout 을 통한 후원 창을 띄움. ``donation_bnt_clicked()`` 함수
- UI 구성

	![enter image description here](https://user-images.githubusercontent.com/34594339/88701869-8f93d400-d145-11ea-8afb-74253e978f2e.png)

	![enter image description here](https://user-images.githubusercontent.com/34594339/88702211-fca76980-d145-11ea-8c57-05689e2823ce.png)

	- 금액이 지정된 radion button 클릭 시 ⇒ 지정된 금액이 자동으로 후원 금액 text box로 입력. 수정 불가능.
	- 직접 입력 radio button 클릭 시 ⇒ 후원 금액을 직접 입력.

> ### 04. Package
> ``pyinstaller`` 를 이용하여 OpenCV 등과 같은 설치 모듈들을 다 포함한 exe 파일을 패키징.
