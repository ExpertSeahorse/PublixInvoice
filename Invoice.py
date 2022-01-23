#! /usr/bin/python3

import sys, os
import re

from General_Packages import read_my_email, login_to_email

# test_network()


class Utility:
    def __init__(self, name, subject, total=r"\$\d+\.\d+"):
        self.name = name
        self.subject = subject
        self.total = total

if os.name == 'nt':
    here = os.path.join(
        "C:\\", "Users", "dtfel", "projects", "PublixInvoice"
    )

else:
    here = os.path.join(
        os.sep, "home", "david", "Documents", "PersonalProjects", "PublixInvoice"
    )
# print(os.getcwd())
try:
    # I don't want to put my TECO acct_num in the code
    teco_acct_num = ""
    with open(os.path.join(here, ".key", "teco_acct_num.txt"), "r") as fin:
        teco_acct_num = fin.read()

    # Generate utilities
    u = [
        ["Publix", "Your Publix receipt.", r"Grand Total\s+\d+\.\d+"],
        ["Utilities", "Your statement is ready to view for Cambridge Woods Apts"],
        ["TECO", "New Bill for Tampa Electric Account #" + teco_acct_num],
        # ["Spectrum", "Your Spectrum Bill is now available"],
        ["Spectrum", "Statement Ready"],
        ["HelloFresh", "Receipt for Your Payment to HelloFresh", r"You sent a payment of \$\d+\.\d\d USD to HelloFresh"]
    ]
    utilities = []
    for i in u:
        utilities.append(Utility(*i))

    ticket_arr = []
    conn = login_to_email()
    prefixes = ["", "FW: ", "Fwd: "]
    # for each of the utilities
    for utility in utilities:
        # and for each type of prefix
        for prefix in prefixes:
            # get all the emails
            subject = prefix + utility.subject
            for mail in read_my_email(subject, conn):
                mail = str(mail)
                print("starting", utility.subject)

                # get the grand total and date from the receipt
                date = re.findall(r"\d+\/\d+\/\d{4}", mail)
                total = re.findall(utility.total, mail)

                if date == []:
                    # Check for abbr month, ex: Jan 22, 2022
                    date = re.findall(r"\b\w{3} \d+, 20\d\d", mail)
                if date == []:
                    # Check for month of any len, ex: January 22, 2022
                    # EOL included to reduce false positives (intended for v2 Spectrum emails)
                    date = re.findall(r"\w+ \d+, 20\d\d", mail)
                if date == []:
                    with open("INVOICE_FAILURE.txt", 'w') as fout:
                        conn.logout()
                        print("Failure to capture date on:", utility.name)
                        print(mail, file=fout)
                        sys.exit()

                # if 2+ matches, only need first one
                if type(total) == type([]):
                    total = total[0]
                if type(date) == type([]):
                    if utility.name == "Publix":
                        date = date[1]
                    else:
                        date = date[0]

                print(utility.name, total, date)
                ticket_arr.append((total, date, utility.name))
    conn.logout()
    # Send any venmo request to Kristen
    if ticket_arr:
        import Venmo

        for total, date, name in ticket_arr:
            message = name + " " + date

            try:
                total = float(
                    re.search(r"\d+\.\d+", total).group()
                )  # Get the number out of the string
            except AttributeError:
                total = float(total[1:])

            if name == "Publix" and total > 100.00:
                total = 100.00  # only paying for $50 of groceries

            Venmo.charge_money(total / 2, "Kristen-Lockhart-10", message)

    else:
        from datetime import date

        print("\nNo receipts on: ", date.today())
except Exception as e:
    from General_Packages import send_sms
    import json

    raise e

    # Get phone credentials and send sms that the script failed
    with open(os.path.join(here, ".key", "phone"), "r") as fin:
        phone = json.load(fin)
        send_sms("The Publix Invoice didn't work", phone[0], phone[1])
