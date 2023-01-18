from propositions.models import Proposition
from evaluations.models import Evaluation
from redicos.models import Redico
from django.db.models import Count
import json

nb_Items = 5
def redicos_importants(request):
    redicos_importants = Proposition.objects.all().values('redico__id', 'redico__titre').annotate(cnt=Count('redico')).order_by('-cnt')[:nb_Items]
    return { 'redicos_importants': redicos_importants, }
def redicos_dynamiques(request):
    redicos_dynamiques = Proposition.objects.all().values('redico__id', 'redico__titre').annotate(cnt=Count('redico')).order_by('-cnt')[:nb_Items]
    return {'redicos_dynamiques': redicos_dynamiques, }
def dern_props(request):
    dernieres_props = Proposition.objects.all().values('texte', 'redico__id', 'sequence', 'auteur__id', 'auteur__username').order_by('-id')[:nb_Items]
    return {'dern_props': dernieres_props, }
def dern_evals(request):
    dernieres_evals = Evaluation.objects.all().values('proposition__sequence',
                                                      'proposition__redico__id',
                                                      'proposition__texte',
                                                      'joueur__username',
                                                      'eval').order_by('-id')[:nb_Items]
    return {'dern_evals': dernieres_evals, }
def joueurs_actifs(request):
    joueurs_actifs = Evaluation.objects.all().values('joueur__username', 'joueur__id').annotate(cnt=Count('joueur')).order_by('-cnt')[:nb_Items]
    return {'joueurs_actifs': joueurs_actifs,}



def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        # '{method} HTTP/1.1\n'
        # 'Content-Length: {content_length}\n'
        # 'Content-Type: {content_type}\n'
        # '{headers}\n\n'
        '{body}'
    ).format(
        # method=request.method,
        # content_length=request.META['CONTENT_LENGTH'],
        # content_type=request.META['CONTENT_TYPE'],
        # headers=headers,
        body=request.body,
    )

# def is_auteur_du_redico(request):
#     redico_id = get_redicoId(request)['id']
#     if redico_id == -1:
#         return {'result': False}
#     else:
#         red = Redico.objects.get(pk=redico_id)
#     if red.createur == request.user:
#         return {'result': True }
#     else:
#         return {'result': False}

# def is_auteur_de_la_prop(request):
#     pass
#
# def est_auteur_du_redico(request):
#     pass
#
# def nb_props_redico(request):
#     pass
#
# def participe_au_redico(request):
#     pass

# def liste_des_joueurs(request, redico_id):
#     red = Redico.objects.get(id=redico_id)
#     return { 'liste_des_joueurs': red.les_joueurs() }


# def listeRedicos(request):
#     # def index():
#     # Liste des redicos et du nombre de propositions
#     # r[0].proposition__count
#     reds = Redico.objects.filter(actif=True) \
#         .annotate(Count('proposition', distinct=True)) \
#         .annotate(Count('proposition__evaluation__joueur',
#                         distinct=True)).order_by('-id')
#     # reds = Redico.objects.all().annotate(Count('proposition', distinct=True)).annotate(Count('proposition__evaluation__joueur', distinct=True)).order_by('-id')
#     return {'reds': reds}

"""
from redicos.context_processors import listeRedicos
from redicos.models import Redico
r = Redico.objects.get(pk=55)
redicos = listeRedicos(r)

for r in redicos['reds']:
    print(r.createur) 


"""
import re
# # (.*redico\/)(\d*)(\/proposition\/)(\d*)
# # (.*redico\/)(\d*)(\/.*\/)?(\d+)?
# def get_redicoId(request):
#     url = request.get_full_path()
#     print(f'url: {url}')
#     redico_id = re.match(".*redico\/(\d*)", url)
#     print(f'redico_id: {redico_id}')
#     if redico_id is None:
#         print(f'redico_id: {redico_id}')
#         return {'Id': 0 }
#     else:
#         print(f'redico_id.group(1): {redico_id.group(1)}')
#         print(f'redico_id.group(0): {redico_id.group(0)}')
#         return {'Id': redico_id.group(1) }


# def get_propId(request):
#     url = request.get_full_path()
#     prop_id = re.match(".*redico\/\d*\/proposition\/(\d*)", url)
#     # return {'get_propId': 1}
#     if prop_id:
#         return {'get_propId': prop_id.group(1) }
#     else:
#         return {'get_propId': 11111 }


from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_current_users(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    # return User.objects.filter(id__in=user_id_list).values_list('username', flat=True)
    lst = User.objects.filter(id__in=user_id_list).values_list('username', flat=True)
    return {'get_current_users':User.objects.filter(id__in=user_id_list).values_list('username', flat=True)}
