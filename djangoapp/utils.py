import requests
import json
import logging
from requests.auth import HTTPBasicAuth

# Initialize logger
logger = logging.getLogger(__name__)

# Cloudant and IBM Cloud Function credentials and URLs
CLOUDANT_SERVICE_URL = "https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud"
DEALER_GET_SERVICE_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/54ee907b-434c-4f03-a1b3-513c235fbeb4/default/myAction"
CLOUDANT_API_KEY = "AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8"
CLOUDANT_USERNAME = "41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix"

def get_dealer_reviews_from_cf(dealer_id):
    """
    Retrieve dealer reviews from Cloudant given a dealer ID.
    """
    try:
        url = f"{CLOUDANT_SERVICE_URL}/reviews/_find"  # Adjust if necessary
        query = json.dumps({"selector": {"dealership": dealer_id}})
        auth = HTTPBasicAuth(CLOUDANT_USERNAME, CLOUDANT_API_KEY)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=query, headers=headers, auth=auth)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting dealer reviews from Cloudant: {e}")
        return []

def get_dealers_from_cf():
    """
    Retrieve dealers from IBM Cloud Function.
    """
    try:
        headers = {'accept': 'application/json'}
        response = requests.get(DEALER_GET_SERVICE_URL, headers=headers)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting dealers from IBM Cloud Function: {e}")
        return []

# Example usage
dealers = get_dealers_from_cf()
print("Dealers:", dealers)

# Replace 'your-dealer-id' with an actual dealer ID for testing
dealer_reviews = get_dealer_reviews_from_cf('your-dealer-id')
print("Dealer Reviews:", dealer_reviews)
