#!/usr/bin/python
# coding=iso-8859-1
# 
# Charger les modules standards de python inclus dans BP
import BP
import sys
import cPickle
# Déclarer le chemin d'accès aux modules Python supplémentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\")+1]
sys.path.append(Path + "PyPack")
sys.path.append(Path + "PyMods")
# Charger les modules standards de python non inclus dans BP
import os
# Charger les modules spécifiques au plugin
from GUI import *               # fontions générales de création de l'interface utilisateur
from PrefsForm import *         # formulaire des préférences
from fDate import *             # fonctions relatives aux dates
from fNum import *              # fonctions relatives aux nombres
from fCategs import *           # fonctions relatives qux catégories
from AccountsListsForm import * # formulaire de gestion des groupes de comptes

# lecture des paramètres du fihier .ini
CC = CreateComponent
P, params = pref(CC, 'Accueil')
version = params['version']

# constantes
index_Logo = 0
index_Compte = 1
index_Rapproche = 2
index_Pointe = 3
index_Aujourdhui = 4
index_Complet = 5

index_Rapproche_total = 0
index_Pointe_total = 1
index_Aujourdhui_total = 2
index_Complet_total = 3

#-------------------------------------------------------------------------------
#Constantes & variables
#-------------------------------------------------------------------------------
today = time.localtime()[:3]


d_end_of_2019 = time.gmtime( 1577833199 )
d_end_of_2018 = time.gmtime( 1546297199 )
d_end_of_2017 = time.gmtime( 1514764799 )
d_end_of_2016 = time.gmtime( 1483228799 )
d_end_of_2015 = time.gmtime( 1451606399 )

d_end_of_col1 = d_end_of_2017
d_end_of_col2 = d_end_of_2018
d_end_of_col3 = d_end_of_2019

np=1
ID_YES = 6
s_names=['S0_off.png','S1_on.png','S2_off.png','S3_off.png']
margin = 15
values=[]
Logos=[]
records={}
prefs = []
tiers=[]
prev=[]
todo=[]
lists={}
lists_logos={}
klist=[]
Sw={}
grid_C={}
bm_list_C={}
logo_C={}
data = {}
headers_O = ["Date","Compte","Montant"]
headers_R = ["Date","Mode","Montant"]
group_logo = Path + "groups\\_pas de logo_.png"
no_logo = group_logo
#-------------------------------------------------------------------------------
# section comptes
#Liste des comptes triés selon les réglages manuels de l'utilisateur
display_accounts = BPEval("get_accounts").split(";")
#Dictionnaire qui renvoie l'index réel d'un compte en fonction de sa position dans la liste classée
real_accounts = {}  # {position: N°BP, ...}
real_index = {}     # {nom du compte: position, ...}
display_index = {}  # {n°BP: position}
for i, name in enumerate(display_accounts):
    p = name.find("=")
    if p == -1: continue
    index = int(name[:p], 10)
    name = name[p+1:]
    display_accounts[i] = name
    display_index[index] = i
    real_accounts[i] = index
    real_index[name] = index

## chargement des paramètres
#def load_PrefAccounts(Sender=None):
#    global prefs, lists, klist, lists_logos
#    #récupération de la dernière sélection de comptes (version < 3.0)
#    prefs = BP.GetURL("load_script_data:RgsAccueilPref")
#    if prefs != '':
#        prefs = cPickle.loads(prefs)
#        try: df.Date = to_delphi_date(prefs[1]) # date du solde futur
#        except: df.Date = to_delphi_date(today)
#        try: sf.Checked = prefs[0]              # affichage du solde futur ?
#        except: sf.Checked = True
#        try: lists = prefs[2]                   # groupes de comptes
#        except: lists = {}
#        try: Switches = prefs[3]                # grilles à afficher
#        except: Switches = [0,0,0,0]
#        try: Lists = prefs[4]                   # associations grilles/groupes
#        except: Lists = [-1,-1,-1,-1]
#        try: memo.Lines.Text = prefs[6]         # mémo
#        except:memo.Lines.Text = ''
#        try: lists_logos = prefs[7]             # logos des groupes de comptes
#        except:lists_logos = {}
#        BP.GetURL("save_script_data:RgsAccueilPref:") # effacement de cette version des paramètres
#        # prévention des erreurs si les fichiers logos sont absents
#        for name in lists_logos:
#            if not os.path.isfile(lists_logos[name]): lists_logos[name]=no_logo
#        # mise au format v3.0
#        for key in lists:
#            lists[key]=[lists[key],lists_logos[key]]
#        del lists_logos
#
#        ''' {'liste1':[[Uid1,Uid2, ...],"logo1"], 'liste2':[[Uidn, ...],"logo2"],  ...} '''
#
#
#    for key in ['position','memo','operations','rappels','sf_view','sf_date','switches','groups','text']:
#        if key in params:pass
#    if 'sf_date' in params : df.Date = to_delphi_date(params['sf_date'])
#    if 'sf_view' in params : sf.Checked = params['sf_view']
#    if 'switches' in params : Switches = params['switches']
#    if 'text' in params : memo.Lines.Text = params['text']
#    if 'groups' in params : Lists = params['groups']
#    if 'lists' in params : lists = params['lists']
#
#    if not isinstance(lists,dict): lists={} # cas où aucun groupe de comptes n'est défini
#    klist = lists.keys()
#    klist.sort()
#    for i in range(4):
#        bm_list_C[i].Items.Text = '\n'.join(klist)
#        bm_list_C[i].ItemIndex = Lists[i]
#        if Switches[i] and Lists[i]!=-1:
#            Sw[i][0] = len(lists[bm_list_C[i].Items[Lists[i]]])
#            Sw[i][1].Picture.LoadFromFile(Path + "icons\\C_on.png")
#        else:
#            Sw[i][0] = 0
#            Sw[i][1].Picture.LoadFromFile(Path + "icons\\C_off.png")
#
#
#
##  sauvegarde des paramètres
#def save_PrefAccounts(Sender=None):
#    # préparation
#    params['sf_view']=sf.Checked                                            # solde futur
#    params['sf_date']=from_delphi_date(df.Date)                             # date du solde futur
#    Switches = Sw.items(); Switches.sort()
#    params['switches']=[sw[1][0] for sw in Switches]                         # grilles à afficher
#    Lists = bm_list_C.items(); Lists.sort()
#    params['groups']=[l[1].ItemIndex for l in Lists]                        # associations grilles/groupes
#    params['text']=memo.Lines.Text                                          # mémo
#    params['lists']=lists                                                   # groupes de comptes
##    # enregistrement
##    s = cPickle.dumps(s)
##    BP.GetURL("save_script_data:RgsAccueilData:" + s)



