from bs4 import BeautifulSoup
import requests
import time
from stack import Stack


def get_first_link(url):
    
    """ function that gives you the first link given a wikipedia url """
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", attrs = {"class":"mw-parser-output"}) # get the first div present in every eligible wikipedia page
    html_tags = ["i", "span", "b", "sup"]   # the following html tags are children of the div 
                                     #and our first link exists as a  direct child, hence will not exist 
                                     #under any of these tags.
                                      #Hence we will remove them
    
    try :  # some wikipedia links are broken, hence the need for a try catch. 
        try:  # most wikipedia pages contain tables on the side, although not all. Hence we will get rid of them. 
            for t in div.find_all("table"):
                    t.decompose()
        except:
            pass
        
        p_tags = div.find_all("p", attrs ={"style":None }) #get all p tags because our first url is a direct child of a p tag

        paren = False #checks if we are in a middle of a parenthesis
    

        for p in p_tags:
            for html_tag in html_tags:    #get rid of all the unnecessary tags. 
                for tag in p.find_all(html_tag):
                    tag.decompose()
            for node  in p.descendants:
                '''this conditionmakes sure that we are 
                not inside a link tag because we don't want to remove parenthesis in side a link'''
                if str(node).startswith("<") == False: 
                    for char in  str(node):
                        if char == "(": 
                            paren = True # We are inside a parenthesis 
                        elif char == ")":
                            paren = False # We are outsid a parenthesis
                if  node.name == 'a' and paren ==False:
                    return "https://en.wikipedia.org"+node["href"]
    except Exception as E: 
        print(E)
        return "broken link"

def keep_looking(url,stack):
    
    "function that keeps looking for first links"
    
    if url  == "broken link":  #ends if broken link
        return "broken link"
    
    elif url == "https://en.wikipedia.org/wiki/Philosophy":  #ends the recursive function if philosophy found
        return "Found"
    
    else: 
        url = get_first_link(url)
        if url is None:
            return "No links found"   #ends if  wikipedia page has no outgoing links
        print(url)
        stack.push(url) # when pushing a url into a stack, the push function inside the stack class raises an error when a url                            #already exists
        time.sleep(0.5)   
        return keep_looking(url,stack) # make the recursive call
    
    
#Let's try it out: 

st = Stack()
keep_looking("https://en.wikipedia.org/wiki/Special:Random",st)
   