#!/usr/env/bin Python3

import os
from PIL import Image, ImageOps, ImageDraw
from fuzzywuzzy import process

with open('./articles.txt') as f:
	articles = f.readlines()
	articles = [article.strip() for article in articles]

for article in articles:
		size = 128, 128
		print(article)
		files = os.listdir('./' + article)
		for image_name in files:	
			if image_name != "profile.png":
				im = Image.open('./' + article + '/' + image_name)
				im.thumbnail(size, Image.ANTIALIAS)
				im.save('./'+article+'/'+image_name,optimize=True,quality=90)
