import tkinter as tk
from tkinter import messagebox
class CustomerAccount:
    def __init__(self, fname, lname, address, account_no, balance,acc_type):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)
        self.acc_type=acc_type
        if acc_type=='business':
            self.overdraft_limit=25
        elif acc_type=='savings':
            self.overdraft_limit=50
            
    def update_first_name(self, fname):
        self.fname = fname
    
    def update_last_name(self, lname):
        self.lname = lname
                
    def get_first_name(self):
        return self.fname
    
    def get_last_name(self):
        return self.lname
        
    def update_address(self, addr):
        self.address = addr
        
    def get_address(self):
        return self.address
    
        
    def get_acc_no(self):
        return self.account_no
    
    def deposit(self, amount):
        self.balance+=amount
        
    def withdraw(self, amount):
        #ToDo
         self.balance-=amount
        
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
        
    def get_balance(self):
        return self.balance
    
    def get_account_type(self):
        return self.acc_type
    