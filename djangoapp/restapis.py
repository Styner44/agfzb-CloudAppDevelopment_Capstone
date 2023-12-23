import requests
import json
from requests.auth import HTTPBasicAuth
from djangoapp.models import DealerReview

# Define the missing variable
api_key = "your_api_key"

# Define the get_request function
# Cloudant credentials
cloudant_username = '41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix'
cloudant_api_key = 'AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8'

def get_request(url, **kwargs):
    print("GET from {}".format(url))
    print("With params: {}".format(kwargs))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth(cloudant_username, cloudant_api_key))
        status_code = response.status_code
        print("With status {}".format(status_code))
        return response.json()
    except:
        print("Network exception occurred")
        return {}

def post_request(url, payload=None, headers=None):
    headers = headers or {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(cloudant_username, cloudant_api_key))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error in post_request: {}".format(e))
        return {}

def get_dealers_from_cf(url):
    try:
        data = get_request(url)
        dealers = []
        if 'docs' in data:
            for doc in data['docs']:
                dealer = {
                    'id': doc['id'],
                    'name': doc['name'],
                    'city': doc['city'],
                    'state': doc['state'],
                    'st': doc['st'],
                    'address': doc['address'],
                    'zip': doc['zip'],
                    'lat': doc['lat'],
                    'long': doc['long'],
                    'short_name': doc['short_name'],
                    'dealer_type': doc['dealer_type'],
                }
                dealers.append(dealer)
        return dealers
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

def get_dealer_reviews_from_cf(url, dealerId):
    try:
        data = get_request(
            url,
            params={'dealerId': dealerId},
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(cloudant_username, cloudant_api_key)
        )
        reviews = []
        if 'docs' in data:
            for doc in data['docs']:
                review = DealerReview(
                    dealership=doc['dealership'],
                    name=doc['name'],
                    purchase=doc['purchase'],
                    review=doc['review'],
                    purchase_date=doc['purchase_date'],
                    car_make=doc['car_make'],
                    car_model=doc['car_model'],
                    car_year=doc['car_year'],
                    sentiment=doc['sentiment'],
                    id=doc['id'],
                )
                reviews.append(review)
        return reviews
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

# Other imports and functions remain unchanged

# Watson NLU credentials
watson_nlu_api_key = 'KidOOw8m-hso_lc2AgTMLdxmudJdgaJAe-dewXr62x1L'
watson_nlu_url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ea601f46-3769-4375-85f1-9c79b2d0f580'

def analyze_review_sentiments(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + watson_nlu_api_key
    }
    try:
        response = post_request(watson_nlu_url, payload={'text': text}, headers=headers)
        return response.get('sentiment', {}).get('label', 'Unknown')
    except Exception as e:
        print("Error in analyze_review_sentiments: {}".format(e))
        return 'Unknown'

# Remaining parts of the restapis.py remain unchanged
