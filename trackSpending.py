
from useresapi import user_IDs
from inUtils import  posPutInt
#todo get user info
#todo create menu that chooses user
def makeSelection():
    return posPutInt('please enter a number from 1-5 ')
def chooseUser():
    ids=''
    selection=makeSelection()
    if  (selection ==1) :
        ids=user_IDs[0]
    elif (selection ==2):
        ids=user_IDs[1]
    elif (selection ==3):
        ids=user_IDs[2]
    elif (selection ==4):
        ids=user_IDs[3]
    elif (selection ==5):
        ids=user_IDs[4]
    else:
        print('please enter a valid selection')
        makeSelection()

    return ids
if __name__ == '__main__':
    ids=chooseUser()
    print(ids)
    print(user_IDs["Codes"])
# todo get  userID



#todo get user account info



#todo get mechid create an empty dictionary of merch id:totals


#todo loop user account info  and merch dictionary with conditional when a transactions merch code and transaction merch code are the same add purchase amount to values purchaseTotals={merchcode:total}

#todo create  variable TotalAmountSpent={k:sum(v) for k,v in purchaseTotals.items()}

#todo create dictionary that shows percentage spent on each item percentSpent={merchcode:percent%}

#todo create a dictionary  categories={categoryname: merchcode} create a menu funtion?

'''todo add new transaction variable newPurchase then select from categories menu  then push to purchaseTotals  [if k=[ k for k,v in categories] purchaseTotals.update(k=v+newPurchase) for k,v in purchaseTotals] '''

#todo display current account info purchase transaction categories percentages



