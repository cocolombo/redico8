from django.forms import ModelForm, Textarea
from propositions.models import Proposition

class PropositionAjoutEditForm(ModelForm):
    class Meta:
        model = Proposition
        fields = ('preambule', 'texte', 'lien', ) # 'redico', 'proposition')
        widgets = {
          'texte'     : Textarea(attrs={'cols': 70, 'rows': 8}),
          'preambule' : Textarea(attrs={'cols': 70, 'rows': 8}),
          'lien'      : Textarea(attrs={'cols': 70, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(PropositionAjoutEditForm, self).__init__(*args, **kwargs)
        self.fields['texte'].widget.attrs['class'] = 'form-group'
        self.fields['texte'].widget.attrs['placeholder'] = 'Le texte (requis)'
        self.fields['texte'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['texte'].help_text = ''

        self.fields['preambule'].widget.attrs['class'] = 'form-group'
        self.fields['preambule'].widget.attrs['placeholder'] = 'Le préambule (facultatif)'
        self.fields['preambule'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['preambule'].help_text = ''

        self.fields['lien'].widget.attrs['class'] = 'form-group'
        self.fields['lien'].widget.attrs['placeholder'] = "Un lien (facultatif)"
        self.fields['lien'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['lien'].help_text = ''




