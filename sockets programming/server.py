#   Ex. 2.7 template - server side
#   Author: Chani Viner, 2021
#   Modified for Python 3, 2020

import socket
import protocol
import glob
import os
import shutil
import subprocess
import pyautogui

IP = "0.0.0.0"
PHOTO_PATH = r'C:\Networks\work\screen.JPEG'  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    param_list = cmd.rsplit(" ")
    my_cmd = param_list.pop(0)
    if protocol.check_cmd(cmd):
        # Then make sure the params are valid
        if param_list:
            if not os.path.exists(param_list[0]):
                return False, my_cmd, param_list
        return True, my_cmd, param_list
    return False, my_cmd, param_list


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = ""
    if command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = "Screenshot saved"
    elif command == "SEND_PHOTO":
        photo = open(PHOTO_PATH, 'rb')
        response = str(os.stat(PHOTO_PATH).st_size)  # save the length of the photo
    elif command == "DIR":
        my_directory = params[0] + r'\*.*'
        files_list = glob.glob(my_directory)
        response = ', '.join(files_list)
    elif command == "DELETE":
        os.remove(params[0])
        response = "File removed"
    elif command == "COPY":
        shutil.copy(params[0], params[1])
        response = "Copy succeeded"
    elif command == "EXECUTE":
        subprocess.call(params[0])
        response = "Execution succeeded"
    elif command == "EXIT":
        response = "Exit"
    else:
        response = "Error"
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, 8820))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                response = handle_client_request(command, params)
                packet = protocol.create_msg(response)
                client_socket.send(packet)
                if command == 'SEND_PHOTO':  # need to save the photo itself after sending the length of the photo
                    photo = open(PHOTO_PATH, 'rb')
                    photo_size = os.stat(PHOTO_PATH).st_size
                    while photo_size > 0:
                        if photo_size > 9999:
                            read_size = 9999
                        else:
                            read_size = photo_size
                        photo_read = photo.read(read_size)
                        client_socket.send(photo_read)
                        photo_size -= read_size
                    photo.close()
                if command == 'EXIT':
                    break
            else:
                response = 'Bad command or parameters'
                packet = protocol.create_msg(response)
                client_socket.send(packet)
        else:
            response = 'Packet not according to protocol'
            packet = protocol.create_msg(response)
            client_socket.send(packet)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
