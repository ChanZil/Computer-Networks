#   Ex. 2.7 template - client side
#   Author: Chani Viner, 2021
#   Modified for Python 3, 2020


import socket
import protocol


IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved:
SAVED_PHOTO_LOCATION = r'C:\Networks\work\copy_screen.JPEG'


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    if cmd != "SEND_PHOTO":
        valid_protocol, response = protocol.get_msg(my_socket)
        print(response)
    else:
        length_field = my_socket.recv(4)
        length_field = int(length_field.decode())
        photo_size = my_socket.recv(length_field)
        photo_size = int(photo_size.decode())
        saved_photo = open(SAVED_PHOTO_LOCATION, 'wb')
        while photo_size > 0:
            if photo_size > 9999:
                read_size = 9999
            else:
                read_size = photo_size
            photo_write = my_socket.recv(read_size)
            saved_photo.write(photo_write)
            photo_size -= read_size
        saved_photo.close()


def main():
    # open socket with the server

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, 8820))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()