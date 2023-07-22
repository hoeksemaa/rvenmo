from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
import pickle
import time
from os import path

# file parsing is for the weak
# lmaoooooooooooooo jk?
source_username = "John-Hoeksema-2"
source_id = 2304882732171264893
pickle_filename = "data.pickle"
gexf_filename = "data.gexf"
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

def gexf_save(graph_dict, filepath):
    G = nx.DiGraph()
    for actor in graph_dict:
        for target in graph_dict[actor]:
            G.add_edge(actor, target, weight=graph_dict[actor][target])
    nx.write_gexf(G, filepath)

class venmo_network():

    def __init__(self, client):
        if path.exists(data_path + pickle_filename):
            print("START: Initializing from {}...".format(data_path + pickle_filename))
            self.data = pickle_load(data_path + pickle_filename)
        else:
            print("START: Initializing fresh...")
            self._init_data()
            self._get_users(client)
        print("COMPLETE: Initialized.")
        print()

    def _init_data(self):
        self.data = {}
        self.data["users"] = {}
        self.data["transactions"] = {}

    def _save(self):
        pickle_save(self.data, data_path + pickle_filename)

    def save(self):
        print("START: Saving to .gexf...")
        gexf_save(self.data["transactions"], data_path + gexf_filename)
        print("COMPLETE: Saved.")
        print()

    def _add_user(self, user):
        if user.username not in self.data["users"]:
            self.data["users"][user.username] = {
                "id": user.id,
                "first name": user.first_name,
                "last name": user.last_name,
                "processed": False
            }

    def _get_users(self, client):
        print(" > START: Getting users...")
        # add john
        john = client.user.get_my_profile()
        self._add_user(john)

        # add john friends
        users = client.user.get_user_friends_list(self.data["users"][source_username]["id"])
        [self._add_user(user) for user in users]
        print(" > COMPLETE: Users gotten.")
        print()

    def _is_not_processed(self, username):
        if self.data["users"][username]["processed"] == False:
            return True
        else:
            return False

    def _is_valid_transaction(self, transaction):
        if transaction.actor and transaction.target:
            return True
        else:
            return False

    def _count_processed_users(self):
        return sum(user_data["processed"] == True for user_data in self.data["users"].values())

    def get_transactions(self, client):
        print("START: Getting transactions...")

        num_users = len(self.data["users"])
        for username in filter(self._is_not_processed, self.data["users"]):
            
            # get user transactions
            transactions = client.user.get_user_transactions(self.data["users"][username]["id"]) 
            for transaction in filter(self._is_valid_transaction, transactions):

                actor_u = transaction.actor.username
                target_u = transaction.target.username

                # update transaction user details
                if actor_u not in self.data["transactions"]:
                    self.data["transactions"][actor_u] = {}
                if target_u not in self.data["transactions"][actor_u]:
                    self.data["transactions"][actor_u][target_u] = 0

                # update transaction count
                self.data["transactions"][actor_u][target_u] += 1

            # mark username as processed
            self.data["users"][username]["processed"] = True

            # save network data
            self._save()

            print(" > {}/{} users complete.".format(self._count_processed_users(), num_users))
            time.sleep(1)
        print("COMPLETE: Transactions gotten.")

def main(args):
    
    client  = Client(access_token=args.token)

    network = venmo_network(client)
    network.get_transactions(client)
    network.save()

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--token", type=str, required=True, help="venmo access token")

    main(args = parser.parse_args())
