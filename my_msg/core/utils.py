def get_message(open_socket, CONF, COD):
    response = open_socket.recv(CONF)
    if isinstance(response, bytes):
        decoded_data = response.decode(COD)
        return decoded_data
    raise ValueError

def send_message(message, COD):
    response = message.encode(COD)
    return response