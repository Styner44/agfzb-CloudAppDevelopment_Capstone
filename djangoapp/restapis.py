import requests
from requests.auth import HTTPBasicAuth
from .models import DealerReview

# Define the missing variable
API_KEY = "AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8"

# Define the get_request function
# Cloudant credentials
CLOUDANT_USERNAME = '41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix'
CLOUDANT_API_KEY = 'AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8'

# Watson NLU credentials
WATSON_NLU_API_KEY = 'KidOOw8m-hso_lc2AgTMLdxmudJdgaJAe-dewXr62x1L'
WATSON_NLU_URL = (
    'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/'
    'ea601f46-3769-4375-85f1-9c79b2d0f580'
)

def get_request(url, api_key=False, **kwargs):
    """
    Make a GET request to the specified URL.
    """
    print(f"GET from {url}")
    try:
        headers = {'Content-Type': 'application/json'}
        if api_key:
            # Basic authentication GET
            response = requests.get(
                url,
                headers=headers,
                params=kwargs,
                auth=HTTPBasicAuth('apikey', api_key),
                timeout=10
            )
        else:
            # No authentication GET
            response = requests.get(
                url,
                headers=headers,
                params=kwargs,
                timeout=10
            )
        response.raise_for_status()  # If the request failed, this will raise a HTTPError
        return response.json()  # Return the JSON response from the server
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making GET request: {e}")
        return {}  # Return an empty dictionary when an exception occurs

def post_request(url, json_payload, auth_needed=True, **kwargs):
    """
    Make a POST request to the specified URL with the given JSON payload.
    - If auth_needed is True, use HTTP Basic Auth with Cloudant credentials.
    - kwargs can be used to pass additional parameters like headers.
    """
    headers = kwargs.get('headers', {'Content-Type': 'application/json'})

    # If authentication is needed, use HTTPBasicAuth
    if auth_needed:
        auth = HTTPBasicAuth(CLOUDANT_USERNAME, CLOUDANT_API_KEY)
    else:
        auth = None

    try:
        response = requests.post(
            url,
            json=json_payload,
            headers=headers,
            auth=auth,
            timeout=10,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in post_request: {e}")
        return {}

# ... [The rest of your existing methods]

def get_dealers_from_cf(url):
    """
    Get the list of dealers from the specified URL.
    """
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
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def analyze_review_sentiments(dealerreview):
    """
    Analyze the sentiment of a review text using Watson NLU.
    """
    text = dealerreview.review
    url = WATSON_NLU_URL + '/v1/analyze'
    params = {
        'text': text,
        'version': '2021-08-01',
        'features': 'sentiment',
        'return_analyzed_text': True
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + WATSON_NLU_API_KEY
    }
    try:
        response = post_request(url, json_payload=params, headers=headers)
        sentiment = response.get('sentiment', {}).get('label', 'Unknown')
        return sentiment
    except Exception as e:
        print(f"Error in analyze_review_sentiments: {e}")
        return 'Unknown'

def get_dealer_reviews_from_cf(url, dealer_id):
    """
    Get the reviews for a specific dealer from Cloudant.
    """
    try:
        data = get_request(url, params={'dealerId': dealer_id})
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
                    sentiment=analyze_review_sentiments(doc['review'])  # Analyze sentiment using Watson NLU
                )
                reviews.append(review)
        return reviews
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# Example usage
DEALERS_URL = (
    "https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud/"
    "dealers/_all_docs"
)
REVIEWS_URL = (
    "https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix.cloudantnosqldb.appdomain.cloud/"
    "reviews/_find"
)

# Get dealers from Cloudant
dealers_cf = get_dealers_from_cf(DEALERS_URL)
for dealer_cf in dealers_cf:
    print(dealer_cf)

# Get reviews for a specific dealer from Cloudant
DEALER_ID = "your-dealer-id"
reviews_cf = get_dealer_reviews_from_cf(REVIEWS_URL, DEALER_ID)
for review_cf in reviews_cf:
    print(review_cf)
