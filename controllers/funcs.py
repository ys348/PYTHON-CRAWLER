import re
import urllib2
import os
from cgitb import html
import socket
from urlparse import urlparse
import string
import server
import logging
import time
from google.appengine import runtime
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
from google.appengine.runtime import apiproxy_errors


urlfetch.set_default_fetch_deadline(60)
socket.setdefaulttimeout(12)

global url_all_str
url_all_str=''
global num_records
num_records=0
global url_records
url_records=[]
global url_sum_total
url_sum_total=0
global TLD
TLD=''
global max_records
max_records=200
global max_circles
max_circles=5


def getFllURL(url,tld):
    global TLD
#    reg=r'href="(/[a-zA-Z0-9._-]+?.*?)"'
  #  re_orig=''
    print '@@@@@@@@@@@@@@@@@@url is:'+url
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Referer':"http://"+TLD+"/"}
        req=urllib2.Request(url=url,headers=headers)
        #req.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
        #req.add_header("Connection", "keep-alive")
        #req.add_header("Accept-Encoding", "gzip, deflate")
        #req.add_header("Referer","http://"+TLD+"/")
        response=urllib2.urlopen(req,timeout=5)
        html=response.read().decode('UTF-8','ignore')

    except (socket.error,apiproxy_errors.DeadlineExceededError,urllib2.URLError,IOError,runtime.DeadlineExceededError,runtime.apiproxy_errors.DeadlineExceededError,urlfetch_errors.DeadlineExceededError) as e:
        URLlist_F=[]
        return URLlist_F
    reg1=r'href="(https?://[a-z.]*?'+tld+'/[a-zA-Z0-9-._]+?/.*?)"'
    urlre1=re.compile(reg1)
    reg2=r"href='(https?://[a-z.]*?"+tld+"/[a-zA-Z0-9-._]+?/.*?)'"
    urlre2=re.compile(reg2)
    URLlist_F1=urlre1.findall(html)
    URLlist_F2=urlre2.findall(html)
    URLlist_F=URLlist_F1+URLlist_F2
#    URLlist_F=[line+'\n' for line in URLlist_F]
    return URLlist_F

#reg=r'www(.*?ez.*?.com)'
#imgre=re.compile(reg)
#imglist=re.findall(imgre, s1)

def getPartialURL(url):
    global TLD
    try:
#        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#        'Accept':'text/html;q=0.9,*/*;q=0.8',
#        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#        'Accept-Encoding':'gzip',
#        'Connection':'close',
#        'Referer':TLD
#        }
#        req_timeout = 5
#        req = urllib2.Request(url,None,req_header)
#        response = urllib2.urlopen(req,None,req_timeout)	
        
        #headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        #req = urllib2.Request(url = url,data = postdata,headers = headers)
        
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Referer':"http://"+TLD+"/"}
        req=urllib2.Request(url=url,headers=headers)
        #req.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
        #req.add_header("Connection", "keep-alive")
        #req.add_header("Accept-Encoding", "gzip, deflate")
        #req.add_header("Referer","http://"+TLD+"/")
        response=urllib2.urlopen(req,timeout=5)
        html=response.read().decode('UTF-8','ignore')
		
    except (socket.error,apiproxy_errors.DeadlineExceededError,urllib2.URLError,IOError,runtime.DeadlineExceededError,runtime.apiproxy_errors.DeadlineExceededError,urlfetch_errors.DeadlineExceededError) as e:
        URLlist_P=[]
        return URLlist_P
    r_get_domain=re.compile(r'(https?://[a-zA-Z0-9.-_]+?.)/.*?')
    top_level_domain=r_get_domain.findall(url)

    reg1=r'href="(/[a-zA-Z0-9._-]+?.*?)"'
#    reg=r'href="(https?://[a-z.]*?apple.com/[a-zA-Z0-9-._]+?/.*?)"'
    urlre1=re.compile(reg1)
    URLlist_P1=urlre1.findall(html)
    
    reg2=r'href="(/[a-zA-Z0-9._-]+?.*?)"'
#    reg=r'href="(https?://[a-z.]*?apple.com/[a-zA-Z0-9-._]+?/.*?)"'
    urlre2=re.compile(reg2)
    URLlist_P2=urlre2.findall(html)
    
    URLlist_P=URLlist_P1+URLlist_P2
    
    URLlist_P=[top_level_domain[0]+line for line in URLlist_P]

    return URLlist_P
    
    
