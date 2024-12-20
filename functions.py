# generate random number
# function definition,takes no argument
def gen_random():
    import random
    # random is used to generate random numbers and make random selection
    import string
    # it provides a collection of string constants, including digits, letters
    # initiallize the size of 
    N=6
    # N is set to 6, specifies the length of string
    # generate a random string
    res = ''.join(random.choices(string.digits, k=N))
    # ''.join() it concatitnates the random strings to single string
    # print the result
    print("The generated string is: "+str(res))
    return str(res)
# gen_ramdom()

# check phone validity
import re
# its a module that provides support for working with regular expressions.
def check_phone(phone):
    # the function takes one argument phone
    regex = "^\+254\d{9}"
    # ^ it asserts the start of the string
    #\+254 it matches the literal string +254
    #\d{9} it matches a exactly nine digits
    if not re.match(regex,phone)or len(phone) != 13:
        print("Phone is not valid")
        return False
    else:
        print("Phone is Valid, OK")
        return True
    
# check_phone ("+254114373702")
    
# check password validity+assword is not valid
import re
def password_validity(password):
    if len(password) < 8:
        return("Password is too short")
    elif not re.search("[A-Z]",password):
        return("Password must contain atleast an uppercase letter")
    elif not re.search("[a-z]",password):
        return("Password must contain atleast a lowercase letter")
    elif not re.search("[0-9]",password):
        return("Password must contain atleast a digit")
    elif not re.search("[@#$%&]",password):
        return("Password must contain atleast a special character")
    else:
        return True
    
# password_validity(input("Enter your password: "))
    
# sending an sms
import africastalking
africastalking.initialize(
username="joe2022",
api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#justpaste.it/1nua8
)
sms = africastalking.SMS
def send_sms(phone,message):
    recipients = [phone]
    sender = "AFRICASTALKING"
    try:
        response = sms.send(message,recipients)
        print(response)
    except Exception as error:
        print("Error is :",error)

# send_sms("+254114373701", "This is my message")


# hash password
import bcrypt
# bcrypt is a module for hashing and checking passwords
# it is very secure
def hash_password(password):
    bytes = password.encode("utf-8")
    # password is encoded into bytes 
    # it is necessary because bcrypt library works well with byte data
    # print(bytes)
    salt = bcrypt.gensalt()
    # using a unique salt for each password ensures that even if two users have same passwords, their hashed password will be different
    # print(salt)
    hash = bcrypt.hashpw(bytes,salt)
    # print(hash)
    return hash.decode()

# hash_password(input("Enter your password: "))

# verify password
def hash_verify(password,hash_password):
    bytes = password.encode("utf-8")
    result = bcrypt.checkpw(bytes,hash_password.encode("utf-8"))
    print(result)
    return result

# hash_verify("1234","$2b$12$i40MHuWDL6IMDZGzKcEBUesUmF6quGCkvqAqdKuMiMJ3rok7P53t6")

# encrypt data
from cryptography.fernet import Fernet
# we import fernet class
# the module is used for encryption and decryption
def generate_key():
    # its a function used to generate a new encryption key
    key = Fernet.generate_key()
    # print(key)
    with open("key.key", "wb") as key_file:
    # with open it opens a new file if it exists
    # creates a new file if it doesnt exist
    # wb(write binary) ensures the file is properly closed after writing on it
        key_file.write(key)

# generate_key()
# load key
def load_key():
    return open("key.key", "rb").read()
# it reads the entire content of the file

# load_key()

# encrypt data
def encypt(data):
    key = load_key()
    fernet = Fernet(key)
    # print(fernet)
    # this creates a fernet object for encryption
    encypt_data = fernet.encrypt(data.encode())
    return (encypt_data.decode())
# encypt("1234") 


# decrypt data
def decrypt(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return(decrypted_data.decode())

# decrypt("gAAAAABmUELDvvXXgXB97jGaB26jhrWLAFf7nj_Fnq39BCfaXVYbFZr5SsG9_KwrORzW8g6XIueYiuZ5H2OOCwNwgPvFScDE7w==")
import  requests
import base64
import datetime
from requests.auth import HTTPBasicAuth    
def mpesa_payment(amount, phone, invoice_no):
        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)