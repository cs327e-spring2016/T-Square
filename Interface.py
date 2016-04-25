from bs4 import BeautifulSoup
import requests
import prettytable

import pandas as pd
import numpy as np

import re
import pymysql
#needed to convert unicode to numeric
import unicodedata

# print out the introduction in the function
def intro():
	print('T-Square')
	print(" ")
	print("Plese select a topic that you are interested: ")
	print(" ")
	print("     " + "Press 1 for Outstanding On-Court Performance of Centers")
	#print("     " + 'Press 2 for How successful a school')
	#print("     " + 'Press 3 for variation of 3-point influence in-game')
	#print("     " + 'Press 4 for different game affects a player to get rebound')
	print("     " + 'Press 2 for Draw out the selfish NBA star' )
	print("     " + 'Press 3 for Excellent 3-point shooting team and their team performance' )
	#print("     " + 'Press 4 for Potential shooting guard star style')
	print(" ")

def get_result(cur,num):
	# operating 1st query
	if num == 1:
		display_query = "select t1.player_id as Player_id, t1.name as Name, t3.points as Point, t3.total_reb as Rebound, t2.position as Position, t3.game_date as Date from player as t1 left join player_position as t2 on t1.player_id = t2.player_id left join player_stats as t3 on t1.player_id = t3.player_id where t2.position = 'CENTER' and t3.points >= 30 and t3.total_reb >= 15;"
		cur.execute(display_query)
		result_set = cur.fetchall()
		
		center = []
		center_check = []
		total_num = 0
		for row in result_set:
			if (not(row[1] in center_check)):
				center.append(row[1])
				center_check.append(row[1])
				total_num += 1
		for item in result_set:
			print(item[1:])

		print("Based on their on-court performance, there is a number of "+ str(total_num) + " distinct centers getting more than 30 points and 15 rebounds within 1 game in NBA ")


	# operating 2nd query
	

	# operating 4th query
	#elif num == 4:


	# operating 2nd query
	elif num == 2:
		display_query = "select distinct t1.name as Name, t2.points as Point, t2.assistant as Assistant from player as t1 inner join player_stats as t2 on t1.player_id = t2.player_id where t2.points > 30 and t2.assistant <3;"
		cur.execute(display_query)
		result_set = cur.fetchall()
		
		selfish_player = []
		selfish_player_check = []
		total_num = 0
		for row in result_set:
			if (not(row[0] in selfish_player_check)):
				selfish_player.append(row[0])
				selfish_player_check.append(row[0])
				total_num += 1
		
		for item in selfish_player:
			print(item)
		
		print()
		print("Based on their on-court performance, there is a number of "+ str(total_num) + " comparatively selfish players in NBA currently")

	# operating 3rd query
	elif num == 3:
		Three_made = input("Please enter a number to evaluate team's 3-point shooting capbility: ")
		Three_percentage = input("Please enter a deciaml to evaluate team's 3-point shooting effciency: ")
		display_query = 'select t1.game as DATE, t1.team as TEAM, t1.tassistant as ASSISTANT, t1.tblock as BLOCK, t1.tfieldg3_pct as Three_Point_Percentage, t1.tfieldg3 as Three_Point_Made from team_stats as t1 where t1.tfieldg3_pct > '+ Three_percentage +'and t1.tfieldg3 >'+ Three_made +' group by t1.team, t1.game, t1.tassistant, t1.tblock, t1.tfieldg3, t1.tfieldg3_pct;'
		cur.execute(display_query)
		result_set = cur.fetchall()

		for row in result_set:
			print(row)
		
		#print("DATE    TEAM   ASSISTANT    BLOCK    Three_Point_Percentage    Three_Point_Made")
		# Good_Three_shooting_team = []
		# Good_Three_shooting_team_check = []
		# for row in result_set:
		# 	if (not(row[1] in Good_Three_shooting_team_check)):
		# 		Good_Three_shooting_team.append(row[1])
		# 		Good_Three_shooting_team_check.append(row[1])

	# operating 3rd query
	#elif num == 4:


	# operating 6th query
	# else:
	# 	star_stl = input('put the name for who do you think may has the potential shooting guard style: ')
	# 		print('WOw! He may be the raise star!!!')
	# 		# print(cursor.6_query)
		

def main():
	
	conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
	                       user='root', passwd='15174903378', db='NBA')
	cur = conn.cursor() 
	intro()

	# ask the user to input a number to the related topic
	num = int(input('Please enter the responsed number for your topic: '))
	# check the valid number
	while num<1 or num>6:
		print('please make your choice again')
		num = int(input('Please enter the responsed number for your topic: '))
	else:
		get_result(cur,num)
	cur.close()
	conn.close()
main()