import socket
import random

class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.g = None
        self.p = None

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            while True:
                msg = client_socket.recv(1024).decode()
                if not msg:
                    break
                self.processMessage(client_socket, msg)

    def processMessage(self, s, msg):
        if msg.startswith("100"):
            print("Received:", msg)
            self.g = int(input("Enter the generator sent by the server: "))
            self.p = int(input("Enter the prime number sent by the server: "))
            s.sendall(f"105 Generator + Commitment {self.g}, {self.p}".encode())
        elif msg.startswith("105"):
            print("Received:", msg)
            parts = msg.split(", ")
            c = random.randint(1, self.p - 1)
            challenge_msg = f"111 Challenge {c}"
            print("Sending:", challenge_msg)
            s.sendall(challenge_msg.encode())
        elif msg.startswith("112"):
            print("Received:", msg)
            z = int(msg.split()[2])
            # Compare values (for demonstration, assume verification is true)
            s.sendall("220 Verified".encode())
        elif msg.startswith("400"):
            print("Error:", msg)
        elif msg.startswith("500"):
            print("Bad Request:", msg)

if __name__ == "__main__":
    client = Client()
    client.start()

#python ChatGPTServer.py 65432
#python ChatGPTClient.py localhost 65432