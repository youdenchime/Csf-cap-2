
import random

class Account:
    def __init__(self, account_number, balance, account_type):
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            print("insufficient balance")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print("Withdrawal successful")
            else:
                print("Insufficient balance")
        else:
            print("0 fund")

    def get_balance(self):
        return self.balance

class PersonalAccount(Account):
    def __init__(self, account_number, balance):
        super().__init__(account_number, balance, "Personal")

class BusinessAccount(Account):
    def __init__(self, account_number, balance):
        super().__init__(account_number, balance, "Business")

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    account_info = line.strip().split(',')
                    account_number = int(account_info[0])
                    password = account_info[1]
                    account_type = account_info[2]
                    balance = float(account_info[3])
                    if account_type.lower() == "personal":
                        account = PersonalAccount(account_number, balance)
                    elif account_type.lower() == "business":
                        account = BusinessAccount(account_number, balance)
                    else:
                        print(f"Invalid account type for account number {account_number}")
                        continue
                    self.accounts[account_number] = (password, account)
        except FileNotFoundError:
            print("No existing accounts file found.")

    def save_accounts(self):
        with open("accounts.txt", "w") as file:
            for account_number, (password, account) in self.accounts.items():
                file.write(f"{account_number},{password},{account.account_type},{account.get_balance()}\n")

    def create_account(self, account_type):
        account_number = random.randint(100000000, 999999999)
        password = ''.join(random.choices('210942679', k=6))
        if account_type.lower() == "personal":
            account = PersonalAccount(account_number, 0)
        elif account_type.lower() == "business":
            account = BusinessAccount(account_number, 0)
        else:
            print("Invalid account type")
            return
        self.accounts[account_number] = (password, account)
        self.save_accounts()
        print("Account created successfully")
        print(f"Account number: {account_number}")
        print(f"Default password: {password}")

    def login(self, account_number, password):
        if account_number in self.accounts:
            if self.accounts[account_number][0] == password:
                return self.accounts[account_number][1]
            else:
                print(" wrong passward24")
        else:
            print("Account does not exist")

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            print("Account deleted successfully")
        else:
            print("Account does not exist")

    def transfer(self, sender_account_number, receiver_account_number, amount):
        if sender_account_number in self.accounts and receiver_account_number in self.accounts:
            sender_account = self.accounts[sender_account_number][1]
            receiver_account = self.accounts[receiver_account_number][1]
            if sender_account.get_balance() >= amount:
                sender_account.withdraw(amount)
                receiver_account.deposit(amount)
                print("Transfer successful")
                self.save_accounts()
            else:
                print("Insufficient funds")
        else:
            print("Sender or receiver account does not exist")

def main():
    bank_system = BankingSystem()
    while True:
        print("\nWelcome to the Bank Management System")
        print("1. Create Account")
        print("2. Login")
        print("3. Delete Account")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ")
            bank_system.create_account(account_type)
        elif choice == "2":
            account_number = int(input("Enter account number: "))
            password = input("Enter password: ")
            account = bank_system.login(account_number, password)
            if account:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transfer Money")
                    print("5. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif sub_choice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif sub_choice == "3":
                        print("Current balance:", account.get_balance())
                    elif sub_choice == "4":
                        receiver_account_number = int(input("Enter receiver's account number: "))
                        amount = float(input("Enter amount to transfer: "))
                        bank_system.transfer(account_number, receiver_account_number, amount)
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid choice")
            else:
                print("Login failed")
        elif choice == "3":
            account_number = int(input("Enter account number to delete: "))
            bank_system.delete_account(account_number)
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