#-------------------------------------------------------------------------------
# section spécifique


# charger l'échéancier
def load_echeancier():
    try:
        s = BP.GetURL("load_script_data:fabiobpscheduler")
        if s != "": return cPickle.loads(s)
    except:
        pass
    return []

# charger les opérations de tous les comptes
def load_values():
    values = []
    for position, account_name in enumerate(display_accounts):
        i = real_accounts[position]
        accs = [account_name]*BP.OperationCount[i]
        categs = [categ_names[c] for c in BP.OperationCateg[i]]
        amounts = BP.OperationAmount[i]
        marks = BP.OperationMark[i]
        dates = BP.OperationDate[i]
        dates = [str_to_tup(d) for d in dates]
        values += zip(accs, amounts, dates, marks, categs)
    return values

# fait le total des échéances à venir jusqu'à la date 'Until'
def apply_record(Rec, Until):
    v = 0
    modif = True
    End, n = Rec["enddate"], Rec["nextdate"]
    #Si l'échéance se termine plus tôt que la date de fin, on décale d'autant la date de fin
    if End != (0, 0, 0) and End < Until: Until = End
    while n <= Until:
        if "modif" in Rec.keys():
            if Rec["modif"]!=0 and modif:
                montant, modif = Rec["modif"]*abs(Rec["montant"])/Rec["montant"],False
            else:
                montant = Rec["montant"]
        else:
            montant = Rec["montant"]
        v += montant
        n = add_to_date(n, Rec["delta"], Rec["deltaunit"])
    return v

# initialisation des tableaux pour les grilles de comptes
def init_data():
    ''' création de la structure de données'''
    global data
    dummy = Path + "Thumbs\\Dummy.png"
    for i in range(4):
        data[i]=[]
        for k in range(len(display_accounts)+1):
            data[i].append([make(CC, "TImage", grid_C[i], Width=100, Height=25, Enabled=False, Picture = dummy),'','','','','',''])
            data[i][k][0].visible = True


# mise à jour après modification des choix
def update(S=None,P=None):
    global data, headers, prev, todo, selected_accounts
    # mise à jour des en-têtes de colonnes
    headers = ["Logos","Comptes","Fin 2017","Fin 2018","Fin 2019","Aujourd'hui"]
    date_f=from_delphi_date(df.Date)
    headers.append(date_to_str(date_f))
    # préparation des constantes et variables
    selected_accounts = []
    for i in range(4):
        if Sw[i][0]:
            grid_C[i].ColCount = 6 + sf.Checked
            if bm_list_C[i].ItemIndex!=-1 :
                for UId in lists[bm_list_C[i].Items[bm_list_C[i].ItemIndex]][0]:
                    selected_accounts.append(UId)
                    selected_accounts.append(int(BP.GetURL("get_account_id_from_uid:%s" % UId)))
    prev = [v for v in values if v[2]>=today and real_index[v[0]] in selected_accounts]
    todo = []
    for Rec in records:
        if Rec["account"] in selected_accounts:
            if isinstance(Rec["account"],str): acc = int(BP.GetURL("get_account_id_from_uid:%s" % Rec["account"]))
            else : acc = Rec["account"]
            acc = display_accounts[display_index[acc]]
            if Rec.get("action","insert")=="insert":
                if Rec["enddate"] == (0, 0, 0) or today<=Rec["enddate"]:
                    prev.append((acc, Rec["montant"], Rec["nextdate"], 0, categ_names[Rec["categ"]])) #accs, amounts, dates, marks
                    transfert = Rec.get("transfer",-1)
                    if transfert != -1 :
                        if transfert in selected_accounts :
                            if isinstance(transfert,str): acc = int(BP.GetURL("get_account_id_from_uid:%s" % transfert))
                            else : acc = transfert
                            acc=display_accounts[display_index[acc]]
                            prev.append((acc, -1*Rec["montant"], Rec["nextdate"], 0, categ_names[Rec["categ"]])) #accs, amounts, dates, marks
            else:
                todo.append((BP.OperationGetNameFromModeIndex(Rec["mode"]), Rec["montant"], Rec["nextdate"], Rec["tiers"], categ_names[Rec["categ"]], acc)) #accs, amounts, dates, marks
    # --- trier les opérations planifiées par dates
    tmp = [(p[2],p) for p in prev]
    tmp.sort()
    prev = [t[1] for t in tmp]
    # --- trier les rappels par dates
    tmp = [(p[2],p) for p in todo]
    tmp.sort()
    todo = [t[1] for t in tmp]
    # mise à jour des soldes de comptes
    for i in range(4):
        idx=Sw[i][0]
        if Sw[i][0]:
            total = [0,0,0,0,0]
            selected_accounts = []

            if bm_list_C[i].ItemIndex!=-1 :
                name = bm_list_C[i].Items[bm_list_C[i].ItemIndex]
