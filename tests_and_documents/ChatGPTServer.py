import socket
import random

class NumTheory:
    @staticmethod
    def expMod(b, n, m):
        if n == 0:
            return 1
        elif n % 2 == 0:
            return NumTheory.expMod((b * b) % m, n // 2, m)
        else:
            return (b * NumTheory.expMod(b, n - 1, m)) % m

    @staticmethod
    def isValidGenerator(g, p):
        seen = set()
        for i in range(1, p):
            seen.add(NumTheory.expMod(g, i, p))
        return len(seen) == (p - 1) and g < p

class Server:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.g = None
        self.p = None
        self.x = random.randint(1, 7919)  # Secret integer
        self.r = random.randint(1, 7919)  # Nonce

    def collectParameters(self):
        self.g = int(input("Enter a generator for the prime number: "))
        self.p = int(input("Enter a prime number between 127 and 7919: "))

    def clientHello(self):
        return f"105 Generator + Commitment {self.g}, {self.p}, {NumTheory.expMod(self.g, self.r, self.p)}, {NumTheory.expMod(self.g, self.x, self.p)}"

    def generateChallenge(self, c):
        z = self.r + c * self.x
        return f"112 Response {z}"

    def start(self):
        self.collectParameters()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}...")
            
            conn, addr = server_socket.accept()
            with conn:
                print('Connected by', addr)
                conn.sendall("100 Hello".encode())
                
                while True:
                    msg = conn.recv(1024).decode()
                    if not msg:
                        break
                    self.processMessage(conn, msg)

    def processMessage(self, conn, msg):
        if msg.startswith("105"):
            response = self.clientHello()
            conn.sendall(response.encode())
        elif msg.startswith("111"):
            c = int(msg.split()[2])
            response = self.generateChallenge(c)
            conn.sendall(response.encode())
        elif msg.startswith("112"):
            z = int(msg.split()[2])
            if (NumTheory.expMod(self.g, z, self.p) == (NumTheory.expMod(self.g, self.r, self.p) * NumTheory.expMod(self.g, c, self.p)) % self.p):
                conn.sendall("220 OK".encode())
            else:
                conn.sendall("400 Error".encode())
        else:
            conn.sendall("500 Bad Request".encode())

if __name__ == "__main__":
    server = Server()
    server.start()

#python ChatGPTServer.py 65432
#python ChatGPTClient.py localhost 65432