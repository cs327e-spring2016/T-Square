from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

import re
import pymysql
#needed to convert unicode to numeric
import unicodedata

#open file for writing
#in_file = open("./NewPlayer.txt","r")


#for line in in_file:
	#line = line.strip()
	#regular season data
leb = 'http://www.basketball-reference.com/players/j/jamesle01/gamelog/2016/'
#######
#lebron
#######
player_string_key = leb
req = requests.get(player_string_key)
text = BeautifulSoup(req.text, "html.parser")
stats = text.find('table', {'id': 'pgl_basic'})

# find the schema
cols = [i.get_text() for i in stats.thead.find_all('th')][2:]  

# convert from unicode to string
cols = [x.encode('UTF8') for x in cols]                    


#these are schema with empty string names
cols[5]='home_away'
cols[7]='win-loss'

# get rows
rows = [i.get_text().split('\n') for i in stats.tbody.find_all('tr')] 


'''
# convert rows to strings
for i in range(len(rows)):
    rows[i] = [x.decode('UTF8') for x in rows[i]]   
rows=rows[1:-1]
'''
'''
#row is a 2-D list, get every list of this 2-D list which is the 
#per game stats
for items in rows:
	print(len(items))
	#items is the list and get the data which is the element of this list
	Date = items[2]
	#print(Date)
	Minutes_played = items[10]
	#Fieldg = items[11]
	#print(items[11])
	#Fieldg_attempts = items[12]
'''



short = []
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                       user='root', passwd='15174903378', db='NBA')
cur = conn.cursor()
Player_id = "jamesle01"
for i in range(len(rows)):
    if ((len(rows[i]) < 31) or (rows[i][1]=="Rk")):
        short.append(i)   
    else:
    	Date = rows[i][3]
    	#Date = Date.strip()
    	#print(Player_id, Date)
    	Minutes_played = rows[i][10]
    	Fieldg = rows[i][11]
    	Fieldg = int(Fieldg)
    	Fieldg_attempts = rows[i][12]  
    	Fieldg_pct = rows[i][13]
    	print(Fieldg_pct)
    	Fieldg3 = rows[i][14]
    	Fieldg3 = int(Fieldg3)
    	Fieldg3_attempt = rows[i][15]
    	Fieldg3_pct = rows[i][16]
    	Freethrow = rows[i][17]
    	Freethrow_attempt = rows[i][18]
    	Freethrow_pct = rows[i][19]
    	orb = rows[i][20]
    	drb = rows[i][21]
    	trb = rows[i][22]
    	ast = rows[i][23]
    	stl = rows[i][24]
    	blk = rows[i][25]
    	tov = rows[i][26]
    	pf = rows[i][27]
    	pts = rows[i][28]
    	# cur.execute("INSERT INTO game (date) VALUES (%s)",(Date))
    	#cur.execute("INSERT INTO player_stats(player_id, game_date, assistant, block, dereound, fieldg, fieldg3,) VALUES  (%s, %s)", (Player_id, Date))

    	# cur.execute("INSERT INTO player_stats (player_id, game_date) VALUES (%s, %s)", (Player_id, Date))
    	cur.connection.commit()
cur.close()
conn.close()