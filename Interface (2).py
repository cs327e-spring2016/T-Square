import mysql.connector

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

def get_result(num):
	# operating 1st query
	if num == 1:
		print(cursor.1_NAME)
	# operating 2nd query
	elif num == 2:
		print(cursor.2_NAME)
	# operating 3rd query
	elif num == 3:
		print(cursor.3_NAME)
	# operating 4th query
	elif num == 4:
		player_name = input('Please enter your favorite player: ')
		# check user input whether in the database player list 
		if player_name in Player:
			print(cursor.4_NAME)
		else:
			print('We do not have his data here, check other players -_- !!!')
			player_name = input('Please enter your favorite player: ')
	# operating 5th query
	elif num == 5:
		NBA_star = input('Please enter the name of your favorite NBA star: ')
		if NBA_star in Player:
			print(cursor.5_query)
		else:
			print('He is not on the list, Sorry!')
			NBA_star = input('Please enter the name of your favorite NBA star: ')
	# operating 6th query
	else:
		star_stl = input('put the name for who do you think may has the potential shooting guard style: ')
		if star_stl in Player:
			print('WOw! He may be the raise star!!!')
			print(cursor.6_query)
		

def main():
	
	cnx = mysql.connector.connect(user='root', password='password',host='127.0.0.1',database='utf8')
	cursor = cnx.cursor()
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
		get_result(num)
main()