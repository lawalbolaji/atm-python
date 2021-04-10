from datetime import datetime
import string
import random
import pickle

reg_user_credentials = {}
user_logged_in = None #details of currently logged in user

with open("credentials.config", 'rb') as reg_user_credentials_file:
    reg_user_credentials = pickle.load(reg_user_credentials_file)

def register():
    username = input("\n>>>Please enter your desired username\n")
    password = input("\n>>>Please enter your desired password\n")

    reg_user_credentials[username] = {
        "account name": username,
        "account number": gen_act_num(),
        "password": password,
        "account balance": 0
        }

    with open("credentials.config", 'wb') as reg_user_credentials_file:
        pickle.dump(reg_user_credentials, reg_user_credentials_file)
        
    print("\n\nYou can now login!\n\nThank you for banking with us\n\n")
    return True

def login():
    '''log user in and return credentials of currently logged in user
    '''
    
    name = input(">>>Enter your username? \n")
    
    if(name in reg_user_credentials.keys()):
        while(True):
            password = input("\n>>>Enter your password? \n")
            if(password == reg_user_credentials[name]["password"]):
                return reg_user_credentials[name]
            print("\nIncorrect password, please try again\n")

    print("\n\nUsername not found, please create account below\n\n")


def gen_act_num():
    return ''.join(random.choices(string.digits, k=10))

def display_menu(user_logged_in):
    print("\n")
    print(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    print("\n")

    print("Welcom %s\n\n" %user_logged_in["account name"])
    print("These are the available options:\n")
    print("1. Withdrawal\n")
    print("2. Cash Deposit\n")
    print("3. Complaint\n\n")

def display_welcome():
    print("\n\n\n\n==============WELCOME TO ZURIBANK================\n\n\n\nPlease login\n\n")

def logout(user_logged_in):

    reg_user_credentials[user_logged_in["account name"]] = user_logged_in

    with open("credentials.config", 'wb') as reg_user_credentials_file:
        pickle.dump(reg_user_credentials, reg_user_credentials_file)
    
    user_logged_in = None

    print("Thank you for baking with us, you have been successfully logged out!")

    return user_logged_in

def withdraw(user_logged_in):
    withdrawal_amount = input("\n>>> How much would you like to withdraw?\n")
    if(int(withdrawal_amount) > user_logged_in["account balance"]):
        return user_logged_in
    user_logged_in["account balance"] -= int(withdrawal_amount)
    print("\ntake your cash")

    return logout(user_logged_in)

def deposit(user_logged_in):
    deposit_amount = input("\n>>> How much would you like to deposit?\n")
    user_logged_in["account balance"] += int(deposit_amount)
    print("\nYour current balance is %s" %user_logged_in["account balance"])

    return logout(user_logged_in)

def complain(user_logged_in):
    complaint = input("\n>>> What issue will you like to report?\n")
    print("\nThank you for contacting us")

    return logout(user_logged_in)    

def atm():

    display_welcome()

    user_logged_in = login()

    while(not user_logged_in):
        register()
        user_logged_in = login()

    while(user_logged_in):
            
        display_menu(user_logged_in)
        selected_option = input(">>> Please select an option\n")

        if(selected_option.strip() == "1"):
            user_logged_in = withdraw(user_logged_in)
            if(user_logged_in):
                print("\n\nYour account balance is insufficient for this transaction, please try again!\n\n")
                continue
            
        elif(selected_option.strip()  == "2"):
            user_logged_in = deposit(user_logged_in)
            if(user_logged_in):
                print("Processing error, please try again!")
                continue
            
        elif(selected_option.strip()  == "3"):
            user_logged_in = complain(user_logged_in)
          
        else:
            print("invalid selection, please try again")


## Run application here
atm()
    
