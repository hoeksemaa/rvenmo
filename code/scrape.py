from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
import pickle
import time
from os import path

def pickle_save(data, filepath):
    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def pickle_load(filepath):
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    handle.close()
    return data

class network():

    def __init__(self, args, client):
        pickle_path = args.path + "data/" + args.filename + ".pickle"
        if path.exists(pickle_path):
            self.data = pickle_load(pickle_path)
        else:
            self._init_data()
            self._seed(args, client)

    def _init_data(self):
        self.data = {}
        self.data["users"] = {}
        self.data["transactions"] = {}
        self.data["syncer"] = {
            "state": 0
            }

    def _add_user()

    def _seed(self, args, client):
        profile = client.user.get_my_profile(args.username)
        

def main(args):
    client     = Client(access_token=args.token)
    my_network = network(args, client)
    
if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", type=int, default=1, help="depth of friend search")
    parser.add_argument("-f", "--filename", type=str, required=True, help="filename of pickle storage object")
    parser.add_argument("-p", "--path", type=str, required=True, help="path to top-level directory")
    parser.add_argument("-t", "--token", type=str, required=True, help="venmo access token")
    parser.add_argument("-u", "--username", type=str, required=True, help="your username")
    main(args = parser.parse_args())
