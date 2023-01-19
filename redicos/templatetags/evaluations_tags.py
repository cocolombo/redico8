# -*- coding: latin-1 -*-

from django import template
from joueurs.models import Joueur
from django.utils.safestring import mark_safe
import inspect
from propositions.models import Proposition
from redicos.models import Redico
from evaluations.models import Evaluation

# from global_fn.global_fn import get_Redico, get_proposition
register = template.Library()
# usager =        """<i class="fa fa-user" aria-hidden="true" title="Votre profil usager"></i>"""
# right_arrow =   """<i class="fa fa-arrow-circle-right" aria-hidden="true" title="Nouveau redico"></i>"""
# eye =           """<i class="fas fa-eye" aria-hidden="true" title="Details"></i>"""
# edit =          """<i class="fa fa-pencil-square-o" aria-hidden="true" title="Éditer"></i>"""
# editEval =      """<i class="fa fa-pencil-square-o" aria-hidden="true" title="Éditer évaluation"></i>"""
# editRedico =    """<i class="fa fa-pencil-square-o" aria-hidden="true" title="Éditer le titre du Reddico"></i>"""
# editProp =      """<i class="fa fa-pencil-square-o" aria-hidden="true" title="Éditer la proposition"></i>"""
# poubelle_redico =      """<i class="fa fa-trash" aria-hidden="true" title="Supprimer ce redico"></i>"""
# poubelle_proposition =      """<i class="fa fa-trash" aria-hidden="true" title="Supprimer cette proposition"></i>"""


usager =                """ <i class="fas fa-user"                title="Votre profil usager"></i> """
right_arrow =           """ <i class="fas fa-arrow-circle-right"  title="Nouveau redico"></i> """
eye =                   """ <i class="fas fa-eye"                 title="Details"></i> """
edit =                  """ <i class="fas fa-pencil-square-o"     title="Éditer"></i> """
editEval =              """ <i class="fa-solid  fa-calculator"    title="Évaluer la proposition"></i>"""
editRedico =            """ <i class="fas fa-pencil-square-o"     title="Éditer le titre du Reddico"></i> """
editProp =              """ <i class="fas fa-pencil-square-o"     title="Éditer la proposition"></i> """
poubelle_redico =       """ <i class="fa-solid fa-trash-can"      title="Supprimer ce redico"></i> """
poubelle_proposition =  """ <i class="fa-solid fa-trash-can"      title="Supprimer cette proposition"></i> """
# loupe =         """<i class="fa-solid fa-folder-magnifying-glass" aria-hidden="true" title="Détails du redico"></i>"""
loupe_redico =  """<i class="fa-solid fa-magnifying-glass"        title='Détails du redico'></i>"""
loupe_profil =  """<i class="fa-solid fa-magnifying-glass"        title='Vor le profil'></i>"""
loupe_proposition =  """<i class="fa-solid fa-magnifying-glass" title='Détails de cette proposition'></i>"""
pluspprop =              """<i class="fa-solid fa-plus"           title="Ajout d'une proposition"></i>"""
calculateur =           """<i class="fa-solid  fa-calculator"     title="Évaluer la proposition"></i>"""

btn_open = """ <li class="actions"> <button class="btn-action  btn-link "> """
btn_close = """ </button>  </li>  """
messages_open = """ <p class="alert alert-success"> """
messages_close = """ </p> """
# REDICO

# Sur la page redico-details.html
@register.filter
def meter_val(val) -> str:
    """
    Curseau pour afficher la valeur d'une évaluation en pourcentage
    """
    html = mark_safe(f""" <meter  value={val} min="0" max="100" >{val}</meter> """)
    return html

from joueurs.models import UserProfile
# M'avetir si quelqu'un fait une proposition
@register.simple_tag(takes_context=True)
def courrielOK(context):
    u = context.request.user
    if not u.is_authenticated:
        return ""
    else:
        profile = UserProfile.objects.get(user=u)
        html_OUI = mark_safe(f""" {btn_open} (Notification courriel OUI {btn_close} """)
        html_NON = mark_safe(f""" {btn_open} (Notification courriel NON {btn_close} """)
        return html_NON if u.profile.courrielOK  else html_OUI



