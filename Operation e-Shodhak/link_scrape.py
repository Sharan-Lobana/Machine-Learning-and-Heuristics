from bs4 import BeautifulSoup
import re, socket, urllib.request, urllib.parse, urllib.error, urllib.error, urllib.parse
from urllib.parse import urlparse
from urllib.parse import urljoin
from collections import defaultdict
from time import time
import pickle, os
mine = "mine"
if not os.path.exists(mine):
	os.makedirs(mine)

mine = os.path.join(mine, "pdf.txt")
miner = open(mine, "w+")
f=open('out.txt','w+')
unvisited = []
unvisited_map = {}
visited = defaultdict(lambda: 0)
pdfs = []
local_ip = ""
numPDF = 0
numUnvisited = 0

# def get_ip(url):
# 	#print(url)
# 	try:
# 		url = (socket.gethostbyname(urlparse(url).netloc)).split('.')
# 	except:
# 		pass
# 	return url[0] + "." + url[1] + "." + url[2]

def crawl():
	global local_ip, unvisited, visited, pdfs, unvisited_map, f, numPDF, numUnvisited
	website = unvisited.pop()
	numUnvisited -= 1
	print((website,"\n"))
	f.write(website+"\n")
	visited[website] = 1
	try:
		req = urllib.request.Request(website)
	except:
		return
	page = "xyz"
	if website[-4:] == ".pdf":
		pdfs.append(website)
		numPDF += 1
		return
	try:
		reponse = urllib.request.urlopen(req,timeout=5)
	except:
		print('Error 404 :Not Found')
		f.write('Error 404 :Not Found\n')
		return
	print('The Content-Type of processing url is: '+str(reponse.getheader('Content-Type')))
	try:
		if 'text/pdf' in reponse.getheader('Content-Type') or 'application/pdf' in reponse.getheader('Content-Type') or 'application/x-pdf' in reponse.getheader('Content-Type'):
			pdfs.append(abs_link)
			numPDF += 1
			return
		if 'text/html' in reponse.getheader('Content-Type'):
			page = reponse.read()
		else:
			return
	except:
		print("Invalid Response")
		return
	soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('a'):
		path = link.get('href')
		classlink = link.get('class')
		idlink = link.get('id')
		if path == None or path=='' or path[0] == '#':
			return
		if '\n' in path or '\r' in path:
			path=path.replace('\n','')
			path=path.replace('\r','')
			print('New line or carriage return character found in path')
		if "http" == path[:4]:
			abs_link = path
		else:
			abs_link = urljoin(website, path)
		if ( visited[abs_link] == 0 ):
			if abs_link[-4:] == ".pdf":
				visited[abs_link] = 1
				pdfs.append(abs_link)
				numPDF += 1
			else:
				try:
					ip = (urlparse(abs_link).netloc)
					if (ip == local_ip) and (abs_link not in unvisited_map):
						unvisited.append(abs_link)
						unvisited_map[abs_link] = 1
						numUnvisited += 1
				except:
					pass

def get_links(start_url):
	global unvisited, pdfs, unvisited_map, local_ip, numPDF, numUnvisited, miner
	numUnvisited = 0
	local_ip = (urlparse(start_url).netloc)
	unvisited = []
	unvisited.append(start_url)
	numUnvisited += 1
	unvisited_map[start_url] = 1
	scanned = 0
	while ( numUnvisited > 0 ):
		crawl()
		if ( (numPDF != 0)  and numPDF % 100 == 0 ):
			for var in range(numPDF-100, numPDF):
				miner.write(pdfs[var]+"\n")
		scanned += 1
		stri=("%d PDFs found, %d links scanned, %d links still left" % (numPDF, scanned, numUnvisited))
		print(stri)
		stri=stri+"\n"
		f.write(stri)

	return pdfs

# def get_pdf_links():
# 	global f
# 	grand_list = []
# 	filename = "FinalDomains.txt"
# 	data = open(filename, "r")
# 	directory = "pickled_links"
# 	for line in data.readlines():
# 		line = line[:-1]
# 		pdf_list = get_links(line)
# 		grand_list.extend(pdf_list)
# 		line = urlparse(line).netloc.split(".")[1]+".p"
# 		if not os.path.exists(directory):
# 			os.makedirs(directory)
# 		dir_path = os.path.join(directory,line)
# 		print(("The pickle is saved in ",dir_path))
# 		pick_file = open(dir_path, "wb")
# 		pickle.dump(pdf_list, pick_file)
# 		pick_file.close()
# 	f.close()
# 	data.close()
# 	dir_path = os.path.join(directory,"grand_list.p")
# 	pickle_file = open(dir_path, "wb")
# 	pickle.dump(grand_list, pickle_file)
# 	pickle_file.close()
# miner.close()