#                logo = lists_logos.get(name,Path + "groups\\_pas de logo_.png")
                logo = lists.get(name,Path + "groups\\_pas de logo_.png")[1]
                logo_C[i].Picture.LoadFromFile(logo)
                for UId in lists[name][0]:
                    selected_accounts.append(UId)
                    selected_accounts.append(int(BP.GetURL("get_account_id_from_uid:%s" % UId)))
                idx=0
                for t,compte in enumerate(display_accounts):
                    if real_accounts[t] in selected_accounts:
                        logo = BP.AccountBankLogo [real_accounts[t]]
                        file = logo.split('\\')[-1:][0]
                        logo =  Path + "Thumbs\\%s" % file

                        # choix du LOGO
                        if os.path.isfile(logo):
                            data[i][idx][index_Logo].Picture.LoadFromFile(logo)
                        else :
                            data[i][idx][index_Logo].Picture.LoadFromFile(Path + "Thumbs\\dummy.png")

                        # choix du nom du compte
                        data[i][idx][index_Compte] = compte

                        # total colonne Rapproche : cible d_end_of_col1
                        v = sum([amount for acc, amount, date, mark, categ in values if (date<=d_end_of_col1 and acc==compte)])
                        data[i][idx][index_Rapproche] = fmt_float(v);
                        total[index_Rapproche_total]+=v

                        # total colonne Pointe : cible d_end_of_col2
                        v = sum([amount for acc, amount, date, mark, categ in values if (date<=d_end_of_col2 and acc==compte)])
                        data[i][idx][index_Pointe] = fmt_float(v);
                        total[index_Pointe_total]+=v

                        # total colonne Aujourd'hui : : cible d_end_of_col3
                        v = sum([amount for acc, amount, date, mark, categ in values if (date<=d_end_of_col3 and acc==compte)])
                        data[i][idx][index_Aujourdhui] = fmt_float(v);
                        total[index_Aujourdhui_total]+=v

                        # total colonne Complet
                        v = sum([amount for acc, amount, date, mark, categ in values if (date<=today and acc==compte)])
                        data[i][idx][index_Complet] = fmt_float(v);
                        total[index_Complet_total]+=v

                        #On parcoure la liste des échéances et on garde celles qui concernent le compte courant
                        v = sum([amount for acc, amount, date, mark, categ in values if (date<=date_f and acc==compte)])
                        acc = real_accounts[t]
                        UID = BP.GetURL("get_account_uid_from_id:%s" % acc)
                        for Rec in records:
                            if Rec["account"] in (acc, UID) :
                                v += apply_record(Rec, date_f)
                            transfert = Rec.get("transfer",-1)
                            if transfert != -1 :
                                if transfert in (acc, UID) :
                                    v -= apply_record(Rec, date_f)
                        data[i][idx][6] = fmt_float(v); total[4]+=v
                        idx+=1

            # impression LOGO
            data[i][idx][index_Logo].Picture.LoadFromFile(Path + "Thumbs\\dummy.png")
            data[i][idx][index_Compte]="Total"
            Sw[i][0]=idx
            for k in range(len(total)):
                data[i][idx][k+2]=fmt_float(total[k])
            for k in range(len(data[i])-1):
                data[i][k][index_Logo].visible = True
    SetColumnsWidth()
    ResizeForm()

def toggle_sf(S=None):
    df.visible = sf.Checked
    update()
#-------------------------------------------------------------------------------
# section affichage

# calcul des largeurs de colonnes
def SetColumnsWidth():
    # grille des comptes
    w0 = 20; w1 = 50; w2 = 0
    for i in range(4):
        if Sw[i][0]:
            for j in range(Sw[i][0]):
                w0=max(w0,data[i][j][0].Picture.Width+10)
                w1=max(w1,grid_C[i].Canvas.TextWidth(data[i][j][1])*1.15+10)
    for i in range(4):
        for j in range(Sw[i][0]):
            for n in range(2,len(data[i][j])):
                w2 = max(w2,grid_C[i].Canvas.TextWidth(data[i][j][n])+10)
            if (grid_C[i].DefaultRowHeight+1) * grid_C[i].RowCount+2 >= grid_C[i].Height:
                grid_C[i].DefaultColWidth = max(w2,(grid_C[i].Width - grid_C[i].ColCount - 20 - w0 - w1) / (grid_C[i].ColCount - 2))
            else:
                grid_C[i].DefaultColWidth = max(w2,(grid_C[i].Width - grid_C[i].ColCount - 2 - w0 - w1) / (grid_C[i].ColCount - 2))
        grid_C[i].ColWidths[0] = w0
        grid_C[i].ColWidths[1] = w1

    # grille des opérations programmées
    w0 = grid_O.Canvas.TextWidth("  01/01/2001  ")
    w2 = grid_O.Canvas.TextWidth("-999 999.00")
    l = 0
    if ((grid_O.DefaultRowHeight+1)*grid_O.RowCount)+4 >= grid_O.Height:
        l+=23
    w1 = grid_O.Width-w0-w2-l-3
    grid_O.ColWidths[0] = w0
    grid_O.ColWidths[1] = w1
    grid_O.ColWidths[2] = w2
    grid_R.ColWidths[0] = w0
    grid_R.ColWidths[1] = w1
    grid_R.ColWidths[2] = w2


