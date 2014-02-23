# -*- coding: utf-8 -*-

import math

separateurs = ".,;:/?!&\n\\\"\'()[]{}#-"

mots_filtres = ['le','la','les','un','une','des','de','du','d','l','m','t','s','mais','ou','et','douc','or','ni','car','qui','que','quoi','dont','où','à','dans','par','pour','en','vers','avec','sans','sur','sous','entre','derrière','devant','en','je','tu','il','elle','nou','vous','ils','elles','son','sa','ses','mon','ma','mes','au','ton','ta','tes','notre','nos','votre','vos','leur','leurs','ai','as','a','avons','avez','ont','eu','suis','es','est','sommes','êtes','sont','été','plus','moins','moi','lui','toi','me','te','se','eux']

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

def tf(textes):
    resultat = []
    for texte in textes:
        resultat.append(frequences_mots(simplifie(texte)))
    return resultat


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
        
            
            

def simplifie(texte):
    texte2 = texte.lower()
    for x in separateurs:
        texte2 = texte2.replace(x,' ')
    mots = texte2.split()
    mots2 = []
    for mot in mots:
        if mot not in mots_filtres:
            mots2.append(mot)
    return mots2

def mots_frequents(tfidfs,n):
    resultat = []
    for poids in tfidfs:
        mots = poids.items()
        mots.sort(lambda x,y:cmp(x[1],y[1]),None,True)
        resultat_partiel = []
        i=0
        while i<len(mots) and len(resultat_partiel)<n:
            p= mots[i][1]
            while i<len(mots) and mots[i][1] == p:
                resultat_partiel.append(mots[i][0])
                i += 1
        resultat.append(resultat_partiel)
    return resultat


def mots_clefs(textes,n):
    tfidfs = tfidf(textes)
    return mots_frequents(tfidfs,n)
