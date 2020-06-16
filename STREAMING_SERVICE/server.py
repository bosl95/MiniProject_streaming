import threading, socket
HOST = '192.168.22.113' # 서버 아이피
port_chat = 9999 # 사용할 포트 번호(chatting)
sockets= []
chat_sock = {} # 접속된 채팅 클라이언트 소켓(key - ip, value - 닉네임)
donations = {} # 후원 목록들

# def makeRank(client_socket, addr):
#     rank = "3/"
#     l = sorted(donations.items(), key = (lambda x:x[1]), reverse=True)
#     i = 1
#     for key,value in l:
#         rank += (str(i)+'등 '+str(chat_sock[key])+'님 :'+str(value)+'원입니다 ~!')
#         i+=1
#     client_socket.sendall(rank.encode())  # 순위 목록 보내기

def sendMsg(client_socket, addr, msg):  # 채팅 메세지 전송하는 함수
    msg = '1/' + str(chat_sock[addr]) + ' : ' + msg # 닉네임 : 내용
    for s in sockets:
        s.sendall(msg.encode())  # 접속한 모든 유저들에게

def sendDonation(client_socket, addr, msg): # 유저가 보낸 후원 메세지를 접속한 모든 유저들에게 전송
    ops = msg.split('@')
    newMsg = '2/'+ str(chat_sock[addr])+'님 '+ ops[0]+ '원 후원 감사합니당 ^----^\n' + ops[1]
    print(newMsg)   # 후원 메세지 확인
    for s in sockets:   # 모든 유저에게
        s.sendall(newMsg.encode())  # 받은거 다시 보내기
    # 후원
    if addr in donations: # 있다면 후원 금액 업데이트
        tmp = donations[addr]
        donations[addr] = tmp + int(ops[0])
    else:
        donations[addr] = int(ops[0])  # 후원 금액 추가

def recvOp(client_socket,addr):
    data = client_socket.recv(1024)  # 사용자가 사용할 닉네임 받음
    nickname = data.decode()
    print(nickname+"님 입장하셨습니다")
    chat_sock[addr] = nickname  # 유저 소켓 추가
    sockets.append(client_socket)
    while True:
        data = client_socket.recv(1024) # 1/내용
        msg = data.decode()
        print(nickname+ ": "+msg)
        ops = msg.split('/')
        if ops[0] == '1': # 채팅 메세지
            sendMsg(client_socket, addr, ops[1])
        elif ops[0] == '2': # 후원 메세지
            sendDonation(client_socket, addr, ops[1])
        # elif ops[0] == '3': # 후원 순위
        #     makeRank(client_socket, addr)
        elif ops[0] == '4': # 나감
            sockets.remove(client_socket)
            break
    if addr in chat_sock:
            print(nickname, '퇴장')
            del chat_sock[addr]
def main():
    # 채팅을 위한 서버 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port_chat))
    server_socket.listen()
    while 1:
        client_socket, addr = server_socket.accept()  # accpet로 클라이언트의 접속을 기다리다 요청시 소켓 생성해 줌
        t1 = threading.Thread(target=recvOp, args=(client_socket,addr))
        t1.start()
main()