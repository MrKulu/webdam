# -*- coding: utf-8 -*-

from parse_channel import *
from motsclefs import *
import pickle


#videos : liste de videos
#taille_groupe : taille des groupes de mots clefs voulus
#n : nombre de groupes de mots clefs choisis par vidéo, parmis lesquels la sélection sera faite
#p : nombre min de groupes de mots clefs voulus
def mots_clefs_videos(videos,taille_groupes,n,p):
    descriptions = []
    mots = []
    for v in videos:
        name = preparation(v.name.encode("utf8"),[],taille_groupes)
        mots.extend(name)
        desc = preparation(v.desc.encode("utf8"),[],taille_groupes)
        descriptions.append(desc)
    mots_clefs_descriptions = mots_clefs(descriptions,n)
    for l in mots_clefs_descriptions:
        for m in l:
            mots.append(m)
    return mots_clefs([mots],p)

file = open("result_MrKuluW","r")
resultat_parse = pickle.load(file)
print('fichier chargé')
print(mots_clefs_videos(resultat_parse.playlists["watchHistory"],3,3,6))

