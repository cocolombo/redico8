from __future__ import annotations
import base64
import io
import urllib.parse
from django.db.models.query import QuerySet
from django.db.models import F, Q
import statistics
import pandas as pd
import matplotlib.pyplot as plt

from evaluations.models import Evaluation
from django.contrib.auth.models import User
# from redicos.models import Redico
# from typing import TYPE_CHECKING
# from django.db import migrations, models
# if TYPE_CHECKING:
from propositions.models import Proposition

# The recommended way is to create a new model
# and give it a OneToOneField() with the built-in User
# https://stackoverflow.com/questions/2886987/adding-custom-fields-to-users-in-django
# Then you can access the fields like this:
# user = User.objects.get(username='jsmith')
# college = user.student.college

# class JoueurAccepteCourriel(models.Model):
#     joueur = models.OneToOneField(User, on_delete=models.CASCADE)         #models.OneToOneField(User, on_delete=models.CASCADE)
#     accepte_courriel = models.BooleanField(default=False, null=True)
#
#     def __str__(self):
#         return self.joueur.username

# AJOUT D'UN CHAMP À USER
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Un modèle pour stocker des informations supplémentaires sur un utilisateur.
    Champ avertir_par_courriel
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    courrielOK = models.BooleanField(default=False, null=True)

    # def __str__(self):
    #     return f""" Username: {self.user.username} - Courriel OK: {self.courrielOK} """

