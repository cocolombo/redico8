from django.shortcuts import render

# Create your views here.
# -*- coding: latin-1 -*-
# from django.shortcuts import render
from django.views.generic import CreateView, DeleteView

from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from redicos.models import Redico
from evaluations.models import Evaluation
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RedicoAjoutEditForm
from django.views import View
from .decorator import peut_effacer_redico
from django.contrib import messages
from django.shortcuts import get_object_or_404



def index(request):
    # def index():
    # Liste des redicos et du nombre de propositions
    # r[0].proposition__count
    print('redico.index')
    reds = Redico.objects.filter(actif=True).order_by('-id')
    # reds_avant_2016 = Redico.objects.filter(actif=True).filter(debut__year__lte='2016').order_by('-id')
    # reds_apres_2016 = Redico.objects.filter(actif=True).filter(debut__year__gte='2016').order_by('-id')

    # reds = Redico.objects.all().annotate(Count('proposition', distinct=True)) \
    #     .annotate(Count('proposition__evaluation__joueur', distinct=True)).order_by('-id')
    c = {'reds': reds,
         # 'reds_avant_2016': reds_avant_2016,
         # 'reds_apres_2016': reds_apres_2016,
         'show_add_redico': True,
         'show_profil': True,
         'show_stats': True,
         }
    return render(request, "redicos/index.html", c)

def detail(request, redico_id):
    """
    :
    :param request:
    :param redico_id:
    :return:
    """
    red = Redico.objects.filter(pk=redico_id)[0]
    props = red.les_props()
    nb_joueurs = red.nb_joueurs()
    d1 = {}
    try:
        stats = red.heatmap()
        d1['stats'] = stats
    except:
        pass


    # df_joueursIdEtEvals = red.joueursId_et_evals()['df']
    # heatmap = None # red.heatmap()
    # comb = red.joueurs_comb()['df']
    # if red.nb()['joueurs'] > 1:
    # if df_joueursIdEtEvals.empty == False:
    #     grp = df_joueursIdEtEvals.groupby(['joueur']).mean().to_html
    # else:
    #     grp = None
    # liste_joueurs = red.les_joueurs()['noms']
    # data = red.data()
    # graphs = []
    # for prop in red.les_props()['obj']:
    #     print('===', prop.redico.id, prop.sequence)
    #     graphs.append(prop.heatmap())
    # print('heatmapList: ', heatmapLst)
    # sys.exit()
    # prop = red.les_props()['obj'][0]
    # gr = heatmap2(prop.redico, prop.sequence)
    # print(f'L129 red: {red}')
    d2 = { 'red': red,
          'props': props,
          'redico_id':redico_id,
          'show_profil': True,
          'show_stats': True,
          'show_add_redico': False,
          'show_edit_redico': False,
          'show_supprime_redico': False,
          'show_add_prop': True,
          'show_edit_prop': False,
          'show_supprime_prop': False,
          'show_add_eval': False,
          'show_edit_eval': False,


          }
    c = {**d1, **d2}
          # 'id':  redico_id,
         # 'grp': grp,
         # 'graphs': graphs
    return render(request, "redicos/detail.html", c)

@login_required
def ajout(request):
    red = Redico(createur=request.user)
    # La forme a ete soumise
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        redform = RedicoAjoutEditForm(request.POST, instance=red)
        # Invalid form si user deja inscrit par ex.
        # check whether it's valid:
        if redform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            redform.save()
            return HttpResponseRedirect('/redicos')
    # On a clique sur le lien 'Nouveau redico'
    # if a GET (or any other method) we'll create a blank form
    else:
        # form = NameForm()
        redform = RedicoAjoutEditForm(instance=red) # ??? Unbound form
    return render(request,
                  'redicos/ajout.html',
                  {'form': redform,
                   'red': red})  # 'redico_id':redico_id})

