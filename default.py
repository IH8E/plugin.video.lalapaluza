import sys,re,urllib,urllib2,xbmc,xbmcplugin,xbmcgui

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
URL_INDEX='http://www.lalapaluza.ru/'

def HOME():
        addD(0,'South Park','http://www.sp-fan.ru/episode/','s','')
        addD(0,'Simpsons','http://www.simp-fan.ru/episode/','s','')
        addD(0,'Family Guy','http://www.grif-fan.ru/episode/','s','')

def SEASONS(url):
        link = getHtml(url)
        matchurl = re.compile('<li><a href="(.*)" title=".*" class="big.*>').findall(link)
        matchname = re.compile('<li><a href=".*" title="(.*)" class="big.*>').findall(link)
        for urlc,name in zip(matchurl, matchname):
            addD(0,name, urlc,'e', '')
        
def EPISODES(url):
        link = getHtml(url)
        matchurl = re.compile('<div class="ep_block">\s*<a href="(.*)">').findall(link)
        matchthumb = re.compile('src="(.*.jpg)".*>\s*<table class="episode-name-outer">').findall(link)
        matchname = re.compile('<td class="episode-name">\s*(.*?)\s*</td>').findall(link)
        for urlc,thumb,name in zip(matchurl, matchthumb, matchname):
            addD(1,name, urlc,'l', URL_INDEX+thumb)

def CHOOSE(url,name):
        link = getHtml(url)
        href = re.compile('<a href="(.*)" class="video-pleer__nav-act.*">').findall(link)
        names = re.compile('<a href=".*" class="video-pleer__nav-act.*">(.*)</a>').findall(link)
        names[:0] = re.compile('<span class="video-pleer__nav-act nav-act-selected">(.*)</span>').findall(link)
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Выберите озвучку', names)
        if(ret>-1):
            if(ret==0):
                newUrl = url
            else: 
                newUrl = url+href[ret-1].split('/')[-1]
            PLAY(newUrl,name)
		
def PLAY(url,name):
        link = getHtml(url)
        match = re.compile('var videoFile = mVideoFile = \'(.+?.m3u8)\'').findall(link)
        for u in match:
                listitem = xbmcgui.ListItem(name)
                listitem.setInfo('video', {'Title': name, 'Genre': 'Humor'})
                xbmc.Player().play(urllib.unquote(u), listitem)

def getHtml(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data

def getParams():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?','')
                if (params[len(params)-1] == '/'):
                        params = params[0:len(params)-2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
        return param

def addD(X,name,url,mode,iconimage): #addDir if X==0|addDownLink if X==1
        u = (sys.argv[0] +
             "?url=" + urllib.quote_plus(url) +
             "&mode=" + str(mode) +
             "&name=" + urllib.quote_plus(name))
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png" if X==0 else "DefaultVideo.png",
                               thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                         url=u, listitem=liz, isFolder=True if X==0 else False)
        return ok		

params = getParams()
try:
        url = urllib.unquote_plus(params["url"])
except:
        url = None
try:
        name = urllib.unquote_plus(params["name"])
except:
        name = None
try:
        mode = urllib.unquote_plus(params["mode"])
except:
        mode = None

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
if mode == None or url == None or len(url)<1:
        HOME()
elif mode == 's':
        SEASONS(url)
elif mode == 'e':
        EPISODES(url)
elif mode == 'l':
        CHOOSE(url,name)
elif mode == 'v':
        PLAY(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))