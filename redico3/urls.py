""" redico3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

# import settings
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from joueurs import views as joueurs_views
from redicos import views as redicos_views
from propositions import views as prop_views
# from stats.views import show_stats
from evaluations import views as eval_views
# from heatmap.views import heatmap2
# from accounts.forms import PasswordResetForme


urlpatterns = [
    re_path('admin/',       admin.site.urls),


    re_path('^$',           redicos_views.RedicosIndexView.as_view(), name='redicos-index'),
    re_path('index',        redicos_views.RedicosIndexView.as_view(), name='redicos-index'),

    re_path(r'home',        TemplateView.as_view(template_name='home.html'),
                            name='home'),


    # REGISTER
    re_path(r'register/', account_views.register,
            name='register'),
    # ACTIVATE
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]*)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,50})/$',
            account_views.activate, name='activate'),

    re_path(r'login/',      account_views.login_user,
                            name='login'),

    re_path(r'login2/',     auth_views.LoginView.as_view(template_name='registration/login.html'),
                            name='login2'),

    re_path('logout/',      account_views.logout_user,
                            name='logout'),


    re_path('activate/<slug:uidb64>/<slug:token>/',
             account_views.activate, name='activate'),
    # Change = ancien mdp est commt


    re_path(r'changer_mdp/',    account_views.password_change,
                                name='changer-mdp'),
    re_path(r'changer_mdp_ok/',
                                account_views.password_change_ok,
                                name='changer-mdp-ok'),



    re_path('mdp_oublie/',      auth_views.PasswordResetView.as_view(),
                                 name='mdp_oublie'),


    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
                                name='password_reset_done'),


    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,50})/$',
                                auth_views.PasswordResetConfirmView.as_view(),
                                name='password_reset_confirm'),



    re_path(r'^reset/done/$',   auth_views.PasswordResetCompleteView.as_view(),
                                    name='password_reset_complete'),



    re_path(r'^comment_jouer',      TemplateView.as_view(template_name='comment_jouer.html')),

    # re_path(r'^base3', TemplateView.as_view(template_name='base3.html')),
    # re_path(r'^base4', TemplateView.as_view(template_name='base4.html')),



    # Reset = ancien mdp oublié
    re_path(r'^reinitialiser_mdp/$', auth_views.PasswordResetView.as_view(),
                            name='reinitialiser-mdp'),

    # http://127.0.0.1:8000/redico/11/statsdetail/
    # re_path(r'^redico/(?P<redico_id>\d+)/statsdetail/$',
    #                         redicos_views.statsdetail,
    #                         name='stats-detail'),

    # REDICO INDEX
    re_path(r'^redicos/$',  redicos_views.RedicosIndexView.as_view(),
                            name='redicos-index'),

    # REDICO DETAIL
    # redico/111/
    re_path(r'^redico/(?P<redico_id>\d+)/$',
                            redicos_views.RedicoDetailsView.as_view(),
                            name='redico-details'),
    # REDICO AJOUT
    re_path(r'^redico/ajout/$',
                            redicos_views.RedicoAjoutView.as_view(),
                            name='redico-ajout'),  # http://127.0.0.1:8000/redicos/ajout
    # http://127.0.0.1:8000/redico/11/edit/

    # REDICO SUPPRIME
    # re_path(r'^redico/efface/(?P<redico_id>\d+)/$', redicos_views.EffacerView.as_view(), name='redico-efface'),
    re_path(r'^redico/(?P<redico_id>\d+)/supprime/$',
                            redicos_views.RedicoSupprimeView.as_view(),
                            name='redico-supprime'),
    # REDICO EDIT
    re_path(r'^redico/(?P<redico_id>\d+)/edit/$',
                            redicos_views.RedicoEditTitreView.as_view(),
                            name='redico-edit'),  # http://127.0.0.1:8000/redicos/edit/11

    # path('/efface/', CourseDeleteView.as_view(), name='courses-efface'),
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/ajout/$',  # Pas de sequence_id -> ajout
                                    prop_views.ajoutProp, name='proposition-ajout'),

    # PROPOSITION DETAIL
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/$',
                            prop_views.detail,
                            name='proposition-detail'),

    # PROPOSITON AJOUT
    # path('/efface/', CourseDeleteView.as_view(), name='courses-efface'),
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/ajout/$',
                            prop_views.ajoutProp,
                            name='proposition-ajout'),

    # PROPOSITION EDIT
    # redico/1/proposition/1/edit
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/edit/$',
                            prop_views.editProp,
                            name='proposition-edit'),

    # PROPOSITION SUPPRIMER
    # redico/1/proposition/1/supprime
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/supprime/$',
                            prop_views.supprimeProp,
                            name='proposition-supprime'),

    # JOUEURS INDEX
    re_path(r'^joueurs/$',  joueurs_views.JoueursIndexView.as_view(),
                            name='joueurs-index'),
    # JOUEUR DETAIL
    re_path(r'^joueur/(?P<joueur_id>\d+)/$',
                            joueurs_views.JoueurDetailsView.as_view(),
                            name='joueur-detail'),

    # http://127.0.0.1:8000/heatmap/11/proposition/1/
    # re_path(r'^heatmap/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/$',
    #                         heatmap_views.heatmap,
    #                         name='heatmap'),
    # # Heatmap
    # # http://127.0.0.1:8000/heatmap/11/1/
    # re_path(r'^heatmap/(?P<redico_id>\d+)/(?P<sequence_id>\d+)', heatmap_views.heatmap),
    # # re_path('chat/', include('chat.urls')),


    # EVALUATION AJOUT
    #   Ajout
    # http://127.0.0.1:8000/redico/1/proposition/1/evaluation/ajout/
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/evaluation/ajout/$',
            eval_views.ajout, name='evaluation-ajout'),
    #   EVALUATION EDIT
    # redico/1/proposition/1/evaluation/edit/
    re_path(r'^redico/(?P<redico_id>\d+)/proposition/(?P<sequence_id>\d+)/evaluation/edit/$',
            eval_views.edit, name='evaluation-edit'),
]
# ]
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()