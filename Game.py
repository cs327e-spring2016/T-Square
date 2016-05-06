from bs4 import BeautifulSoup
import requests
import re
import pymysql
import unicodedata

MONTH = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

TEAM_ABBREV = ["GSW","OKC","HOU","LAC","SAS","DAL","LAL","PHO","MEM","NOH","DEN",
				"MIN","SAC","POR","UTA","CLE","TOR","MIA","ATL","BOS","CHA","IND","DET",
				"CHI","WAS","ORL","MIL","NYK","NJN","PHI"]

TEAM_NAME = ['Golden State Warriors','Oklahoma City Thunder','Houston Rockets','Los Angeles Clippers',
			'San Antonio Spurs','Dallas Mavericks','Los Angeles Lakers','Phoenix Suns','Memphis Grizzlies',
			'New Orleans Hornets','Denver Nuggets','Minnesota Timberwolves','Sacramento Kings','Portland Trail Blazers',
			'Utah Jazz','Cleveland Cavaliers','Toronto Raptors','Miami Heat','Atlanta Hawks','Boston Celtics','Charlotte Bobcats',
			'Indiana Pacers','Detroit Pistons','Chicago Bulls','Washington Wizards','Orlando Magic','Milwaukee Bucks','New York Knicks',
			'New Jersey Nets','Philadelphia 76ers']

NEW_TEAM_ABBREV = {'CHA':'CHO','NJN':'BRK','NOH':'NOP'}

NEW_TEAM_NAME = {'Charlotte Hornets':'CHO','Brooklyn Nets':'BRK','New Orleans Pelicans':'NOP'}

GAME_TABLE_COLUMN_NAME = ["date","host","guest","host_score","guest_score"]

def srapping_game_data(leb):
	req = requests.get(leb)
	text = BeautifulSoup(req.text, "html.parser")
	stats = text.find('table', {'id': 'teams_games'})
	if(stats == None):
		return False
	else:
		cols = [i.get_text() for i in stats.thead.find_all('th')][2:]  
		cols = [x.encode('UTF8') for x in cols]    
		rows = [i.get_text().split('\n') for i in stats.tbody.find_all('tr')] 
		for i in range(len(rows)):
			if(rows[i][1]!='G'):
				rows[i][2]=covert_date(rows[i][2])
		return rows

def covert_date(i):
	date = ((i.split(',')[1]).split(' ')[1:])
	date.append(i.split(',')[2])
	for i in range(len(MONTH)):
		if(date[0] == MONTH[i]):
			date[0] = str(i+1)
	return date[2]+'-'+date[0]+'-'+date[1]

def convert_team_name(item):

	for i in range(len(TEAM_NAME)):
		if item == TEAM_NAME[i]:
			return TEAM_ABBREV[i]
	return NEW_TEAM_NAME[item] if item in NEW_TEAM_NAME else False

def get_game_info(rows,team_abbrev):
	game_info = []
	date = rows[2]
	if(rows[6]!="@"):
		guest_name = convert_team_name(rows[7])
		host_score = rows[10]
		guest_score = rows[11]
		if(guest_name!=False):
			game_info.append(date)
			game_info.append(team_abbrev)
			game_info.append(guest_name)
			game_info.append(host_score)
			game_info.append(guest_score)
	else:
		guest_name = convert_team_name(rows[7])
		host_score = rows[10]
		guest_score = rows[11]
		if(guest_name!=False):
			game_info.append(date)
			game_info.append(guest_name)
			game_info.append(team_abbrev)
			game_info.append(guest_score)
			game_info.append(host_score)
	return game_info

def game_table (game_info, cur):
	game_info_check = []
	for i in game_info:
		if(not (i in game_info_check)):
			game_info_check.append(i)
			if len(i) != 0:
				output1 = create_insert_string("game",i,GAME_TABLE_COLUMN_NAME) 
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
	for year in range (1996,2017):
		all_game_info = []
		for team in TEAM_ABBREV:
			leb = 'http://www.basketball-reference.com/teams/'+team+'/'+str(year)+'_games.html'
			if(srapping_game_data(leb) == False):
				if(team in NEW_TEAM_ABBREV):
					leb = 'http://www.basketball-reference.com/teams/'+NEW_TEAM_ABBREV[team]+'/'+str(year)+'_games.html'
					rows = srapping_game_data(leb) 
					if(rows!=False):
						team = NEW_TEAM_ABBREV[team]
						for i in range(len(rows)):
							if (rows[i][1] != "G"):
								all_game_info.append(get_game_info(rows[i],team))
			else:
				rows = srapping_game_data(leb)
				for i in range(len(rows)):
					if (rows[i][1] != "G"):
						all_game_info.append(get_game_info(rows[i],team))
		game_table(all_game_info,cur) 
	cur.close()
	conn.close()
	

main()
