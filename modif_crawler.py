import requests
import re
from bs4 import BeautifulSoup
import urllib.robotparser

#This regular expression makes sure that the crawler sticks to udacity webpages only,
#instead of crawling the whole web
udacity_url=re.compile(r'https?://([a-z])*.udacity.com')

crawled=[]

visible_text=""
keyword_index=dict()
graph=dict()
def strip_punctuation(str):
    out = "".join(c for c in str if c not in ('!','.',':','"','(',')','&','/',',',';','$'))    
    return out 

def lookup(keyword):
    keyword=keyword.lower()
    if keyword in keyword_index:
        return keyword_index[keyword]

def union(a,b):#The union function merges the second list into first, with out duplicating an element of a, if it's already in a. Similar to set union operator. This function does not change b. If a=[1,2,3] b=[2,3,4]. After union(a,b) makes a=[1,2,3,4] and b=[2,3,4]
    for e in b:
        if e not in a:
            a.append(e)

#Adds all the words from a page, strips the unnecessary punctuation, and builds a word Index.
def add_words_fromPage(url,word):
    word=strip_punctuation(word)
    word=word.lower()
    if word in keyword_index:
        if url not in keyword_index[word]:
            keyword_index[word].append(url)
            return
    else:
        
        keyword_index[word]=[url]
        

def add_eachPage(url,split_content):
    #print (split_content)
    for k in split_content:
        add_words_fromPage(url,k)

#Crawls the page given to it, gathers all the links in that page and
#returns it in an index
def crawl(page):
    index=[]
    r=requests.get(page)
    htmltext=r.text
    soup=BeautifulSoup(htmltext)
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    global visible_text
    visible_text = soup.getText()
    for link in soup.find_all('a',href= True):
            value_of_link=link['href']
            if value_of_link=='':
                 continue
            if value_of_link[0]=='/':
                 value_of_link='http://www.udacity.com'+value_of_link
            #print value_of_link
            if udacity_url.match(value_of_link):
                if value_of_link not in crawled: 
                    index.append(value_of_link)
                    #print (value_of_link)           
    return index
    

def crawl_the_website(page):
    tocrawl=[page] 
    rp=urllib.robotparser.RobotFileParser() # To obey robots.txt protocols
    rp.set_url("https://www.udacity.com/robots.txt")
    rp.read()
    
    count=0 #This is to keep the number of indexed websites below 1500 due to limited computing power
    while tocrawl:
        page=tocrawl.pop()
        count=count+1
        
        if page not in crawled and rp.can_fetch("*",page)  :
            try:
                c=crawl(page)
                graph[page]=c
                split_content=visible_text.split()
                add_eachPage(page,split_content)
                union(tocrawl,c)
                crawled.append(page)
            except:
                print ("Unable to index "+page )
        if count>1500 :        
            break
    
#Ranking algorithm for webpages         
def compute_ranks():
    d = 0.8 # damping factor
    numloops = 10

    ranks={}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))

            newranks[page] = newrank
        ranks = newranks
    return ranks

#Function to return the best page for a query    
def lucky_search(ranks, keyword):
    pages = lookup( keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page  
    
  
crawl_the_website("https://www.udacity.com/")
ranks=compute_ranks() 
print (keyword_index)


