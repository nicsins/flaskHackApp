import requests
import os
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
                       "2791", "2842"]
            transportation = ["4214", "4511", "5511", "5521", "5947", "7217", "7512", "7542",
                              "7996", "8050", "8351"]
            food_stores = ["5411", "7033", "5812", "5814", "5499", "5814", "5995", "5310", "5311", "5331", "5309",
                           "5441", "5451", "5621", "5651", "5621", "5651", "5641", "5655", "5661", "5691", "5611",
                           "5698", "5714", "5732", "5733", "5734", "5735", "5912", "5931", "5941", "5942", "5943",
                           "5944", "5949", "5950", "5946", "5948", "5977", "5978", "5972", "5997", "5973", "5473",
                           "7841", "5300"]
            medical_health = ["7298", "5047", "8071", "8099", "8011", "8021", "8031", "8042", "8044", "8062", "8041",
                              "8049", "8050", "8043"]
            household_supplies = ["4225","5200", "5722", "7210", "7211", "2842", "7216", "7217", "7251", "7349",
                                  "5211", "5231", "5251", "5261", "5719", "5712", "5713", "5718"]
            personal = ["8699", "5977", "5968"]
            education = ["5943", "7911", "8211", "8241", "8244", "8249", "8220", "5192"]
            entertainment = ["5921", "5993", "5945", "7993", "7994", "5968", "7998", "7995"]

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

        for i in range(len(self.user_dict_list)):
            try:
                for g in self.user_dict_list[i].get("TransactionList"):
                    for j in g:
                        if (j.get("StandardIndustryCode") is not None) and (j.get("StandardIndustryCode") != "00000"):
                            print(categorize_data(j.get("StandardIndustryCode")[1:5]))
                            print(j.get("StandardIndustryCode"))
                            print(j.get("PostedAmount"))
                            self.SINGE_CATEGORY_URL += j.get("StandardIndustryCode")[1:5]


                            """
                            specific_category = requests.get(self.SINGE_CATEGORY_URL, headers=self.api_key).json()
                            try:
                                del specific_category['Status']
                            except KeyError:
                                pass

                            self.SINGE_CATEGORY_URL = self.SINGE_CATEGORY_URL[:-4]
                            if bool(specific_category) is True:
                                self.user_dict_list[i].update(specific_category)
                            """
            except TypeError:
                pass
        self.organize_data()

    def organize_data(self):
        pass






UserApi("YOUR_API").get_users_list()
