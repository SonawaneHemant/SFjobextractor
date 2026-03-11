import requests
import os
from dotenv import load_dotenv

load_dotenv()

def refresh_salesforce_token():

    token_url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET"),
        "refresh_token": "YOUR_SAVED_REFRESH_TOKEN"
    }

    response = requests.post(token_url, data=payload)

    data = response.json()

    return data["access_token"], data["instance_url"]


def get_salesforce_access_token():

    url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"

    payload = {
        "grant_type": "password",
        "client_id": os.getenv("SF_CLIENT_ID"),
        "client_secret": os.getenv("SF_CLIENT_SECRET"),
        "username": os.getenv("SF_USERNAME"),
        "password": os.getenv("SF_PASSWORD") + os.getenv("SF_SECURITY_TOKEN")
    }

    print("Calling Salesforce OAuth endpoint...")
    print("URL:", url)

    response = requests.post(url, data=payload)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        raise Exception(f"Salesforce OAuth Error: {response.text}")

    data = response.json()

    return data["access_token"], data["instance_url"]

from simple_salesforce import Salesforce
import os
from dotenv import load_dotenv

def login_salesforce():

    sf = Salesforce(
        username=os.getenv("SF_USERNAME"),
        password=os.getenv("SF_PASSWORD"),
        security_token=os.getenv("SF_SECURITY_TOKEN"),
        domain="test"   # sandbox
    )

    session_id = sf.session_id
    instance_url = sf.sf_instance
    print("\nSUCCESS!")
    return session_id, instance_url


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

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    data = response.json()

    return data["access_token"], data["instance_url"]

if __name__ == "__main__":

    print("Starting Salesforce authentication test...\n")

    #access_token, instance_url = get_salesforce_access_token()
    #session_id, instance_url=login_salesforce()
    access_token, instance_url = get_salesforce_access_token_ClientCred()
    sf = Salesforce(
    instance_url=instance_url,
    session_id=access_token
    )

    print("\nSUCCESS!")
    print("Access Token:", access_token)
    print("Instance URL:", instance_url)    
    # print("Session id:", session_id)
    # print("Instance URL:", instance_url)