from django.forms import ModelForm, Textarea
from redicos.models import Redico

class RedicoAjoutForm(ModelForm):
    class Meta:
        model = Redico
        fields  = ('titre',) # 'debut')

        widgets = {
            'titre': Textarea(attrs={'cols': 30, 'rows': 5}), }

    def __init__(self, *args, **kwargs):
        super(RedicoAjoutForm, self).__init__(*args, **kwargs)
        self.fields['titre'].widget.attrs['class'] = 'form-group'
        self.fields['titre'].widget.attrs['placeholder'] = 'Entrez le titre de votre Redico'
        self.fields['titre'].label = ''
        # self.fields['titre'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['titre'].help_text = ''