from bs4 import BeautifulSoup
import requests
import time
from stack import Stack


def get_first_link(url):
    
    """ function that gives you the first link given a wikipedia url """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div",attrs = {"class":"mw-parser-output"}) # get the first div
    html_tags = ["i", "span", "b", "sup"]
    
    try : 
        try: 
            for tag in div.find_all("table"):
                    tag.decompose()
        except:
            pass
        
        ps = div.find_all("p", attrs = {"style":None })

        paren = False #checks if we are in a middle of a parenthesis
    

        for p in ps:
            for html_tag in html_tags:
                for tag in p.find_all(html_tag):
                    tag.decompose()
            for node  in p.descendants :
                if str(node).startswith("<") == False: #makes sure that the parenthesis are not inside a link tag
                    for char in  str(node):
                        if char == "(":
                            paren = True
                        elif char == ")":
                            paren = False
                if  node.name == 'a' :
                    if  paren ==False : 
                        return "https://en.wikipedia.org"+node["href"]
    except Exception as E: 
        print(E)
        return "broken link"

def keep_looking(url,stack):
    
    "function that keeps looking for first links"
    
    if url  == "broken link":
        return "broken link"
    
    elif url == "https://en.wikipedia.org/wiki/Philosophy":
        return "Found"
    
    else: 
        url = get_first_link(url)
        if url is None:
            return "No links found"
        print(url)
        stack.push(url)
        time.sleep(0.5)   
        return keep_looking(url,stack)
    
    
#Let's try it out: 

st = Stack()
keep_looking("https://en.wikipedia.org/wiki/Special:Random",st)
   