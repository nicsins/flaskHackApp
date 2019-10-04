import requests
import os

apiKey = os.environ['APIKEY']

users_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
user_IDs = []

header = {'apiKey' : apiKey}
response = requests.get(users_URL,headers = header).json()
user_list = response['UserList']
for user in user_list:
    print(user)
    user_IDs.append(user['LegalParticipantIdentifier'])

print(user_IDs[0])
data = {'LegalParticipantIdentifier': user_IDs[0]}

accounts_url = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
account_deets = []
for id in user_IDs:
    data = {'LegalParticipantIdentifier': id}
    account_deets.append(requests.post(accounts_url, headers= header, data= data).json())

print(account_deets)

for account in account_deets:
    print(account)