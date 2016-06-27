import sys,os,re,urllib,urllib2,xbmc,xbmcplugin,xbmcgui,xbmcaddon

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
URL_INDEX='http://www.lalapaluza.ru/'

addon = xbmcaddon.Addon(id='plugin.video.lalapaluza')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def HOME():
        addD(0,'Южный парк','http://www.sp-fan.ru/episode/','s','')
        addD(0,'Симпсоны','http://www.simp-fan.ru/episode/','s','')
        addD(0,'Гриффины','http://www.grif-fan.ru/episode/','s','')
        addD(0,'Американский Папаша','http://www.dad-fan.ru//episode/','s','')
        addD(0,'Приграничный Городок','http://www.border-fan.ru/episode/','s','')

def SEASONS(url):
        #rand
        addD(1,'Случайная серия', url+'rand.php','l', '')
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
            addD(1,name, urlc,'l', URL_INDEX+thumb)

def CHOOSE(url,name):
        link = getHtml(url)
        # nname = re.match('',link)
        nname = re.compile('<meta property="og:title" content="(.*)">').match(link)
        href = re.compile('<a href="(.*)" class="video-pleer__nav-act.*">').findall(link)
        names = re.compile('<a href=".*" class="video-pleer__nav-act.*">(.*)</a>').findall(link)
        names[:0] = re.compile('<span class="video-pleer__nav-act nav-act-selected">(.*)</span>').findall(link)
        subsHref = re.compile('<a href="(.*sub=.*)" class="download" title=".*">').findall(link)
        print 'choose test'
        dialog = xbmcgui.Dialog()
        ret = dialog.select(nname, names)
        if(ret>-1):
            for s in subsHref:
                ss=url+s.split('/')[-1]
                # Save(ss,'cSub')
                # urllib.urlretrieve (ss, "C:\sub")
                # with open('mylog', 'a') as file_:
                    # file_.write(getHtml(ss))
                # Save(ss,s.split('/')[-2])
                fname='C:\sub.srt'
                Save(ss,fname)
                # ss.replace('&amp;','&')
                print 'Субтитры',ss
                # xbmc.Player().setSubtitles('C:\sub.srt')

                # subtitle=xbmc.translatePath( fname)
                # xbmc.Player().setSubtitles(fname)
                # xbmc.Player().setSubtitles(subtitle.encode("utf-8"))
                # xbmc.Player().play(playlist)
                # xbmc.Player().setSubtitles(getHtml(ss).encode("utf-8"))
            if(ret==0):
                newUrl = url
            else: 
                newUrl = url+href[ret-1].split('/')[-1]
            PLAY(newUrl,name)


def Save(target, name):
    # LstDir = __settings__.getSetting("DownloadDirectory")
    LstDir = os.path.join( addon.getAddonInfo('path'), "subs" )
    with open(name, 'w') as file_:
        file_.write(getHtml(target))

def PLAY(url,name):
        link = getHtml(url)
        match = re.compile('var videoFile = mVideoFile = \'(.+?.m3u8)\'').findall(link)
        for u in match:
                listitem = xbmcgui.ListItem(name)
                listitem.setInfo('video', {'Title': name, 'Genre': 'Humor'})
                fname='C:\sub.srt'
                subtitle=xbmc.translatePath( fname)
                xbmc.Player().play(urllib.unquote(u), listitem)
                print 'Length sub: ',len(subtitle),' ',subtitle
                print 'Length sub end '
                while not xbmc.Player().isPlaying():
                    xbmc.sleep(10) #wait until video is being played
                xbmc.Player().setSubtitles(fname);
                # if len(subtitle) > 0:
                #     for _ in xrange(30):
                #         if xbmc.Player().isPlaying():
                #             break
                #         time.sleep(1)
                #     xbmc.Player().setSubtitles(subtitle)
                # playMedia(urllib.unquote(u), 'C:\sub.srt')
                # fname='C:\sub.srt'
                # subtitle=xbmc.translatePath( fname)
                # xbmc.Player().setSubtitles(fname)
                # xbmc.Player().showSubtitles(True)
                # xbmc.Player().setSubtitles(subtitle.encode("utf-8"))

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