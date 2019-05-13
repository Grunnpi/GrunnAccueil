# To change this template, choose Tools | Templates
# and open the template in the editor.

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

__author__="Bob"
__date__ ="$01/01/14 16:41$"

import BP
import sys
# Déclarer le chemin d'accès aux modules Python supplémentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\") + 1]
sys.path.append(Path[:-1])
sys.path.append(Path + "PyMods")
sys.path.append(Path + "PyPack")
# Charger les modules standards de python non inclus dans BP
# Charger les modules spécifiques au plugin
from GUI import *


#-------------------------------------------------------------------------------
# section catégories
# récupérer les catégories et sous-catégories du fichier BP


no_categ =  "Sans catégorie"        # libellé en cas d'absence de catégorie
categ_ids = {no_categ:-1}           # retrouver l'id à partir du libellé
categ_names = {-1: no_categ}        # retrouver le libellé à partir de l'id
categ_all_ids = []                  # liste de tous les id's
categ_parent_ids = [-1]             # liste de tous les id's de catégories (à l'exclusion des sous-catégories)
parent_ids_list = []                # liste de tous les id's de catégories qui ont des sous-catégories rattachées
parent_list = []                    # liste de tous les libellés les catégories (à l'exclusion des sous-catégories)
categ_parents = {-1: -1}            # retrouver la catégorie 'parent' d'une sous-catégorie
categ_childs = {-1: []}             # trouver la liste de toutes les sous-catégories rattachées à une catégorie
categ_list = []                     # liste [(catégorie,[sous-catégories]), ...] contenant des libellés
CNames = []                         # liste des libellés de catégories et sous-catégories (les s/cat sont précédées de 4 blancs)
CPositions = {-1: -1}               # trouver la position d'un id dans la liste des catégories et sous-catégories gérée par BP
C_full_names = []                   # liste de libellés complets "cat>s/cat" dans l'ordre défini par BP

authorized_categs = {-1: -1}


# fournit le libellé complet d'une catégorie ou sous-catégorie pour affichage
def categ_display_name(id):
    if id in categ_parent_ids: return categ_names[id]
    else: return categ_names[categ_parents[id]] + ">" + categ_names[id]

for categ in BP.CategName:
    '''lecture des catégories'''
    index = int(categ.split("=")[0], 10)
    authorized_categs[index] = 1


categs = {-1: ("", "")}
current_parent = ""
for i, categ in enumerate(BP.CategName):
    p = categ.find("=")
    name = categ[p+1:]
    id = int(categ[:p], 10)
    if name.startswith(" "):
        name = name.strip()
        categs[id] = (current_parent, name)
    else:
        current_parent = name
        categs[id] = (name, "")


current_parent = -1
for i, categ in enumerate(BP.CategName):
    p = categ.find("=")
    name = categ[p + 1:]
    CNames.append(name)
    id = int(categ[:p], 10)
    CPositions[id] = i
    is_parent = not name.startswith(" ")
    if is_parent:
        current_parent = id
        categ_childs[id] = []
        categ_parent_ids.append(id)
        categ_ids[name]=id
    else:
        name = name.strip()
        categ_childs[current_parent].append(id)
        categ_ids[categ_names[current_parent]+">"+name]=id
    categ_parents[id] = current_parent
    categ_names[id] = name
    categ_all_ids.append(id)
categ_list = {}
categ_list["Sans catégorie"] = []
for i in range(len(categ_parent_ids)):
    parent_id = categ_parent_ids[i]
    parent_name = categ_names[parent_id]
    categ_list[parent_name]=[]
    for j in range(len(categ_childs[parent_id])):
        child_id = categ_childs[parent_id][j]
        child_name = categ_names[child_id]
        categ_list[parent_name].append(child_name)
categ_list = categ_list.items()
categ_list.sort()
parent_list = []
for i, c in enumerate(categ_list):
    parent_list.append(c[0])
    if c[1]!=[]: parent_ids_list.append(categ_ids[c[0]])
C_full_names = [categ_display_name(id) for id in categ_all_ids]


if __name__ == "__main__":
    print "Hello World"
