# -*- coding: latin-1 -*-
from django import template
from propositions.models import Proposition
from redicos.models import Redico
register = template.Library()


# Fontion pour tag d'inclusion
# @register.inclusion_tag('redicos/insertion_tags/evalueYN.html')
# Le tag pour inclure ou non, le lien pour Évaluer la proposition
# @register.simple_tag(takes_context=False)
# def evaluerPropYN(red, seq, joueur_id):
#     # htmlAjout = """<img src="/public/site_media/fleche.gif" alt = ""/> <a class ="linkEvaluer" href="/redico/""" + str(red) + """/proposition/""" + str(seq) + """/evaluation/ajout/">Evaluer la prop</a>"""
#     # html =  "evaluerPropYN "
#     # html = """ "/redico/""" + str(red) + """/proposition/""" + str(seq) + """/evaluation/ajout/""""
#     html = f"/redico/{str(red)}/proposition/{str(seq)}/evaluation/ajout/"
#     print(f'evaluation_tags,py fn: evaluerPropYN Ligne q6 - html: {html}')
#     prop = Proposition.objects.get(redico=red, sequence=seq)
#     peut_evaluer = prop.peut_evaluer(joueur_id)
#     print(peut_evaluer)
#     if peut_evaluer:
#         return html
#     else:
#         return ""

from django.utils.safestring import mark_safe

# VOIR PROFIL
@register.simple_tag(takes_context=True)
def peut_voir_son_profil(context):
    request = context['request']
    joueur = request.user

    html = mark_safe(f""" <div> <button class='btn-action'>
                             <i class="fas fa-eye""></i>
                                <a href="/joueur/{ joueur.id }">
                                Votre profil  
                                </a></button> </div> """)
    return html


# VOIR PROFIL
@register.simple_tag(takes_context=True)
def peut_voir_un_profil(context):
    request = context['request']
    createur = context.dicts[5]['joueur'].id
    html = mark_safe(f""" <div> <button class='btn-action'>
                             <i class="fas fa-eye"></i>
                                <a href="/joueur/{ createur }">
                                Voir le profil  
                                </a></button> </div> """)
    return html
# AJOUT REDICO
@register.simple_tag(takes_context=True)
def peut_demarrer_redico(context):

    html = mark_safe(f""" <div> <button class='btn-action'>
                                 <i class="fa fa-plus-square""></i>
                                    <a href="/redico/ajout">
                                    Nouveau redico  </a></button> </div> """)
    return html


# DETAIL DU REDICO
@register.simple_tag(takes_context=True)
def detail_du_redico(context):
    request = context['request']
    redico_Id = context.dicts[5]['red'].id
    html = mark_safe(f""" <div> <button class='btn-action'>
                             <i class="fas fa-eye""></i>
                                <a href="/redico/{ redico_Id}">
                                Détails  
                                </a></button> </div> """)
    return html

# ÉDITER TITRE DU REDICO
@register.simple_tag(takes_context=True)
def peut_editer_titre_redico(context):
    request = context['request']
    redico_Id = context.dicts[5]['red'].id
    # print(f"redico_Id: {redico_Id}")
    joueur = request.user
    red = Redico.objects.get(pk=redico_Id)
    createur = red.createur
    nbProps = red.nb_props()
    # html = mark_safe(f""" <div> <button class='btn-action'>
    #                             <a href="{{% url 'redico-edit' { redico_Id} %}}">
    #                             Éditer le redico</a></button> </div> """)
    html = mark_safe(f""" <div> <button class='btn-action'>
                                <i class="fa fa-edit""></i>
                                <a href="/redico/{ redico_Id }/edit">
                                Éditer</a></button> </div> """)
    if (joueur == createur) and (nbProps < 2):
        return html
    else:
        return ""

# SUPPRIMER REDICO
@register.simple_tag(takes_context=True)
def peut_supprimer_redico(context):
    request = context['request']
    redico_Id = context.dicts[5]['red'].id
    joueur = request.user
    red = Redico.objects.get(pk=redico_Id)
    createur = red.createur
    nbProps = red.nb_props()
    html = mark_safe(f""" <div> <button class='btn-action'
                             <i class="fas fa-trash""

                    <a href="/redico/{ redico_Id}/supprime"> 
                    Supprimer</a></button> </div>  """)

    if joueur == createur and nbProps == 0:
        return html
    else:
        return ""

# DÉTAILS DE LA PROPOSITION (TOUS PEUVENT VOIR)
@register.simple_tag(takes_context=True)
def detail_de_la_proposition(context):
    # request = context['request']
    redico_Id = context.dicts[5]['prop'].redico_id
    sequence_Id = context.dicts[5]['prop'].sequence

    html = mark_safe(f""" <div> <button class='btn-action'>
                                <a href="/redico/{ redico_Id }/proposition/{sequence_Id}">
                                <i class="fas fa-eye""></i>
                                <abbr title="Détail de la propositiin">Détails</abbr></a>
                                </button> </div> """)
    return html

@register.simple_tag(takes_context=True)
def peut_ajouter_proposition_vide(context):
    request = context['request']
    joueur = request.user

    redico_Id =  context.dicts[3]['red'].id
    html = mark_safe(f""" <div><button class="btn-action">
                            <a href="/redico/{redico_Id}/proposition/ajout/">
                            <i class="fa fa-plus-square""></i>     
                            <abbr title="Ajout d'une proposition à ce Redico">Ajout prop</abbr></a>                  
                            </button></div>  """)
    if joueur.is_authenticated:
        return html
    else:
        return ""


