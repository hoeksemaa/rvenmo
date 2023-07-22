from argparse import ArgumentParser
from venmo_api import Client
import networkx as nx
import pprint
import pickle
import time
from os import path

source_username = "John-Hoeksema-2"
source_id = 2304882732171264893
pickle_filename = "data.pickle"
gexf_filename = "data.gexf"
data_path = "/Users/johnhoeksema/rvenmo/data/"

token = "7f002c4b3504471552eb1da03cd5ce0656063d0805fee70990db692d995f9577" 
client  = Client(access_token=token)
friends = client.user.get_user_friends_list(source_id)
length = len(friends)
count = 0
for f in friends: 
    try:
        print("{}/{}   {}   {}".format(count, length, f.username, len(client.user.get_user_transactions(f.id))))
    except Exception as e: 
        print(e)
        print("Request failed, waiting 5 minutes...")
        time.sleep(60)
        print("{}/{}   {}   {}".format(count, length, f.username, len(client.user.get_user_transactions(f.id))))

    count += 1

print("all friends complete!")
