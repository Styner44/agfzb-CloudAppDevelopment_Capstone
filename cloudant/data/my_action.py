import json
from urllib.parse import urlparse
from cloudant.client import Cloudant  # This is the import statement

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