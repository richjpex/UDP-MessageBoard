# Richard John Pecson Jr.
# Jose Lorenzo Santos
# CSNETWK - S13

import socket, json, threading
from art import *

current_handle = None
# Create a function to send JSON commands to server
def send_json():
    
    global current_handle
    #current_handle = None
    while True:
        # get user input
        user_input = input()
        registered = False
        # parse user input
        command_list = user_input.split()
        command = command_list[0].lower()
        # create JSON object based on user input
        json_obj = {}

        # Send JSON commands to server
        if command == '/register':
            if len(command_list) == 2:
                if current_handle is None:
                    json_obj['command'], json_obj['handle'] = 'register', command_list[1]
                    current_handle = command_list[1]
                else:
                    json_obj['command'],  json_obj['message'] = 'error', 'ALREADY-REGISTERED'
                    current_handle = current_handle

                
            else:
                json_obj['command'],  json_obj['message'] = 'error', 'INVALID-PARAMETERS'
            
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/all':
            if len(command_list) >= 2:
                json_obj['command'], json_obj['message'] = 'all', ' '.join(command_list[1:])
                
            else:
                json_obj['command'], json_obj['message'] = 'error', 'INVALID-PARAMETERS'
            
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/msg':
            if len(command_list) >= 3:
                json_obj['command'], json_obj['handle'], json_obj['message'] = 'msg', command_list[1], ' '.join(command_list[2:])
            else:
                json_obj['command'], json_obj['message'] = 'error', 'INVALID-PARAMETERS'

            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

        elif command == '/leave':
            if len(command_list) == 1:
                json_obj['command'] = 'leave'
                json_str = json.dumps(json_obj)
                sock.sendall(json_str.encode())
                print('\n' * 50)
                tprint("Message Board")
                print("Connection closed. Thank you!")
                login()
                return False
                
            else:
                json_obj['command'], json_obj['message']  = 'error', 'INVALID-PARAMETERS'
                json_str = json.dumps(json_obj)
                sock.sendall(json_str.encode())
            
        elif command == '/?' and len(command_list) == 1:
            print("Commands:")
            print("/register <handle>")
            print("/all <message>")
            print("/msg <handle> <message>")
            print("/leave")

        # unknown command
        else:
            json_obj['command'], json_obj['message'] = 'error', 'UNKNOWN-COMMAND'
            json_str = json.dumps(json_obj)
            sock.sendall(json_str.encode())

# Create a function to listen for messages from server
def listen_for_messages():
    global current_handle
    while True:
        # Receive data from the server
        try:
            data = sock.recv(1024)
            if not data:
                break
            # Decode JSON data
            json_obj = json.loads(data.decode())
            # Print messages from server
            if json_obj['command'] == 'register':
                #print(f"Welcome {json_obj['handle']}!")
                print(f"{json_obj['message']}")

            elif json_obj['command'] == 'all':
                print(f"{json_obj['handle']}: {json_obj['message']}")

            elif json_obj['command'] == 'msg':
                print(f"{json_obj['message']}")

            elif json_obj['command'] == 'error':
                print(f"{json_obj['message']}")
                current_handle = None

            elif json_obj['command'] == 'leave':
                print("Disconnected from server.")
                return False
            
        except ConnectionResetError:
            print("Error: Connection to the Message Board Server has failed!")
        
        

def login():
    global current_handle
    while True:
        
        user_input = input()

        # Parse user input
        command_list = user_input.split()
        command = command_list[0].lower()

        # Create JSON object based on user input
        json_obj = {}

        # Check if user input is valid
        if command == '/join' and len(command_list) == 3:
            host = command_list[1]
            port = command_list[2]
            if host == 'localhost' or host == '127.0.0.1' and port == '12345':
                # Connect the socket to the port where the server is listening
                server_address = (host, int(port))
                sock.connect(server_address)

                print('\n' * 50)
                tprint("Welcome!")

                # Send JSON command
                json_obj['command'] = 'join'
                json_str = json.dumps(json_obj)
                sock.sendall(json_str.encode())

                print("Connection to the Message Board Server is successful!")

                # Create threads
                send_thread = threading.Thread(target=send_json)
                listen_thread = threading.Thread(target=listen_for_messages)
                # Start threads
                send_thread.start()
                listen_thread.start()
                # Join threads
                send_thread.join()
                listen_thread.join()
            else:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

        elif len(command_list) != 3 and command != '/?':
            print("Error: Command parameters do not match or is not allowed.")

        elif command == '/leave' and len(command_list) == 1:
            print("Error: Disconnection failed. Please connect to the server first.")
            
        elif command == '/?' and len(command_list) == 1:
            print("Commands:")
            print("/join <host> <port>")
        else:
            print("Error: Command not found.")

if __name__ == '__main__':

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\n' * 50)
    tprint("Message Board")
    # Reprompt the user for input if the user enters an invalid command
    login()


