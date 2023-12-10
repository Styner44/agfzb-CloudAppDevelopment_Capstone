import json
from cloudant.client import Cloudant

def main(dict):
    client = Cloudant.iam(
        account_name=dict["username"],
        api_key=dict["apikey"],
        connect=True,
    )
    dbs = client.all_dbs()
    return {"dbs": dbs}

# Read the JSON file
with open('.creds.json', 'r') as f:
    credentials = json.load(f)

# Call the main function with the credentials
print(main(credentials))