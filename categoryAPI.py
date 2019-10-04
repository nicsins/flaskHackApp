import requests
import os

apiKey = 'API_KEY'

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
company_ID = []
product_code= []
primary_ID = []

for account in account_deets:
    print(account['AccessibleAccountDetailList'][0])
    company_ID.append(account['AccessibleAccountDetailList'][0]['OperatingCompanyIdentifier'])
    product_code.append(account['AccessibleAccountDetailList'][0]['ProductCode'])
    primary_ID.append(account['AccessibleAccountDetailList'][0]['PrimaryIdentifier'])

print (company_ID)
print(product_code)
print(primary_ID)

# Search based on categroy
CATEGORY_URL = 'https://alpha-api.usbank.com/innovations/v1/codes'

category_list = list()

#category_list.append(requests.post(CATEGORY_URL, headers=header).json())
print("ok")
print(requests.get(CATEGORY_URL, headers=header).json())