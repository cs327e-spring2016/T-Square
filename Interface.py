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
	if num == 1:
		print("result for #1")
	elif num == 2:
		print("result for #2")
	elif num == 3:
		print("result for #3")
	elif num == 4:
		player_name = input('Please enter your favorite player: ')
		# how to show the player query here?????
	elif num == 5:
		NBA_star = input('Please enter the name of your favorite NBA star: ')
	else:
		# for query 6...........

def main():
	#an introduction to the user 
	intro()
	#ask the user to input a number to the related topic
	num = int(input('Please enter the responsed number for your topic: '))
	#check the valid number
	if num<1 or num>6:
		print('please make your choice again')
		num = int(input('Please enter the responsed number for your topic: '))
	else:
		get_result(num)
main()