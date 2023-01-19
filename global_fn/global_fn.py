# from redicos.models import Redico
# from propositions.models import Proposition
# from evaluations.models import Evaluation
# from __future__ import annotations
# from django.contrib.auth import get_user_model
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
# from joueurs.models import Joueur


def get_Redico(red_id: int):
    from redicos.models import Redico
    return Redico.objects.get(pk=red_id)

def get_Proposition(red_id: int, seq_id: int):
    from propositions.models import Proposition
    return Proposition.objects.get(redico_id=red_id, sequence=seq_id)


def get_Evaluation(red_id: int, seq_id: int, auteur_id: int):
    from evaluations.models import Evaluation
    return Evaluation.objects.get(proposition_id=get_Proposition(red_id, seq_id).id, auteur_id=auteur_id)
