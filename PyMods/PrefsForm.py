# To change this template, choose Tools | Templates
# and open the template in the editor.

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

__author__="Bob"
__date__ ="$1 janv. 2014 16:43:19$"

import BP
import time
from GUI import *
from fDate import *
import cPickle


def get_params(IniFile = Path + "%s.ini"%application):
#    if inifile == None : IniFile = Path + "%s.ini"%application      # par défaut, on récupère les paramètres du ficier .ini de l'application
#    else : IniFile = inifile                                        # mais on peut en récupérer un autre si on le précise

    # récupération des paramètres du fichier .ini (applicables à la 1ère utilisation du plugin sur ce fichier de comptes)
    today = time.localtime()[:3]
    params = {'position':[],'memo':True,'operations':True,'rappels':True,'sf_view':False,'sf_date':(today[0],12,31),'switches':[1,0,0,0],'groups':[-1,-1,-1,-1],'text':'','lists':{}}
    f=loadfile(IniFile)
    for line in f:
        if line.find("=") != -1:
            key = line.split("=")[0]
            val = "".join(line.split("=")[1:]).strip()
            params[key] = val
            if val in ['False', 'True'] or val.isdigit(): # or str_to_float(val)!=0
                params[key] = eval(val)

    # récupération des paramètres spécifiques du fichier de comptes (applicables dès la 2ème utilisation du plugin sur ce fichier de comptes)
    params2 = {}
    # --- --- --- cette section des paramètres est spécifique au plugin "Accueil" --- --- ---
    prefs = BP.GetURL("load_script_data:RgsParams")
    if prefs != '':
        prefs = cPickle.loads(prefs)    
        #----------------------------------------------------------------------------------------------------------------#
        # cette section est à adapter pour chaque plugin                                                                 #
        script, keys = "Accueil", ['position','memo','operations','rappels','sf_view','sf_date','switches','groups','text']
        ''' 
            'position':[558, 290, 500, 324] : position de la fenêtre à la fermeture de la session précédente
          } '''
        #----------------------------------------------------------------------------------------------------------------#
        if script in prefs:
            for key in keys: 
                if key in prefs[script]: params[key]=prefs[script][key]

        #----------------------------------------------------------------------------------------------------------------#
        # cette section est à adapter pour chaque plugin                                                                 #
        script, keys = "groupes_comptes", ['lists']
        ''' {'liste1':[[Uid1,Uid2, ...],"logo1"], 'liste2':[[Uidn, ...],"logo2"],  ...} '''
        #----------------------------------------------------------------------------------------------------------------#
        if script in prefs:
            for key in keys:
                if key in prefs[script]: params[key]=prefs[script][key]
       
    for key in params2:                 # on remplace les paramètres lus dans le fichier .ini (options par défaut)
        params[key]=params2[key]        # par les paramètres lus dans la fichier de comptes (si on en a trouvé = options spécifiques du fichier de comptes)

    return params


def set_params(params):
    # mise à jour du fichier .ini   # afin que les options soient dipsonibles pour des fichiers de coptes avec lesquels on n'a jamais utilisé le plugin
    IniFile = Path + "%s.ini"%application
    file=open(IniFile,"r")
    lines = file.readlines()
    for i, line in enumerate(lines):
        if '=' in line:
            key = line.split("=")[0]
            if key=='ExecuteWithFile':
                lines[i] = '%s=%s\n' % (key, params[key])
            if key=='position':
                lines[i] = '%s=%s\n' % (key, params[key])
            if key=='memo':
                lines[i] = '%s=%s\n' % (key, params[key])
            if key=='operations':
                lines[i] = '%s=%s\n' % (key, params[key])
            if key=='rappel':
                lines[i] = '%s=%s\n' % (key, params[key])
    file=open(IniFile,"w")
    file.writelines(lines)
    file.close()
    
    # mise à jour des paramètres au sein du fichier de comptes
    # --- --- --- cette section des paramètres est spécifique au plugin "Accueil" --- --- ---
    prefs = BP.GetURL("load_script_data:RgsParams")
    if prefs != '': prefs = cPickle.loads(prefs) 
    else : prefs={}
    #----------------------------------------------------------------------------------------------------------------#
    # cette ligne est à adapter pour chaque plugin                                                                   #
    script, keys = "Accueil", ['position','memo','operations','rappels','sf_view','sf_date','switches','groups','text']
    #----------------------------------------------------------------------------------------------------------------#
    if not script in prefs : prefs[script]={}
    for key in keys: prefs[script][key]=params[key]    

    #----------------------------------------------------------------------------------------------------------------#
    # cette ligne est à adapter pour chaque plugin                                                                   #
    script, keys = "groupes_comptes", ['lists']
    #----------------------------------------------------------------------------------------------------------------#
    if not script in prefs : prefs[script]={}
    for key in keys: prefs[script][key]=params[key]

    s = cPickle.dumps(prefs)
    BP.GetURL("save_script_data:RgsParams:" + s)
    
    params = get_params()
    P.ModalResult = 1
    return params



