import json
from googleapiclient.discovery import build

# Set up the API client
service = build('customsearch', 'v1', developerKey='95514ab5701b455481b8e2f3abedbf16')

# Set the query string
query = 'YOUR_QUERY_STRING'

# Make the search request
response = service.cse().list(q=query, cx='YOUR_CSE_ID').execute()

# Print the results
print(json.dumps(response, indent=2))
