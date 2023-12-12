import json
from urllib.parse import urlparse
from cloudant.client import Cloudant
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import FunctionsV1

def main(dict):
    url = urlparse(dict["COUCH_URL"])
    account_name = url.netloc.split('.')[0]
    client = Cloudant.iam(
        account_name=account_name,
        api_key=dict["IAM_API_KEY"],
        connect=True,
    )
    dbs = client.all_dbs()
    return {"dbs": dbs}

# Read the JSON file
with open('../../functions/.creds.json', 'r') as f:
    credentials = json.load(f)

# Call the main function with the credentials
print(main(credentials))

# Use the IBM Cloud API key from the credentials
authenticator = IAMAuthenticator(credentials["IAM_API_KEY"])
functions = FunctionsV1(authenticator=authenticator)

response = functions.list_actions().get_result()

actions = response['actions']
for action in actions:
    print(action['name'])