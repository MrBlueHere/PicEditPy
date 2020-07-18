import sys
from command import *


def main():
    args = sys.argv
    try:
        apply_args(args)
    except Exception as ex:
        print(ex)
        print_help_msg()


if __name__ == '__main__':
    main()
