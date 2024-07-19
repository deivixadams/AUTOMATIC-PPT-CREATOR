import requests
from PIL import Image
from io import BytesIO

# Define the endpoint URL
url = f'https://pixabay.com/api/?key={pixabay_api_key}&q=beach&image_type=photo'

# Send a GET request to the Pixabay API
response = requests.get(url)

# Parse the JSON response
data = json.loads(response.text)

# Get the URL of the first image
image_url = data['hits'][0]['largeImageURL']

# Make a get request to the image url
response = requests.get(image_url)

# Load the image from the response
img = Image.open(BytesIO(response.content))

# Save the image
img.save('beach_image.jpg')