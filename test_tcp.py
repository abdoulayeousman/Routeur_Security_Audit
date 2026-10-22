import sys
import socket

def test_tcp(cible, portlist):
    ports_ouverts = []
    try:
        print("==========================\n"
            "[+] Analyse des port TCP\n"
            "===============================")
        for port in portlist:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((cible, port))
            if result == 0:
                print("Port {} \t :OUVERT".format(port))
                ports_ouverts.append(port)
            else:
                print("Port {} \t :FERME".format(port))
            sock.close()
    except socket.error as error:
        print(str(error))
        print("Connection error")
        sys.exit()
    return ports_ouverts