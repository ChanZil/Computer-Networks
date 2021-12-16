#   Ex. 2.7 template - protocol
#   Author: Chani Viner, 2021


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    cmd_list = data.rsplit(" ")
    list_of_cmd_0_param = ["TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT"]
    list_of_cmd_1_param = ["DIR", "DELETE", "EXECUTE"]
    list_of_cmd_2_param = ["COPY"]
    if cmd_list[0] in list_of_cmd_0_param and len(cmd_list) == 1:
        return True
    if cmd_list[0] in list_of_cmd_1_param and len(cmd_list) == 2:
        return True
    if cmd_list[0] in list_of_cmd_2_param and len(cmd_list) == 3:
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    data_length = str(len(data))
    msg = "0" * (4 - len(data_length)) + data_length + data
    return msg.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length_field = my_socket.recv(4)
    length_field = int(length_field.decode())
    if length_field == 0:
        return False, "Error"
    return True, my_socket.recv(length_field).decode()


