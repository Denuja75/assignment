import os
from datetime import datetime # Used to get current date and time

accounts = {} # This dictionary stores account details
next_account_number = 112211

# File names to store account and transaction data
accounts_file = "accountsDetails.txt"
transactions_file = "transactionsDetails.txt"

# Load account data from the text file when program starts
def load_accounts():
    global next_account_number
    if os.path.exists(accounts_file):
        with open(accounts_file, "r") as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 4:
                    acc_no = int(parts[0])
                    name = parts[1]
                    balance = float(parts[2])
                    password=int(parts[3])
                    accounts[acc_no] = {"name": name, "balance": balance,"password":password}#dictionery account number ku value name,balance
                    next_account_number = max(next_account_number, acc_no + 1)#compare chose max number and adding +1

# Write all accounts to file 
def save_accounts():
    with open(accounts_file, "a") as f: 
        f.write("AccountNo\tName\tInitialBalance\n")   
        for acc, data in accounts.items():  #accounts a dictionery .acc key.data (values-name,balance).items using for loop key and value at the same time
            f.write(f"{acc}\t{data['name']}\t{data['balance']}{data['password']}\n")

# Add a line to the transactionsDetails.txt file
def log_transaction(acc_no, action, amount, balance):#action value"deposited or withraw "
    with open(transactions_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#format for take date,time
        f.write(f"{timestamp} - {acc_no} - {action} {amount} - New Balance: {balance}\n")

# Menu #here not added user or admin login
def display_menu():
    print("\n===== welcome to mini bank =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Exit")

def create_account(): #Create new account
    global next_account_number
    name = input("Enter account holder name: ")
    password=int(input("enter password:"))
    try:
        balance = float(input("Enter initial balance: "))
        if balance < 0:
            print("Initial balance must be gratr than 0:")
            return
    except ValueError:
        print("Invalid input.")
        return

    accounts[next_account_number] = {"name": name, "balance": balance,"password":password} # Add account to dictionary
     # Save to accountsDetails file
    save_accounts()
    print(f"Account created successfully. Your account number is {next_account_number}")
    next_account_number += 1 # Next number for future accounts

# Option 2: Deposit money
def deposit_money():
    try:
        acc = int(input("Enter account number: "))
        password=int(input("enter password:"))
        if acc not in accounts and password not in accounts:
            print("Account not found.or password incorrect")
            return

        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Amount must be grater than 0:")
            return

        accounts[acc]['balance'] += amount # Update balance in dictionary
        # Save new data and log the transaction
        save_accounts()#save to account detail file
        log_transaction(acc, "Deposited", amount, accounts[acc]['balance']) #save to transection file#here action -value "deposited"
        print("Deposit successful.")

    except ValueError:
        print("Invalid input.")

# Option 3: Withdraw money
def withdraw_money():
    try:
        acc = int(input("Enter account number: "))
        password=int(input("enter password:"))
        if acc not in accounts and password not in accounts:
            print("Account not found.or incorrect password")
            return

        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Amount must be grater than 0.")
            return

        if accounts[acc]['balance'] < amount:
            print("Insufficient funds.")
            return

        # Update balance and save
        accounts[acc]['balance'] -= amount
        save_accounts()
        log_transaction(acc, "Withdrew", amount, accounts[acc]['balance'])#here "withraw "is action
        print("Withdrawal successful.")

    except ValueError:
        print("Invalid input.")

# Option 4: Check balance 
def check_balance():
    try:
        acc = int(input("Enter account number: "))
        password=int(input("enter password:"))
        if acc in accounts and password in accounts:
            print(f"Account: {acc} - Name: {accounts[acc]['name']} - Balance: {accounts[acc]['balance']}")
        else:
            print("Account not found.")
    except ValueError:
        print("Invalid input.")

#Option 5: Show transaction history
def transaction_history():
    try:
        acc = int(input("Enter account number: "))
        if not os.path.exists(transactions_file):#file or dictionery cheking exists
            print("No transactions recorded yet.")
            return

        found = False
        print(f"\n--- Transaction history for account {acc} ---")
        with open(transactions_file, "r") as f:
            for line in f:
                if line.strip().split(" - ")[1] == str(acc):#[1]==str(acc)checking,1=account number in file
                    print(line.strip())
                    found = True

        if not found:
            print("No transactions found for this account.")
    except ValueError:
        print("Invalid input.")

# Main
def main():
    load_accounts() # Load existing data
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            print("Thank you for using mini bank app😊. Exiting...")
            break
        else:
            print("Invalid choice.")

main()
#end program