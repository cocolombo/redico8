from django.shortcuts import render

# Create your views here.
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView
from joueurs.models import Joueur
from django.contrib.auth.models import User
from django.db.models import Q #, F

class JoueurDetailsView(DetailView):
    """
    Détails des activités d'un joueur
    """
    model = Joueur
    template_name = 'joueurs/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        joueur = self.object
        context["joueur"] = joueur
        return context


class JoueursIndexView(ListView):
    """
    Liste des joueurs inscrit dans le site
    """
    model = Joueur
    template_name = 'joueurs/index.html'
    ordering = '-pk'

    def get_queryset(self):
        qs = Joueur.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        joueurs = context['object_list']
        context["joueurs"] = joueurs
        return context


"""
class DetailsJoueurView(DetailView):
    model = Joueur
    template_name = 'joueurs/joueur-details.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['joueur'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
        
class IndexJoueursView(ListView):
    model = Joueur
    template_name = 'joueurs/joueurs-index.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            joueurs = self.object_list  #Joueur.objects.filter(actif=True).order_by('-id')
            context['joueurs'] = joueurs
            # print(context['joueurs'])
            return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.filter(is_active=True).order_by('-id')
        # Enlever admin de la liste des joueurs affichée
        qs = qs.filter(~Q(username='admin'))
        # print(qs)
        return qs               # self.object_lidt = q

       	
"""