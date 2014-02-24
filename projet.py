# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from parse_channel import *
from motsclefs import *
import pickle


#videos : liste de videos
#taille_groupe : taille des groupes de mots clefs voulus
#n : nombre de groupes de mots clefs choisis par vidéo, parmis lesquels la sélection sera faite
#p : nombre min de groupes de mots clefs voulus
def mots_clefs_videos(videos,taille_groupes,n,p,resultats):
    descriptions = []
    mots = []
    for v in videos:
        name = preparation(v.name,resultats,taille_groupes)
        mots.extend(name)
        desc = preparation(v.desc,resultats,taille_groupes)
        descriptions.append(desc)
    mots_clefs_descriptions = mots_clefs_multiple(descriptions,n)
    for l in mots_clefs_descriptions:
        for m in l:
            mots.append(m)
    if taille_groupes == 1:
        return resultats+mots_clefs(mots,p,False)
    else:
        return mots_clefs_videos(videos,taille_groupes - 1,n,p,resultats+mots_clefs(mots,p,True))

if len(sys.argv) > 1:
    pp = int(sys.argv[1])
else:
    pp = 5

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    print "Begin parse_channel..."
    parse_channel()
    filename = "result"

file = open(filename,"r")
resultat_parse = pickle.load(file)
print('fichier chargé')
print " ; ".join(mots_clefs_videos(resultat_parse.playlists["watchHistory"],3,4,pp,[]))
print " ; ".join(mots_clefs_videos(resultat_parse.playlists["likes"],3,4,pp,[]))
print " ; ".join(mots_clefs_videos(resultat_parse.playlists["favorites"],3,4,pp,[]))

r = []
for i in resultat_parse.subs:
    r += [Video("",""," ".join(mots_clefs_videos(i.videos,3,4,pp,[])),"","")]
print " ; ".join(mots_clefs_videos(r,3,4,pp,[]))

print entropie_vids(resultat_parse.playlists["watchHistory"])
print entropie_vids(resultat_parse.playlists["likes"])
print entropie_vids(resultat_parse.playlists["favorites"])
print entropie_vids(r)
