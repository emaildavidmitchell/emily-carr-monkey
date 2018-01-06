#!/usr/env/bin Python3

import os

with open('./articles.txt') as f:
	articles = f.readlines()
	articles = [article.strip() for article in articles]

for article in articles:
	files = os.listdir('./' + article)
	numb = 0
	for num in range(len(files)):
		if (files[num] != "profile.png"):
			ext = files[num].split('.')[-1]
			os.rename('./' + article + '/' + files[num],'./' + article + '/' + str(numb) + '.' + ext)
			numb = numb+1