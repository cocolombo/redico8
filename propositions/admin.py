from django.contrib import admin
# -*- coding: latin-1 -*-
from django.contrib import admin
from propositions.models import Proposition

from django.contrib import admin

# Register your models here.
# -*- coding: latin-1 -*-
from django.contrib import admin
from propositions.models import Proposition # 1.3
#from redico.evaluations.models import Evaluation

#class EvalInline(admin.TabularInline):
#    model = Evaluation
#    extra = 1


class PropositionAdmin(admin.ModelAdmin):

    list_display   = ('texte', 'red', 'auteur', 'date_de_pub', )
    list_filter    = ('auteur', )
    ordering       = ('-redico', 'auteur',)
    #search_fields  = ('texte',  'auteur',)
    date_hierarchy = 'date_de_pub'

    #fieldsets = [
    #    ('Identification',                {'fields': [ 'redico']}),
    #    ('texte de votre proposition',    {'fields': ['texte']}),
    #    ('Optionel',                      {'classes': ('collapse',),  \
    #                                       'fields' : ['preambule']}),
    #]
    #inlines = [EvalInline]
    #actions = ['prop_action']
    #def prop_action(self, request, queryset):
    #    self.message_user(request, "Action sur model prop")

    def red(self, obj):
        return obj.redico.titre
'''
    def minEval(self):
        p = Proposition.objects.latest().order_by(eval)
        return p

    def maxEval(self):
        p = Proposition.objects.all().order_by(eval)
        return p
'''

admin.site.register(Proposition, PropositionAdmin)