import os

# URL of the ncryptify service - can be overridden but currently defaults to the staging ncryptify service
NCRYPTIFY_URL = os.getenv('NCRYPTIFY_URL', 'https://api.ncryptify.com/v1')
