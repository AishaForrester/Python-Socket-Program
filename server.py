# Server to implement a simple program that will carry out an exchange of
# messages that contains elements of a zero knowledge
# proof. The client sends a hello message to the server. The server responds
# with a message containing a generator, a prime, some public information, and
# a "commitment" message. The client will respond with a challenge message that
# contains an integer. The server transforms that received integer and then
# sends a response message to the client. The client checks that this
# transformed integer shows that the server knows the secret (without the
# secret being revealed).

# Author: Aisha Forrester
# Last modified: 2024-10-22
#!/usr/bin/python3

import socket
import sys
from random import SystemRandom
from NumTheory import NumTheory
import random

serverPort =  10128  

def PrimeCollect():
  """Accepts a prime number to send to the client"""
  primeNbr = input("Enter a prime number between 127 and 7919: ")
  return primeNbr

def GeneratorCollect():
  """Accepts a generator for the prime"""
  generator = input("Enter a generator for the prime number: ")
  return generator


def clientHello(g, p, x, r):
  """Generates an acknowledgement for the client heGeneratoressage"""
  msg = "105 Generator + Commitment "+ str(g) + ", " + str(p) + ", "+ \
  str(NumTheory.expMod(g,r,p)) + ", " + str(NumTheory.expMod(g,x,p))
  return msg

# r is the nonce chosen by the server
# x is the server's secret integer
# c is the client's challenge integer
def genChallengeResponse(r, x, c):
  """Generates the 107 LCM string"""
  z = r + c*x
  msg = "112 Response " + str(z)
  return msg

#s      = socket
#msg    = message being processed
#state  = dictionary containing state variables
def processMsgs(s, msg, state):
  """This function processes messages that are read through the socket. It returns
     a status, which is an integer indicating whether the operation was successful."""
  g = state['g']
  p = state['p']
  t = state['t']
  V = state['V']
  x = state['x']
  r = state['r']
  if msg.startswith("100"):  #Making sure that the client had sent over the correct message
    serverMessage1 = clientHello(g, p, x, r)
    s.send(serverMessage1.encode())
    print("\n*** (3.) Sent 105 Generator + Commitment g,p,t,V to client ***\n") #Informative message for testing and grader
    return 1
  elif msg.startswith('111'):
    parts = msg.split()   #Splitting the message to extract C
    c = int(parts[-1])
    serverMessage2 = genChallengeResponse(r, x, c)
    s.send(serverMessage2.encode())
    print("*** (7.) Sent over 112 Response B ***\n")
  elif msg.startswith('220'):
    print("*** (10.) This server received a 220 verified message. All good!! ***") #Informative message for testing and grader
    s.close()
  elif msg.startswith('400'):
    print("*** (10.) This server received a 400 message: Retrace code!! ***")  #Informative message for testing and grader
    s.close()
  else:
    serverMessage3 = "500 Bad Request"
    print("*Program received a bad request from server. Closing connection*") #Informative message for testing and grader
    s.send(serverMessage3.encode())
    return 1


     

def main():
  """Driver function for the server."""
  args = sys.argv
  if len(args) != 2:
    print ("Please supply a server port.")
    sys.exit()
  HOST = ''              #Symbolic name meaning all available interfaces
  PORT = int(args[1])    #The port on which the server is listening.
  if (PORT < 1023 or PORT > 65535):
    print("Invalid port specified.")
    sys.exit()

  print("Server of Aisha K.Forrester")
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    # Bind socket:  the socket will bind to any available interfaces iin this case
    s.bind(("0.0.0.0",serverPort))  #Allows the os to not assign us a random port number and connect to all available interface on the network
    # listen                        #This will help with the interoperability tests and grading ("0.0.0.0")
    s.listen(1)  #We listen for 1 incoming connection and thats from our client
    
    conn, addr = s.accept()  # accept connections using socket, established a new dedicated socket for the connection
    with conn:
      print("Connected from: ", addr)
      #Process messages received from socket using 
      #  processMsgs(s, msg, state)
      
      sentence = conn.recv(2048).decode()  #Grabbing the data from the socket
      print("\n*** (2.) Received 100 Hello from client ***\n")
      p = int(PrimeCollect())     #Asking the user for a prime number
      g = int(GeneratorCollect()) #Asking the user for a generator
      if NumTheory.IsValidGenerator(g, p):
        newg = g
      else:
        print("Invalid generator. Closing connection")
        conn.close()
        sys.exit()

      if 127 <= p <= 7919:
        newp = p
      else:
        print("Incorrect values for prime number. Closing connection")
        conn.close()
        sys.exit()

      r = random.randint(1,p)
      x = random.randint(1,p)
      t = NumTheory.expMod(g,r,p)
      V = NumTheory.expMod(g,x,p)

      

      statCode = {
         'g': newg,
         'p': newp,
         'r': r,
         'x': x,
         't': t,
         'V': V,
      
      }
      processMsgs(conn, sentence, statCode)

      sentence2 = conn.recv(2048).decode()
      print("*** (6.) Received 111 Challenge c message from client ***\n")
      processMsgs(conn, sentence2,statCode)

      sentence3 = conn.recv(2048).decode()  #received 220 or 400 from client
      processMsgs(conn, sentence3,statCode)




      
if __name__ == "__main__":
    main()

  #python server.py 10128                  ---> copy and paste for grading and testing
  #python client.py localhost 10128        ---> copy and paste for grading and testing 
  #Test cases that works:                  (3, 257), (19,719), (5, 743),(11, 769), and (5, 907)
  #Test Cases that do not work:            (5,23), (5,47), (19,83)
  #They will not work because the prime is less than 127 which is specified