@login_required
@peut_effacer_redico
def supprime(request, redico_id):
    red = get_object_or_404(Redico, id=redico_id)
    context = {'titre': red.titre}
    if request.method == 'POST':
        red.delete()
        messages.success(request, 'Le redico a été supprimé')
        url = reverse('redicos-index')
        return HttpResponseRedirect(url)
    return render(request, 'redicos/supprime.html', context) #HttpResponse(messages)

@login_required
def edit(request, redico_id=None):
    # Redico existe
    if redico_id:
        red = Redico.objects.get(id=redico_id)
        if red.createur != request.user:
            return HttpResponseForbidden()
    # Redico n'existe pas
    else:
        red = Redico(createur=request.user)

    form = RedicoAjoutEditForm(request.POST or None, instance=red)
    # if this is a POST request we need to process the form data
    if request.POST and form.is_valid():
        form.save()
        redirect_url = reverse('redicos-index')
        return redirect(redirect_url)
        # return HttpResponseRedirect('/redicos')
    return render(request, template_name='redicos/edit.html',
            context= {
                    'form': form,
                    'red': red,
                    'redico_id': redico_id,
                    'show_add_redico': False,
                    'show_edit_redico': False,
                    'show_supprime_redico': False,
                    'show_add_prop': False,
                    'show_edit_prop': False,
                    'show_supprime_prop': False,
                    'show_add_eval': False,
                    'show_edit_eval': False,
                    'show_stats' : True
            })

def statsdetail(request, redico_id):
    red = Redico.objects.get(pk=redico_id)
    if red.nb_joueurs() > 1:
        heatmap = red.heatmap()['df']
        print(f'heatmap: {heatmap.to_html()}' )
    c = {'request': request,
         'show_stats': True,
         'redico_id':redico_id,
         'heatmap': heatmap.to_html(),
         'red': red}
    return render(request, "statistiques.html", c)



# La liste des redicos et nombre de propositions


# import numpy
# import numpy.ma as ma
import itertools
# import pandas as pd
from django.db.models import Q


def calcStats(redico_id):
    red = Redico.objects.get(id=redico_id)
    joueurs_list = list(red.les_joueurs())
    joueur_comb = list(itertools.combinations(joueurs_list, 2))
    props_list = list(red.les_props()['obj'].values_list('redico', 'sequence'))
    evals_list = Evaluation.objects.filter(Q(proposition__redico=red) & ~Q(eval=-1))
    evals_list = evals_list.values_list('joueur', 'eval')
    return list(evals_list)


