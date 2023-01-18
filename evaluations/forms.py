# from django.forms import ModelForm, Textarea
# from evaluations.models import Evaluation
# from django.forms.widgets import NumberInput
# import floppyforms as forms

# class RangeInput(NumberInput):
#     input_type = 'range'
#
# class EvaluationForm(ModelForm):
#     class Meta:
#         model = Evaluation
#         fields = ('eval', 'commentaire')
#         widgets = {
#             'eval': RangeInput(attrs={'max': 100,
#             'min':0,
#             'step':5}),
#             'commentaire': Textarea(attrs={'cols': 40, 'rows': 4}),
#         }
#
#         # fieldsets = [('Optionel',  {'classes': ('collapse',),
#         #                            'fields' : ['commentaire']})],


from django.forms import ModelForm, Textarea
from evaluations.models import Evaluation


class EvaluationAjoutEditForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ('eval', 'commentaire')

        widgets = {
            'commentaire': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(EvaluationAjoutEditForm, self).__init__(*args, **kwargs)
        self.fields['commentaire'].widget.attrs['class'] = 'form-group'
        self.fields['commentaire'].widget.attrs['placeholder'] = 'Votre commentaire (facultatif)'
        self.fields['commentaire'].label = ''
        # self.fields['titre'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['commentaire'].help_text = ''
