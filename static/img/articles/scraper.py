#!/usr/env/bin Python3

import wikipedia, urllib.request

with open('./articles.txt','r') as f:
	articles = f.readlines()
	articles = [article.strip() for article in articles]

for article in articles:
	try:
		num = 0
		wikipage = wikipedia.page(article)
		print(article)
		for image in wikipage.images:
			if image.endswith('.jpg') or image.endswith('.jpeg') or image.endswith('.png') or image.endswith('.gif') or image.endswith('.tiff') or image.endswith('bmp'):
				print('\t'+str(num)+" "+image)
				urllib.request.urlretrieve(image,'./' + article + '/' + image.split('/')[-1])
				num = num+1
				if (num > 10):
					break
	except:
		pass