# ÉDITER PROP
# S'il est l'auteur de la proposition et que la proposition
# n'est pas encore évaluée, il peut éditer la proposition
# return True
@register.simple_tag(takes_context=True)
def peut_editer_proposition(context):
    request = context['request']
    joueur = request.user
    redico_Id =  context.dicts[5]['prop'].redico_id
    sequence_Id = context.dicts[5]['prop'].sequence
    prop = Proposition.objects.get(redico=redico_Id,sequence=sequence_Id)
    html = mark_safe(f""" <div> <button class="btn-action">
                            <a href="/redico/{redico_Id}/proposition/{sequence_Id}/edit/">
                            <i class="fa fa-edit""></i>
                            
                            Éditer</a></button> </div>  """)
    if joueur == prop.auteur and prop.nb_evaluations() == 0:
        return html
    else:
        return ""

# ÉDITER PROP
# S'il est l'auteur de la proposition et que la proposition
# n'est pas encore évaluée, il peut éditer la proposition
# return True
@register.simple_tag(takes_context=True)
def peut_supprimer_proposition(context):
    request = context['request']
    joueur = request.user
    redico_Id =  context.dicts[5]['prop'].redico_id
    sequence_Id = context.dicts[5]['prop'].sequence
    prop = Proposition.objects.get(redico=redico_Id,sequence=sequence_Id)
    html = mark_safe(f""" <div> <button class="btn-action">
                             <i class="fas fa-trash""></i>
            <a href="/redico/{redico_Id}/proposition/{sequence_Id}/supprime/">
            Effacer</a></button> </div>  """)

    if joueur == prop.auteur and prop.nb_evaluations() == 0:
        return html
    else:
        return ""


# PEUT ÉVALUER LA PROPOSITION
@register.simple_tag(takes_context=True)
def peut_evaluer_proposition(context):
    request = context['request']
    joueur = request.user
    redico_Id =  context.dicts[5]['prop'].redico_id
    sequence_Id = context.dicts[5]['prop'].sequence
    # Ne participe pas ou a déjà évalué
    prop = Proposition.objects.get(redico=redico_Id,sequence=sequence_Id)
    red = Redico.objects.get(pk=redico_Id)

    # Ne participe pas ou a déjà évalué
    les_evaluateurs_id = prop.les_evaluateurs_id()
    a_deja_evalue = joueur.id in les_evaluateurs_id
    participe_au_redico = red.participe_au_redico(joueur.id)
    html = mark_safe(f""" <div> <button class="btn-action">
                             <i class="fa fa-calculator""></i>
                    <a href="/redico/{redico_Id}/proposition/{sequence_Id}/evaluation/ajout/">
                    Évaluer</a></button> </div>  """)
    if (participe_au_redico == True) and (a_deja_evalue == False): # T/F
        return html
    else:
        return ""

@register.simple_tag(takes_context=True)
def peut_editer_eval(context):
    request = context['request']
    joueur = request.user
    redico_Id = context.dicts[5]['prop'].redico_id
    sequence_Id = context.dicts[5]['prop'].sequence

    prop = Proposition.objects.get(redico=redico_Id, sequence=sequence_Id)
    red = Redico.objects.get(pk=redico_Id)
    participe_au_redico = red.participe_au_redico(joueur.id)
    peut_editer_eval = participe_au_redico and \
                       joueur.id in prop.les_evaluateurs_id()
    html = mark_safe(f""" <div> <button class="btn-action">
                             <i class="fa fa-edit""></i>
                        <a href="/redico/{redico_Id}/proposition/{sequence_Id}/evaluation/edit/">
                        Modif éval</a></button> </div>  """)
    # print(peut_editer_eval)
    if peut_editer_eval:
        return html
    else:
        return ""



# ÉVALUER LA PROPOSITION
# @register.simple_tag(takes_context=True)
# def peut_evaluer_prop(context, red, seq):
#     request = context['request']
#     joueur =
# {# /ICONE SUPPRIMER LA PROPOSITION #}
#
# {# ======================================================================== #}
# {# ICONE ÉVALUER PROPOSITION #} request.user
#     prop = Proposition.objects.get(redico=red, sequence=seq)
#     peut_evaluer = prop.peut_evaluer(joueur)
#     print(peut_evaluer)
#     if peut_evaluer:
#         return True
#     else:
#         return False




# Le tag pour inclure ou non, le lien pour Éditer l'evaluation
# @register.simple_tag(takes_context=False)
# def editerEvalYN(red, seq, joueur_id):
#     # htmlEdit = """<a class ="linkEditer" href="/redico/""" + str(red) + """/proposition/""" + str(seq) + """/evaluation/edit/">Modifier votre évaluation</a>"""
#     # html =       """ "/redico/""" + \
#     #              str(red) + """/proposition/""" + \
#     #              str(seq) + \
#     #              """/evaluation/edit/" """
#     html = f"/redico/{str(red)}/proposition/{str(seq)}/evaluation/edit/"
#     # html =  "editerEvalYN "
#     # print('red: {:d} seq: {:d}'.format(red, seq))
#     print(f'evaluation_tags,py fn:editerEvalYN Ligne 35 - html: {html}')
#     prop = Proposition.objects.get(redico=red, sequence=seq)
#     peut_editer_eval = prop.peut_editer_eval(joueur_id)
#     if peut_editer_eval:
#         return True
#     else:
#         return False
# ÉDITER ÉVALUATION



