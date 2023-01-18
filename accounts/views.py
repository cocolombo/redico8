
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash, authenticate, logout, login
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import UserCreationForme, AuthenticationForme, PasswordChangeForme
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.models import User

# REGISTER
def register(request):
    if request.method == 'POST':
        # En cliquant sur le bouton "Confirmer" de la
        # forme tu aboutis ici
        form = UserCreationForme(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation de votre compte'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Vous n'êtes pas encore inscrit. "
                                      "Pour activer votre compte, cliquez sur le "
                                      "lien envoyé à votre adresse de courriel")

            return redirect('redicos-index')

    else:   # En cliquant sur S'emregistrer tu arrives isi
        form = UserCreationForme()
    return render(request, 'accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        context = {'uidb64':uidb64, 'token':token}
        # return render(request, 'accounts/acc_active_email.html', context)
        messages.success(request, 'Inscription complétée et vous êtes maintenant connecté')
        return redirect('redicos-index') #render(request, 'redico', context)
    else:
        messages.error(request, "Une erreur s'est produite, votre inscription a échouée")
        return redirect('redicos-index') #HttpResponse('accounts/acc_active_email_invalid.html')

# @anonymous_required
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForme(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print(f'user: {user}')
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Session ouverte, {username} vous pouvez participer aux Redicos')
                return redirect('redicos-index')
        else:
            messages.error(request, 'La combinaison Usager/MDP est inconnue. Veuillez réessayer')
            return redirect('login')
    else:
        form = AuthenticationForme()
    return render(request, 'registration/login.html', {
                            'form': form})

@login_required
def logout_user(request):
    print('logout')
    user = request.user
    logout(request)
    messages.success(request, (f'{user} votre session vient de prendre fin...'))
    return redirect('redicos-index')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForme(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a été changé')

            return redirect('redicos-index')
        else:
            messages.error(request, 'Veuillez corriger les erreurs.')
    else:
        form = PasswordChangeForme(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })

def password_change_ok(request):
    return render(request, 'registration/password_change_ok.html', {})


# from django.urls import reverse
# def password_reset_view(request):
#     return PasswordResetView(
#         template_name='registration/password_reset_form.html',
#         email_template_name='/registration/password_reset_email.html',
#         subject_template_name='changeMe',
#         post_reset_redirect=reverse('changer-mdp-ok'),
#         password_reset_form=PasswordResetForme)

# class ResetPasswordRequestView(FormView):
#     template_name = "registration/password_reset/password_reset_form.html"
#     success_url = '/account/login'
#     form_class = PasswordResetRequestForm
#
#     def form_valid(self, *args, **kwargs):
#         form = super(ResetPasswordRequestView, self).form_valid(*args, **kwargs)
#         data = form.cleaned_data["email_or_username"]
#         user = User.objects.filter(Q(email=data) | Q(username=data)).first()
#         if user:
#             c = {
#                 'email': user.email,
#                 'domain': self.request.META['HTTP_HOST'],
#                 'site_name': 'your site',
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'user': user,
#                 'token': default_token_generator.make_token(user),
#                 'protocol': self.request.scheme,
#             }
#             email_template_name = 'registration/password_reset/password_reset_email.html'
#             subject = "Reset Your Password"
#             email = loader.render_to_string(email_template_name, c)
#             send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
#         messages.success(self.request, 'An email has been sent to ' + data + " if it is a valid user.")
#         return form

    #     if request.method == 'POST':
    #     form = PasswordResetForme(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)  # Important!
    #         messages.success(request, 'Votre mot de passe a été changé')
    #
    #         return redirect('redicos-index')
    #     else:
    #         messages.error(request, 'Veuillez corriger les erreurs.')
    # else:
    #     form = PasswordResetForme(request.user)
    # return render(request, 'registration/password_reset_form.html', {
    #     'form': form
    # })


def home(request):
    return render(request, 'joueurs/index.html', {})
















# def register_user(request)user_authenticate():
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username  = form.cleaned_data['username']
#             password1 = form.cleaned_data['password1']
#             # password2 = form.cleaned_data['password2']
#             user = authenticate(username=username, password=password1)
#             login(request, user)
#             messages.success(request, (f'Bienvenue {username} vous vous ètes bien enregistré. '))
#             return redirect('joueurs-index')
#     else:
#         form = SignUpForm()
#     context = {'form': form}
#     return render(request, 'registration/register.html', context)

# def register_user(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             usernuser_authenticateame  = form.cleaned_data['username']
#             password1 = form.cleaned_data['password1']
#             # password2 = form.cleaned_data['password2']
#             user = authenticate(username=username, password=password1)
#             login(request, user)
#             messages.success(request, (f'{username} vous vous ètes bien enregistré. '))
#             return redirect('joueurs-index')
#     else:
#         form = SignUpForm()
#     context = {'form': form}
#     return render(request, 'registration/register.html', context)


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         context = {'uidb64':uidb64, 'token':token}
#         return render(request, 'accounts/acc_active_email.html', context)
#     else:
#         return HttpResponse('accounts/acc_active_email_invalid.html')



