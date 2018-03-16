with open("./articles.txt") as f:
	articles = f.read().splitlines()

with open("./ak.txt",'w') as f:
	for i in range(len(articles)):
		f.write(articles[i] + ":::" + str(i+10000) + "\n")
