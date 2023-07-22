from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
import pickle
import time
from os import path

# file parsing is for the weak
source_username = "John-Hoeksema-2"
source_id = 2304882732171264893
pickle_filename = "data.pickle"
data_path = "/Users/johnhoeksema/rvenmo/data/"

def pickle_save(data, filepath):
    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

def pickle_load(filepath):
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    handle.close()
    return data

class venmo_network():

    def __init__(self):
        if path.exists(data_path + pickle_filename):
            self.data = pickle_load(data_path + pickle_filename)
        else:
            self._init_data()
            self._init_john()

    def _init_data(self):
        self.data = {}
        self.data["syncer"] = {
            "depth": 0,
            "friends_unprocessed": [],
            "transactions_unprocessed": []
        }
        self.data["users"] = {}

    def _init_john(self):
        self.data["users"][source_id] = {
            "first name":             "John",
            "last name":              "Hoeksema",
            "username":               "John-Hoeksema-2",
            "friends_processed":      False,
            "transactions_processed": False 
        }
        self.data["syncer"]["friends_unprocessed"] = [source_id]

    def _save(self):
        pickle_save(self.data, data_path + pickle_filename)

    def print_data(self):
        print(self.data)

    def _add_user(self, user):
        if user.id not in self.data["users"]:
            self.data["users"][user.id] = {
                "first name":             user.first_name,
                "last name":              user.last_name,
                "username":               user.username,
                "friends_processed":      False,
                "transactions_processed": False
            }

    def get_friends_unprocessed_userids(self):
        ids = []
        for userid in self.data["users"]:
            if self.data["users"][userid]["friends_processed"] == False:
                ids.append(userid)
        return ids

    def get_users(self, args, client):

        while self.data["syncer"]["depth"] < args.depth:

            print("Getting friends of users at depth {}".format(self.data["syncer"]["depth"]))
            num = len(self.data["syncer"]["friends_unprocessed"])
            count = 0

            for userid in self.data["syncer"]["friends_unprocessed"]:

                print(userid)

                # get users friends
                friends = client.user.get_user_friends_list(userid)
                # add users friends
                for friend in friends:
                    self._add_user(friend)
                # save
                self._save()
                # mark the user as processed
                self.data["users"][userid]["friends_processed"] = True
                # remove the processed id
                self.data["syncer"]["friends_unprocessed"].remove(userid)
                """
                this ordering with flexibe methods guarantees maximum data saved
                along with easily picking up where the program left off;
                reason is to work around venmo error code 401: too many requests
                """

                print("{}/{}".format(count, num))
                count += 1

            # reset unprocessed ids
            self.data["syncer"]["friends_unprocessed"] = self.get_friends_unprocessed_userids()
            # increment depth
            self.data["syncer"]["depth"] += 1
            self._save()

        print("Friends gotten to set depth of {}.".format(args.depth))

def main(args):
    
    client  = Client(access_token=args.token)
    network = venmo_network()
    #network.get_users(args, client)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--token", type=str, required=True, help="venmo access token")
    parser.add_argument("-d", "--depth", type=int, default=1, help="The depth of the friend search")

    main(args = parser.parse_args())
