import sys,os,re,urllib,urllib2,xbmc,xbmcplugin,xbmcgui,xbmcaddon

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
URL_INDEX='http://www.lalapaluza.ru/'
addon = xbmcaddon.Addon(id='plugin.video.lalapaluza')
SUBS_DIRECTORY = 'subs'

def HOME():
    addD(0,'Южный парк','http://www.sp-fan.ru/episode/','s','')
    addD(0,'Симпсоны','http://www.simp-fan.ru/episode/','s','')
    addD(0,'Гриффины','http://www.grif-fan.ru/episode/','s','')
    addD(0,'Американский Папаша','http://www.dad-fan.ru//episode/','s','')
    addD(0,'Приграничный Городок','http://www.border-fan.ru/episode/','s','')

def SEASONS(url):
    addD(1,'Случайная серия', url+'rand.php','l', '') #random video
    link = getHtml(url)
    matchurl = re.compile('<li><a href="(.*)" title=".*" class="big.*>').findall(link)
    matchname = re.compile('<li><a href=".*" title="(.*)" class="big.*>').findall(link)
    for urlc,name in zip(matchurl, matchname):
        addD(0,name, urlc,'e', '')
        
def EPISODES(url):
    link = getHtml(url)
    matchurl = re.compile('<div class="ep_block">\s*<a href="(.*)">').findall(link)
    matchthumb = re.compile('<div class="ep_block">\s*<a href=".*?">\s*<img src="(.*?[.jpg|.png])".*>').findall(link)
    matchname = re.compile('<td class="episode-name">\s*(.*?)\s*</td>').findall(link)
    for urlc,thumb,name in zip(matchurl, matchthumb, matchname):
        addD(1,formatName(name,urlc), urlc,'l', URL_INDEX+thumb)

def formatName(name,url):
    return '['+url.split('/')[-2]+'] '+name

def CHOOSE(url,name):
    link = getHtml(url)
    nname = link.split('<title>')[1].split('</title>')[0]
    href = re.compile('<a href="(.*)" class="video-pleer__nav-act.*">').findall(link)
    names = re.compile('<a href=".*" class="video-pleer__nav-act.*">(.*)</a>').findall(link)
    names[:0] = re.compile('<span class="video-pleer__nav-act nav-act-selected">(.*)</span>').findall(link)
    subsHref = re.compile('<a href="(.*sub=.*)" class="download" title=".*">').findall(link)
    dialog = xbmcgui.Dialog()
    ret = dialog.select(nname, names)
    if(ret>-1):
        if(ret==0):
            newUrl = url
        else: 
            newUrl = url+href[ret-1].split('/')[-1]
        PLAY(newUrl,name,subsHref)

def saveFile(target, name):
    with open(name, 'w') as file_:
        file_.write(getHtml(target))

def saveSubs(subsHref=[]):
    subs = []
    for s in subsHref:
        sList = s.split('/')
        ss=url+sList[-1]
        fileName = sList[-2]+sList[-1][5:7]+'.srt'
        subName = os.path.join( addon.getAddonInfo('path'), SUBS_DIRECTORY,fileName)
        saveFile(ss,subName)
        subs.append(subName)
    return subs

def PLAY(url,name,subFiles=[]):
    link = getHtml(url)
    match = re.compile('var videoFile = mVideoFile = \'(.+?.m3u8)\'').findall(link)
    for u in match:
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Humor'})
        xbmc.Player().play(urllib.unquote(u), listitem)
        while not xbmc.Player().isPlaying():
            xbmc.sleep(10) #wait until video is being played
        for s in saveSubs(subFiles):
            xbmc.Player().setSubtitles(s);                

def playMedia(mediafile, subfile):
    player = xbmc.Player()
    player.play(mediafile)
    if len(subfile) > 0:
        for _ in xrange(30):
            if player.isPlaying():
                break
            time.sleep(1)
        player.setSubtitles(subfile)
    return
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

def addD(X,name,url,mode,iconimage,plot='defaultDescription'): #addDir if X==0|addDownLink if X==1
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png" if X==0 else "DefaultVideo.png",
                           thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "plotoutline" : plot })
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