# LISTE DES MESSAGES
@register.simple_tag(takes_context=True)
def message_comment_participer(context, red: Redico)-> str:
    html_logue      = mark_safe(f""" {messages_open}Vous ne participez pas encore à ce Redico. Pour y participer et pouvoir 
                                    évaluer les propositions, il faut tout d'abord faire une proposition)  {messages_close} """)
    html_non_logue  = mark_safe(f""" {messages_open}Vous ne participez pas encore à ce Redico. Pour y participer et pouvoir 
                                    évaluer les propositions, il faut tout d'abord vous loguer et ensuite faire une proposition)  {messages_close} """)

    joueur = context.request.user
    # Participe = Ceux qui ont fait au moins une proposition
    # red.participe_a_ce_redico(joueur) vétifie si le joueur est logué
    participe_au_redico = red.participe_a_ce_redico(joueur) == True
    if   participe_au_redico:
        return ""
    elif not joueur.is_authenticated:
        return html_non_logue
    else:
        return html_logue

@ register.simple_tag(takes_context=True)
def trop_de_props_consecutives(context, red: Redico) -> str:
    """
    Authentication vérifiée par la template redico-details.html
    s'il arrive ici, il est logué
    """
    # prop = Proposition.objects.filter(redico=red, sequence=red.max_sequence() - 1)
    html_trop_de_props_consecutives = mark_safe(f""" {messages_open}
                                Vous dépassez le maximum de 5 propositions consécutives suggéré  {messages_close} """)
    joueur = Joueur.objects.get(pk=context.request.user.id)
    if joueur.trop_de_props_consecutives(red):
        return html_trop_de_props_consecutives
    else:
        fn_name = inspect.stack()[0][3]
        return ""

@ register.simple_tag()
def info_ajout_prop() -> str:
    """
    Message: N'oubliez pas d'évaluer toutes ....
    """
    # prop = Proposition.objects.filter(redico=red, sequence=red.max_sequence() - 1)
    html_info = mark_safe(f"""  {messages_open}
                                N'oubliez pas d'évaluer toutes les propositions en suspends. <br></brp>
                                Le champ texte est obligatoire les autres sont facultatifs
                                {messages_close} """)
    return html_info


@register.simple_tag(takes_context=True)
def voir_details_du_redico(context, red: Redico) -> str:
    """
    Accès pour tous logué ou non à la page de détails du redico
    """
    html = mark_safe(f"""   {btn_open} 
                            <a href="/redico/{red.id}">  
                            {eye} Détails du redico</a> 
                            {btn_close}""")
    return html

@register.simple_tag(takes_context=True)
def editer_titre_redico(context, red: Redico) -> str:
    """
    En référence au fichier redico_details.html
    """

    # usager logué
    # joueur = Joueur.objects.get(pk=context.request.user.id)
    html = mark_safe(f"""   {btn_open}  
                            <a href="/redico/{red.id}/edit"> 
                            {editRedico} Éditer le titre du Redico</a>  
                            {btn_close} """)
    # Autorisé à éditer le titre du redico ?
    if red.peut_editer_titre(context.request.user):
        return html
    # Non autorisé à éditer le titre du redico
    else:
        return ""
                                    #fn_name = inspect.stack()[0][3]
                                    #mark_safe(f"<li class="actions"> {fn_name} </li>")

@register.simple_tag(takes_context=True)
def supprimer_redico(context, red: Redico) -> str:
    """
    Authentication férifiée pas la fonction red.peut_supprimer_redico(joueur)
    En référence au fichier redico_details.html
    """
    # usager non logué
    joueur = Joueur.objects.get(pk=context.request.user.id)
    html = mark_safe(f"""   {btn_open}  
                            <a href="/redico/{red.id}/supprime">  
                            {poubelle_redico} Supprimer ce Redico</a>  
                            {btn_close} """)
    # Autorisé à éditer le titre du redico ?
    if red.peut_supprimer_redico(joueur):
        return html
    else:
        return ""

# JOUEUR

