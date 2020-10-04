import json
import sys
import re
from datetime import date

from General_Packages import read_my_email
import Venmo


# Get emails
email_arr = []
subjects = ["FW: Your Publix receipt.", 'Fwd: Your Publix receipt.']
for s in subjects:
    for mail in read_my_email(subject=s):
        mail = str(mail)
        total = re.findall(r'Grand Total\s+\d+\.\d+', mail) # replace this with a ReGeX string in the body of the email you are looking for
        print(total)
        email_arr.append(total)

"""
# Cached emails for debug
with open("../gggg.txt", "r") as file:
    email_arr = json.load(file)
"""

for total_str in email_arr:
    total = float(re.search(r"\d+.\d+", total_str[0]).group()) # Get the number out of the string
    d= date.today()
    message = "Publix " + str(d.month) + "-" + str(d.day)
    Venmo.charge_money(total, 'Kristen-Lockhart-10', message)
    sys.exit()


Venmo.logout()