# mise à jour du mémo
def change_memo(Sender=None):
    global params
#    params['memo']=memo.Lines.Text.split('\n')[:-1]
    if memo.Lines.Text=='': memo.Color=0x00ffffff
    else: memo.Color=0x00a0ffff

# mise à jour des listes de comptes préférées
def maj_listes(Sender=None):
    FormLists.show(lists)
    for i in bm_list_C:
        val = Cvalue(bm_list_C[i])
        bm_list_C[i].Items.Text = "\n".join(FormLists.klist)
        if val in FormLists.klist and val!='':
            bm_list_C[i].ItemIndex = Ivalue(bm_list_C[i],val)
        else :
            bm_list_C[i].ItemIndex = -1
            if grid_C[i].visible: toggle_grids(Sw[i][1])





# adaptation des composants sur redimentionnement du formulaire
def ResizeForm(Sender=None):
    cW = FormTotals.ClientWidth
    cH = FormTotals.ClientHeight

#    trace(FormTotals.DockSite)

    g0.Width = cW; g0.Height = cH
    base = 150
    # groupe "réglages et préférences"
    gP.Left=0; gP.Height=70; gP.Top=cH-gP.Height; gP.Width=base*16/9+30
    b_operations.Left = margin; b_operations.Top = gP.Height-b_operations.Height-margin
    b_rappels.Left = b_operations.Left+b_rappels.Width+margin/3; b_rappels.Top = b_operations.Top
#    b_comptes.Left = b_rappels.Left+b_comptes.Width+margin/3; b_comptes.Top = b_operations.Top
    b_memo.Left = b_rappels.Left+b_memo.Width+margin/3; b_memo.Top = b_operations.Top
    Pref.Left = gP.Width-Pref.Width-margin; Pref.Top = gP.Height-Pref.Height-margin
    Wiki.Left = Pref.Left-Wiki.Width-5;Wiki.Top = Pref.Top+4

    # groupe "comptes"
    if gO.visible or gR.visible: gC.Left=gP.Width
    else: gC.Left=0
    gC.Top=0; gC.Width=cW-gC.Left
    if gM.visible: gC.Height=cH-base
    else: gC.Height=cH-2
    t0.Left = c_comptes.Left+c_comptes.Width+margin/3; t0.Top = c_comptes.Top+10
    bm.Left = gC.Width-bm.Width-margin; bm.Top = t0.Top-4
    df.Left = bm.Left-df.Width-margin/2; df.Top = t0.Top-2                      # date du solde futur
    sf.Left = df.Left-sf.Width-margin/2; sf.Top = t0.Top-1                      # solde futur
    Sw[3][1].Left = sf.Left-Sw[3][1].Width-margin; Sw[3][1].Top = sf.Top
    for i in range(2,-1,-1):
        Sw[i][1].Left = Sw[i+1][1].Left-Sw[i][1].Width-2; Sw[i][1].Top = Sw[i+1][1].Top
    grids_base = c_comptes.Top+c_comptes.Height+margin/2
    # --- grilles
    for i in range(4):
        if Sw[i][0]!=0:
            grid_C[i].visible = True; bm_list_C[i].visible = True
            grid_C[i].Top = grids_base; grid_C[i].Left = margin; grid_C[i].Width = gC.Width - grid_C[i].Left - margin; grid_C[i].Height = min((Sw[i][0]+2)*(grid_C[i].DefaultRowHeight+1)+3,gC.Height-grid_C[i].Top-margin)
            grid_C[i].RowCount = Sw[i][0] + 2
            bm_list_C[i].Left = grid_C[i].Left+grid_C[i].ColWidths[0]+margin; bm_list_C[i].Top = grid_C[i].Top-15; bm_list_C[i].Width = grid_C[i].ColWidths[1]+grid_C[i].ColWidths[2]-margin*2
            grids_base += grid_C[i].Height+margin*2
        else:
            grid_C[i].visible = False; bm_list_C[i].visible = False

    # groupe "opérations planifiées"
    gO.Left=0; gO.Top=0
    if gC.visible: gO.Width=gP.Width
    else: gO.Width=cW-2
    if gR.visible: gO.Height=gP.Top*2/3    #max(50,min(gP.Top*(len(prev)+1)/(len(todo)+len(prev)+2)-50,gP.Top-50))gP.Top*2/3
    else: gO.Height=gP.Top-1
    t1.Left = c_operations.Left+c_operations.Width+margin/3; t1.Top = c_operations.Top+10
    # --- grille
    grid_O.visible = len(prev)!=0
    grid_O.Top = c_operations.Top+c_operations.Height; grid_O.Left = margin; grid_O.Width = gO.Width - grid_O.Left - margin; grid_O.Height = min((len(prev)+1)*(grid_O.DefaultRowHeight+1)+3,gO.Height-grid_O.Top-margin)
    grid_O.RowCount=len(prev)

    # groupe "rappels"
    gR.Left=0
    if gO.visible: gR.Top=gO.Height
    else: gR.Top=0
    gR.Width=gP.Width; gR.Height=gP.Top-gR.Top
    t3.Left = c_rappels.Left+c_rappels.Width+margin/3; t3.Top = c_rappels.Top+10
    # --- grille
    grid_R.visible = len(todo)!=0
    grid_R.Top = c_rappels.Top+c_rappels.Height; grid_R.Left = margin; grid_R.Width = gR.Width - grid_R.Left - margin; grid_R.Height = min((len(prev)+1)*(grid_R.DefaultRowHeight+1)+3,gR.Height-grid_R.Top-margin)
    grid_R.RowCount=len(todo)

    SetColumnsWidth()

    # groupe "mémo"
    gM.Left=gP.Width;gM.Top=cH-base; gM.Width=cW-gM.Left; gM.Height=base
    t2.Left = c_memo.Left+c_memo.Width+margin/2; t2.Top = c_memo.Top+10
    # --- mémo
    memo.Left = margin; memo.Top = c_memo.Top+c_memo.Height; memo.Width = gM.Width-memo.Left-margin; memo.Height = gM.Height-memo.Top-margin
    if memo.Lines.Text=='': memo.Color=0x00ffffff
    else: memo.Color=0x00a0ffff
    # boutons de fonctions
    ver.Left = cW-ver.Width-margin
    ver.Top = cH-ver.Height-2

