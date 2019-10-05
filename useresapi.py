import requests
import operator
import datetime

apiKey = 'jYDXW9HlEAkNwEdd4MOCq9grb9UEhR8u'
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

# Breaking up grand list into dicts to sort individually.
for i in range(len(transactions)):
    postedAmountDict[i] = transactions[i][0]
    effectiveDateDict[i] = transactions[i][1]
    primaryIDDict[i] = transactions[i][2]

# Converting them to lists and sorting the appropriate one.
postedAmountList = []
for item in postedAmountDict:
    postedAmountList.append(postedAmountDict[item])
primaryIDList = []
for item in primaryIDDict:
    primaryIDList.append(primaryIDDict[item])
effectiveDateList = sorted(effectiveDateDict.items(), key=operator.itemgetter(1))

tempSortedDateDict = {}
tempSortedAmountDict = {}
tempSortedIDDict = {}

# Converting them back into dicts, and sorting the remaining list to match the other.
for i in range(len(effectiveDateList)):
    index = effectiveDateList[i]
    index = index[0]
    tempAmountValue = postedAmountList[index]
    tempIDValue = primaryIDList[index]
    tempSortedAmountDict[index] = tempAmountValue
    tempSortedIDDict[index] = tempIDValue
    tempSortedDateDict[i] = effectiveDateList[i][1]

# Converting them back into lists and sorting appropriate ones.
tempSortedDateList = []
for item in tempSortedDateDict:
    tempSortedDateList.append(tempSortedDateDict[item])
tempSortedAmountList = []
for item in tempSortedAmountDict:
    tempSortedAmountList.append(tempSortedAmountDict[item])
# Resetting the keys of the IDList
tempSortedIDList = []
for item in tempSortedIDDict:
    tempSortedIDList.append(tempSortedIDDict[item])
tempSortedIDDict.clear()
for i in range(len(tempSortedIDList)):
    tempSortedIDDict[i] = tempSortedIDList[i]
tempSortedIDList = sorted(tempSortedIDDict.items(), key=operator.itemgetter(1))

sortedAmountDict = {}
sortedDateDict = {}
sortedIDDict = {}

# Converting them back into dicts, and sorting the remaining list to match the other.
currentID = tempSortedIDList[0]
for i in range(len(tempSortedIDList)):
    index = tempSortedIDList[i]
    index = index[0]
    tempDateValue = tempSortedDateList[index]
    tempAmountValue = tempSortedAmountList[index]
    sortedDateDict[index] = tempDateValue
    sortedAmountDict[index] = tempAmountValue
    sortedIDDict[i] = tempSortedIDList[i][1]

# Converting them back into lists.
sortedAmountList = []
for item in sortedAmountDict:
    sortedAmountList.append(sortedAmountDict[item])
sortedDateList = []
for item in sortedDateDict:
    sortedDateList.append(sortedDateDict[item])
sortedIDList = []
for item in sortedIDDict:
    sortedIDList.append(sortedIDDict[item])

# Combining them back into a list of lists.
sortedTransactions = []
for i in range(len(sortedAmountDict)):
    sortedTransactions.append([sortedAmountList[i], sortedDateList[i], sortedIDList[i]])

#TODO count how many clients
#TODO break each client into lists
#TODO break into each week
#TODO count for each week
#TODO return to grand total list

#TODO REAL TIME grab totls for each week for each client and put them in a dict

lastID = sortedTransactions[0][2]
clients = 1

for item in sortedTransactions:
    if item[2] != lastID:
        lastID = item[2]
        clients +=1

totalTransactions = []
weeklyTransactions = []
currentID = sortedTransactions[0][2]
firstWeek = datetime.datetime.strptime(sortedTransactions[0][1], '%Y-%m-%d')
weeklyTotal = 0.0
week = 1

for transaction in sortedTransactions:
    currentWeek = datetime.datetime.strptime(transaction[1], '%Y-%m-%d')
    if currentID != transaction[2]:
        weeklyTransactions.append([week, weeklyTotal])
        totalTransactions.append([currentID, weeklyTransactions])
        currentID = transaction[2]
        weeklyTransactions.clear()
        firstWeek = datetime.datetime.strptime(transaction[1], '%Y-%m-%d')
        weeklyTotal = 0.0
        week = 1
    if currentWeek >= firstWeek + datetime.timedelta(days=(7*week)):
        weeklyTransactions.append([week, weeklyTotal])
        weeklyTotal = 0.0
        week += 1
    weeklyTotal += float(transaction[0])

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
print(totalDict)

# for total in totalDict:
#     #TODO determine how many weeks the user has been using this to save and multiply it by .002
#     percentToSave = .002
#     print('User: ' + total)
#     amount = float(totalDict[total]) * percentToSave
#     print('Amount to save: $' + str(round(amount, 2)))



