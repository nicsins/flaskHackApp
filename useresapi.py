import requests
import os
import operator

apiKey = os.environ['APIKEY']

users_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
user_IDs = []

header = {'apiKey' : apiKey}
response = requests.get(users_URL, headers=header).json()
user_list = response['UserList']
for user in user_list:
    user_IDs.append(user['LegalParticipantIdentifier'])

data = {'LegalParticipantIdentifier': user_IDs[0]}

accounts_url = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
account_deets = []
for id in user_IDs:
    data = {'LegalParticipantIdentifier': id}
    account_deets.append(requests.post(accounts_url, headers=header, data=data).json())


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
    #TODO add something to only pull in last week or whatever
    try:
        for i in range(len(transaction)):
            for j in range(len(transaction['TransactionList'])):

                try:
                    tempTransaction = [transaction['TransactionList'][j]['PostedAmount'],
                                       transaction['TransactionList'][j]['EffectiveDate'],
                                       transaction['TransactionList'][j]['AccountPrimaryIdentifier'],
                                       transaction['TransactionList'][j]['TransactionDescription']]
                    transactions.append(tempTransaction)
                except KeyError:
                    tempTransaction = [transaction['TransactionList'][j]['PostedAmount'],
                                       transaction['TransactionList'][j]['EffectiveDate'],
                                       transaction['TransactionList'][j]['AccountPrimaryIdentifier']]

                    transactions.append(tempTransaction)
    except KeyError:
        print("No transactions for this user.")

postedAmountDict = {}
effectiveDateDict = {}
primaryIDDict = {}

for i in range(len(transactions)):
    postedAmountDict[i] = transactions[i][0]
    effectiveDateDict[i] = transactions[i][1]
    primaryIDDict[i] = transactions[i][2]
tempSortedDateList = sorted(effectiveDateDict.items(), key=operator.itemgetter(1))
print(tempSortedDateList)

tempSortedDateDict = {}
tempSortedAmountDict = {}
tempSortedIDDict = {}

for i in range(len(tempSortedDateList)):
    index = tempSortedDateList[i]
    index = index[0]
    tempAmountValue = postedAmountDict[index]
    tempIDValue = primaryIDDict[index]
    tempSortedAmountDict[index] = tempAmountValue
    tempSortedIDDict[index] = tempIDValue
    tempSortedDateDict[index] = tempSortedDateList[index]

tempSortedIDList = sorted(tempSortedIDDict.items(), key=operator.itemgetter(1))

sortedAmountDict = {}
sortedDateDict = {}
sortedIDDict = {}

for i in range(len(tempSortedIDList)):
    index = tempSortedIDList[i]
    index = index[0]
    tempDateValue = tempSortedDateDict[index]
    tempAmountValue = tempSortedAmountDict[index]
    sortedDateDict[index] = tempDateValue
    sortedAmountDict[index] = tempAmountValue
    sortedIDDict[index] = tempSortedIDList[index]

sortedTransactions = []

for i in range(len(sortedAmountDict)):
    sortedTransactions.append([sortedAmountDict[i][1], sortedDateDict[i][1], sortedIDDict[i][1]])

print(sortedTransactions)

#TODO count how many clients
#TODO break each client into lists
#TODO break into each week
#TODO count for each week
#TODO return to grand total list

temporaryID = transactions[0][2]
temporaryTotal = 0.0
totalDict = {}

for transaction in transactions:
    if transaction[2] != temporaryID:
        totalDict[temporaryID] = temporaryTotal
        temporaryID = transaction[2]
        temporaryTotal = 0.0
        #print(transaction)
    temporaryTotal += float(transaction[0])
totalDict[temporaryID] = temporaryTotal


for total in totalDict:
    #TODO determine how many weeks the user has been using this to save and multiply it by .002
    percentToSave = .002
    print('User: ' + total)
    amount = float(totalDict[total]) * percentToSave
    print('Amount to save: $' + str(round(amount, 2)))



