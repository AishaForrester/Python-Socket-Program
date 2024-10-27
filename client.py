# Client to implement a simple program that will carry out an exchange of
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
from socket import * 
import random 
#Note: to run this code against the server, you must change the localhost below into your ip address
serverName = 'localhost' #Python client module: The ip address will be resolved by a call to the DNS
serverPort = 10128       #Python client module: Port number of the server that we wish to contact

def serverHello():
  """Generates server hello message"""
  status = "100 Hello"
  return status

def AllGood():
  """Generates 220 Verified"""
  status = "220 OK"
  return status

def ErrorCondition():
  """Generates 400 Error"""
  status = "400 Error"
  return status

def ChallengeMsg(c):
  """Generates 111 Challenge """
  status = "111 Challenge " + str(c)
  return status

 
# s     = socket
# msg   = message being processed
# state = dictionary containing state variables
def processMsgs(s, msg, state):
  """This function processes messages that are read through the socket. It
     returns a status, which is an integer indicating whether the operation
     was successful.
  for key, values in state.items():
    print(f"{key}: {values}")
  print("end was met: stop HERE")"""
  #Extracting the integers from the dictionary that we will use in this function
  c = state['c']    
  g = state['g']
  p = state['p']
  t = state['t']
  V = state['V']

  if msg.startswith("105"):           #Making sure that the server had sent over the correct message
    clientMessage2 = ChallengeMsg(c)
    s.send(clientMessage2.encode())
    print("*** (5.) Sent 111 Challenge c over to the server ***\n") #Informative message for testing and grader
    return 1
  elif msg.startswith("112"):  #we need to extract the b as it is our z
    parts2 = msg.split()
    z = int(parts2[-1])        #Extracting B
    
    comparison1 = NumTheory.expMod(g,z,p)
    comparison2 = (t*(V**c)) %p
    if comparison1 == comparison2:        #Comparison between the two calculations
      clientMessage3 = AllGood()
      s.send(clientMessage3.encode())
      print("*** (9.) 220 Was sent to client. All Good!! ***")   #Informative message for testing and grader
      s.close()
    else:
      clientMessage4 = ErrorCondition()
      s.send(clientMessage4.encode())
      print("***(9.)400 Was sent to client. No match!!***")   #Informative message for testing and grader
      s.close()
  else:
    clientMessage5 = "500 Bad Request"
    print("*Program received a bad request from server. Closing connection*")  #Informative message for testing and grader
    s.send(clientMessage5.encode())
    return 1
    

  

def main():
  """Driver function for the project"""
  args = sys.argv
  if len(args) != 3:
    print("Please supply a server address and port.")
    sys.exit()
  serverHost = str(args[1])  #The remote host
  serverPort = int(args[2])  #The port used by the server
  print("Client of Aisha K Forrester")
  print("""
  The purpose of this program is to collect two prime numbers from the client, and then
  send them to the server. The server will compute their LCM and send it back to the
  client. If the server-computed LCM matches the locally computed LCM, the
  clientsends the server a 200 OK status code. Otherwise it sends a 400 error status code,
  and then closes the socket to the server.
  """)
  #Add code to initialize the socket
  clientSocket = socket(AF_INET, SOCK_STREAM)    #Created the client TCP socket
  clientSocket.connect((serverName, serverPort)) #Establishing the connection to the server via handshaking

  msg = serverHello()
  #Add code to send data into the socket
  clientSocket.send(msg.encode())                              #Initial 100 Hello message to server
  print("*** (1.) Sent 100 Hello to the server ***\n")         #Informative message for testing and grader

  serverMessage1 = clientSocket.recv(1024).decode()            #The server sent over the first message
  print("*** (4.) Client received 105 Generator + Commitment g,p,t,V from server ***\n") #Informative message for testing and grader
  if not serverMessage1.startswith("105"): #preventing invalid generator and wrong prime from entering
    print("\nServer received an invalid generator or invalid prime contraint. Closing connection")
    clientSocket.close()
    sys.exit()
  parts = serverMessage1.split('+')       #Here, we are splitting the message to extract g,pt, V
  values_part = parts[-1].strip() #split
  values = values_part.replace("Commitment", "").strip().split(',')

  # Convert values to integers
  g = int(values[0].strip())
  p = int(values[1].strip())
  t = int(values[2].strip())
  V = int(values[3].strip())
  print("Where: \ng = " + str(g) + "\n"+ "p = " + str(p) + "\n" + "t= " + str(t) + "\n" + "V = " + str(V) + "\n")

  c = random.randint(1,p)  #Generating the random c to send to the server for challenging

  #storing these values in a dictionary
  statCodeC = {
         'g': g,
         'p': p,
         't': t,
         'V': V,
         'c': c
      }
  
  processMsgs(clientSocket, serverMessage1, statCodeC)  #sending the information for processing
  

  serverMessage2 = clientSocket.recv(1024).decode() # received message: 112 response B from server
  print("*** (8.) Received 112 response B from server ***\n")
  processMsgs(clientSocket, serverMessage2, statCodeC)
  


  #Handle the data that is read through the socket by using processMsgs(s, msg, state)

  #Close the socket
if __name__ == "__main__":
    main()


  #python server.py 10128                  ---> copy and paste for grading and testing
  #python client.py localhost 10128        ---> copy and paste for grading and testing 
  #Test cases that works:                  (3, 257), (19,719), (5, 743),(11, 769), and (5, 907)
  #Test Cases that do not work:            (5,23), (5,47), (19,83)