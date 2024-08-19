import socket

conn_data = ('127.1', 4321)

buffSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(conn_data)
    while True:
        #Primim de la server o actiune si un argument la actiune separate printr-un separator
        server_string = sock.recv(buffSize).decode('utf-8')
        #actiunea se gaseste inainte de separator
        server_action = server_string.split('#')[0]
        #argumentul se gaseste dupa separator
        server_argument = server_string.split('#')[1]
        match server_action:
            #in caz de exit clientul se opreste
            case "exit":
                exit()
            #in caz de print afisam mesajul primit de la server prin argument
            case "print":
                print(server_argument)
                #dupa ce afisam trimitem inapoi la server orice pentru a anunta ca am terminat de afisat
                sock.send(bytes(".", 'utf-8'))
            case "get_input":
                #in caz de get_input cerem utilizatorului un string pe care il trimitem inapoi serverului
                #in caz ca utilizatorul trimite mai mult de 1000 de caractere, urmatoarele se ignora pentru a nu face
                #un buffer overflow, vom trimite mereu un punct ca si atunci cand utilizatorul nu trimite nimic
                #serverul sa primeasca instintare ca s-a incercat sa se trimita ceva
                sock.send(bytes("."+input(server_argument + "> ")[:1000], 'utf-8'))
