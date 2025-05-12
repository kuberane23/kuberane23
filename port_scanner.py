import socket

target = input("Ip to scan: ")

def pscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((target, port))
        s.close()
        return True
    except:
        return False

for x in range(1, 1025):  # Scan ports 1 to 1024
    if pscan(x):
        print(f"Port {x} is open")
    else:
        print(f"Port {x} is closed")
