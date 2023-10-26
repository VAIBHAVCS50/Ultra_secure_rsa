import socket
import threading
import modified_rsa as habsd
import timeit
import pandas as pd
import matplotlib.pyplot as plt

HEADER = 2048
PORT = 80
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected succesfully.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False




            print(f"[{addr}] {msg}")
            tic=timeit.default_timer()
            encrypted_msg = habsd.callme(msg,threading.active_count())
            toc=timeit.default_timer()
            # print("\nYour encrypted message is: ")



            # print(''.join([str(x) for x in encrypted_msg]))
            # dey = habsd.decrypt(encrypted_msg)
            # print("\nYour decrypted message is: ")
            # print(dey)
            # print("\nTotal time taken to encrypt:")
            #print(toc - tic)
            #encrypted_salted_text = HashingAndSalting.salt(encrypted_msg)
            #Sender_HASH = hashlib.sha256(encrypted_salted_text.encode()).hexdigest()

            print("encrypted and hashed value stored in database\n")
            dataset = pd.read_excel('storedhashandsalt.xlsx')
            x = dataset.iloc[:,3].values
            y = dataset.iloc[:,4].values

            plt.scatter(x,y)
            plt.title('Key vs. Time Taken')
            plt.xlabel('Time Taken')
            plt.ylabel('Key Size')
            plt.show()



           # print("\nDecrypting message with private key ")
            #print("\nYour message is:")
           # tic = timeit.default_timer()
           # print(habsd.decrypt(encrypted_msg))
         #   toc = timeit.default_timer()
           # print("\nTotal time taken to decrypt:")
          #  print(toc - tic)
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()