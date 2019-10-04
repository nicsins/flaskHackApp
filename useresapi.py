import requests
import os

apiKey = os.environ['APIKEY']

users_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
user_IDs = []

header = {'apiKey' : apiKey}
response = requests.get(users_URL,headers = header).json()
user_list = response['UserList']
for user in user_list:
    user_IDs.append(user['LegalParticipantIdentifier'])

data = {'LegalParticipantIdentifier': user_IDs[0]}

accounts_url = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
account_deets = []
for id in user_IDs:
    data = {'LegalParticipantIdentifier': id}
    account_deets.append(requests.post(accounts_url, headers= header, data= data).json())


company_ID = []
product_code = []
primary_ID = []

for account in account_deets:

    company_ID.append(account['AccessibleAccountDetailList'][0]['OperatingCompanyIdentifier'])
    product_code.append(account['AccessibleAccountDetailList'][0]['ProductCode'])
    primary_ID.append(account['AccessibleAccountDetailList'][0]['PrimaryIdentifier'])


transactions_url = 'https://alpha-api.usbank.com/innovations/v1/account/transactions'
transaction_data = []
for i in range(len(company_ID)):
    company_data = {'OperatingCompanyIdentifier': company_ID[i], 'ProductCode': product_code[i], 'PrimaryIdentifier': primary_ID[i]}
    transaction_data.append(requests.post(transactions_url, headers=header, data=company_data).json())

transactions = []

for transaction in transaction_data:

    try:
        for i in range(len(transaction)):
            for j in range(len(transaction['TransactionList'])):
                tempTransaction = [transaction['TransactionList'][j]['PostedAmount'],
                                   transaction['TransactionList'][j]['EffectiveDate'],
                                   transaction['TransactionList'][j]['AccountPrimaryIdentifier']]
                transactions.append(tempTransaction)
    except KeyError:
        print("No transactions for this user.")

for transaction in transactions:
    # print('Transaction: ' + str(transaction))
    amount = float(transaction[0]) * .002
    # print('Amount to be saved: $' + str(round(amount, 2)))

temporaryID = transactions[0][2]
temporaryTotal = 0.0
totalDict = {}

for transaction in transactions:
    if transaction[2] != temporaryID:
        totalDict[temporaryID] = temporaryTotal
        temporaryID = transaction[2]
        temporaryTotal = 0.0
    temporaryTotal += float(transaction[0])
totalDict[temporaryID] = temporaryTotal

print(totalDict)
