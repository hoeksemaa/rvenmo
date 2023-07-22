from venmo_api import Client

access_token = "6c5e1837d1388a3b2e836e3d43327cf535d4f64641d9dafba83a6a93e096d4d9"
venmo = Client(access_token=access_token)

kelly_username = "John-Hoeksema-2"
kelly_info = venmo.user.get_my_profile(kelly_username)
print(kelly_info)
kelly_friends = venmo.user.get_user_friends_list(kelly_info.id)
for f in kelly_friends:
    print(f)
