from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np


#needed to convert unicode to numeric
import unicodedata

#open file for writing
in_file = open("./NewPlayer.txt","r")

for line in in_file:
	line = line.strip()
	#regular season data
	leb = 'http://www.basketball-reference.com/players/'+line[0]+'/'+line+'/'+'gamelog/2016/'
	#######
	#lebron
	#######
	player_string_key = leb
	req = requests.get(player_string_key)
	text = BeautifulSoup(req.text, "html.parser")
	print(text)
	stats = text.find('table', {'id': 'pgl_basic'})

	# find the schema
	cols = [i.get_text() for i in stats.thead.find_all('th')]  

	# convert from unicode to string
	cols = [x.encode('UTF8') for x in cols]                    


	#these are schema with empty string names
	cols[5]='home_away'
	cols[7]='win-loss'

	# get rows
	rows = [i.get_text().split('\n') for i in stats.tbody.find_all('tr')] 


	# convert rows to strings
	for i in range(len(rows)):
	    rows[i] = [x.encode('UTF8') for x in rows[i]]                          


	#rows=rows[1:-1]

	short = []

	for i in range(len(rows)):
	    if len(rows[i]) < 31:
	        short.append(i)

	#print (short)    

	 
	new_rows = []

	for i in range(len(rows)):
	    if i in short:
	        continue
	    else:
	        new_rows.append(rows[i])
	#print(new_rows)

	l = range(len(new_rows))