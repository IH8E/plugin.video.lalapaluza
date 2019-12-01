# -*- coding: utf-8 -*-
import sys, os, re, xbmcplugin, xbmcgui
from xbmcaddon import Addon
from urllib import unquote
from xbmc import Player, sleep
import settings
from utils import get_param, add_item, format_name, save_file, get_html, save_subs

addon = Addon(id='plugin.video.lalapaluza')


def HOME():
    for name_url in settings.NAME_URLS:
        try:
            print name_url['name'], name_url['url']
            add_item(name=name_url['name'], url=name_url['url'])
        except KeyError:
            pass


def SEASONS(url):
    add_item(name='Случайная серия', url=url + 'rand.php', mode='l')  # random video
    link = get_html(url)
    matchurl = re.compile('<li><a href="(.*)" title=".*" class="big.*>').findall(link)
    matchname = re.compile('<li><a href=".*" title="(.*)" class="big.*>').findall(link)
    for urlc, name in zip(matchurl, matchname):
        add_item(name=name, url=urlc, mode='e')


def EPISODES(url):
    link = get_html(url)
    matchurl = re.compile('<div class="ep_block">\s*<a href="(.*)">').findall(link)
    matchthumb = re.compile('<div class="ep_block">\s*<a href=".*?">\s*<img src="(.*?[.jpg|.png])".*>').findall(link)
    matchname = re.compile('<td class="episode-name">\s*(.*?)\s*</td>').findall(link)
    for urlc, thumb, name in zip(matchurl, matchthumb, matchname):
        add_item(X=1, name=format_name(name, urlc), url=urlc, mode='l', thumb='http:' + thumb)


def CHOOSE(url, name):
    link = get_html(url)
    title_name = link.split('<title>')[1].split('</title>')[0]
    href = re.compile('<a href="(.*)" class="video-pleer__nav-act.*">').findall(link)
    names = re.compile('<a href=".*" class="video-pleer__nav-act.*">(.*)</a>').findall(link)
    names[:0] = re.compile('<span class="video-pleer__nav-act nav-act-selected">(.*)</span>').findall(link)
    subs_href = re.compile('<a href="(.*sub=.*)" class="download" title=".*">').findall(link)
    dialog = xbmcgui.Dialog()
    ret = dialog.select(title_name, names)
    if ret > -1:
        if ret == 0:
            new_url = url
        else:
            new_url = url + href[ret - 1].split('/')[-1]
        PLAY(new_url, name, subs_href)


def PLAY(url, name, sub_files=[]):
    link = get_html(url)
    match = re.compile('\'(.+?.m3u8)\'').findall(link)
    for u in match:
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Humor'})
        Player().play(unquote(u), listitem)
        while not Player().isPlaying():
            sleep(10)  # wait until video is being played
        for s in save_subs(path=addon.getAddonInfo('path'), subs_href=sub_files, url=url):
            Player().setSubtitles(s)

url = get_param("url")
name = get_param("name")
mode = get_param("mode")

if mode is None or url is None or len(url) < 1:
    HOME()
elif mode == 's':
    SEASONS(url)
elif mode == 'e':
    EPISODES(url)
elif mode == 'l':
    CHOOSE(url, name)
elif mode == 'v':
    PLAY(url, name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
