from django.shortcuts import render
from propositions.models import Proposition
from redicos.models import Redico
# from django.db.models import Count
from propositions.forms import PropositionAjoutEditForm
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Max
# from heatmap.views import heatmap
from django.views.generic import CreateView, DeleteView
from django.contrib import messages
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
import re
# Create your views here.

# from .decorator import must_bmesuree_yours


def show_actions():
    show_profil = {'show_profil': True}

    show_add_redico = {'show_add_redico': False}
    show_edit_redic = {'show_edit_redico': False}

    show_add_prop = {'show_add_prop': False}
    show_edit_prop = {'show_edit_prop': False}

    show_add_eval = {'show_add_eval': False}
    show_edit_eval = {'show_edit_eval': False}


# Bloc actions
def actions_index():
    return { 'show_profil'    : True,
             'show_add_redico': True }

def actions_detail():
    return { 'show_profil     ': True,
             'show_add_redico' : True,
             'show_add_prop'   : False }

# Colonne Actions dans redico.detail.html
def actions_props():
    return { 'show_edit_prop'  : False,
             'show_add_eval'   : False,
             'show_edit_eval'  : False
             }






# SUPPRIMER LA PROPOSITION
# redico.detail.py ligne 75
# Icone ans colonnes actions
@login_required
def supprimeProp(request, redico_id, sequence_id):
    # La validation est faite dans evaluations_tags.peut_supprimer_proposition
    # red = Redico.objects.get(id=redico_id)
    prop   = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
    # is_auteur = request.user == prop.auteur
    # zero_evals = prop.nb_evals() == 0
    # if is_auteur and zero_evals:
    prop.delete()
    messages.success(request, f'La proposition {prop.sequence} du redico {prop.redico} a été supprimée')
    return redirect('redicos-index')
    # else:
    #     messages.success(request, f"Vous n'êtes pas autorisé à faire cette opération")
    #     return redirect('redicos-index')

@login_required
def ajoutProp(request, redico_id):
    prop = Proposition(auteur=request.user) #, redico=redico_id)
    # next_seq_id = Redico.objects.get(id=redico_id).nb()['props'] + 1 # 2017-11-20
    red = Redico.objects.get(pk=redico_id)

    try:
        next_seq_id = Proposition.objects.filter(redico_id=redico_id).aggregate(Max('sequence'))['sequence__max'] + 1
    # Cas nouveau redico avec 0 proposition
    except:
        next_seq_id = 1
    if request.POST:
        form = PropositionAjoutEditForm(request.POST) #  or None, instance=prop)
        if form.is_valid():
            f = form.save(commit=False)
            f.redico      = red
            f.auteur      = request.user
            f.sequence    = next_seq_id
            f.date_de_pub = datetime.today()
            f.save()
            url = reverse('redico-detail', kwargs={'redico_id':redico_id})
            return HttpResponseRedirect(url)
        # return redirect('post_detail', pk=post.pk)
    else:
        form = PropositionAjoutEditForm()
    return render(request, template_name='propositions/ajout.html',
                  context={'form': form,
                            'prop':prop,
                            'red':red}) # Traiter le cas ou c'est la premiere proposition du redico
                   # 'sequence_id':sequence_id} )


@login_required
def editProp(request, redico_id, sequence_id=None):
    # Proposition existe, on l'edite (sequence reste identique)
    prop   = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
    #print('Proposition existe: ', prop.sequence)
    next_seq_id = sequence_id
    if prop.auteur != request.user:
        return HttpResponseForbidden()
    # Proposition n'existe pas on en cree une nouvelle (incrementer sequence)
    red = Redico.objects.get(pk=redico_id)
    if request.POST:
        form = PropositionAjoutEditForm(request.POST or None, instance=prop)
        if form.is_valid():
            #print('POST')
            # red = Redico.objects.get(pk=redico_id)
            f = form.save(commit=False)
            # prop_count    = Proposition.objects.filter(redico=redico_id).aggregate(Count('sequence'))
            f.redico      = red
            # Traiter le cas ou c'est la premiere proposition du redico
            # try:
            # next_seq_id = max(Proposition.objects.filter(redico=red).values_list('sequence', flat=True)) + 1
            # except:
            #     next_seq_id = 1
            f.auteur      = request.user
            f.sequence    = next_seq_id
            f.date_de_pub = datetime.today()
            f.save()
            url = reverse('redico-detail', kwargs={'redico_id':redico_id})
            return HttpResponseRedirect(url)
    else:
        form = PropositionAjoutEditForm(instance=prop)
        return render(request, template_name='propositions/edit.html',
                      context={'form': form,
                       'prop':prop,
                       'redico_id':redico_id,        # Traiter le cas ou c'est la premiere proposition du redico
                       'redico':red,
                       'sequence_id':sequence_id,
                       'extra': 'Éditez votre proposition' } )


@login_required
def edit2(request, redico_id, sequence_id=None, template_name='propositions/edit.html'):
    # Proposition existe, on l'edite (sequence reste identique)
    if sequence_id and redico_id:
        prop   = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
        #print('Proposition existe: ', prop.sequence)
        next_seq_id = sequence_id
        if prop.auteur != request.user:
            return HttpResponseForbidden()
    # Proposition n'existe pas on en cree une nouvelle (incrementer sequence)
    else: #from django.shortcuts import render

