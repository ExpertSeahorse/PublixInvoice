from datetime import datetime, timedelta
from General_Packages import privacy_decoder, send_sms
import venmo_api
import json, os

# Venmo documentation: https://pypi.org/project/venmo-api/

with open(os.path.join("key", "venmo_login"), "r") as file:
    me = json.load(file)

try:
    access_token = me[3]
    venmo = venmo_api.Client(access_token=access_token)
except IndexError: 
    try:
        access_token = venmo_api.Client.get_access_token(username=me[0],
                                                        password=me[1], 
                                                        device_id=me[2])
        venmo = venmo_api.Client(access_token=access_token)
        
        me.append(access_token)
        with open(os.path.join("key", "venmo_login"), "w") as file:
            json.dump(me, file)

    except:
        send_sms("Venmo login failed.")


def send_money(amount, target, message):
    """
    Sends money to people with Venmo
    :param amount: The amount to send to the target
    :param target: The username of the person to receive the money
    :param message: The message for the transaction
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
    :param amount:
    :param target:
    :param message:
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
    logout()