def writeIntoFile(URL,tld):

    global url_all_str
    global url_sum_total
	
    if server.query_termination=='Y':
        server.query_termination='N'
        quit()
    URLlist_F=getFllURL(URL,tld)
    URLlist_P=getPartialURL(URL)
    URLlist_A=list(set(URLlist_F+URLlist_P))
    
    s1=url_all_str.split("\n")
    
    s_a=list(set(s1+URLlist_A))
    print '------'+str(len(s_a))+' records in the file------\n'
    url_sum_total=len(s_a)
    url_all_str='\n'.join(s_a)



def findAllUrl(URL):
    
    server.query_status = 'pre-calculating... (in average, it takes 1 minute)'
    server.query_termination
    global url_all_str
    global num_records
    global url_records
    global max_records
    global max_circles
    global url_sum_total
	
#    print 'calculating......(about 1 minute)'
    TLD=findTLD(URL)

    URL="http://"+TLD+"/"
    
    writeIntoFile(URL,TLD)

    url_records=url_all_str.split("\n")

    circle=0;

    while len(url_records)<max_records and circle<max_circles: # max_records indicates the level of accuracy of the spider
#        print "record number:"+str(len(url_records))+"we are in this while iteration!!!!!!!"
        for record in url_records:
            #try:
            if record!='':
                print 'record in url_records:'+record
                writeIntoFile(record,TLD)
                url_records=url_all_str.split("\n")
                print "circle:"+str(circle)
            circle=circle+1
            if circle>=max_circles:
                break
            #except (Exception,socket.error,apiproxy_errors.DeadlineExceededError,urllib2.URLError,IOError,runtime.DeadlineExceededError,runtime.apiproxy_errors.DeadlineExceededError,urlfetch_errors.DeadlineExceededError) as e:
                #continue

    s1_all=url_all_str.split("\n")
    num_records=len(s1_all)
    print '\n#############Number of Records in s1: '+str(num_records)+'#################'

    numbers=0

    for i in s1_all:
        if i!='':
            logging.info('**************find_all_urls:****************')	
            logging.info(i)
            numbers=numbers+1
            print str(numbers)+': '+i+'\n'
            writeIntoFile(i,TLD)
            complet_percent=(numbers*100)/num_records

            #server.query_status = server.query_termination str()
            #server.query_status = "collecting data, "+str(complet_percent)+"% complete. <"+str(url_sum_total)+' records in array>'+'  <max_circles:'+str(max_circles)+'>  <max_records:'+str(max_records)+'>  <the num for pre_loop:'+str(num_records)+'>'
            server.query_status = "Scanning "+TLD+", "+str(complet_percent)+"% complete. "+str(url_sum_total)+" URLs gained."

    logging.info("******************************end*******************************") 

