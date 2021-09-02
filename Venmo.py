from datetime import datetime, timedelta
from General_Packages import privacy_decoder, send_sms
import venmo_api
import json, os, errno, re

# Venmo documentation: https://pypi.org/project/venmo-api/

here = os.path.join(
    os.sep, "home", "david", "Documents", "projects", "PublixInvoice"
)

###### Build Venmo client from credential file
def make_venmo():
    CREDENTIAL_FILE = os.path.join(here, ".key", "venmo_login")

    # Get login credentials
    try:
        with open(CREDENTIAL_FILE, "r") as file:
            me = json.load(file)

    # If no credential file, get credentials from user
    except FileNotFoundError:
        try:
            os.mkdir(os.path.join(os.getcwd(), ".key"))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise exec
            pass
        me = [input("Venmo username: "), input("Venmo password: ")]
        # See if the device_id can be stolen from the logs
        try:
            with open("output_logs", "r") as file:
                log = file.read()
                me.append(re.findall(r"device-id: \w+-\w+-\w+-\w+-\w+", log)[-1])
        except:
            me.append("<No Device ID in logs>")

    # Create Venmo token
    try:
        access_token = me[3]

    # If access_token not saved
    except IndexError:
        try:
            access_token = venmo_api.Client.get_access_token(
                username=me[0], password=me[1]
            )
            me.append("<REPLACE THIS WITH A VALID DEVICE ID>")
            me.append(access_token)
            client = venmo_api.Client(access_token=access_token)

        except:
            send_sms("Venmo login failed.")
    # If access_token is saved
    else:
        try:
            client = venmo_api.Client(access_token=access_token)

        # If the saved access_token is bad, get a new one
        except:
            me[3] = venmo_api.Client.get_access_token(
                username=me[0], password=me[1], device_id=me[2]
            )
            try:
                client = venmo_api.Client(access_token=me[3])
            except:
                send_sms("Venmo login failed.")

    # Make/update credential file
    with open(CREDENTIAL_FILE, "w") as file:
        json.dump(me, file)

    return client

venmo = make_venmo()


def get_user(user):
    if user[0] == "@":
        user = user[1:]

    target = venmo.user.search_for_users(user)[
        0
    ].id  # search for users (there should only be one) -> the first one -> get id

    return target


def send_money(amount, target, message):
    """
    Sends money to people with Venmo
    :param amount: double: The amount to send to the target
    :param target: string: The username of the person to receive the money
    :param message: string: The message for the transaction
    :return:
    """
    target = get_user(target)

    final_amount = float(round(amount, 2))
    venmo.payment.send_money(final_amount, message, target)


def charge_money(amount, target, message):
    """
    Requests money from people with Venmo
    :param amount: double: The amount to send to the target
    :param target: string: The username of the person to receive the money
    :param message: string: The message for the transaction
    :return:
    """
    target = get_user(target)

    final_amount = float(round(amount, 2))

    # print(final_amount, target, message)
    venmo.payment.request_money(final_amount, message, target)


if __name__ == "__main__":
    charge_money(0.01, "Kristen-Lockhart-10", "Python Testing")
    # logout()
    pass
