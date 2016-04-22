import pymysql

# print out the introduction in the function
def intro():
	print('T-Square')
	print(" ")
	print("Plese select a topic that you are interested: ")
	print(" ")
	print("     " + "Press 1 for influence of player size")
	print("     " + 'Press 2 for How successful a school')
	print("     " + 'Press 3 for variation of 3-point influence in-game')
	print("     " +  'Press 4 for different game affects a player to get rebound')
	print("     " + 'Press 5 for Draw out the selfish NBA star' )
	print("     " + 'Press 6 for Potential shooting guard star style')
	print(" ")

def query1:
def query2:
	query2=conn.query2("SELECT 'ps.player', 'ps.pts', 'ps.drb', 'ps.ast', 'p.College' AVG('ps.pts') avg.pts, AVG('ps.drb') avg.drb, AVG('ps.ast') avg.ast FROM 'player_stats ps' INNER JOIN 'player p' WHERE 'ps.pts'> 'avg.pts' AND 'ps.drb'>'avg.drb' AND 'ps.ast'>'avg.ast'")
def query3:

def query4(player_name):
	query4=conn.query("SELECT 'P.trb', 'p.player', 'p.game', 'g.host','g,guest' FROM 'player_stats p' INNER JOIN 'Game g' WHERE 'p.game'='g.id' AND 'player'= player_name")
	print (query4)

def query5(NBA_star):
	query5=conn.query("SELECT 'p.pts', 'p.ast', 'p.player' FROM 'player_stats p' WhERE 'p.pts'> '10' AND 'p.ast'< '3' AND 'player'= NBA_star")
	print (query5)


def query6(star_stl):
	query6=conn.query("SELECT 'p.pts', 'p.ast','p.player' FROM 'player_stats p' WHERE 'p.pst'> '25' AND 'p.ast' > '8' AND 'player'= star_stl" )
	print(query6)


def get_result(num):
	# operating 1st query
	if num == 1:
		print(query1)
	# operating 2nd query
	elif num == 2:
		print(query2)
	# operating 3rd query
	elif num == 3:
		print(query3)
	# operating 4th query
	elif num == 4:
		player_name = input('Please enter your favorite player: ')
		# check user input whether in the database player list 
		if player_name in Player:
			print(query4(player_name))
		else:
			print('We do not have his data here, check other players -_- !!!')
			player_name = input('Please enter your favorite player: ')
	# operating 5th query
	elif num == 5:
		NBA_star = input('Please enter the name of your favorite NBA star: ')
		if NBA_star in Player:
			print(query5(NBA_star))
		else:
			print('He is not on the list, Sorry!')
			NBA_star = input('Please enter the name of your favorite NBA star: ')
	# operating 6th query
	else:
		star_stl = input('put the name for who do you think may has the potential shooting guard style: ')
		if star_stl in Player:
			print('WOw! He may be the raise star!!!')
			print(query6(star_stl))
		

def main():
	
	conn = pymysql.connect(host='localhost', user='root', password='Tiffany@160.com',db='NBA', charset='utf8')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM NBA")
	connection.commit()
	# an introduction to the user 
	intro()
	# ask the user to input a number to the related topic
	num = int(input('Please enter the responsed number for your topic: '))
	# check the valid number
	if num<1 or num>6:
		print('please make your choice again')
		num = int(input('Please enter the responsed number for your topic: '))
	else:
		if (get_result(num)):
			print()

main()