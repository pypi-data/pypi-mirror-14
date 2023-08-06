from Config import settings
import argparse
import getpass


def build_arg_parser():
    """
    Minimum args to connect to vCenter
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--host',
                        required=False,
                        default=settings['host'],
                        action='store',
                        help='vShere service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        required=False,
                        help='port to connect on')

    parser.add_argument('-u', '--user',
                        required=False,
                        action='store',
                        default=settings['user'],
                        help='Username to use when connecting')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        default=settings['password'],
                        help='Password to use when connecting to host')

    return parser


def prompt_for_password(args):
    """
    Prompts user for vCenter password if none was provided 
    with --password
    """
    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host'
        )

    return args


def get_args():
    """
    Builds parser and returns any added args
    """
    parser = build_arg_parser()
    args = parser.parse_args()
    return prompt_for_password(args)
