from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import pymysql
#needed to convert unicode to numeric
import unicodedata

TEAM_STATS_TABLE_COLUMN_NAME = ['game','team','tassistant','tblock','tfieldg','tfieldg3',
								'tfieldg3_pct','tfreethrow_attempt','toffebound','tpersonal_foul',
								'tpoints','tsteal','tturnover','ttotal_reb','tfieldg_attempt','tfreethrow','tfieldg3_attempt',
								'tfreethrow_pct','tfieldg_pct']

TEAM_ABBREV = ["GSW","OKC","HOU","LAC","SAS","DAL","LAL","PHO","MEM","NOP","DEN",
				"MIN","SAC","POR","UTA","CLE","TOR","MIA","ATL","BOS","CHO","IND","DET",
				"CHI","WAS","ORL","MIL","NYK","BRK","PHI"]

TEAM_NAME = ['Golden State Warriors','Oklahoma City Thunder','Houston Rockets','Los Angeles Clippers',
			'San Antonio Spurs','Dallas Mavericks','Los Angeles Lakers','Phoenix Suns','Memphis Grizzlies',
			'New Orleans Hornets','Denver Nuggets','Minnesota Timberwolves','Sacramento Kings','Portland Trail Blazers',
			'Utah Jazz','Cleveland Cavaliers','Toronto Raptors','Miami Heat','Atlanta Hawks','Boston Celtics','Charlotte Bobcats'
			'Indiana Pacers','Detroit Pistons','Chicago Bulls','Washington Wizards','Orlando Magic','Milwaukee Bucks','New York Knicks',
			'New Jersey Nets','Philadelphia 76ers']

NEW_TEAM_ABBREV = {'CHA':'CHO','NJN':'BRK','NOH':'NOP'}

NEW_TEAM_NAME = {'Charlotte Hornets':'CHO','Brooklyn Nets':'BRK','New Orleans Pelicans':'NOP'}

def srapping_game_data(leb):
	req = requests.get(leb)
	text = BeautifulSoup(req.text, "html.parser")
	stats = text.find('table', {'id': 'tgl_basic'})
	if(stats == None):
		return False
	else:
		cols = [i.get_text() for i in stats.thead.find_all('th')][2:]  
		cols = [x.encode('UTF8') for x in cols]    
		rows = [i.get_text().split('\n') for i in stats.tbody.find_all('tr')] 
		return rows

def get_team_stats_info(rows,team_abbrev):
	team_stats_info = []
	Date = rows[3]
	points = rows[7]
	Fieldg = rows[9]
	Fieldg_attempts = rows[10]
	Fieldg_pct = rows[11]
	Fieldg3 = rows[12]
	Fieldg3_attempt = rows[13]
	Fieldg3_pct = rows[14]
	Freethrow = rows[15]
	Freethrow_attempt = rows[16]
	Freethrow_pct = rows[17]
	orb = rows[18]
	trb = rows[19]
	ast = rows[20]
	stl = rows[21]
	blk = rows[22]
	tov = rows[23]
	pf = rows[24]
	team_stats_info.append(Date)
	team_stats_info.append(team_abbrev)
	team_stats_info.append(ast)
	team_stats_info.append(blk)
	team_stats_info.append(Fieldg)
	team_stats_info.append(Fieldg3)
	team_stats_info.append(Fieldg3_pct)
	team_stats_info.append(Freethrow_attempt)
	team_stats_info.append(orb)
	team_stats_info.append(pf)
	team_stats_info.append(points)
	team_stats_info.append(stl)
	team_stats_info.append(tov)
	team_stats_info.append(trb)
	team_stats_info.append(Fieldg_attempts)
	team_stats_info.append(Freethrow)
	team_stats_info.append(Fieldg3_attempt)
	team_stats_info.append(Freethrow_pct)
	team_stats_info.append(Fieldg_pct)
	return team_stats_info

def team_stats_table(team_stats_info,cur):
	team_stats_info_check = []
	for i in team_stats_info:
		if(not (i in team_stats_info_check)):
			team_stats_info_check.append(i)
			if len(i) != 0:
				output1 = create_insert_string("team_stats",i,TEAM_STATS_TABLE_COLUMN_NAME) 
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
	for year in range (2010,2017):
		all_team_stats_info = []
		for team in TEAM_ABBREV:
			leb = 'http://www.basketball-reference.com/teams/'+team+'/'+str(year)+'/gamelog/'
			if(srapping_game_data(leb) == False):
				if(team in NEW_TEAM_ABBREV):
					leb = 'http://www.basketball-reference.com/teams/'+NEW_TEAM_ABBREV[team]+'/'+str(year)+'_games.html'
					rows = srapping_game_data(leb) 
					if(rows!=False):
						team = NEW_TEAM_ABBREV[team]
						for i in range(len(rows)):
							if (rows[i][1] != "Rk" and len(rows[i])>10):
								all_team_stats_info.append(get_team_stats_info(rows[i],team))

			else:
				rows = srapping_game_data(leb)
				for i in range(len(rows)):
					if (rows[i][1] != "Rk" and len(rows[i])>10):
						all_team_stats_info.append(get_team_stats_info(rows[i],team))
						#team_stats_table(get_team_stats_info(rows[i],team),cur) 
		team_stats_table(all_team_stats_info,cur)
	cur.close()
	conn.close() 
main()