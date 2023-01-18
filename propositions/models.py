from django.db import models

# Create your models here.
# -*- coding: latin-1 -*-

from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from evaluations.models import Evaluation
from django.db.models import Q
import pandas as pd
import itertools
import numpy as npe
from django.db.models import F
from itertools import groupby
import more_itertools as mit

class Proposition(models.Model):
    auteur      = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    redico      = models.ForeignKey('redicos.Redico', editable=False, on_delete=models.CASCADE)
    sequence    = models.IntegerField(editable=False)    # Repart a 1 pour chaque redico
    texte       = models.TextField()
    photo       = models.ImageField(blank=True, upload_to='static/image')  # Il faut instaler PIL
    lien        = models.URLField(blank=True)
    preambule   = models.TextField(blank=True, verbose_name='preambule')
    date_de_pub = models.DateField(verbose_name='date de publication', auto_now_add=True)

    def __str__(self):
        return f"id:{self.id:>6} auteur:{self.auteur.username:>6} redico: {self.redico.id:>3} " \
               f"seq:{self.sequence:>3} texte: {self.texte[:5]:>5} " \
               f"lien: {self.lien:>5} préambule: {self.preambule[:5]:>5}"
    def name(self):
        return self.texte.split('\n', 2)[0]
    def get_absolute_url(self):
        p = Proposition.objects.get(pk=self.id)
        # return "/redico/%i/%i/" % self.p.redico, self.p.sequence
        return "/redico/%i/proposition/%i/" % (p.redico.id, p.sequence)


    def evals(self):
        """
        Retourne les évaluations pour cette proposition
        Type ; list de tuple de tuple
        Champs: Redico#, sequence%, nomjoueur, idjoueur, eval
        Val : [((49, 1, 'Denis', 2, 5.0), (49, 1, 'LePsychosophe', 209, 10.0)), ...

        :return:
        """
        evals = Evaluation.objects.filter(proposition=self.id).order_by('joueur__username')  # .values_list('eval', flat=True)
        prop_evals = evals.values(redId=F('proposition__redico_id'),
                                     seqId=F('proposition__sequence'),
                                     nom=F('joueur__username'),
                                     joueurId=F('joueur'),
                                     evaluation=F('eval'),
                                     le_commentaire=F('commentaire'),
                                     nbEdits=F('nb_edit'),
                                     laDate=F('date_eval'))
        joueur_eval_comb = list(itertools.combinations(prop_evals, 2))
        # Traiter le cas d'un seul joueur
        if len(evals) > 1:
            eval00 = joueur_eval_comb[0][0]['evaluation']
            eval01 = joueur_eval_comb[0][1]['evaluation']
            if (eval00 == -1) or (eval01 == -1):
                diff = 0
            else:
                diff = abs(eval00-eval01)
        else:
            diff = 0
        return { 'evals': prop_evals , 'diff': diff, 'joueur_eval_comb': joueur_eval_comb }


    def les_evaluateurs_id(self):
        """
        Retourne type list
        Retourne val  [216, 228, 229]
        :return:
        """
        evaluateurs_id = list(Evaluation.objects.filter(proposition=self.id).
                        values_list('proposition__evaluation__joueur', flat=True).distinct())
        # cnt = len(evaluateurs)
        return evaluateurs_id

    def nb_evaluateurs(self):
        nb = len(self.les_evaluateurs_id())
        return nb

    def nb_evaluations(self):
        nb = len(self.evals()['evals'])
        return nb

    def moyenne_des_evals(self):
        """
        Retourne: type float
        Retourne: val 96.2
        :return:
        """
        moy = Evaluation.objects.filter(Q(proposition=self.id) & ~Q(eval=-1)).aggregate(Avg('eval'))
        return moy['eval__avg']

    def short_username(self):
        return self.auteur.username[:5]

    # def joueurs_eval_comb(self):
    #     """
    #     # Retourne tous les couples de joueurs pour la proposition
    #     # [(('Denis', 2, 99.9), ('EtienneBeauman', 26, 50.0)),
    #     #  (('Denis', 2, 99.9), ('eatsalad', 46, 99.9)),
    #     #  (('Denis', 2, 99.9), ('Talisker', 106, 99.0)),
    #     #  (('EtienneBeauman', 26, 50.0), ('eatsalad', 46, 99.9)),
    #     #  (('EtienneBeauman', 26, 50.0), ('Talisker', 106, 99.0)),
    #     #  (('eatsalad', 46, 99.9), ('Talisker', 106, 99.0))]
    #     :return:
    #     """
    #     evals = self.les_evaluations()
    #     joueur_eval = list(evals.values_list('proposition__redico_id', 'proposition__sequence', 'joueur__username', 'joueur', 'eval'))
    #     # joueur_eval_comb = list(itertools.combinations(joueur_eval, 2))
    #     joueur_eval_comb = sorted(itertools.combinations(joueur_eval, 2))
    #     return joueur_eval_comb


    def joueurs_eval_comb(self):
        """
        # Retourne tous les couples de joueurs pcount()our la proposition
        # [(('Denis', 2, 99.9), ('EtienneBeauman', 26, 50.0)),
        #  (('Denis', 2, 99.9), ('eatsalad', 46, 99.9)),
        #  (('Denis', 2, 99.9), ('Talisker', 106, 99.0)),
        #  (('EtienneBeauman', 26, 50.0), ('eatsalad', 46, 99.9)),
        #  (('EtienneBeauman', 26, 50.0), ('Talisker', 106, 99.0)),
        #  (('eatsalad', 46, 99.9), ('Talisker', 106, 99.0))]
        :return:
        """
        evals = self.evals()['evals']
        # print(evals[0])
        joueur_eval = list(evals.values_list('proposition__redico_id', 'proposition__sequence', 'joueur__username', 'joueur', 'eval'))
        # joueur_eval_comb = list(itertools.combinations(joueur_eval, 2))
        joueur_eval_comb = sorted(itertools.combinations(joueur_eval, 2))
        return joueur_eval_comb


    # def a_deja_evalue(self, joueur_id):
    #     """
    #     :param joueur_id:
    #     :return:
    #     """
    #     if joueur_id in self.les_evaluateurs()['lst']:
    #         return True
    #     else:
    #         return False
    #
    # def peut_evaluer(self, joueur_id):
    #     """
    #     :param joueur_id:
    #     :return: True False
    #     """
    #     # Ne participe pas ou a déjà évalué
    #     if not self.redico.participe_au_redico(joueur_id) or self.a_deja_evalue(joueur_id): # T/F
    #         return False
    #     else:
    #         # N'a pas encore evalué il peut le faire)
    #         return True
    # def peut_editer_eval(self, joueur_id):
    #     """
    #     :param joueur_id:
    #     :return: True False
    #     """
    #     # S'il participe au redico et a déjà évalué cette proposition
    #     # il peut éditer son évaluation
    #     if self.redico.participe_au_redico(joueur_id) and joueur_id in self.les_evaluateurs()['lst']:
    #         return True
    #     else:
    #         return False
    # def peut_editer_prop(self, joueur_id):
    #     # S'il est l'auteur de la proposition et que la proposition
    #     # n'est pas encore évaluée, il peut éditer la proposition
    #     # return True
    #     if joueur_id == self.auteur_id and self.les_evaluations().count() == 0:
    #         return True
    #     else:
    #         return False
    def df_diff(self):
        """
        # Retourne un df pour les différences
        # Retourne lst des différences
        # Out[3]:
        #   props_seq   nom0 #0   e0  nom1 #1    e1 diff
        # 0        18  Denis  2 99.9 Etien 26  50.0 49.9
        # 1        18  Denis  2 99.9 eatsa 46  99.9  0.0
        # 2        18  Denis  2 99.9 Talis 106 99.0  0.9
        # 3        18  Etien 2            # prop_seq = couple[0][1];
            # red = couple[0][0];
            # id1  = couple[1][0];
            # nom0 = couple[0][2][:5];
            # nom1 = couple[1][2][:5];6 50.0 eatsa 46  99.9 49.9
        # 4        18  Etien 26 50.0 Talis 106 99.0 49.0
        # 5        18  eatsa 46 99.9 Talis 106 99.0  0.9

        :return:
        """
        lst = []
        for couple in self.joueurs_eval_comb():
            # print(couple)
            prop_seq = couple[0][1];
            red = couple[0][0];      id1  = couple[1][0]
            nom0 = couple[0][2][:5]; nom1 = couple[1][2][:5]
            id0 = couple[0][3];      id1  = couple[1][3]
            val0 = couple[0][4];     val1 = couple[1][4]
            lst.append([red, prop_seq, nom0, id0, val0, nom1, id1, val1])
        df_diff = pd.DataFrame.from_records(lst,
                                            columns=['red', 'props_seq', 'nom0', 'id0', 'e0', 'nom1', 'id1', 'e1'])
        df_diff['diff'] = (abs(df_diff['e0'] - df_diff['e1']))/100
        df_diff = df_diff.sort_values(by=['nom0'])

        return {'df':df_diff, 'lst':lst}


    def nbPropsConsecutives(self, joueur_id):
        ps = list(Proposition.objects.filter(auteur=joueur_id, redico=self.redico_id).values_list('sequence'))
        ps = [item for t in ps for item in t]
        l = [list(group) for group in mit.consecutive_groups(ps)]
        return len(l[-1])


    # def heatmap(self):
    #     return
    #     from heatmap.views import heatmap
    #     return heatmap(self.redico.id, self.sequence)


    # def heatmap2(self):
    #     """
    #     # df_diff
    #     # nom0  # 0        e0  nom1  #1      e1     diff
    #     # 0 Denis 2   99.9990 Cogit 108 99.9999 0.0009
    #     # 1 Denis 2   99.9990 LePsy 209 60.0000 39.9990
    #     # 2 Cogit 108 99.9999 LePsy 209 60.0000 39.9999
    #     # df_grid
    #     #        LePsy Cogit Denis
    #     # LePsy    0.0   0.0   0.0
    #     # Cogit    0.0   0.0   0.0
    #     # Denis    0.0   0.0   `0.0
    #     :return:
    #     """
    #     def df_empty():
    #         """
    #         :param noms: str
    #         :return df_grid: pd.DataFrame
    #         """
    #         from joueurs.models import Joueur
    #         evaluateurs = self.les_evaluateurs()['lst']  # <QuerySet [2, 26, 46, 106, 105, 19, 107]>
    #         evaluateursO = list((Joueur.objects.filter(id__in=evaluateurs)))
    #         noms = [n.username[0:5] for n in evaluateursO]
    #         #noms = list(reversed(noms))
    #         noms = sorted(noms)
    #         n = len(evaluateursO)
    #         mat = np.empty((n, n))
    #         mat.fill(-1)
    #         df_grid = pd.DataFrame(mat, index=noms, columns=noms)
    #         return df_grid
    #     def my_apply(row):
    #         # Source df_diff (row)
    #         # Target df_grid_a_remplir (.at)
    #         if row.e0 == -1 or row.e1 == -1:
    #             diff = np.nan
    #         else:
    #             diff = abs(row.e0 - row.e1)
    #         df_grid_a_remplir.at[row.nom0, row.nom1] = diff
    #     # def df_color(val):
    #     #     """
    #     #     Takes a scalar and returns a string with the css
    #     #     property `'color: red'` for negative strings, black otherwise.
    #     #     """
    #     #     if type(val) is str or val is None:
    #     #         color = 'black'
    #     #     else:
    #     #         color = 'black' if val < 0 else 'green'
    #     #     return 'color: %s' % color
    #     def df_background_color(val):
    #         if   val > 0 and val < 10:       color = '#01B400'
    #         elif val >= 10 and val < 33.3:   color = '#51FF50'
    #         elif val >= 33.3 and val < 66.7: color = '#FFFFFF'
    #         elif val >= 66.7 and val < 90:   color = '#FE504F'
    #         elif val >= 90 and val <= 100:   color = '#B40001'
    #         else:                            color = '#c8d1d7'
    #         return 'background-color: %s' % color
    #
    #     # Pas d'affichage pour 1 joueur
    #     if self.redico.nb()['joueurs'] < 2:
    #         return None
    #     else:
    #         df_grid_a_remplir = df_empty()
    #         df_diff = self.df_diff()['df']
    #         df_diff.apply(my_apply, axis=1)
    #         # df_grid_a_remplir = df_grid_a_remplir.fillna('=')
    #         # df_grid_a_remplir = df_grid_a_remplir.style.applymap(df_background_color).render()
    #         df_grid_a_remplir = df_grid_a_remplir.replace('-1','*')
    #         return df_grid_a_remplir