## adaptation des composants sur redimentionnement du formulaire "listes"
#def ResizeLists(Sender=None):
#    cW = FormLists.ClientWidth
#    cH = FormLists.ClientHeight
#    fond_lists.Width = cW; fond_lists.Height = cH
#
#    ll0.Top = margin
#    list0.Left=margin; list0.Top=ll0.Top+ll0.Height+margin/2; list0.Width=150; list0.Height=200
#    list1.Left=list0.Left+list0.Width+margin; list1.Top=list0.Top; list1.Width=150; list1.Height=200
#    ll0.Left = list1.Left-ll0.Width
#    cb_lists.Left = list1.Left; cb_lists.Top = margin-4; cb_lists.Width = list1.Width
#
#    ll1.Top = list1.Top+list1.Height+margin/2; ll1.Left = list1.Left-ll1.Width
#    new_list.Left = list1.Left; new_list.Top = ll1.Top-4; new_list.Width=list1.Width
#    ok_list.Left = new_list.Left+new_list.Width+margin/2; ok_list.Top = new_list.Top-2
#    ok_list.visible = new_list.Text!=''
#    ko_list.Left = cb_lists.Left+cb_lists.Width+margin/2; ko_list.Top = cb_lists.Top-2
#    ko_list.visible = cb_lists.ItemIndex!=-1
#    picker.Left = list1.Left+list1.Width+margin/2
#    picker.Top = list1.Top

# dessin de la grille des comptes
def draw(Sender, ACol, ARow, R, State):
    for i in range(4):
        if Sender == grid_C[i]: grid=i
    if Sw[grid]==0: return
    grid_C[grid].FixedRows = 1
    cv = Sender.Canvas
    maginV = (Sender.DefaultRowHeight-cv.TextHeight("A"))/2
    cv.Font.Color = 0x00000000
    cv.Brush.Color = 0x00e0e0e0
    if headers[ACol]=="Logos" or headers[ACol]=="Comptes":
        cv.Font.Color  = 0x00000000
        cv.Brush.Color = 0x00d0d0d0
    if ARow == 0 :
        cv.Font.Color = 0x00ffffff
        cv.Brush.Color = 0x00400000
    else:
        if headers[ACol]=="Aujourd'hui":
            cv.Brush.Color -= 0x00200000
        elif headers[ACol]=="Pointé":
            cv.Brush.Color -= 0x00001020

    if ARow % 2 == 0: cv.Brush.Color += 0x001f1f1f
    cv.FillRect(R)
    index = ARow-1
    try:
        if ARow == 0:
            #Ligne d'en-tête
            s = headers[ACol]
            cv.Font.Style = ["fsBold"]
            cv.TextRect(R, R.Left + 3, R.Top + maginV, s)
        else:
            #Autres lignes
            if ARow == Sw[grid][0]+1:
                cv.Brush.Color = 0x00600000
                cv.Font.Color  = 0x00ffffff
                cv.Font.Style = ["fsBold"]
            if headers[ACol]=="Logos":
                # masquer toute image se trouvant sur cette ligne
                for i in range(len(data[grid])-1):
                    if (data[grid][i][ACol].Top == R.Top+3) and i!=index: data[grid][i][ACol].Visible = False
                # afficher l'image de la ligne
                data[grid][index][ACol].SetProps(Top = R.Top+3, Left = R.Right -5 - data[grid][index][ACol].Picture.Width, Visible = True)
            elif  headers[ACol]=="Comptes":
                cv.Font.Style = ["fsBold"]
                s = data[grid][index][ACol]
                #Alignement à gauche pour les textes
                cv.TextRect(R, R.Left + 3, R.Top + maginV, s)
            else:
                #Alignement à droite pour les montants
                z = data[grid][index][ACol]
                if z.startswith("-"):
                    cv.Font.Color = 0x000000cc
                    if ARow == Sw[grid][0]+1:
                        cv.Font.Color  += 0x00404030
                else :
                    cv.Font.Color = 0x00008800
                    if ARow == Sw[grid][0]+1:
                        cv.Font.Color  += 0x00404040
                cv.TextRect(R, R.Right - 4 - cv.TextWidth(z), R.Top + maginV, z)
    except: pass
    c_comptes.BringToFront()