# Create your views here.
        prop = Proposition(auteur=request.user) #, redico=redico_id)
        # next_seq_id = Redico.objects.get(id=redico_id).nb()['props'] + 1 # 2017-11-20
        try:
            next_seq_id = Proposition.objects.filter(redico_id=redico_id).aggregate(Max('sequence'))['sequence__max'] + 1
        # Cas nouveau redico avec 0 proposition
        except:
            next_seq_id = 1
        #print('Proposition existe pas: ', prop.sequence)
    # Forme
    form = PropositionAjoutEditForm(request.POST or None, instance=prop)
    if request.POST and form.is_valid():
        #print('POST')
        red = Redico.objects.get(pk=redico_id)
        f = form.save(commit=False)
        # prop_count    = Proposition.objects.filter(redico=redico_id).aggregate(Count('sequence'))
        f.redico      = red
        # Traiter le cas ou c'est la premiere proposition du redico
        # try:
        # next_seq_id = max(Proposition.objects.filter(redico=red).values_list('sequence', flat=True)) + 1
        # except:
        #     next_seq_id = 1
        f.auteur      = request.user
        f.sequence    = next_seq_id
        f.date_de_pub = datetime.today()
        f.save()
        url = reverse('redico-detail', kwargs={'redico_id':redico_id})
        return HttpResponseRedirect(url)
    return render(request, template_name,
                  {'form': form,
                   'prop':prop,
                   'redico_id':redico_id,        # Traiter le cas ou c'est la premiere proposition du redico

                   'sequence_id':sequence_id} )

def detail(request, redico_id, sequence_id):
    #Trouver le pk a partir de redico_id et sequence_id
    prop_id = Proposition.objects.get(redico=redico_id, sequence=sequence_id)
    red     = Redico.objects.get(pk=redico_id)
    prop    = Proposition.objects.get(id=prop_id.id)
    # evals   = prop.les_evaluations()['les_evaluations']   # ev   = Evaluation.objects.filter(proposition=prop_id)
    avg     = prop.moyenne_des_evals() # avg  = Evaluation.objects.filter(proposition=prop_id).aggregate(Avg('eval'))
    # heatmap = prop.heatmap2()
    # if prop.les_evaluateurs()['cnt'] > 1:
    #     heatmap = prop.heatmap2()
    c = {'request': request,
         'red': red,
         'prop': prop,
         # 'evals': evals,
         'avg': avg,
         'redico_id':redico_id,
         'sequence_id': sequence_id,
         'show_add_redico' : False,
         'show_add_prop'   : False,
         'show_add_eval'   : True,
         'show_edit_redico': False,
         'show_edit_prop'  : False,
         'show_edit_eval'  : False
         # 'heatmap':heatmap
         }

    return render(request, "propositions/detail.html", c )

# redico/1/propositions
def index(request, redico_id):
    # props = Proposition.objects.filter(redico=redico_id)
    red   = Redico.objects.get(pk=redico_id)
    props = red.les_propositions()
    props = props.order_by('-id')
    c = {'request': request,
         'props':props,
         'red':red}
    return render(request, "propositions/index.html", c)


#
# class AjoutView(CreateView):
#     model = Proposition
#     # fields = ['titre']
#     # fields = '__all__'
#     template_name = 'propositions/ajout.html'
#     form_class = PropositionForm
#
#     # def __init__(self, *args, **kwargs):
#     #     # print('self.user', self.user)
#     #     print('self', self)
#     #     print('kwargs', kwargs)
#     #     # self.user = kwargs.pop('user')
#     #     super(PropositionForm, self).__init__(*args, **kwargs)
#
#
#     # @method_decorator(login_required)prop_sequence
#     # def dispatch(self, *args, **kwargs):
#     #     return super().dispatch(*args, **kwargs)
#
#     def get_form_kwargs(self, *args, **kwargs):
#         form_kwargs = super(AjoutView, self).get_form_kwargs(*args, **kwargs)
#     #     form_kwargs['sequence'] = 9999 #self.sequenceId()
#     #     print('self.user.id', self.request.user.id)
#     #     print('form_kwargs', form_kwargs)
#     #     # form_kwargs['sequence_id'] = self.sequenceId()
#
#         return form_kwargs
#
#     def form_valid(self, form):
#         print(self.request)
#
#         # form = form.save(commit=False)
#         form.instance.auteur = self.request.user
#         form.instance.redico = Redico.objects.get(id=self.get_redicoId()) #get_redicoId()
#         form.instance.sequence = self.sequenceId()
#         # print(form)
#         # form.save()
#         return super(AjoutView, self).form_valid(form)
#

#
#
#
#
#
#
#
#     # def get_form_kwargs(self, *args, **kwargs):
#     #     form_kwargs = super(AjoutView, self).get_form_kwargs(*args, **kwargs)
#     #     form_kwargs['sequence_id'] = self.sequenceId()
#     #     return form_kwargs
#

# redico/1/propositions/1/
# Les details d'une proposition comportent ses evaluations