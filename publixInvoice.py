import json
import sys
import re

from General_Packages import read_my_email
import Venmo


# For each subject...
subjects = ["FW: Your Publix receipt.", 'Fwd: Your Publix receipt.']
for s in subjects:
    # Look thru my inbox for matches and...
    for mail in read_my_email(subject=s):
        # get the grand total and date from the receipt
        mail = str(mail)
        total = re.findall(r'Grand Total\s+\d+\.\d+', mail)
        date = re.findall(r'\d{2}\/\d{2}\/\d{4}', mail)
        print(total, date)

        # Send venmo request to Kristen
        total = float(re.search(r"\d+.\d+", total[0]).group()) # Get the number out of the string    
        message = "Publix " + date
        Venmo.charge_money(total/2, 'Kristen-Lockhart-10', message)
    

Venmo.logout()