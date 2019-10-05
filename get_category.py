import requests
import os
import random
import ast


class UserApi:
    """Can provide data about all user or about specific person."""

    def __init__(self, api_key, user_id=None):
        self.api_key = api_key
        self.api_key = {"apiKey": api_key}
        self.user_id = user_id

        self.USER_URL = 'https://alpha-api.usbank.com/innovations/v1/users'
        self.ACCOUNTS_URL = 'https://alpha-api.usbank.com/innovations/v1/user/accounts'
        self.TRANSACTION_URL = 'https://alpha-api.usbank.com/innovations/v1/account/transactions'
        self.SINGE_CATEGORY_URL = 'https://alpha-api.usbank.com/innovations/v1/codes/'
        # All user list
        self.user_dict_list = []
        # User Dictionary
        self.final_dict = dict()

    def get_users_list(self):
        if self.user_id is None:
            all_users_response = requests.get(self.USER_URL, headers=self.api_key).json()
            list_of_users = all_users_response['UserList']
            for each_user in list_of_users:
                self.user_dict_list.append(each_user)
        else:
            self.user_id = {'LegalParticipantIdentifier': str(self.user_id)}

        self.get_user_account_details()

    def get_user_account_details(self):
        temp_list = []

        if self.user_id is None:
            for i in range(len(self.user_dict_list)):
                temp_list.append(self.user_dict_list[i])
                get_account_request = requests.post(self.ACCOUNTS_URL, headers=self.api_key,
                                                    data=self.user_dict_list[i]).json()
                del get_account_request['Status']
                temp_list.append(get_account_request)
        else:
            get_account_request = requests.post(self.ACCOUNTS_URL, headers=self.api_key,
                                                data=self.user_id).json()
            temp_list.append(get_account_request)

        self.user_dict_list = temp_list

        self.get_account_transaction()

    def get_account_transaction(self):
        for i in range(len(self.user_dict_list)):
            temp_list = []
            if self.user_dict_list[i].get("AccessibleAccountDetailList") is not None:

                for j in self.user_dict_list[i].get("AccessibleAccountDetailList"):
                    company_id = j.get("OperatingCompanyIdentifier")
                    product_code = j.get("ProductCode")
                    primary_id = j.get("PrimaryIdentifier")

                    transaction_parameters = {"OperatingCompanyIdentifier": company_id,
                                              "ProductCode": product_code,
                                              "PrimaryIdentifier": primary_id}
                    transaction_history = requests.post(self.TRANSACTION_URL, headers=self.api_key,
                                                        data=transaction_parameters).text
                    # TODO: Needs to be fixed in the future
                    if len(transaction_history) > 200:

                        # print(company_id)
                        # print(product_code)
                        # print(primary_id)

                        transaction_history = ast.literal_eval(transaction_history)
                        del transaction_history['Status']

                        if bool(transaction_history) is True:

                            temp_list.append(transaction_history.get("TransactionList"))
                    else:
                        pass
            temp_dict = {"TransactionList": temp_list}
            if len(temp_list) == 0:
                pass
            else:
                self.user_dict_list[i].update(temp_dict)

        self.get_purchase_category()

    def get_purchase_category(self):
        def categorize_data(data):
            housing = ["0742", "0780", "0763", "1731", "1711", "1740","1750", "1761", "1520", "1771", "1799",
                       "2791", "2842", "7375", "4899", "4814"]
            transportation = ["4214", "4511", "5511", "5521", "5947", "7217", "7512", "7542",
                              "7996", "8050", "8351", "5541", "7538", "5542"]
            food_stores = ["5411", "7033", "5812", "5814", "5499", "5814", "5995", "5310", "5311", "5331", "5309",
                           "5441", "5451", "5621", "5651", "5621", "5651", "5641", "5655", "5661", "5691", "5611",
                           "5698", "5714", "5732", "5733", "5734", "5735", "5912", "5931", "5941", "5942", "5943",
                           "5944", "5949", "5950", "5946", "5948", "5977", "5978", "5972", "5997", "5973", "5473",
                           "7841", "5300", "5940", "5699"]
            medical_health = ["7298", "5047", "8071", "8099", "8011", "8021", "8031", "8042", "8044", "8062", "8041",
                              "8049", "8050", "8043"]
            household_supplies = ["4225","5200", "5722", "7210", "7211", "2842", "7216", "7217", "7251", "7349",
                                  "5211", "5231", "5251", "5261", "5719", "5712", "5713", "5718"]
            personal = ["8699", "5977", "5968", "7230", "5960", "7997"]
            education = ["5943", "7911", "8211", "8241", "8244", "8249", "8220", "5192"]
            entertainment = ["5921", "5993", "5945", "7993", "7994", "5968", "7998", "7995", "5813"]

            if data in housing:
                return "Housing and Utility"
            if data in transportation:
                return "Transportation"
            if data in food_stores:
                return "Food/Stores"
            if data in medical_health:
                return "Medical/Healthcare"
            if data in household_supplies:
                return "Household Items/Supplies"
            if data in personal:
                return "Personal"
            if data in education:
                return "Education"
            if data in entertainment:
                return "Entertainment "
            else:
                return "Others"
        # TODO: One user does't get any transactions
        for i in range(len(self.user_dict_list)):
            try:
                #print(self.user_dict_list[i])
                temp_dict_category = dict()
                user_number = "User_" + str(i)
                for g in self.user_dict_list[i].get("TransactionList"):
                    for j in g:
                        if (j.get("StandardIndustryCode") is not None) and (j.get("StandardIndustryCode") != "00000"):
                            category_name = categorize_data(j.get("StandardIndustryCode")[1:5] )
                            if category_name in  temp_dict_category.keys():
                                value = temp_dict_category.get(category_name)
                                value += float(j.get("PostedAmount"))
                                temp_dict_category.update({category_name: value})
                            else:
                                temp_dict_category.update({category_name: float(j.get("PostedAmount"))})
                self.final_dict.update({user_number: [temp_dict_category]})
            except:
                pass

        self.get_percentage()

    def get_percentage(self):
        housing = []
        transportation= []
        food_stores =[]
        medical_health =[]
        household_supplies = []
        personal = []
        education = []
        entertainment = []
        other = []

        for i in self.final_dict.keys():
            for g in self.final_dict[i]:
                if "Housing and Utility" in g.keys():
                    housing.append(g.get("Housing and Utility"))
                if "Transportation" in g.keys():
                    transportation.append(g.get("Transportation"))
                if "Food/Stores" in g.keys():
                    food_stores.append(g.get("Food/Stores"))
                if "Medical/Healthcare" in g.keys():
                    medical_health.append(g.get("Medical/Healthcare"))
                if "Household Items/Supplies" in g.keys():
                    household_supplies.append(g.get("Household Items/Supplies"))
                if "Personal" in g.keys():
                    personal.append(g.get("Personal"))
                if "Education" in g.keys():
                    education.append(g.get("Education"))
                if "Entertainment" in g.keys():
                    entertainment.append(g.get("Entertainment"))
                else:
                    other.append(other)

        def get_total (original_table):
            number = 0
            for table_range in range(len(original_table)):
                try:
                    number += original_table[table_range]
                except:
                    pass
            return number

        housing_total = get_total(housing)
        transportation_total = get_total(transportation)
        food_stores_total = get_total(food_stores)
        medical_health_total = get_total(medical_health)
        household_supplies_total = get_total(household_supplies)
        personal_total = get_total(personal)
        education_total = get_total(education)
        entertainment_total = get_total(entertainment)
        other_total = get_total(other)

        for k in self.final_dict.keys():
            total_per = 0
            for g in self.final_dict[k]:
                if "Housing and Utility" in g.keys():
                    try:
                        total_per = abs((((
                                    g.get("Housing and Utility") / (housing_total - g.get("Housing and Utility")) / (
                                        len(housing) - 1))) / 100) - 1)
                        g.update({"Housing and Utility": total_per})
                    except:
                        g.update({"Housing and Utility": 0})
                if "Transportation" in g.keys():
                    try:
                        transportation.append(g.get("Transportation"))
                        total_per = abs(
                            (((g.get("Transportation") / (transportation_total - g.get("Transportation")) / (
                                    len(transportation) - 1))) * 100) - 100)
                        g.update({"Transportation": total_per})
                    except:
                        g.update({"Transportation": 0})
                if "Food/Stores" in g.keys():
                    try:
                        food_stores.append(g.get("Food/Stores"))
                        total_per = abs((((g.get("Food/Stores") / (food_stores_total - g.get("Food/Stores")) / (
                                len(food_stores) - 1))) * 100) - 100)
                        g.update({"Food/Stores": total_per})
                    except:
                        g.update({"Food/Stores": 0})
                if "Medical/Healthcare" in g.keys():
                    try:
                        medical_health.append(g.get("Medical/Healthcare"))
                        total_per = abs(
                            (((g.get("Medical/Healthcare") / (medical_health_total - g.get("Medical/Healthcare")) / (
                                    len(medical_health) - 1))) * 100) - 100)
                        g.update({"Medical/Healthcare": total_per})
                    except:
                        g.update({"Medical/Healthcare": 0})
                if "Household Items/Supplies" in g.keys():
                    try:
                        household_supplies.append(g.get("Household Items/Supplies"))
                        total_per = abs(
                            (((g.get("Household Items/Supplies") / (
                                        household_supplies_total - g.get("Household Items/Supplies")) / (
                                       len(household_supplies) - 1))) * 100) - 100)
                        g.update({"Household Items/Supplies": total_per})
                    except:
                        g.update({"Household Items/Supplies": 0})
                if "Personal" in g.keys():
                    try:
                        personal.append(g.get("Personal"))
                        total_per = abs(
                            (((g.get("Personal") / (
                                    personal_total - g.get("Personal")) / (
                                       len(personal) - 1))) * 100) - 100)
                        g.update({"Personal": total_per})
                    except:
                        g.update({"Personal": 0})
                if "Education" in g.keys():
                    try:
                        education.append(g.get("Education"))
                        total_per = abs(
                            (((g.get("Education") / (
                                    education_total - g.get("Education")) / (
                                       len(education) - 1))) * 100) - 100)
                        g.update({"Education": total_per})
                    except:
                        g.update({"Education": 0})
                if "Entertainment" in g.keys():
                    try:
                        entertainment.append(g.get("Entertainment"))
                        total_per = abs(
                            (((g.get("Entertainment") / (
                                    entertainment_total - g.get("Entertainment")) / (
                                       len(entertainment) - 1))) * 100) - 100)
                        g.update({"Entertainment": total_per})
                    except:
                        g.update({"Entertainment": 0})
                else:
                    try:
                        other.append(other)
                        total_per = abs(
                            (((g.get("Others") / (
                                    other_total - g.get("Others")) / (
                                       len(other) - 1))) * 100) - 100)
                        g.update({"Others": total_per})
                    except:
                        g.update({"Others": 0})

        self.format_for_print()

    def format_for_print(self):
        random_name = ["John", "Steve", "Maxim", "Alex", "Carl"]
        for k in self.final_dict.keys():
            if k == "User_1":
                pass
            else:
                print("User: " + random.choice(random_name))
                for g in self.final_dict[k]:
                    for z in g:
                        print(z + ": " + str(g.get(z)))



UserApi("YOUR_API").get_users_list()
