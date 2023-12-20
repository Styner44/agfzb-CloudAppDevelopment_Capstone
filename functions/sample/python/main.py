"""IBM Cloud Function that retrieves reviews for a specific dealership

Returns:
  List: List of reviews for the given dealership
"""
from cloudant import Cloudant
from cloudant import CloudantException
import requests


def main(param_dict):
  """Main Function

  Args:
    param_dict (Dict): input parameter

  Returns:
    List: List of reviews for the given dealership
  """
  try:
    client = Cloudant.iam(
      account_name=param_dict["COUCH_USERNAME"],
      api_key=param_dict["IAM_API_KEY"],
      connect=True,
    )
    db = client['reviews']  # Access the 'reviews' database
  except CloudantException as cloudant_exception:
    print("unable to connect")
    return {"error": cloudant_exception}
  except (requests.exceptions.RequestException, ConnectionResetError) as err:
    print("connection error")
    return {"error": err}

  # Validate the presence of the dealership_id parameter
  if "dealership_id" not in param_dict:
    print("Missing required parameter: dealership_id")
    return {"error": "Missing dealership_id"}

  # Extract the dealership ID
  dealership_id = param_dict["dealership_id"]

  # Build the query selector
  selector = {"dealership_id": dealership_id}

  # Retrieve matching reviews
  docs = db.get_query_result(selector)

  # Convert the query result to a list of dictionaries
  reviews = list(docs)

  return reviews


credentials = {
  "COUCH_USERNAME": "41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix",
  "IAM_API_KEY": "Udq3_mK0zxdnBA4cx2bBE045ZYD2BtzGF5tGT20fFKOh",
  "dealership_id": 123  # Replace with the actual dealership ID
}

print(main(credentials))
