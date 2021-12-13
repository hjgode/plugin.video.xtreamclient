# Module: main
# Author: HJ_G.
# Created on: 07.12.2021
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Example video Xtream client plugin that is compatible with Kodi 19.x "Matrix" and above?
"""
import sys
import os
from urllib.parse import urlencode, parse_qsl

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

import web_pdb

import re

# create a class for your addon, we need this to get info about your addon
ADDON = xbmcaddon.Addon()
# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
CWD = ADDON.getAddonInfo('path') #.decode('utf-8')
sys.path.append(CWD)

def log(msg, level=xbmc.LOGINFO):
    plugin = "plugin.video.xtreamclient"

#    if isinstance(msg, unicode):
#    msg = msg.encode('utf-8')

    xbmc.log("[%s] %s" % (plugin, msg.__str__()), level)
    
log(CWD)

#for development use this
#import xtreamcode_config as cfg


from client import Client
from connection import Connection

from series_xtream import *

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

# disable in development!
myconfig={} # cfg.config
def get_settings():
    log("get_settings...")
    global myconfig
    myconfig={}
    my_addon = xbmcaddon.Addon()
    log("get_settings addon="+str(my_addon.getAddonInfo('path')))
    #     url = cfg.config["url"] + ":" + cfg.config["port"] + "?username=" + cfg.config["username"] + "&password=" + cfg.config["password"]
    myconfig['url']=my_addon.getSetting('sett_website')
    myconfig['username']=my_addon.getSetting('sett_username')
    myconfig['password']=my_addon.getSetting('sett_password')
    myconfig['port']=my_addon.getSetting('sett_portnumber')
    myconfig['filter']=my_addon.getSetting('sett_filter')
    myconfig['filter_is_regex']=my_addon.getSetting('sett_filter_is_regex') # returns the string 'true' or 'false'
    my_addon.setSetting('my_setting', 'false')
    return myconfig

from categories_class import Categories

"""
def get_vod_categories(myclient, myfilter):
    mylist=myclient.vod_categories()
    cats=Categories()
    log ("myfilter="+myfilter)
    if isinstance (mylist, list):        
        for o in mylist :
            if len(myfilter)>0:
                if o['category_name'].startswith(myfilter):                
                    cats.add(o['category_name'], o['category_id'])
                #categories[o['category_name']]={}
                #categories[o['category_name']]['category_name']=o['category_name']
                #categories[o['category_name']]['category_id']=o['category_id']
            else:
                cats.add(o['category_name'], o['category_id'])
                
    if isinstance (mylist, dict):
        print ('ERROR, not a list')
    return cats    
