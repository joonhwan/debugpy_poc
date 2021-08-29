from debugpy.launcher import connect


def main():

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 56790  # The port used by the server

    connect()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("connected!")
        response = recv_timeout(s)
        print_response(response)

        run(s)


if __name__ == "__main__":
    main()
