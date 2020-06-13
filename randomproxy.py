#importing used packages
import requests,random,fake_useragent,socket

#importing BeautifulSoup from its main lib
from bs4 import BeautifulSoup

#making my oun error type
class IncorrectInfo(Exception):
    pass

#start
def free_proxy_list_api(includes=False):
    #i was too lazy to rewrite the code , it was the fastest soloutin
    country=includes

    #proxies that had a reply
    pr=[]

    #fun begins
    try:

        #sending a requests with fake user agent (in case the site have some protections)
        r=requests.get("http://www.socks-proxy.net/",headers={"user-agent":fake_useragent.UserAgent().random})

    #EXP always says that when you get a error from
    #free-proxy-list , it is because it's blocked in
    #your country or by google and you need to use a
    #vpn to make a connection.

    #if we were not able to send a requests
    except ConnectionError:
        ConnectionError("can not connect to free-proxy-list.net now. check your connection.")

    #getting site's source
    r2=r.text

    #check if the connection status is 200 (it means the connection is stablished)
    if r.status_code == 200:

        #if there was malicious error shit
        if "This website has been classified as malicious" in r.text:

            #say some shit
            raise ConnectionError("This website has been classified as malicious")

        #parsing site's html source code
        soup = BeautifulSoup(r2,"html.parser")

        #findig tables
        ta=soup.find("table")

        #if the status code is 403 or it's 200 but we can not access contents
        if (("403" in r2 and "forbidden" in r2) or "403" in r2 and "Forbidden" in r2) and str(r.status_code).startswith("4"):
            raise ConnectionError("website is fucking with us , turn on VPN.")

        #finding table rows
        tr=ta.find_all("tr")

        #making the list of found proxies
        p=[]

        #enter to table rows
        for i in tr:

            #finding <td> tags in the rows
            td=i.find_all("td")

            #if there is codes that matchs with the information we asked for
            if td is not None:

                #this is a python trick that you can read about it in google
                ro=[e.text for e in td]

                #if we had a custom word
                if country is not False:
                    problem=False
                    #if ro includes the word
                    for i in country.split(","):

                        if i in ro:
                            continue
                        else:
                            problem=True
                    if problem is not True:
                        #adding the proxy to the list
                        p.append(ro)
                #if there was no custom word:
                else:

                    #adding the word to the list
                    p.append(ro)


            #if there was no td <td> tags show an error (because it means there is a problem with the site)
            else:
                raise ConnectionError("website is fucking with us , turn on VPN.")

        #if nothing found thad matches with information
        if len(p) == 0:

            #raise my beautiful error :)
            raise IncorrectInfo("can not find any proxy that matches with the information . try using this form : india = India")

        #if there is no custom country
        else:
            #adding the information we got from <td> tags
            p.append(ro)

        #finding proxies with reply(s)
        for i in range(len(p)):

            #tbh , i was just too lazy to rewrite all the code , that's why sa exist.
            sa=p[i]

            #trying to make a connection with the proxy
            try:

                #defind a socket
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

                #connecting to the proxy
                s.connect((sa[0],int(sa[1])))

                #sending some data
                s.send(b"test")

                #closing the connection
                s.close()

            #if there was a problem
            except :

                #don't give a fuck
                pass

            #if there wasn't a problem
            else:

                #add the proxy to the list of ok proxies
                pr.append(sa)
        
        #return a random proxy from ok proxies list
        return random.choice(pr)

    #if the status code is not 200 (it means there is a problem)
    else:

        #When something is filtered in iran, we will be redirected to a page with these tags (It is called 'peyvandha', you can get more info about it in wikipedia):
        Iran_filter = [
            '<html><head><meta http-equiv="Content-Type" content="text/html; charset=',
            '"><title>HT1-15(2)</title></head><body><iframe src="',
            '" style="width: 100%; height: 100%" scrolling="no" marginwidth="0" marginheight="0" frameborder="0" vspace="0" hspace="0"></iframe></body></html>\r\n\r\n'
        ]
        #So if it had these tags in it, it means we are in iran and we need to use VPN
        if Iran_filter[0] in r.text and Iran_filter[1] in r.text and Iran_filter[2] in r.text :
            raise ConnectionError("We are in iran and we need to use VPN. (Fucking stupid rules >:( )")
        #If it didn't have these tags, just do:
        else:
            #as i said , i'm too lazy . so i just give the user the status code
            raise ConnectionError("we have status code "+str(r.status_code)+" and we can't connect .\nText : "+r.text)