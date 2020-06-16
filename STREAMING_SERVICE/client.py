import socket, threading
name = None
def th_input(soc):
    global name
    name = input("id을 입력하세요")
    soc.sendall(name.encode())
    while True:
        str = "1채팅 2.후원 3.목록"
        print(str)
        menu = int(input("선택:"))
        if menu == 1:
            while True:
                msg = input('msg:')
                ch = "1/"
                soc.sendall(ch.encode()+msg.encode())
                if msg == '/stop':
                    break
        elif menu == 2:
            done = input("후원금?")
            msg = input("msg:")
            ch = "2/"
            ch1 = "@"
            soc.sendall(ch.encode()+done.encode()+ch1.encode()+msg.encode())
        elif menu == 3:
            ch = "3/"
            soc.sendall(ch.encode())
    print('키보드 입력 쓰레드 종료')
def th_read(soc):
    while True:
        data = soc.recv(1024)
        msg = data.decode()
        tmp = msg.split("/")
        if tmp[0]=="1":
            print(tmp[1])
        elif tmp[0]=="2":
            print(tmp[1])
        elif tmp[0] == "3":
            print(tmp[1])
        if msg == '/stop':
            break
    print('서버 메시지 출력 쓰레드 종료')
def main():
    HOST = '192.168.22.113'
    PORT = 9999
    #통신할 소켓 오픈
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #서버에 연결요청. server ip, port
    client_socket.connect((HOST, PORT))
    t1 = threading.Thread(target=th_input, args=(client_socket,))
    t1.start()
    t2 = threading.Thread(target=th_read, args=(client_socket,))
    t2.start()
    #client_socket.close()
main()