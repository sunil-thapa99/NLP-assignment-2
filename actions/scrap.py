import time
import requests
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'https://www.kijiji.ca/'


start_page = 1
address = ''
room_and_rental_term_url = BASE_URL + f'b-for-rent/city-of-toronto/{address}/page-2/k0c30349001l1700273'