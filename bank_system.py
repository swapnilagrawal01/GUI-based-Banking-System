# We have assumed 2 types of account: 1) Savings 2) Business
#importing required libraries
import tkinter as tk
from tkinter import messagebox
from customer_account import CustomerAccount
from admin import Admin
import csv

#Creating Empty list to store data
accounts_list = []
admins_list = []

class BankSystem(object):
    def __init__(self):
        #Initialization
        self.accounts_list = []
        self.admins_list = []
        
        #Loading Bank Data
        self.load_bank_data()
        
        #Interest Rate 
        self.business_rate=0
        self.savings_rate=4
        
        #Overdraft Limit
        self.business_overdraft_limit=25
        self.savings_overdraft_limit=50
    # Function to load bank data from csv
    def load_bank_data(self):
     
        #Read Customer CSV File
        with open('Customer.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:         
                customer=CustomerAccount(row[0],row[1],[row[2],row[3],row[4],row[5]],row[6],row[7],row[8])
                self.accounts_list.append(customer)
                
        #Read Admin Csv File    
        with open('Admin.csv') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:  
                adm=Admin(row[0],row[1],[row[2],row[3],row[4],row[5]],row[6],row[7],row[8])
                self.admins_list.append(adm) 
                
     # Function for searching  Admins by username           
    def search_admins_by_name(self, admin_username):
            #STEP A.2
            found_admin = None
            #searching in the admins list
            for a in self.admins_list:
                username = a.get_username()           
                if username == admin_username:
                    found_admin = a
                    break
            return found_admin
        
    # Function for searching  Customers by username  
    def search_customers_by_name(self, customer_lname):
        #STEP A.3
        found_customer = None
        for a in self.accounts_list:
            username = a.get_last_name()
            if username == customer_lname:
                found_customer = a
                break

        return found_customer

    # Function for searching  Customers by account number
    def search_customers_by_acc(self, customer_acc):
        found_customer = None
        for a in self.accounts_list:
            acc = a.get_acc_no()
            if acc == customer_acc:
                found_customer = a
                return found_customer
                
        if found_customer == None:
            messagebox.showinfo("Error","Invalid Credentials!\nTry Again!")
        return found_customer
    
    # Helper Function for transferring money
    def transfer_money_helper(self, master,sender_acc_no, receiver_account_no, amount):
            #ToDo
            try:
                #Destroying Window
                master.destroy()
                #Getting Customer object
                sender = self.search_customers_by_acc(sender_acc_no)
                if sender==None:
                    return
                reciever = self.search_customers_by_acc(receiver_account_no)
                amount=float(amount)
                overdraft_limit=0
                if sender.get_account_type()=='business':
                    overdraft_limit=self.business_overdraft_limit
                elif sender.get_account_type()=='savings':
                    overdraft_limit=self.savings_overdraft_limit
                    
                 #Checking for overdraft limit   
                if reciever != None and sender != None and sender.get_balance()+overdraft_limit>=amount:
                    reciever.deposit(amount)
                    sender.withdraw(amount)                
                    messagebox.showinfo("Success","\nSender Updated Balance:%s \nReceivers' Updated Balance: %s " %(sender.get_balance(),reciever.get_balance()))
                else:
                    messagebox.showinfo("Failure","Insufficient Balance in the account")
            except Exception as e:
                messagebox.showinfo("Error",e)
                
            
    #Function for transferring Money
    def transferMoney(self):
        
            #Creating a new window 
            tfwn=tk.Tk()
            tfwn.geometry("600x300")
            tfwn.title("Transfer Money")
            tfwn.configure(bg="orange")
            fr1=tk.Frame(tfwn,bg="blue")
            l_title=tk.Message(tfwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
            l_title.config(font=("Courier","50","bold"))
            l_title.pack(side="top")
            l1=tk.Label(tfwn,text="Sender's Account Number",relief="raised")
            l1.pack(side="top")
            e1=tk.Entry(tfwn)
            e1.pack(side="top")
            l2=tk.Label(tfwn,text="Receiver Account Number",relief="raised")
            l2.pack(side="top")
            e2=tk.Entry(tfwn)
            e2.pack(side="top")
            l3=tk.Label(tfwn,text="Enter Amount to be transferred",relief="raised")
            l3.pack(side="top")
            e3=tk.Entry(tfwn)
            e3.pack(side="top")
            
            #Creating buttons
            b1=tk.Button(tfwn,text="Submit",command=lambda: self.transfer_money_helper(tfwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
            b1.pack(side="top")
            b2=tk.Button(tfwn,text="Exit",command=tfwn.destroy)
            b2.pack(side="top")
            return
        
    #Function for displaying Management Report
    def get_management_report(self):
            try:
                total_customers=0
                total_interest_payable=0
                total_sum=0
                total_overdrafts=0
                rate=0
                for c in self.accounts_list:
                    total_customers+=1
                    if c.get_account_type()=='business':
                        rate=self.business_rate
                    elif c.get_account_type()=='savings':
                        rate=self.savings_rate             
                    total_interest_payable+=c.get_balance()* rate/100

                    balance=c.get_balance()
                    if balance>=0:
                        total_sum+=balance
                    else:
                        total_overdrafts+=abs(balance)

                messagebox.showinfo("Info","Total Number of Customers: %s \nTotal Money in bank:%s \nTotal Interest Payable:%s \nTotal Overdrafts taken by customers:%s" %(total_customers,total_sum,total_interest_payable,total_overdrafts))
            except Exception as e:
                print(e)
     
    # Helper Function for updating customer name
    def update_customer_name_helper(self,master,sender,fname,sname):
        master.destroy()
        sender.update_first_name(fname)
        sender.update_last_name(sname)
        messagebox.showinfo("Name Update Successfull")
        
    # Helper Function for updating customer address    
    def update_customer_address_helper(self,master,sender,addr):
        master.destroy()
        sender.update_address(addr)
        messagebox.showinfo("Address Update Successfull")
        
    # Function for updating customer name
    def update_customer_name(self,sender):
        
        #Creating Window, buttons and labels
        ndwn=tk.Tk()
        ndwn.geometry("600x300")
        ndwn.title("Update Customer Name")
        ndwn.configure(bg="orange")
        fr1=tk.Frame(ndwn,bg="blue")
        l_title=tk.Message(ndwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l1=tk.Label(ndwn,text="Enter Customer New First Name:",relief="raised")
        l1.pack(side="top")
        e1=tk.Entry(ndwn)
        e1.pack(side="top")
        l2=tk.Label(ndwn,text="Enter Customer New Last Name:",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(ndwn)
        e2.pack(side="top")
        b1=tk.Button(ndwn,text="Update",command=lambda: self.update_customer_name_helper(ndwn,sender,e1.get().strip(),e2.get().strip()))
        b1.pack(side="top")
        b2=tk.Button(ndwn,text="Exit",command=ndwn.destroy)
        b2.pack(side="top")
        return
    
    # Function for updating customer address
    def update_customer_address(self,sender):
        
        #Creating Window, buttons and labels
        nawn=tk.Tk()
        nawn.geometry("600x300")
        nawn.title("Update Customer Address")
        nawn.configure(bg="orange")
        fr1=tk.Frame(nawn,bg="blue")
        l_title=tk.Message(nawn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")

        addr=[]
        l1=tk.Label(nawn,text="Enter Customer New House Number:",relief="raised")
        l1.pack(side="top")
        e1=tk.Entry(nawn)
        e1.pack(side="top")
        addr.append(e1.get().strip())
        l2=tk.Label(nawn,text="Enter Customer New Street name:",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(nawn)
        e2.pack(side="top")
        addr.append(e2.get().strip())
        l3=tk.Label(nawn,text="Enter Customer New City Name:",relief="raised")
        l3.pack(side="top")
        e3=tk.Entry(nawn)
        e3.pack(side="top")
        addr.append(e3.get().strip())
        l4=tk.Label(nawn,text="Enter Customer New Post Code:",relief="raised")
        l4.pack(side="top")
        e4=tk.Entry(nawn)
        e4.pack(side="top")
        addr.append(e4.get().strip())
        b1=tk.Button(nawn,text="Update",command=lambda:self.update_customer_address_helper(nawn,sender,addr))
        b1.pack(side="top")
        b2=tk.Button(nawn,text="Exit",command=nawn.destroy)
        b2.pack(side="top")
        return  
    
    # Helper Function for depositing money
    def deposit_money_helper(self,master,sender,amt):
        master.destroy()
        sender.deposit(float(amt))
        messagebox.showinfo('Money deposited')
      
    # Helper Function for withdrawing money
    def withdraw_money_helper(self,master,sender,amt):
        master.destroy()
        overdraft_limit=0
        if sender.get_account_type()=='business':
            overdraft_limit=25
        elif sender.get_account_type()=='savings':
            overdraft_limit=50
        if sender.get_balance()+overdraft_limit<float(amt):
            messagebox.showinfo("Failure","Insufficient Balance in the account")
        else:        
            sender.withdraw(float(amt))
            messagebox.showinfo('Money Withdrawn') 
            
    # Function for depositing money
    def deposit_Money(self,sender):
        #Creating Window, buttons and labels
        tfwn=tk.Tk()
        tfwn.geometry("600x300")
        tfwn.title("Deposit Money")
        tfwn.configure(bg="orange")
        fr1=tk.Frame(tfwn,bg="blue")
        l_title=tk.Message(tfwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l2=tk.Label(tfwn,text="Enter Amount to be deposited",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(tfwn)
        e2.pack(side="top")

        b1=tk.Button(tfwn,text="Deposit",command=lambda:self.deposit_money_helper(tfwn,sender,e2.get().strip()))
        b1.pack(side="top")
        b2=tk.Button(tfwn,text="Exit",command=tfwn.destroy)
        b2.pack(side="top")
        return
    
    # Function for withdrawing money
    def Withdraw(self,sender):
        #Creating Window, buttons and labels
        tfwn=tk.Tk()
        tfwn.geometry("600x300")
        tfwn.title("Withdraw Money")
        tfwn.configure(bg="orange")
        fr1=tk.Frame(tfwn,bg="blue")
        l_title=tk.Message(tfwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l2=tk.Label(tfwn,text="Enter Amount to be withdrawn",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(tfwn)
        e2.pack(side="top")
        b1=tk.Button(tfwn,text="Withdraw",command=lambda: self.withdraw_money_helper(tfwn,sender,e2.get().strip()))
        b1.pack(side="top")
        b2=tk.Button(tfwn,text="Exit",command=tfwn.destroy)
        b2.pack(side="top")
        return
    
    # Function for checking customer account balance
    def check_balance(self,sender):
        messagebox.showinfo('Balance Info',"Balance: %s" %sender.get_balance())
        return
    
    # Function for printing the details of particular customer
    def print_details(self,c):
        #Creating Window, buttons and text widget
        root1=tk.Tk() 
        # specify size of window. 
        root1.geometry("250x170")
        # Create text widget and specify size. 
        T = tk.Text(root1, height = 5, width = 52) 

        # Create label 
        l = tk.Label(root1, text = "Customer Details") 
        l.config(font =("Courier", 14)) 
        # Create an Exit button. 
        b2 = tk.Button(root1, text = "Exit",command = root1.destroy)
        l.pack() 
        T.pack() 
        b2.pack() 
        data=""
        
        data+= "\nAccount Number:"+ str(c.get_acc_no())
        data+="\n"+ "First name:"+ str(c.get_first_name())
        data+="\n"+"Last name:" +str(c.get_last_name())
        address=c.get_address()
        data+="\n"+"Address:"+str(address[0])
        data+="\n"+str(c.address[1])
        data+="\n"+str(c.address[2])
        data+="\n"+str(c.address[3])
        data+='\n'
        # Insert The Fact. 
        T.insert(tk.END,data) 
    
    # Function for signing out
    def sign_out(self,master,admin):
        master.destroy()
        self.run_admin_options(admin)
     
    # Function for choosing options for particular customer
    def run_account_options(self,sender,admin):
        
        #Creating Window, buttons and labels
        cawn=tk.Tk()
        cawn.geometry("700x400")
        cawn.title("Customer Account cations")
        cawn.configure(bg="orange")
        fr1=tk.Frame(cawn,bg="blue")
        l_title=tk.Message(cawn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")

        b1=tk.Button(text="Deposit Money",command=lambda: self.deposit_Money(sender))
        b2=tk.Button(text="Withdraw",command=lambda:self.Withdraw(sender))
        b3=tk.Button(text="Check balance",command=lambda: self.check_balance(sender))
        b4=tk.Button(text="Show customer details",command=lambda: self.print_details(sender))
        b5=tk.Button(text="Update Customer Name",command=lambda: self.update_customer_name(sender))
        b6=tk.Button(text="Update Customer Address",command=lambda: self.update_customer_address(sender))
        b7=tk.Button(text="Sign out",command=lambda: self.sign_out(cawn,admin))
        b1.place(x=100,y=100)
        b2.place(x=400,y=100)
        b3.place(x=100,y=200)
        b4.place(x=400,y=200)
        b5.place(x=100,y=300)
        b6.place(x=300,y=300)
        b7.place(x=500,y=300)
        cawn.mainloop()     
    
    # Helper Function for customer operations
    def helper(self,master,master1,acc,admin):
        master.destroy()
        
        sender = self.search_customers_by_acc(acc)
        if sender==None:
            return
        master1.destroy()
        self.run_account_options(sender,admin)
    
    # Function for customer operations
    def customer_operations(self,master,admin):
        
        #Creating Window, buttons and labels
        tfwn=tk.Tk()
        tfwn.geometry("600x300")
        tfwn.title("Customer Operations")
        tfwn.configure(bg="orange")
        fr1=tk.Frame(tfwn,bg="blue")
        l_title=tk.Message(tfwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l2=tk.Label(tfwn,text="Enter Account Number",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(tfwn)
        e2.pack(side="top")
        b1=tk.Button(tfwn,text="Submit",command=lambda:self.helper(tfwn,master,e2.get().strip(),admin))
        b1.pack(side="top")
        b2=tk.Button(tfwn,text="Exit",command=tfwn.destroy)
        b2.pack(side="top")
        return
    
    # Helper Function for deleting record
    def delete_helper(self,master,acc_no):
        master.destroy()
        customer_account = self.search_customers_by_acc(acc_no)
        if customer_account != None:
            self.accounts_list.remove(customer_account)
            messagebox.showinfo("Success","%s was deleted successfully!" %customer_account.get_first_name())
    
    # Function for deleting customer from records
    def delete_customer(self,admin_obj):
        
        #Creating Window, buttons and labels
        if admin_obj.has_full_admin_right():
            dcwn=tk.Tk()
            dcwn.geometry("600x300")
            dcwn.title("Delete Customer Account")
            dcwn.configure(bg="orange")
            fr1=tk.Frame(dcwn,bg="blue")
            l_title=tk.Message(dcwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
            l_title.config(font=("Courier","50","bold"))
            l_title.pack(side="top")
            l1=tk.Label(dcwn,text="Enter Customer Account Number:",relief="raised")
            l1.pack(side="top")
            e1=tk.Entry(dcwn)
            e1.pack(side="top")
            b1=tk.Button(dcwn,text="Delete",command=lambda: self.delete_helper(dcwn,e1.get().strip()))
            b1.pack(side="top")
            b2=tk.Button(dcwn,text="Exit",command=dcwn.destroy)
            b2.pack(side="top")
            return        
        else:
            messagebox.showinfo("Error","Admin %s %s does not have full admin rights" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
        return
    
    # Helper Function for updating the admin name
    def update_admin_name_helper(self,master,admin_obj,fname,sname):
        master.destroy()
        admin_obj.update_first_name(fname)
        admin_obj.update_last_name(sname)
        messagebox.showinfo("Name Update Successfull")
        
    # Helper Function for updating the admin address
    def update_admin_address_helper(self,master,admin_obj,addr):
        master.destroy()
        admin_obj.update_address(addr)
        messagebox.showinfo("Address Update Successfull")
        
    # Function for updating the admin name
    def update_admin_name(self,admin_obj):
        
        #Creating Window, buttons and labels
        ndwn=tk.Tk()
        ndwn.geometry("600x300")
        ndwn.title("Update Admin Name")
        ndwn.configure(bg="orange")
        fr1=tk.Frame(ndwn,bg="blue")
        l_title=tk.Message(ndwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l1=tk.Label(ndwn,text="Enter Admin New First Name:",relief="raised")
        l1.pack(side="top")
        e1=tk.Entry(ndwn)
        e1.pack(side="top")
        l2=tk.Label(ndwn,text="Enter Admin New Last Name:",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(ndwn)
        e2.pack(side="top")
        b1=tk.Button(ndwn,text="Update",command=lambda: self.update_admin_name_helper(ndwn,admin_obj,e1.get().strip(),e2.get().strip()))
        b1.pack(side="top")
        b2=tk.Button(ndwn,text="Exit",command=ndwn.destroy)
        b2.pack(side="top")
        return
    
    # Function for updating the admin address
    def update_admin_address(self,admin_obj):
        
        #Creating Window, buttons and labels
        nawn=tk.Tk()
        nawn.geometry("600x300")
        nawn.title("Update Admin Address")
        nawn.configure(bg="orange")
        fr1=tk.Frame(nawn,bg="blue")
        l_title=tk.Message(nawn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")

        addr=[]
        l1=tk.Label(nawn,text="Enter Admin New House Number:",relief="raised")
        l1.pack(side="top")
        e1=tk.Entry(nawn)
        e1.pack(side="top")
        addr.append(e1.get().strip())
        l2=tk.Label(nawn,text="Enter Admin New Street name:",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(nawn)
        e2.pack(side="top")
        addr.append(e2.get().strip())
        l3=tk.Label(nawn,text="Enter Admin New City Name:",relief="raised")
        l3.pack(side="top")
        e3=tk.Entry(nawn)
        e3.pack(side="top")
        addr.append(e3.get().strip())
        l4=tk.Label(nawn,text="Enter Admin New Post Code:",relief="raised")
        l4.pack(side="top")
        e4=tk.Entry(nawn)
        e4.pack(side="top")
        addr.append(e4.get().strip())
        b1=tk.Button(nawn,text="Update",command=lambda:self.update_admin_address_helper(nawn,admin_obj,addr))
        b1.pack(side="top")
        b2=tk.Button(nawn,text="Exit",command=nawn.destroy)
        b2.pack(side="top")
#         nawn.destroy()
        
        return
    
    # Function for Printing all account details
    def print_all_accounts_details(self):
        
        #Creating Window, buttons and labels
        root=tk.Tk() 
        # specify size of window. 
        root.geometry("250x170")

        # Create text widget and specify size. 
        T = tk.Text(root, height = 5, width = 52) 

        # Create label 
        l = tk.Label(root, text = "Customer Details") 
        l.config(font =("Courier", 14)) 
        # Create an Exit button. 
        b2 = tk.Button(root, text = "Exit",command = root.destroy)
        l.pack() 
        T.pack() 
        b2.pack() 
        data=""
        i = 0
        for c in self.accounts_list:
            i+=1
            data=data+'\n'+ str(i)
            data+= "\nAccount Number:"+ str(c.get_acc_no())
            data+="\n"+ "First name:"+ str(c.get_first_name())
            data+="\n"+"Last name:" +str(c.get_last_name())
            address=c.get_address()
            data+="\n"+"Address:"+str(address[0])
            data+="\n"+str(c.address[1])
            data+="\n"+str(c.address[2])
            data+="\n"+str(c.address[3])
            data+='\n'
            
        # Insert The Data. 
        T.insert(tk.END,data) 
    
    # Function for Checking admin credentials
    def admin_login(self,master,username,password):

        found_admin = self.search_admins_by_name(username)
        if found_admin == None or found_admin.get_password() != password:
            found_admin=None
            messagebox.showinfo("Login Failed","Invalid Credentials\nPlease try again.")
            master.destroy()
            self.Main_Menu()

#         messagebox.showinfo("Login Succesfull")
        master.destroy()              
        self.run_admin_options(found_admin)
    
    # Function for Calling the menu of the options available with admin
    def run_admin_options(self,admin_obj):
        
        #Creating Window, buttons and labels
        opwn=tk.Tk()
        opwn.geometry("700x400")
        opwn.title("Admin Options")
        opwn.configure(bg="orange")
        fr1=tk.Frame(opwn,bg="blue")
        l_title=tk.Message(opwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")

        b1=tk.Button(text="Tranfer Money",command=self.transferMoney)
        b2=tk.Button(text="Customer account operations & profile settings",command=lambda: self.customer_operations(opwn,admin_obj))
        b3=tk.Button(text="Delete customer",command=lambda: self.delete_customer(admin_obj))
        b4=tk.Button(text="Print all customers details",command=self.print_all_accounts_details)
        b5=tk.Button(text="Update Admin Name",command=lambda: self.update_admin_name(admin_obj))
        b6=tk.Button(text="Update Admin Address",command=lambda: self.update_admin_address(admin_obj))
        b7=tk.Button(text="Get Management Report",command=self.get_management_report)
        b8=tk.Button(text="Sign out",command=opwn.destroy)
        b1.place(x=100,y=100)
        b2.place(x=200,y=100)
        b3.place(x=500,y=100)
        b4.place(x=100,y=200)
        b5.place(x=300,y=200)
        b6.place(x=500,y=200)
        b7.place(x=100,y=300)
        b8.place(x=400,y=300)
        opwn.mainloop()

    # Function for Calling the login windoe for admin
    def login(self,master):
        
        #Creating Window, buttons and labels
        master.destroy()
        crwn=tk.Tk()
        crwn.geometry("600x300")
        crwn.title("Admin Login")
        crwn.configure(bg="orange")
        fr1=tk.Frame(crwn,bg="blue")
        l_title=tk.Message(crwn,text="Python Banking System",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")
        l1=tk.Label(crwn,text="Enter Admin username:",relief="raised")
        l1.pack(side="top")
        e1=tk.Entry(crwn)
        e1.pack(side="top")
        l2=tk.Label(crwn,text="Enter Admin password",relief="raised")
        l2.pack(side="top")
        e2=tk.Entry(crwn,show="*")
        e2.pack(side="top")
        b=tk.Button(crwn,text="Submit",command=lambda: self.admin_login(crwn,e1.get().strip(),e2.get().strip()))
        b.pack(side="top")



# Function for Calling the main menu
    def Main_Menu(self):
        
        #Creating Window, buttons and labels
        rootwn=tk.Tk()
        rootwn.geometry("700x300")
        rootwn.title("Python Banking System")
        rootwn.configure(background='orange')
        fr1=tk.Frame(rootwn)
        fr1.pack(side="top")
        l_title=tk.Message(text="Python BANKING\n SYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
        l_title.config(font=("Courier","50","bold"))
        l_title.pack(side="top")

        b1=tk.Button(text="Admin Login",command=lambda: self.login(rootwn))
        b2=tk.Button(text="Quit Python Bank System",command=rootwn.destroy)
        b1.place(x=100,y=200)
        b2.place(x=400,y=200)
        rootwn.mainloop()
        
#Creating instance of BankSystem Class
app = BankSystem()
#Calling Main_Menu function
app.Main_Menu()