#    return mylist
"""

def get_live_categories(myclient, myfilter:str, myregex:str):
    mylist = myclient.live_categories() #this returns a list of json objects
    cats=Categories()
    #TODO: remove for release
    #web_pdb.set_trace()

    log ("myfilter = "+myfilter+", regex="+myregex)
    if isinstance (mylist, list):        
        for o in mylist :
            if len(myfilter)>0:
                if myregex=="true":
                    re.compile(myfilter)
                    if re.match(myfilter, o['category_name']):
                        cats.add(o['category_name'], o['category_id'])    
                    pass
                else:
                    if o['category_name'].startswith(myfilter):                
                        cats.add(o['category_name'], o['category_id'])
            else:
                cats.add(o['category_name'], o['category_id'])
                
    if isinstance (mylist, dict):
        print ('ERROR, not a list')
    return cats    
    
def start_connection():
    global myconfig
    url = myconfig["url"] + ":" + myconfig["port"] + "?username=" + myconfig["username"] + "&password=" + myconfig["password"]
    client=Client(url)
    #print(client)
    return client

def get_Vod_categories():
    myclient=start_connection()
    categories=myclient.vod_categories()
    return categories

def get_Live_categories():
    log('get_Live_categories...')
    myconfig=get_settings()
    myclient=start_connection()
    log("myconfig is '" + str(myconfig) + "'")
    categories=get_live_categories(myclient, myconfig['filter'], myconfig['filter_is_regex'])
    return categories    

def get_Live_by_category(category):
    myclient=start_connection()
    videos=myclient.live_streams_by_category(category)    
    mylist=[]
    if isinstance (videos, list):        
        for o in videos :
            #TODO: fixme Mapping
            if o['epg_channel_id']!=None:
                item={}
                item['name']=o['name']
                item['video']=o['direct_source']
                item['thumb']=o['stream_icon']
                item['category']=category
                item['category_id']=o['category_id']
                item['epg_channel_id']=o['epg_channel_id']
                mylist.append(item)
                #mylist[o['name']]=item
                #categories[o['category_name']]={}
                #categories[o['category_name']]['category_name']=o['category_name']
                #categories[o['category_name']]['category_id']=o['category_id']
                #cats.add(o['category_name'], o['category_id'])
                
    if isinstance (videos, dict):
        item={}
        item['name']=o['name']
        item['video']=o['direct_source']
        item['thumb']=o['stream_icon']
        mylist[o['name']]=item

    return mylist

def get_vod_by_category(category):
    myclient=start_connection()
    videos=myclient.vod_streams_by_category(category)    
    mylist=[]
    if isinstance (videos, list):        
        for o in videos :
            #TODO: fixme Mapping
            item={}
            item['name']=o['name']
            item['video']=o['direct_source']
            item['thumb']=o['stream_icon']
            item['category']=category
            item['category_id']=o['category_id']
            item['year']=o['year']
            item['thumb']=o['stream_icon']
            item['plot']=o['plot']
            item['genre']=o['genre']
            item['title']=o['title']
            mylist.append(item)
            #mylist[o['name']]=item
            #categories[o['category_name']]={}
            #categories[o['category_name']]['category_name']=o['category_name']
            #categories[o['category_name']]['category_id']=o['category_id']
            #cats.add(o['category_name'], o['category_id'])
                
    return mylist

VIDEOS = get_Live_categories()
VOD = get_Vod_categories()


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(_URL, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or API.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    return VIDEOS.get_categories().keys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or API.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    vids=get_Live_by_category(category)
    log("### list video for category="+category)
    return vids #VIDEOS.get_id(category)

def get_vod_videos(category):
    vids=get_vod_by_category(category)
    log("### list video for category="+category)
    return vids #VIDEOS.get_id(category)

def list_stream_types():
    global CWD
    myconfig=get_settings()
    mysettfilter=myconfig['filter']
    mysettisregex=myconfig['filter_is_regex']
    log('list_stream_types: Filter="'+mysettfilter+'", regex='+mysettisregex)
    xbmcplugin.setPluginCategory(_HANDLE, 'Select stream type:')
    
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'files')
    # Get video categories
    TYPES = {'Live Streams': [{'name': 'livestreams',
                       'thumb': os.path.join( CWD, 'resources', 'live_icon.jpg' )}],
             'Videos': [{'name': 'videos',
                        'thumb': os.path.join( CWD, 'resources', 'vod_icon.jpg' )}],
             'Series': [{'name': 'series',
                       'thumb': os.path.join( CWD, 'resources', 'series_icon.jpg' ),}]
                       }
    # Iterate through categories
    for t in TYPES:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=t)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        #TODO: fixme
#        image= os.path.join( CWD, 'resources', 'live_icon.jpg' )
        list_item.setArt({'icon': TYPES[t][0]['thumb']})
        #list_item.setArt({'thumb': VIDEOS.get_categories()[category][0]['thumb'],
        #                  'icon': VIDEOS.get_categories()[category][0]['stream_icon'],
        #                  'fanart': VIDEOS.get_categories()[category][0]['thumb']})
        
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': t,
                                    'genre': t,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='list', type=TYPES[t][0]['name'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_live_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'Livestreams Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        
        #TODO: fixme
        #list_item.setArt({'thumb': VIDEOS.get_categories()[category][0]['thumb'],
        #                  'icon': VIDEOS.get_categories()[category][0]['stream_icon'],
        #                  'fanart': VIDEOS.get_categories()[category][0]['thumb']})
        
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'set': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_vod_categories():
    global VOD
    global myconfig
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'VideoOnDemand Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video categories
    categories = get_Vod_categories()
    # Iterate through categories
    log("###list_vod_categories: "+str(categories))
    vods=Categories()
    filterstr=myconfig['filter']
    filterregex=myconfig['filter_is_regex']
    try:
        p=re.compile(filterstr);
    except Exception:
        log("ERROR with regex: "+filterstr)
    if p==None:
        filterregex='false'    
    for category in categories:
        if len(filterstr)>0:
            if filterregex=="true":
                if p.match(filterstr, category['category_name'])==None:
                    continue
            elif not category['category_name'].startswith(filterstr):
                continue
        #Need a global?
        vods.add(category['category_name'], category['category_id'])
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['category_name'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        #list_item.setArt({'thumb': VIDEOS.get_categories()[category][0]['thumb'],
        #                  'icon': VIDEOS.get_categories()[category][0]['stream_icon'],
        #                  'fanart': VIDEOS.get_categories()[category][0]['thumb']})
        
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category['category_name'],
                                    'set': category['category_id'],
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='list_vod_for_cat', category_id=category['category_id'], category_name=category['category_name'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    #global
    VOD=vods
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_live_streams(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, category)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    id=VIDEOS.get_id(category)
    videos = get_videos(id) # get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        id=video['category_id']
        genre=VIDEOS.get_name(id)
        list_item.setInfo('video', {'title': video['name'],
                                    'set': genre, #video['category'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_vod_streams(category_id, category_name):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, category_name)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    #FIXME: need another global for VODs
    id=category_id
    videos = get_vod_videos(id) # get_videos(category)
    log("list_vod_streams...")
    # Iterate through videos.
    for video in videos:
        log("list_vod_streams, list_item=video: "+str(video))
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        id=video['category_id']
        genre=VIDEOS.get_name(id) #change for VOD
        list_item.setInfo('video', {'title': video['name'],
                                    'set': genre, #video['category'],
                                    'year':video['year'],
                                    'mediatype': 'video',
                                    "plot" : video["plot"]})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    myconfig=get_settings()
    log("filter: "+myconfig['filter']+", regex: "+myconfig['filter_is_regex'])
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    log("###router called with: " + str(params))
    if params:
        # url = get_url(action='list_vod_for_cat', category=category['category'], category_id=category['category_id'])
        if params['action'] == 'list_vod_for_cat':
#            if params['category']:
#                log("router calling list_vod_for_category...")
             if params['category_id']:
                 list_vod_streams(params['category_id'], params['category_name'])

        elif params['action']=="list_series_in_category":
            if params['category_id'] and params['category_name']:
                log("router: list_series_in_category/"+params['category_id'] + ", " + params['category_name'])
                list_series_in_category(params['category_name'], params['category_id'])

        elif params['action']=="list_seasons_in_serie":
            if params['serie_id'] and params['serie_name'] and params['category_name']:
                log("router: list_seasons_in_serie/"+params['category_name']+ ", "+params['serie_name'] + ", " + params['serie_id'])
                list_seasons_in_serie(params['category_name'], params['serie_name'], params['serie_id'])
                log("router: list_seasons_in_serie DONE")
        elif params['action']=="list_episodes_in_season":
            #list_episodes_in_season(season_number:str, series_name:str, series_id:str):
            log("router() list_episodes_in_season...")
            if params['season_number'] and params['serie_name'] and params['serie_id']:
              list_episodes_in_season(params['season_number'], params['serie_name'], params['serie_id'])
            pass

        elif params['action'] == 'list': #list called with type = livestreams,videos or series
            if params['type']=='livestreams':
                log("router calling list_live_categories...")
                list_live_categories()
            elif params['type']=='videos':
                list_vod_categories()
            elif params['type']=='series':
                list_series_categories()

        elif params['action'] == 'listing':
            # Display the list of videos in a provided category.
            #log("###listing for category: "+params['category'])
            list_live_streams( params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_stream_types() #list_live_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
