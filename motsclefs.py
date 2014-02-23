# -*- coding: utf-8 -*-

import math

separateurs = ".,;:/?!&\n\\\"\'()[]{}#-|"

mots_a_retirer = ['http','www','youtube','com']

mots_filtres = ['le','la','les','un','une','des','de','du','d','l','m','t','s','mais','ou','et','douc','or','ni','car','qui','que','quoi','dont','où','à','dans','par','pour','en','vers','avec','sans','sur','sous','entre','derrière','devant','en','je','tu','il','elle','nou','vous','ils','elles','son','sa','ses','mon','ma','mes','au','ton','ta','tes','notre','nos','votre','vos','leur','leurs','ai','as','a','avons','avez','ont','eu','suis','es','est','sommes','êtes','sont','été','plus','moins','moi','lui','toi','me','te','se','eux','and','by','http','https','www','com','youtube','to','of','the','for','you','on','in','it','is','with','this','my','from','your','are','if','how','org','can','out','one','will','that','user','video','watch','like','upload','was','but','now','have','our','there','some','all']

#mots : liste de chaines
def frequences_mots(mots):
    frequences = dict({})
    for mot in mots:
        if mot in frequences:
            frequences[mot] += 1
        else:
            frequences[mot] = 1
    try:
        i = frequences.iterkeys()
        while True:
            mot = i.next()
            frequences[mot] /= float(len(mots))
    except StopIteration:
        return frequences

#textes : liste de listes de chaines 
def tf(textes):
    resultat = []
    for texte in textes:
        resultat.append(frequences_mots(texte))
    return resultat

#table_frequences : dict chaine -> frequence
def idf(table_frequences):
    resultat = []
    occurrences = dict({})
    for frequences in table_frequences:
        for mot in frequences:
            try:
                occurrences[mot] += 1
            except KeyError:
                occurrences[mot] = 1
    for frequences in table_frequences:
        idfrequences = dict({})
        for mot in frequences:
            idfrequences[mot] = math.log((float(len(table_frequences))+1) / occurrences[mot])
        resultat.append(idfrequences)
    return resultat

#textes : listes de listes de chaines
def tfidf(textes):
    tfs = tf(textes)
    idfs = idf(tfs)
    resultat = []
    for i in xrange(len(textes)):
        tfidfs = dict({})
        for mot in tfs[i]:
            tfidfs[mot] = tfs[i][mot]*idfs[i][mot]
        resultat.append(tfidfs)
    return resultat
        
            
            
#texte : chaine
#chaines_a_retirer : liste de chaines
def simplifie(texte,chaines_a_retirer):
    texte2 = texte.lower()
    for x in separateurs:
        texte2 = texte2.replace(x,' ')
    for x in chaines_a_retirer:
        texte2 = texte2.replace(x,' ')
    for x in mots_a_retirer:
        texte2 = texte2.replace(x,' ')
    return texte2

#texte : chaine
def groupe_mots(texte,n):
    mots = texte.split()
    mots2 = []
    mots_recents = ["" for i in range(n)]
    if n<=0:
        return []
    for mot in mots:
        del mots_recents[0]
        mots_recents.append(mot)
        if mots_recents[0] != "":
            groupe = " ".join(mots_recents)
            if groupe not in mots_filtres and len(groupe)>1:
                mots2.append(groupe)
    return mots2
                

#texte : chaine
#chaines_a_retirer : liste de chaines
def preparation(texte,chaines_a_retirer,n):
    texte2 = simplifie(texte,chaines_a_retirer)
    return groupe_mots(texte2,n)


#tfidfs : liste de dict chaine -> coeff
def mots_frequents(tfidfs,n,seuil):
    resultat = []
    for poids in tfidfs:
        mots = poids.items()
        mots.sort(lambda x,y:cmp(x[1],y[1]),None,True)
        resultat_partiel = []
        i = 0
        if seuil:
            while i<len(mots) and mots[i][1]>=n:
                resultat_partiel.append(mots[i][0])
                i += 1
        else:
            while i<len(mots) and len(resultat_partiel)<n:
                p= mots[i][1]
                while i<len(mots) and mots[i][1] == p:
                    resultat_partiel.append(mots[i][0])
                    i += 1
        resultat.append(resultat_partiel)
    return resultat


#textes : liste de listes de chaines
def mots_clefs(textes,n,seuil):
    tfs = []
    if len(textes)==1:
        tfs = tf(textes)
    else:
        tfs = tfidf(textes)
    return mots_frequents(tfs,n,seuil)

