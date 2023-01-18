from django.contrib import admin
from evaluations.models import Evaluation
# Register your models here.

class EvaluationAdmin(admin.ModelAdmin):
    fields = ('prop', 'joueur', 'eval', 'date_eval')
    list_display = ('prop', 'joueur', 'eval', 'date_eval')
    #    list_filter    = ('joueur', 'redico', 'prop_Courte', )
    # list_filter    = ('joueur', 'prop__redico', )
    list_filter = ('joueur',)
    ordering = ('proposition', 'date_eval',)
    date_hierarchy = 'date_eval'

    # fieldsets = [
    #    ('Identification',                   {'fields': ['proposition']}),
    #    ('Evaluation de cette proposition',  {'fields': ['eval', 'joueur']}),
    #    ('Optionel',                         {'classes': ('collapse',),  'fields' : ['commentaire']}),
    #    ]

    actions = ['eval_action']

    def eval_action(self, request, queryset):
        self.message_user(request, "Action sur model eval")
    def prop_Courte(self, obj):
        return ("%s" % obj.proposition.texte[:15])
    def prop(self, obj):
        return ("%s" % obj.proposition.texte)
    def red(self, obj):
        return obj.proposition.redico.id

admin.site.register(Evaluation, EvaluationAdmin)