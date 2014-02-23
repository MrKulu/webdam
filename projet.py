# -*- coding: utf-8 -*-

from parse_channel import *
from motsclefs import *
import pickle



def mots_clefs_videos(videos,m,n):
    l = []
    lmots = []
    for v in videos:
        lmots.append(v.name.encode("utf8"))
        l.append(v.desc.encode("utf8"))
        #l.append(v.cat.encode("utf8"))
    llmots = mots_clefs(l,m)
    for l in llmots:
        for m in l:
            lmots.append(m)
    s = " ".join(lmots)
    return mots_clefs([s],n)

file = open("result_MrKuluW","r")
resultat_parse = pickle.load(file)
print('fichier chargé')
print(mots_clefs_videos(resultat_parse.playlists["watchHistory"],3,6))

