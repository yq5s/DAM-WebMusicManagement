import scan
def quote(s):
	return "'"+s+"'"
folder = raw_input("Where to put your search results? ")
while True:
	keyword= raw_input("What to search? ")
	total = input("How many of related songs you want? ")
	s=scan.Song_search_by_lyric(folder, search = keyword, total=total)
	s.run()
	print("Finished")
	print("type ctrl+c to quit")
