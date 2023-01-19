from django.shortcuts import render
from redicos.models import Redico
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView, DeleteView
from .forms import RedicoAjoutForm
from django.urls import reverse_lazy
# Create your views here.
from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from global_fn.global_fn import get_Redico, get_Proposition
# from rules.contrib.views import permission_required
# from rules.contrib.views import PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from propositions.models import Proposition
from django.utils.safestring import mark_safe
from propositions.models import Proposition
from django.http import HttpResponseForbidden
###################################################################
# LIST
class RedicosIndexView(ListView):
    model = Redico
    # permission_required = 'is_auteur_du_redico'
    template_name = 'redicos/index.html'
    # def get_queryset(self):
    #     return Redico.objects.all()
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            reds =  self.object_list.order_by('-id')        #Redico.objects.filter(actif=True).order_by('-id')
            context["reds"] = reds
            return context

###################################################################
# AJOUT REDICO
class RedicoAjoutView(LoginRequiredMixin, CreateView):
    model = Redico
    form_class = RedicoAjoutForm
    template_name = 'redicos/redico-ajout.html'
    # queryset = Redico.objects.all()

    def get_success_url(self):
        # Retour à http://127.0.0.1:8008/redico/83/
        return reverse_lazy('redico-details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.auteur = self.request.user
        self.object.save()
        # Insérer la proposition zéro de l'admin
        red = self.object
        red.insert_prop_zero()
        return super().form_valid(form)

# EDITER LE TITRE DU REDICO

#################################################################
# EDIT
class RedicoEditTitreView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    http://127.0.0.1:8008/redico/80/edit
    """
    model = Redico
    template_name = 'redicos/redico-edit-titre.html'
    fields = ['titre']
    success_url = reverse_lazy("redicos-index")

    def test_func(self) -> bool:
        user_id = self.request.user.id
        red = get_Redico(self.kwargs.get("pk"))
        nbProps     = len(red.ses_props())
        if (user_id == red.auteur.id) and (nbProps == 1):
            return True
        else:
            return  False

##################################################################
# DETAILS
class RedicoDetailsView(DetailView):
    model = Redico
    template_name = 'redicos/details.html'

    def get_context_data(self, **kwargs):
            context = super(RedicoDetailsView, self).get_context_data(**kwargs)
            context["red"] = self.object
            return context

###################################################################################################################
# SUPPRIME
class RedicoSupprimeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    http://127.0.0.1:8008/redico/70/supprime/
    """
    model = Redico
    template_name = 'redicos/supprime.html'
    success_url = reverse_lazy("redicos-index")

    def test_func(self):
        red = self.get_object()
        if red.peut_supprimer_redico(self.request.user):
            return True
        return False



    # # S'il n'est pas l'auteur de ce redico, il ne peut effacer
    # def get_object(self, queryset=None):
    #     """
    #     Check the logged in user is the owner of the object or 404
    #     """
    #     obj = super(RedicoSupprimeView, self).get_object(queryset)
    #     if obj.auteur == self.request.user:
    #         return obj
    #     else:
    #         messages.info(self.request, 'Opération interdite sur un objet qu ne vous appartient pas')
    #         return redirect("http://stackoverflow.com/") #('redicos-index')

    # @login_required
    # def edit(request, redico_id=None):
    #     # Redico existe
    #     if redico_id:
    #         red = Redico.objects.get(id=redico_id)
    #         if red.createur != request.user:
    #             return HttpResponseForbidden()
    #     # Redico n'existe pas
    #     else:
    #         red = Redico(createur=request.user)
    #
    #     form = RedicoAjoutEditForm(request.POST or None, instance=red)
    #     # if this is a POST request we need to process the form data
    #     if request.POST and form.is_valid():
    #         form.save()
    #         redirect_url = reverse('redicos-index')
    #         return redirect(redirect_url)
    #         # return HttpResponseRedirect('/redicos')
    #     return render(request, template_name='redicos/edit.html',
    #             context= {
    #                     'form': form,
    #                     'red': red,
    #                     'redico_id': redico_id,

    #             })








