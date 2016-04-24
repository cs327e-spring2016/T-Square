import pymysql
conn = pymysql.connect(host='localhost', user='root', password='Tiffany@160.com',db='NBA', charset='utf8')
cur=conn.cursor()
cur.execute("USE NBA")
cur.execute("SELECT player, pts, ast FROM player_stats WhERE pts> 10 AND ast< 3 AND player='a'")
print(cur.fetchall())
cur.close()
conn.close()