def findTLD(url):
    url=url.replace(" ", "")
    if len(url)<4:
        return 'unknown'
    else:
        if url[0:4]=='http':
            pass
        elif url[0:2]=='//':
            pass
        elif url[0:3]=='://':
            pass
        else:
            url="http://"+url
    print url
    topHostPostfix=['.market', '.ke', '.kg', '.kh', '.ki', '.km', '.vote', '.kp', '.com.mx', '.kr', '.press', '.kw', '.media', '.ky', '.kz', '.pink', '.digital', '.qpon', '.hosting', '.name', '.bz', '.by', '.website', '.bs', '.br', '.bw', '.rest', '.bt', '.bj', '.bi', '.bh', '.bo', '.bn', '.bm', '.bb', '.ba', '.jobs', '.bg', '.bf', '.be', '.bd', '.toys', '.eg', '.ee', '.ec', '.et', '.eu', '.es', '.pm', '.pl', '.pn', '.ph', '.pk', '.pe', '.pg', '.pf', '.pa', '.joburg', '.py', '.attorney', '.kiwi', '.pt', '.pw', '.nom.es', '.ps', '.pr', '.lawyer', '.camera', '.cab', '.expert', '.fit', '.net.ag', '.city', '.arpa', '.ngo', '.cat', '.pro', '.rehab', '.photos', '.systems', '.host', '.university', '.axa', '.camp', '.repair', '.world', '.post', '.country', '.cymru', '.news', '.realtor', '.career', '.services', '.wiki', '.om', '.red', '.social', '.ren', '.energy', '.luxury', '.recipes', '.report', '.ads', '.dating', '.help', '.beer', '.army', '.place', '.democrat', '.fo', '.cheap', '.fm', '.fj', '.fi', '.fr', '.porn', '.bar', '.org.nz', '.moscow', '.care', '.software', '.quebec', '.gal', '.education', '.supply', '.yt', '.yu', '.org.ag', '.irish', '.nagoya', '.google', '.archi', '.ye', '.tz', '.tp', '.tr', '.tt', '.tw', '.tv', '.th', '.tk', '.tj', '.tm', '.tl', '.to', '.tn', '.dnp', '.asia', '.tc', '.okinawa', '.tg', '.tf', '.lgbt', '.coach', '.ceo', '.everbank', '.science', '.parts', '.fail', '.london', '.juegos', '.pub', '.trade', '.deals', '.claims', '.jetzt', '.email', '.gb', '.estate', '.clinic', '.fitness', '.reisen', '.nrw', '.audio', '.dz', '.aero', '.hamburg', '.immobilien', '.training', '.horse', '.graphics', '.cx', '.cy', '.cz', '.party', '.wien', '.cr', '.cu', '.cv', '.cw', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.\xa7\xe0\xa7\xdf\xa7\xdd\xa7\xd1\xa7\xdb\xa7\xdf', '.ca', '.blackfriday', '.cc', '.cd', '.cf', '.cg', '.zw', '.international', '.marketing', '.za', '.info', '.video', '.zm', '.diamonds', '.tech', '.finance', '.hiv', '.financial', '.engineering', '.new', '.org.es', '.menu', '.net', '.actor', '.house', '.pictures', '.gifts', '.gent', '.sap', '.watch', '.best', '.com.co', '.com.cn', '.dev', '.hiphop', '.hm', '.dental', '.hn', '.hk', '.hu', '.ht', '.hr', '.accountants', '.industries', '.mortgage', '.webcam', '.singles', '.firm.in', '.tokyo', '.dentist', '.rocks', '.tel', '.site', '.space', '.surgery', '.boutique', '.pizza', '.church', '.casa', '.cash', '.christmas', '.supplies', '.paris', '.reviews', '.plumbing', '.kitchen', '.moe', '.shoes', '.co.in', '.club', '.kaufen', '.sexy', '.here', '.qa', '.com', '.surf', '.management', '.ooo', '.guitars', '.exchange', '.gmail', '.top', '.bv', '.tax', '.citic', '.museum', '.yoga', '.today', '.ind.in', '.coffee', '.cancerresearch', '.ls', '.clothing', '.lu', '.lt', '.lv', '.ly', '.glass', '.direct', '.builders', '.la', '.com.hk', '.lc', '.lb', '.desi', '.sydney', '.li', '.lk', '.gd', '.tools', '.gg', '.ga', '.discount', '.ovh', '.gl', '.gm', '.credit', '.gh', '.gi', '.gt', '.reise', '.gp', '.gr', '.gs', '.gy', '.monash', '.work', '.ro', '.life', '.re', '.globo', '.cricket', '.rs', '.com.tw', '.rw', '.ru', '.buzz', '.foo', '.property', '.trust', '.black', '.capital', '.tienda', '.construction', '.uz', '.uy', '.us', '.partners', '.rich', '.uk', '.solutions', '.ug', '.ua', '.co.uk', '.bike', '.bargains', '.krd', '.wedding', '.travel', '.diet', '.in', '.io', '.il', '.im', '.physio', '.id', '.ie', '.rentals', '.futbol', '.ir', '.is', '.iq', '.academy', '.it', '.fish', '.boo', '.aq', '.wales', '.blue', '.condos', '.viajes', '.productions', '.vision', '.coop', '.vegas', '.durban', '.cool', '.investments', '.global', '.org.cn', '.mobi', '.guide', '.college', '.town', '.org', '.gift', '.florist', '.vu', '.vet', '.fly', '.nom.co', '.limited', '.brussels', '.edu', '.support', '.vg', '.ve', '.vc', '.va', '.koeln', '.vn', '.guru', '.youtube', '.vi', '.me.uk', '.center', '.int', '.goog', '.bzh', '.onl', '.events', '.soy', '.shiksha', '.sucks', '.net.co', '.net.cn', '.prod', '.ink', '.gle', '.berlin', '.frl', '.co.jp', '.pics', '.nyc', '.memorial', '.com.bz', '.com.br', '.how', '.mv', '.org.uk', '.mt', '.mu', '.mr', '.ms', '.mp', '.mz', '.mx', '.my', '.mw', '.mg', '.md', '.me', '.mc', '.ma', '.mn', '.mo', '.ml', '.mm', '.mk', '.mh', '.dk', '.dj', '.dm', '.do', '.business', '.de', '.xyz', '.catering', '.farm', '.dance', '.nexus', '.gov', '.tattoo', '.gop', '.auction', '.goo', '.properties', '.voyage', '.technology', '.vacations', '.directory', '.holdings', '.cleaning', '.restaurant', '.holiday', '.link', '.scot', '.fund', '.institute', '.com.es', '.yokohama', '.airforce', '.money', '.rip', '.cruises', '.ninja', '.je', '.lat', '.jo', '.jm', '.jp', '.click', '.alsace', '.photo', '.wtf', '.bayern', '.\xa7\xe2\xa7\xe6', '.capetown', '.gen.in', '.immo', '.org.in', '.lr', '.computer', '.domains', '.agency', '.zone', '.land', '.net.in', '.yandex', '.careers', '.garden', '.delivery', '.uol', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sa', '.sb', '.sc', '.sd', '.se', '.band', '.sg', '.sx', '.sy', '.sz', '.consulting', '.idv.tw', '.sr', '.st', '.su', '.sv', '.photography', '.exposed', '.flights', '.net.nz', '.wf', '.codes', '.design', '.kim', '.ventures', '.com.ag', '.villas', '.\xa7\xe5\xa7\xdc\xa7\xe2', '.tips', '.org.tw', '.eus', '.\xa7\xde\xa7\xe0\xa7\xe3\xa7\xdc\xa7\xd3\xa7\xd1', '.foundation', '.wang', '.taipei', '.community', '.network', '.solar', '.works', '.no', '.healthcare', '.versicherung', '.nl', '.ni', '.ge', '.ng', '.nf', '.ne', '.nc', '.biz', '.na', '.creditcard', '.bid', '.nz', '.insure', '.bio', '.nu', '.nr', '.np', '.ac', '.poker', '.af', '.ag', '.ad', '.ae', '.ai', '.an', '.ao', '.al', '.am', '.ar', '.as', '.company', '.aw', '.at', '.au', '.az', '.ax', '.cards', '.melbourne', '.amsterdam', '.docs', '.bnpparibas', '.wed', '.moda', '.build', '.co.nz', '.mil', '.gallery', '.xxx', '.ws', '.uno', '.net.br', '.net.bz', '.limo', '.osaka', '.lighting', '.equipment', '.saarland', '.contractors', '.gratis'] 
    regx = r'[^\.]+('+'|'.join([h.replace('.',r'\.') for h in topHostPostfix])+')$'
    pattern = re.compile(regx,re.IGNORECASE)
    parts = urlparse(url)
    host = parts.netloc
    m = pattern.search(host)
    res =  m.group() if m else host
    if not res:
        return 'unknown'
    else:
        return res

		

