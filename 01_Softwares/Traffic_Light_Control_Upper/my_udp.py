import socket

def send_to(address:str,port:int,message:str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (address, port)
    message += "\r\n"
    sock.sendto(message.encode(), server_address)
    sock.close()

if __name__ == "__main__":
    send_to("192.168.14.78",159,"set 0 0 0;")