# dessin de la grille des opérations planifiées
def draw_O(Sender, ACol, ARow, R, State):
    if len(prev)==0 : return
    cv = Sender.Canvas
    maginV = (Sender.DefaultRowHeight-cv.TextHeight("A"))/2
    cv.Font.Color = 0x00000000
    cv.Brush.Color = 0x00e0e0e0
    if headers_O[ACol]=="Comptes":
        cv.Font.Color  = 0x00000000
        cv.Brush.Color = 0x00d0d0d0
    if ARow % 2 == 0: cv.Brush.Color += 0x001f1f1f
    cv.FillRect(R)
    index = ARow
    #try:
    #Autres lignes
    if  headers_O[ACol]=="Compte":
        cv.Font.Style = ["fsBold"]
        s = prev[index][0]; Tmp= R.Bottom; R.Bottom = (R.Top+R.Bottom)/2
        cv.TextRect(R, R.Left + 3, R.Top, s)
        cv.Font.Style = ["fsItalic"]
        s = prev[index][4]; R.Bottom=Tmp; R.Top = (R.Top+R.Bottom)/2
        cv.TextRect(R, R.Left + 3, R.Top, s)
    elif headers_O[ACol]=="Date":
        s = date_to_str(prev[index][2])
        #Alignement à gauche pour les dates
        cv.TextRect(R, R.Left + 3, R.Top + maginV, s)
    else:
        #Alignement à droite pour les montants
        z = fmt_float(prev[index][1])
        if z.startswith("-"): cv.Font.Color = 0x000000cc
        else : cv.Font.Color = 0x00008800
        cv.TextRect(R, R.Right - 4 - cv.TextWidth(z), R.Top + maginV, z)
    #except: pass

# dessin de la grille des opérations planifiées
def draw_R(Sender, ACol, ARow, R, State):
    if len(todo) == 0 : return
    cv = Sender.Canvas
    maginV = (Sender.DefaultRowHeight-cv.TextHeight("A"))/2
    cv.Font.Color = 0x00000000
    cv.Brush.Color = 0x00e0e0e0
    if headers_R[ACol]=="Mode":
        cv.Font.Color  = 0x00000000
        cv.Brush.Color = 0x00d0d0d0
    if ARow % 2 == 0: cv.Brush.Color += 0x001f1f1f
    cv.FillRect(R)
    #try:

    index = ARow
    #Autres lignes
    if  headers_R[ACol]=="Mode":
        cv.Font.Style = ["fsBold"]
        s = todo[index][0]
        TmpB, TmpR = R.Bottom, R.Right
        R.Bottom = (R.Top+R.Bottom)/2; R.Right = R.Left+int(cv.TextWidth(s)*1.15)+3
        cv.TextRect(R, R.Left + 3, R.Top, s)
        cv.Font.Style = ["fsItalic"]
        s = todo[index][3]
        R.Bottom, TmpL = TmpB, R.Left
        R.Left = R.Right; R.Right = TmpR
        cv.TextRect(R, R.Left + 3, R.Top, s)
        s = todo[index][4]
        R.Top = (R.Top+R.Bottom)/2; R.Left = TmpL
        cv.TextRect(R, R.Left + 3, R.Top, s)
    elif headers_R[ACol]=="Date":
        s = date_to_str(todo[index][2])
        #Alignement à gauche pour les dates
        cv.TextRect(R, R.Left + 3, R.Top + maginV, s)
    else:
        #Alignement à droite pour les montants
        z = fmt_float(todo[index][1])
        if z.startswith("-"): cv.Font.Color = 0x000000cc
        else : cv.Font.Color = 0x00008800
        cv.TextRect(R, R.Right - 4 - cv.TextWidth(z), R.Top + maginV, z)
    #except: pass


#def repaint(sender=None):
#    FormTotals.Repaint()
#-------------------------------------------------------------------------------
#Formulaire principal
#-------------------------------------------------------------------------------

def toggle_memo(S=None):
    global params
    if params['memo']:
        gM.visible=False
        b_memo.Hint="Afficher le mémo "
        b_memo.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\memo_off.png")
    else:
        b_memo.Hint="Masquer le mémo "
        b_memo.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\memo_on.png")
        gM.visible=True
    params['memo']= not params['memo']
    ResizeForm()

def toggle_operations(S=None):
    global params
    if params['operations']:
        gO.visible=False
        b_operations.Hint="Afficher les echéances "
        b_operations.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\operations_off.png")
    else:
        b_operations.Hint="Masquer les echéances "
        b_operations.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\operations_on.png")
        gO.visible=True
    params['operations']= not params['operations']
    ResizeForm()

