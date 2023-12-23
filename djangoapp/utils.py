import requests
import json
import logging
logger = logging.getLogger(__name__)

def get_dealer_reviews_from_cf():
    # Implementation for retrieving dealer reviews from CF
    pass

def get_dealers_from_cf():
    # Load credentials from JSON file
    with open('.creds.json', 'r') as f:
        creds = json.load(f)
    iam_api_key = creds['IAM_API_KEY']

    # Get IAM token
    iam_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': iam_api_key}
    )
    iam_response.raise_for_status()  # Ensure the request was successful
    iam_token = iam_response.json()['access_token']

    # Make request to Cloud Function
    url = 'https://us-south.functions.cloud.ibm.com/api/v1/namespaces/54ee907b-434c-4f03-a1b3-513c235fbeb4/actions/myAction'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {iam_token}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Error getting dealers from cloud function: {response.status_code}")
        return []
