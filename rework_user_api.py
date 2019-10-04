import requests
import os


class UserApi:
    """
    Users:
    get_user_list = > returns all users
    """
    def __init__(self, api_key, user_id=None):
        self.api_key = api_key
        self.user_id = user_id

        self.USER_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
        self.ACCOUNTS_URL = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
        self.CATEGORY_URL = 'https://alpha-api.usbank.com/innovations/v1/codes'
        # All user list
        self.user_dict = []
        # User Dictionary

    def get_users_list(self):
        all_users_response = requests.get(self.USER_URL, headers={'apiKey': self.api_key}).json()
        list_of_users = all_users_response['UserList']
        for each_user in list_of_users:
            self.user_dict.append(each_user)
        print(self.user_dict)
        self.get_user_account_details()

    def get_user_account_details(self):
        if len(self.user_dict) == 0:
            print(">> No User")

UserApi("YOUR API KEY").get_users_list()
