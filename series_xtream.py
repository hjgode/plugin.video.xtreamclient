#series xtream API
# Module: series_xtream
# Author: HJ_G.
# Created on: 09.12.2021
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Xtream series is organized as:
     Series Categories (ie DE ACTION)
      + Series Infos (ie Game of Thrones)
        + Season 1
          + Episode 1
          + Episode 2
          + ...
        + Season 2
        ...
      + another series info
        + Season x

first get the categories
then list the series (see series_info)
then list the seasons (see series_info) with streams attached
"""
"""
    url routing
    -----------
    list series categories:
    action=                     params=                     function
    list                        series                      list_series_categories()

    list series in selected category:
    list_series_by_category     category_name
                                category_id                 list_series_by_category

    list seasons in selected series:
    list_seasons_in_series     category_name
                                category_id                 list_seasons_in_series

    list episodes in selected season:
    list_episodes_in_serie      series_id
                                season_number

    play video
"""

import sys
import os
from urllib.parse import urlencode, parse_qsl

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# create a class for your addon, we need this to get info about your addon
ADDON = xbmcaddon.Addon()
# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
CWD = ADDON.getAddonInfo('path') #.decode('utf-8')
sys.path.append(CWD)

def log(msg, level=xbmc.LOGINFO):
    plugin = "plugin.video.xtreamclient"
    xbmc.log("[%s] %s" % (plugin, msg.__str__()), level)
    
log(CWD)

#import xtreamcode_config as cfg

from client import Client
from connection import Connection

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

myconfig={} # cfg.config
def get_settings():
    log("get_settings...")
    global myconfig
    myconfig={}
    my_addon = xbmcaddon.Addon()
    #     url = cfg.config["url"] + ":" + cfg.config["port"] + "?username=" + cfg.config["username"] + "&password=" + cfg.config["password"]
    myconfig['url']=my_addon.getSetting('sett_website')
    myconfig['username']=my_addon.getSetting('sett_username')
    myconfig['password']=my_addon.getSetting('sett_password')
    myconfig['port']=my_addon.getSetting('sett_portnumber')
    myconfig['filter']=my_addon.getSetting('sett_filter')
    myconfig['filter_is_regex']=my_addon.getSetting('sett_filter_is_regex') # returns the string 'true' or 'false'
    my_addon.setSetting('my_setting', 'false')
    return myconfig

#from categories_class import Categories

myclient=None
def start_connection():
    myconfig=get_settings()
    url = myconfig["url"] + ":" + myconfig["port"] + "?username=" + myconfig["username"] + "&password=" + myconfig["password"]
    client=Client(url)
    #print(client)
    return client

#use a global to cache info
myinfo=None
def get_myinfo(series_id:str):
    global myclient
    global myinfo
    if myinfo==None:
        myclient=start_connection()
        myinfo = myclient.series_info_by_id(series_id)
    return myinfo
    pass

def get_series_categories_list(myclient:Client, myfilter:str):
  """get a list with dicts of categories filtered by filter
    if filter is "" all categories are listed
    
    Parameters
    ----------
      myclient: Client: 
        the connected Xtream Client to use
      myfilter: Str:
        the fileter string, ie "" for all or "DE " for all categories that name starts with "DE "
    
    Returns
    -------
      list[] with dicts 
        print (mylist[0].keys())
        dict_keys(['category_id', 'category_name', 'parent_id'])
  """
  #clear cached info
  global myinfo
  myinfo=None
  data=myclient.series_categories()
  
  mylist=[]
  log ("myfilter="+myfilter)
  if isinstance (data, list):        
    for o in data :
      if len(myfilter)>0:
        if o['category_name'].startswith(myfilter):
          item={}
          item['category_name']=o['category_name']
          item['category_id']=o['category_id']
          mylist.append(item)                
      else:
        item={}
        item['category_name']=o['category_name']
        item['category_id']=o['category_id']
        mylist.append(item)                
  elif isinstance (mylist, dict):
    print ('ERROR, not a list')
  return mylist    

#global myclient

def get_Series_Info_by_id(series_id):
  """
  we get all the seasons and episodes in one call

  """
  myclient=start_connection()
  streams=myclient.series_info_by_id(series_id)    
  mylist=[]
  if isinstance (streams, list):        
    for o in streams :
          #TODO: fixme Mapping
          if o['name']!=None:
              item={}
              item['season']=o['season_number'] #season
              item['episode']
              item['stream_id']=o['id'] #used as stream name
              mylist.append(item)
            
    if isinstance (streams, dict):
        item={}
        item['name']=o['name'] #season
        item['stream_id']=o['id'] #used as stream name
        mylist.append(item)
        mylist[o['name']]=item

  return mylist

def get_Series_by_category(category):
    myclient=start_connection()
    videos=myclient.series_streams_by_category(category)    
    mylist=[]
    if isinstance (videos, list):        
        for o in videos :
            #TODO: fixme Mapping
            if o['name']!=None:
                item={}
                item['name']=o['name']
                item['series_id']=o['series_id']
                item['thumb']=o['cover']
                item['category']=category
                item['category_id']=o['category_id']
                item['plot']=o['plot']
                mylist.append(item)
                #mylist[o['name']]=item
                #categories[o['category_name']]={}
                #categories[o['category_name']]['category_name']=o['category_name']
                #categories[o['category_name']]['category_id']=o['category_id']
                #cats.add(o['category_name'], o['category_id'])
                
    if isinstance (videos, dict):
        item={}
        item['name']=o['name']
        item['series_id']=o['series_id']
        item['thumb']=o['cover']
        mylist[o['name']]=item

    return mylist


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    url='{}?{}'.format(_URL, urlencode(kwargs))
    log("get_url: urlencode()="+url)
    return url

def get_Series_by_category_list(myclient:Client,category_name:str,category_id:str):
  """get a list of series for a category_id

    Parameters
    ----------
      myclient: Client: 
        the connected Xtream Client to use
      category_name : str: 
        category name for the series    
      category_id : str: 
        the id to be used to get the series    

    Returns
    -------
      list[] with dicts 
      print(series_for_category[0].keys())

      dict_keys(['name', 'series_id', 'thumb', 'category_name', 'category_id', 'plot'])
  """
  data=myclient.series_streams_by_category(category_id)    
  mylist=[]
  if isinstance (data, list):        
    for o in data :
      if o['name']!=None:
        item={}
        item['name']=o['name']
        item['series_id']=o['series_id']
        item['thumb']=o['cover']
        item['category_name']=category_name
        item['category_id']=o['category_id']
        item['plot']=o['plot']
        mylist.append(item)          
  elif isinstance (data, dict):
    o=data
    if data['name']!=None:
      item={}
      item['name']=o['name']
      item['series_id']=o['series_id']
      item['thumb']=o['cover']
      item['category_name']=category_name
      item['category_id']=o['category_id']
      item['plot']=o['plot']
      mylist.append(item)          
  return mylist

############# XBMC lists
"""     action=                     params=
        list                        series
