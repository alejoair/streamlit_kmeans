from bs4 import BeautifulSoup as bs
import re
import pandas as pd

def preprocesar(f):

	html_doc = f.read()
	soup = bs(html_doc, 'html.parser')
	tabla = soup.find_all("table")

	cols = {}
	orden = []
	ordennums = []
	for ind, row in enumerate(tabla[1]):
		if ind==1:
			for col in row:
				cols[col.text] = []
				orden.append(col.text)
		if ind==3:
			cadena = row.td.attrs["title"]
			r = re.findall(r"(\S*)=", cadena)
			for m in r:
				cols[m] = []
				ordennums.append(m)

		if ind>1:
			try:
				row.td
				cadena = row.td.attrs["title"]
				r = re.findall(r"=([^\s]*);", cadena)
				for i, num in enumerate(r):
					cols[ordennums[i]].append(num)
			except:
				continue
			for i, td in enumerate(row.find_all("td")):
				cols[orden[i]].append(td.text)

	df=pd.DataFrame(cols).set_index("Pass")
	for col in df.columns:
		df[col]= df[col].map(lambda x: str(x).replace('\n',''))
		df[col]= df[col].map(lambda x: str(x).replace(',','.')).astype(float)

	print(df.columns)
	return df
	
