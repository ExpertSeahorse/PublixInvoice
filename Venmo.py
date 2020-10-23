from datetime import datetime, timedelta
from General_Packages import privacy_decoder, send_sms
import venmo_api
import json, os, errno

# Venmo documentation: https://pypi.org/project/venmo-api/

###### Build Venmo client from credential file

CREDENTIAL_FILE = os.path.join(".key", "venmo_login") 

# Get login credentials
f = True
try:
    with open(CREDENTIAL_FILE, "r") as file:
        me = json.load(file)
        print("here")
    
# If no credential file, get credentials from user
except FileNotFoundError:
    f = False
    try:
        os.mkdir(os.path.join(os.getcwd(), ".key"))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    me = [input("Venmo username: "), input("Venmo password: ")]

# Create Venmo token
try:
    access_token = me[3]
    print("Here2")
    
# If access_token not saved
except IndexError: 
    f = False
    try:
        access_token = venmo_api.Client.get_access_token(username=me[0], password=me[1])
        me.append("<REPLACE THIS WITH A VALID DEVICE ID>")            
        me.append(access_token)
        venmo = venmo_api.Client(access_token=access_token)

    except:
        send_sms("Venmo login failed.")
# If access_token is saved
else:
    try:
        venmo = venmo_api.Client(access_token=access_token)
        print("here3")

    # If the saved access_token is bad, get a new one
    except:
        f = False
        access_token = venmo_api.Client.get_access_token(username=me[0], password=me[1], device_id=me[2])
        try:
            venmo = venmo_api.Client(access_token=access_token)
        except:
            send_sms("Venmo login failed.")

# Make/update credential file
if not f:
    with open(CREDENTIAL_FILE, "w") as file:
        json.dump(me, file)
    

def send_money(amount, target, message):
    """
    Sends money to people with Venmo
    :param amount: double: The amount to send to the target
    :param target: string: The username of the person to receive the money
    :param message: string: The message for the transaction
    :return:
    """
    if target[0] == '@':
        target = target[1:]

    target = venmo.user.search_for_users(target)[0].id  # search for users (there should only be one) -> the first one -> get id
    
    final_amount = float(round(amount, 2))
    venmo.payment.send_money(
        final_amount,
        message,
        target
    )


def charge_money(amount, target, message):
    """
    Requests money from people with Venmo
    :param amount: double: The amount to send to the target
    :param target: string: The username of the person to receive the money
    :param message: string: The message for the transaction
    :return:
    """
    if target[0] == '@':
        target = target[1:]

    target = venmo.user.search_for_users(target)[0].id  # search for users (there should only be one) -> the first one -> get id
    
    final_amount = float(round(amount, 2))
    venmo.payment.request_money(
        final_amount,
        message,
        target
    )


def logout():
    venmo.log_out(access_token)

if __name__ == '__main__':
    #charge_money(.01, 'Kristen-Lockhart-10', "Python Testing")
    logout()