from django.contrib.auth.forms import   UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
                                        # PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, Textarea

from django import forms

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


# class PasswordResetForme(forms.Form):
#     class Meta:
#         model = User
#         fields = ('email',)
#     def __init__(self, *args, **kwargs):
#         super(PasswordResetForme, self).__init__(*args, **kwargs)
#
#         self.fields['email'].widget.attrs['class'] = 'form-group'
#         self.fields['email'].widget.attrs['placeholder'] = 'Courrrrriel'
#         self.fields['email'].label = ''
#         # self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
#         self.fields['email'].help_text = ''


class UserChangeForme(UserChangeForm):  # Edit Profile
    password = forms.CharField(label="",  widget=forms.TextInput(attrs={'type':'hidden'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class UserCreationForme(UserCreationForm):
    # email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), )
    # first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    # last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UserCreationForme, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-group'
        self.fields['username'].widget.attrs['placeholder'] = 'Nom/Alias'
        self.fields['username'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['username'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'form-group'
        self.fields['email'].widget.attrs['placeholder'] = 'Courriel'
        self.fields['email'].label = ''
        # self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['email'].help_text = ''


        self.fields['password1'].widget.attrs['class'] = 'form-group'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password1'].label = ''
        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-group'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmer le mot de passe'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
        # self.fields['password2'].help_text = ''

class AuthenticationForme(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

        widgets = {
            'username': Textarea(attrs={'cols': 40, 'rows': 1}),
            # 'password': (attrs={'cols': 40, 'rows': 1}),
        }


    def __init__(self, *args, **kwargs):
        super(AuthenticationForme, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-group'
        self.fields['username'].widget.attrs['placeholder'] = 'Nom/Alias'
        self.fields['username'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['username'].help_text = ''

        self.fields['password'].widget.attrs['class'] = 'form-group'
        self.fields['password'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password'].label = ''
        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password'].help_text = ''

class PasswordChangeForme(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2', )

        widgets = {
            'old_password': Textarea(attrs={'cols': 40, 'rows': 1}),
            # 'password': (attrs={'cols': 40, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForme, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-group'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Ancien mdp'
        self.fields['old_password'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['old_password'].help_text = ''

        self.fields['new_password1'].widget.attrs['class'] = 'form-group'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nouveau mdp'
        self.fields['new_password1'].label = ''
        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].widget.attrs['class'] = 'form-group'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Nouveau mdp (bis)'
        self.fields['new_password2'].label = ''
        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