class Joueur(User):
    """
    Voir: # https://stackoverflow.com/questions/36317816/relatedobjectdoesnotexist-user-has-no-userprofile
    """
    class Meta:
        proxy = True
        ordering = ('-id', )

    def __str__(self):
        return f""" id: {self.id} - username: {self.username} - Courriel OK: {self.profile.courrielOK} """

    def __repr__(self):
        return f"\n    Class:           {self.__class__.__name__} " \
               f"\n    id:              {self.id}  " \
               f"\n    username:        {self.username}  " \
               f"\n    is_courriel_ok:  {self.profile.courrielOK}  "

    def username(self) -> str:
        return self.username

    def toggle_courriel_ok(self) -> bool:
        """
        Passer de courriel OK à non OK et vice-versa
        """
        self.profile = UserProfile.objects.get(user_id=self.id)
        # Inverser le choix
        self.profile.courrielOK = not self.profile.courrielOK
        UserProfile.objects.filter(user_id=self.id).update(courrielOK=self.profile.courrielOK)
        return self.profile.courrielOK

    # Redicos
    def AuteurDeCesRedicos(self)  -> QuerySet[Redico]:
        """
        Liste des redicos dont self est l'auteur
        """
        reds = Redico.objects.filter(auteur_id=self.id, actif=True)
        return reds.values('id', 'titre')
        # return Redico.objects.filter(auteur_id=self.id) \
        #                      .values(red_id=F('proposition__redico__id'),
        #                             red_auteur=F('proposition__redico__auteur'),
        #                             red_titre=F('proposition__redico__titre'),
        #                             red_date=F('proposition__redico__debut')).distinct()

    def ParticipeACesRedicos(self) -> QuerySet[Redico]:
        """
        Liste des redicos dont self est participant
        ParticipeACesRedicos = TousDontilEstParticipant  - AuteurDeCesRedicos
        """
        # Tous
        reds = Redico.objects.filter(actif=True)
        # Tous ou il participe
        reds = reds.filter(Q(proposition__auteur=self.id)).distinct()
        # Moins ceux dont il est le createur
        reds = reds.filter(~Q(auteur=self.id))
        return reds

    # # Props
    # def trop_de_props_consecutives(self, red: Redico) -> bool:
    #     """
    #     Calcule ne nombre de propositions consécutives dans un redico par self
    #     Retourne True si 5 ou plus
    #     Retourne False si moins de 5
    #     Cette fonction sert dans le cas où on voudrait limiter le nombre de propositions
    #     """
    #     def previous_proposition(prop: Proposition):
    #         """ Return prevoius proposition in the same redico  """
    #         return Proposition.objects.get(redico=prop.redico, sequence=prop.sequence - 1)
    #
    #     max_sequence = red.max_sequence()
    #     prop_courante = Proposition.objects.get(redico=red, sequence=max_sequence)
    #     # Vérifier les 5 prop_precedentes et si l'auteur n'est pas le même
    #     # que pour la prop_courante retourner False
    #     for i in range(5):
    #         prop_precedente = previous_proposition(prop_courante)
    #         if prop_precedente.auteur != self.id:  # prop_courante.auteur:
    #             return False
    #         prop_courante = prop_precedente
    #     return True

    def trop_de_props_consecutives(self, red: Redico) -> bool:
        """
        Calcule ne nombre de propositions consécutives dans un redico par self
        Retourne True si 5 ou plus
        Retourne False si moins de 5
        Cette fonction sert dans le cas où on voudrait limiter le nombre de propositions
        """
        def previous_proposition(prop: Proposition):
            """ Return prevoius proposition in the same redico  """
            return Proposition.objects.get(redico=prop.redico, sequence=prop.sequence - 1)

        # propPrecedente = prop_courante.precedente
        if red.max_sequence() < 5:
            return False

        prop_courante = Proposition.objects.get(redico=red, sequence=red.max_sequence())

        for count in range(prop_courante.sequence, prop_courante.sequence - 5, -1):
            prop_precedente = previous_proposition(prop_courante)
            # print(f"""prop_courante.auteur: {prop_courante}""")
            # print(f"""prop_precedente.auteur: {prop_precedente}""")
            # if prop_courante.auteur != prop_precedente.auteur:
            if self.id != prop_precedente.auteur_id:
                print(f""" Différent:  : {self} - {prop_precedente.auteur_id} """)
                return False
            else:
                print(f""" Pareil:  : {self} - {prop_precedente.auteur_id} """)
                prop_courante = prop_precedente
        return True

    def AuteurDeCesPropositions(self) -> QuerySet[Proposition]:
        """
        Liste des propositions dont self est l'auteur
        """
        return Proposition.objects.filter(auteur=self.id).values()

    # Evaluations
    def AuteurDeCesEvaluations(self) -> QuerySet[Evaluation]:
        """
        Liste des evaluations dont self est l'auteur et qui n'est pas une abstention
        """
        return Evaluation.objects.filter(auteur=self.id).values()

    # int
    def RedicosParticipant_nb(self) -> int:
        """
        Calcul du nombre de redicos dont self est participant
        """
        return len(self.ParticipeACesRedicos())  + len(self.AuteurDeCesRedicos())
    def AuteurDeCesEvaluations_nb(self) -> int:
        """
        Calcul du nombre d'evaluations dont self est l'auteur
        """
        return len(self.AuteurDeCesEvaluations())
    def Abstentions_nb(self) -> int:
        """
        Calcul du nombre d'évaluation ou self a donné une abstention
        """
        return len([x['eval'] for x in self.AuteurDeCesEvaluations() if x['eval'] == -1])

    # Pourcentages
    def Abstentions_Pourcentage(self) -> float:
        """
        Le pourcentage d'abstentions données par self
        """
        return (self.AuteurDeCesEvaluations_nb()/self.Abstentions_nb()) * 100
    def meanEvals(self) -> float:
        """
        Calcul de la moyenne des évaluations données par self
        """
        evals =  [x['eval'] for x in self.AuteurDeCesEvaluations()]
        return statistics.mean(evals)
        # return statistics.mean(list(Evaluation.objects.filter(joueur=self.id).values_list('eval', flat=True)))

    def histoEvals(self) -> str:
        """
        Histogramme des évaluations du joueur
        """
        from matplotlib.patches import Rectangle
        buf = None
        ev = list(Evaluation.objects.filter(auteur=self.id).values_list('eval', flat=True))
        data = pd.Series(ev)
        plt.gca().cla()
        ax = data.plot.hist(bins=10, alpha=0.5)
        # Avec transAxes les coordonnées vont de 0,0 à 1,1
        plt.text(0.4, 0.5, self.datadescribe(),transform=ax.transAxes )
        # plt.legend(handles, labels)
        plt.plot()
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        # plt.show()
        return uri

    def datadescribe(self)-> pd.Series[str]:
        # ev = list(Evaluation.objects.filter(auteur=self.id).values_list('eval', flat=True))
        ev = list(Evaluation.objects.filter(Q(auteur=self.id) & ~Q(eval=-1)).values_list('eval', flat=True))
        data = pd.Series(ev)
        # print(data.describe())
        return data.describe().loc[['count', 'mean']].round(1).to_string()



"""
    # [i[0] for i in e]
    # def redsAuteurDe_nb(self) -> int:
    #     return len(self.AuteurDe())
    # def redsParticipeA_nb(self) -> int:
    #     return len(self.ParticipeA())
    
    # def propsAuteurDe_nb(self) -> int:
    #     return len(self.propsAuteurDe())
    # Evals  

    # def evalsAuteurDe_nb(self) -> int:
    #     return len(self.propsAuteurDe())
"""