# def calcStats(redico_id):
#
#     props   = Proposition.objects.filter(redico=redico_id)
#     joueurs =redicos Evaluation.objects.filter(proposition__redico=redico_id).values('joueur_id', 'joueur__username').distinct()
#     joueursList = [(joueur["joueur_id"], joueur["joueur__username"]) for joueur in joueurs]
#     propsList = [prop.id for prop in props]
#
#     #print(props)
#     #print(joueurs)
#
#     nbProps      = len(propsList)
#     tableProps   = numpy.zeros(len(propsList), int)  # <---------------------int
#     nbJoueurs    = len(joueursList)
#     tableJoueurs = numpy.zeros(len(joueursList), int) # <---------------------int
#
#     if nbJoueurs < 2: # NbJoueurs = 1 ou 0 (evite les index out of bounds)
#         extraCols=1
#     else:
#         extraCols = numpy.cumsum(range(1, nbJoueurs))[-1]   # Colonnes pour difference
#
#     # Reserver une rangee de plus pour les stats
#     # et une autre pour le nombre de masques
#     extraRan = 0
#     tableEvalsPlusDiff   = numpy.ma.zeros((nbProps+extraRan, nbJoueurs+extraCols), int)
#
#     tableEvalsPlusDiffM  = numpy.ma.masked_less(tableEvalsPlusDiff, 0)
#     #tableEvalsPlusDiffM.fill_value(-1)
#
#     #print(tableEvalsPlusDiff)
#     #print(tableEvalsPlusDiffM)
#
#
#     # for propositions (horz)
#     for idxseq, p in enumerate(propsList):
#         p = Proposition.objects.get(id=p)
#         tableProps[idxseq] = p.sequence
#         # for joueurs (vert)
#         for idxjou, (jid, jnom)  in enumerate(joueursList):        # (0, 2)
#             # j = (2, u'Denis')
#             tableJoueurs[idxjou] = jid
#             try:
#                 e = p.evaluation_set.get(joueur=jid)
#                 tableEvalsPlusDiff[idxseq][idxjou] = e.eval
#                 #print(e, idxseq, idxjou)
#             except Evaluation.DoesNotExist:
#                 tableEvalsPlusDiff[idxseq][idxjou] = -1  # Non /value
#                 #print(e, idxseq, idxjou)
#
#     #print(tableEvalsPlusDiff)
#     tableEvalsPlusDiffM = ma.masked_equal(tableEvalsPlusDiff, -1)
#     #print(tableEvalsPlusDiffM)
#
#
#
#     x = range(nbJoueurs)
#     # z([1, 2, 3]) = [(0,1),(0, 2),(0,3), (1, 2),(1, 3),(2, 3)]
#     # Combinaison de 2 elements pris parmi nj (nombre de joueurs)
#     z  = list(itertools.combinations(x, 2))
#     #print z     # [(0, 1),(0, 2),(1, 2)]
#
#     # Remplir colonnes avec calcul de difference
#     for ic in range(len(z)): #, c in enumerate([0,1]):
#             #tableEvalsDiff[ir][ic] = abs(tableEvals[ir][z[ic][0]] - tableEvals[ir][z[ic][1]])
#redform.createur = request.user
#             colGauche = z[ic][0] # (0, .), (0, .), (1, .)
#             colDroite = z[ic][1] # (., 1), (., 2), (., 2)
#
#             tmp1 = tableEvalsPlusDiffM[:, colGauche]
#             tmp2 = tableEvalsPlusDiffM[:, colDroite]
#             tableEvalsPlusDiffM[:, ic+nbJoueurs] = abs(tmp1-tmp2)
#
#
#     # Pour le calcul des stats, ne pas inclure la derniere rangee
#     # qui est reserve pour le bn de masques ni l'avant derniere
#     # pour la moyenne
#     lstAvg = numpy.ma.average(tableEvalsPlusDiffM, axis=0)
#     nbMask = ma.count_masked(tableEvalsPlusDiffM, axis=0)
#     lstEvals = nbProps - nbMask
#
#
#     # La liste des differences entre joueurs
#
#     lstCouples = []
#     for idx, zz in enumerate(z):
#         j1 = joueurs[zz[0]]["joueur__username"]
#         j2 = joueurs[zz[1]]["joueur__username"]
#         lstCouples.append(j1[:4] + "-" + j2[:4]) # Racourcir les noms pour les tableaux
#         #print(lstCouples)
#
#
#     # Retourner que les stats de la table et les couples
#     return [tableEvalsPlusDiffM[:, -len(z):], lstAvg[-len(z):], lstEvals[-len(z):], lstCouples]

# ####################################

