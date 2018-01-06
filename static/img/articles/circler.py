#!/usr/env/bin Python3

import os
from PIL import Image, ImageOps, ImageDraw
from fuzzywuzzy import process

with open('./articles.txt') as f:
	articles = f.readlines()
	articles = [article.strip() for article in articles]

for article in articles:
	try: 
		files = os.listdir('./' + article)
		if len(files) > 0:
			image_name, _ = process.extractOne(article,files)
			im = Image.open('./' + article + '/' + image_name)
			minsize = min(im.size[0],im.size[1])
			im = im.crop((0,0,minsize,minsize))
			im = im.resize((128,128), Image.ANTIALIAS)
			bigsize = (im.size[0] * 3, im.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(im.size, Image.ANTIALIAS)
			im.putalpha(mask)
			im.save('./'+article+'/profile.png')
		else:
			im = Image.open('./logo.png')
			im = im.resize((128,128), Image.ANTIALIAS)
			bigsize = (im.size[0] * 3, im.size[1] * 3)
			mask = Image.new('L', bigsize, 0)
			draw = ImageDraw.Draw(mask) 
			draw.ellipse((0, 0) + bigsize, fill=255)
			mask = mask.resize(im.size, Image.ANTIALIAS)
			im.putalpha(mask)
			im.save('./'+article+'/profile.png')

	except:
		print("I died while looking for " + article + " " + image_name)
		pass