"""

def list_series_categories():
    log("### list_series_category()...")
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'Series Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video categories
    myclient=start_connection()
    categories = get_series_categories_list(myclient, "DE ")
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['category_name'])
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
        list_item.setInfo('video', {'title': category['category_name'],
                                    'set': category['category_id'],
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='list_series_in_category', category_name=category['category_name'], category_id=category['category_id'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_series_in_category(category_name:str, category_id:str):
    log("### list_series_in_category")
    xbmcplugin.setPluginCategory(_HANDLE, category_name)
    xbmcplugin.setContent(_HANDLE, 'tvshows')
    myclient=start_connection()
    series = get_Series_by_category_list(myclient, category_name, category_id) # get_videos(category)
    """
    list[] with dicts print(series_for_category[0].keys())
    dict_keys(['name', 'series_id', 'thumb', 'category_name', 'category_id', 'plot'])
    """
    # Iterate through the series.
    #TODO: add total episodes count? But that would require to get every series info for the listed series
    for serie in series:
        serie_id=serie['series_id']
        serie_name=serie['name']
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=serie_name)
        list_item.setInfo('video', {'title': serie_name,
                                    'set': serie_id,
                                    'mediatype': 'video',
                                    'plot' : serie['plot'],
                                    })
        list_item.setArt({'thumb': serie['thumb'], 'icon': serie['thumb'], 'fanart': serie['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'false')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='list_seasons_in_serie', serie_id=serie_id, serie_name=serie_name, category_name=category_name)
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    pass

def list_seasons_in_serie(category_name:str, serie_name:str, serie_id:str):
    log("### list_season_in_serie")
    myclient=start_connection()
    data=get_myinfo(serie_id) # myclient.series_info_by_id(series_id)
    serie_info=data['info'] # a dict
    seasons=data['seasons'] # a list
    episodes=data['episodes'] # a dict
    season_name=serie_info['name'] 
    # not all season in seasons is provided, so check if season is in episodes.keys
    xbmcplugin.setPluginCategory(_HANDLE, serie_name+":"+category_name)
    xbmcplugin.setContent(_HANDLE, 'videos')
    """  
    infos: dict_keys(['name', 'title', 'year', 'cover', 'plot', 'cast', 'director', 'genre', 
     'release_date', 'releaseDate', 'last_modified', 'rating', 'rating_5based', 'backdrop_path', 
     'youtube_trailer', 'episode_run_time', 'category_id', 'category_ids'])
     season 1: dict_keys(['air_date', 'episode_count', 'id', 'name', 'overview', 'season_number', 
     'cover', 'cover_big'])
    """
    # Iterate through seasons.
    for season in seasons: # season is a dict
        episode_count=season['episode_count']
        season_number=season['season_number']
        season_name=season['name']
        if not str(season_number) in episodes.keys():
          log("Season "+str(season_number)+" is not available")
          continue
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=season_name)
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        # TODO: add number of episodes to season info?
        print(str(season_number)+":"+season_name+" ("+str(episode_count)+")")

        list_item.setInfo('video', {'title': season_name+" ("+str(episode_count)+")",
                                    'season' : season_number,
                                    'set': season['id'],
                                    'mediatype': 'video',
                                    'plot' : season['overview'],
                                    'genre' : serie_info['genre'],
                                    })
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': season['cover'], 'icon': season['cover'], 'fanart': season['cover_big']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'false')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='list_episodes_in_season', season_number=season_number, serie_name=serie_name, serie_id=serie_id)
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

    pass

def list_episodes_in_season(season_number:str, serie_name:str, serie_id:str):
    #TODO FIXME for right info
    log("### list_episodes_in_season")
    xbmcplugin.setPluginCategory(_HANDLE, serie_name+"/"+season_number)
    xbmcplugin.setContent(_HANDLE, 'episodes')
    data=get_myinfo(serie_id) # myclient.series_info_by_id(series_id)
    serie_info=data['info'] # a dict
    seasons=data['seasons'] # a list
    episodes=data['episodes'] # a dict
    """  
    infos: dict_keys(['name', 'title', 'year', 'cover', 'plot', 'cast', 'director', 'genre', 
     'release_date', 'releaseDate', 'last_modified', 'rating', 'rating_5based', 'backdrop_path', 
     'youtube_trailer', 'episode_run_time', 'category_id', 'category_ids'])
     season 1: dict_keys(['air_date', 'episode_count', 'id', 'name', 'overview', 'season_number', 
     'cover', 'cover_big'])
    """
    if not season_number in episodes.keys(): ##episodes[season_number]==None: # gives exception KeyError
      list_item = xbmcgui.ListItem(label=serie_name)
      list_item.setInfo('video', {'title': "N/A",
                                 })
      list_item.setProperty('IsPlayable', 'false')
      is_folder = False
#      url = get_url(action='list_seasons_in_serie', category_name, serie_name, serie_id)
      # Add our item to the Kodi virtual folder listing.
#      xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
      # Add a sort method for the virtual folder items (alphabetically, ignore articles)
      xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
      # Finish creating a virtual folder.
      xbmcplugin.endOfDirectory(_HANDLE)
      return 

    if episodes[season_number]==None:
      return 
    for video in episodes[season_number]:
        myplot=""
        try:
          myplot=video['info']['plot']
        except Exception:
          log("ERROR: Missing plot for video")
          log("video dict: "+str(video['info']))
          myplot=""
        
        extension=video['container_extension']
        direct_source=video['direct_source'] #+"."+extension
        episode_num=video['episode_num']        
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=serie_name)
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['title'],
                                    'set': season_number,
                                    'mediatype': 'video',
                                    'plot' : myplot,
                                    'video' : direct_source,
                                    })
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['info']['movie_image'], 'icon': video['info']['movie_image'], 'fanart': video['info']['cover_big']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=direct_source)
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    pass


def list_series_streams(season_name:str, serie_name:str, serie_id:str):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, serie_name+"/"+season_name)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'episodes')
    # Get the list of videos in the category.
    myclient=start_connection()
    data=get_myinfo(serie_id)

    videos = get_Series_by_category_list(myclient, category_name, category_id) # get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'set': video['series_id'],
                                    'mediatype': 'video',
                                    'plot' : video['plot'],
                                    })
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

