from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
import pickle
import time

# Globals (file parsing is for the weak)
access_token = "6c5e1837d1388a3b2e836e3d43327cf535d4f64641d9dafba83a6a93e096d4d9"
source_username = "John-Hoeksema-2"


class venmo_data():

    def __init__(self):
        self._init_data()

    def _init_data(self):
        self.data = {}
        self.data["users"] = {}

    def get_users(self):
        return self.data["users"]

    def add_user(self, user):
        if user.id not in self.data["users"]:
            self.data["users"][user.id] = {
                "first name": user.first_name,
                "last name":  user.last_name,
                "username":   user.username,
                "friends_processed": False,
                "transactions_processed": False
                }

    def set_friends_processed(self, userid, truth):
        if userid in self.data["users"]:
            self.data["users"][userid]["friends_processed"] = truth
        else:
            print("user with user id: {} not found.".format(userid))
            print("failed to set condition: {}.".format(userid))

    def get_user_ids_with_unprocessed_friends(self):
        ids = []
        for userid in self.data["users"]:
            if self.data["users"][userid]["friends_processed"] == False:
                ids.append(userid)
        return ids

def get_users(args, client, data):

    johns_info = client.user.get_my_profile()
    data.add_user(johns_info)
    
    for n in range(args.depth):
        ids = data.get_user_ids_with_unprocessed_friends()

        for i in ids:
            friends = client.user.get_user_friends_list(i)
            for f in friends:
                data.add_user(f)
            data.set_friends_processed(i, True)
 
def main(args):
    
    client = Client(access_token=access_token)
    data   = venmo_data()

    get_users(args, client, data)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", type=int, default=1, help="The depth of the friend search")

    main(args = parser.parse_args())
