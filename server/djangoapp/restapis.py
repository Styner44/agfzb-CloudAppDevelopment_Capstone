import requests
import json
from requests.auth import HTTPBasicAuth

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

# Create a `post_request` to make HTTP POST requests
def post_request(url, payload=None, headers=None):
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    # Call get_request() with specified arguments
    response = get_request(url, params=kwargs, headers={'Content-Type': 'application/json'},
                           auth=HTTPBasicAuth('apikey', api_key))
    # Parse JSON results into a CarDealer object list
    car_dealers = [CarDealer(dealer['id'], dealer['name']) for dealer in response.json()]
    return car_dealers

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    # Call get_request() with specified arguments
    response = get_request(url, params={'dealerId': dealerId}, headers={'Content-Type': 'application/json'},
                           auth=HTTPBasicAuth('apikey', api_key))
    # Parse JSON results into a DealerView object list
    dealer_reviews = [DealerView(review['id'], review['comment']) for review in response.json()]
    return dealer_reviews

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # Call post_request() to analyze text
    response = post_request('https://watson-nlu-api', payload={'text': text}, headers={'Content-Type': 'application/json'})
    # Get the returned sentiment label such as Positive or Negative
    sentiment_label = response.get('sentiment', 'Unknown')
    return sentiment_label
