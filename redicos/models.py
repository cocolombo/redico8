from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from propositions.models import Proposition
from evaluations.models import Evaluation
from django.db.models import Q  # Count
import itertools
import pandas as pd
from joueurs.models import Joueur
from propositions.models import Proposition
from joueurs.models import Joueur
from itertools import chain
import numpy as np
from django.db.models import F
from propositions.models import Proposition
from operator import itemgetter
import math as m
from statistics import mean
from operator import attrgetter
from django.db.models.query import QuerySet
# Create your models here.
nb_Items = 5


class Redico(models.Model):
    """
    nb()['joueurs'] ['props'] ['evals']
    les_joueurs()['obj'] ['ids'] ['df'] ['noms']
    joueur_participe(self, id)
    les_props()['obj']  ['ids']  ['df']
    les_evals()['lst'] ['df']
    calcstats()['df']
    joueurs_comb()['lst']  ['df']
    data() ['lst']  ['df']
    heatmap()['df']
    """
    # class Meta:
    #     ordering = ('-id', )
    titre = models.TextField(unique=True)
    createur = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name='Redico_createur')
    debut = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True, editable=True)

    def get_absolute_url(self):
        return "/redico/%i/" % self.id
    def createur_nom_id(self):
        return list(Redico.objects.values(nom_=F('createur__username'),id_=F('createur')).get(id=self.id))
    def participants_noms_ids(self):
        # [{'nom_': 'cocolombo2', 'id_': 275}, ... ]
        noms_ids = list(Proposition.objects.filter(redico=self.id).values(nom_=F('auteur__username'),id_=F('auteur__id')).distinct())
        return noms_ids
    def nb_joueurs(self):
        return len(self.participants_noms_ids())
    def les_props(self):
        # [<Proposition: Proposition object (3511)>, ... ]
        props = Proposition.objects.filter(redico=self.id).order_by('-sequence')
        return props
    def nb_props(self):
        return len(self.les_props())
    def les_evals(self):
        # [{'id': 10428, 'proposition_id': 3510, 'joueur_id': 275,
        # 'commentaire': 'Le chiffre ne s'affiche pas sous le slider',
        # 'eval': 70.0, 'date_eval': datetime.date(2020, 12, 9), 'nb_edit': 0}, ...]
        evals_lst = list(Evaluation.objects.values().filter(Q(proposition__redico=self.id) & ~Q(eval=-1)))
        return evals_lst
    def nb_evals(self):
        return len(self.les_evals())
    def participe_au_redico(self, joueur_id):
        participants = self.participants_noms_ids()
        try:
            p = list(map(itemgetter('id_'), participants)).index(joueur_id)
            # print(p)
            return True
        except:
            return False

            # def joueurs_combinaison2x2(self):
    #     """
    #     Toutes les combinaisons entre les joueurs
    #     # joueurs_comb['lst'] = [[2, 209], [2, 108], [209, 108]]
    #     # joueurs_comb['df'] =
    #     #      j1    j2
    #     # 0    2    209
    #     # 1    2    108
    #     # 2    209  108
    #     :return:
    #     """
    #     joueurs_list = list(self.les_joueurs_noms_et_ids()['lst_ids'])  # .values('id'))
    #     joueurs_comb = list(itertools.combinations(joueurs_list, 2))
    #     lst = [list([l[0], l[1]]) for l in joueurs_comb]
    #     df = pd.DataFrame(lst, columns=['j1', 'j2'])
    #     return {'lst': lst, 'df': df}
    #
    #

    # Ça apparaît dans le câdre entre action et Dernières propositions
    def heatmap(self):
        """
        # df_diff
        # nom0  # 0        e0  nom1  #1      e1     diff
        # 0 Denis 2   99.9990 Cogit 108 99.9999 0.0009
        # 1 Denis 2   99.9990 LePsy 209 60.0000 39.9990
        # 2 Cogit 108 99.9999 LePsy 209 60.0000 39.9999
        # df_grid
        #        LePsy Cogit Denis
        # LePsy    0.0   0.o, i, df, 0   0.0
        # Cogit    0.0   0.0   0.0
        # Denis    0.0   0.0   `0.0
        :return:
        """
        def my_apply(row):
            df_diff.at[row.J0, row.J1] = abs(row.e0 - row.e1)

        def df_bg_color(val):
            if   val > 0 and val < 10:       color = '#01B400'
            elif val >= 10 and val < 33.3:   color = '#51FF50'
            elif val >= 33.3 and val < 66.7: color = '#FFFFFF'
            elif val >= 66.7 and val < 90:   color = '#FE504F'
            elif val >= 90 and val <= 100:   color = '#B40001'
            else:                            color = '#c8d1d7'
            return f'background-color: {color}; color: black;'
        # def df_empty():
        #     """
        #     :param
        #     :return df_grid: pd.DataFrame
        #     df_grid
        #            EeG  Alain  samue  Etien
        #     EeG   -1.0   -1.0   -1.0   -1.0
        #     Alain -1.0   -1.0   -1.0   -1.0
        #     samue -1.0   -1.0   -1.0   -1.0
        #     Etien -1.0   -1.0   -1.0   -1.0
        #     """
        #     noms = [n[0:5] for n in self.les_joueurs_noms()]
        #     noms = sorted(noms)
        #     n = len(noms)
        #     mat = np.empty((n, n))
        #     mat.fill(-1)
        #     df_grid = pd.DataFrame(mat, index=noms, columns=noms)
        #     df_grid.replace('-1', '*', inplace=True)
        #     return df_grid
        def df_diff():
            """
            # Appelle proposition.models.df_diff()['lst']
            # pourchaque proposition
            # Retourne un df pour les différences
            # Out[3]:
            #   props_seq   nom0 #0   e0  nom1 #1    e1 diff
            # 0        18  Denis  2 99.9 Etien 26  50.0 49.9
            # 1        18  Denis  2 99.9 eatsa 46  99.9  0.0
            # 2        18  Denis  2 99.9 Talis 106 99.0  0.9
            # 3        18  Etien 26 50.0 eatsa 46  99.9 49.9
            # 4        18  Etien 26 50.0 Talis 106 99.0 49.0
            # 5        18  eatsa 46 99.9 Talis 106 99.0  0.9
            :return:
            """
            lst = []
            for prop in self.les_props(): # [<Proposition: Proposition object (3511)>, ... ]
                for p in prop.df_diff()['lst']:
                    lst.append(p)
            df = pd.DataFrame(lst, columns=['red_id', 'props_seq', 'J0', '#0', 'e0', 'J1', '#1', 'e1'])
            num = df._get_numeric_data()
            num[num < 0] = np.nan

            # df['e0-e1'] = abs(df['e0'] - df['e1'])
            # df['e0+e1'] = abs(df['e0'] + df['e1'])
            # df['moy'] = df['e0+e1']/2
            # df['moy*1-moy'] = abs((df['moy']*(1-df['moy'])))
            #
            # # df['(df[moy]/(1-df[moy])'] = np.ma.array(df['(df[moy]/(1-df[moy])'], mask=np.isnan(df['(df[moy]/(1-df[moy])']))
            # df['sqrt'] = np.sqrt(df['moy*1-moy'])
            # # print(f'L 172: {df}')
            # df['diff'] = abs(df['e0-e1']/df['sqrt'])
            # # print(f'L 179: {df}')
            df['écart'] = abs(df['e0'] - df['e1'])

            # =ABS(R$1-$N6)/SQRT((ABS((R$1+$N6)/2))*ABS((1-(R$1+$N6)/2)))
            df = df.sort_values(by=['props_seq', 'J0', 'J1'])
            return {'lst': lst,
                    'df': df}


        # if self.nb_joueurs() < 2:
        #     return None

        # heatmap = df_empty()
        df_diff = df_diff()['df']
        df_diff.apply(my_apply, axis=1)
        # print('df_diff: ', df_diff)
        # heatmap = heatmap.replace('-1', '*')
        # heatmap = heatmap.style.applymap(df_color).render()
        if df_diff.empty == False:
            df_diff.groupby(['props_seq', 'J0', 'J1']).mean()
            df = df_diff['écart'].groupby([df_diff['J0'], df_diff['J1']]).mean()
            df = df.to_frame()
            print(f'df: L198 {df}')
            # df = df.round(decimals=2)
            print(f'df: L200 {df}')
            # df.apply(highlight_max())
            # df['écart-50'] = df['écart']-50
            # df = df.style.applymap(df_bg_color).set_precision(2).bar(subset=['écart'], color=['#d65f5f']).render()
            df = df.style.set_caption('Écarts').\
                          highlight_max(subset='écart', color='#cf7474', axis=0).\
                          highlight_min(subset='écart', color='#01B400', axis=0).\
                          set_precision(2).render()

            print(f'L 203 {df}')
            # df.style.apply(highlight_max)
            # df.style.set_caption("Statistiques").re
            # df = df.to_html()
            # print(f'L 191 {df}')

            # df = df.style.applymap(df_background_color).set_precision(1).render() # table_title="Statistiques")
            return df
        else:
            return None



