from pydebuggee.api import greet
from pydebuggee.api.operation import show

def main():
    msg = greet('joonhwan')
    show(msg)

if __name__ == '__main__':
    main()    

