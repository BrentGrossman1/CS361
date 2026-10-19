
def encode_data(message, value):
    byte_array = bytearray()

    msg_bytes = message.encode()
    value_bytes = value.to_bytes(4, "big", signed=True)
    total_message_length = 2 + len(msg_bytes + value_bytes)
    total_length_bytes = total_message_length.to_bytes(2, "big")

    byte_array += total_length_bytes
    byte_array += msg_bytes
    byte_array += value_bytes

    return byte_array


def decode_data(data):
    total_message_length = int.from_bytes(data[0:2], "big")
    message_length = total_message_length - 6

    message_bytes = data[2:2 + message_length]
    value_bytes = data[2 + message_length:2 + message_length + 4]

    message = message_bytes.decode()
    value = int.from_bytes(value_bytes, "big", signed=True)

    return (message, value)


def main():
    encoded = encode_data("Hello there, General Kenobi!", -513)
    print(decode_data(encoded))

if __name__ == "__main__":
    main()