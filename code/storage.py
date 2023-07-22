from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
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
        self.data["transactions"] = {}

    def get_users(self):
        return self.data["users"]

    def add_user(self, user):
        if user.id not in self.data["users"]:
            self.data["users"][user.id] = {
                "first name": user.first_name,
                "last name":  user.last_name,
                "username":   user.username
                }

    def user_is_added(self, userid):
        if userid in self.data["users"]:
            return True
        else:
            return False

    def print_users(self):
        pprint.PrettyPrinter(indent=4).pprint(self.data["users"])

    def get_transactions(self):
        return self.data["transactions"]

    def add_transaction(self, transaction):
        actor_username = transaction.actor.username
        target_username = transaction.target.username

        first_username = min(actor_username, target_username)
        second_username = max(actor_username, target_username)

        if first_username not in self.data["transactions"]:
            self.data["transactions"][first_username] = {}

        if second_username not in self.data["transactions"][first_username]:
            self.data["transactions"][first_username][second_username] = 0

        self.data["transactions"][first_username][second_username] += 1

    def print_transactions(self):
        pprint.PrettyPrinter(indent=4).pprint(self.data["transactions"])

def main(args):
    
    client = Client(access_token=access_token)
    data   = venmo_data()

    johns_info    = client.user.get_my_profile()
    data.add_user(johns_info)

    johns_friends = client.user.get_user_friends_list(johns_info.id)
    for f in johns_friends:
        data.add_user(f)
    
    num_frens = len(johns_friends)
    count = 0
    for f in johns_friends:
        transactions = client.user.get_user_transactions(f.id)
        for t in transactions:
            if t.actor and t.target:
                if data.user_is_added(t.actor.id) and data.user_is_added(t.target.id):
                    data.add_transaction(t)
                    print("{} --> {}".format(t.actor.username, t.target.username))
                    print(t)
                    print()

        count += 1
        print("COMPLETION")
        print("{} / {}".format(count, num_frens))
        print()
        time.sleep(10)

    data.print_users()
    data.print_transactions()

if __name__=='__main__':
    parser = ArgumentParser()
    
    main(args = parser.parse_args())
