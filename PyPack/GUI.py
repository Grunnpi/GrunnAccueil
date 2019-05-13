
# coding = iso-8859-15
__author__ = "Rgs78"
__date__ ="$01/01/14 18:00$"


#==============================================================================#
# section Importation des modules Python                                                           #
#==============================================================================#

import BP
import imp
import sys
import time
# Déclarer le chemin d'accès aux modules Python supplémentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\") + 1]
sys.path.append(Path + "PyPack")
# Charger les modules standards de python non inclus dans BP
import os
import webbrowser
# Charger les modules spécifiques au plugin
#fDate = imp.load_source("", Path + "fDate.py")

application = 'Accueil'

#-------------------------------------------------------------------------------
# formulaire "préférences"
#-------------------------------------------------------------------------------

# Charge le fichier désigné par Path
def loadfile(path):
    f = open(path, "r")
    rec = f.read().split("\n")
    return rec

defaults={
    'Position':"poMainFormCenter",
    'FontStyle':[], 'FontSize':8, 'FontName':'Tahoma', 'FontColor':0x00000000,
    }

def make(CC,Type,Parent,**kwargs):
    if Type!='MyButton': o = CC(Type, Parent)
    else:
        o = CC('TButton', Parent)
        img = make(CC, 'TImage', o, Enabled=False, **kwargs)
        Width = kwargs.get('Width',1)
        Height = kwargs.get('Height',1)
        img.Left=(Width-img.Picture.Width)/2;img.Top=(Height-img.Picture.Height)/2
    o.Parent = Parent
    attr = dir(o)

    defs = [kw for kw in defaults if not kw in kwargs]
    for kw in defs:
        if 'Font'in kw and 'Font' in attr:
            o.Font.__setattr__(kw[4:],defaults[kw])
        if kw in attr :
            if   kw=='Picture' : o.Picture.LoadFromFile(defaults[kw])
            else: o.__setattr__(kw,defaults[kw])

    for kw in kwargs:
        if 'Font'in kw and 'Font' in attr:
            o.Font.__setattr__(kw[4:],kwargs[kw])
        if kw in attr :
            if   kw=='Picture' : o.Picture.LoadFromFile(kwargs[kw])
            else: o.__setattr__(kw,kwargs[kw])
    if "OnClick" in attr and o.OnClick != None: o.Cursor = -21
    return o

def Debug():
    for acc in range(BP.AccountCount()):
        l = ';'.join(BP.Operationthirdparty[acc])
        if ('debug '+ application).lower() in l.lower():
            for i in range(BP.OperationCount[acc]-1,-1,-1):
                if ('debug '+ application).lower() in BP.Operationthirdparty[acc][i].lower():
                    return True, BP.Operationthirdparty[acc][i]
    return False, ''

def trace(s=None):
    if s==None: BP.MsgBox('test',0)
    else: BP.MsgBox(repr(s),0)

# version de BP
def BP_version():
    f=open(BP.BankPerfectExePath()+'\\history.txt','r')
    ok = False
    while not ok:
        l=f.readline()
        n = l.find("Build")
        if n != -1:
            p=l[n:].find(']')
            v=l[n+6:n+p]
            ok = True
    return v


def goto_wiki(Sender):
    webbrowser.open("http://www.chelly.net/wiki/wiki/%s" % params['Name'])


