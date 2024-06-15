import requests
from bs4 import BeautifulSoup
import pandas as pd

#url = "https://en.wikipedia.org/wiki/2021_FIVB_Men%27s_Volleyball_Nations_League"
#url = "https://en.wikipedia.org/wiki/2022_FIVB_Men%27s_Volleyball_Nations_League"
url = "https://en.wikipedia.org/wiki/2023_FIVB_Men%27s_Volleyball_Nations_League"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})

data = []
for table in tables:
   if table.get('width') == '95%':
       headers = [th.text.strip() for th in table.find_all('th')]
       rows = table.find_all('tr')[1:]
       for row in rows:
           cells = row.find_all(['td', 'th'])
           cells = [cell.text.strip() for cell in cells[0:5]]
           data.append(cells)

headers= ['date','hour','Team A','result','Team B']
df = pd.DataFrame(data, columns=headers)
df.to_csv('python/vnl_2023_results.csv', index=False)
