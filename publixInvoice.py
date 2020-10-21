#! /usr/bin/python3

import json
import sys
import re

from General_Packages import read_my_email


# For each subject...
ticket_arr = []
subjects = ["FW: Your Publix receipt.", 'Fwd: Your Publix receipt.']
for s in subjects:
    # Look thru my inbox for matches and...
    for mail in read_my_email(subject=s):
        # get the grand total and date from the receipt
        mail = str(mail)
        total = re.findall(r'Grand Total\s+\d+\.\d+', mail)
        date = re.findall(r'\d{2}\/\d{2}\/\d{4}', mail)
        print(total, date)
        ticket_arr.append(total, date)

# Send any venmo request to Kristen
if ticket_arr:
    import Venmo
    for total, date in ticket_arr:
        total = float(re.search(r"\d+.\d+", total[0]).group()) # Get the number out of the string    
        message = "Publix " + date
        Venmo.charge_money(total/2, 'Kristen-Lockhart-10', message)
            
    Venmo.logout()

else:
    from datetime import date
    print("\nNo receipts on: ", date.today())
