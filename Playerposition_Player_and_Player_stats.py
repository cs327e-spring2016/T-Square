import csv
import basketballCrawler as bc
import json
from bs4 import BeautifulSoup
import pymysql

import requests
import unicodedata
PLAYER_TABLE_COLUMN_NAME =["player_id","name","height","weight"]
PLAYER_POSITION_TABLE_COLUMN_NAME = ["player_id","position"]
PLAYER_STATS_TABLE_COLUMN_NAME = ["player_id","assistant","block","fieldg","fieldg3","fieldg3_pct","freet_attemp","minute_played","offrebound","personal_foul","points",
								  "steal","turnover","total_reb","fieldg_attempt","freethrow","fieldg3_attempt","fieldg_pct","freethrow_pct","game_date","derebound"]


def get_player_info(name,players):
	player_info = []
	playerurl = players[name].gamelog_url_list	
	player_id = (playerurl[0])[46:55].strip('/')
	player_info.append(player_id)
	player_info.append(name)
	player_info.append(players[name].height)
	player_info.append(players[name].weight)
	player_info.append(players[name].positions)
	return player_info


def player_table(player_info,cur):
	player_table_info = []
	player_table_info = player_info[0:len(player_info)-1]
	output1 = create_insert_string("player",player_table_info,PLAYER_TABLE_COLUMN_NAME) 
	# print(output1)
	cur.execute(output1)
	cur.connection.commit()

	# print(player_table_info)
	for i in player_info[len(player_info)-1]:
		player_position_table_info = []
		player_position_table_info.append(player_info[0])
		player_position_table_info.append(i)
		output2 = create_insert_string("player_position",player_position_table_info,PLAYER_POSITION_TABLE_COLUMN_NAME)
		# print(output2)
		cur.execute(output2)
		cur.connection.commit()

def get_player_stats_info(rows,player_id):
	player_stats_info = []
	if (len(rows) < 30):
		Date = rows[2]
		for i in range(len(PLAYER_STATS_TABLE_COLUMN_NAME)):
			player_stats_info.append(None)
		player_stats_info[0] = player_id
		player_stats_info[-2] = Date
	else:
		Date = rows[2]
		Minutes_played = rows[9]
		Fieldg = rows[10]
		Fieldg_attempts = rows[11]  
		Fieldg_pct = rows[12]
		Fieldg3 = rows[13]
		Fieldg3_attempt = rows[14]
		Fieldg3_pct = rows[15]
		Freethrow = rows[16]
		Freethrow_attempt = rows[17]
		Freethrow_pct = rows[18]
		orb = rows[19]
		drb = rows[20]
		trb = rows[21]
		ast = rows[22]
		stl = rows[23]
		blk = rows[24]
		tov = rows[25]
		pf = rows[26]
		pts = rows[27]
		player_stats_info.append(player_id)
		player_stats_info.append(ast)
		player_stats_info.append(blk)
		player_stats_info.append(Fieldg)
		player_stats_info.append(Fieldg3)
		player_stats_info.append(Fieldg3_pct)
		player_stats_info.append(Freethrow_attempt)
		player_stats_info.append(Minutes_played)
		player_stats_info.append(orb)
		player_stats_info.append(pf)
		player_stats_info.append(pts)
		player_stats_info.append(stl)
		player_stats_info.append(tov)
		player_stats_info.append(trb)
		player_stats_info.append(Fieldg_attempts)
		player_stats_info.append(Freethrow)
		player_stats_info.append(Fieldg3_attempt)
		player_stats_info.append(Fieldg_pct)
		player_stats_info.append(Freethrow_pct)
		player_stats_info.append(Date)
		player_stats_info.append(drb)
	return player_stats_info


def player_stats_table(player_stats_info,cur):
	output1 = create_insert_string("player_stats",player_stats_info,PLAYER_STATS_TABLE_COLUMN_NAME) 
	# print(output1)
	cur.execute(output1)
	cur.connection.commit()


def create_insert_string(table_name,column_value,column_name):
	insert_string = "INSERT INTO "+table_name +"("
	for i in column_name:
		insert_string += i
		if(i!=column_name[len(column_name)-1]):
			insert_string += ','
	insert_string += ") VALUES ("

	for i in range(len(column_value)):
		if column_value[i] is None or column_value[i] == '':
			insert_string += "null"
		else:
			insert_string += '"'+ column_value[i] +'"'	
		if(i!=len(column_value)-1):
			insert_string += ','
	insert_string += ");"
	return insert_string

def main():
	conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
	                       user='root', passwd='15174903378', db='NBA')
	cur = conn.cursor()
	players = bc.loadPlayerDictionary("players.json")
	urllist = []
	for name in players:
		playerurl = players[name].gamelog_url_list

		player_table(get_player_info(name,players),cur)

		for item in playerurl:
			urllist.append(item)
	#gete the column headers and find the schema
	leb = urllist[0]
	player_string_key = leb

	req = requests.get(player_string_key)
	text = BeautifulSoup(req.text, "html.parser")
	stats = text.find('table', {'id': 'pgl_basic'})
	cols = [i.get_text() for i in stats.thead.find_all('th')]  
	# convert from unicode to string
	cols = [x.encode('UTF8') for x in cols]                    
	#these are schema with empty string names
	cols[5]='home_away'
	cols[7]='win-loss'
	rows = []
	for item in urllist:
		leb = item
		player_string_key = leb
		player_id = leb[46:55].strip('/')
		req = requests.get(player_string_key)
		text = BeautifulSoup(req.text, "html.parser")
		stats = text.find('table', {'id': 'pgl_basic'})
		rows = []
		for i in stats.tbody.find_all('tr'):
			app = []
			for j in i.find_all('td'):
				app.append(j.get_text())
			rows.append(app)
		for i in range(len(rows)):
			if (len(rows[i])!= 0 ):
			#if (rows[i][1] != "Rk"):
				player_stats_table(get_player_stats_info(rows[i],player_id),cur) 

	cur.close()
	conn.close()

main()
