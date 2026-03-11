import requests
import os
from dotenv import load_dotenv

load_dotenv()

# def get_salesforce_access_token():

#     import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

def get_salesforce_access_token():

    token_url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET"),
        "refresh_token": os.getenv("SF_REFRESH_TOKEN")
    }

    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Salesforce Token Refresh Failed: {response.text}")

    data = response.json()

    return data["access_token"], data["instance_url"]


def get_salesforce_access_token_ClientCred():

    url = f"{os.getenv('SF_INSTANCE_URL')}/services/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET")
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    data = response.json()

    return data["access_token"], data["instance_url"]

#def get_salesforce_access_token():
    # url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

    # payload = {
    #     "grant_type": "password",
    #     "client_id": os.getenv("SF_CLIENT_ID"),
    #     "client_secret": os.getenv("SF_CLIENT_SECRET"),
    #     "username": os.getenv("SF_USERNAME"),
    #     "password": os.getenv("SF_PASSWORD") + os.getenv("SF_SECURITY_TOKEN")
    # }

    # response = requests.post(url, data=payload)

    # if response.status_code != 200:
    #     raise Exception(f"Salesforce OAuth Error: {response.text}")

    # auth_response = response.json()

    # access_token = auth_response["access_token"]
    # instance_url = auth_response["instance_url"]

    # return access_token, instance_url