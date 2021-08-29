#!/usr/bin/env python3
import socket
import sys
import json
import time
import re

_seq = 1


def send_request(s, msg_or_function):
    global _seq
    _seq += 1
    if callable(msg_or_function):
        msg = msg_or_function()
    else:
        # print('not function but msg : ', msg_or_function[0])
        msg = msg_or_function
    msg["seq"] = _seq
    payload = json.dumps(msg, indent=2)
    full_msg = f"Content-Length: {len(payload)}\r\n\r\n{payload}"
    print("---------------------------")
    print("sending : ", msg["command"])
    print(full_msg)
    print()
    s.sendall(full_msg.encode())


def initialize_request():
    return {
        "seq": 0,
        "type": "request",
        "command": "initialize",
        "arguments": {
            "clientID": "rcid",
            "clientName": "recipe_creator_name",
            "adapterID": "debugpy",
        },
    }


def launch():
    return {
        "seq": 0,
        "type": "request",
        "command": "launch",
        "arguments": {
            "noDebug": False,
            "__restart": None,
        },
    }


def attach():
    return {
        "seq": 0,
        "type": "request",
        "command": "attach",
        "arguments": {"__restart": None},
    }


def set_break_points():
    return {
        "seq": 0,
        "type": "request",
        "command": "setBreakpoints",
        "arguments": {
            "source": {
                "path": "/Users/vine/prj/py-debug/csharp-debugpy/test-py-debugee/pydebuggee/api/__init__.py",
            },
            "breakpoints": [{"line": 2}],
        },
    }


def configuration_done():
    return {
        "seq": 0,
        "type": "request",
        "command": "configurationDone",
        "arguments": {},
    }


def stack_trace():
    return {
        "seq": 0,
        "type": "request",
        "command": "stackTrace",
        "arguments": {
            "threadId": 1,
        },
    }


def scopes():
    return {
        "seq": 0,
        "type": "request",
        "command": "scopes",
        "arguments": {"frameId": 2},
    }


def variables(variables_reference):
    return {
        "seq": 0,
        "type": "request",
        "command": "variables",
        "arguments": {"variablesReference": variables_reference},
    }


def continue_request(threadId=1):
    return {
        "seq": 0,
        "type": "request",
        "command": "continue",
        "arguments": {"threadId": threadId},
    }


def next_request(threadId=1):
    return {
        "seq": 0,
        "type": "request",
        "command": "next",
        "arguments": {
            "threadId": threadId
        }
    }


def send_msg(s, msg):
    print("sending : ")
    print(msg)
    print()
    s.sendall(msg.encode())


def print_response(data):
    # print(bytes.decode(data, 'utf-8'))
    # print()
    print("response : ")
    print(data)
    print()


def recv_timeout(s, timeout=1):
    global _seq

    # make socket non blocking
    s.setblocking(0)

    # total data partwise in an array
    total_data = []
    data = ""

    # beginning time
    begin = time.time()
    while 1:
        # if you got some data, then break after timeout
        if total_data and time.time() - begin > timeout:
            break

        # if you got no data at all, wait a little longer, twice the timeout
        elif time.time() - begin > timeout * 2:
            break

        # recv something
        try:
            data = s.recv(8192)
            if data:
                total_data.append(bytes.decode(data))
                # change the beginning time for measurement
                begin = time.time()
            else:
                # sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    # join all parts to make final string
    result = "".join(total_data)
    splitted_result = list(
        filter(
            lambda s: len(s) > 0,
            re.sub("Content-Length: [0-9]+\r\n\r\n", "_@sep@_", result).split(
                "_@sep@_"
            ),
        )
    )
    msg_list = []
    json_list = []
    for r in splitted_result:
        msg = json.loads(r)
        msg_list.append(msg)
        print_response(json.dumps(msg, indent=2))
        _seq += 1
    return msg_list


def run(s: socket):

    input = sys.stdin.readline().strip()
    while len(input) > 0:
        if input == "init":
            send_request(s, initialize_request)
            recv_timeout(s)
            # elif input == "2":
            send_request(s, attach)
            recv_timeout(s)
            # elif input == "3":
            send_request(s, set_break_points)
            recv_timeout(s)
        elif input == "done":
            send_request(s, configuration_done)
            recv_timeout(s)
        elif input == "st":
            send_request(s, stack_trace)
            recv_timeout(s)
        elif input.startswith("scopes"):
            send_request(s, scopes)
            recv_timeout(s)
        elif input.startswith("var"):
            variables_reference = int(input.split(" ")[1])
            send_request(s, variables(variables_reference))
            recv_timeout(s)
        elif input == "n":
            send_request(s, next_request(threadId=1)) # main thread ?!
            recv_timeout(s)
        elif input == "c":
            send_request(s, continue_request(threadId=1)) # main thread ?!
            recv_timeout(s)
        else:
            print("@@@ UNKNONW COMMAND ")

        input = sys.stdin.readline().strip()


def main():
    print('len = ', len(sys.argv))
    port = sys.argv[1] if len(sys.argv) > 1 else 56789
    print('using port : ', port)
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = port  # The port used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("connected!")
        response = recv_timeout(s)
        print_response(json.dumps(response, indent=2))

        run(s)


if __name__ == "__main__":
    main()
