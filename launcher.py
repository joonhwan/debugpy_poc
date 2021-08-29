import sys
import signal
from debugpy import launcher
from debugpy.common import log
from debugpy.launcher import debuggee


def main():
    log.to_file('launcher.log')
    log.describe_environment("debugpy.launcher startup environment:")

    print('@@@ 1')
    if sys.platform == "win32":
        # For windows, disable exceptions on Ctrl+C - we want to allow the debuggee
        # process to handle these, or not, as it sees fit. If the debuggee exits
        # on Ctrl+C, the launcher will also exit, so it doesn't need to observe
        # the signal directly.
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Everything before "--" is command line arguments for the launcher itself,
    # and everything after "--" is command line arguments for the debuggee.
    log.info("sys.argv before parsing: {0}", sys.argv)
    sep = sys.argv.index("--")
    launcher_argv = sys.argv[1:sep]
    sys.argv[:] = [sys.argv[0]] + sys.argv[sep + 1 :]
    log.info("sys.argv after patching: {0}", sys.argv)

    print('@@@ 2')
    # The first argument specifies the host/port on which the adapter is waiting
    # for launcher to connect. It's either host:port, or just port.
    adapter = launcher_argv[0]
    host, sep, port = adapter.partition(":")
    if not sep:
        host = "127.0.0.1"
        port = adapter
    port = int(port)

    print('@@@ 3')
    launcher.connect(host, port)
    print('@@@ 4')
    launcher.channel.wait()
    launcher.channel.send_request('initialize')
    launcher.channel.wait()
    launcher.channel.send_request('launch')
    launcher.channel.wait()

    
    print('@@@ 5')
    
    print('@@@ after wait. ')
    if debuggee.process is not None:
        sys.exit(debuggee.process.returncode)
    else:
        print('ohohoho : ', debuggee.process)


if __name__ == "__main__":
    main()