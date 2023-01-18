from django.shortcuts import render

# Create your views here.
# -*- coding: latin-1 -*-
# joueurs/views.py
# VIEWS
# from django.http import Http404
# from redicos.models import Redico
# from evaluations.models import Evaluation
from django.shortcuts import render
from joueurs.models import Joueur

def index(request):
    # joueurs = Joueur.objects.all().order_by('-id')
    # Que les joueurs actifs (avec au moins une evaluation
    # joueurs = Evaluation.objects.values_list('joueur__id').distinct()
    # joueurs = Joueur.objects.values('evaluation__joueur__id').distinct()
    joueurs = Joueur.objects.exclude(evaluation__joueur__id=None).distinct()
    joueurs = joueurs.order_by('-date_joined')
    c = {'request':request,
         'joueurs':joueurs,
         'show_profil'     : True,
         'show_add_redico' : True,
         'show_add_prop'   : False,
         'show_add_eval'   : False,
         'show_edit_redico': False,
         'show_edit_prop'  : False,
         'show_edit_eval'  : False
         }
    return render(request,  "joueurs/index.html",c)
# https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
# def index_df(request):
#     joueurs = Joueur.objects.exclude(evaluation__joueur__id=None).distinct()
#     joueurs = joueurs.order_by('username')
#     print(joueurs)
#     joueurs_df = joueurs.values_list('id','username')
#     joueurs_df = list(joueurs_df)
#     df = pd.DataFrame(joueurs_df, columns=['id', 'username']).to_html
#     c = {'request':request,
#          'df': df}
#     return render(request,  "joueurs/index_df.html", c)
def detail(request, joueur_id):
    joueur = Joueur.objects.get(id=joueur_id)
    # redAuteur = Redico.objects.filter(createur=lejoueur)
    # redParticipants = Evaluation.objects.filter(joueur=joueur_id).values('proposition__redico__id', 'proposition__redico__titre').distinct()
    # c = {'request':request,
    #      'joueur':joueur,}

    c = { 'joueur': joueur,
          'show_profil'         : True,
          'show_action_redico'  : True,
          'show_action_prop'    : False }

    # 'redAuteur':redAuteur }
    # 'redParticipants':redParticipants, }
    # return HttpResponse(t.render(c))
    return render(request, "joueurs/detail.html", c)


# from django.contrib.auth.models import User
import pandas as pd
# def index(request):
#     # joueurs = Joueur.objects.all().order_by('-id')
#     # Que les joueurs actifs (avec au moins une evaluation
#     # joueurs = Evaluation.objects.values_list('joueur__id').distinct()
#     # joueurs = Joueur.objects.values('evaluation__joueur__id').distinct()
#     lst = []
#     joueurs = Joueur.objects.exclude(evaluation__joueur__id=None).distinct()
#     joueurs = joueurs.order_by('username')
#     for j in joueurs:
#         lst.append(list(j.redsParticipantsList().values_list('proposition__redico__id', flat=True)))
#     info = zip(joueurs, lst)
#     df = pd.DataFrame(info)
#     df.at[:, 'B'] = lst
#     print(df)
#     c = {'request':request,
#          'df':df.to_html()}
#     # c = {'request':request,
#     #      'joueurs':joueurs}
#     return render(request,  "joueurs/index_df.html",c)

# /home/nimzo/PycharmProjects/redico/redico/templates/joueurs/index.htmlhere.