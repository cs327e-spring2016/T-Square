import pymysql
def main():
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
	num = int(input('Please enter the responsed number for your topic: '))
	NBA_star = input('Please enter the name of your favorite NBA star: ')
	if num == 5:
		conn = pymysql.connect(host='localhost', user='root', password='Tiffany@160.com',db='NBA', charset='utf8')
		cur=conn.cursor()
		cur.execute("SELECT player, pts, ast FROM player_stats WhERE pts> 10 AND ast< 3 AND player= 'NBA_star'")
		print(cur.fetchall())
		cur.close()
		conn.close()
			
main()


