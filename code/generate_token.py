from venmo_api import Client
from argparse import ArgumentParser

def main(args):
    access_token = Client.get_access_token(username=args.email, password=args.password)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--password", type=str, required=True, help="your venmo account password")
    parser.add_argument("-e", "--email", type=str, required=True, help="your venmo account email")
    main(args = parser.parse_args())
