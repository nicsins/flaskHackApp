import requests
import operator
import datetime

apiKey = 'jYDXW9HlEAkNwEdd4MOCq9grb9UEhR8u'
header = {'apiKey' : apiKey}

users_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
user_IDs = []
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


def listsToDicts(orderedList, unorderedOneList, unorderedTwoList):
    unorderedOneDict = {}
    unorderedTwoDict = {}
    orderedDict = {}
    for i in range(len(orderedList)):
        index = orderedList[i]
        index = index[0]
        valueOne = unorderedOneList[index]
        valueTwo = unorderedTwoList[index]
        unorderedOneDict[index] = valueOne
        unorderedTwoDict[index] = valueTwo
        orderedDict[i] = orderedList[i][1]
    return unorderedOneDict, unorderedTwoDict, orderedDict


def dictToList(dictionary):
    list = []
    for item in dictionary:
        list.append(dictionary[item])
    return list


postedAmountDict = {}
effectiveDateDict = {}
primaryIDDict = {}

# Breaking up grand list into dicts to sort individually.
for i in range(len(transactions)):
    postedAmountDict[i] = transactions[i][0]
    effectiveDateDict[i] = transactions[i][1]
    primaryIDDict[i] = transactions[i][2]

# Converting them to lists and sorting the appropriate one.
postedAmountList, primaryIDList = dictToList(postedAmountDict), dictToList(primaryIDDict)
effectiveDateList = sorted(effectiveDateDict.items(), key=operator.itemgetter(1))

# Converting them back into dicts, and sorting the remaining list to match the other.
tempSortedAmountDict, tempSortedIDDict, tempSortedDateDict =\
    listsToDicts(effectiveDateList, postedAmountList, primaryIDList)

# Converting them back into lists and sorting appropriate ones.
tempSortedDateList, tempSortedAmountList = dictToList(tempSortedDateDict), dictToList(tempSortedAmountDict)
# Resetting the indices of the ID list
tempSortedIDList = dictToList(tempSortedIDDict)
tempSortedIDDict.clear()
for i in range(len(tempSortedIDList)):
    tempSortedIDDict[i] = tempSortedIDList[i]
tempSortedIDList = sorted(tempSortedIDDict.items(), key=operator.itemgetter(1))

# Converting them back into dicts, and sorting the remaining list to match the other.
sortedDateDict, sortedAmountDict, sortedIDDict =\
    listsToDicts(tempSortedIDList, tempSortedDateList, tempSortedAmountList)

# Converting them back into lists.
sortedAmountList, sortedDateList, sortedIDList =\
    dictToList(sortedAmountDict), dictToList(sortedDateDict), dictToList(sortedIDDict)

# Combining them back into a list of lists.
sortedTransactions = []
for i in range(len(sortedAmountDict)):
    sortedTransactions.append([sortedAmountList[i], sortedDateList[i], sortedIDList[i]])

# Getting weekly transaction figures with proper percent of spent to be saved.
totalTransactions = {}
weeklyTransactions = []
emptyTransactions = []
currentID = sortedTransactions[0][2]
firstWeek = datetime.datetime.strptime(sortedTransactions[0][1], '%Y-%m-%d')
weeklyTotal = 0.0
week = 1

for transaction in sortedTransactions:
    currentWeek = datetime.datetime.strptime(transaction[1], '%Y-%m-%d')
    if currentID != transaction[2]:
        weeklyTransactions.append([week, weeklyTotal, (weeklyTotal * .002 * week)])
        totalTransactions[currentID] = weeklyTransactions
        currentID = transaction[2]
        weeklyTransactions = []
        firstWeek = datetime.datetime.strptime(transaction[1], '%Y-%m-%d')
        weeklyTotal = 0.0
        week = 1
    if currentWeek >= firstWeek + datetime.timedelta(weeks=week):
        weeklyTransactions.append([week, weeklyTotal, (weeklyTotal * .002 * week)])
        weeklyTotal = 0.0
        week += 1
    weeklyTotal += float(transaction[0])

# Displaying our fun noise.
print()
for total in totalTransactions:
    totalSpent = 0.0
    totalSaved = 0.0
    for transaction in totalTransactions[total]:
        totalSpent += transaction[1]
        totalSaved += transaction[2]
    print('Account number:\t' + total)
    print('Total spent:\t$' + str(round(totalSpent, 2)))
    print('Total saved:\t$' + str(round(totalSaved, 2)))
    print('Percent saved:\t' + str(round(totalSaved / totalSpent * 100, 3)) + '%')
    print()
