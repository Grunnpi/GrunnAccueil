# To change this template, choose Tools | Templates
# and open the template in the editor.

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

__author__="Bob"
__date__ ="$01/01/14 16:41$"

import BP
import sys
# D�clarer le chemin d'acc�s aux modules Python suppl�mentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\") + 1]
sys.path.append(Path[:-1])
sys.path.append(Path + "PyMods")
sys.path.append(Path + "PyPack")
# Charger les modules standards de python non inclus dans BP
# Charger les modules sp�cifiques au plugin
from GUI import *


#-------------------------------------------------------------------------------
# section cat�gories
# r�cup�rer les cat�gories et sous-cat�gories du fichier BP


no_categ =  "Sans cat�gorie"        # libell� en cas d'absence de cat�gorie
categ_ids = {no_categ:-1}           # retrouver l'id � partir du libell�
categ_names = {-1: no_categ}        # retrouver le libell� � partir de l'id
categ_all_ids = []                  # liste de tous les id's
categ_parent_ids = [-1]             # liste de tous les id's de cat�gories (� l'exclusion des sous-cat�gories)
parent_ids_list = []                # liste de tous les id's de cat�gories qui ont des sous-cat�gories rattach�es
parent_list = []                    # liste de tous les libell�s les cat�gories (� l'exclusion des sous-cat�gories)
categ_parents = {-1: -1}            # retrouver la cat�gorie 'parent' d'une sous-cat�gorie
categ_childs = {-1: []}             # trouver la liste de toutes les sous-cat�gories rattach�es � une cat�gorie
categ_list = []                     # liste [(cat�gorie,[sous-cat�gories]), ...] contenant des libell�s
CNames = []                         # liste des libell�s de cat�gories et sous-cat�gories (les s/cat sont pr�c�d�es de 4 blancs)
CPositions = {-1: -1}               # trouver la position d'un id dans la liste des cat�gories et sous-cat�gories g�r�e par BP
C_full_names = []                   # liste de libell�s complets "cat>s/cat" dans l'ordre d�fini par BP

authorized_categs = {-1: -1}


# fournit le libell� complet d'une cat�gorie ou sous-cat�gorie pour affichage
def categ_display_name(id):
    if id in categ_parent_ids: return categ_names[id]
    else: return categ_names[categ_parents[id]] + ">" + categ_names[id]

for categ in BP.CategName:
    '''lecture des cat�gories'''
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
categ_list["Sans cat�gorie"] = []
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
