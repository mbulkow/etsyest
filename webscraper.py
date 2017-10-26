from bs4 import BeautifulSoup
import csv
import math
import re
import requests
import random
import time

def generate_valid_etsy_item():
	""" finds a valid url to an etsy item """
	url = 'https://www.etsy.com/listing/'
	maxlistingnum = 999999999
	tries = 0
	found = False
	nextpause = random.randint(0,30)
	while found == False:
		tries += 1
		if tries == nextpause:
			nextpause += random.randint(0,30)
			time.sleep(10)
		itemnum = random.randint(0,maxlistingnum)
		itemnumstring = '0'*(9-len(str(itemnum)))+str(itemnum)
		currenturl = url + itemnumstring + '/?show_sold_out_detail=1'
		response = requests.get(currenturl)
		html = response.content
		soup = BeautifulSoup(html, "html.parser")
		robotmeta = soup.head.find_all("meta",{"content":"noindex,nofollow"}, limit=1)
		unavailablelist = soup.find_all('span', {'class':'inline-svg unavailable-listing-alert vertical-align-middle pr-xs-1'},limit=1)
		if len(robotmeta)+len(unavailablelist) == 0:
			found = True
	return url+itemnumstring, soup
	
def findtags(soup):
	""" returns a list of strings, the tags for the item """
	tagsection = soup.find("div",{"id":"tags"})
	taglist = []
	if tagsection != None:
		for a in tagsection.find_all('a'):
			taglist.append(str(a.string))
	return taglist
	
def wassuccess(soup, cutoff):
	"""returns the number of people who favorited the item """
	overview = soup.find("div", {"id":"item-overview"})
	if overview == None:
		soldout = soup.find("span",{"class":"text-body-sm text-danger"})
		if soldout == None:
			return 0
		elif str(soldout.string) == "Sold out":
			return 1
		else:
			return 0
	favtext = overview.find_all(href = re.compile("listings"))
	if len(favtext) == 0:
		return 0
	else:
		n = str(favtext[0].string)
		n = n[:-7]
		if int(n) > cutoff:
			return 1
		else:
			return 0
	
	
def issold(soup):
	""" returns a boolean value whether or not the item is sold out """
	buybutton = soup.find("div", {"class":"buy-button clear"})
	button = str(buybutton.find(button).string)
	if button == "Sold":
		return True
	else:
		return False

def getetsydata(n, successcutoff):
	""" look at n items and get their tags """
	tags = {}
	itemtags = {}
	urllist = []
	successes = {}
	for i in range(n):
		if i%5 ==0:
			print(i)
		currenturl, currentsoup = generate_valid_etsy_item()
		urllist.append(currenturl)
		taglist = findtags(currentsoup)
		success = wassuccess(currentsoup, successcutoff)
		itemtags[currenturl] = taglist
		successes[currenturl] = success
		for tag in taglist:
			if tag in tags:
				tags[tag] = tags[tag]+1
			else:
				tags[tag] = 1
	return tags, urllist, itemtags, successes

def gettopetsytags(tags, numtags):
	""" look at numitems items and reurn the numtags most common tags """
	values = tags.values()
	values = sorted(values)
	cutoff = values[-numtags]
	toptags = []
	for key in tags:
		if tags[key]>cutoff:
			toptags.append(key)
	return toptags

def findandrecordetsydata(numitems,numtags,filetoptags,fileurls,filetags,filesuccess,successcutoff):
	""" get a sample of numtiems items and record them, find most popular tags """
	tags, urllist, itemtags, successes = getetsydata(numitems, successcutoff)
	toptags = gettopetsytags(tags, numtags)
	filett = open(filetoptags, 'w')
	for tag in toptags:
		filett.write(tag + '\n')
	filett.close()
	file1 = open(fileurls, 'w')
	file2 = open(filetags, 'w')
	file3 = open(filesuccess, 'w')
	for url in urllist:
		file1.write(url + '\n')
		currentrow = ''
		for tag in toptags:
			if tag in itemtags[url]:
				currentrow += '1'
			else:
				currentrow += '0'
		file2.write(currentrow+'\n')
		file3.write(str(successes[url])+'\n')
	file1.close()
	file2.close()
	file3.close()

def findandrecordtestset(numitems, filetoptags, fileurls, filetags, filefavs, cutoff):
	filett = open(filetoptags, 'r')
	toptags = filett.readlines()
	filett.close()
	fileu = open(fileurls, 'w')
	filet = open(filetags, 'w')
	filef = open(filefavs, 'w')
	for i in range(numitems):
		url, soup = generate_valid_etsy_item()
		fileu.write(url + '\n')
		itemtags = findtags(soup)
		currentrow = ''
		for tag in toptags:
			if tag[:-1] in itemtags:
				currentrow += '1'
			else:
				currentrow += '0'
		filet.write(currentrow+'\n')
		filef.write(str(wassuccess(soup, cutoff))+'\n')
	fileu.close()
	filet.close()
	filef.close()
	
def findandrecordsuccess(fileurls, filefavs, cutoff):
	filein = open(fileurls, 'r')
	fileout = open(filefavs, 'w')
	lines = filein.readlines()
	for line in lines:
		response = requests.get(line)
		html = response.content
		soup = BeautifulSoup(html, "html.parser")
		n = wassuccess(soup, cutoff)
		print(n)
		fileout.write(str(n)+'\n')
	filein.close()
	fileout.close()

#findandrecordetsydata(1000,200,'Desktop\\etsyestdata\\toptags.txt','Desktop\\etsyestdata\\urls.txt','Desktop\\etsyestdata\\tags.txt','Desktop\\etsyestdata\\successes.txt',20)
#findandrecordtestset(200, 'Desktop\\etsyestdata\\toptags.txt', 'Desktop\\etsyestdata\\urlstest.txt', 'Desktop\\etsyestdata\\tagstest.txt','Desktop\\etsyestdata\\favsstest.txt',20)
findandrecordsuccess('Desktop\\etsyestdata\\urlstest.txt','Desktop\\etsyestdata\\favsstest.txt',20)