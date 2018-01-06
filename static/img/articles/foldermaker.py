#!/usr/env/bin Python3
import os

with open('./articles.txt') as f:
	articles = f.readlines()
	articles = [article.strip() for article in articles]

for article in articles:
	if not os.path.exists('./' + article):
		os.makedirs('./' + article)