def pref(CreateComponent, app):
    global P, Pr1, Pr2, application
    application = app
    CC = CreateComponent

    def pExit(Sender):
        P.ModalResult = 2
        return

    def init_controls(Sender=None):
        params = get_params()
        spl.Checked = params['ExecuteWithFile'] == 1

    def save_params(Sender):
        set_params(params)
        P.ModalResult = 1

    def browse(Sender):
        Path = BP.OpenDialog("Choisissez le fichier image", "", "*.png", "fichier image(*.png)|*.png")
        if Path != '':
            Sender.Picture.LoadFromFile(Path)
            name = Path.split('\\')[-1]
            dst = '\\'.join(BP.BankPerfectExePath().split('\\')[:-1])+'\\icons'
            shutil.copyfile(Path,'%s/%s.png'%(dst,params[Sender.name][0]))

    def default(Sender):
        src = ('\\'.join(BP.BankPerfectPluginPath().split('\\')[:-1])+'\\icons\\icons')[1:]
        dst = '\\'.join(BP.BankPerfectExePath().split('\\')[:-1])+'\\icons'
        if not os.path.isdir(dst): os.mkdir(dst)
        # recopier les fichiers du répertoire source vers le répertoire icons de BP
        names = os.listdir(src)
        for name in names :
            shutil.copyfile('%s/%s'%(src,name),'%s/%s'%(dst,name))
        for i,P in enumerate(Pi):
            P.Picture.LoadFromFile(dst + "\\%s.png" % i_file[i])


    def message_prive(sSender):
        webbrowser.open("http://www.chelly.net/phpbb/ucp.php?i=pm&mode=compose&u=9774")

    def donate(Sender):
        webbrowser.open("https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=36E2ATWEW5ZAA ")


    def toggle_spl(Sender):
        if spl.Checked : params['ExecuteWithFile'] = 1
        else : params['ExecuteWithFile'] = 0

    L = 300
    H = 330  #+len(i_code)*20
    P = make(CC, "TForm", None, Caption = None, Width=L, Height=H, OnActivate=init_controls)
    PTitre = make(CC, "TLabel", P, Left=20, Top=15, Caption="Accueil ", FontStyle=["fsBold","fsItalic"], FontSize = 12)
    make(CC, "TBevel",P,Top = PTitre.Top+30, Left = 2,Height = 2,Width = L-20)
    PT2 = make(CC, "TLabel", P, Left=10, Top=PTitre.Top+40, Caption="Paramètres :", FontStyle = ["fsBold"], FontSize = 10)
    # groupe 'Intégration à BP -----------------------------------------------------
    # groupe 'préférences' ---------------------------------------------------------
    Pg2 = make(CC, "TGroupBox", P, Caption="Préférences", Left=10, Top=PT2.Top+20, Width=L-40, Height=70, FontStyle = ["fsItalic"])
    spl = make(CC,"TCheckBox", Pg2, Left=10, Top=20, Width = 150, Caption = "Afficher à l'ouverture ? (*)", OnClick = toggle_spl)
    make(CC, "TLabel", P, Left=10, Top=Pg2.Top+Pg2.Height, Caption="(*) après redémarrage de BP ", FontStyle = ["fsItalic"], FontSize = 8, FontColor = 0x00808080)
    # boutons ----------------------------------------------------------------------
#    PKO = make(CC, "TImage", P, Left = L-100, Top = Pg2.Top+Pg2.Height+10, Width=30, Height=30, OnClick= pExit, Picture = Path + "icons\\KO2.png")
    POK = make(CC, "TImage", P, Left = L-60, Top = Pg2.Top+Pg2.Height+10, Width=30, Height=30, OnClick=save_params, Picture = Path + "\\icons\\OK2.png")
    # signature --------------------------------------------------------------------
    make(CC, "TBevel",P,Top = POK.Top+POK.Height+10, Left = 2,Height = 2,Width = L-20)
    Pimage = make(CC, "TImage", P, Left = L-75, Top = POK.Top+POK.Height+55, Width=60, Height=60, Anchors=["akRight"],OnClick=message_prive, Picture = Path + "\\icons\\rgs78.png")
    PRgs78 = make(CC, "TLabel",P, Caption = "Rgs78", Left=L-65,Top=H-60,FontStyle=["fsBold"], FontColor = 0x00008800)
    PLZ = make(CC, "TLabel", P, Left=20, Top=Pimage.Top+Pimage.Height/2-55, Caption="Vous pouvez remonter des bugs ou\ndemander des évolutions ici        =>")
    Pdonate = make(CC, "TImage", P, Left = 70, Top = H-70, Width=71, Height=20,OnClick=donate, Picture = Path + "\\icons\\donate.png")
    # \params_panel
    #-------------------------------------------------------------------------------
    #Pref = make("TImage", ff_panel, Left = margin, Top = ff.Height-32-3, Width=32, Height=32, Anchors=["akLeft", "akBottom"], OnClick=ParamsCall, Picture=Path + "icons\\preferences.png")
    #-------------------------------------------------------------------------------
    params = get_params()
    return P, params

if __name__ == "__main__":
    print "Hello World"
