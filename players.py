def main():
	#open the file word.txt
	in_file = open('./Players.txt','r')

	#open file for writing
	out_file = open("./NewPlayer.txt","w")

	Players = []
	#populate the dictionary
	for line in in_file:
		line = line.strip()
		line = line.split("	")
		Playersname = line[0]
		Playersname = Playersname.split()
		#print(Playersname)
		Lastname = Playersname[2]
		Lastname = Lastname[:-1]
		firstname = Playersname[1]
		ideaname = Lastname[:5] + firstname[:2] + "01"
		out_file.write(ideaname)
		out_file.write('\n')

	#print(Players)
	in_file.close()
	out_file.close()
main()
