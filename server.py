import socket
import random

#convertim numerele de la 0 la 2 in litera aferenta miscarii pe care o reprezinta
def number_to_letter(n):
    return {0:"P", 1:"H", 2:"F"}.get(n, "X")

#convertim literele P,H,F in numarul de la 0 la 2 aferent miscarii pe care o reprezinta
def letter_to_number(l):
    return {"P":0, "H":1, "F":2}.get(l, 3)

#functia trimite clientului prin conexiunea conn mesajul sa printeze stringul s
#apoi asteapta raspuns ca mesajul a fost afisat
def c_print(conn, s):
    conn.send(bytes("print" + "#" + s, 'utf-8'))
    conn.recv(buffSize).decode('utf-8')

#functia trimite clientului mesajul ca asteapta input de la jucator
#apoi primeste inputul si il returneaza
#promt e o variabila ce stabileste stringul ce se va afisa la utilizator inainte de input
#returnul ceea ce primim incepand cu pozitia 1 nu 0 deoarece vom primi mereu acel . standard
#folosit pentru a evita situatia in care nu se trimite nimic
def c_get(conn, prompt):
    conn.send(bytes("get_input" + "#" + prompt, 'utf-8'))
    return conn.recv(buffSize).decode('utf-8')[1:]

#functia ii transmite clientului sa se opreasca
def c_exit(conn):
    conn.send(bytes("exit" + "#", 'utf-8'))

#functia aceasta apeleaza c_get pana cand primeste un input valid
def c_get_validated(conn, prompt, options):
    while True:
        data = c_get(conn, prompt)
        if data not in options:
            c_print(conn, "Nu există o astfel de variantă. Verificați și introduceți din nou\n")
        else:
            return data

conn_data = ('127.1', 4321)

buffSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(conn_data)
    sock.listen()
    conn, _ = sock.accept()
    
    with conn:
        #Prima bucla va sustine toate jocurile pana cand jucatorul da EXIT
        while True:
            data = c_get_validated(conn, "Tastati START pentru a incepe un joc nou si EXIT pentru a opri aplicatia.\n", ("START", "EXIT"))
            #Cazul in care jucatorul vrea sa opreasca aplicatia
            if data == "EXIT":
                c_exit(conn)
                sock.close()
                exit()
            #Cazul in care jocul aplicatia continua
            else:
                rounds = 1 
                scor_server = 0
                scor_client = 0
                #A doua bucla corespunde unui singur joc
                while True:
                    #Serverul isi genereaza aleatoriu propria miscare pentru runda inainte sa ceara miscarea jucatorului
                    server_move = random.randint(0,2)
                    #Serverul cere jucatorului miscarea sa
                    answer = c_get_validated(conn, f"P pentru Piatra\nH pentru Hartie\nF pentru Foarfeca\nRUNDA {rounds}", ("P", "H", "F"))
                    #Transformam mutarea jucatorului in numere de la 0 la 2 echivalente ca valoarea cu cele generate de server
                    #Diferenta dintre cele doua + 3 totul modulo 3 va fi mereu egala cu 0,1 sau 2 ce vor semnifica egal, pierdere sau castig
                    match (server_move - letter_to_number(answer) + 3) % 3: 
                        case 0:
                            c_print(conn, "Egal, mai incearca!")
                        case 1:
                            c_print(conn, "Ai pierdut runda!")
                            scor_server += 1
                        case 2:
                            c_print(conn, "Ai castigat runda!")
                            scor_client += 1
                    #daca scorul clientului sau scorul serverului a ajuns la 2 victorii atunci jocul e decis
                    if scor_client == 2:
                        c_print(conn, f"Ai castigat din {rounds} runde")
                        break
                    if scor_server == 2:
                        c_print(conn, f"Serverul a castigat din {rounds} runde, ai pierdut!")
                        break
                    #dupa finalul rundei numaram runda jucata
                    rounds += 1
