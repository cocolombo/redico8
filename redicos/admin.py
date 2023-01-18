from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from redicos.models import Redico
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#class PropChoiceInline(admin.StackedInline):
#    model = Proposition
#    extra = 6
class RedicoAdmin(admin.ModelAdmin):
    list_display   = ('titre', 'createur', 'debut', 'actif', )
    list_filter    = ('createur', )
    ordering       = ('-debut',)
    #search_fields  = ('texte',  'auteur',)
    date_hierarchy = 'debut'


admin.site.register(Redico, RedicoAdmin)


from django.contrib import admin

# Register your models here.