# @register.simple_tag(takes_context=True)
# def voir_le_profil(context, profil_id) -> str:
#     html = mark_safe(f""" {btn_open}
#                          <a href="/joueur/{ profil_id }">
#                          {usager} Vor ce profil</a>
#                          {btn_close} """)
#     return html


# PROPOSITIONS
@register.simple_tag(takes_context=True)
def ajouter_proposition(context, red: Redico) -> str: # ???
    """
    Authentication vérifiée par la template redico-details.html
    s'il arrive ici, il est logué
    """
    joueur = Joueur.objects.get(pk=context.request.user.id)
    # Autorisé à ajouter une proposition ?
    if red.peut_ajouter_proposition(joueur):
        return mark_safe(f"""   {btn_open}   
                                </i> <a href="/redico/{red.id}/proposition/ajout/">  
                                {pluspprop} Ajouter prop </a>  
                                {btn_close} """)
    else:
        return ""

@register.simple_tag(takes_context=True)
def editer_proposition(context, prop: Proposition) -> str:
    """
    Authentication vérifiée par la fonction prop.peut_editer_proposition(joueur)
    """
    joueur = context.request.user
    # Autorisé à éditer la proposition ?
    if prop.peut_editer_proposition(joueur):
        return  mark_safe(f"""  {btn_open}  
                                <a href="/redico/{prop.redico.id}/proposition/{prop.sequence}/edit/">  
                                {editProp} Éditer prop</a>   
                                {btn_close}""")
    else:
        return ""

# DÉTAILS DE LA PROPOSITION (TOUS PEUVENT VOIR)
# @register.simple_tag(takes_context=True)
# def details_de_la_proposition(context, red: Redico, prop: Proposition) -> str:
#     # joueur = Joueur.objects.get(pk=context.request.user.id)
#     joueur = context.request.user
#     # request = context['request']
#     html = mark_safe(f""" <li class="actions"> {btn_open}
#                             <a href="/redico/{ red.id }/proposition/{prop.sequence}">
#                            { loupe_proposition }Détails de la proposition</a>
#                            {btn_close} </li> """)
#     if joueur.peut_voir_detail_de_la_proposition(prop):
#         return html
#     else:
#         fn_name = inspect.stack()[0][3]
#         return "" #mark_safe(f"<li class="actions"> {fn_name} </li>")

@register.simple_tag(takes_context=True)
def supprimer_proposition(context, prop : Proposition) -> str:
    """

    """
    # usager non logué
    joueur = Joueur.objects.get(pk=context.request.user.id)
    html = mark_safe(f"""   {btn_open}  
                            <a href="/redico/{prop.redico.id}/proposition/{prop.sequence}/supprime/">  
                            {poubelle_proposition} Supprimer prop</a>  
                            {btn_close}""")
    # Autorisé à supprimer la proposition ?
    if prop.peut_supprimer_proposition(joueur):
        return html
    else:
        return ""

# EVALUATION
@register.simple_tag(takes_context=True)
def evaluer_la_proposition(context, prop: Proposition) -> str:
    """
    En référence au fichier proposition_details.html
    """
    # joueur = Joueur.objects.get(pk=context.request.user.id)
    # Autorisé à évaluer la proposition ?
    if prop.peut_evaluer_proposition(context.request.user):
       return mark_safe(f"""    {btn_open}  
                                <a href="/redico/{prop.redico.id}/proposition/{prop.sequence}/evaluation/ajout/">  
                                Évaluer prop</a> 
                                {btn_close} """)
    else:
        return ""

@register.simple_tag(takes_context=True)
def aveccommentaire(context, eval: Evaluation) -> str:
    prop = eval.proposition
    redico_id = prop.redico.id
    sequence_id = prop.sequence
    auteur_id = eval.auteur.id

    if eval.commentaire:
        commentaire = eval.commentaire[:25] + "... "
        return mark_safe(f""" <li class="actions">
                                <a title="{eval.commentaire}"
                                href="/redico/{redico_id}/proposition/{sequence_id}/evaluation/{auteur_id}/details/">
                                ({commentaire})</a>
                                {btn_close} """)
    # {  # <a title="{{ e.commentaire }}"#}
    # {  # href="{% url "proposition-details" red.id prop.sequence %}">#}
    # {  # <b><i>(*)</i></b></a>#}
    return ""