def toggle_rappels(S=None):
    global params
    if params['rappels']:
        gR.visible=False
        b_rappels.Hint="Afficher les echéances "
        b_rappels.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\rappels_off.png")
    else:
        b_rappels.Hint="Masquer les echéances "
        b_rappels.ToTuple()[0].Picture.LoadFromFile(Path + "icons\\rappels_on.png")
        gR.visible=True
    params['rappels']= not params['rappels']
    ResizeForm()

def toggle_grids(S):
    for i in range(4):
        if S==Sw[i][1]: n=i
    if grid_C[n].visible:
        grid_C[n].visible=False
        bm_list_C[n].visible=False
        Sw[n][0]=0
        Sw[n][1].Picture.LoadFromFile(Path + "icons\\C_off.png")
        name_list ='~'
        if bm_list_C[n].ItemIndex!=-1: name_list = bm_list_C[n].Items[bm_list_C[n].ItemIndex]
        bm_list_C[n].Items.Text = '\n'.join(klist)
        if name_list in bm_list_C[n].Items.Text:
            bm_list_C[n].ItemIndex = bm_list_C[n].Items.Text.split('\n').index(name_list)
        else:
            bm_list_C[n].ItemIndex = -1
    else:
        grid_C[n].visible=True
        bm_list_C[n].visible=True
        Sw[n][0]=1
        Sw[n][1].Picture.LoadFromFile(Path + "icons\\C_on.png")
    update()

def Sortie(Sender=None,P=None):
    i=4
    for n in range(4):
        if Sender == grid_C[n]: i=n
    if i<4:
        if grid_C[i].Row-1 < Sw[i][0]:
            name = data[i][grid_C[i].Row-1][1]
            if name!='':
                acc = real_index[name]
                BP.AccountChangeCurrent(acc)
            FormTotals.ModalResult = 2
    elif Sender == grid_O:
        if grid_O.Row < len(prev):
            name = prev[grid_O.Row][0]
            acc = real_index[name]
            BP.AccountChangeCurrent(acc)
            FormTotals.ModalResult = 2
#    elif Sender == grid_R:
#        if grid_R.Row < len(todo):
#            name = todo[grid_R.Row][5]
#            acc = real_index[name]
#            BP.AccountChangeCurrent(acc)
#            FormTotals.ModalResult = 2
    return

def close_form(S=None,P=None):
    # sauvegarde des parmaètres de position et de taille de la fenêtre
    params['position']=[FormTotals.Left,FormTotals.Top,FormTotals.Width,FormTotals.Height]
    params['sf_view']=sf.Checked                                            # solde futur
    params['sf_date']=from_delphi_date(df.Date)                             # date du solde futur
    Switches = Sw.items(); Switches.sort()
    params['switches']=[sw[1][0] for sw in Switches]                         # grilles à afficher
    Lists = bm_list_C.items(); Lists.sort()
    params['groups']=[l[1].ItemIndex for l in Lists]                        # associations grilles/groupes
    params['text']=memo.Lines.Text                                          # mémo
    params['lists']=lists                                                   # groupes de comptes
    set_params(params)

# icône 'préférences'
def ParamsCall(Sender): P.ShowModal()

# création du formulaire principal
FormTotals = CreateComponent("TForm", None)
FormTotals.SetProps(Width=900, Height=600, Caption = "Accueil", ShowHint=True, OnClose=close_form)
g0 = make(CC,"TImage", FormTotals, Left = 0, Top = 0, Picture=Path + "Icons\\ciel.png")

# groupe "comptes"
gC = make(CC,"TGroupBox", FormTotals)
c_comptes = make(CC, "TImage", gC, Width=50, Height=40, Picture=Path + "icons\\cadre_pieces.png")
t0 = make(CC, "TLabel", gC, FontSize = 12, FontStyle = ["fsBold","fsItalic"], Caption="Mes comptes ")
bm = make(CC,"MyButton", gC, Left = 50, Top = margin, Width=26, Height=26, OnClick=maj_listes, Hint='Gérer les groupes de comptes', Picture=Path + "Icons\\bookmark.png")
# --- solde futur
sf = make(CC,"TCheckBox", gC, Width = 80, Caption = "Solde futur", OnClick = toggle_sf)
df = make(CC,"TDateTimePicker", gC, Width=110, Date=time.mktime(time.localtime()) / 86400 + 25569)
df.OnChange=update
df.visible=sf.Checked
# --- switches et grilles
for i in range(4):
    Sw[i] = [0, make(CC, "TImage", gC, Width=18, Height=18, OnClick=toggle_grids, Picture = Path + "icons\\C_on.png")]
    grid_C[i] = make(CC,"TDrawGrid", gC)
    grid_C[i].SetProps(ColCount=7, OnDrawCell=draw, FixedCols=0, FixedRows=1, DefaultRowHeight = 31, ScrollBars="ssBoth", Options = ["goHorzLine", "goVertLine", "goThumbTracking"])
    grid_C[i].OnClick = Sortie
    bm_list_C[i] = make(CC, "TComboBox", gC, FontSize = 9, OnClick=update)
    bm_list_C[i].Style="csDropDownList"
    bm_list_C[i].ItemIndex = 1
    logo_C[i] = make(CC, "TImage", grid_C[i], Width=50, Height=40, Picture = Path + "Groups\\_pas de logo_.png")

