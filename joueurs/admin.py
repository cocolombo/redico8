from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from joueurs.models import Joueur
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#class PropChoiceInline(admin.StackedInline):
#    model = Proposition
#    extra = 6
class JoueurAdmin(UserAdmin):
    ordering = ['-date_joined']
    list_display = ('username', 'email', 'date_joined')
admin.site.register(Joueur, JoueurAdmin)
