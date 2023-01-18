from django.shortcuts import render

# Create your views here.
# -*- coding: latin-1 -*-
# Create your views here.
# from django.shortcuts import render
from evaluations.models import Evaluation
from propositions.models import Proposition
from redicos.models import Redico
# from django.db.models import Count
from evaluations.forms import EvaluationAjoutEditForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.template import RequestContext
# from django.template import Context, Template
from django.shortcuts import render

# from django.views.generic.simple import direct_to_template


# (r'^redico/(?P<redico_id>\d+)/proposition/(?P<proposition_id>\d+)/evaluations/ajout/$',
#                                                'redico.evaluation.views.ajout'),
# redico/1/proposition/1/evlauations/ajout
# Model Evaluation:
#    proposition
#    redico
#    joueur
#    commentaire
#    eval
#    date-eval


from django.contrib.auth.decorators import login_required


# redico/1/proposition/1/evaluations/ajout
# (r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/evaluation/ajout/$',
#                                           'redico.evaluations.views.ajout'),
@login_required
def ajout(request, redico_id, sequence_id):
    prop = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
    red = Redico.objects.get(pk=redico_id)  # joueur = User.objects.get(pk=request.user.id)  #evals = prop.evaluation_set.all()
    e = Evaluation(proposition=prop, joueur=request.user)
    # la forme est soumise
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = EvaluationAjoutEditForm(request.POST, instance=e)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            evalform = form.save(commit=False)
            evalform.proposition = prop  # evalform.redico = red
            evalform.redico = redico_id  # evalform.joueur = joueur
            evalform.joueur = request.user  # pdb.set_trace()
            evalform.save()
            return HttpResponseRedirect('/redico/%s/' % redico_id)
    # On arrive ici en provenance du lien "Evaluer"
    # if a GET (or any other method) we'll create a blank form
    else:
        # form = NameForm()
        form = EvaluationAjoutEditForm(instance=e)  # ???
    return render(request,
                  'evaluations/ajout.html',
                  {'form': form,
                   'prop': prop,
                   'red': red,
                   'e': e})


@login_required
def edit(request, redico_id, sequence_id):
    prop = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
    red = Redico.objects.get(pk=redico_id)
    joueur = User.objects.get(pk=request.user.id)
    eval = Evaluation.objects.get(proposition__redico=redico_id, proposition__sequence=sequence_id, joueur=joueur.id)

    # create a form instance and populate it with data from the request:
    if request.method == 'POST':
        evalform = EvaluationAjoutEditForm(request.POST, instance=eval)
        # check whether it's valid:
        if evalform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            eval.nb_edit += 1
            # print(eval.nb_edit)
            evalform.save()
            return HttpResponseRedirect('/redico/%s/' % redico_id)
    # if a GET (or any other method) we'll create a blank form
    else:
        # form = NameForm()
        evalform = EvaluationAjoutEditForm(instance=eval)  # ???

    return render(request,
                  'evaluations/edit.html',
                  {'form': evalform,
                   'prop': prop,
                   'red': red,
                   'joueur': joueur,
                   'eval': eval})


def detail(request, evaluation_id):
    try:
        e = Evaluation.objects.get(pk=evaluation_id)

    except Evaluation.DoesNotExist:
        raise Http404

    e_context = {'e': e}

    return render(request, 'evaluations/detail.html',
                  context=e_context)
    # context_instance=RequestContext(request))


def index(request):
    eval_list = Evaluation.objects.all()
    e_context = {'eval_list': eval_list}

    return render(request, 'evaluations/detail.html',
                  e_context,
                  context_instance=RequestContext(request))
