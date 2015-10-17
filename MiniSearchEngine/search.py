# Mini Search Engine

# Vincent Pham

import urllib2
import urlparse
import os
import re
from bs4 import *

TIMEOUT = 10

def request_response(url): 
    '''Open connection to url'''
    try:
        response = urllib2.urlopen(url)
        return response
    except urllib2.URLError:
        return None
    except Exception:
        return None

def read_from_response(request):
    ''' 
    Read the whole document from request as a string.
    '''
    try:
        return request.read()
    except Exception:
        print "read failed"
        return ""


def is_url_in_domain(domain, url):
    '''
    Returns true if the domain of the url 
    matches the specified domain.  False, otherwise.
    '''
    loc = urlparse.urlparse(url).netloc
    if loc == "":
        return False
    return domain == loc[-len(domain):]


def is_url_ok_to_follow(url):
    '''
    Returns true if the protocol for the url is http and the path is
    either a directory (starts with /) or a file that ends in .html
    '''

    if url == "":
        return False

    parsed_url = urlparse.urlparse(url)
    if parsed_url.scheme == "http" or url[0] == "/":
        (filename, ext) = os.path.splitext(parsed_url.path)
        return (ext == "" or ext == ".html")
    else:
        return False


######### PROVIDED UTILITIES END #########

### YOUR CODE GOES HERE ###

def getLinks(URL, domain):
	f = urllib2.urlopen(URL)
	soup = BeautifulSoup(f)
	L = [link.get('href') for link in soup.find_all('a')]
	rv = []
	for link in L:
		if (is_url_ok_to_follow(link) and is_url_in_domain(domain, URL)):
			rv.append(link)
	return rv
		

def webCrawler(startURL, domain, maxPgs):	
	f = urllib2.urlopen(startURL)
	sp = BeautifulSoup(f)
	text = sp.get_text()
	wordList = re.findall('[A-Za-z0-9]+',text)[1:16]
	word_map = {}
	
	lowercase_wordList = text.lower()
        words =re.findall('(?<![0-9])[A-Za-z][A-Za-z0-9]*',lowercase_wordList)
        str_words = []
        for word in words:
            word_map[str(word)] = set([0])
	
	printWords = ''
	for w in wordList:
		printWords += w+' '
	
	index = {}
	id_map = {}

	id_map[0] = (startURL, sp.title.string, printWords)

	
	unique_ID = 1
	
	pending = getLinks(startURL, domain)
	visited = [startURL]
	N = maxPgs - 1
	
	while (len(pending) > 0 and N>0):
		currentURL = pending.pop()
		N-=1
		
		if not currentURL in visited:
			visited.append(currentURL)
			#DL website
			f = urllib2.urlopen(currentURL)
			soup = BeautifulSoup(f)
			text = soup.get_text()
			wordList = re.findall('\w+',text)[1:16]

			lowercase_wordList = text.lower()
                        words =re.findall('(?<![0-9])[A-Za-z][A-Za-z0-9]*',lowercase_wordList)
                        str_words = []
                        for word in words:
                            if word in word_map:
                                word_map[word].add(unique_ID)
                            else:
                                word_map[word] = set([unique_ID])
                        
			printWords = ''
			for w in wordList:
				printWords += w+' '
					
			id_map[unique_ID] = (currentURL, soup.title.string, printWords)
			
			unique_ID+=1
			
			links = [link.get('href') for link in soup.find_all('a')]
			for link in links:
				link = str(link)
				if link not in visited:
					if link[0] == '/':
						link = 'http://' + domain + link
					if is_url_in_domain(domain, link) and is_url_ok_to_follow(link) and link not in pending:
						pending.append(link)
					
	return (word_map, id_map)

		
def miniIndexer(word, wordMap):
	if word in wordMap:
            return wordMap[word]
        else:
            return None
				

	
def setIntersection(L): #input is a LIST of sets
	if len(L) == 1:
		return L[0]
	else:
		rv = set.intersection(L[0],L[1])
		for s in L[2:]:
			rv = set.intersection(rv, s)
	return  rv

def build_search_engine(start_URL, domain, maxPgs):
        wordMap, idMap = webCrawler(start_URL, domain, maxPgs)
        word_map = []
	def search(query):
		terms = re.split(' ', query)
		pageList = []
		
		
		
		for term in terms:
                    failed_num = "word cannot start with a number"
                    
                    term_set = miniIndexer(term,wordMap)
                    if term_set == None:
                        print "can not find at least one of the words"
                        print "or word starts with number(which is not allowed)"
                        print "or please use only lowercase: "
                        print "First word error: " + term
                        return None
                    else:
                        pageList.append(term_set)
		
		hits = setIntersection(pageList)
		index = range(1, len(hits)+1)
		
		n=0 #we want less than 10 pages printed#
		
                for (i,j) in zip(hits, index):
                    if n < 10:
                        print ('Hit ' + str(j))
                        print idMap[i][1]
                        print idMap[i][0]
                        print idMap[i][2]
                        print
                        n+=1
	return search



		
		
		
		
		
		
		
		
		