#
#
#
#
# # -*- coding: latin-1 -*-
# from djanginline-block;o.shortcuts import render_to_response
# from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
# from redicos.models import Redico
# from propositions.models import Proposition
# from evaluations.models import Evaluation
# from redicos.forms import RedicoForm
# from django.db.models import Count
# from django.template import RequestContext, loader
# #from redicos.context_processors import redicos_importants
# #from redicos.context_processors import redicos_dynamiques
# from django.contrib.auth.decorators import login_required
# #import pdb;
#
# # Ajout d'un nouveau redico
# @login_required
# def ajout(request):
#     red = Redico(createur=request.user)
#     # La forme a ete soumise
#     if request.method == "POST":
#         redform = RedicoForm(request.POST, instance=red)
#         # Invalid form si user deja inscrit par ex.
#         if redform.is_valid():
#             #redform = redform.save(commit=False)
#             #redform.createur = request.user
#             redform.save()
#             return HttpResponseRedirect('/redicos')
#
#     # On a clique sur le lien 'Nouveau redico'
#     else:
#         redform = RedicoForm(instance=red) # Unbound form
#
#     return render_to_response('redicos/ajout.html',
#                               {'form': redform, 'red':  red }) #'redico_id':redico_id})
# from django.core.exceptions import PermissionDenied
# def edit(request, redico_id=None):
#     if redico_id:
#         red = Redico.objects.get(id=redico_id)
#         if red.createur != request.user:
#             	raise PermissionDenied # raise HttpResponseForbidden()
#     else:
#         red = Redico(createur=request.user)
#
#     #pdb.set_trace()
#     if request.method == "POST":
#         redform = RedicoForm(request.POST, instance=red)
#         # Invalid form si user deja inscrit par ex.
#         if redform.is_valid():
#             #redform = redform.save(commit=False)
#             #redform.createur = request.user
#             redform.save()
#             return HttpResponseRedirect('/redicos')
#     else:
#         redform = RedicoForm(instancen=red) # Unbound form
#
#     return render_to_response('redicos/edit.html',
#                               {'form': redform, 'red':
#                                red, 'redico_id':redico_id})
#
#
# # Les details d'un redico comprennent ses propositions
#
# def detail(request, redico_id, statsdetail=None):
#     #import pdb;
#     #pdb.set_trace()
#     try:
#         red           = Redico.objects.get(pk=redico_id)
#         props         = Proposition.objects.filter(redico=redico_id).order_by('-id')
#         participants  = Evaluation.objects.filter(proposition__redico=redico_id).values('joueur__username').distinct()
#         # stats         = calcStats(redico_id)
#         red_context    = {'red': red,
#                           'props': props,
#                           'participants': participants,                         'stats': stats
#                           }
#     except Redico.DoesNotExist:
#         raise Http404
#     if statsdetail:
#         t = loader.get_template("redicos/statsdetail.html")
#     else:
#     #pdb.set_trace()
#         t = loader.get_template("redicos/detail.html")
#
#     c = RequestContext(request,
#                        red_context,
#                        #[redicos_importants,
#                        # redicos_dynamiques]
#                        )
#     return HttpResponse(t.render(c))
#     #render_to_response('redicos/detail.html',    #                              red_context,     #                              context_instance=RequestContext(request),    #                              )
#
# # La liste des redicos et nombre de propositions
# def index(request):
#     # Liste des redicos et du nombre de propositions
#     # r[0].proposition__count
#     reds   = Redico.objects.all().annotate(Count('proposition',distinct=True)) \
#                                  .annotate(Count('proposition__evaluation__joueur', distinct=True)).order_by('-id')
#     #red_context = { 'reds': reds}
#     t = loader.get_template("redicos/index.html")
#     red_context    = {'reds': reds }
#
#     c = RequestContext(request,
#                        red_context)
#                        #[redicos_importants,
#                        # redicos_dynamiques])
#
#     return HttpResponse(t.render(c))
#     #return render_to_response('redicos/index.html',
#     #                              red_context,
#     #                              context_instance=RequestContext(request))
#