def find_first_level_url_dic():
    
    global url_all_str
    global url_records

    global TLD
    
    num_all=str(len(url_records))
#    print num_all
    reg=r'https?://([a-zA-Z0-9-_.]*?'+TLD+').*?\n?'
    imgre=re.compile(reg)
    all_flu=imgre.findall(url_all_str)
    
    reduced_flu=list(set(all_flu))
    
#     idx=0
    flu_counts_dic={}
    for item in reduced_flu:
        num=all_flu.count(item)
        logging.info('************************first_level_dic_key:************************************')	
        logging.info(item)
        flu_counts_dic[item]=num
#         idx=idx+num
    all_counts_dic={}
    all_counts_dic['root_nodes']=flu_counts_dic
    
    return all_counts_dic
	
	
	
def https_http_cmp(url):
    TLD=findTLD(url)
    f1=open(TLD+'.txt','r')
    url_list=f1.readlines()
    f1.seek(0,0)
    url_records=f1.read()
    f1.close()
    num_all=str(len(url_list))
    
    reg=r'(https://.*?'+TLD+'\S*?)'
    imgre=re.compile(reg)
    all_flu1=imgre.findall(url_records)

    reg=r'(http://.*?'+TLD+'\S*?)'
    imgre=re.compile(reg)
    all_flu2=imgre.findall(url_records)

    https_http={len(all_flu1):'https',len(all_flu2):'http'}
    print https_http




def get_reduced_dic(url_list):
    
    reduced_flu=list(set(url_list))
#    print reduced_flu
#     idx=0
    flu_counts_dic={}
    for item in reduced_flu:
        num=url_list.count(item)
        flu_counts_dic[item]=num
#         idx=idx+num
    
    return flu_counts_dic
	
	
	
def sort_nodes(dic):
    sorted_key=sorted(dic.keys(),reverse=True)
    return sorted_key
     #   print item+" : "+str(all_flu.count(item))
     
    

