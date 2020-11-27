from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import dateparser as dateparser

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
    row = table.find_all('tr')[i]
    
    #get bulan
    period = row.find_all('td')[0].text
    period = period.strip()

    inflation = row.find_all('td')[2].text
    inflation = inflation.strip()

    temp.append((period,inflation))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Tanggal','Kurs'))

#insert data wrangling here
df['Kurs'] = df['Kurs'].apply(lambda x: x.replace(',', ''))
df['Kurs'] = df['Kurs'].apply(lambda x: x.replace(' IDR', ''))

df['Kurs'] = df['Kurs'].astype('float64')
df['Tanggal']=df['Tanggal'].apply(dateparser.parse)
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["Kurs"].mean()}'

	# generate plot
	ax = df.set_index('Tanggal').plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
