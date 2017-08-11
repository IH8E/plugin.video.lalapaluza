# -*- coding: utf-8 -*-
import sys
from urllib import quote_plus, unquote_plus
from urllib2 import urlopen, Request
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem
import settings
import os


def add_item(name, url, X=0, mode='s', thumb='', plot='defaultDescription'):  # addDir if X==0|addDownLink if X==1
    u = (sys.argv[0] +
         "?url=" + quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + quote_plus(name))
    liz = ListItem(name, iconImage="DefaultFolder.png" if X == 0 else "DefaultVideo.png",
                           thumbnailImage=thumb)
    liz.setInfo(type="Video", infoLabels={"Title": name, "plotoutline": plot})
    ok = addDirectoryItem(handle=int(sys.argv[1]),
                                     url=u, listitem=liz, isFolder=True if X == 0 else False)
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def format_name(name, url):
    return '[' + url.split('/')[-2] + '] ' + name


def save_file(target, name):
    with open(name, 'w') as file_:
        file_.write(get_html(target))


def get_html(url):
    req = Request(url)
    req.add_header('User-Agent', settings.USER_AGENT)
    response = urlopen(req)
    data = response.read()
    response.close()
    return data


def get_param(index):
    result = None
    try:
        result = unquote_plus(get_params()[index])
    except:
        pass
    return result


def save_subs(url, path, subs_href):
    subs_dir = os.path.join(path, settings.SUBS_DIRECTORY)
    if not os.path.exists(subs_dir):
        try:
            os.makedirs(subs_dir)
        except:
            subs_dir = path
    subs = []
    for s in subs_href:
        s_list = s.split('/')
        ss = url + s_list[-1]
        filename = s_list[-2] + s_list[-1][5:7] + '.srt'
        sub_name = os.path.join(subs_dir, filename)
        try:
            save_file(ss, sub_name)
            subs.append(sub_name)
        except:
            pass
    return subs