def find_sub_nodes(parent_url):  # parent_url is something like www.amazon.com , amazon.com/hp, help.apple.com/job/needed
    
    num_all=str(len(url_records))

    reg=r'https?://('+parent_url+'/.*?)(?:/|\n)'
    imgre=re.compile(reg)
    all_flu1=imgre.findall(url_all_str)
    
    return all_flu1


#dic_flu=find_first_level_url('apple.com')
#idx=sort_nodes(dic_flu)
#print dic_flu
#for i in idx:
#    print dic_flu[i]
#    find_sub_nodes(dic_flu[i], 'apple.com')


def handling_node_data():

    server.query_status = 'creating structure tree...'
    time.sleep(2)

    global url_all_str
    
    global num_records
    
    global url_records
    
    global TLD
    
    global url_sum_total
        
    global max_records
        
    global max_circles
		
    first_level_dic= find_first_level_url_dic()
    
    key_pool=first_level_dic['root_nodes'].keys()
		
    first_level_dic['url_sum_total']=url_sum_total
    first_level_dic['TLD_value']=TLD
		
#        server.query_status ='key_pool setted'
    for i in key_pool:
    
        sub_nodes=get_reduced_dic(find_sub_nodes(i))
        if sub_nodes!={}:
            first_level_dic[i]=sub_nodes
            sub_key_pool=sub_nodes.keys()
            for k in sub_key_pool:
                sub_nodes_2=get_reduced_dic(find_sub_nodes(k))
                if sub_nodes_2!={}:
                    first_level_dic[k]=sub_nodes_2
                    sub_key_pool_2=sub_nodes_2.keys()
                    for j in sub_key_pool_2:
                        sub_nodes_3=get_reduced_dic(find_sub_nodes(j))
                        if sub_nodes_3!={}:
                            first_level_dic[j]=sub_nodes_3
                            sub_key_pool_3=sub_nodes_3.keys()
                            for w in sub_key_pool_3:
                                sub_nodes_4=get_reduced_dic(find_sub_nodes(w))
                                if sub_nodes_4!={}:
                                    first_level_dic[w]=sub_nodes_4
                                    sub_key_pool_4=sub_nodes_4.keys()
                                    for p in sub_key_pool_4:
                                        sub_nodes_5=get_reduced_dic(find_sub_nodes(p))
                                        if sub_nodes_5!={}:
                                            first_level_dic[p]=sub_nodes_5
                                            sub_key_pool_5=sub_nodes_5.keys()
                                            for t in sub_key_pool_5:
                                                sub_nodes_6=get_reduced_dic(find_sub_nodes(p))
                                                if sub_nodes_6!={}:
                                                    first_level_dic[p]=sub_nodes_6
        #for i in first_level_dic:
        #    logging.info('************************dic_key:************************************')    
        #    logging.info(i)
        #    logging.info('dic_value:')
        #    logging.info(first_level_dic[i])

    url_all_str=''
    
    num_records=0
    
    url_records=[]
        
    url_sum_total=0
    
    TLD=''
        
    max_records=200
        
    max_circles=5
    
    server.query_status = ''    
    
    return first_level_dic






def all_in_one_func(url,crawler_mode):
    
    try: 
        server.query_status = 'pre-calculating... (in average, it takes 1 minute)'
        server.query_termination='N'
        global url_all_str
    
        global num_records
    
        global url_records
    
        global TLD
    
        global url_sum_total
        
        global max_records
        
        global max_circles
    
        url_all_str=''
    
        num_records=0
    
        url_records=[]
        
        url_sum_total=0
    
        TLD=''
        
        max_records=200
        
        max_circles=5
        
        if crawler_mode=='no_1':
            max_records=200
            max_circles=5
        elif crawler_mode=='no_2':
            max_records=600
            max_circles=30
        elif crawler_mode=='no_3':
            max_records=1800
            max_circles=100
#        server.query_status ='before findTLD called'
        TLD=findTLD(url)
#        server.query_status ='findTLD called'
        findAllUrl(url)
#        server.query_status ='findAllUrl called'
    #    https_http_cmp('www.google.com')
        
        logging.info('&&&&&&&&&&&&&&&&&&&&&&  after https_http_cmp  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')    
    
        return handling_node_data()
    except Exception as ex:
        #template = "An exception of type {0} occured. Arguments:\n{1!r}"
        #message = template.format(type(ex).__name__, ex.args)
        #return message
        return handling_node_data() #return data anyway






