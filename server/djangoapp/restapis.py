import requests
import requests
from requests.auth import HTTPBasicAuth
from djangoapp.models import CarDealer, DealerReview

# Define the missing variable
api_key = "your_api_key"

# Create a `get_request` to make HTTP GET requests
def get_request(url, params=None, headers=None, auth=None):
    try:
        response = requests.get(url, params=params, headers=headers, auth=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    response = get_request(url, params=kwargs, headers={'Content-Type': 'application/json'},
                          auth=HTTPBasicAuth('apikey', api_key))
    json_result = response.json()
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    # Call get_request() with specified arguments
    response = get_request(url, params={'dealerId': dealerId}, headers={'Content-Type': 'application/json'},
                          auth=HTTPBasicAuth('apikey', api_key))
    # Parse JSON results into a DealerReview object list
    dealer_reviews = [DealerReview(review['id'], review['comment']) for review in response.json()]
    return dealer_reviews

# Create a post_request method to make HTTP POST requests
def post_request(url, payload=None, headers=None, auth=None):
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
    return response

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # Call post_request() to analyze text
    response = post_request('https://watson-nlu-api', payload={'text': text}, headers={'Content-Type': 'application/json'})
    # Get the returned sentiment label such as Positive or Negative
    sentiment_label = response.get('sentiment', 'Unknown')
    return sentiment_label