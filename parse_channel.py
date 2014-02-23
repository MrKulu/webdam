# -*- coding: utf-8 -*-
#!/usr/bin/python

import httplib2
import os
import sys
import pickle

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


class Video:
  """YouTube video"""
  def __init__(self,name,video_id,description,uploader,category):
    self.name = name
    self.id = video_id
    self.desc = description
    self.cat = category
    self.upload = uploader

class Channel:
  """Youtube channel"""
  def __init__(self,name,description,video_list):
    self.name = name
    self.desc = description
    self.videos = video_list

class Result_parse:
  """The results of the fonction parse_channel"""
  def __init__(self):
    self.playlists = {}
    self.uploads = []
    self.subs = []

def parse_channel():
  
  res = Result_parse()

  PRIVATE_PLAYLISTS = ["likes","favorites","watchHistory"]

  for i in PRIVATE_PLAYLISTS:
    res.playlists[i] = []

  categories = {}

  CLIENT_SECRETS_FILE = "client_secret.json"
  YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"
  
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                 scope=YOUTUBE_READONLY_SCOPE)
  
  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()
  
  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)
    
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  http=credentials.authorize(httplib2.Http()))
  
  def category(cat_id):
    if cat_id not in categories.keys():
      tmp = youtube.videoCategories().list(
        part="snippet",
        id=cat_id).execute()["items"]
      if len(tmp) == 0:
        categories[cat_id] = cat_id
      else:
        categories[cat_id] = tmp[0]["snippet"]["title"]
    return categories[cat_id]
  # End Def category

  def videosInPlaylist(playlist_id):
    videos = []
    next_page_token = ""
    while next_page_token is not None:
      playlistitems_response = youtube.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=50,
        pageToken=next_page_token
        ).execute()
      
      for playlist_item in playlistitems_response["items"]:
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        video_response = youtube.videos().list(
          part="snippet",
          id=video_id
          ).execute()
        if len(video_response["items"]) == 0:
          break
        videos += [Video(
            video_response["items"][0]["snippet"]["title"],
            video_id,
            video_response["items"][0]["snippet"]["description"],
            video_response["items"][0]["snippet"]["channelTitle"],
            category(video_response["items"][0]["snippet"]["categoryId"]))]
  
      next_page_token = playlistitems_response.get("nextPageToken")
    print playlistitems_response["pageInfo"]["totalResults"]
    return videos
  # End Def videosInPlaylist


  channels_response = youtube.channels().list(
    mine=True,
    part="contentDetails"
    ).execute()

  # Parcours des playlists privées
  for play in PRIVATE_PLAYLISTS:
    for channel in channels_response["items"]:
      list_id = channel["contentDetails"]["relatedPlaylists"][play]
      print "Videos in list", play
      res.playlists[play] = videosInPlaylist(list_id)
  
  # Parcours des vidéos uploadées
  for channel in channels_response["items"]:
    uploads_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    print "Videos uploaded"
    res.uploads = videosInPlaylist(uploads_id)

  # Parcours des abonnements
  next_page = ""
  while next_page is not None:
    subscriptions = youtube.subscriptions().list(
      part="snippet",
      mine=True,
      pageToken=next_page,
      maxResults=50).execute()
  
    for channel in subscriptions["items"]:
      channelId = channel["snippet"]["resourceId"]["channelId"]
      channel_content = youtube.channels().list(
        part="contentDetails",
        id=channelId).execute()["items"]
      if len(channel_content) > 0:
        res.subs += [Channel(
            channel["snippet"]["title"],
            channel["snippet"]["description"],
            videosInPlaylist(channel_content[0]["contentDetails"]["relatedPlaylists"]["uploads"]))]
      
    next_page = subscriptions.get("nextPageToken")
  

  store = open("result","w")
  pickle.dump(res,store)
  store.close()
  return res
          
#parse_channel()
