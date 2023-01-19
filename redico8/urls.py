"""redico6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from redicos.views import RedicosIndexView, RedicoDetailsView, RedicoAjoutView, RedicoSupprimeView, RedicoEditTitreView
from joueurs.views import DetailsJoueurView, IndexJoueursView
from joueurs.views import DetailsJoueurView, IndexJoueursView
from propositions.views import PropositionDetailsView, PropositionAjoutView, PropositionEditView, PropositionSupprimeView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from evaluations.views import  EvaluationEditView, EvaluationAjoutView, EvaluationDetailsView
from registration.views import RegistrationView

urlpatterns = [
    path('admin/',           admin.site.urls),
    # path('accounts/password_change/', ChangePasswordView.as_view(template_name='registration/password_change_form.html'),
    #      name='changer-mdp'),

    path('accounts/',         include('registration.backends.default.urls')),
    path('chat/',             include('chat.urls')),

    # path('login/',           LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'),
    #                                                                 name='login'),
    # path('password_reset/',  PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
    #                                                                 name='auth_password_reset'),
    # path('logout/',          LogoutView.as_view(template_name='registration/logout.html'),
    #                                                                 name='logout'),

    # path('senregistrer/',    RegistrationView.as_view(redirect_authenticated_user=True, template_name='registration/registration_form.html'),
    #                                                                 name='senregistrer'),


    # REDICO
    path('',                 RedicosIndexView.as_view(),             name='redicos-index'),
    # path('index/',         IndexRedicoView.as_view(),             name='redicos-index'),
    path('redicos/',         RedicosIndexView.as_view(),             name='redicos-index'),
    path('redico/<int:pk>/', RedicoDetailsView.as_view(),           name='redico-details'),
    path('redico/ajout/',    RedicoAjoutView.as_view(),             name='redico-ajout'),
    path('redico/<int:pk>/supprime/',
                             RedicoSupprimeView.as_view(),          name='redico-supprime'),
    path('redico/<int:pk>/edit/', RedicoEditTitreView.as_view(),    name='redico-edit-titre'),




    # JOUEURS
    path('joueurs/',         IndexJoueursView.as_view(),            name='joueurs-index'),
    path('joueur/<int:pk>',  DetailsJoueurView.as_view(),           name='joueur-details'),


    # PROPOSITIONs
    path('redico/<int:redico_id>/proposition/<int:sequence_id>/',
                             PropositionDetailsView.as_view(),      name='proposition-details'),

    # PROPOSITON AJOUT
    # path('/efface/', CourseDeleteView.as_view(), name='courses-efface'),
    path('redico/<int:pk>/proposition/ajout/',
                             PropositionAjoutView.as_view(),        name='proposition-ajout'),

    # PROPOSITON SUPPRIME
    # http://127.0.0.1:8008/redico/1/proposition/2/supprime/
    path('redico/<int:red_id>/proposition/<int:sequence_id>/supprime/',
                             PropositionSupprimeView.as_view(),      name='proposition-supprime'),

    # PROPOSITON EDIT
    # path('/efface/', CourseDeleteView.as_view(), name='courses-efface'),
    path('redico/<int:red_id>/proposition/<int:sequence_id>/edit/',
                             PropositionEditView.as_view(),         name='proposition-edit'),

    # EVALUATIONS
    path('redico/<int:red_id>/proposition/<int:sequence_id>/evaluation/ajout/',
                             EvaluationAjoutView.as_view(),          name='evaluation-ajout'),


    # MODIFIER ÉVALUATION DE CETTE PROPOSITION
    path('redico/<int:red_id>/proposition/<int:sequence_id>/evaluation/edit/',
                             EvaluationEditView.as_view(),           name='evaluation-edit'),

    # DETAILS DES ÉVALUATIONS DE CETTE PROPOSITION
    path('redico/<int:red_id>/proposition/<int:sequence_id>/evaluation/<int:auteur_id>/details/',
                             EvaluationDetailsView.as_view(),           name='evaluation-details'),

    path('chat', include('chat.urls'))
]
