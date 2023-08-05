import sys
import argparse
from action import ActionManager

import config
a = config.Config()

SERVICES = ('iaas',)


def check_argument(args):
    service = ''
    usage = ''
    if len(args) < 3:
        if len(args) < 2:
            usage = 'Please input service'
        else:
            service = args[1]
            usage = 'Please input action [command <service> <action> [params]]'
        parser = argparse.ArgumentParser(
            prog='qingcloud %s' % service,
            usage=usage)
        parser.print_help()
        sys.exit(-1)


def get_action(service, action):
    if service == 'iaas':
        return ActionManager.get_action(action)
    else:
        return 1001


def main():
    args = sys.argv
    check_argument(args)
    action = get_action(args[1], args[2])
    if action:
        if isinstance(action, int):
            print args[2] + ' service is Invalid'
        else:
            action.main(args[3:])
    else:
        print args[2] + ' command is Invalid'

if __name__ == '__main__':
    main()