# groupe "opérations planifiées"
gO = make(CC,"TGroupBox", FormTotals)
grid_O = make(CC,"TDrawGrid", gO)
grid_O.SetProps(ColCount=3, OnDrawCell=draw_O, FixedCols=0, FixedRows=0, DefaultRowHeight = 31, ScrollBars="ssBoth", Options = ["goHorzLine", "goVertLine", "goThumbTracking"])
grid_O.OnClick = Sortie
c_operations = make(CC, "TImage", gO, Width=50, Height=40, Picture=Path + "icons\\cadre_echeancier.png")
t1 = make(CC, "TLabel", gO, FontSize = 12, FontStyle = ["fsBold","fsItalic"], Caption="Mes opérations planifiées ")

# groupe "mémo"
gM = make(CC,"TGroupBox", FormTotals)
memo = make(CC,"TMemo", gM, FontSize = 12); memo.OnChange = change_memo; memo.ScrollBars="ssVertical"
c_memo = make(CC, "TImage", gM, Width=50, Height=40, Picture=Path + "icons\\cadre_memo.png")
t2 = make(CC, "TLabel", gM, FontSize = 12, FontStyle = ["fsBold","fsItalic"], Caption="Ne pas oublier ")

# groupe "rappels"
gR = make(CC,"TGroupBox", FormTotals)
grid_R = make(CC,"TDrawGrid", gR)
grid_R.SetProps(ColCount=3, OnDrawCell=draw_R, FixedCols=0, FixedRows=0, DefaultRowHeight = 31, ScrollBars="ssBoth", Options = ["goHorzLine", "goVertLine", "goThumbTracking"])
grid_R.OnClick = Sortie
c_rappels = make(CC, "TImage", gR, Width=50, Height=40, Picture=Path + "icons\\cadre_rappels.png")
t3 = make(CC, "TLabel", gR, FontSize = 12, FontStyle = ["fsBold","fsItalic"], Caption="Mes rappels ")

# groupe "préférences et réglages"
gP = make(CC,"TGroupBox", FormTotals)
Pref = make(CC, "TImage", gP, Width=32, Height=32, OnClick=ParamsCall, Picture=Path + "icons\\preferences.png")
Wiki = make(CC, "TImage", gP, Hint = "Documentation en ligne", Width=28, Height=28, OnClick=goto_wiki, Picture=Path + "icons\\wiki.png")
# --- bascules d'affichage pour le mémo, les opérations planifiées, les rappels
b_memo = make(CC,"MyButton", gP, Left = margin, Top = sf.Top+sf.Height+margin/2, Width=54, Height=44, OnClick=toggle_memo, ShowHint=1, Hint="Masquer le mémo ", Picture=Path + "icons\\memo_on.png")
b_operations = make(CC,"MyButton", gP, Left = margin, Top = sf.Top+sf.Height+margin/2, Width=54, Height=44, OnClick=toggle_operations, ShowHint=1, Hint="Masquer les opérationso ", Picture=Path + "icons\\operations_on.png")
b_rappels = make(CC,"MyButton", gP, Left = margin, Top = sf.Top+sf.Height+margin/2, Width=54, Height=44, OnClick=toggle_rappels, ShowHint=1, Hint="Masquer les rappels ", Picture=Path + "icons\\rappels_on.png")
# --- version
ver = make(CC, "TLabel", FormTotals, Left = 30, Top = 70, FontSize = 7, FontColor = 0x00606060, FontStyle = ["fsItalic"], Caption="version "+version+" ")




#-------------------------------------------------------------------------------
#Programme principal
#-------------------------------------------------------------------------------

FormLists = AccountsListsForm(CC, None)    # mise en place du formulaire de gestion des groupes de comptes

#initialistion des contrôles en fonction des paramètres
df.Date = to_delphi_date(params['sf_date'])
sf.Checked = params['sf_view']
Switches = params['switches']
memo.Lines.Text = params['text']
Lists = params['groups']
lists = params['lists']
klist = lists.keys()
klist.sort()
for i in range(4):
    bm_list_C[i].Items.Text = '\n'.join(klist)
    bm_list_C[i].ItemIndex = Lists[i]
    if Switches[i] and Lists[i]!=-1:
        Sw[i][0] = len(lists[bm_list_C[i].Items[Lists[i]]])
        Sw[i][1].Picture.LoadFromFile(Path + "icons\\C_on.png")
    else:
        Sw[i][0] = 0
        Sw[i][1].Picture.LoadFromFile(Path + "icons\\C_off.png")



init_data()                                     # création de la structure de données
records = load_echeancier()                     # chargement de l'échéancier
#load_PrefAccounts()                             # chargement des paramètres de la session précédentes (groupes de comptes, listes à afficher, ...)
values = load_values()                          # chargement des données de BP (toutes les opérations de tous les comptes)
update()                                        # chargement des données dans les grilles à afficher


if len(params['position'])==4:
    FormTotals.Left,FormTotals.Top,FormTotals.Width,FormTotals.Height = params['position']
else:
    FormTotals.Position = "poMainFormCenter"
toggle_memo();toggle_memo()
toggle_operations();toggle_operations()
toggle_rappels();toggle_rappels()

FormTotals.OnResize = ResizeForm        # mise en forme de la fenêtre
#ResizeForm()

if params['position'][0]<0 : 
    FormTotals.WindowState='wsMaximized'
    for i in range(4): params['position'][i]+=[8,8,-16,-16][i]
    FormTotals.Left,FormTotals.Top,FormTotals.Width,FormTotals.Height = params['position']

FormTotals.ShowModal()                  # affichage de la fenêtre
