from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import F
"""
 the Meta class is used to provide additional options for a model. 
 One of the options that can be set is proxy = True, which indicates 
 that the model should be used as a proxy for another model. 
 This means that the proxy model will share the same database table 
 as the original model, but can have different fields, methods, 
 or other behavior. 

"""
class Joueur(User):
    class Meta:
        proxy = True
        ordering = ('-id', )
    def __str__(self) -> str:
        return f"{self.username}"

    def redsAuteurList(self):
        from redicos.models import Redico
        return Redico.objects.filter(createur=self.id).\
                              values(RedId=F('proposition__redico__id'),
                                     RedCreateur=F('proposition__redico__createur'),
                                     RedTitre=F('proposition__redico__titre'),
                                     RedDate=F('proposition__redico__debut')).distinct()
    def redsParticipantsList(self):
        from evaluations.models import Evaluation
        l1  = Evaluation.objects.filter(joueur=self.id). \
                            values(RedId=F('proposition__redico__id'),
                                   RedCreateur=F('proposition__redico__createur'),
                                   RedTitre=F('proposition__redico__titre'),
                                   RedDate=F('proposition__redico__debut')).distinct()
        l2 = self.redsAuteurList()
        return l1.difference(l2)

                                                         # 'proposition__redico__titre').\
                                                         # distinct().\
                                                         # order_by('proposition__redico')
    # [i[0] for i in e]
    def redsAuteurNb(self):
        from redicos.models import Redico
        return Redico.objects.filter(createur=self.id).count()
    def redsParticipantsNb(self):
        from evaluations.models import Evaluation
        return Evaluation.objects.filter(joueur_id=self.id).values('proposition__redico__id',
                                                           'proposition__redico__titre').distinct().count()-1
    def get_username(self) -> str:
        return f"{self.username}"

    def get_absolute_url(self) -> str:
        """
        Used to define the URL for an object. It is often used for the detail view of an object
        Returns a string that represents the URL for the object, and it's often used by the
        Django's reverse function to automatically generate URLs for the object.
        You might define a get_absolute_url method on a Book model that returns
        the URL for the detail view of a book, such as "/books/1/".
        """
        return f"/joueur/{self.id}" # "/joueur/%i/" % self.id