"""
import numpy
import numpy.ma as ma
import itertools


def calcStats(redico_id):

    props   = Proposition.objects.filter(redico=redico_id)
    joueurs = Evaluation.objects.filter(proposition__redico=redico_id).values('joueur_id', 'joueur__username').distinct()
    joueursList = [(joueur["joueur_id"], joueur["joueur__username"]) for joueur in joueurs]
    propsList = [prop.id for prop in props]

    #print(props)
    #print(joueurs)         

    nbProps      = len(propsList)
    tableProps   = numpy.zeros(len(propsList), int)  # <---------------------int
    nbJoueurs    = len(joueursList)
    tableJoueurs = numpy.zeros(len(joueursList), int) # <---------------------int

    if nbJoueurs < 2: # NbJoueurs = 1 ou 0 (evite les index out of bounds)
        extraCols=1
    else:
        extraCols = numpy.cumsum(range(1, nbJoueurs))[-1]   # Colonnes pour difference

    # Reserver une rangee de plus pour les stats
    # et une autre pour le nombre de masques 
    extraRan = 0
    tableEvalsPlusDiff   = numpy.ma.zeros((nbProps+extraRan, nbJoueurs+extraCols), int)

    tableEvalsPlusDiffM  = numpy.ma.masked_less(tableEvalsPlusDiff, 0)
    #tableEvalsPlusDiffM.fill_value(-1)

    #print(tableEvalsPlusDiff)
    #print(tableEvalsPlusDiffM)


    # for propositions (horz)
    for idxseq, p in enumerate(propsList):
        p = Proposition.objects.get(id=p)
        tableProps[idxseq] = p.sequence
        # for joueurs (vert)    
        for idxjou, (jid, jnom)  in enumerate(joueursList):        # (0, 2)
            # j = (2, u'Denis')
            tableJoueurs[idxjou] = jid
            try:
                e = p.evaluation_set.get(joueur=jid)
                tableEvalsPlusDiff[idxseq][idxjou] = e.eval
                #print(e, idxseq, idxjou)
            except Evaluation.DoesNotExist:
                tableEvalsPlusDiff[idxseq][idxjou] = -1  # Non /value
                #print(e, idxseq, idxjou)

    #print(tableEvalsPlusDiff)
    tableEvalsPlusDiffM = ma.masked_equal(tableEvalsPlusDiff, -1)
    #print(tableEvalsPlusDiffM)



    x = range(nbJoueurs)
    # z([1, 2, 3]) = [(0,1),(0, 2),(0,3), (1, 2),(1, 3),(2, 3)]
    # Combinaison de 2 elements pris parmi nj (nombre de joueurs)
    z  = list(itertools.combinations(x, 2))
    #print z     # [(0, 1),(0, 2),(1, 2)]

    # Remplir colonnes avec calcul de difference
    for ic in range(len(z)): #, c in enumerate([0,1]):
            #tableEvalsDiff[ir][ic] = abs(tableEvals[ir][z[ic][0]] - tableEvals[ir][z[ic][1]])

            colGauche = z[ic][0] # (0, .), (0, .), (1, .)
            colDroite = z[ic][1] # (., 1), (., 2), (., 2)

            tmp1 = tableEvalsPlusDiffM[:, colGauche]
            tmp2 = tableEvalsPlusDiffM[:, colDroite]
            tableEvalsPlusDiffM[:, ic+nbJoueurs] = abs(tmp1-tmp2)


    # Pour le calcul des stats, ne pas inclure la derniere rangee 
    # qui est reserve pour le bn de masques ni l'avant derniere 
    # pour la moyenne
    lstAvg = numpy.ma.average(tableEvalsPlusDiffM, axis=0)
    nbMask = ma.count_masked(tableEvalsPlusDiffM, axis=0)
    lstEvals = nbProps - nbMask


    # La liste des differences entre joueurs

    lstCouples = []
    for idx, zz in enumerate(z):
        j1 = joueurs[zz[0]]["joueur__username"]
        j2 = joueurs[zz[1]]["joueur__username"]
        lstCouples.append(j1[:4] + "-" + j2[:4]) # Racourcir les noms pour les tableaux
        #print(lstCouples)


    # Retourner que les stats de la table et les couples
    return [tableEvalsPlusDiffM[:, -len(z):], lstAvg[-len(z):], lstEvals[-len(z):], lstCouples]
"""





