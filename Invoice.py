#! /usr/bin/python3

import sys, os
import re

from General_Packages import read_my_email, test_network

test_network()

class Utility:
    def __init__(self, name, subject, total=r"\$\d+\.\d+"):
        self.name = name
        self.subject = subject
        self.total = total

here = os.path.join(os.sep, "home", "david", "Documents", "PersonalProjects", "PublixInvoice")
#print(os.getcwd())
try:
    # I don't want to put my TECO acct_num in the code
    teco_acct_num = ""
    with open(os.path.join(here, ".key", "teco_acct_num.txt"), 'r') as fin:
        teco_acct_num = fin.read()

    # Generate utilities
    u= [
        ["Publix", "Your Publix receipt.", r"Grand Total\s+\d+\.\d+"],
        ["Utilities", "Your statement is ready to view for Cambridge Woods Apts"],
        ["TECO", "New Bill for Tampa Electric Account #"+teco_acct_num],
        ["Spectrum", "Your Spectrum Bill is now available"]
    ]
    utilities = []
    for i in u:
        utilities.append(Utility(*i))

    ticket_arr = []
    prefixes = ["", "FW: ", "Fwd: "]
    # for each of the utilities
    for utility in utilities:                       
        # and for each type of prefix
        for prefix in prefixes:                     
            # get all the emails
            for mail in read_my_email(subject=prefix+utility.subject):   
                mail = str(mail)

                # get the grand total and date from the receipt
                date = re.findall(r"\d+\/\d+\/\d{4}", mail)
                total = re.findall(utility.total, mail)

                if date == []:
                    print(mail)

                # if 2+ matches, only need first one
                if type(total) == type([]): 
                    total = total[0]
                if type(date) == type([]): 
                    if utility.name == 'Publix':
                        date = date[1]
                    else:
                        date = date[0]

                print(utility.name, total, date)
                ticket_arr.append((total, date, utility.name))

    # Send any venmo request to Kristen
    if ticket_arr:
        import Venmo

        for total, date, name in ticket_arr:
            message = name + ' ' + date

            try:
                total = float(re.search(r"\d+\.\d+", total).group()) # Get the number out of the string    
            except AttributeError:
                total = float(total[1:])

            if name == "Publix" and total > 100.00:
                total = 100.00  # only paying for $50 of groceries
            
            Venmo.charge_money(total/2, 'Kristen-Lockhart-10', message)
                
    else:
        from datetime import date
        print("\nNo receipts on: ", date.today())
except:
    from General_Packages import send_sms
    import json

    # Get phone credentials and send sms that the script failed
    with open(os.path.join(here, ".key", "phone"), 'r') as fin:
        phone = json.load(fin)
        send_sms("The Publix Invoice didn't work", phone[0], phone[1])