@ register.simple_tag(takes_context=True)
def modifier_son_eval(context, prop: Proposition, eval: Evaluation) -> str:
    """
    Authentication vérifiée dans prop.peut_modifier_son_eval(joueur)
    Voir aussi le fichier proposition_details.html
    Sur sa ligne d'évaluation afficher le bouton pour modifier son evaluation
    """
    # Autorisé à éditer l'évaluation ?
    if prop.peut_modifier_son_eval(context.request.user, eval):
        return mark_safe(f"""   {btn_open} 
                                <a href="/redico/{prop.redico.id}/proposition/{prop.sequence}/evaluation/edit/">  
                                Modifier éval</a> 
                                {btn_close} """)
    else:
        return ""

"""
@ register.simple_tag(takes_context=True)
def chatter(context, red: Redico) -> str:
    "
    Authentication vérifiée par la template redico-details.html
    s'il arrive ici, il est logué
    "
    html = mark_safe(f"   {btn_open}
                            <a href="/redico/{red.id}/chatter/">
                            {chat_redico}
                            </a>
                            {btn_close})
    joueur = Joueur.objects.get(pk=context.request.user.id)
    # Autorisé à chatter ?
    if red.peut_chatter(joueur):
        return html
    else:
        fn_name = inspect.stack()[0][3]
        return ""
"""


############################################################################
# Barre de navigation

@register.simple_tag(takes_context=True)
def navjoueurs(context) -> str:
    """
    Liste des joueurs
    """
    html = """   <li class="nav-item btn-action">  <a class="nav-link active" href="/joueurs">Joueurs</a> </li> """
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def navredicos(context) -> str:
    """
    Liste des redicos
    """
    html = """    <li class="nav-item  btn-action">  <a class="nav-link active" href="/redicos">Redicos</a> </li>  """
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def navloguer(context) -> str:
    """
    Se loguer
    """
    user = context.request.user
    if user.is_authenticated:
        html = ""
    else:
        html = """  <li class="nav-item  btn-action"> <a class="nav-link"  href="/accounts/login">Se loguer</a> </li>  """
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def navdeloguer(context) -> str:
    """
    Se déloguer
    """
    user = context.request.user
    if user.is_authenticated:
        html = """  <li class="nav-item  btn-action"> <a class="nav-link" href="/accounts/logout">Se déloguer</a> </li>  """
    else:
        html = ""
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def navsenregistrer(context) -> str:
    """
    S'enregistrer
    """
    user = context.request.user
    if user.is_authenticated:
        html = ""
    else:
        html = """  <li class="nav-item  btn-action"> <a class="nav-link"  href="/accounts/register">S'enregistrer</a> </li>  """
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def navchangermdp(context) -> str:
    """
    Changer son mot de passe
    """
    user = context.request.user
    if user.is_authenticated:
        html = """  <li class="nav-item  btn-action"> <a class="nav-link"  href="/accounts/password/change">Changer votre mdp</a> </li>  """
    else:
        html = ""
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def navvotreprofil(context) -> str:
    """
    Consulter son profil
    """
    user = context.request.user
    if user.is_authenticated:
        html = f"""  <li class="nav-item  btn-action"> <a class="nav-link"  href="/joueur/{user.id}">Votre profil</a> </li>  """
    else:
        html = ""
    return mark_safe(html)


# AJOUT REDICO
@register.simple_tag(takes_context=True)
def navdemarrerredico(context) -> str:
    """
    Démarrer un nouveau redico
    """
    user = context.request.user
    if user.is_authenticated:
        html = """ `<li class="nav-item  btn-action"> <a class="nav-link"  href="/redico/ajout">Démarrer un redico</a> </li>  """
    else:
        fn_name = inspect.stack()[0][3]
        html = "" #mark_safe(f"<li class="actions"> {fn_name} </li>")
    return mark_safe(html)




